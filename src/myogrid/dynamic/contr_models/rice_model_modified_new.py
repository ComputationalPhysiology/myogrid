# Gotran generated code for the  "rice_model_modified" model
# NB: Slightly modified from the generated code

from __future__ import division

# from cellmodels.overlap import Overlap, OverlapRice, OverlapDummy


# global variable for now
# original version: overlap_func = Overlap(SL_zero=1.6,SL_low=1.7)
# version 2, overlap_func = OverlapRice(len_thin=1.4, len_thick=1.65)
# overlap_func = OverlapRice(len_thin=1.4, len_thick=1.45)
# overlap_func = OverlapRice() #SL_zero=1.6,SL_low=1.7)

# modified version with steeper LDA at SL < 1.7
# Used for figure 4 in original paper, and gives better match with experiments
# overlap_func = Overlap(SL_zero=1.6,SL_low=1.7)

# overlap_func = OverlapRice(len_thin=1.4,len_thick=1.4)

# default from Rice model
# overlap_func = Overlap()#SL_zero=1.6,SL_low=1.7)


def init_state_values(**values):
    """
    Initialize state values
    """
    # Imports
    import numpy as np
    from modelparameters.utils import Range

    # Init values
    # intf=-4.51134525104e-06, SL=1.85, TRPNCaL=0.0147730085064,
    # TRPNCaH=0.130660965615, N=0.99999783454, XBpostr=1.81017564384e-06,
    # XBprer=3.049496488e-07, xXBprer=3.41212828972e-08,
    # xXBpostr=0.00700005394874
    init_values = np.array(
        [
            -4.51134525104e-06,
            1.85,
            0.0147730085064,
            0.130660965615,
            0.99999783454,
            1.81017564384e-06,
            3.049496488e-07,
            3.41212828972e-08,
            0.00700005394874,
        ],
        dtype=np.float64,
    )

    # State indices and limit checker
    state_ind = dict(
        [
            ("intf", (0, Range())),
            ("SL", (1, Range())),
            ("TRPNCaL", (2, Range())),
            ("TRPNCaH", (3, Range())),
            ("N", (4, Range())),
            ("XBpostr", (5, Range())),
            ("XBprer", (6, Range())),
            ("xXBprer", (7, Range())),
            ("xXBpostr", (8, Range())),
        ]
    )

    for state_name, value in values.items():
        if state_name not in state_ind:
            raise ValueError("{0} is not a state.".format(state_name))
        ind, range = state_ind[state_name]
        if value not in range:
            raise ValueError(
                "While setting '{0}' {1}".format(state_name, range.format_not_in(value))
            )

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
    # Qfapp=6.25, Qgapp=2.5, Qgxb=6.25, Qhb=6.25, Qhf=6.25, fapp=0.5,
    # gapp=0.07, gslmod=6, gxb=0.07, hb=0.4, hbmdc=0, hf=2,
    # hfmdc=5, sigman=1, sigmap=8, xbmodsp=1, Cp=0.002, SLmax=2.4,
    # SLmin=1.4, SLrest=1.85, SLset=1.85, applied_stretch=0, b_ff=50.0,
    # kxb_normalised=120, visc=0.003, Ca_amplitude=1.45,
    # Ca_diastolic=0.09, start_time=5, tau1=20, tau2=110, TmpC=24,
    # len_hbare=0.1, len_thick=1.65, len_thin=1.2, x_0=0.007,
    # Qkn_p=1.6, Qkoff=1.3, Qkon=1.5, Qkp_n=1.6, kn_p=0.5,
    # koffH=0.025, koffL=0.25, koffmod=1, kon=0.05, kp_n=0.05,
    # nperm=15, perm50=0.5, xPsi=2, Trop_conc=70, kxb=120, T_ref=50
    init_values = np.array(
        [
            6.25,
            2.5,
            6.25,
            6.25,
            6.25,
            0.5,
            0.07,
            6,
            0.07,
            0.4,
            0,
            2,
            5,
            1,
            8,
            1,
            0.002,
            2.4,
            1.4,
            1.85,
            1.85,
            0,
            50.0,
            120,
            0.003,
            1.45,
            0.09,
            5,
            20,
            110,
            24,
            0.1,
            1.65,
            1.2,
            0.007,
            1.6,
            1.3,
            1.5,
            1.6,
            0.5,
            0.025,
            0.25,
            1,
            0.05,
            0.05,
            15,
            0.5,
            2,
            70,
            120,
            1.0,
        ],
        dtype=np.float64,
    )

    # Parameter indices and limit checker
    param_ind = dict(
        [
            ("Qfapp", (0, Range())),
            ("Qgapp", (1, Range())),
            ("Qgxb", (2, Range())),
            ("Qhb", (3, Range())),
            ("Qhf", (4, Range())),
            ("fapp", (5, Range())),
            ("gapp", (6, Range())),
            ("gslmod", (7, Range())),
            ("gxb", (8, Range())),
            ("hb", (9, Range())),
            ("hbmdc", (10, Range())),
            ("hf", (11, Range())),
            ("hfmdc", (12, Range())),
            ("sigman", (13, Range())),
            ("sigmap", (14, Range())),
            ("xbmodsp", (15, Range())),
            ("Cp", (16, Range())),
            ("SLmax", (17, Range())),
            ("SLmin", (18, Range())),
            ("SLrest", (19, Range())),
            ("SLset", (20, Range())),
            ("applied_stretch", (21, Range())),
            ("b_ff", (22, Range())),
            ("kxb_normalised", (23, Range())),
            ("visc", (24, Range())),
            ("Ca_amplitude", (25, Range())),
            ("Ca_diastolic", (26, Range())),
            ("start_time", (27, Range())),
            ("tau1", (28, Range())),
            ("tau2", (29, Range())),
            ("TmpC", (30, Range())),
            ("len_hbare", (31, Range())),
            ("len_thick", (32, Range())),
            ("len_thin", (33, Range())),
            ("x_0", (34, Range())),
            ("Qkn_p", (35, Range())),
            ("Qkoff", (36, Range())),
            ("Qkon", (37, Range())),
            ("Qkp_n", (38, Range())),
            ("kn_p", (39, Range())),
            ("koffH", (40, Range())),
            ("koffL", (41, Range())),
            ("koffmod", (42, Range())),
            ("kon", (43, Range())),
            ("kp_n", (44, Range())),
            ("nperm", (45, Range())),
            ("perm50", (46, Range())),
            ("xPsi", (47, Range())),
            ("Trop_conc", (48, Range())),
            ("kxb", (49, Range())),
            ("T_ref", (50, Range())),
        ]
    )

    for param_name, value in values.items():
        if param_name not in param_ind:
            raise ValueError("{0} is not a parameter.".format(param_name))
        ind, range = param_ind[param_name]
        if value not in range:
            raise ValueError(
                "While setting '{0}' {1}".format(param_name, range.format_not_in(value))
            )

        # Assign value
        init_values[ind] = value

    return init_values


def state_indices(*states):
    """
    State indices
    """
    state_inds = dict(
        [
            ("intf", 0),
            ("SL", 1),
            ("TRPNCaL", 2),
            ("TRPNCaH", 3),
            ("N", 4),
            ("XBpostr", 5),
            ("XBprer", 6),
            ("xXBprer", 7),
            ("xXBpostr", 8),
        ]
    )

    indices = []
    for state in states:
        if state not in state_inds:
            raise ValueError("Unknown state: '{0}'".format(state))
        indices.append(state_inds[state])
    if len(indices) > 1:
        return indices
    else:
        return indices[0]


def parameter_indices(*params):
    """
    Parameter indices
    """
    param_inds = dict(
        [
            ("Qfapp", 0),
            ("Qgapp", 1),
            ("Qgxb", 2),
            ("Qhb", 3),
            ("Qhf", 4),
            ("fapp", 5),
            ("gapp", 6),
            ("gslmod", 7),
            ("gxb", 8),
            ("hb", 9),
            ("hbmdc", 10),
            ("hf", 11),
            ("hfmdc", 12),
            ("sigman", 13),
            ("sigmap", 14),
            ("xbmodsp", 15),
            ("Cp", 16),
            ("SLmax", 17),
            ("SLmin", 18),
            ("SLrest", 19),
            ("SLset", 20),
            ("applied_stretch", 21),
            ("b_ff", 22),
            ("kxb_normalised", 23),
            ("visc", 24),
            ("Ca_amplitude", 25),
            ("Ca_diastolic", 26),
            ("start_time", 27),
            ("tau1", 28),
            ("tau2", 29),
            ("TmpC", 30),
            ("len_hbare", 31),
            ("len_thick", 32),
            ("len_thin", 33),
            ("x_0", 34),
            ("Qkn_p", 35),
            ("Qkoff", 36),
            ("Qkon", 37),
            ("Qkp_n", 38),
            ("kn_p", 39),
            ("koffH", 40),
            ("koffL", 41),
            ("koffmod", 42),
            ("kon", 43),
            ("kp_n", 44),
            ("nperm", 45),
            ("perm50", 46),
            ("xPsi", 47),
            ("Trop_conc", 48),
            ("kxb", 49),
            ("T_ref", 50),
        ]
    )

    indices = []
    for param in params:
        if param not in param_inds:
            raise ValueError("Unknown param: '{0}'".format(param))
        indices.append(param_inds[param])
    if len(indices) > 1:
        return indices
    else:
        return indices[0]


def monitor_indices(*monitored):
    """
    Monitor indices
    """
    monitor_inds = dict(
        [
            ("fappT", 0),
            ("gapslmd", 1),
            ("gappT", 2),
            ("hfmd", 3),
            ("hbmd", 4),
            ("hfT", 5),
            ("hbT", 6),
            ("gxbmd", 7),
            ("gxbT", 8),
            ("SSXBprer", 9),
            ("SSXBpostr", 10),
            ("Fnordv", 11),
            ("force", 12),
            ("active", 13),
            ("lmbda", 14),
            ("passive", 15),
            ("preload", 16),
            ("afterload", 17),
            ("total_force", 18),
            ("dSL", 19),
            ("beta", 20),
            ("Cai", 21),
            ("konT", 22),
            ("koffLT", 23),
            ("koffHT", 24),
            ("dTRPNCaL", 25),
            ("dTRPNCaH", 26),
            ("Tropreg", 27),
            ("perm50_on_Tropreg", 28),
            ("permtot", 29),
            ("inprmt", 30),
            ("kn_pT", 31),
            ("kp_nT", 32),
            ("dXBpostr", 33),
            ("P", 34),
            ("dXBprer", 35),
            ("dutyprer", 36),
            ("dutypostr", 37),
            ("dxXBprer", 38),
            ("dxXBpostr", 39),
            ("FrSBXB", 40),
            ("dFrSBXB", 41),
            ("dsovr_ze", 42),
            ("dsovr_cle", 43),
            ("dlen_sovr", 44),
            ("dSOVFThin", 45),
            ("dSOVFThick", 46),
            ("TropTot", 47),
            ("dTropTot", 48),
            ("dforce", 49),
            ("sovr_ze", 50),
            ("sovr_cle", 51),
            ("len_sovr", 52),
            ("SOVFThick", 53),
            ("SOVFThin", 54),
            ("dintf_dt", 55),
            ("dSL_dt", 56),
            ("dTRPNCaL_dt", 57),
            ("dTRPNCaH_dt", 58),
            ("dN_dt", 59),
            ("dXBpostr_dt", 60),
            ("dXBprer_dt", 61),
            ("dxXBprer_dt", 62),
            ("dxXBpostr_dt", 63),
        ]
    )

    indices = []
    for monitor in monitored:
        if monitor not in monitor_inds:
            raise ValueError("Unknown monitored: '{0}'".format(monitor))
        indices.append(monitor_inds[monitor])
    if len(indices) > 1:
        return indices
    else:
        return indices[0]


def rhs(states, t, parameters, ca_func, overlap_func, values=None):
    """
    Compute the right hand side of the rice_model_modified ODE
    """
    # Imports
    import numpy as np
    import math

    # Assign states
    assert len(states) == 9
    SL = states[1]
    TRPNCaL = states[2]
    TRPNCaH = states[3]
    N = states[4]
    XBpostr = states[5]
    XBprer = states[6]
    xXBprer = states[7]
    xXBpostr = states[8]

    # Assign parameters
    assert len(parameters) == 51
    Qfapp = parameters[0]
    Qgapp = parameters[1]
    Qgxb = parameters[2]
    Qhb = parameters[3]
    Qhf = parameters[4]
    fapp = parameters[5]
    gapp = parameters[6]
    gslmod = parameters[7]
    gxb = parameters[8]
    hb = parameters[9]
    hbmdc = parameters[10]
    hf = parameters[11]
    hfmdc = parameters[12]
    sigman = parameters[13]
    sigmap = parameters[14]
    xbmodsp = parameters[15]
    Cp = parameters[16]
    SLrest = parameters[19]
    SLset = parameters[20]
    applied_stretch = parameters[21]
    b_ff = parameters[22]
    kxb_normalised = parameters[23]
    visc = parameters[24]
    Ca_amplitude = parameters[25]
    Ca_diastolic = parameters[26]
    start_time = parameters[27]
    tau1 = parameters[28]
    tau2 = parameters[29]
    TmpC = parameters[30]
    len_hbare = parameters[31]
    len_thick = parameters[32]
    len_thin = parameters[33]
    x_0 = parameters[34]
    Qkn_p = parameters[35]
    Qkoff = parameters[36]
    Qkon = parameters[37]
    Qkp_n = parameters[38]
    kn_p = parameters[39]
    koffH = parameters[40]
    koffL = parameters[41]
    koffmod = parameters[42]
    kon = parameters[43]
    kp_n = parameters[44]
    nperm = parameters[45]
    perm50 = parameters[46]
    xPsi = parameters[47]
    T_ref = parameters[50]

    # Init return args
    if values is None:
        values = np.zeros((9,), dtype=np.float64)
    else:
        assert isinstance(values, np.ndarray) and values.shape == (9,)

    # Expressions for the Sarcomere geometry component
    sovr_ze = len_thick / 2 if len_thick / 2 < SL / 2 else SL / 2
    sovr_cle = len_thin - SL / 2 if len_thin - SL / 2 > len_hbare / 2 else len_hbare / 2
    len_sovr = -sovr_cle + sovr_ze

    SOVFThick = overlap_func(SL)  # 2*len_sovr/(len_thick - len_hbare)
    SOVFThin = len_sovr / len_thin  # overlap_func(SL)
    # print(len_sovr/len_thin)

    # Expressions for the Thin filament regulation and crossbridge cycling
    # rates component

    fappT = fapp * xbmodsp * math.pow(Qfapp, -37 / 10 + TmpC / 10)
    gapslmd = 1 + gslmod * (1 - SOVFThick)
    gappT = gapp * xbmodsp * math.pow(Qgapp, -37 / 10 + TmpC / 10) * gapslmd
    hfmd = math.exp(
        -hfmdc * (xXBprer * xXBprer) * math.copysign(1.0, xXBprer) / (x_0 * x_0)
    )
    hbmd = math.exp(
        hbmdc
        * ((-x_0 + xXBpostr) * (-x_0 + xXBpostr))
        * math.copysign(1.0, -x_0 + xXBpostr)
        / (x_0 * x_0)
    )

    """
    print(-hfmdc*(xXBprer*xXBprer)*math.copysign(1.0,\
        xXBprer)/(x_0*x_0))
    print('XT: ',hfmdc,math.copysign(1.0, xXBprer),x_0*x_0,xXBprer*xXBprer)
    if hfmd < 1e-5:
        print(hfmd)
        exit()
    """

    hfT = hf * xbmodsp * math.pow(Qhf, -37 / 10 + TmpC / 10) * hfmd
    hbT = hb * xbmodsp * math.pow(Qhb, -37 / 10 + TmpC / 10) * hbmd
    gxbmd = (
        math.exp(sigmap * ((x_0 - xXBpostr) * (x_0 - xXBpostr)) / (x_0 * x_0))
        if xXBpostr < x_0
        else math.exp(sigman * ((-x_0 + xXBpostr) * (-x_0 + xXBpostr)) / (x_0 * x_0))
    )
    gxbT = gxb * xbmodsp * math.pow(Qgxb, -37 / 10 + TmpC / 10) * gxbmd

    # Expressions for the Normalised active and passive force component
    SSXBpostr = (
        fapp
        * hf
        / (fapp * gxb + fapp * hb + fapp * hf + gapp * gxb + gapp * hb + gxb * hf)
    )

    Fnordv = kxb_normalised * x_0 * SSXBpostr
    force = kxb_normalised * (XBpostr * xXBpostr + XBprer * xXBprer) * SOVFThick
    active = T_ref * force / Fnordv
    lmbda = SL / SLset

    # Quick and dirty hack to change the passive model (also modified in monitored)
    PCon_t = Cp
    PExp_t = b_ff
    ppforce_t = (
        PCon_t
        * (-1 + math.exp(PExp_t * math.fabs(SLset - SL)))
        * math.copysign(1.0, -SLset + SL)
    )
    passive = ppforce_t

    # passive = Cp*b_ff*(-0.5 + 0.5*(lmbda*lmbda))*math.exp(b_ff*((-0.5 +\
    #    0.5*(lmbda*lmbda))*(-0.5 + 0.5*(lmbda*lmbda))))

    """ preload should come from external model
    preload = Cp*b_ff*(-0.5 +\
        0.5*(SLset*SLset)/(SLrest*SLrest))*math.exp(b_ff*((-0.5 +\
        0.5*(SLset*SLset)/(SLrest*SLrest))*(-0.5 +\
        0.5*(SLset*SLset)/(SLrest*SLrest))))
    """
    preload = 0

    afterload = applied_stretch
    # print(afterload)
    total_force = -preload + active + passive
    # print('Total_force:', total_force, preload, active, passive)
    dSL = (-total_force + afterload) / visc
    values[0] = -total_force + afterload
    values[1] = dSL
    # print dSL, active, passive, afterload
    # Expressions for the Equation for simulated calcium transient component
    Cai = ca_func(t)

    # Expressions for the Ca binding to troponin to thin filament regulation
    # component
    konT = kon * math.pow(Qkon, -37 / 10 + TmpC / 10)
    koffLT = koffL * koffmod * math.pow(Qkoff, -37 / 10 + TmpC / 10)
    koffHT = koffH * koffmod * math.pow(Qkoff, -37 / 10 + TmpC / 10)
    dTRPNCaL = -TRPNCaL * koffLT + (1 - TRPNCaL) * Cai * konT
    dTRPNCaH = -TRPNCaH * koffHT + (1 - TRPNCaH) * Cai * konT
    Tropreg = (1 - SOVFThin) * TRPNCaL + SOVFThin * TRPNCaH
    perm50_on_Tropreg = perm50 / Tropreg if Tropreg > 0.01 else 100 * perm50
    permtot = math.sqrt(math.fabs(1.0 / (1 + math.pow(perm50_on_Tropreg, nperm))))
    inprmt = 1.0 / permtot if 1.0 / permtot < 100 else 100
    values[2] = dTRPNCaL
    values[3] = dTRPNCaH
    kn_pT = kn_p * math.pow(Qkn_p, -37 / 10 + TmpC / 10) * permtot
    kp_nT = kp_n * math.pow(Qkp_n, -37 / 10 + TmpC / 10) * inprmt

    # Expressions for the Regulation and crossbridge cycling state equations
    # component
    dXBpostr = XBprer * hfT - XBpostr * gxbT - XBpostr * hbT
    P = 1 - N - XBpostr - XBprer
    values[4] = P * kp_nT - N * kn_pT
    dXBprer = P * fappT + XBpostr * hbT - XBprer * gappT - XBprer * hfT
    # print(dXBprer,dXBpostr)

    values[5] = dXBpostr
    values[6] = dXBprer

    # hfT = max(hfT,1e-6)
    # Expressions for the Mean strain of strongly bound states component
    dutyprer = (fappT * gxbT + fappT * hbT) / (
        fappT * gxbT
        + fappT * hbT
        + fappT * hfT
        + gappT * gxbT
        + gappT * hbT
        + gxbT * hfT
    )
    dutypostr = (
        fappT
        * hfT
        / (
            fappT * gxbT
            + fappT * hbT
            + fappT * hfT
            + gappT * gxbT
            + gappT * hbT
            + gxbT * hfT
        )
    )

    """
    print(dutyprer, dutypostr)
    print(fappT, hfT, gxbT, hbT, gappT)
    if dutypostr < 1e-5:
        exit()
    """

    dxXBprer = (
        dSL / 2
        + xPsi * ((-x_0 - xXBprer + xXBpostr) * hbT - fappT * xXBprer) / dutyprer
    )
    dxXBpostr = dSL / 2 + xPsi * (x_0 - xXBpostr + xXBprer) * hfT / dutypostr
    # print(dutypostr,hfT)
    # if dutypostr < 1e-8:
    #    exit()
    values[7] = dxXBprer
    values[8] = dxXBpostr

    # Return results
    return values


def monitor(states, t, parameters, overlap_func, monitored=None):
    """
    Computes monitored expressions of the rice_model_modified ODE
    """
    # Imports
    import numpy as np
    import math

    # Assign states
    assert len(states) == 9
    SL = states[1]
    TRPNCaL = states[2]
    TRPNCaH = states[3]
    N = states[4]
    XBpostr = states[5]
    XBprer = states[6]
    xXBprer = states[7]
    xXBpostr = states[8]

    # Assign parameters
    assert len(parameters) == 51
    Qfapp = parameters[0]
    Qgapp = parameters[1]
    Qgxb = parameters[2]
    Qhb = parameters[3]
    Qhf = parameters[4]
    fapp = parameters[5]
    gapp = parameters[6]
    gslmod = parameters[7]
    gxb = parameters[8]
    hb = parameters[9]
    hbmdc = parameters[10]
    hf = parameters[11]
    hfmdc = parameters[12]
    sigman = parameters[13]
    sigmap = parameters[14]
    xbmodsp = parameters[15]
    Cp = parameters[16]
    SLrest = parameters[19]
    SLset = parameters[20]
    applied_stretch = parameters[21]
    b_ff = parameters[22]
    kxb_normalised = parameters[23]
    visc = parameters[24]
    Ca_amplitude = parameters[25]
    Ca_diastolic = parameters[26]
    start_time = parameters[27]
    tau1 = parameters[28]
    tau2 = parameters[29]
    TmpC = parameters[30]
    len_hbare = parameters[31]
    len_thick = parameters[32]
    len_thin = parameters[33]
    x_0 = parameters[34]
    Qkn_p = parameters[35]
    Qkoff = parameters[36]
    Qkon = parameters[37]
    Qkp_n = parameters[38]
    kn_p = parameters[39]
    koffH = parameters[40]
    koffL = parameters[41]
    koffmod = parameters[42]
    kon = parameters[43]
    kp_n = parameters[44]
    nperm = parameters[45]
    perm50 = parameters[46]
    xPsi = parameters[47]
    Trop_conc = parameters[48]
    kxb = parameters[49]
    T_ref = parameters[50]

    # Init return args
    if monitored is None:
        monitored = np.zeros((64,), dtype=np.float64)
    else:
        assert isinstance(monitored, np.ndarray) and monitored.shape == (64,)

    # Expressions for the Sarcomere geometry component
    monitored[50] = len_thick / 2 if len_thick / 2 < SL / 2 else SL / 2
    monitored[51] = (
        len_thin - SL / 2 if len_thin - SL / 2 > len_hbare / 2 else len_hbare / 2
    )
    monitored[52] = -monitored[51] + monitored[50]
    monitored[53] = overlap_func(
        SL
    )  # NB modified here 2*monitored[52]/(len_thick - len_hbare)
    monitored[54] = overlap_func(SL)  # monitored[52]/len_thin

    # Expressions for the Thin filament regulation and crossbridge cycling
    # rates component
    monitored[0] = fapp * xbmodsp * math.pow(Qfapp, -37 / 10 + TmpC / 10)
    monitored[1] = 1 + gslmod * (1 - monitored[53])
    monitored[2] = gapp * xbmodsp * math.pow(Qgapp, -37 / 10 + TmpC / 10) * monitored[1]
    monitored[3] = math.exp(
        -hfmdc * (xXBprer * xXBprer) * math.copysign(1.0, xXBprer) / (x_0 * x_0)
    )
    monitored[4] = math.exp(
        hbmdc
        * ((-x_0 + xXBpostr) * (-x_0 + xXBpostr))
        * math.copysign(1.0, -x_0 + xXBpostr)
        / (x_0 * x_0)
    )
    monitored[5] = hf * xbmodsp * math.pow(Qhf, -37 / 10 + TmpC / 10) * monitored[3]
    monitored[6] = hb * xbmodsp * math.pow(Qhb, -37 / 10 + TmpC / 10) * monitored[4]
    monitored[7] = (
        math.exp(sigmap * ((x_0 - xXBpostr) * (x_0 - xXBpostr)) / (x_0 * x_0))
        if xXBpostr < x_0
        else math.exp(sigman * ((-x_0 + xXBpostr) * (-x_0 + xXBpostr)) / (x_0 * x_0))
    )
    monitored[8] = gxb * xbmodsp * math.pow(Qgxb, -37 / 10 + TmpC / 10) * monitored[7]

    # Expressions for the Normalised active and passive force component
    monitored[9] = (fapp * gxb + fapp * hb) / (
        fapp * gxb + fapp * hb + fapp * hf + gapp * gxb + gapp * hb + gxb * hf
    )
    monitored[10] = (
        fapp
        * hf
        / (fapp * gxb + fapp * hb + fapp * hf + gapp * gxb + gapp * hb + gxb * hf)
    )
    monitored[11] = kxb_normalised * x_0 * monitored[10]
    monitored[12] = (
        kxb_normalised * (XBpostr * xXBpostr + XBprer * xXBprer) * monitored[53]
    )
    monitored[13] = T_ref * monitored[12] / monitored[11]
    monitored[14] = SL / SLset
    PCon_t = Cp
    PExp_t = b_ff
    ppforce_t = (
        PCon_t
        * (-1 + math.exp(PExp_t * math.fabs(SLrest - SL)))
        * math.copysign(1.0, -SLrest + SL)
    )
    monitored[15] = ppforce_t

    """
    monitored[15] = Cp*b_ff*(-0.5 +\
        0.5*(monitored[14]*monitored[14]))*math.exp(b_ff*((-0.5 +\
        0.5*(monitored[14]*monitored[14]))*(-0.5 +\
        0.5*(monitored[14]*monitored[14]))))"""
    monitored[16] = (
        Cp
        * b_ff
        * (-0.5 + 0.5 * (SLset * SLset) / (SLrest * SLrest))
        * math.exp(
            b_ff
            * (
                (-0.5 + 0.5 * (SLset * SLset) / (SLrest * SLrest))
                * (-0.5 + 0.5 * (SLset * SLset) / (SLrest * SLrest))
            )
        )
    )
    monitored[17] = applied_stretch
    monitored[18] = -monitored[16] + monitored[13] + monitored[15]
    monitored[19] = (-monitored[18] + monitored[17]) / visc
    monitored[55] = -monitored[18] + monitored[17]
    monitored[56] = monitored[19]

    # Expressions for the Equation for simulated calcium transient component
    monitored[20] = math.pow(tau1 / tau2, -1 / (-1 + tau1 / tau2)) - math.pow(
        tau1 / tau2, -1 / (1 - tau2 / tau1)
    )
    monitored[21] = (
        Ca_diastolic
        + (Ca_amplitude - Ca_diastolic)
        * (-math.exp((start_time - t) / tau2) + math.exp((start_time - t) / tau1))
        / monitored[20]
        if t > start_time
        else Ca_diastolic
    )

    # Expressions for the Ca binding to troponin to thin filament regulation
    # component
    monitored[22] = kon * math.pow(Qkon, -37 / 10 + TmpC / 10)
    monitored[23] = koffL * koffmod * math.pow(Qkoff, -37 / 10 + TmpC / 10)
    monitored[24] = koffH * koffmod * math.pow(Qkoff, -37 / 10 + TmpC / 10)
    monitored[25] = (
        -TRPNCaL * monitored[23] + (1 - TRPNCaL) * monitored[21] * monitored[22]
    )
    monitored[26] = (
        -TRPNCaH * monitored[24] + (1 - TRPNCaH) * monitored[21] * monitored[22]
    )
    monitored[27] = (1 - monitored[54]) * TRPNCaL + TRPNCaH * monitored[54]
    monitored[28] = perm50 / monitored[27] if monitored[27] > 0.01 else 100 * perm50
    monitored[29] = math.sqrt(math.fabs(1.0 / (1 + math.pow(monitored[28], nperm))))
    monitored[30] = 1.0 / monitored[29] if 1.0 / monitored[29] < 100 else 100
    monitored[57] = monitored[25]
    monitored[58] = monitored[26]
    monitored[31] = kn_p * math.pow(Qkn_p, -37 / 10 + TmpC / 10) * monitored[29]
    monitored[32] = kp_n * math.pow(Qkp_n, -37 / 10 + TmpC / 10) * monitored[30]

    # Expressions for the Regulation and crossbridge cycling state equations
    # component
    monitored[33] = (
        XBprer * monitored[5] - XBpostr * monitored[6] - XBpostr * monitored[8]
    )
    monitored[34] = 1 - N - XBpostr - XBprer
    monitored[59] = monitored[32] * monitored[34] - N * monitored[31]
    monitored[35] = (
        XBpostr * monitored[6]
        + monitored[0] * monitored[34]
        - XBprer * monitored[2]
        - XBprer * monitored[5]
    )
    monitored[60] = monitored[33]
    monitored[61] = monitored[35]

    # Expressions for the Mean strain of strongly bound states component
    monitored[36] = (monitored[0] * monitored[6] + monitored[0] * monitored[8]) / (
        monitored[0] * monitored[5]
        + monitored[0] * monitored[6]
        + monitored[0] * monitored[8]
        + monitored[2] * monitored[6]
        + monitored[2] * monitored[8]
        + monitored[5] * monitored[8]
    )
    monitored[37] = (
        monitored[0]
        * monitored[5]
        / (
            monitored[0] * monitored[5]
            + monitored[0] * monitored[6]
            + monitored[0] * monitored[8]
            + monitored[2] * monitored[6]
            + monitored[2] * monitored[8]
            + monitored[5] * monitored[8]
        )
    )
    monitored[38] = (
        monitored[19] / 2
        + xPsi
        * ((-x_0 - xXBprer + xXBpostr) * monitored[6] - monitored[0] * xXBprer)
        / monitored[36]
    )
    monitored[39] = (
        monitored[19] / 2
        + xPsi * (x_0 - xXBpostr + xXBprer) * monitored[5] / monitored[37]
    )
    monitored[62] = monitored[38]
    monitored[63] = monitored[39]

    # Expressions for the Calculation of micromolar per millisecondes of Ca
    # for apparent Ca binding component
    monitored[40] = (XBpostr + XBprer) / (monitored[10] + monitored[9])
    monitored[41] = (monitored[33] + monitored[35]) / (monitored[10] + monitored[9])
    monitored[42] = -0.5 * monitored[19] if SL < len_thick else 0
    monitored[43] = -0.5 * monitored[19] if -SL + 2 * len_thin > len_hbare else 0
    monitored[44] = -monitored[43] + monitored[42]
    monitored[45] = monitored[44] / len_thin
    monitored[46] = 2 * monitored[44] / (len_thick - len_hbare)
    monitored[47] = Trop_conc * (
        (1 - monitored[54]) * TRPNCaL
        + ((1 - monitored[40]) * TRPNCaL + TRPNCaH * monitored[40]) * monitored[54]
    )
    monitored[48] = Trop_conc * (
        (1 - monitored[54]) * monitored[25]
        + ((1 - monitored[40]) * TRPNCaL + TRPNCaH * monitored[40]) * monitored[45]
        + (
            (1 - monitored[40]) * monitored[25]
            + TRPNCaH * monitored[41]
            + monitored[26] * monitored[40]
            - TRPNCaL * monitored[41]
        )
        * monitored[54]
        - TRPNCaL * monitored[45]
    )
    monitored[49] = (
        kxb * (XBpostr * xXBpostr + XBprer * xXBprer) * monitored[46]
        + kxb
        * (
            XBpostr * monitored[39]
            + XBprer * monitored[38]
            + monitored[33] * xXBpostr
            + monitored[35] * xXBprer
        )
        * monitored[53]
    )

    # Return results
    return monitored
