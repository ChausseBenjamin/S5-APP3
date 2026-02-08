from code.saveFigure import save_plot
from code.wavSignal import WavSignal

import matplotlib.pyplot as plt
import numpy


class SignalFFT:
    """
    Class which purpose is to contain the FFT of a WavSignal.
    It does everything for you, including plotting.
    """

    def __init__(self, signal: WavSignal, amountOfSin: int = 32):
        self._ogSignal = signal
        self._sinKept = amountOfSin

        fft = numpy.fft.fft(signal.get_signal())

        frequencies = numpy.fft.fftfreq(
            signal.get_sample_count(), d=(1 / signal.get_sampling_rate())
        )
        amplitudes = numpy.abs(fft)
        phases = numpy.angle(fft)

        # TODO: How the fuck do I only keep the 32 most important harmonics without fucking up the graphs?!
        self._frequencies = frequencies
        self._amplitudes = amplitudes
        self._phases = phases

    # Getters
    def get_amplitudes(self):
        """
        Obtain an array of amplitudes for each frequencies of the FFT
        """
        return self._amplitudes

    def get_frequencies_axis(self):
        """
        The x axis of frequencies used when plotting graphs for ffts
        """
        return self._frequencies

    def get_phases(self):
        """
        Obtain an array of phases for each frequencies of the FFT
        """
        return self._phases

    def get_fft(self):
        """
        Obtain the FFT of the given signal.
        """
        return self._fft

    def get_signal(self):
        """
        Get the signal you originally gave to this object, to access its metadata
        """
        return self._ogSignal

    def print_info(self):
        """
        Debugging
        """
        print(f"FFT of {self.get_signal().get_name()}")
        print(f"\t - Amount of sins kept:    {self._sinKept}")
        print(f"\t - Size of frequency axis: {len(self.get_frequencies_axis())}")

    def partial_phase_plot(self):
        """
        Integrates this fft's phases within a larger plot.
        You handle the business, but this essentially
        does the plt for you so you dont have to mess
        with the getters.
        """
        plt.plot(self.get_frequencies_axis(), self.get_phases(), label="Phases")
        plt.title(f"Spectre de phases de {self.get_signal().get_name()}")
        plt.xlabel("Fréquence (Hz)")
        plt.ylabel("Phase (rad)")
        plt.legend()
        plt.grid(True)

    def partial_amplitude_plot(self):
        """
        Integrates this fft's amplitude within a larger plot.
        You handle the business, but this essentially
        does the plt for you so you dont have to mess
        with the getters.
        """
        plt.plot(
            self.get_frequencies_axis(),
            self.get_amplitudes(),
            label="Amplitudes",
        )
        plt.title(f"Spectre fréquentielle de {self.get_signal().get_name()}")
        plt.xlabel("Fréquence (Hz)")
        plt.ylabel("Phase (rad)")
        plt.legend()
        plt.grid(True)

    def full_plot(self, show: bool, save: bool):
        """
        Plot the full signal's FFGet signalT.
        """
        plt.figure()

        plt.subplot(3, 1, 1)
        self.get_signal().partial_plot()

        plt.subplot(3, 1, 2)
        self.partial_amplitude_plot()

        plt.subplot(3, 1, 3)
        self.partial_phase_plot()

        if show:
            plt.show()
        if save:
            save_plot(f"full_fft_{self.get_signal().get_name()}")

        plt.close()
