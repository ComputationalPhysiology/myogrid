import numpy as np
import matplotlib.pyplot as plt
from myogrid.overlap import OverlapRice
from myogrid.dynamic import (
    SarcArray2D,
    contr_model
)
from myogrid.dynamic.plot_functions import (
    plot_sarc_array, 
    plot_results, 
    get_results
)
from myogrid.dynamic.ca_transients import CaTransientFromFile


N_SERIES = 5
N_FIBRILS = 3
    
overlap_func = OverlapRice(len_thin=1.4, len_thick=1.45)
    
try:
    ca_func = CaTransientFromFile('../../data/ca_data/ca_trace.dat')
except FileNotFoundError:
    print("Warning: ca_trace.dat not found. Falling back to a dummy Ca transient.")
    ca_func = lambda t: 0.001
    
array_model = SarcArray2D(
    n_series=N_SERIES, 
    n_fibrils=N_FIBRILS, 
    model=contr_model, 
    default_ca_func=ca_func,
    overlap_func=overlap_func
)
    
sample_sl = np.full((N_FIBRILS, N_SERIES), 1.85)
sample_sl[1, 1:4] = [1.8, 1.8, 1.95]
highlight_sarcs = [(1, 1), (1, 2), (1, 3)]
    
#plot the sarc array and save the color map for later:
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
SLind = contr_model.state_indices("SL")
t0, s0 = get_results(t, s, N_SERIES, N_FIBRILS, SLind, highlight_sarcs)    
    
plt.figure()
for i in range(len(highlight_sarcs)):
    plt.plot(t0, s0[:, i], color=colors[i], label=f'Sarc {highlight_sarcs[i]}')

plt.xlabel('Time (ms)')
plt.ylabel('Sarcomere Length (μm)')
plt.legend()

plt.show()
  
