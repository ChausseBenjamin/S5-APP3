import numpy as np
from scipy.io import wavfile


class WavSignal:
    """
    Class which purpose is to contain a .wav signal.
    Instanciate it with the path to a .wav signal.
    You'll then be able to obtain the duration, amount of samples
    and perform other tasks to the signal.
    """

    def __init__(self, path):
        self._path = path
        self._fs, self._signal = wavfile.read(path)
        self._N = len(self._signal)
        self._t = np.arange(self._N) / self._fs

    # Getters
    def get_sampling_rate(self):
        return self._fs

    def get_signal(self):
        return self._signal

    def get_time_axis(self):
        return self._t

    def get_num_samples(self):
        return self._N

    def get_path(self):
        return self._path
