from code.saveFigure import save_plot
from code.signalFFT import SignalFFT
from code.wavSignal import WavSignal

import matplotlib.pyplot as plt
import numpy
import scipy.signal as sp


def get_harmonics(
    signal: WavSignal,
    amount_to_get: int = 32,
    sample_distance_between_peaks: int = 1285,
):
    start = 1
    end = amount_to_get + 1

    # Obtaining the amplitudes of each frequencies of the signal.
    fft = SignalFFT(signal)
    amplitudes = fft.get_amplitudes()

    local_peaks, _ = sp.find_peaks(amplitudes, distance=sample_distance_between_peaks)

    peaks_indexes = local_peaks[start:end]
    peaks = amplitudes[peaks_indexes]

    plt.figure()
    plt.title("Harmonics identification")
    plt.xlabel("index de fréquence (m)")
    plt.ylabel("Amplitude (dB)")
    plt.xlim(0, 70000)
    plt.plot(20 * numpy.log10(amplitudes))
    plt.plot(
        peaks_indexes,
        20 * numpy.log10(peaks),
        "xr",
    )
    save_plot(f"{amount_to_get} harmonics of {signal.get_name()}")
    plt.close()

    print(f"{amount_to_get} harmonics analysis of {signal.get_name()}")
    print(f"\t- Frequency indexes:   {peaks_indexes}")
    print(f"\t- Harmonic amplitudes: {peaks}")

    return peaks_indexes, peaks


def print_harmonics(original_signal: WavSignal, peaks_indexes, peaks):
    """
    Generates the table required for the rapport, for all the harmonics
    we chose to have.
    """
    print(
        f"Data table of {len(peaks_indexes)} harmonics of {original_signal.get_name()}"
    )
    fft = SignalFFT(original_signal)

    current_harmonic = 0
    for index in peaks_indexes:
        amplitude = peaks[current_harmonic]
        amplitude = 20 * numpy.log10(amplitude)
        frequency = fft.get_frequencies_axis()[index]
        phase = fft.get_phases()[index]

        current_harmonic += 1
        print(
            f"- {current_harmonic:<3} | "
            f"Amplitude: {amplitude:>8.2f} | "
            f"Frequency: {frequency:>8.2f} Hz | "
            f"Phase: {phase:>9.4f} rads"
        )
