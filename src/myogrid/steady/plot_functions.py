import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
import numpy as np
from typing import Optional, Union, List, Dict

def plot_sarcomere_groups(
    n_sarc_group: Union[List, np.ndarray],
    filename: str,
    summaryfile: Optional[str] = None,
    merge_groups: bool = True,
    label: str = ''
) -> None:
    """
    Panel 4H: Proportion of sarcomeres in each group as a function of stretch.
    Tracks how the numbers in each group change with total stretch.
    """
    n_sarc_group = np.asarray(n_sarc_group)
    total_number = np.sum(n_sarc_group[0, 1:])
    
    # --- Guard against ZeroDivisionError for empty groups ---
    if total_number == 0:
        print(f"Skipping group plot for '{label}': 0 sarcomeres present.")
        return
    
    plt.plot(n_sarc_group[:, 0], n_sarc_group[:, 1] / total_number, label=f'{label} Contracting')
    
    if merge_groups:
        stretched = n_sarc_group[:, 2] + n_sarc_group[:, 3]  # constant + stretched
        plt.plot(n_sarc_group[:, 0], stretched / total_number, label=f'{label} Stretched')
    else:
        plt.plot(n_sarc_group[:, 0], n_sarc_group[:, 2] / total_number, label=f'{label} Constant')
        plt.plot(n_sarc_group[:, 0], n_sarc_group[:, 3] / total_number, label=f'{label} Stretched')
        
    plt.legend()
    yticks = np.linspace(0, 1, 6)
    ylabels = [f'{l*100:2.0f}' for l in yticks]
    plt.yticks(yticks, ylabels)
    plt.ylabel('Proportion of sarcomeres (%)')
    plt.xlabel('Total stretch (%)')
    plt.savefig(filename)

    # Save figure data in a text file:
    if summaryfile is not None:
        with open(summaryfile, 'a') as outfile:
            outfile.write('Panel 4H, number of sarcs\n')
            outfile.write('Stretch values (x axis):\n')
            outfile.write(f'{n_sarc_group[:, 0]}\n')
            outfile.write('Number of sarcs (y axis):\n')
            outfile.write(f'Contracting: {n_sarc_group[:, 1]}\n')
            outfile.write(f'Constant: {n_sarc_group[:, 2]}\n')
            outfile.write(f'Stretched: {n_sarc_group[:, 3]}\n\n\n')


def plot_mutant_distribution(
    mutant_mask: np.ndarray, 
    filename: str, 
    show: bool = False
) -> None:
    """
    Visualizes the 2D sarcomere array grid, color-coding Control vs. Mutant sarcomeres.
    """
    plt.clf()
    
    # Create a discrete colormap: 0 (False/Control) -> Light Blue, 1 (True/Mutant) -> Orange
    colors = ['#add8e6', '#ff7f0e']
    cmap = ListedColormap(colors)
    
    # imshow treats True as 1 and False as 0
    # aspect='auto' ensures the cells stretch to fit standard figure sizes
    plt.imshow(mutant_mask, cmap=cmap, aspect='auto', origin='lower')
    
    plt.title('Spatial Distribution of Mutant Sarcomeres')
    plt.ylabel('Myofibril Index (Parallel)')
    plt.xlabel('Sarcomere Index (Serial)')
    
    # Create a custom legend
    ctrl_patch = mpatches.Patch(color=colors[0], label='Control (WT)')
    mut_patch = mpatches.Patch(color=colors[1], label='Mutant')
    
    # Place legend completely outside the plot box
    plt.legend(handles=[ctrl_patch, mut_patch], bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # tight_layout ensures the external legend isn't cut off during save
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    
    if show:
        plt.show()


def plot_sarcomere_length(
    stretch: Union[List, np.ndarray],
    stretched_sls: List[Dict[str, Union[float, np.ndarray]]],
    filename: str,
    merge_groups: bool = True,
    summaryfile: Optional[str] = None,
    label: str = ''
) -> None:
    """
    Panel 4I: Sarcomere length after stretch, before contraction,
    for each group, as a function of mean stretch.
    """
    # Restructure the list of dicts into a dict of arrays
    sl0_groups = {
        key: np.array([sl0[key] for sl0 in stretched_sls]) 
        for key in stretched_sls[0]
    }

    if merge_groups:
        merged_stretch = (sl0_groups['Constant'] + sl0_groups['Stretched']) / 2
        plt.plot(stretch, merged_stretch, label=f'{label} Stretched')
        plt.plot(stretch, sl0_groups['Contracting'], label=f'{label} Contracting')
    else:
        for key, values in sl0_groups.items():
            plt.plot(stretch, values, label=f'{label} {key}')

    plt.legend()
    plt.title("Resting sarcomere lengths after stretch")
    plt.xlabel('Total stretch (%)')
    plt.ylabel('Sarcomere length (μm)')
    plt.savefig(filename)

    if summaryfile is not None:
        with open(summaryfile, 'a') as outfile:
            outfile.write('Panel 4I, sarcomere lengths\n')
            outfile.write('Stretch values (x axis):\n')
            for key, values in sl0_groups.items():
                outfile.write(f'{key}: {values}\n')
            outfile.write('\n\n')


def plot_active_work(
    stretch: Union[List, np.ndarray],
    active_work: Union[List, np.ndarray],
    filename: str,
    grouped: bool = True,
    merge_groups: bool = True,
    summaryfile: Optional[str] = None,
    label: Optional[str] = None,
    baseline: Optional[float] = None
) -> float:
    """
    Panel 4K: Active work as a function of stretch for each group,
    grouped according to their behavior at zero stretch.
    """
    active_work_arr = np.array(active_work)
    sum_work = np.sum(active_work_arr, 1)
    
    if baseline is None:
        baseline = float(sum_work[0])

    sum_work = sum_work / baseline
    active_work_arr = active_work_arr / baseline
    
    if label is None:
        label = 'Total'

    if grouped:
        plt.plot(stretch, active_work_arr[:, 0], label=f'{label} Contracting')
        if merge_groups:
            plt.plot(stretch, active_work_arr[:, 1] + active_work_arr[:, 2], label=f'{label} Stretched')
        else:
            plt.plot(stretch, active_work_arr[:, 1], label=f'{label} Constant')
            plt.plot(stretch, active_work_arr[:, 2], label=f'{label} Stretched')
            
    plt.plot(stretch, sum_work, label=label)
    plt.legend()
    plt.xlabel('Total stretch (%)')
    plt.ylabel('Normalized active work')
    plt.title('Total active work')
    plt.savefig(filename)

    if summaryfile is not None:
        with open(summaryfile, 'a') as outfile:
            outfile.write('Panel 4K, total active work\n')
            outfile.write('Stretch values (x axis):\n')
            outfile.write(f'{stretch}\n')
            outfile.write('Normalized work (y axis):\n')
            outfile.write(f'Total: {sum_work}\n')
            outfile.write(f'Contracting: {active_work_arr[:, 0]}\n')
            outfile.write(f'Constant: {active_work_arr[:, 1]}\n')
            outfile.write(f'Stretched: {active_work_arr[:, 2]}\n\n\n')

    return baseline


def plot_active_force(
    stretch: Union[List, np.ndarray],
    total_active: Union[List, np.ndarray],
    filename: str,
    grouped: bool = True,
    label: Optional[str] = None,
    summaryfile: Optional[str] = None,
    baseline: Optional[float] = None
) -> float:
    """
    Panel 4J: Force as a function of stretch for each group,
    grouped according to their behavior at zero stretch.
    """
    total_active_arr = np.array(total_active)
    sum_active = np.sum(total_active_arr, 1)
    
    if baseline is None:
        baseline = float(sum_active[0])
        
    sum_active = sum_active / baseline
    total_active_arr = total_active_arr / baseline
    
    if label is None:
        label = 'Total'
        
    plt.plot(stretch, sum_active, label=label)
    
    if grouped:
        plt.plot(stretch, total_active_arr[:, 0], label='Contracting')
        plt.plot(stretch, total_active_arr[:, 1], label='Constant')
        plt.plot(stretch, total_active_arr[:, 2], label='Stretched')
        
    plt.legend()
    plt.title("Total active force")
    plt.ylabel('Normalized active force')
    plt.xlabel('Total stretch (%)')
    plt.savefig(filename)

    if summaryfile is not None:
        with open(summaryfile, 'a') as outfile:
            outfile.write('Panel 4J, total active force\n')
            outfile.write('Stretch values (x axis):\n')
            outfile.write(f'{stretch}\n')
            outfile.write('Normalized force (y axis):\n')
            outfile.write(f'Total: {sum_active}\n')
            outfile.write(f'Contracting: {total_active_arr[:, 0]}\n')
            outfile.write(f'Constant: {total_active_arr[:, 1]}\n')
            outfile.write(f'Stretched: {total_active_arr[:, 2]}\n\n\n')

    return baseline