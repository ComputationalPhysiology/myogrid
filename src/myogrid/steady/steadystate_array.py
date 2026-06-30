import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton_krylov, NoConvergence
from typing import Callable, Dict, Optional, Tuple, Any

class SarcArray:
    def __init__(
        self,
        overlap: Callable[[np.ndarray], np.ndarray],
        params: Dict[str, float],
        no_myofibrils: int,
        no_serial_sarcs: int,
        mean: float = 1.75,
        sigma: float = 0.15,
        seed: Optional[int] = None,
        mutant_mask: Optional[np.ndarray] = None,
        mutant_scale: float = 1.0  # Default to 1.0 so control arrays remain unaffected
    ) -> None:
        if seed is not None:
            np.random.seed(1)
            
        self.SLset: np.ndarray = np.random.normal(mean, sigma, (no_myofibrils, no_serial_sarcs))
        self.SLrest: np.ndarray = self.SLset
        self.overlap: Callable[[np.ndarray], np.ndarray] = overlap
        self.params: Dict[str, float] = params
        self.mean_init_sl: float = float(np.mean(self.SLset))

        # --- Handle Mutant Scaling ---
        if mutant_mask is None:
            self.mutant_mask = np.zeros_like(self.SLset, dtype=bool)
        else:
            self.mutant_mask = mutant_mask
            
        # Create a fully vectorized float array for fast multiplication in the solver
        self.overlap_scale = np.ones_like(self.SLset, dtype=float)
        self.overlap_scale[self.mutant_mask] = mutant_scale

        # Initial solve with no activation
        SL0, SL, contr, constant, stretch, neighbors = self.solve(
            activation=0.0, preload=0.0
        )

        # Initial solve to define groups at full activation
        SL0, SL, contr, constant, stretch, neighbors = self.solve(
            activation=1.0, preload=0.0
        )
        self.init_contr: np.ndarray = contr
        self.init_non_c: np.ndarray = stretch + constant
        self.init_stretch: np.ndarray = stretch
        self.init_constant: np.ndarray = constant
    # --- Physics & Force Calculation Methods ---

    def passive_force_titin(self, SL: np.ndarray, PExp_t: float = 10.0) -> np.ndarray:
        PCon_t = self.params["PCon_t"]
        p_force = (
            PCon_t * (-1 + np.exp(PExp_t * np.abs(self.SLrest - SL))) * np.sign(SL - self.SLrest)
        )
        return p_force

    def active_force(self, SL: np.ndarray, phi: float, strain_scaling: bool = False) -> np.ndarray:
        # Calculate base overlap, then multiply by our pre-computed scaling array
        o_lap = self.overlap(SL) * self.overlap_scale 
        
        T_ref = self.params["T_ref"]
        SL_rest_ref = 1.75
        alpha = 1.5
        
        sf = alpha * (SL / SL_rest_ref)
        if strain_scaling:
            strain_factor = np.where(sf > 1.0, sf, 1.0)
        else:
            strain_factor = 1.0

        return T_ref * phi * o_lap * strain_factor

    def afterload(self, x: np.ndarray) -> np.ndarray:
        k_se = self.params["k_se"]
        load = x[:, -1] * k_se
        return np.repeat(load, x.shape[1]).reshape(x.shape)

    def z_force(self, x: np.ndarray) -> np.ndarray:
        k_im = self.params["k_im"]
        n_fibs = x.shape[0]
        if n_fibs == 1:
            return np.zeros_like(x)  # Ensured consistent return type
            
        fz = np.zeros_like(x)
        fz[0, :] = -k_im * (x[0, :] - x[1, :])
        for i in range(1, n_fibs - 1):
            fz[i, :] = -k_im * (2 * x[i, :] - x[i - 1, :] - x[i + 1, :])
        fz[n_fibs - 1, :] = -k_im * (x[n_fibs - 1, :] - x[n_fibs - 2, :])
        
        return np.cumsum(fz[:, ::-1], 1)[:, ::-1]

    def calculate_nodal_forces(self, SL: np.ndarray, phi: float, preload: float) -> np.ndarray:
        """Calculates the sum of forces on each sarcomere."""
        x = SL - self.SLset
        x = np.cumsum(x, 1)
        
        F_act = self.active_force(SL, phi)
        F_pas = self.passive_force_titin(SL)
        F_aft = self.afterload(x)
        F_pre = -preload
        F_z = -self.z_force(x)

        return F_act + F_pas + F_aft + F_pre + F_z

    def _compute_force_balance(self, phi: float, SL0_guess: np.ndarray, preload: float) -> np.ndarray:
        """Internal solver for equilibrium force balance."""
        def force_balance(SL: np.ndarray) -> np.ndarray:
            return self.calculate_nodal_forces(SL, phi, preload)

        try:
            solution = newton_krylov(force_balance, SL0_guess, f_tol=1e-4, maxiter=500)
        except NoConvergence as e:
            print("Solver not converged")
            print(e.args)
            exit() 

        return solution

    # --- Simulation Methods ---

    def solve(
        self, activation: float, preload: float
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Solves the force balance equations for equilibrium."""
        
        # First compute stretch without contraction
        SL0 = self._compute_force_balance(0.0, self.SLset, preload)
        print(f"Preload = {preload}, mean stretch = {(np.mean(SL0)/np.mean(self.SLset)-1.0)*100:2.1f}%")

        # Then with contraction
        SL = self._compute_force_balance(activation, self.SLset, preload)

        SL_tol = 20 / 1000  # change < 20 nm is considered constant

        contr = (SL - SL0) < -SL_tol
        stretch = (SL - SL0) > SL_tol
        constant = np.abs(SL - SL0) <= SL_tol #constant = np.abs(SL - SL0) < SL_tol
        neighbors = np.empty_like(stretch)

        neighbors[:, 0] = stretch[:, 1]
        neighbors[:, -1] = stretch[:, -2]
        for i in range(1, stretch.shape[1] - 1):
            for j in range(stretch.shape[0]):
                neighbors[j, i] = stretch[j, i - 1] or stretch[j, i + 1]

        sl_contr = SL0[contr]
        sl_stretch = SL0[stretch]
        sl_const = SL0[constant]

        print("Sarcomere groups:")
        print("Parameters", self.params)
        print("SLset mean: ", np.mean(self.SLset))
        print("SL0 mean: ", np.mean(SL0))
        print("SL mean: ", np.mean(SL))
        print("Mean contraction: ", np.mean(SL) / np.mean(SL0) - 1.0)

        n_contr = np.sum(contr)
        n_const = np.sum(constant)
        n_stretch = np.sum(stretch)
        print("Contracting: ", n_contr)
        print("Constant: ", n_const)
        print("Stretched: ", n_stretch)
        print("Total: ", n_contr + n_const + n_stretch)
        
        if n_contr > 0:
            print("Mean initial length of contracting sarcomeres: ", np.mean(sl_contr))
        if n_const > 0:
            print("Mean initial length of constant sarcomeres: ", np.mean(sl_const))
        if n_stretch > 0:
            print("Mean initial length of stretched sarcomeres: ", np.mean(sl_stretch))

        self.SL0, self.SL = SL0, SL
        self.contr, self.constant, self.stretch, self.neighbors = (
            contr,
            constant,
            stretch,
            neighbors,
        )

        return SL0, SL, contr, constant, stretch, neighbors

    # --- Analysis & Outputs ---

    def total_force(self, SL: np.ndarray, SL0: np.ndarray) -> float:
        """Returns the macroscopic negative mean load."""
        x_loc = SL - SL0
        x = np.cumsum(x_loc, 1)
        load = self.afterload(x)
        return float(-np.mean(load))

    def sarc_strain(self, SL: np.ndarray) -> float:
        SLref = self.mean_init_sl
        return float((np.mean(SL) / SLref - 1) * 100)

    def active_force_grouped(self, activation: float) -> Tuple[float, float, float]:
        """Total active force for the three groups."""
        active = self.active_force(self.SL, activation)
        active_contr = float(np.sum(active[self.init_contr]))
        active_constant = float(np.sum(active[self.init_constant]))
        active_stretch = float(np.sum(active[self.init_stretch]))
        return active_contr, active_constant, active_stretch

    def active_work_grouped(self, activation: float) -> Tuple[float, float, float]:
        """Work produced by the three groups."""
        active = self.active_force(self.SL, activation)
        x_loc = self.SL - self.SL0
        loc_work = -active * x_loc
        
        print("XTR", np.sum(active), np.sum(x_loc), np.sum(loc_work))
        
        work_contr = float(np.sum(loc_work[self.init_contr]))
        work_constant = float(np.sum(loc_work[self.init_constant]))
        work_stretch = float(np.sum(loc_work[self.init_stretch]))

        return work_contr, work_constant, work_stretch

    def plot_statistics(self, filename: str = "tmp", title: Optional[str] = None, show: bool = True) -> None:
        """Plot pie chart and histogram of contracting, constant, stretched sarcs."""
        sarcs = [np.sum(self.contr), np.sum(self.constant), np.sum(self.stretch)]
        labels = "Contracting", "Constant", "Stretched"

        plt.clf()
        plt.pie(sarcs, labels=labels)
        if title is not None:
            plt.title(title)
        plt.savefig(filename + "_pie.pdf")

        sl_contr = self.SL0[self.contr]
        sl_stretch = self.SL0[self.stretch]
        sl_const = self.SL0[self.constant]

        plt.clf()
        if title is not None:
            plt.title(title)

        count, bins, ignored = plt.hist(
            [sl_contr, sl_const, sl_stretch], bins=np.linspace(1.5, 2.5, 11), rwidth=0.3
        )
        plt.legend(["contr", "const", "stretch"])

        print("Panel G:", count, bins)
        plt.savefig(filename + "_hist.pdf")

        if show:
            plt.show()