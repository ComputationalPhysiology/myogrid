"""
Simulate a mixed array containing 80% Wild-Type (Control) and 
20% Mutant sarcomeres. The mutant sarcomeres use a scaled down 
overlap function to simulate reduced thick filament length.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Optional

from steadystate_array import SarcArray
from overlap import Overlap
from plot_functions import (
    plot_sarcomere_groups, 
    plot_active_work, 
    plot_active_force,
    plot_mutant_distribution  
)

ResultDict = Dict[str, List[Any]]


def run_simulation_sweep(
    sarc_array: SarcArray, 
    preloads: List[float], 
    activation: float,
    mutant_mask: np.ndarray
) -> ResultDict:
    """Runs the force balance simulation and separates control vs mutant metrics."""
    
    ctrl_mask = ~mutant_mask

    result_keys = [
        "stretched_sls", "tot_force", "strains", 
        "n_sarc_group_tot", "n_sarc_group_ctrl", "n_sarc_group_mut", 
        "active", "work"
    ]
    results: ResultDict = {key: [] for key in result_keys}

    for p in preloads:
        SL0, SL, contr, constant, stretch, neighbors = sarc_array.solve(
            activation=activation, preload=p
        )
        
        # Array Subtotals
        contr_tot, const_tot, stretch_tot = int(np.sum(contr)), int(np.sum(constant)), int(np.sum(stretch))
        
        contr_ctrl = int(np.sum(contr & ctrl_mask))
        const_ctrl = int(np.sum(constant & ctrl_mask))
        stretch_ctrl = int(np.sum(stretch & ctrl_mask))
        
        contr_mut = int(np.sum(contr & mutant_mask))
        const_mut = int(np.sum(constant & mutant_mask))
        stretch_mut = int(np.sum(stretch & mutant_mask))
        
        print(f"\n--- Preload {p} ---")
        print(f"Entire Array       -> Contracting: {contr_tot}, Constant: {const_tot}, Stretched: {stretch_tot}")
        print(f"Control Sarcomeres -> Contracting: {contr_ctrl}, Constant: {const_ctrl}, Stretched: {stretch_ctrl}")
        print(f"Mutant Sarcomeres  -> Contracting: {contr_mut}, Constant: {const_mut}, Stretched: {stretch_mut}")

        strain = sarc_array.sarc_strain(SL0)
        
        # Save group numbers for plotting
        results["n_sarc_group_tot"].append([strain, contr_tot, const_tot, stretch_tot])
        results["n_sarc_group_ctrl"].append([strain, contr_ctrl, const_ctrl, stretch_ctrl])
        results["n_sarc_group_mut"].append([strain, contr_mut, const_mut, stretch_mut])
        
        # Save forces and work
        results["strains"].append(strain)
        results["active"].append(sarc_array.active_force_grouped(activation=activation))
        results["work"].append(sarc_array.active_work_grouped(activation=activation))

    return results


def main() -> None:
    figure_dir = "mixed_sim_panels"
    if not os.path.isdir(figure_dir):
        os.makedirs(figure_dir)

    # --- 1. Define Parameters ---
    params_wt = {"k_se": 1.0, "PCon_t": 0.002, "k_im": 1.0, "T_ref": 15.0}
    overlap_wt = Overlap(SL_zero=1.6, SL_low=1.7)
    
    mean_sl, sd_sl = 1.952, 0.15
    preloads = [0, 2.5, 5, 7.5, 10, 11, 12.5, 15]
    activation = 1.0
    
    n_myofibrils = 30
    n_serial_sarcs = 50

    # --- 2. Generate the 20% Mutant Mask ---
    np.random.seed(42)  
    mutant_mask = np.random.rand(n_myofibrils, n_serial_sarcs) < 0.20
    
    plot_mutant_distribution(
        mutant_mask, 
        filename=os.path.join(figure_dir, "array_distribution.pdf")
    )


    actual_pct = np.mean(mutant_mask) * 100
    print(f"========== Initializing Mixed Array ==========")
    print(f"Grid size: {n_myofibrils} x {n_serial_sarcs} ({n_myofibrils * n_serial_sarcs} total sarcomeres)")
    print(f"Generated mutant mask with {actual_pct:.1f}% mutant sarcomeres.\n")

    # --- 3. Run Simulation ---
    # We pass the standard WT parameters to the whole array, but provide the 
    # mutant_mask and mutant_scale so SarcArray handles the local scaling internally.
    mixed_array = SarcArray(
        overlap=overlap_wt, 
        params=params_wt, 
        no_myofibrils=n_myofibrils, 
        no_serial_sarcs=n_serial_sarcs, 
        mean=mean_sl, 
        sigma=sd_sl, 
        seed=1,
        mutant_mask=mutant_mask,
        mutant_scale=0.7857 
    )

    results = run_simulation_sweep(mixed_array, preloads, activation, mutant_mask)

    # --- 4. Generate Plots ---
    print("\n========== Generating Plots ==========")
    
    # Plot Total Force
    plt.clf()
    force_file = os.path.join(figure_dir, "mixed_force.pdf")
    plot_active_force(
        results["strains"], results["active"], force_file,
        label="Mixed Array", grouped=True
    )
    
    # Plot Total Work
    plt.clf()
    work_file = os.path.join(figure_dir, "mixed_work.pdf")
    plot_active_work(
        results["strains"], results["work"], work_file,
        label="Mixed Array", grouped=True
    )

    # Plot Sub-population Proportions
    plt.clf()
    plot_sarcomere_groups(
        results["n_sarc_group_tot"], os.path.join(figure_dir, "groups_total.pdf"),
        label="Total Array", merge_groups=True
    )
    
    plt.clf()
    plot_sarcomere_groups(
        results["n_sarc_group_ctrl"], os.path.join(figure_dir, "groups_control.pdf"),
        label="Control", merge_groups=True
    )
    
    plt.clf()
    plot_sarcomere_groups(
        results["n_sarc_group_mut"], os.path.join(figure_dir, "groups_mutant.pdf"),
        label="Mutant", merge_groups=True
    )
    
    print(f"Simulation complete. Plots saved to '{figure_dir}/'.")


if __name__ == "__main__":
    main()