import numpy as np
from numpy import pi
import sys
import matplotlib.pyplot as plt
from pathlib import Path


try:
    # Try relative imports first (when imported as module)
    from . import visualize as vis
except ImportError:
    # Fall back to absolute imports (when run as script)
    # Add parent directory to path so we can import 'code' package
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from code import visualize as vis


def lpf(cutoff, N, rate):
    """
    Generate a low-pass filter with a given
    cutoff frequency
    """
    # Create symmetric index array centered around 0
    n = np.arange(N) - (N - 1) / 2
    h = np.empty(N, dtype=float)
    # Isolating k in cutoff = (k-1)/2 * (rate/N)
    # from the windowed LPF filter equation
    k = (2 * cutoff * N) / rate + 1

    # Find the center index (where n=0)
    center_idx = (N - 1) // 2

    # Handle n=0 case separately to avoid division by zero
    h[center_idx] = k / N

    # Calculate for all other indices
    for i in range(N):
        if i != center_idx:
            h[i] = (1 / N) * (np.sin(pi * n[i] * k / N) / np.sin(pi * n[i] / N))

    return h


def notch(N, cutoff, freq, rate):
    """
    freq:   frequency to cut out (Hz)
    cutoff: frequency range of the filter (Hz, +-) to reach -3dB
    rate:   sample rate of the filter (Hz)
    N:      number of samples for the filter
    """
    omega_0 = 2 * pi * (freq / rate)

    # Use same indexing scheme as LPF function
    n = np.arange(N) - (N - 1) / 2
    d = np.zeros(N, dtype=float)  # Initialize with zeros
    center_idx = (N - 1) // 2
    d[center_idx] = 1  # Delta function at n=0 (center)

    lowpass = lpf(cutoff, N, rate)
    h = d - 2 * lowpass * np.cos(omega_0 * n)

    return h


if __name__ == "__main__":
    # Test LPF function is actually an LPF
    N = 6000
    cutoff = 40
    rate = 44100

    h = lpf(cutoff, N, rate)
    fig, axs, data_dict = vis.create_plot(h, subplots=["freq", "phase"], rate=44100)
    vis.save_plot(fig, "lpf_test.pdf")

    # Test that the conversion to a notch works
    h = notch(N, cutoff, 1000, rate)
    fig, axs, data_dict = vis.create_plot(h, subplots=["freq", "phase"], rate=44100)
    plt.show()
    vis.save_plot(fig, "notch_test.pdf")
