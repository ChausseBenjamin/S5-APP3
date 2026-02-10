from code.filters import best_sliding_average_low_pass_coefficient
from code.music import (
    AMONG_US,
    BETHOVEN,
    TRICKY,
    get_music,
    optimized_build_synthesized_note,
)
from code.rawSignals import get_guitar
from code.saveFigure import save_plot

# from code.sandbox import sandbox
from code.signalAnalysis import (
    get_fondamental_harmonic_frequency,
    get_harmonics,
    print_harmonics,
)
from code.signalFFT import SignalFFT
from code.signalModifications import (
    apply_absolute,
    apply_gain,
    apply_sliding_average_low_pass_filter,
)
from code.wavSignal import WavSignal

import matplotlib.pyplot as plt
import numpy


def execute_guitar():
    print("Executing code for guitar")
    harmonics_index, harmonics_peaks = get_guitar_harmonics()
    enveloppe = get_guitar_enveloppe()
    plot_enveloppe(enveloppe)

    synthesized = get_synthesized_guitar(harmonics_index, harmonics_peaks, enveloppe)
    generate_guitar_music(synthesized, harmonics_index, harmonics_peaks, enveloppe)


def get_guitar_harmonics():
    print("Harmonic analysis of Guitar")
    guitar = get_guitar()
    apply_absolute(guitar)
    harmonics_index, harmonics_peaks = get_harmonics(guitar, amount_to_get=31)
    print_harmonics(guitar, harmonics_index, harmonics_peaks)
    return harmonics_index, harmonics_peaks


def get_guitar_enveloppe():
    print("Getting enveloppe of Guitar")
    guitar = get_guitar()
    apply_absolute(guitar)

    best_N = best_sliding_average_low_pass_coefficient(-3, 10, 1, 1000)
    apply_sliding_average_low_pass_filter(guitar, best_N, "guitar_enveloppe")
    return guitar


def get_guitar_fft():
    guitar = get_guitar()
    fft = SignalFFT(guitar)
    return fft


def get_synthesized_guitar(harmonics_index, harmonics_peaks, enveloppe):
    print("Synthetizing guitar...")
    synthesized = optimized_build_synthesized_note(
        harmonics_index, harmonics_peaks, enveloppe, get_guitar()
    )
    plot_synthesized_versus_original(synthesized, enveloppe)
    plot_fft_synthesized_versus_original(synthesized)
    print("saving synthesized signal audio")
    synthesized.save()
    return synthesized


def generate_guitar_music(
    synthesized,
    harmonics_index,
    harmonics_peaks,
    enveloppe,
):
    guitar = get_guitar()
    fundamental = get_fondamental_harmonic_frequency(guitar, harmonics_index)

    print("Generating Among_us.wav")
    music = get_music(
        synthesized,
        fundamental,
        harmonics_index,
        harmonics_peaks,
        enveloppe,
        get_guitar(),
        AMONG_US,
    )
    music.set_name("among_us")
    music.save()

    print("Generating bethoven.wav")
    bethoven = get_music(
        synthesized,
        fundamental,
        harmonics_index,
        harmonics_peaks,
        enveloppe,
        get_guitar(),
        BETHOVEN,
    )
    bethoven.set_name("bethoven")
    bethoven.save()

    print("Generating tricky.wav")
    tricky = get_music(
        synthesized,
        fundamental,
        harmonics_index,
        harmonics_peaks,
        enveloppe,
        get_guitar(),
        TRICKY,
    )
    tricky.set_name("bethoven_trust")
    tricky.save()


def plot_enveloppe(enveloppe: WavSignal):
    print("Plotting guitar's enveloppe")
    guitar = get_guitar()
    apply_absolute(guitar)

    plt.figure()
    guitar.partial_plot()
    enveloppe.partial_plot()
    apply_gain(enveloppe, 2)
    save_plot("guitar_enveloppe")
    plt.close()


def plot_synthesized_versus_original(synthesized: WavSignal, enveloppe: WavSignal):
    print("Plotting difference between synthesized signal and original signal")
    original = get_guitar()

    plt.figure()
    original.partial_plot()
    synthesized.partial_plot()
    enveloppe.partial_plot()
    save_plot("original guitar versus synthesized")
    plt.close()


def plot_fft_synthesized_versus_original(synthesized: WavSignal):
    print("Fourier analysis of synthesized signal versus real one")
    guitar = get_guitar()

    fft_guitar = SignalFFT(guitar)
    fft_synthesized = SignalFFT(synthesized)

    plt.figure()
    plt.title("FFT amplitude original versus synthesized")
    plt.xlabel("index de fréquence (m)")
    plt.ylabel("Amplitude (dB)")
    plt.xlim(0, 70000)
    plt.plot(20 * numpy.log10(fft_guitar.get_amplitudes()), label=guitar.get_name())
    plt.plot(
        20 * numpy.log10(fft_synthesized.get_amplitudes()), label=synthesized.get_name()
    )
    plt.grid(True)
    plt.legend()
    save_plot("ampltitude guitar fourier versus synthesized fourier")
    plt.close()

    plt.figure()
    plt.subplot(2, 1, 1)
    plt.xlim(0, 20000)
    fft_guitar.partial_phase_plot()
    plt.subplot(2, 1, 2)
    plt.xlim(0, 20000)
    fft_synthesized.partial_phase_plot()
    plt.grid(True)
    save_plot("phase guitar fourier versus synthesized fourier")
    plt.close()
