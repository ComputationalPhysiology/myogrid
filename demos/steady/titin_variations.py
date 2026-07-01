"""
Test the significance of different factors affecting force and
contraction in ttnda mutant cells:
- SL variance
- Reduced passive stiffness
- Reduced thick filament length
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Tuple, Any, Union

from myogrid.overlap import Overlap, OverlapRice
from myogrid.steady import SteadySarcArray2D

# Import the Pipeline architecture
from myogrid.steady.plot_functions import (
    process_sarcomere_groups,
    process_active_metric,
    export_group_summary,
    export_metric_summary,
    plot_sarcomere_groups,
    plot_active_metric,
)

# Type alias for cleaner type hinting
ResultDict = Dict[str, List[Any]]


def create_sarc_array(
    params: Dict[str, float], 
    overlap_func: Overlap, 
    sl_params: Tuple[float, float]
) -> SteadySarcArray2D:
    """Helper function to instantiate a SteadySarcArray2D with given parameters."""
    return SteadySarcArray2D(
        overlap=overlap_func, 
        params=params, 
        no_myofibrils=30, 
        no_serial_sarcs=50, 
        mean=sl_params[0], 
        sigma=sl_params[1], 
        seed=1
    )


def plot_overlap_comparison(overlap_wt: Overlap, overlap_ttn: Overlap, filename: Union[str, Path]) -> None:
    """Generates and saves the filament overlap (force-length relation) plot."""
    sl = np.linspace(1.6, 2.4, 100)
    fig, ax = plt.subplots()
    ax.plot(sl, overlap_wt(sl), label="WT")
    ax.plot(sl, overlap_ttn(sl), label="TTN")
    ax.set_title("Filament overlap (force-length relation)")
    ax.set_xlabel("Sarcomere length (μm)")
    ax.set_ylabel("Overlap")
    
    xmin, xmax, ymin, ymax = ax.axis()
    ax.axis([xmin, xmax, 0, ymax])
    ax.legend()
    fig.savefig(filename)
    plt.close(fig)


def run_simulation_sweep(
    sarc_array: SteadySarcArray2D, 
    preloads: List[float], 
    activation: float
) -> ResultDict:
    """Runs the force balance simulation across a sweep of preloads for a homogeneous array."""
    
    result_keys = ["stretched_sls", "tot_force", "strains", "n_sarc_group_tot", "active", "work"]
    results: ResultDict = {key: [] for key in result_keys}

    for p in preloads:
        SL0, SL, contr, constant, stretch, neighbors = sarc_array.solve(
            activation=activation, preload=p
        )
        
        # --- Total Array Reporting ---
        contr_tot = int(np.sum(contr))
        const_tot = int(np.sum(constant))
        stretch_tot = int(np.sum(stretch))

        print(f"\n--- Preload {p} ---")
        print(f"Entire Array -> Contracting: {contr_tot}, Constant: {const_tot}, Stretched: {stretch_tot} (Total: {contr_tot + const_tot + stretch_tot})")

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
        
        # Save total groups for downstream processing
        results["n_sarc_group_tot"].append([strain, contr_tot, const_tot, stretch_tot])
        
        results["strains"].append(strain)
        results["active"].append(sarc_array.active_force_grouped(activation=activation))
        results["work"].append(sarc_array.active_work_grouped(activation=activation))

    return results


def main() -> None:
    figure_dir = Path("titin_var_results")
    figure_dir.mkdir(parents=True, exist_ok=True)

    # Active default parameters:
    params_wt = {"k_se": 1.0, "PCon_t": 0.002, "k_im": 1.0, "T_ref": 15.0}
    params_ttn = {"k_se": 1.0, "PCon_t": 0.001, "k_im": 1.0, "T_ref": 15.0}

    # Overlap models
    overlap_wt = Overlap(SL_zero=1.6, SL_low=1.7)
    overlap_ttn = Overlap(SL_zero=1.6, SL_low=1.7, scale=0.7857)

    plot_overlap_comparison(overlap_wt, overlap_ttn, filename=figure_dir / "overlap_ttn.png")

    wt_mean, wt_sd = 1.952, 0.15
    ttn_mean, ttn_sd = 1.952, 0.15

    preloads = [0, 2.5, 5, 7.5, 10, 11, 12.5, 15]
    activation = 1.0

    # --- Setup and Run Simulations ---

    print("\n========== Running Control Simulation (WT) ==========")
    wt_array = create_sarc_array(params_wt, overlap_wt, (wt_mean, wt_sd))
    control_results = run_simulation_sweep(wt_array, preloads, activation)

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
        ttn_results[name] = run_simulation_sweep(mut_array, preloads, activation)

    # --- Process, Export, and Visualize Data ---

    for key in ttn_results:
        summaryfile = figure_dir / f"force_{key}.txt"
        filename = figure_dir / f"force_{key}.pdf"
        
        # 1. PROCESS Force Data (Normalize against Control baseline)
        force_data_ctrl = process_active_metric(control_results["active"])
        baseline = force_data_ctrl["baseline"]
        force_data_mut = process_active_metric(ttn_results[key]["active"], baseline=baseline)

        # 2. EXPORT Force Data
        export_metric_summary(summaryfile, "Control", control_results["strains"], force_data_ctrl)
        export_metric_summary(summaryfile, key, ttn_results[key]["strains"], force_data_mut)

        # 3. VISUALIZE Force Data (Overlaying Control and Mutant on same Axes)
        ax = plot_active_metric(
            stretch=control_results["strains"], 
            metric_data=force_data_ctrl, 
            title="Total active force", ylabel="Normalized active force", 
            label="Control", grouped=False
        )
        plot_active_metric(
            stretch=ttn_results[key]["strains"], 
            metric_data=force_data_mut, 
            ax=ax, filename=filename,  # Reuse ax and trigger save
            title="Total active force", ylabel="Normalized active force",
            label=key, grouped=False
        )

        # ---------------------------------------------
        # Groups plots
        summaryfile_grp = figure_dir / f"groups_{key}.txt"
        filename_grp = figure_dir / f"groups_{key}.pdf"
        
        # 1. PROCESS Groups Data (Now purely using the total array data)
        groups_data_ctrl = process_sarcomere_groups(control_results["n_sarc_group_tot"])
        groups_data_mut = process_sarcomere_groups(ttn_results[key]["n_sarc_group_tot"])

        # 2. EXPORT Groups Data
        export_group_summary(summaryfile_grp, "Control Array", groups_data_ctrl)
        export_group_summary(summaryfile_grp, f"{key} Array", groups_data_mut)

        # 3. VISUALIZE Groups Data
        ax_grp = plot_sarcomere_groups(
            group_data=groups_data_ctrl,
            label="Control", merge_groups=True
        )
        plot_sarcomere_groups(
            group_data=groups_data_mut,
            ax=ax_grp, filename=filename_grp, 
            label=key, merge_groups=True
        )

    # --- Specific Plot: Combined No Passive Work ---
    
    key = "combined_no_passive"
    summaryfile_work = figure_dir / "titin_var_work.txt"
    
    # 1. PROCESS Work Data
    work_data_ctrl = process_active_metric(control_results["work"])
    baseline_work = work_data_ctrl["baseline"]
    work_data_mut = process_active_metric(ttn_results[key]["work"], baseline=baseline_work)

    # 2. EXPORT Work Data
    export_metric_summary(summaryfile_work, "Control Work", control_results["strains"], work_data_ctrl)
    export_metric_summary(summaryfile_work, f"{key} Work", ttn_results[key]["strains"], work_data_mut)

    # 3. VISUALIZE Total Work Plot
    ax_wt = plot_active_metric(
        stretch=control_results["strains"], 
        metric_data=work_data_ctrl, 
        title="Total active work", ylabel="Normalized active work", 
        label="Control", grouped=False
    )
    plot_active_metric(
        stretch=ttn_results[key]["strains"], 
        metric_data=work_data_mut, 
        ax=ax_wt, filename=figure_dir / "work_combined_total.pdf", 
        title="Total active work", ylabel="Normalized active work",
        label=key, grouped=False
    )

    # 4. VISUALIZE Grouped Work Plot
    ax_wg = plot_active_metric(
        stretch=control_results["strains"], 
        metric_data=work_data_ctrl, 
        title="Total active work", ylabel="Normalized active work", 
        label="Control", grouped=True
    )
    plot_active_metric(
        stretch=ttn_results[key]["strains"], 
        metric_data=work_data_mut, 
        ax=ax_wg, filename=figure_dir / "work_combined_grouped.pdf", 
        title="Total active work", ylabel="Normalized active work",
        label=key, grouped=True
    )

if __name__ == "__main__":
    main()