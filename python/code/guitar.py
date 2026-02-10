from code.filters import best_sliding_average_low_pass_coefficient
from code.music import AMONG_US, BETHOVEN, get_music, optimized_build_synthesized_note
from code.rawSignals import get_guitar
from code.saveFigure import save_plot

# from code.sandbox import sandbox
from code.signalAnalysis import get_harmonics
from code.signalFFT import SignalFFT
from code.signalModifications import (
    apply_absolute,
    apply_gain,
    apply_sliding_average_low_pass_filter,
)
from code.wavSignal import WavSignal

import matplotlib.pyplot as plt


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
    return get_harmonics(guitar)


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

    print("saving synthesized signal audio")
    synthesized.save()
    return synthesized


def generate_guitar_music(
    synthesized,
    harmonics_index,
    harmonics_peaks,
    enveloppe,
):
    print("Generating Among_us.wav")
    music = get_music(
        synthesized,
        466.2,
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
        466.2,
        harmonics_index,
        harmonics_peaks,
        enveloppe,
        get_guitar(),
        BETHOVEN,
    )
    bethoven.set_name("bethoven")
    bethoven.save()


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
