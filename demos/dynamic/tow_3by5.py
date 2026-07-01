import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from myogrid.overlap import OverlapRice
from myogrid.dynamic import (
    SarcArray2D,
    contr_models    
)
from myogrid.dynamic.plot_functions import plot_sarc_array, get_results
from myogrid.dynamic.ca_transients import CaTransientFromFile
from myogrid.dynamic.ca_transients import CaTransientFromFile

contraction_model = contr_models.rice_model_modified_new
def main():
    figure_dir = 'tow_plots'
    if not os.path.isdir(figure_dir):
        os.makedirs(figure_dir)

    no_sarc_series = 5
    no_myofib = 3

    # These four lines are for plotting the sarcomere array and saving the color map:
    SLarr = np.array([[2.0] * no_sarc_series, [2.0] * no_sarc_series, [2.0] * no_sarc_series])
    sarcs_to_plot = [(1, 1), (1, 2), (1, 3)]
    filename = os.path.join(figure_dir, 'tow_array.pdf')
    colors = plot_sarc_array(filename, SLarr, sarcs_to_plot, True)

    overlap_func = OverlapRice(len_thin=1.4, len_thick=1.45)
    
    current_dir = Path(__file__).resolve().parent
    repo_root = current_dir.parent.parent
    ca_shortening_path = repo_root / "data" / "ca_data" / "hf_shortening.dat"
    ca_tow_path = repo_root / "data" / "ca_data" / "hf_tow.dat"

    hf_shortening_ca = CaTransientFromFile(str(ca_shortening_path), scale=1.0)
    hf_tow_ca = CaTransientFromFile(str(ca_tow_path), scale=1.0)

    sarc3by5 = SarcArray2D(
        no_sarc_series, 
        no_myofib, 
        model=contraction_model, 
        default_ca_func=hf_shortening_ca, 
        overlap_func=overlap_func,
        ca_func_variations={(1, 2): hf_tow_ca}
    )
    
    SLind = contraction_model.state_indices("SL")
    t_stop = 1000
    SL = 2.0

    init = sarc3by5.init_state_values({
        'all': {'SL': 2.0}, 
        (1, 2): {'SL': SL}
    })
    
    params = sarc3by5.init_parameter_values({
        'k_im': 0.1, 
        'k_se': 0.25,
        'all': {'Cp': 0.002, 'b_ff': 10, 'xbmodsp': 1.0, 'visc': 3.0, 'T_ref': 15.0, 'SLrest': 2.0, 'SLset': 2.0},
        (1, 1): {'Cp': 0.002, 'b_ff': 10, 'xbmodsp': 1.0, 'visc': 3.0, 'T_ref': 15.0, 'SLrest': 2.0, 'SLset': SL}
    })

    p = (params,)
    
    # solve ODEs and extract results from selected plots:
    t, s = sarc3by5.simulate(t_stop, init, p, method='Radau')
    t0, s0 = get_results(t, s, no_sarc_series, no_myofib, SLind, sarcs_to_plot)

    plt.figure()
    for i in range(len(sarcs_to_plot)):
        plt.plot(t0, s0[:, i], color=colors[i], label=f'Sarc {sarcs_to_plot[i]}')

    plt.xlabel('Time (ms)')
    plt.ylabel('Sarcomere Length (μm)')
    plt.legend()
    
    filename = os.path.join(figure_dir, 'tow_curves.pdf')
    plt.savefig(filename)
    plt.show()

if __name__ == '__main__':
    main()