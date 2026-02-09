from code.rawSignals import get_guitar, plot_raw_signals
from code.signalFFT import SignalFFT
from code.signalModifications import apply_absolute

import numpy


def main():
    plot_raw_signals()

    guitar = get_guitar()
    print("-------------- Guitar before absolute")
    guitar.print_info()

    print("-------------- Guitar after absolute")
    apply_absolute(guitar)
    guitar.print_info()

    guitar_fft = SignalFFT(guitar, amountOfSin=32)
    guitar_fft.full_plot(show=False, save=True)

    # Applying an Hanning window
    windowedGuitar = (
        guitar.get_signal()
        * numpy.hanning(len(guitar.get_signal()))
        / guitar.get_sample_count()
    )

    # Idk fam, this whole shit seems completely hella wrong as fuck.
    guitar.set_signal(windowedGuitar)
    guitar.set_name("windowed_guitar")
    guitar.full_plot(show=False, save=True)
    windowed_guitar_fft = SignalFFT(guitar)
    windowed_guitar_fft.full_plot(show=False, save=True)


if __name__ == "__main__":
    main()


# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.io import wavfile

# fs_guitar, signal_guitar = wavfile.read("note_guitare_lad.wav")  # fs_guitar = fréquence d'échantillonnage

# t_guitar = np.arange(len(signal_guitar)) / fs_guitar
# print(signal_guitar)
# N_guitar = len(signal_guitar)
# print(N_guitar)
# fft_guitar = np.fft.fft(signal_guitar)
# freqs_guitar = np.fft.fftfreq(N_guitar, d=1/fs_guitar)
# print(freqs_guitar)

# # Amplitudes (normalisées)
# amplitudes_guitar = np.abs(fft_guitar)

# # Phases
# phases_guitar = np.angle(fft_guitar)

# plt.figure(1)

# # --- signal_guitar temporel ---
# plt.subplot(3, 1, 1)
# plt.plot(t_guitar, signal_guitar, label="signal_guitar temporel")
# plt.title("signal_guitar dans le domaine temporel")
# plt.xlabel("Temps (s)")
# plt.ylabel("Amplitude")
# plt.legend()
# plt.grid(True)

# # --- Amplitude spectrale ---
# plt.subplot(3, 1, 2)
# plt.plot(freqs_guitar, amplitudes_guitar, label="Spectre d'amplitude")
# plt.title("Amplitude FFT")
# plt.xlabel("Fréquence (Hz)")
# plt.ylabel("Amplitude")
# plt.legend()
# plt.grid(True)

# # --- Phase spectrale ---
# plt.subplot(3, 1, 3)
# plt.plot(freqs_guitar, phases_guitar, label="Spectre de phase")
# plt.title("Phase FFT")
# plt.xlabel("Fréquence (Hz)")
# plt.ylabel("Phase (rad)")
# plt.legend()
# plt.grid(True)


# ###########################################################################
# # window
# ###########################################################################

# signal_guitar_window = np.abs(signal_guitar)*np.hanning(len(signal_guitar))/N_guitar
# plt.figure(2)
# plt.subplot(2, 1, 1)
# plt.plot(t_guitar, signal_guitar_window, label="Signal avec fenêtre")
# plt.title("Signal avec fenêtre de Hanning")
# plt.xlabel("Temps (s)")
# plt.ylabel("Amplitude")
# plt.legend()
# plt.grid(True)

# plt.subplot(2, 1, 2)
# window = np.hanning(len(signal_guitar))
# plt.plot(t_guitar, window, linestyle='--')
# plt.title("fenêtre de Hanning")
# plt.xlabel("Temps (s)")
# plt.ylabel("Amplitude")
# plt.legend()
# plt.grid(True)


# plt.tight_layout()
# plt.show()
