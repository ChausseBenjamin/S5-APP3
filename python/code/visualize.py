import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

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
        "y_axis": "Amplitude",
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


def create_plot(data, subplots, titles=True, stem_freq=False):
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
    fig, axs = plt.subplots(rows, 1, sharex=(want_freq and want_phase))
    if rows == 1:
        axs = [axs]

    n = 0
    x = np.arange(len(data))

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
        phase = np.angle(fft)

    # Plot frequency magnitude
    if want_freq:
        plt_text = plt_settings["freq"]
        ax = axs[n]

        if stem_freq:
            ax.stem(x, mag, basefmt=" ")
        else:
            ax.plot(x, mag)

        if titles:
            if want_phase:
                ax.set_title(plt_settings["bode"]["title"])
            else:
                ax.set_title(plt_text["title"])
        # Only set xlabel if this is the last subplot or phase is not following
        if not want_phase:
            ax.set_xlabel(plt_text["x_axis"])
        ax.set_ylabel(plt_text["y_axis"])
        n += 1

    # Plot phase
    if want_phase:
        plt_text = plt_settings["phase"]
        ax = axs[n]

        if stem_freq:
            ax.stem(x, phase, basefmt=" ")
        else:
            ax.plot(x, phase)

        if titles and not want_freq:
            ax.set_title(plt_text["title"])
        # Always set xlabel for phase subplot (it's either alone or the last one)
        ax.set_xlabel(plt_text["x_axis"])
        ax.set_ylabel(plt_text["y_axis"])

    plt.tight_layout()

    # Prepare data dictionary for return
    data_dict = {
        "x": x,
        "signal": data_time if want_signal else None,
        "magnitude": mag if want_freq else None,
        "phase": phase if want_phase else None,
        "is_fft": is_fft,
    }

    return fig, axs, data_dict


def save_plot(fig, filename):
    plt.savefig(f"{outputs_path}/{filename}")
    plt.close(fig)


def show_plot(fig):
    plt.show()


if __name__ == "__main__":
    # Sawtooth for the first quarter, then nothing
    h = np.zeros(444)
    h[:111] = np.linspace(0, 1, 111)
    fig1, axs, data_dict = create_plot(h, ["freq", "phase", "sig"])
    save_plot(fig1, "sawtooth_test.pdf")
