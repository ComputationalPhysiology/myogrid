import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional

def plot_sarc_array(filename, data, plot_sarcs = [(1,2)], plot_springs = True):
    labels = [str(i) for i in range(data.shape[0])]
    data_cum = data.cumsum(axis=1)

    grey_scales = plt.get_cmap('Greys')(
        np.linspace(0.15, 0.85, data.shape[1]))

    colors = plt.get_cmap('Reds')(
        np.linspace(0.15, 0.85, len(plot_sarcs)))

    #category_colors[2,:] = [0.99707805, 0.9987697,  0.74502115, 1.]
    hsize, vsize = 10.0, 2.0
    fig, ax = plt.subplots(figsize=(hsize, vsize))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())


    for i, color in enumerate(grey_scales):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        b_height = 0.4
        barlist = ax.barh(labels, widths, left=starts, height=b_height, color=color,edgecolor ='k')
        xcenters = starts + widths / 2

        for index,s in enumerate(plot_sarcs):
            if s[1] == i:
                barlist[s[0]].set_facecolor(colors[index])

        if plot_springs:
            x = starts + widths
            y_start = b_height/2
            v_dist = 1.0
            y = np.array([y_start, -y_start+v_dist])
            for i in range(len(x)-1):
                plt.plot(x[i:i+2],y,linestyle='--',color='k')
                y += v_dist

        r, g, b, _ = color
        text_color = 'black' if r * g * b > 0.01 else 'white'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            #hack, does not work for general cases:
            xlow = widths[0]*plot_sarcs[1][1]
            xhigh = xlow+widths[0]
            y_plot = plot_sarcs[0][0]
            if xlow < x < xhigh and y == y_plot:
                ax.text(x, y, 'HF TOW', ha='center', va='center',
                        color=text_color)
            else:
                ax.text(x, y, 'HF Shortening', ha='center', va='center',
                        color=text_color)

    plt.savefig(filename)

    return colors #fig, ax



def plot_results(
    t: np.ndarray,
    s: np.ndarray,
    no_sarc_series: int,
    no_myofibrils: int,
    sl_ind: int,
    sarcs_to_plot: List[Tuple[int, int]],
    colors: np.ndarray
) -> None:
    """
    Plots the trajectories of specific state variables for highlighted sarcomeres.
    """
    sn = int(s.shape[1] / (no_sarc_series * no_myofibrils)) - 1

    for r, sarc in enumerate(sarcs_to_plot):
        j, i = sarc[0], sarc[1]
        idx = j * no_sarc_series * sn + sl_ind + i * sn
        plt.plot(t, s[:, idx], color=colors[r])


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
    filename: str = 'all_sarcomeres_sl.pdf'
) -> None:
    """
    Plots Sarcomere Length (SL) for each unit in the 2D array.
    """
    # Cap grid size at 10x10 for readability
    n_cols = min(10, n_series)
    n_rows = min(10, n_fibrils)
    
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

    plt.tight_layout()
    plt.savefig(filename)


def plot_total_force(
    ax: plt.Axes, 
    t: np.ndarray, 
    s: np.ndarray, 
    n_series: int, 
    n_fibrils: int, 
    k_se: float = 100.0
) -> None:
    """
    Calculates and plots the mean afterload across myofibrils.
    """
    total_sarcs = n_series * n_fibrils
    
    # Z-displacements are stored at the end of the state vector
    x_total = s[:, -1 : -total_sarcs - 1 : -n_series]

    afterload = -x_total * k_se
    mean_afterload = np.mean(afterload, axis=1)

    ax.plot(t, mean_afterload)
    ax.set_ylabel('Force')
    ax.set_xlabel('Time (ms)')