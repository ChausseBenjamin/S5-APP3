from code.saveFigure import save_plot
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile


class WavSignal:
    """
    Class which purpose is to contain a .wav signal.
    Instanciate it with the path to a .wav signal.
    You'll then be able to obtain the duration, amount of samples
    and perform other tasks to the signal.
    """

    def __init__(self, path: str):
        self._path = path
        self._name = Path(self._path).stem
        self._fs, self._signal = wavfile.read(path)
        self._N = len(self._signal)
        self._t = np.arange(self._N) / self._fs

    def save(self):
        wavfile.write(
            f"audio/{self.get_name()}.wav", self.get_sampling_rate(), self.get_signal()
        )

    # Setters
    def set_name(self, name: str):
        self._name = name

    def set_signal(self, newSignal):
        """
        So you can modify the signal and give it back.
        """
        self._signal = newSignal
        print()
        self._N = len(self._signal)
        self._t = np.arange(self._N) / self._fs

    # Getters
    def get_sampling_rate(self):
        return self._fs

    def get_duration(self):
        """
        Returned in seconds, from the sampling rate and total amount of samples
        """
        return self.get_sample_count() / self.get_sampling_rate()

    def get_signal(self):
        return self._signal

    def get_time_axis(self):
        return self._t

    def get_sample_count(self):
        return self._N

    def get_path(self):
        return self._path

    def get_name(self):
        return self._name

    def print_info(self):
        print(f"{self.get_name()}:")
        print(f"\t- Sample rate: {self.get_sampling_rate()}")
        print(f"\t- N:           {self.get_sample_count()}")
        print(f"\t- Duration:    {self.get_duration()}")
        print(f"\t- Signal:      {self.get_signal()}")
        print(f"\t- Time:        {self.get_time_axis()}")

    def partial_plot(self):
        """
        Integrates this signal within a larger plot.
        You handle the business, but this essentially
        does the plt for you so you dont have to mess
        with the getters.

        Does not apply a title.
        """
        plt.plot(self.get_time_axis(), self.get_signal(), label=self.get_name())
        plt.xlabel("Temps (s)")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.grid(True)

    def full_plot(self, show: bool = True, save: bool = True):
        """
        Plot the raw signal using matplotlib.
        Titles and axis automatically done.
        Hardcoded image output path.
        """
        plt.figure()

        # --- signal_guitar temporel ---
        self.partial_plot()
        plt.title(f"Raw {self.get_name()}")

        if show:
            plt.show()
        if save:
            save_plot(self.get_name())
        plt.close()
