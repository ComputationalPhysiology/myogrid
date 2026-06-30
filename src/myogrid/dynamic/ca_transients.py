from typing import Protocol, Union
from scipy.interpolate import interp1d
import numpy as np
import math
import numpy.typing as npt

FloatOrArray = Union[float, npt.NDArray[np.float64]]


class CaTransient(Protocol):
    """
    Protocol defining the callable interface for calcium transients.
    """

    def __call__(self, t: FloatOrArray) -> FloatOrArray:
        """Evaluates the calcium concentration at the given time.

        Args:
            t (FloatOrArray): The time in milliseconds.

        Returns:
            FloatOrArray: The calcium concentration in uM.
        """
        ...


class CaTransientFromFile:
    """
    Class for creating a callable Ca transient from file
    """

    def __init__(self, filepath: str, scale: float = 1.0):
        data = np.loadtxt(filepath)
        self.interpolator = interp1d(
            data[:, 0] * 1e3, data[:, 1] * 1e-3 * scale, fill_value="extrapolate"
        )

    def __call__(self, t: FloatOrArray) -> FloatOrArray:
        """Evaluate the interpolator for the data"""
        return self.interpolator(t)


class ParameterizedCaTransient:
    """
    Parameterized Ca transient from the model by Rice et al (2008)
    """

    def __init__(
        self,
        ca_amp: float = 1.45,
        ca_diastolic: float = 0.09,
        start_time: float = 5,
        tau1: float = 20,
        tau2: float = 110,
    ):
        self.ca_amp = ca_amp
        self.ca_diastolic = ca_diastolic
        self.start_time = start_time
        self.tau1 = tau1
        self.tau2 = tau2

    def __call__(self, t: float):
        """Evaluates the parameterized ca function"""
        ca_amp, ca_diastolic = self.ca_amp, self.ca_diastolic
        start_time = self.start_time
        tau1, tau2 = self.tau1, self.tau2
        beta = -math.pow(tau1 / tau2, -1 / (1 - tau2 / tau1)) + math.pow(
            tau1 / tau2, -1 / (-1 + tau1 / tau2)
        )

        ca = np.where(
            t > start_time,
            (-ca_diastolic + ca_amp)
            * (np.exp((start_time - t) / tau1) - np.exp((start_time - t) / tau2))
            / beta
            + ca_diastolic,
            ca_diastolic,
        )

        return ca


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    """Plot two ca transients from file and two 
    parameterized versions fit to the file data."""

    ca1 = CaTransientFromFile("../../ca_data/hf_shortening.dat")
    ca2 = CaTransientFromFile("../../ca_data/hf_tow.dat")
    # parameters fit to the hf_shortening and hf_tow data, respectively:
    ca3 = ParameterizedCaTransient(
        1.02334224e00, 1.08565781e-01, 1.69131142e02, 8.68081716e00, 1.70174213e02
    )
    ca4 = ParameterizedCaTransient(
        1.02312953e00, 1.10749672e-01, 1.75731403e02, 1.29928119e01, 2.54589242e02
    )

    time = np.linspace(0, 1000, 1001)

    plt.plot(time, ca1(time), label="Ctr from file")
    plt.plot(time, ca2(time), label="TOW from file")
    plt.plot(time, ca3(time), label="Ctr fitted")
    plt.plot(time, ca4(time), label="TOW fitted")

    plt.legend()
    plt.savefig("fitted_ca_transients.pdf")

    plt.show()
