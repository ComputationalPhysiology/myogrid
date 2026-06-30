# Gotran generated code for the  "simple" model
from __future__ import division

def init_state_values(**values):
    """
    Initialize state values
    """
    # Imports
    import numpy as np
    from modelparameters.utils import Range

    # Init values
    # z=0.014417937837, SL=1.892, TRPN=0.067593139865
    init_values = np.array([0.014417937837, 1.85, 0.067593139865],\
        dtype=np.float_)

    # State indices and limit checker
    state_ind = dict([("z",(0, Range())), ("SL",(1, Range())), ("TRPN",(2,\
        Range()))])

    for state_name, value in values.items():
        if state_name not in state_ind:
            raise ValueError("{0} is not a state.".format(state_name))
        ind, range = state_ind[state_name]
        if value not in range:
            raise ValueError("While setting '{0}' {1}".format(state_name,\
                range.format_not_in(value)))

        # Assign value
        init_values[ind] = value

    return init_values

def init_parameter_values(**values):
    """
    Initialize parameter values
    """
    # Imports
    import numpy as np
    from modelparameters.utils import Range

    # Param values
    # SL_rest=1.85, SLset=1.85, beta_0=2.5, visc=3, applied_stretch=5.0,
    # k_passive=100.0, Ca_amplitude=1.45, Ca_diastolic=0.09,
    # start_time=5, tau1=20, tau2=110, Ca_50ref=0.00105, K_z=0.15,
    # alpha_0=0.008, alpha_r1=0.002, alpha_r2=0.00175, beta_1=-2,
    # n_Hill=3, n_Rel=3, z_p=0.85, T_ref=56.2, Ca_TRPN_Max=0.07,
    # gamma_trpn=2, k_Ref_off=0.2, k_on=100
    init_values = np.array([1.85, 1.85, 2.5, 3, 0.0, 100.0, 1.45, 0.09, 5, 20,\
        110, 0.00105, 0.15, 0.008, 0.002, 0.00175, -2, 3, 3, 0.85, 56.2,\
        0.07, 2, 0.2, 100], dtype=np.float_)

    # Parameter indices and limit checker
    param_ind = dict([("SL_rest", (0, Range())), ("SLset", (1, Range())),\
        ("beta_0", (2, Range())), ("visc", (3, Range())), ("applied_stretch",\
        (4, Range())), ("k_passive", (5, Range())), ("Ca_amplitude", (6,\
        Range())), ("Ca_diastolic", (7, Range())), ("start_time", (8,\
        Range())), ("tau1", (9, Range())), ("tau2", (10, Range())),\
        ("Ca_50ref", (11, Range())), ("K_z", (12, Range())), ("alpha_0", (13,\
        Range())), ("alpha_r1", (14, Range())), ("alpha_r2", (15, Range())),\
        ("beta_1", (16, Range())), ("n_Hill", (17, Range())), ("n_Rel", (18,\
        Range())), ("z_p", (19, Range())), ("T_ref", (20, Range())),\
        ("Ca_TRPN_Max", (21, Range())), ("gamma_trpn", (22, Range())),\
        ("k_Ref_off", (23, Range())), ("k_on", (24, Range()))])

    for param_name, value in values.items():
        if param_name not in param_ind:
            raise ValueError("{0} is not a parameter.".format(param_name))
        ind, range = param_ind[param_name]
        if value not in range:
            raise ValueError("While setting '{0}' {1}".format(param_name,\
                range.format_not_in(value)))

        # Assign value
        init_values[ind] = value

    return init_values

def state_indices(*states):
    """
    State indices
    """
    state_inds = dict([("z", 0), ("SL", 1), ("TRPN", 2)])

    indices = []
    for state in states:
        if state not in state_inds:
            raise ValueError("Unknown state: '{0}'".format(state))
        indices.append(state_inds[state])
    if len(indices)>1:
        return indices
    else:
        return indices[0]

def parameter_indices(*params):
    """
    Parameter indices
    """
    param_inds = dict([("SL_rest", 0), ("SLset", 1), ("beta_0", 2), ("visc",\
        3), ("applied_stretch", 4), ("k_passive", 5), ("Ca_amplitude", 6),\
        ("Ca_diastolic", 7), ("start_time", 8), ("tau1", 9), ("tau2", 10),\
        ("Ca_50ref", 11), ("K_z", 12), ("alpha_0", 13), ("alpha_r1", 14),\
        ("alpha_r2", 15), ("beta_1", 16), ("n_Hill", 17), ("n_Rel", 18),\
        ("z_p", 19), ("T_ref", 20), ("Ca_TRPN_Max", 21), ("gamma_trpn", 22),\
        ("k_Ref_off", 23), ("k_on", 24)])

    indices = []
    for param in params:
        if param not in param_inds:
            raise ValueError("Unknown param: '{0}'".format(param))
        indices.append(param_inds[param])
    if len(indices)>1:
        return indices
    else:
        return indices[0]

def monitor_indices(*monitored):
    """
    Monitor indices
    """
    monitor_inds = dict([("overlap", 0), ("passive", 1), ("beta", 2), ("Cai",\
        3), ("Ca_b", 4), ("K_2", 5), ("K_1", 6), ("Ca_50", 7), ("Ca_TRPN_50",\
        8), ("alpha_Tm", 9), ("beta_Tm", 10), ("z_max", 11), ("T_Base", 12),\
        ("k_off", 13), ("J_TRPN", 14), ("active", 15), ("total_force", 16),\
        ("dz_dt", 17), ("dSL_dt", 18), ("dTRPN_dt", 19)])

    indices = []
    for monitor in monitored:
        if monitor not in monitor_inds:
            raise ValueError("Unknown monitored: '{0}'".format(monitor))
        indices.append(monitor_inds[monitor])
    if len(indices)>1:
        return indices
    else:
        return indices[0]

def rhs(states, t, parameters, ca_func, values=None):
    """
    Compute the right hand side of the simple ODE
    """
    # Imports
    import numpy as np
    import math

    # Assign states
    assert(len(states) == 3)
    z, SL, TRPN = states

    # Assign parameters
    assert(len(parameters) == 25)
    SL_rest, SLset, beta_0, visc, applied_stretch, k_passive, Ca_amplitude,\
        Ca_diastolic, start_time, tau1, tau2, Ca_50ref, K_z, alpha_0,\
        alpha_r1, alpha_r2, beta_1, n_Hill, n_Rel, z_p, T_ref, Ca_TRPN_Max,\
        gamma_trpn, k_Ref_off, k_on = parameters

    # Init return args
    if values is None:
        values = np.zeros((3,), dtype=np.float_)
    else:
        assert isinstance(values, np.ndarray) and values.shape == (3,)

    # Expressions for the Equation for simulated calcium transient component
    #beta = math.pow(tau1/tau2, -1/(-1 + tau1/tau2)) - math.pow(tau1/tau2,\
    #    -1/(1 - tau2/tau1))
    #Cai = 0.001*(Ca_diastolic + (Ca_amplitude -\
    #    Ca_diastolic)*(-math.exp((start_time - t)/tau2) +\
    #    math.exp((start_time - t)/tau1))/beta if t > start_time else\
    #    Ca_diastolic)
    Cai = 0.001*ca_func(t)
    Ca_b = Ca_TRPN_Max - TRPN

    # Expressions for the Filament overlap component
    overlap = 1 + beta_0*(-SL_rest + SL)

    # Expressions for the Passive force component
    passive = k_passive*(-SLset + SL)

    # Expressions for the Tropomyosin component
    K_2 = alpha_r2*math.pow(z_p, n_Rel)*(1 - n_Rel*math.pow(K_z,\
        n_Rel)/(math.pow(K_z, n_Rel) + math.pow(z_p, n_Rel)))/(math.pow(K_z,\
        n_Rel) + math.pow(z_p, n_Rel))
    K_1 = alpha_r2*n_Rel*math.pow(K_z, n_Rel)*math.pow(z_p, -1 +\
        n_Rel)/((math.pow(K_z, n_Rel) + math.pow(z_p, n_Rel))*(math.pow(K_z,\
        n_Rel) + math.pow(z_p, n_Rel)))
    Ca_50 = Ca_50ref*(1 + beta_1*(-SL_rest + SL))
    Ca_TRPN_50 = Ca_TRPN_Max*Ca_50/(k_Ref_off*(1 - (0.5 +\
        0.5*beta_0*(-SL_rest + SL))/gamma_trpn)/k_on + Ca_50)
    alpha_Tm = alpha_0*math.pow(Ca_b/Ca_TRPN_50, n_Hill)
    beta_Tm = alpha_r1 + alpha_r2*math.pow(z, -1 + n_Rel)/(math.pow(K_z,\
        n_Rel) + math.pow(z, n_Rel))
    values[0] = (1 - z)*alpha_Tm - beta_Tm*z
    z_max = (-K_2 + alpha_0*math.pow(Ca_TRPN_50/Ca_TRPN_Max,\
        -n_Hill))/(alpha_r1 + alpha_0*math.pow(Ca_TRPN_50/Ca_TRPN_Max,\
        -n_Hill) + K_1)

    # Expressions for the Length independent tension component
    T_Base = T_ref*z/z_max

    # Expressions for the Isometric tension component
    active = T_Base*overlap
    total_force = active + passive
    values[1] = (applied_stretch - total_force)/visc
    #print('rhs', applied_stretch, active,passive,visc)
    #print("xtr",values[1])
    # Expressions for the Troponin component
    k_off = k_Ref_off
    J_TRPN = (Ca_TRPN_Max - TRPN)*k_off - k_on*Cai*TRPN

    # Expressions for the Intracellular ion concentrations component
    values[2] = J_TRPN

    # Return results
    return values

def monitor(states, t, parameters, monitored=None):
    """
    Computes monitored expressions of the simple ODE
    """
    # Imports
    import numpy as np
    import math

    # Assign states
    assert(len(states) == 3)
    z, SL, TRPN = states

    # Assign parameters
    assert(len(parameters) == 25)
    SL_rest, SLset, beta_0, visc, applied_stretch, k_passive, Ca_amplitude,\
        Ca_diastolic, start_time, tau1, tau2, Ca_50ref, K_z, alpha_0,\
        alpha_r1, alpha_r2, beta_1, n_Hill, n_Rel, z_p, T_ref, Ca_TRPN_Max,\
        gamma_trpn, k_Ref_off, k_on = parameters

    # Init return args
    if monitored is None:
        monitored = np.zeros((20,), dtype=np.float_)
    else:
        assert isinstance(monitored, np.ndarray) and monitored.shape == (20,)

    # Expressions for the Equation for simulated calcium transient component
    monitored[2] = math.pow(tau1/tau2, -1/(-1 + tau1/tau2)) -\
        math.pow(tau1/tau2, -1/(1 - tau2/tau1))
    monitored[3] = 0.001*(Ca_diastolic + (Ca_amplitude -\
        Ca_diastolic)*(-math.exp((start_time - t)/tau2) +\
        math.exp((start_time - t)/tau1))/monitored[2] if t > start_time else\
        Ca_diastolic)
    monitored[4] = Ca_TRPN_Max - TRPN

    # Expressions for the Filament overlap component
    monitored[0] = 1 + beta_0*(-SL_rest + SL)

    # Expressions for the Passive force component
    monitored[1] = k_passive*(-SLset + SL)

    # Expressions for the Tropomyosin component
    monitored[5] = alpha_r2*math.pow(z_p, n_Rel)*(1 - n_Rel*math.pow(K_z,\
        n_Rel)/(math.pow(K_z, n_Rel) + math.pow(z_p, n_Rel)))/(math.pow(K_z,\
        n_Rel) + math.pow(z_p, n_Rel))
    monitored[6] = alpha_r2*n_Rel*math.pow(K_z, n_Rel)*math.pow(z_p, -1 +\
        n_Rel)/((math.pow(K_z, n_Rel) + math.pow(z_p, n_Rel))*(math.pow(K_z,\
        n_Rel) + math.pow(z_p, n_Rel)))
    monitored[7] = Ca_50ref*(1 + beta_1*(-SL_rest + SL))
    monitored[8] = Ca_TRPN_Max*monitored[7]/(k_Ref_off*(1 - (0.5 +\
        0.5*beta_0*(-SL_rest + SL))/gamma_trpn)/k_on + monitored[7])
    monitored[9] = alpha_0*math.pow(monitored[4]/monitored[8], n_Hill)
    monitored[10] = alpha_r1 + alpha_r2*math.pow(z, -1 +\
        n_Rel)/(math.pow(K_z, n_Rel) + math.pow(z, n_Rel))
    monitored[17] = (1 - z)*monitored[9] - monitored[10]*z
    monitored[11] = (-monitored[5] +\
        alpha_0*math.pow(monitored[8]/Ca_TRPN_Max, -n_Hill))/(alpha_r1 +\
        alpha_0*math.pow(monitored[8]/Ca_TRPN_Max, -n_Hill) + monitored[6])

    # Expressions for the Length independent tension component
    monitored[12] = T_ref*z/monitored[11]

    # Expressions for the Isometric tension component
    monitored[15] = monitored[0]*monitored[12]
    monitored[16] = monitored[15] + monitored[1]
    monitored[18] = (applied_stretch - monitored[16])/visc
    #print('moni', applied_stretch, monitored[15],monitored[1],visc)
    #print('xtr_m',monitored[18])
    #values[1] = (applied_stretch - total_force)/visc
    
    # Expressions for the Troponin component
    monitored[13] = k_Ref_off
    monitored[14] = (Ca_TRPN_Max - TRPN)*monitored[13] - k_on*TRPN*monitored[3]

    # Expressions for the Intracellular ion concentrations component
    monitored[19] = monitored[14]

    # Return results
    return monitored
