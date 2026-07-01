import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional, Union, Dict
from pathlib import Path

def plot_sarc_array(
    data: np.ndarray, 
    plot_sarcs: Optional[List[Tuple[int, int]]] = None, 
    plot_springs: bool = True,
    ax: Optional[plt.Axes] = None,
    filename: Optional[Union[str, Path]] = None,
    sarc_labels: Optional[Dict[Union[Tuple[int, int], str], str]] = None
) -> Tuple[plt.Axes, np.ndarray]:
    """
    Plots a visual representation of the 2D sarcomere grid.
    
    Args:
        data: 2D array of sarcomere lengths.
        plot_sarcs: List of specific (fibril, series) indices to highlight in red.
        plot_springs: Whether to draw connecting springs between myofibrils.
        ax: Optional Matplotlib Axes object to plot on.
        filename: Optional path to save the figure.
        sarc_labels: Dictionary mapping (fibril, series) tuples to text labels. 
                     Use the key "default" to apply a label to all unmapped sarcomeres.
                     
    Returns:
        A tuple containing the modified Matplotlib Axes object and the array of 
        colors used for the highlighted sarcomeres.
    """
    plot_sarcs = plot_sarcs or [(1, 2)]
    sarc_labels = sarc_labels or {}
    
    # If no axis is provided, generate a standalone figure
    if ax is None:
        hsize, vsize = 10.0, 2.0
        fig, ax = plt.subplots(figsize=(hsize, vsize))
        
    labels = [str(i) for i in range(data.shape[0])]
    data_cum = data.cumsum(axis=1)

    grey_scales = plt.get_cmap('Greys')(np.linspace(0.15, 0.85, data.shape[1]))
    colors = plt.get_cmap('Reds')(np.linspace(0.15, 0.85, len(plot_sarcs)))

    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    # Plot the grid
    for i, color in enumerate(grey_scales):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        b_height = 0.4
        
        barlist = ax.barh(labels, widths, left=starts, height=b_height, color=color, edgecolor='k')
        xcenters = starts + widths / 2

        # Highlight specific sarcomeres
        for index, s in enumerate(plot_sarcs):
            if s[1] == i:
                barlist[s[0]].set_facecolor(colors[index])

        # Plot structural springs
        if plot_springs:
            x = starts + widths
            y_start = b_height / 2
            v_dist = 1.0
            y = np.array([y_start, -y_start + v_dist])
            for k in range(len(x) - 1):
                ax.plot(x[k:k+2], y, linestyle='--', color='k')
                y += v_dist

        # Apply labels dynamically
        r, g, b, _ = color
        text_color = 'black' if r * g * b > 0.01 else 'white'
        
        for y_idx, (x_pos, _) in enumerate(zip(xcenters, widths)):
            # Look for a specific label, otherwise fallback to "default", otherwise empty string
            text = sarc_labels.get((y_idx, i), sarc_labels.get("default", ""))
            if text:
                ax.text(x_pos, y_idx, text, ha='center', va='center', color=text_color)

    if filename:
        plt.tight_layout()
        plt.savefig(filename)

    return ax, colors


def plot_results(
    t: np.ndarray,
    s: np.ndarray,
    no_sarc_series: int,
    no_myofibrils: int,
    sl_ind: int,
    sarcs_to_plot: List[Tuple[int, int]],
    colors: np.ndarray,
    ax: Optional[plt.Axes] = None,
    filename: Optional[Union[str, Path]] = None
) -> plt.Axes:
    """
    Plots the trajectories of specific state variables for highlighted sarcomeres.
    """
    if ax is None:
        fig, ax = plt.subplots()
        
    sn = int(s.shape[1] / (no_sarc_series * no_myofibrils)) - 1

    for r, sarc in enumerate(sarcs_to_plot):
        j, i = sarc[0], sarc[1]
        idx = j * no_sarc_series * sn + sl_ind + i * sn
        ax.plot(t, s[:, idx], color=colors[r], label=f'Sarc {sarc}')

    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Sarcomere Length (μm)')
    ax.legend()
    
    if filename:
        plt.savefig(filename)
        
    return ax


def get_results(
    t: np.ndarray,
    s: np.ndarray,
    no_sarc_series: int,
    no_myofibrils: int,
    ind: int,
    sarcs_to_plot: List[Tuple[int, int]]
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extracts state variables with a given index from selected sarcomeres for plotting.
    """
    sn = int(s.shape[1] / (no_sarc_series * no_myofibrils)) - 1
    states = np.zeros((len(t), len(sarcs_to_plot)))

    for r, sarc in enumerate(sarcs_to_plot):
        j, i = sarc[0], sarc[1]
        idx = j * no_sarc_series * sn + ind + i * sn
        states[:, r] = s[:, idx]

    return t, states


def plot_all_sl(
    t: np.ndarray, 
    s: np.ndarray, 
    n_series: int, 
    n_fibrils: int, 
    sn: int, 
    sl_idx: int,
    axes: Optional[np.ndarray] = None,
    filename: Optional[Union[str, Path]] = None
) -> np.ndarray:
    """
    Plots Sarcomere Length (SL) for each unit in the 2D array.
    """
    # Cap grid size at 10x10 for readability
    n_cols = min(10, n_series)
    n_rows = min(10, n_fibrils)
    
    if axes is None:
        fig, axes = plt.subplots(n_rows, n_cols, sharex=True, sharey=True, 
                                 figsize=(n_cols * 2, n_rows * 1.5), squeeze=False)

    for j in range(n_rows):
        axes[j, 0].set_ylabel('SL (μm)')
        for i in range(n_cols):
            # Calculate flat index: fibril_offset + series_offset + sl_internal_index
            idx = (j * n_series * sn) + (i * sn) + sl_idx
            axes[j, i].plot(t, s[:, idx])
            axes[j, i].grid(True, alpha=0.3)
            if j == n_rows - 1:
                axes[j, i].set_xlabel('Time (ms)')

    if filename:
        plt.tight_layout()
        plt.savefig(filename)
        
    return axes


def plot_total_force(
    t: np.ndarray, 
    s: np.ndarray, 
    n_series: int, 
    n_fibrils: int, 
    k_se: float = 100.0,
    ax: Optional[plt.Axes] = None,
    filename: Optional[Union[str, Path]] = None
) -> plt.Axes:
    """
    Calculates and plots the mean afterload across myofibrils.
    """
    if ax is None:
        fig, ax = plt.subplots()
        
    total_sarcs = n_series * n_fibrils
    
    # Z-displacements are stored at the end of the state vector
    x_total = s[:, -1 : -total_sarcs - 1 : -n_series]

    afterload = -x_total * k_se
    mean_afterload = np.mean(afterload, axis=1)

    ax.plot(t, mean_afterload)
    ax.set_ylabel('Force')
    ax.set_xlabel('Time (ms)')
    ax.set_title('Total Array Force')
    
    if filename:
        plt.savefig(filename)
        
    return ax