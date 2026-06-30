"""
Test the significance of different factors affecting force and
contraction in ttnda mutant cells:
- SL variance
- Reduced passive stiffness
- Reduced thick filament length
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from myogrid.overlap import Overlap, OverlapRice
from myogrid.steady import SarcArray
from myogrid.steady.plot_functions import (
    plot_sarcomere_groups, 
    plot_active_work, 
    plot_active_force
)


from typing import Dict, List, Tuple, Any, Optional

#from steadystate_array import SarcArray
#from overlap import Overlap, OverlapRice
#from plot_functions import plot_sarcomere_groups, plot_active_work, plot_active_force

# Type alias for cleaner type hinting
ResultDict = Dict[str, List[Any]]


def create_sarc_array(
    params: Dict[str, float], 
    overlap_func: Overlap, 
    sl_params: Tuple[float, float]
) -> SarcArray:
    """Helper function to instantiate a SarcArray with given parameters."""
    return SarcArray(
        overlap_func, 
        params, 
        no_myofibrils=30, 
        no_serial_sarcs=50, 
        mean=sl_params[0], 
        sigma=sl_params[1], 
        seed=1
    )


def plot_overlap_comparison(overlap_wt: Overlap, overlap_ttn: Overlap, filename: str) -> None:
    """Generates and saves the filament overlap (force-length relation) plot."""
    sl = np.linspace(1.6, 2.4, 100)
    plt.clf()
    plt.plot(sl, overlap_wt(sl), label="WT")
    plt.plot(sl, overlap_ttn(sl), label="TTN")
    plt.title("Filament overlap (force-length relation)")
    plt.xlabel("Sarcomere length (μm)")
    plt.ylabel("Overlap")
    
    xmin, xmax, ymin, ymax = plt.axis()
    plt.axis([xmin, xmax, 0, ymax])
    plt.legend()
    plt.savefig(filename)


def run_simulation_sweep(
    sarc_array: SarcArray, 
    preloads: List[float], 
    activation: float,
    mutant_mask: Optional[np.ndarray] = None
) -> ResultDict:
    """Runs the force balance simulation across a sweep of preloads and collects the metrics."""
    
    if mutant_mask is None:
        mutant_mask = np.zeros(sarc_array.SLset.shape, dtype=bool)
        
    ctrl_mask = ~mutant_mask

    # Added n_sarc_group_tot so you can plot the whole array if needed
    result_keys = ["stretched_sls", "tot_force", "strains", "n_sarc_group_tot", "n_sarc_group_ctrl", "n_sarc_group_mut", "active", "work"]
    results: ResultDict = {key: [] for key in result_keys}

    for p in preloads:
        SL0, SL, contr, constant, stretch, neighbors = sarc_array.solve(
            activation=activation, preload=p
        )
        
        # --- 1. Total Array Reporting ---
        # Note: If these do not sum to 1500, you need to change < to <= for the constant group in steadystate_array.py
        contr_tot = int(np.sum(contr))
        const_tot = int(np.sum(constant))
        stretch_tot = int(np.sum(stretch))

        # --- 2. Separate Reporting by Type ---
        contr_ctrl = int(np.sum(contr & ctrl_mask))
        const_ctrl = int(np.sum(constant & ctrl_mask))
        stretch_ctrl = int(np.sum(stretch & ctrl_mask))
        
        contr_mut = int(np.sum(contr & mutant_mask))
        const_mut = int(np.sum(constant & mutant_mask))
        stretch_mut = int(np.sum(stretch & mutant_mask))
        
        print(f"\n--- Preload {p} ---")
        print(f"Entire Array       -> Contracting: {contr_tot}, Constant: {const_tot}, Stretched: {stretch_tot} (Total: {contr_tot + const_tot + stretch_tot})")
        print(f"Control Sarcomeres -> Contracting: {contr_ctrl}, Constant: {const_ctrl}, Stretched: {stretch_ctrl}")
        print(f"Mutant Sarcomeres  -> Contracting: {contr_mut}, Constant: {const_mut}, Stretched: {stretch_mut}")

        # Metrics collection
        sl0_vals = {
            "Total": float(np.mean(SL0)),
            "Contracting": float(np.mean(SL0[contr])) if np.any(contr) else 0.0,
            "Constant": float(np.mean(SL0[constant])) if np.any(constant) else 0.0,
            "Stretched": float(np.mean(SL0[stretch])) if np.any(stretch) else 0.0,
        }
        
        strain = sarc_array.sarc_strain(SL0)
        
        results["stretched_sls"].append(sl0_vals)
        results["tot_force"].append(sarc_array.total_force(SL, SL0))
        
        # Save groups separately for downstream plotting
        results["n_sarc_group_tot"].append([strain, contr_tot, const_tot, stretch_tot])
        results["n_sarc_group_ctrl"].append([strain, contr_ctrl, const_ctrl, stretch_ctrl])
        results["n_sarc_group_mut"].append([strain, contr_mut, const_mut, stretch_mut])
        
        results["strains"].append(strain)
        results["active"].append(sarc_array.active_force_grouped(activation=activation))
        results["work"].append(sarc_array.active_work_grouped(activation=activation))

    return results


def main() -> None:
    figure_dir = "figure8_panels"
    if not os.path.isdir(figure_dir):
        os.makedirs(figure_dir)

    # Active default parameters:
    params_wt = {"k_se": 1.0, "PCon_t": 0.002, "k_im": 1.0, "T_ref": 15.0}
    params_ttn = {"k_se": 1.0, "PCon_t": 0.001, "k_im": 1.0, "T_ref": 15.0}

    # Overlap models
    overlap_wt = Overlap(SL_zero=1.6, SL_low=1.7)
    overlap_ttn = Overlap(SL_zero=1.6, SL_low=1.7, scale=0.7857)

    plot_overlap_comparison(overlap_wt, overlap_ttn, filename="overlap_ttn.png")

    wt_mean, wt_sd = 1.952, 0.15
    ttn_mean, ttn_sd = 1.952, 0.15

    preloads = [0, 2.5, 5, 7.5, 10, 11, 12.5, 15]
    activation = 1.0
    
    # Define grid dimensions (matching your create_sarc_array arguments)
    n_myofibrils, n_serial_sarcs = 30, 50

    # Example: Create an empty mask (all False = Control)
    all_control_mask = np.zeros((n_myofibrils, n_serial_sarcs), dtype=bool)
    all_mutant_mask = np.ones((n_myofibrils, n_serial_sarcs), dtype=bool)
    #mutant_mask_20_percent = np.random.rand(n_myofibrils, n_serial_sarcs) < 0.20

    # You can verify the exact percentage generated like this:
    #actual_percentage = np.mean(mutant_mask_20_percent) * 100
    #print(f"Generated mutant mask with {actual_percentage:.1f}% mutant sarcomeres.")


    # --- Setup and Run Simulations ---

    print("\n========== Running Control Simulation (WT) ==========")
    wt_array = create_sarc_array(params_wt, overlap_wt, (wt_mean, wt_sd))
    control_results = run_simulation_sweep(wt_array, preloads, activation, mutant_mask=all_control_mask)

    mutations = {
        "short_filament": create_sarc_array(params_wt, overlap_ttn, (wt_mean, wt_sd)),
        "sl_var_inc": create_sarc_array(params_wt, overlap_wt, (ttn_mean, ttn_sd)),
        "passive_reduced": create_sarc_array(params_ttn, overlap_wt, (wt_mean, wt_sd)),
        "combined": create_sarc_array(params_wt, overlap_ttn, (ttn_mean, ttn_sd)),
        "combined_no_passive": create_sarc_array(params_wt, overlap_ttn, (ttn_mean, ttn_sd)),
    }

    ttn_results: Dict[str, ResultDict] = {}
    for name, mut_array in mutations.items():
        print(f"\n========== Running Mutant Simulation: {name} ==========")
        ttn_results[name] = run_simulation_sweep(mut_array, preloads, activation, mutant_mask=all_control_mask)

    # --- Generate Plots ---

    for key in ttn_results:
        # Force plots
        summaryfile = f"force_{key}.txt"
        filename = os.path.join(figure_dir, f"force_{key}.pdf")
        
        plt.clf()
        norm = plot_active_force(
            control_results["strains"], control_results["active"], filename,
            label="Control", grouped=False, summaryfile=summaryfile
        )
        plot_active_force(
            ttn_results[key]["strains"], ttn_results[key]["active"], filename,
            label=key, grouped=False, baseline=norm, summaryfile=summaryfile
        )

        # Groups plots (using the separated control array from our new dictionary keys)
        summaryfile_ctrl = f"groups_{key}_ctrl.txt"
        filename_ctrl = os.path.join(figure_dir, f"groups_{key}_ctrl.pdf")
        
        plt.clf()
        plot_sarcomere_groups(
            control_results["n_sarc_group_ctrl"], filename_ctrl,
            label="Control (WT Sarcomeres)", merge_groups=True, summaryfile=summaryfile_ctrl
        )
        plot_sarcomere_groups(
            ttn_results[key]["n_sarc_group_ctrl"], filename_ctrl,
            label=f"{key} (WT Sarcomeres)", merge_groups=True, summaryfile=summaryfile_ctrl
        )

    # --- Specific Plot: Combined No Passive ---
    
    key = "combined_no_passive"
    print(f"\nActive work {key}")
    print("Control:", control_results["work"])
    print("Mutant:", ttn_results[key]["work"])

    # Total Work Plot
    plt.clf()
    filename = os.path.join(figure_dir, "work_combined_total.pdf")
    norm = plot_active_work(
        control_results["strains"], control_results["work"], filename,
        label="Control", grouped=False, summaryfile="figure8.txt"
    )
    plot_active_work(
        ttn_results[key]["strains"], ttn_results[key]["work"], filename,
        label=key, grouped=False, baseline=norm, summaryfile="figure8.txt"
    )

    # Grouped Work Plot
    plt.clf()
    filename = os.path.join(figure_dir, "work_combined_grouped.pdf")
    norm = plot_active_work(
        control_results["strains"], control_results["work"], filename,
        label="Control", grouped=True, summaryfile="figure8.txt"
    )
    plot_active_work(
        ttn_results[key]["strains"], ttn_results[key]["work"], filename,
        label=key, grouped=True, baseline=norm, summaryfile="figure8.txt"
    )

if __name__ == "__main__":
    main()