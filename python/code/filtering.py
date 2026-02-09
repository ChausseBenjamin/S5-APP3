import numpy as np
from numpy import pi
import sys
from pathlib import Path

try:
    # Try relative imports first (when imported as module)
    from . import visualize as vis
except ImportError:
    # Fall back to absolute imports (when run as script)
    # Add parent directory to path so we can import 'code' package
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from code import visualize as vis


def lpf(cutoff, N):
    """
    Generate a low-pass filter with a given
    cutoff frequency
    """
    n = np.arange(N)
    h = np.empty(N, dtype=float)
    # Isolating k in f_c = (K-1)/2
    # from the windowed LPF filter equation
    k = (2 * cutoff) + 1

    # Handle n=0 case separately to avoid division by zero
    h[0] = k / N

    # Calculate for n > 0
    if N > 1:
        n_nonzero = n[1:]
        h[1:] = (1 / N) * (np.sin(pi * n_nonzero * k / N) / np.sin(pi * n_nonzero / N))

    return h


def notch(N, cutoff, freq, rate):
    """
    freq:   frequency to cut out (Hz)
    cutoff: frequency range of the filter (Hz, +-) to reach -3dB
    rate:   sample rate of the filter (Hz)
    N:      number of samples for the filter
    """
    omega_0 = 2 * pi * (freq / rate)

    n = np.arange(N)
    d = np.zeros(N, dtype=float)  # Initialize with zeros
    d[0] = 1  # Delta function at n=0

    lowpass = lpf(cutoff, N)
    h = d - 2 * lowpass * np.cos(omega_0 * n)

    return h


if __name__ == "__main__":
    # Test LPF function is actually an LPF
    N = 6000
    cutoff = 40
    rate = 44100

    h = lpf(cutoff, N)
    fig, axs, data_dict = vis.create_plot(h, subplots=["freq", "phase"])
    vis.save_plot(fig, "lpf_test.pdf")

    # Test that the conversion to a notch works
    h = notch(N, cutoff, 1000, rate)
    fig, axs, data_dict = vis.create_plot(h, subplots=["freq", "phase"])
    vis.save_plot(fig, "notch_test.pdf")
