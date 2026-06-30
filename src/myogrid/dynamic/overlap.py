import numpy as np
import matplotlib.pyplot as plt


class Overlap():
    """Class for holding a parameterized version of the
    overlap function from Rice et al 2008"""

    def __init__(self,SL_zero = 1.2, SL_low = 1.7, SL_high = 2.3, f_low = 0.6):
        """Default values reproduce Rice et al (2008)"""
        self.SL_zero = SL_zero
        self.SL_low = SL_low
        self.SL_high = SL_high
        self.f_low = f_low

    def __call__(self,SL):
        SL_zero = self.SL_zero
        SL_low = self.SL_low
        SL_high = self.SL_high
        f_low = self.f_low
        f1 = f_low*(SL-SL_zero)/(SL_low-SL_zero)
        f2 = f_low + (SL-SL_low)*(1.0-f_low)/(SL_high-SL_low)
        f = np.minimum(f1,f2)
        return np.minimum(f,1.0)



class OverlapDummy():
    def __call__(self,SL):
        return 1.0


class OverlapRice():

    def __init__(self,len_hbare=0.1,len_thick=1.65,len_thin=1.2):
        "default parameters from Rice et al (2008)"

        self.len_hbare = len_hbare
        self.len_thick = len_thick
        self.len_thin = len_thin

    def __call__(self,SL):
        len_hbare = self.len_hbare
        len_thick = self.len_thick
        len_thin = self.len_thin
        sovr_ze = np.minimum(len_thick/2,SL/2)# if len_thick/2 < SL/2 else SL/2)

        #original formulation, only valid for SL_max <= 2*len_thin:
        sovr_cle = np.maximum(len_thin - SL/2,len_hbare/2)
        #modification to allow force to drop at higher SL:
        sovr_cle = np.maximum(sovr_cle,SL/2-len_thin)

        len_sovr = -sovr_cle + sovr_ze
        SOVFThick = 2*len_sovr/(len_thick- len_hbare)
        #SOVFThin = len_sovr/len_thin
        overlap = SOVFThick

        return overlap



if __name__ == "__main__":
    overlap_func = Overlap(SL_zero=1.6,SL_low=1.7)
    print(f'Stretched 0% (SL = 1.67): {overlap_func(1.67)}')
    print(f'Contracting 0% (SL = 1.78): {overlap_func(1.78)}')
    print(f'Stretched 20% (SL = 1.82): {overlap_func(1.82)}')
    print(f'Contracting 20% (SL = 2.014): {overlap_func(2.014)}')
    print(f'Ratio 0% stretch: {overlap_func(1.78)/overlap_func(1.67)}')
    print(f'Ratio 20% stretch: {overlap_func(2.04)/overlap_func(1.82)}')



    #SL = np.linspace(1.4,2.6,100)
    #plt.plot(SL,overlap_func(SL),label='orig')
    #plt.show()
    #exit()

    overlap1 = OverlapRice()
    overlap2 = OverlapRice(len_thin=1.4, len_thick=1.65)
    overlap3 = OverlapRice(len_thin=1.4, len_thick=1.45)


    overlap_iso = Overlap(SL_zero=1.5, SL_low=1.7, f_low = 0.8)
    overlap_ctr = Overlap(SL_zero=1.6, SL_low=1.7)

    SL = np.linspace(1.4,2.6,100)
    #plt.plot(SL,overlap1(SL),label='orig')
    #plt.plot(SL,overlap2(SL),label='mod')
    #plt.plot(SL,overlap3(SL),label='mod2')
    
    plt.plot(SL, overlap_ctr(SL), label='Ctr')
    plt.plot(SL, overlap_iso(SL), label='ISO')
    plt.legend()
    plt.savefig('overlap_iso_ctr.pdf')
    plt.show()
