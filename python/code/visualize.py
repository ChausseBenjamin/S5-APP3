import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Set font to CMU Serif for all plot elements
plt.rcParams["font.family"] = "CMU Serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rcParams["mathtext.fontset"] = "cm"  # Use Computer Modern for math text

# Smart import pattern for dual-purpose module
try:
    # Try relative imports first (when imported as module)
    from .audio import outputs_path
except ImportError:
    # Fall back to absolute imports (when run as script)
    # Add parent directory to path so we can import 'code' package
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from code.audio import outputs_path

plt_settings = {
    "sig": {
        "title": "Signal dans le domaine temporel",
        "x_axis": "Temps (échantillons)",
        "y_axis": "Amplitude",
    },
    "freq": {
        "title": "Amplitude dans le domaine fréquentiel",
        "x_axis": "Fréquence (échantillons)",
        "y_axis": "Amplitude (dB)",
    },
    "phase": {
        "title": "Phase dans le domaine fréquentiel",
        "x_axis": "Fréquence (échantillons)",
        "y_axis": "Phase (rad)",
    },
    "bode": {
        "title": "Lieu de bode du signal",
    },
}


def create_plot(data, subplots, titles=True, stem_freq=False, rate=0, figsize=(10, 3)):
    """
    Create a plot but don't save - returns fig, axs, data_dict for optional customization

    Parameters:
    -----------
    data : array_like
        Input data (time domain or frequency domain)
    subplots : list
        List of subplot types: ["sig", "freq", "phase"]
    titles : bool
        Whether to add titles to subplots
    stem_freq : bool
        Use stem plots instead of line plots for frequency domain plots
    rate : int or float
        Sample rate in Hz. If non-zero, applies fftshift and scales frequency axis to Hz (default 0)
    figsize : tuple
        Figure size as (width, height) in inches. Default (10, 3) gives wide, not-very-tall plots

    Returns:
    --------
    fig : matplotlib.figure.Figure
        Figure object
    axs : list
        List of matplotlib.axes.Axes objects
    data_dict : dict
        Dictionary containing processed data for each subplot
    """
    mag, phase = None, None
    is_fft = np.iscomplexobj(data)

    want_signal = "sig" in subplots
    want_freq = "freq" in subplots
    want_phase = "phase" in subplots

    rows = sum([want_signal, want_freq, want_phase])
    # Only share x-axis between freq and phase plots when they use the same scale
    # Don't share between time domain (samples) and freq domain (Hz) when rate > 0
    share_x = (want_freq and want_phase) and not (want_signal and rate > 0)
    fig, axs = plt.subplots(rows, 1, sharex=share_x, figsize=figsize)
    if rows == 1:
        axs = [axs]

    n = 0
    x = np.arange(len(data))
    x_freq = x  # Initialize x_freq (will be updated if shifted=True for freq plots)

    # Process signal data
    data_time = None
    if want_signal:
        plt_text = plt_settings["sig"]
        ax = axs[n]

        if is_fft:
            data_time = np.fft.ifft(data)
            if np.isrealobj(data_time):
                data_time = data_time.real
        else:
            data_time = data

        # Normalize amplitude to -1 to +1 range (standard for audio)
        data_max = np.max(np.abs(data_time))
        if data_max != 0:  # Avoid division by zero
            data_time = data_time / data_max

        ax.plot(x, data_time)
        if titles:
            ax.set_title(plt_text["title"])
        ax.set_xlabel(plt_text["x_axis"])
        ax.set_ylabel(plt_text["y_axis"])
        n += 1

    # Process frequency domain data
    if want_freq or want_phase:
        if not is_fft:
            fft = np.fft.fft(data)
        else:
            fft = data

        mag = np.abs(fft)
        # Normalize magnitude relative to maximum, then convert to dB
        mag_normalized = mag / np.max(mag)
        mag = 20 * np.log10(mag_normalized + 1e-10)  # Add small value to avoid log(0)
        phase = np.angle(fft)

        # Apply fftshift and frequency scaling if rate is provided
        if rate > 0:
            mag = np.fft.fftshift(mag)
            phase = np.fft.fftshift(phase)
            # Create proper frequency axis in Hz, centered around 0
            N = len(data)
            x_freq = np.linspace(-rate / 2, rate / 2, N, endpoint=False)
        else:
            x_freq = x

    # Plot frequency magnitude
    if want_freq:
        plt_text = plt_settings["freq"]
        ax = axs[n]

        if stem_freq:
            ax.stem(x_freq, mag, basefmt=" ")
        else:
            ax.plot(x_freq, mag)

        # Use symmetric logarithmic x-axis for frequency domain when rate is provided
        if rate > 0:
            ax.set_xscale("symlog", linthresh=rate / 100)

        if titles:
            if want_phase:
                ax.set_title(plt_settings["bode"]["title"])
            else:
                ax.set_title(plt_text["title"])
        # Only set xlabel if this is the last subplot or phase is not following
        if not want_phase:
            xlabel = "Fréquence (Hz)" if rate > 0 else plt_text["x_axis"]
            ax.set_xlabel(xlabel)
        ax.set_ylabel(plt_text["y_axis"])
        n += 1

    # Plot phase
    if want_phase:
        plt_text = plt_settings["phase"]
        ax = axs[n]

        if stem_freq:
            ax.stem(x_freq, phase, basefmt=" ")
        else:
            ax.plot(x_freq, phase)

        # Use symmetric logarithmic x-axis for frequency domain when rate is provided
        if rate > 0:
            ax.set_xscale("symlog", linthresh=rate / 100)

        if titles and not want_freq:
            ax.set_title(plt_text["title"])
        # Always set xlabel for phase subplot (it's either alone or the last one)
        xlabel = "Fréquence (Hz)" if rate > 0 else plt_text["x_axis"]
        ax.set_xlabel(xlabel)
        ax.set_ylabel(plt_text["y_axis"])

    plt.tight_layout()

    # Prepare data dictionary for return
    data_dict = {
        "x": x,
        "x_freq": x_freq if (want_freq or want_phase) else None,
        "signal": data_time if want_signal else None,
        "magnitude": mag if want_freq else None,
        "phase": phase if want_phase else None,
        "is_fft": is_fft,
        "shifted": rate > 0 if (want_freq or want_phase) else False,
        "sample_rate": rate,
    }

    return fig, axs, data_dict


def save_plot(fig, filename):
    plt.savefig(f"{outputs_path}/{filename}")
    plt.close(fig)


def show_plot(fig):
    plt.show()


if __name__ == "__main__":
    h = np.empty(444, dtype=float)

    ## SAWTOOOTH:
    # h = np.linspace(0, 1, 444)

    ## PULSED SAWTOOOTH 1/4
    h = np.zeros(444)
    h[:111] = np.linspace(0, 1, 111)

    ## PULSE 1/4
    # h = np.zeros(444)
    # h[:111] = np.ones(111)

    ## TRIANGLE
    # h[:222] = np.linspace(0, 1, 222)
    # h[222:] = np.linspace(1, 0, 222)

    fig1, axs, data_dict = create_plot(
        h,
        ["freq", "phase", "sig"],
        titles=False,
        figsize=(6, 5),
        rate=1000,  # comment if need be
    )
    save_plot(fig1, "sawtooth_test.pdf")
