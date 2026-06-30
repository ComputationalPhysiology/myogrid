import numpy as np
from typing import Any, Callable, Dict, Optional, Tuple, Union


class SarcArray2D:
    """
    Class representing a 2D array of connected sarcomeres (myofibrils in parallel, 
    sarcomeres in series) solved as a system of ordinary differential equations.
    """

    def __init__(
        self,
        n_series: int,
        n_fibrils: int,
        model: Any,
        default_ca_func: Callable,
        overlap_func: Callable,
        ca_func_variations: Optional[Dict[Tuple[int, int], Callable]] = None,
    ) -> None:
        """
        Args:
            n_series (int): Number of sarcomeres in series per myofibril.
            n_fibrils (int): Number of parallel myofibrils.
            model (Any): Contraction ODE model module for individual sarcomeres.
            default_ca_func (Callable): Default calcium transient function.
            overlap_func (Callable): Function specifying force-length dependence.
            ca_func_variations (Optional[Dict[Tuple[int, int], Callable]]): 
                Dictionary mapping specific (fibril, series) coordinates to custom calcium functions.
        """
        self.n_series: int = n_series
        self.n_fibrils: int = n_fibrils

        # ODE Model Mappings
        self.loc_rhs: Callable = model.rhs
        self.loc_init_states: Callable = model.init_state_values
        self.loc_init_params: Callable = model.init_parameter_values

        # Vector Dimensions
        self.sn: int = len(self.loc_init_states())
        self.pn: int = len(self.loc_init_params())
        self.stretch_ind: int = model.parameter_indices("applied_stretch")
        self.sl_ind: int = model.state_indices("SL")

        # Physics Indices for Force Extraction
        self.xb_indices: Dict[str, int] = {
            'x_pre': model.state_indices("xXBprer"),
            'x_post': model.state_indices("xXBpostr"),
            'f_pre': model.state_indices("XBprer"),
            'f_post': model.state_indices("XBpostr")
        }
        self.active_force_scale: float = 0.7102777185879678 / 0.007

        self.total_sarcs: int = n_series * n_fibrils
        self.z_start_idx: int = self.total_sarcs * self.sn

        # Store overlap function internally
        self.overlap_func: Callable = overlap_func

        # Setup spatial Calcium functions
        self.ca_funcs: Dict[Tuple[int, int], Callable] = {
            (j, i): default_ca_func for j in range(n_fibrils) for i in range(n_series)
        }

        if ca_func_variations:
            for key, func in ca_func_variations.items():
                self.ca_funcs[key] = func

    def init_state_values(
        self, values: Optional[Dict[Union[Tuple[int, int], str], Dict[str, Any]]] = None
    ) -> np.ndarray:
        """
        Initializes the state variables of all individual sarcomere ODE models.
        """
        values = values or {}
        init = []
        for j in range(self.n_fibrils):
            for i in range(self.n_series):
                state_args = values.get((j, i), values.get("all", {}))
                init.append(self.loc_init_states(**state_args))

        # Append zeros for the z-displacements at the end of the state vector
        return np.concatenate([*init, np.zeros(self.total_sarcs)])

    def init_parameter_values(
        self, values: Optional[Dict[Union[Tuple[int, int], str], Any]] = None
    ) -> np.ndarray:
        """
        Set parameters of all individual sarcomere ODE models.
        """
        values = values or {}
        p = []
        for j in range(self.n_fibrils):
            for i in range(self.n_series):
                param_args = values.get((j, i), values.get("all", {}))
                p.append(self.loc_init_params(**param_args))

        self.k_se: float = values.get("k_se", 1000.0)
        self.k_im: float = values.get("k_im", 1.0)
        self.preload: float = values.get("preload", 0.0)
        
        if "u_app" in values:
            self.preload = self.k_se * values["u_app"]

        return np.array(p).flatten()

    def rhs(
        self,
        t: float,
        states: np.ndarray,
        parameters: np.ndarray,
    ) -> np.ndarray:
        """
        Right-hand side of the global ODE system.
        """
        dy: np.ndarray = np.zeros_like(states)
        n, m, sn, pn = self.n_series, self.n_fibrils, self.sn, self.pn

        # Mechanical Coupling
        current_preload: float = min(self.preload * t / 50.0, self.preload)
        z_displacements: np.ndarray = states[self.z_start_idx :].reshape(m, n)
        f_app: np.ndarray = (-self.k_se * z_displacements[:, -1]) + current_preload

        for j in range(m):
            x = z_displacements[j]
            x_l, x_r = (
                (z_displacements[j - 1] if j > 0 else x),
                (z_displacements[j + 1] if j < m - 1 else x),
            )
            fx: np.ndarray = np.flip(
                np.cumsum(np.flip(-self.k_im * (2 * x - x_l - x_r)))
            )

            for i in range(n):
                s_off, p_off = (j * n * sn + i * sn), (j * n * pn + i * pn)
                s_loc: np.ndarray = states[s_off : s_off + sn]
                p_loc: np.ndarray = parameters[p_off : p_off + pn].copy()
                p_loc[self.stretch_ind] = f_app[j] + fx[i]

                # Pass the dynamically mapped functions to the local model
                dy[s_off : s_off + sn] = self.loc_rhs(
                    s_loc, t, p_loc, self.ca_funcs[(j, i)], self.overlap_func
                )

            # dx/dt (Z-line velocity)
            sl_v: np.ndarray = dy[
                j * n * sn + self.sl_ind : j * n * sn + n * sn + self.sl_ind : sn
            ]
            dy[self.z_start_idx + j * n : self.z_start_idx + (j + 1) * n] = np.cumsum(
                sl_v
            )

        return dy

    # ... inside SarcArray2D class ...

    def simulate(
        self, 
        t_stop: float, 
        init_states: np.ndarray, 
        parameters: tuple, 
        method: str = 'Radau'
    ) -> tuple:

        from scipy.integrate import solve_ivp  # Localized import keeps init fast

        t_span = (0, t_stop)
        t_eval = np.linspace(0, t_stop, int(t_stop * 5))
        
        print(f"Solving ODEs with {method}...")
        sol = solve_ivp(
            fun=self.rhs,            # Notice how it references itself directly now
            t_span=t_span,
            y0=init_states,
            args=parameters,
            t_eval=t_eval,
            method=method,
            rtol=1e-6,
            atol=1e-8
        )
        
        if not sol.success:
            print(f"Warning: Solver failed! {sol.message}")
        else:
            print("Integration complete.")
        
        return sol.t, sol.y.T


    def calculate_max_contraction(self, states: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Finds minimum Sarcomere Length (SL) and maximum active force using 
        vectorized slicing across the array over time.
        """
        total_local_states = self.n_series * self.n_fibrils * self.sn

        # Slicing syntax: [start:stop:step]
        sl_data = states[:, self.sl_ind : total_local_states : self.sn]

        x_pre = states[:, self.xb_indices['x_pre'] : total_local_states : self.sn]
        f_pre = states[:, self.xb_indices['f_pre'] : total_local_states : self.sn]
        x_post = states[:, self.xb_indices['x_post'] : total_local_states : self.sn]
        f_post = states[:, self.xb_indices['f_post'] : total_local_states : self.sn]

        # Calculate force
        active_force = (x_pre * f_pre + x_post * f_post) * self.active_force_scale

        return {
            "min_sl": sl_data.min(axis=0),
            "max_force": active_force.max(axis=0)
        }