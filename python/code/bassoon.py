import numpy as np
from numpy import convolve, fft
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


def gen_filter2(rate, N=6000, cutoff=40, target=1000):
    H = np.ones(N)

    k1 = int(round((target - cutoff) * N / rate))
    k2 = int(round((target + cutoff) * N / rate))

    H[k1:k2] = 0.0
    H[N - k2 : N - k1] = 0.0

    h = np.fft.ifft(H).real
    h = np.roll(h, N // 2)

    return h


def de_noised(method=gen_filter):
    """Remove 1kHz noise from bassoon audio using notch filter"""
    rate, samples = audio.load("bassoon")
    # Class requirements: cutoff=40Hz, target=1000Hz, single pass
    h = method(rate, cutoff=40, target=1000)
    # Single pass of the notch filter
    cleaned = convolve(samples, h, mode="same")
    return cleaned


def envelope(cutoff=40, N=6000):
    rate, samples = audio.load("bassoon")
    lpf = filtering.lpf(cutoff, N, rate)
    return np.convolve(np.abs(samples), lpf)


if __name__ == "__main__":
    rate, samples = audio.load("bassoon")
    cleaned = de_noised()
    audio.save(rate, cleaned, "bassoon-cleaned-basic.wav")
    cleaned = de_noised(method=gen_filter2)
    audio.save(rate, cleaned, "bassoon-cleaned-custom.wav")

    # Calculate envelopes for both original and cleaned signals
    env_original = envelope()
    # Calculate envelope for cleaned signal
    lpf = filtering.lpf(40, 6000, rate)
    env_cleaned = np.convolve(np.abs(cleaned), lpf)

    # Normalize both envelopes to 0-1 range
    env_original = env_original / np.max(env_original)
    env_cleaned = env_cleaned / np.max(env_cleaned)

    # Create overlay plot with both envelopes
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 4))

    # Time axis for plotting
    time_orig = np.arange(len(env_original)) / rate
    time_cleaned = np.arange(len(env_cleaned)) / rate

    # Plot both envelopes with different colors
    ax.plot(
        time_orig, env_original, color="#2E86C1", label="Signal original", linewidth=1.5
    )
    ax.plot(
        time_cleaned,
        env_cleaned,
        color="#E74C3C",
        label="Signal traité (1kHz filtrée)",
        linewidth=1.5,
    )

    # Add cute legend and labels
    ax.legend(loc="upper right", frameon=True, fancybox=True, shadow=True)
    ax.set_xlabel("Temps (s)")
    ax.set_ylabel("Amplitude normalisée")
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)

    # Apply tight layout
    plt.tight_layout()

    vis.save_plot(fig, "bassoon-envelope.pdf")

    h = gen_filter(rate)
    for typ in ["freq", "sig", "phase"]:
        fig, axs, data_dict = vis.create_plot(
            h,
            [typ],
            rate=rate,
            titles=False,
        )
        vis.save_plot(fig, f"bassoon-notch-{typ}.pdf")

    # Test passing a 1kHz sine through the notch filter
    n = np.arange(12_000) / rate
    sin1k = np.sin(2 * np.pi * 1000 * n)
    sin1k = np.convolve(sin1k, h, mode="same")
    fig, axs, data_dict = vis.create_plot(
        sin1k,
        ["sig"],
        rate=rate,
        titles=False,
    )
    vis.save_plot(fig, "bassoon-test-with-1k.pdf")

    # save separate plots for each
    for key, data in {"raw": samples, "cleaned": cleaned}.items():
        fig, axs, data_dict = vis.create_plot(
            data, ["freq", "sig", "phase"], rate=rate, titles=False, figsize=(6, 5)
        )
        vis.save_plot(fig, f"bassoon-{key}-combined.pdf")

        for typ in ["sig", "freq", "phase"]:
            fig, axs, data_dict = vis.create_plot(data, [typ], rate=rate, titles=False)
            vis.save_plot(fig, f"bassoon-{key}-{typ}.pdf")
