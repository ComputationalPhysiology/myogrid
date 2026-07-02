import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
import numpy as np
from typing import Optional, Union, List, Dict, Tuple, Any
from pathlib import Path


# ==========================================
# 1. DATA PROCESSING (The Pipeline)
# ==========================================

def process_sarcomere_groups(n_sarc_group: Union[List, np.ndarray]) -> Dict[str, np.ndarray]:
    """Processes raw group counts into proportions and extracted arrays."""
    n_sarc_group = np.asarray(n_sarc_group)
    total_number = np.sum(n_sarc_group[0, 1:])
    
    if total_number == 0:
        return {}
        
    return {
        "stretch": n_sarc_group[:, 0],
        "contracting_prop": n_sarc_group[:, 1] / total_number,
        "constant_prop": n_sarc_group[:, 2] / total_number,
        "stretched_prop": n_sarc_group[:, 3] / total_number,
        "contracting_raw": n_sarc_group[:, 1],
        "constant_raw": n_sarc_group[:, 2],
        "stretched_raw": n_sarc_group[:, 3],
    }

def process_sarcomere_length(stretched_sls: List[Dict[str, Union[float, np.ndarray]]]) -> Dict[str, np.ndarray]:
    """Extracts sarcomere length dictionaries into plottable arrays."""
    return {
        key: np.array([sl0[key] for sl0 in stretched_sls]) 
        for key in stretched_sls[0]
    }

def process_active_metric(data: Union[List, np.ndarray], baseline: Optional[float] = None) -> Dict[str, Any]:
    """Processes force or work data (calculates sum and normalizes)."""
    
    arr = np.array(data)
        
    sum_val = np.sum(arr, axis=1)
    
    if baseline is None:
        baseline = float(sum_val[0])
        
    return {
        "baseline": baseline,
        "total_norm": sum_val / baseline,
        "contracting_norm": arr[:, 0] / baseline,
        "constant_norm": arr[:, 1] / baseline,
        "stretched_norm": arr[:, 2] / baseline,
        "total_raw": sum_val,
        "contracting_raw": arr[:, 0],
        "constant_raw": arr[:, 1],
        "stretched_raw": arr[:, 2]
    }


# ==========================================
# 2. FILE I/O (Exporting Summaries)
# ==========================================

def export_group_summary(filepath: Union[str, Path], title: str, group_data: dict) -> None:
    """Appends processed group data to a summary text file."""
    if not group_data: 
        return
        
    with open(filepath, 'a') as f:
        f.write(f'{title}\n')
        f.write('Stretch values (x axis):\n')
        f.write(f'{group_data["stretch"]}\n')
        f.write('Number of sarcs (y axis):\n')
        f.write(f'Contracting: {group_data["contracting_raw"]}\n')
        f.write(f'Constant: {group_data["constant_raw"]}\n')
        f.write(f'Stretched: {group_data["stretched_raw"]}\n\n\n')

def export_metric_summary(filepath: Union[str, Path], title: str, stretch: np.ndarray, metric_data: dict) -> None:
    """Appends processed force or work data to a summary text file."""
    with open(filepath, 'a') as f:
        f.write(f'{title}\n')
        f.write('Stretch values (x axis):\n')
        f.write(f'{stretch}\n')
        f.write('Normalized metric (y axis):\n')
        f.write(f'Total: {metric_data["total_norm"]}\n')
        f.write(f'Contracting: {metric_data["contracting_norm"]}\n')
        f.write(f'Constant: {metric_data["constant_norm"]}\n')
        f.write(f'Stretched: {metric_data["stretched_norm"]}\n\n\n')


# ==========================================
# 3. VISUALIZATION (Pure Plotting)
# ==========================================

def plot_sarcomere_groups(
    group_data: dict,
    ax: Optional[plt.Axes] = None,
    filename: Optional[Union[str, Path]] = None,
    merge_groups: bool = True,
    label: str = ''
) -> plt.Axes:
    """Panel 4H: Proportion of sarcomeres in each group as a function of stretch."""
    if ax is None:
        fig, ax = plt.subplots()

    if not group_data:
        print(f"Skipping group plot for '{label}': 0 sarcomeres present.")
        return ax
    
    stretch = group_data["stretch"]
    ax.plot(stretch, group_data["contracting_prop"], label=f'{label} Contracting')
    
    if merge_groups:
        merged = group_data["constant_prop"] + group_data["stretched_prop"]
        ax.plot(stretch, merged, label=f'{label} Stretched')
    else:
        ax.plot(stretch, group_data["constant_prop"], label=f'{label} Constant')
        ax.plot(stretch, group_data["stretched_prop"], label=f'{label} Stretched')
        
    ax.legend()
    yticks = np.linspace(0, 1, 6)
    ylabels = [f'{l*100:2.0f}' for l in yticks]
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels)
    ax.set_ylabel('Proportion of sarcomeres (%)')
    ax.set_xlabel('Total stretch (%)')
    
    if filename:
        ax.figure.tight_layout()
        ax.figure.savefig(filename)

    return ax


def plot_mutant_distribution(
    mutant_mask: np.ndarray, 
    ax: Optional[plt.Axes] = None,
    filename: Optional[Union[str, Path]] = None
) -> plt.Axes:
    """Visualizes the 2D sarcomere array grid, color-coding Control vs. Mutant sarcomeres."""
    if ax is None:
        fig, ax = plt.subplots()
    
    colors = ['#add8e6', '#ff7f0e']
    cmap = ListedColormap(colors)
    
    ax.imshow(mutant_mask, cmap=cmap, aspect='auto', origin='lower')
    ax.set_title('Spatial Distribution of Mutant Sarcomeres')
    ax.set_ylabel('Myofibril Index (Parallel)')
    ax.set_xlabel('Sarcomere Index (Serial)')
    
    ctrl_patch = mpatches.Patch(color=colors[0], label='Control (WT)')
    mut_patch = mpatches.Patch(color=colors[1], label='Mutant')
    ax.legend(handles=[ctrl_patch, mut_patch], bbox_to_anchor=(1.05, 1), loc='upper left')
    
    if filename:
        ax.figure.savefig(filename, bbox_inches='tight')
        
    return ax


def plot_sarcomere_length(
    stretch: Union[List, np.ndarray],
    sl_data: dict,
    ax: Optional[plt.Axes] = None,
    filename: Optional[Union[str, Path]] = None,
    merge_groups: bool = True,
    label: str = ''
) -> plt.Axes:
    """Panel 4I: Sarcomere length after stretch, before contraction."""
    if ax is None:
        fig, ax = plt.subplots()

    if merge_groups:
        merged_stretch = (sl_data.get('Constant', 0) + sl_data.get('Stretched', 0)) / 2
        ax.plot(stretch, merged_stretch, label=f'{label} Stretched')
        ax.plot(stretch, sl_data.get('Contracting', 0), label=f'{label} Contracting')
    else:
        for key, values in sl_data.items():
            ax.plot(stretch, values, label=f'{label} {key}')

    ax.legend()
    ax.set_title("Resting sarcomere lengths after stretch")
    ax.set_xlabel('Total stretch (%)')
    ax.set_ylabel('Sarcomere length (μm)')
    
    if filename:
        ax.figure.tight_layout()
        ax.figure.savefig(filename)

    return ax


def plot_active_metric(
    stretch: Union[List, np.ndarray],
    metric_data: dict,
    title: str = "Active Metric",
    ylabel: str = "Normalized Metric",
    ax: Optional[plt.Axes] = None,
    filename: Optional[Union[str, Path]] = None,
    grouped: bool = True,
    merge_groups: bool = True,
    label: Optional[str] = None
) -> plt.Axes:
    """A generic visualization function for active work or active force."""
    if ax is None:
        fig, ax = plt.subplots()

    label = label or 'Total'

    if grouped:
        ax.plot(stretch, metric_data["contracting_norm"], label=f'{label} Contracting')
        if merge_groups:
            merged = metric_data["constant_norm"] + metric_data["stretched_norm"]
            ax.plot(stretch, merged, label=f'{label} Stretched')
        else:
            ax.plot(stretch, metric_data["constant_norm"], label=f'{label} Constant')
            ax.plot(stretch, metric_data["stretched_norm"], label=f'{label} Stretched')
            
    ax.plot(stretch, metric_data["total_norm"], label=label)
    ax.legend()
    ax.set_xlabel('Total stretch (%)')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    
    if filename:
        ax.figure.tight_layout()
        ax.figure.savefig(filename)

    return ax