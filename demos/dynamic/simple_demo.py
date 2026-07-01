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


contraction_model = contr_models.rice_model_modified_new


N_SERIES = 5
N_FIBRILS = 3
    
overlap_func = OverlapRice(len_thin=1.4, len_thick=1.45)

current_dir = Path(__file__).resolve().parent
repo_root = current_dir.parent.parent
ca_trace_path = repo_root / "data" / "ca_data" / "ca_trace.dat"

try:
    ca_func = CaTransientFromFile(str(ca_trace_path))
except FileNotFoundError:
    print(f"Warning: {ca_trace_path.name} not found. Falling back to a dummy Ca transient.")
    ca_func = lambda t: 0.001
    
array_model = SarcArray2D(
    n_series=N_SERIES, 
    n_fibrils=N_FIBRILS, 
    model=contraction_model, 
    default_ca_func=ca_func,
    overlap_func=overlap_func
)
    
sample_sl = np.full((N_FIBRILS, N_SERIES), 1.85)
sample_sl[1, 1:4] = [1.8, 1.8, 1.95]
highlight_sarcs = [(1, 1), (1, 2), (1, 3)]
    
# plot the sarc array and save the color map for later:
colors = plot_sarc_array('sarcomere_visual.pdf', sample_sl, plot_sarcs=highlight_sarcs)
    
init = array_model.init_state_values({
    (1, 1): {'SL': 1.8}, 
    (1, 2): {'SL': 1.8}, 
    (1, 3): {'SL': 1.95}
})
    
params = array_model.init_parameter_values({
    'k_im': 0.05, 
    'k_se': 100, 
    'all': {'T_ref': 2.0, 'SLrest': 1.85},
    (1, 1): {'SLset': 1.8},
    (1, 2): {'SLset': 1.8},
    (1, 3): {'SLset': 1.95}
})
    
t, s = array_model.simulate(800, init, (params,), method='Radau')
SLind = contraction_model.state_indices("SL")
t0, s0 = get_results(t, s, N_SERIES, N_FIBRILS, SLind, highlight_sarcs)    
    
plt.figure()
for i in range(len(highlight_sarcs)):
    plt.plot(t0, s0[:, i], color=colors[i], label=f'Sarc {highlight_sarcs[i]}')

plt.xlabel('Time (ms)')
plt.ylabel('Sarcomere Length (μm)')
plt.legend()

plt.show()