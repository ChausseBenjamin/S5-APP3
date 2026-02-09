import numpy as np
from numpy import convolve
import sys
from pathlib import Path

# Smart import pattern for dual-purpose module
try:
    # Try relative imports first (when imported as module)
    from . import filtering
    from . import audio
    from . import visualize as vis
except ImportError:
    # Fall back to absolute imports (when run as script)
    # Add parent directory to path so we can import 'code' package
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from code import filtering
    from code import audio
    from code import visualize as vis


def raw_plot():
    """Load and plot raw bassoon audio - used by main.py"""
    rate, samples = audio.load("bassoon")
    fig, axs, data_dict = vis.create_plot(samples, ["sig", "freq"])
    vis.show_plot(fig)
    return fig


def de_noised():
    """Remove 1kHz noise from bassoon audio using notch filter"""
    rate, samples = audio.load("bassoon")
    N = 6000
    cutoff = 40
    target = 1000
    h = filtering.notch(N, cutoff, target, rate)
    # Use 'same' mode to keep output same size as input
    for _ in range(2):
        samples = convolve(samples, h, mode="same")
    return samples


if __name__ == "__main__":
    rate, samples = audio.load("bassoon")
    cleaned = de_noised()

    audio.save(rate, cleaned, "02-filtered_multi_bassoon.wav")

    fig, axs, data_dict = vis.create_plot(cleaned, ["sig", "freq"])
    vis.save_plot(fig, "02-filtered_multi_bassoon.pdf")
