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


def gen_filter(rate, N=6000, cutoff=40, target=1000):
    return filtering.notch(N, cutoff, target, rate)


def de_noised():
    """Remove 1kHz noise from bassoon audio using notch filter"""
    rate, samples = audio.load("bassoon")
    cleaned = samples
    h = gen_filter(rate, cutoff=40)
    for _ in range(1):
        # Use 'same' mode to keep output same size as input
        cleaned = convolve(cleaned, h, mode="same")
    return cleaned


if __name__ == "__main__":
    rate, samples = audio.load("bassoon")
    cleaned = de_noised()
    audio.save(rate, cleaned, "bassoon-cleaned-thin.wav")

    h = gen_filter(rate)
    for typ in ["freq", "sig", "phase"]:
        fig, axs, data_dict = vis.create_plot(
            h,
            [typ],
            rate=rate,
            titles=False,
        )
        vis.save_plot(fig, f"bassoon-notch-{typ}.pdf")

    # save separate plots for each
    for key, data in {"raw": samples, "cleaned": cleaned}.items():
        fig, axs, data_dict = vis.create_plot(
            data, ["freq", "sig", "phase"], rate=rate, titles=False, figsize=(6, 5)
        )
        vis.save_plot(fig, f"bassoon-{key}-combined.pdf")

        for typ in ["sig", "freq", "phase"]:
            fig, axs, data_dict = vis.create_plot(data, [typ], rate=rate, titles=False)
            vis.save_plot(fig, f"bassoon-{key}-{typ}.pdf")
