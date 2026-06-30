import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from typing import Union


class BaseOverlap(ABC):
    """
    Abstract base class for filament overlap models.
    Ensures all overlap classes implement the __call__ method with the correct signature.
    """

    @abstractmethod
    def __call__(self, SL: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Calculate the filament overlap factor given the sarcomere length (SL).
        
        Args:
            SL: Sarcomere length(s) as a float or numpy array.
            
        Returns:
            Filament overlap factor (0.0 to 1.0 scale) as a float or numpy array.
        """
        pass


class OverlapDummy(BaseOverlap):
    """
    Dummy overlap function that always returns 1.0 (full overlap).
    """
    
    def __call__(self, SL: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        if isinstance(SL, np.ndarray):
            return np.ones_like(SL, dtype=float)
        return 1.0


class OverlapRice(BaseOverlap):
    """
    Filament overlap function using default parameters from Rice et al. (2008).
    Includes modifications to allow force to drop at higher sarcomere lengths.
    """

    def __init__(
        self, 
        len_hbare: float = 0.1, 
        len_thick: float = 1.65, 
        len_thin: float = 1.2
    ) -> None:
        self.len_hbare: float = len_hbare
        self.len_thick: float = len_thick
        self.len_thin: float = len_thin

    def __call__(self, SL: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        len_hbare = self.len_hbare
        len_thick = self.len_thick
        len_thin = self.len_thin
        
        sovr_ze = np.minimum(len_thick / 2, SL / 2)

        # Original formulation, valid for SL_max <= 2*len_thin
        sovr_cle = np.maximum(len_thin - SL / 2, len_hbare / 2)
        
        # Modification to allow force to drop at higher SL:
        sovr_cle = np.maximum(sovr_cle, SL / 2 - len_thin)

        len_sovr = sovr_ze - sovr_cle
        SOVFThick = 2 * len_sovr / (len_thick - len_hbare)
        
        return SOVFThick


class Overlap(BaseOverlap):
    """
    Class for holding a parameterized version of the overlap function 
    from Rice et al. (2008). Default values reproduce the original paper.
    """

    def __init__(
        self,
        SL_zero: float = 1.2,
        SL_low: float = 1.65,
        SL_plat: float = 2.3,
        SL_high: float = 2.6,
        f_low: float = 0.6,
        slope_high: float = 1.0,
        scale: float = 1.0,
    ) -> None:
        self.SL_zero: float = SL_zero
        self.SL_low: float = SL_low
        self.SL_plat: float = SL_plat
        self.SL_high: float = SL_high
        self.f_low: float = f_low
        self.slope_high: float = slope_high
        self.scale: float = scale

    def __call__(self, SL: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        SL_zero = self.SL_zero
        SL_low = self.SL_low
        SL_plat = self.SL_plat
        SL_high = self.SL_high
        f_low = self.f_low
        slope_high = self.slope_high
        scale = self.scale
        
        f1 = f_low * (SL - SL_zero) / (SL_low - SL_zero)
        f2 = scale * (f_low + ((SL - SL_low) * (1.0 - f_low) / (SL_plat - SL_low)))
        
        f = np.minimum(f1, f2)
        f = np.minimum(f, 1.0 * scale)
        f = np.minimum((SL_high - slope_high * (SL - SL_high)) / SL_high, f)
        
        return f


class Overlap2(BaseOverlap):
    """
    Alternative overlap function, similar to Campbell (2011).
    Piecewise linear, hat-shaped function taking on values between 0.0 and 1.0.
    """

    def __init__(
        self, 
        SL0: float = 1.2, 
        SL1: float = 2.2, 
        SL2: float = 2.4, 
        SL3: float = 6.0
    ) -> None:
        self.SL0: float = SL0
        self.SL1: float = SL1
        self.SL2: float = SL2
        self.SL3: float = SL3

    def __call__(self, SL: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        SL0 = self.SL0
        SL1 = self.SL1
        SL2 = self.SL2
        SL3 = self.SL3
        
        f1 = 1.0 * (SL - SL0) / (SL1 - SL0)
        f2 = 1.0 * (SL - SL3) / (SL2 - SL3)

        f = np.minimum(f1, f2)
        f = np.minimum(f, 1.0)
        f = np.maximum(f, 0.0)

        return f


if __name__ == "__main__":
    # Test instantiations and print ratios
    overlap_func = Overlap(SL_zero=1.6, SL_low=1.7)
    
    print(f'Stretched 0% (SL = 1.67): {overlap_func(1.67):.4f}')
    print(f'Contracting 0% (SL = 1.78): {overlap_func(1.78):.4f}')
    print(f'Stretched 20% (SL = 1.82): {overlap_func(1.82):.4f}')
    print(f'Contracting 20% (SL = 2.014): {overlap_func(2.014):.4f}')
    print(f'Ratio 0% stretch: {overlap_func(1.78)/overlap_func(1.67):.4f}')
    print(f'Ratio 20% stretch: {overlap_func(2.04)/overlap_func(1.82):.4f}')

    # Visualizing different overlap models
    overlap1 = OverlapRice()
    overlap2 = OverlapRice(len_thin=1.4, len_thick=1.65)
    overlap3 = OverlapRice(len_thin=1.4, len_thick=1.45)

    overlap_iso = Overlap(SL_zero=1.5, SL_low=1.7, f_low=0.8)
    overlap_ctr = Overlap(SL_zero=1.6, SL_low=1.7)

    SL_array = np.linspace(1.4, 2.6, 100)
    
    plt.plot(SL_array, overlap_ctr(SL_array), label='Ctr')
    plt.plot(SL_array, overlap_iso(SL_array), label='ISO')
    plt.xlabel('Sarcomere Length (μm)')
    plt.ylabel('Overlap Factor')
    plt.legend()
    plt.savefig('overlap_iso_ctr.pdf')
    plt.show()