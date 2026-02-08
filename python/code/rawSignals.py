from code.saveFigure import save_plot
from code.wavSignal import WavSignal

import matplotlib.pyplot as plt


def get_guitar():
    return WavSignal("audio/note_guitare_lad.wav")


def get_bason():
    return WavSignal("audio/note_basson_plus_sinus_1000_hz.wav")


def plot_raw_signals():
    """
    Saves a plot of both raw signals together.
    So you don't have to pollute main.py
    """
    guitar = get_guitar()
    bason = get_bason()
    plt.figure()
    plt.subplot(2, 1, 1)
    guitar.partial_plot()
    plt.subplot(2, 1, 2)
    bason.partial_plot()
    save_plot("raw_signals")
    plt.close()
