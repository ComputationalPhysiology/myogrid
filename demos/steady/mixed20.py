"""
Simulate a mixed array containing 80% Wild-Type (Control) and 
20% Mutant sarcomeres. The mutant sarcomeres use a scaled down 
overlap function to simulate reduced thick filament length.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Any

from myogrid.overlap import Overlap 
from myogrid.steady import SteadySarcArray2D
from myogrid.steady.plot_functions import (
    process_sarcomere_groups,
    process_active_metric,
    plot_sarcomere_groups, 
    plot_active_metric, 
    plot_mutant_distribution  
)

ResultDict = Dict[str, List[Any]]


def run_simulation_sweep(
    sarc_array: SteadySarcArray2D, 
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
    
        results["n_sarc_group_tot"].append([strain, contr_tot, const_tot, stretch_tot])
        results["n_sarc_group_ctrl"].append([strain, contr_ctrl, const_ctrl, stretch_ctrl])
        results["n_sarc_group_mut"].append([strain, contr_mut, const_mut, stretch_mut])
        
        results["strains"].append(strain)
        results["active"].append(sarc_array.active_force_grouped(activation=activation))
        results["work"].append(sarc_array.active_work_grouped(activation=activation))

    return results


def main() -> None:
    figure_dir = Path("mixed_sim_panels")
    figure_dir.mkdir(parents=True, exist_ok=True)

    params_wt = {"k_se": 1.0, "PCon_t": 0.002, "k_im": 1.0, "T_ref": 15.0}
    overlap_wt = Overlap(SL_zero=1.6, SL_low=1.7)
    
    mean_sl, sd_sl = 1.952, 0.15
    preloads = [0, 2.5, 5, 7.5, 10, 11, 12.5, 15]
    activation = 1.0
    
    n_myofibrils = 30
    n_serial_sarcs = 50

    # Generate the mask for 20% "mutant" sarcomeres
    np.random.seed(42)  
    mutant_mask = np.random.rand(n_myofibrils, n_serial_sarcs) < 0.20
    
    plot_mutant_distribution(
        mutant_mask=mutant_mask, 
        filename=figure_dir / "array_distribution.pdf"
    )

    actual_pct = np.mean(mutant_mask) * 100
    print(f"========== Initializing Mixed Array ==========")
    print(f"Grid size: {n_myofibrils} x {n_serial_sarcs} ({n_myofibrils * n_serial_sarcs} total sarcomeres)")
    print(f"Generated mutant mask with {actual_pct:.1f}% mutant sarcomeres.\n")

    mixed_array = SteadySarcArray2D(
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

    print("\n========== Generating Plots ==========")
    strains = np.array(results["strains"])
    
    force_data = process_active_metric(results["active"])
    plot_active_metric(
        stretch=strains, 
        metric_data=force_data, 
        title="Total Active Force", 
        ylabel="Normalized Active Force",
        filename=figure_dir / "mixed_force.pdf",
        label="Mixed Array", 
        grouped=True
    )
    
    work_data = process_active_metric(results["work"])
    plot_active_metric(
        stretch=strains, 
        metric_data=work_data, 
        title="Total Active Work", 
        ylabel="Normalized Active Work",
        filename=figure_dir / "mixed_work.pdf",
        label="Mixed Array", 
        grouped=True
    )

    #Plot the number of stretched, constant and contracting for the 
    # control sarcomeres, the 'mutant', and the total
    groups_tot = process_sarcomere_groups(results["n_sarc_group_tot"])
    plot_sarcomere_groups(
        group_data=groups_tot, 
        filename=figure_dir / "groups_total.pdf",
        label="Total Array", 
        merge_groups=True
    )
    
    groups_ctrl = process_sarcomere_groups(results["n_sarc_group_ctrl"])
    plot_sarcomere_groups(
        group_data=groups_ctrl, 
        filename=figure_dir / "groups_control.pdf",
        label="Control", 
        merge_groups=True
    )
    
    groups_mut = process_sarcomere_groups(results["n_sarc_group_mut"])
    plot_sarcomere_groups(
        group_data=groups_mut, 
        filename=figure_dir / "groups_mutant.pdf",
        label="Mutant", 
        merge_groups=True
    )
    
    print(f"Simulation complete. Plots saved to '{figure_dir}/'.")


if __name__ == "__main__":
    main()