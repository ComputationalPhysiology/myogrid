# Gotran generated code for the "rice_model_2008" model

import numpy as np
import math


def init_state_values(**values):
    """
    Initialize state values
    """
    # Init values
    # intf=-4.5113452510363e-06, SL=1.5,
    # TRPNCaL=0.0147730085063734, TRPNCaH=0.13066096561522,
    # N=0.999997834540066, XBpostr=1.81017564383744e-06,
    # XBprer=3.0494964880038e-07, xXBprer=3.41212828972468e-08,
    # xXBpostr=0.00700005394873882
    init_values = np.array([-4.5113452510363e-06, 1.85,\
        0.0147730085063734, 0.13066096561522, 0.999997834540066,\
        1.81017564383744e-06, 3.0494964880038e-07, 3.41212828972468e-08,\
        0.00700005394873882], dtype=np.float_)

    # State indices and limit checker
    state_ind = dict([("intf", 0), ("SL", 1), ("TRPNCaL", 2), ("TRPNCaH", 3),\
        ("N", 4), ("XBpostr", 5), ("XBprer", 6), ("xXBprer", 7), ("xXBpostr",\
        8)])

    for state_name, value in values.items():
        if state_name not in state_ind:
            raise ValueError("{0} is not a state.".format(state_name))
        ind = state_ind[state_name]

        # Assign value
        init_values[ind] = value

    return init_values

def init_parameter_values(**values):
    """
    Initialize parameter values
    """
    # Param values
    # Qfapp=6.25, Qgapp=2.5, Qgxb=6.25, Qhb=6.25, Qhf=6.25, fapp=0.5,
    # gapp=0.07, gslmod=6, gxb=0.07, hb=0.4, hbmdc=0, hf=2,
    # hfmdc=5, sigman=1, sigmap=8, xbmodsp=1, PCon_c=0.02,
    # PCon_t=0.002, PExp_c=70, PExp_t=10, SL_c=2.25, SLmax=2.4,
    # SLmin=1.4, SLrest=1.85, SLset=1.9, applied_stretch=0,
    # kxb_normalised=120, visc=0.03, Ca_amplitude=1.45,
    # Ca_diastolic=0.09, start_time=5, tau1=20, tau2=110, TmpC=24,
    # len_hbare=0.1, len_thick=1.65, len_thin=1.2, x_0=0.007,
    # Qkn_p=1.6, Qkoff=1.3, Qkon=1.5, Qkp_n=1.6, kn_p=0.5,
    # koffH=0.025, koffL=0.25, koffmod=1, kon=0.05, kp_n=0.05,
    # nperm=15, perm50=0.5, xPsi=2, Trop_conc=70, kxb=120, T_ref=1.0
    init_values = np.array([6.25, 2.5, 6.25, 6.25, 6.25, 0.5, 0.07, 6, 0.07,\
        0.4, 0, 2, 5, 1, 8, 1, 0.02, 0.002, 70, 10, 2.25, 2.4, 1.4, 1.85,\
        1.9, 0, 120, 0.03, 1.45, 0.09, 5, 20, 110, 24, 0.1, 1.65, 1.2, 0.007,\
        1.6, 1.3, 1.5, 1.6, 0.5, 0.025, 0.25, 1, 0.05, 0.05, 15, 0.5, 2, 70,\
        120, 1.0], dtype=np.float_)

    # Parameter indices and limit checker
    #Modified from Gotran file: added T_ref as parameter
    param_ind = dict([("Qfapp", 0), ("Qgapp", 1), ("Qgxb", 2), ("Qhb", 3),\
        ("Qhf", 4), ("fapp", 5), ("gapp", 6), ("gslmod", 7), ("gxb", 8),\
        ("hb", 9), ("hbmdc", 10), ("hf", 11), ("hfmdc", 12), ("sigman", 13),\
        ("sigmap", 14), ("xbmodsp", 15), ("PCon_c", 16), ("PCon_t", 17),\
        ("PExp_c", 18), ("PExp_t", 19), ("SL_c", 20), ("SLmax", 21),\
        ("SLmin", 22), ("SLrest", 23), ("SLset", 24), ("applied_stretch",\
        25), ("kxb_normalised", 26), ("visc", 27), ("Ca_amplitude", 28),\
        ("Ca_diastolic", 29), ("start_time", 30), ("tau1", 31), ("tau2", 32),\
        ("TmpC", 33), ("len_hbare", 34), ("len_thick", 35), ("len_thin", 36),\
        ("x_0", 37), ("Qkn_p", 38), ("Qkoff", 39), ("Qkon", 40), ("Qkp_n",\
        41), ("kn_p", 42), ("koffH", 43), ("koffL", 44), ("koffmod", 45),\
        ("kon", 46), ("kp_n", 47), ("nperm", 48), ("perm50", 49), ("xPsi",\
        50), ("Trop_conc", 51), ("kxb", 52), ("T_ref", 53)])

    for param_name, value in values.items():
        if param_name not in param_ind:
            raise ValueError("{0} is not a parameter.".format(param_name))
        ind = param_ind[param_name]

        # Assign value
        init_values[ind] = value

    return init_values

def state_indices(*states):
    """
    State indices
    """
    state_inds = dict([("intf", 0), ("SL", 1), ("TRPNCaL", 2), ("TRPNCaH",\
        3), ("N", 4), ("XBpostr", 5), ("XBprer", 6), ("xXBprer", 7),\
        ("xXBpostr", 8)])

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
    param_inds = dict([("Qfapp", 0), ("Qgapp", 1), ("Qgxb", 2), ("Qhb", 3),\
        ("Qhf", 4), ("fapp", 5), ("gapp", 6), ("gslmod", 7), ("gxb", 8),\
        ("hb", 9), ("hbmdc", 10), ("hf", 11), ("hfmdc", 12), ("sigman", 13),\
        ("sigmap", 14), ("xbmodsp", 15), ("PCon_c", 16), ("PCon_t", 17),\
        ("PExp_c", 18), ("PExp_t", 19), ("SL_c", 20), ("SLmax", 21),\
        ("SLmin", 22), ("SLrest", 23), ("SLset", 24), ("applied_stretch",\
        25), ("kxb_normalised", 26), ("visc", 27), ("Ca_amplitude", 28),\
        ("Ca_diastolic", 29), ("start_time", 30), ("tau1", 31), ("tau2", 32),\
        ("TmpC", 33), ("len_hbare", 34), ("len_thick", 35), ("len_thin", 36),\
        ("x_0", 37), ("Qkn_p", 38), ("Qkoff", 39), ("Qkon", 40), ("Qkp_n",\
        41), ("kn_p", 42), ("koffH", 43), ("koffL", 44), ("koffmod", 45),\
        ("kon", 46), ("kp_n", 47), ("nperm", 48), ("perm50", 49), ("xPsi",\
        50), ("Trop_conc", 51), ("kxb", 52), ("T_ref", 53)])

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
    monitor_inds = dict([("fappT", 0), ("gapslmd", 1), ("gappT", 2), ("hfmd",\
        3), ("hbmd", 4), ("hfT", 5), ("hbT", 6), ("gxbmd", 7), ("gxbT", 8),\
        ("SSXBprer", 9), ("SSXBpostr", 10), ("Fnordv", 11), ("force", 12),\
        ("active", 13), ("ppforce_t", 14), ("ppforce_c", 15), ("preload",\
        16), ("passive", 17), ("afterload", 18), ("total_force", 19), ("dSL",\
        20), ("beta", 21), ("Cai", 22), ("konT", 23), ("koffLT", 24),\
        ("koffHT", 25), ("dTRPNCaL", 26), ("dTRPNCaH", 27), ("Tropreg", 28),\
        ("perm50_on_Tropreg", 29), ("permtot", 30), ("inprmt", 31), ("kn_pT",\
        32), ("kp_nT", 33), ("dXBpostr", 34), ("P", 35), ("dXBprer", 36),\
        ("dutyprer", 37), ("dutypostr", 38), ("dxXBprer", 39), ("dxXBpostr",\
        40), ("FrSBXB", 41), ("dFrSBXB", 42), ("dsovr_ze", 43), ("dsovr_cle",\
        44), ("dlen_sovr", 45), ("dSOVFThin", 46), ("dSOVFThick", 47),\
        ("TropTot", 48), ("dTropTot", 49), ("dforce", 50), ("sovr_ze", 51),\
        ("sovr_cle", 52), ("len_sovr", 53), ("SOVFThick", 54), ("SOVFThin",\
        55), ("dintf_dt", 56), ("dSL_dt", 57), ("dTRPNCaL_dt", 58),\
        ("dTRPNCaH_dt", 59), ("dN_dt", 60), ("dXBpostr_dt", 61),\
        ("dXBprer_dt", 62), ("dxXBprer_dt", 63), ("dxXBpostr_dt", 64)])

    indices = []
    for monitor in monitored:
        if monitor not in monitor_inds:
            raise ValueError("Unknown monitored: '{0}'".format(monitor))
        indices.append(monitor_inds[monitor])
    if len(indices)>1:
        return indices
    else:
        return indices[0]



def rhs(states, t, parameters, ca_func, overlap_func, values = None):
    """
    Compute the right hand side of the rice_model_2008 ODE
    Modified from the Gotran-generated file, to take calcium transient
    and overlap function as arguments. 
    """

    # Assign states
    assert(len(states) == 9)
    SL=states[1]; TRPNCaL=states[2]; TRPNCaH=states[3]; N=states[4];\
        XBpostr=states[5]; XBprer=states[6]; xXBprer=states[7];\
        xXBpostr=states[8]

    # Assign parameters
    assert(len(parameters) == 54)
    Qfapp=parameters[0]; Qgapp=parameters[1]; Qgxb=parameters[2];\
        Qhb=parameters[3]; Qhf=parameters[4]; fapp=parameters[5];\
        gapp=parameters[6]; gslmod=parameters[7]; gxb=parameters[8];\
        hb=parameters[9]; hbmdc=parameters[10]; hf=parameters[11];\
        hfmdc=parameters[12]; sigman=parameters[13]; sigmap=parameters[14];\
        xbmodsp=parameters[15]; PCon_c=parameters[16]; PCon_t=parameters[17];\
        PExp_c=parameters[18]; PExp_t=parameters[19]; SL_c=parameters[20];\
        SLrest=parameters[23]; SLset=parameters[24];\
        applied_stretch=parameters[25]; kxb_normalised=parameters[26];\
        visc=parameters[27]; Ca_amplitude=parameters[28];\
        Ca_diastolic=parameters[29]; start_time=parameters[30];\
        tau1=parameters[31]; tau2=parameters[32]; TmpC=parameters[33];\
        len_hbare=parameters[34]; len_thick=parameters[35];\
        len_thin=parameters[36]; x_0=parameters[37]; Qkn_p=parameters[38];\
        Qkoff=parameters[39]; Qkon=parameters[40]; Qkp_n=parameters[41];\
        kn_p=parameters[42]; koffH=parameters[43]; koffL=parameters[44];\
        koffmod=parameters[45]; kon=parameters[46]; kp_n=parameters[47];\
        nperm=parameters[48]; perm50=parameters[49]; xPsi=parameters[50]; T_ref=parameters[53]

    # Init return args
    if values is None:
        values = np.zeros((9,), dtype=np.float_)
    else:
        assert isinstance(values, np.ndarray) and values.shape == (9,)

    # Expressions for the Sarcomere geometry component
    sovr_ze = (len_thick/2 if len_thick/2 < SL/2 else SL/2)
    sovr_cle = (len_thin - SL/2 if len_thin - SL/2 > len_hbare/2 else\
        len_hbare/2)
    len_sovr = -sovr_cle + sovr_ze
    
    #Modified: Using thick filament overlap function supplied as argument
    SOVFThick = overlap_func(SL) #2*len_sovr/(len_thick - len_hbare)
    SOVFThin = len_sovr/len_thin

    # Expressions for the Thin filament regulation and crossbridge cycling
    # rates component
    fappT = fapp*xbmodsp*math.pow(Qfapp, -37/10 + TmpC/10)
    gapslmd = 1 + gslmod*(1 - SOVFThick)
    gappT = gapp*xbmodsp*math.pow(Qgapp, -37/10 + TmpC/10)*gapslmd
    hfmd = math.exp(-hfmdc*(xXBprer*xXBprer)*math.copysign(1.0,\
        xXBprer)/(x_0*x_0))
    hbmd = math.exp(hbmdc*((-x_0 + xXBpostr)*(-x_0 +\
        xXBpostr))*math.copysign(1.0, -x_0 + xXBpostr)/(x_0*x_0))
    hfT = hf*xbmodsp*math.pow(Qhf, -37/10 + TmpC/10)*hfmd
    hbT = hb*xbmodsp*math.pow(Qhb, -37/10 + TmpC/10)*hbmd
    gxbmd = (math.exp(sigmap*((x_0 - xXBpostr)*(x_0 - xXBpostr))/(x_0*x_0))\
        if xXBpostr < x_0 else math.exp(sigman*((-x_0 + xXBpostr)*(-x_0 +\
        xXBpostr))/(x_0*x_0)))
    gxbT = gxb*xbmodsp*math.pow(Qgxb, -37/10 + TmpC/10)*gxbmd

    # Expressions for the Normalised active and passive force component
    SSXBpostr = fapp*hf/(fapp*gxb + fapp*hb + fapp*hf + gapp*gxb + gapp*hb +\
        gxb*hf)
    Fnordv = kxb_normalised*x_0*SSXBpostr
    force = kxb_normalised*(XBpostr*xXBpostr + XBprer*xXBprer)*SOVFThick
    active = T_ref * force/Fnordv
    ppforce_t = PCon_t*(-1 + math.exp(PExp_t*math.fabs(SLrest -\
        SL)))*math.copysign(1.0, -SLrest + SL)
    
    ppforce_c = (PCon_c*(-1 + math.exp(PExp_c*math.fabs(SL_c - SL))) if SL >\
        SL_c else 0)
    preload = PCon_t*(-1 + math.exp(PExp_t*math.fabs(SLrest -\
        SLset)))*math.copysign(1.0, SLset - SLrest)
    
    #Quick and dirty hack to change the passive model (also modified in monitored)
    #PCon_t = Cp; PExp_t = b_ff
    #ppforce_t = PCon_t*(-1 + math.exp(PExp_t*math.fabs(SLset -\
    #    SL)))*math.copysign(1.0, -SLset + SL)
    #passive = ppforce_t


    #May have to set the preload to zero for some sarcomere array cases
    #preload = 0

    passive = ppforce_c + ppforce_t
    afterload = applied_stretch
    total_force = active + passive
    dSL = (-total_force + afterload + preload)/visc
    values[0] = -total_force + afterload
    values[1] = dSL

    #Modified: Ca transient supplied as argument
    Cai = ca_func(t)

    """
    # Expressions for the Equation for simulated calcium transient component
    beta = math.pow(tau1/tau2, -1/(-1 + tau1/tau2)) - math.pow(tau1/tau2,\
        -1/(1 - tau2/tau1))
    Cai = (Ca_diastolic + (Ca_amplitude -\
        Ca_diastolic)*(-math.exp((start_time - t)/tau2) +\
        math.exp((start_time - t)/tau1))/beta if t > start_time else\
        Ca_diastolic)
    """
        
    # Expressions for the Ca binding to troponin to thin filament regulation
    # component
    konT = kon*math.pow(Qkon, -37/10 + TmpC/10)
    koffLT = koffL*koffmod*math.pow(Qkoff, -37/10 + TmpC/10)
    koffHT = koffH*koffmod*math.pow(Qkoff, -37/10 + TmpC/10)
    dTRPNCaL = -TRPNCaL*koffLT + (1 - TRPNCaL)*Cai*konT
    dTRPNCaH = -TRPNCaH*koffHT + (1 - TRPNCaH)*Cai*konT
    Tropreg = (1 - SOVFThin) * TRPNCaL + SOVFThin * TRPNCaH
    perm50_on_Tropreg = (perm50/Tropreg if Tropreg > 0.01 else 100*perm50)
    permtot = math.sqrt(math.fabs(1.0/(1 + math.pow(perm50_on_Tropreg,\
        nperm))))
    inprmt = (1.0/permtot if 1.0/permtot < 100 else 100)
    
    values[2] = dTRPNCaL
    values[3] = dTRPNCaH
    kn_pT = kn_p * math.pow(Qkn_p, -37/10 + TmpC/10) * permtot
    kp_nT = kp_n * math.pow(Qkp_n, -37/10 + TmpC/10) * inprmt

    # Expressions for the Regulation and crossbridge cycling state equations
    # component
    dXBpostr = XBprer*hfT - XBpostr*gxbT - XBpostr*hbT
    P = 1 - N - XBpostr - XBprer
    values[4] = P*kp_nT - N*kn_pT
    dXBprer = P*fappT + XBpostr*hbT - XBprer*gappT - XBprer*hfT
    values[5] = dXBpostr
    values[6] = dXBprer

    # Expressions for the Mean strain of strongly bound states component
    dutyprer = (fappT*gxbT + fappT*hbT)/(fappT*gxbT + fappT*hbT + fappT*hfT +\
        gappT*gxbT + gappT*hbT + gxbT*hfT)
    dutypostr = fappT*hfT/(fappT*gxbT + fappT*hbT + fappT*hfT + gappT*gxbT +\
        gappT*hbT + gxbT*hfT)
    dxXBprer = dSL/2 + xPsi*((-x_0 - xXBprer + xXBpostr)*hbT -\
        fappT*xXBprer)/dutyprer
    dxXBpostr = dSL/2 + xPsi*(x_0 - xXBpostr + xXBprer)*hfT/dutypostr
    values[7] = dxXBprer
    values[8] = dxXBpostr

    # Return results
    return values

def monitor(states, t, parameters, overlap_func, ca_func = None, monitored=None):
    """
    Computes monitored expressions of the rice_model_2008 ODE
    Modified from the Gotran-generated file, to take 
    overlap function and Ca func as argument. 
    """

    # Assign states
    assert(len(states) == 9)
    SL=states[1]; TRPNCaL=states[2]; TRPNCaH=states[3]; N=states[4];\
        XBpostr=states[5]; XBprer=states[6]; xXBprer=states[7];\
        xXBpostr=states[8]


    # Assign parameters
    assert(len(parameters) == 54)
    Qfapp=parameters[0]; Qgapp=parameters[1]; Qgxb=parameters[2];\
        Qhb=parameters[3]; Qhf=parameters[4]; fapp=parameters[5];\
        gapp=parameters[6]; gslmod=parameters[7]; gxb=parameters[8];\
        hb=parameters[9]; hbmdc=parameters[10]; hf=parameters[11];\
        hfmdc=parameters[12]; sigman=parameters[13]; sigmap=parameters[14];\
        xbmodsp=parameters[15]; PCon_c=parameters[16]; PCon_t=parameters[17];\
        PExp_c=parameters[18]; PExp_t=parameters[19]; SL_c=parameters[20];\
        SLrest=parameters[23]; SLset=parameters[24];\
        applied_stretch=parameters[25]; kxb_normalised=parameters[26];\
        visc=parameters[27]; Ca_amplitude=parameters[28];\
        Ca_diastolic=parameters[29]; start_time=parameters[30];\
        tau1=parameters[31]; tau2=parameters[32]; TmpC=parameters[33];\
        len_hbare=parameters[34]; len_thick=parameters[35];\
        len_thin=parameters[36]; x_0=parameters[37]; Qkn_p=parameters[38];\
        Qkoff=parameters[39]; Qkon=parameters[40]; Qkp_n=parameters[41];\
        kn_p=parameters[42]; koffH=parameters[43]; koffL=parameters[44];\
        koffmod=parameters[45]; kon=parameters[46]; kp_n=parameters[47];\
        nperm=parameters[48]; perm50=parameters[49]; xPsi=parameters[50];\
        Trop_conc=parameters[51]; kxb=parameters[52];T_ref=parameters[53]

    # Init return args
    if monitored is None:
        monitored = np.zeros((65,), dtype=np.float_)
    else:
        assert isinstance(monitored, np.ndarray) and monitored.shape == (65,)

    # Expressions for the Sarcomere geometry component
    monitored[51] = (len_thick/2 if len_thick/2 < SL/2 else SL/2)
    monitored[52] = (len_thin - SL/2 if len_thin - SL/2 > len_hbare/2 else\
        len_hbare/2)
    monitored[53] = -monitored[52] + monitored[51]
    #Modified: using overlap function supplied as argument
    monitored[54] = overlap_func(SL) #2*monitored[53]/(len_thick - len_hbare)
    monitored[55] = monitored[53]/len_thin

    # Expressions for the Thin filament regulation and crossbridge cycling
    # rates component
    monitored[0] = fapp*xbmodsp*math.pow(Qfapp, -37/10 + TmpC/10)
    monitored[1] = 1 + gslmod*(1 - monitored[54])
    monitored[2] = gapp*xbmodsp*math.pow(Qgapp, -37/10 + TmpC/10)*monitored[1]
    monitored[3] = math.exp(-hfmdc*(xXBprer*xXBprer)*math.copysign(1.0,\
        xXBprer)/(x_0*x_0))
    monitored[4] = math.exp(hbmdc*((-x_0 + xXBpostr)*(-x_0 +\
        xXBpostr))*math.copysign(1.0, -x_0 + xXBpostr)/(x_0*x_0))
    monitored[5] = hf*xbmodsp*math.pow(Qhf, -37/10 + TmpC/10)*monitored[3]
    monitored[6] = hb*xbmodsp*math.pow(Qhb, -37/10 + TmpC/10)*monitored[4]
    monitored[7] = (math.exp(sigmap*((x_0 - xXBpostr)*(x_0 -\
        xXBpostr))/(x_0*x_0)) if xXBpostr < x_0 else math.exp(sigman*((-x_0 +\
        xXBpostr)*(-x_0 + xXBpostr))/(x_0*x_0)))
    monitored[8] = gxb*xbmodsp*math.pow(Qgxb, -37/10 + TmpC/10)*monitored[7]

    # Expressions for the Normalised active and passive force component
    monitored[9] = (fapp*gxb + fapp*hb)/(fapp*gxb + fapp*hb + fapp*hf +\
        gapp*gxb + gapp*hb + gxb*hf)
    monitored[10] = fapp*hf/(fapp*gxb + fapp*hb + fapp*hf + gapp*gxb +\
        gapp*hb + gxb*hf)
    monitored[11] = kxb_normalised*x_0*monitored[10]
    monitored[12] = kxb_normalised*(XBpostr*xXBpostr +\
        XBprer*xXBprer)*monitored[54]
    
    monitored[13] = T_ref * monitored[12]/monitored[11]
    monitored[14] = PCon_t*(-1 + math.exp(PExp_t*math.fabs(SLrest -\
        SL)))*math.copysign(1.0, -SLrest + SL)
    monitored[15] = (PCon_c*(-1 + math.exp(PExp_c*math.fabs(SL_c - SL))) if\
        SL > SL_c else 0)
    monitored[16] = PCon_t*(-1 + math.exp(PExp_t*math.fabs(SLrest -\
        SLset)))*math.copysign(1.0, SLset - SLrest)
    monitored[17] = monitored[14] + monitored[15]
    monitored[18] = applied_stretch
    monitored[19] = monitored[13] + monitored[17]
    monitored[20] = (-monitored[19] + monitored[16] + monitored[18])/visc
    monitored[56] = -monitored[19] + monitored[18]
    monitored[57] = monitored[20]

    # Expressions for the Equation for simulated calcium transient component
    
    monitored[21] = math.pow(tau1/tau2, -1/(-1 + tau1/tau2)) -\
        math.pow(tau1/tau2, -1/(1 - tau2/tau1))
    if ca_func == None:
        monitored[22] = (Ca_diastolic + (Ca_amplitude -\
            Ca_diastolic)*(-math.exp((start_time - t)/tau2) +\
            math.exp((start_time - t)/tau1))/monitored[21] if t > start_time else\
            Ca_diastolic)
    else: 
        monitored[22] = ca_func(t)

    
    # Expressions for the Ca binding to troponin to thin filament regulation
    # component
    monitored[23] = kon*math.pow(Qkon, -37/10 + TmpC/10)
    monitored[24] = koffL*koffmod*math.pow(Qkoff, -37/10 + TmpC/10)
    monitored[25] = koffH*koffmod*math.pow(Qkoff, -37/10 + TmpC/10)
    monitored[26] = -TRPNCaL*monitored[24] + (1 -\
        TRPNCaL)*monitored[22]*monitored[23]
    monitored[27] = -TRPNCaH*monitored[25] + (1 -\
        TRPNCaH)*monitored[22]*monitored[23]
    monitored[28] = (1 - monitored[55])*TRPNCaL + TRPNCaH*monitored[55]
    monitored[29] = (perm50/monitored[28] if monitored[28] > 0.01 else\
        100*perm50)
    monitored[30] = math.sqrt(math.fabs(1.0/(1 + math.pow(monitored[29],\
        nperm))))
    monitored[31] = (1.0/monitored[30] if 1.0/monitored[30] < 100 else 100)
    monitored[58] = monitored[26]
    monitored[59] = monitored[27]
    monitored[32] = kn_p*math.pow(Qkn_p, -37/10 + TmpC/10)*monitored[30]
    monitored[33] = kp_n*math.pow(Qkp_n, -37/10 + TmpC/10)*monitored[31]

    # Expressions for the Regulation and crossbridge cycling state equations
    # component
    monitored[34] = XBprer*monitored[5] - XBpostr*monitored[6] -\
        XBpostr*monitored[8]
    monitored[35] = 1 - N - XBpostr - XBprer
    monitored[60] = monitored[33]*monitored[35] - N*monitored[32]
    monitored[36] = XBpostr*monitored[6] + monitored[0]*monitored[35] -\
        XBprer*monitored[2] - XBprer*monitored[5]
    monitored[61] = monitored[34]
    monitored[62] = monitored[36]

    # Expressions for the Mean strain of strongly bound states component
    monitored[37] = (monitored[0]*monitored[6] +\
        monitored[0]*monitored[8])/(monitored[0]*monitored[5] +\
        monitored[0]*monitored[6] + monitored[0]*monitored[8] +\
        monitored[2]*monitored[6] + monitored[2]*monitored[8] +\
        monitored[5]*monitored[8])
    monitored[38] = monitored[0]*monitored[5]/(monitored[0]*monitored[5] +\
        monitored[0]*monitored[6] + monitored[0]*monitored[8] +\
        monitored[2]*monitored[6] + monitored[2]*monitored[8] +\
        monitored[5]*monitored[8])
    monitored[39] = monitored[20]/2 + xPsi*((-x_0 - xXBprer +\
        xXBpostr)*monitored[6] - monitored[0]*xXBprer)/monitored[37]
    monitored[40] = monitored[20]/2 + xPsi*(x_0 - xXBpostr +\
        xXBprer)*monitored[5]/monitored[38]
    monitored[63] = monitored[39]
    monitored[64] = monitored[40]

    # Expressions for the Calculation of micromolar per millisecondes of Ca
    # for apparent Ca binding component
    monitored[41] = (XBpostr + XBprer)/(monitored[10] + monitored[9])
    monitored[42] = (monitored[34] + monitored[36])/(monitored[10] +\
        monitored[9])
    monitored[43] = (-0.5*monitored[20] if SL < len_thick else 0)
    monitored[44] = (-0.5*monitored[20] if -SL + 2*len_thin > len_hbare else 0)
    monitored[45] = -monitored[44] + monitored[43]
    monitored[46] = monitored[45]/len_thin
    monitored[47] = 2*monitored[45]/(len_thick - len_hbare)
    monitored[48] = Trop_conc*((1 - monitored[55])*TRPNCaL + ((1 -\
        monitored[41])*TRPNCaL + TRPNCaH*monitored[41])*monitored[55])
    monitored[49] = Trop_conc*((1 - monitored[55])*monitored[26] + ((1 -\
        monitored[41])*TRPNCaL + TRPNCaH*monitored[41])*monitored[46] + ((1 -\
        monitored[41])*monitored[26] + TRPNCaH*monitored[42] +\
        monitored[27]*monitored[41] - TRPNCaL*monitored[42])*monitored[55] -\
        TRPNCaL*monitored[46])
    monitored[50] = kxb*(XBpostr*xXBpostr + XBprer*xXBprer)*monitored[47] +\
        kxb*(XBpostr*monitored[40] + XBprer*monitored[39] +\
        monitored[34]*xXBpostr + monitored[36]*xXBprer)*monitored[54]

    # Return results
    return monitored
