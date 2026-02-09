from code.wavSignal import WavSignal

import numpy


def apply_absolute(signal: WavSignal, newName: str = None):
    """
    Transforms a WavSignal object into its absolute.
    Direct application of the absolute.
    """
    signal.set_signal(numpy.abs(signal.get_signal()))

    if newName is None:
        signal.set_name(f"abs of {signal.get_name()}")
    else:
        signal.set_name(newName)


def trim_samples(signal: WavSignal, trim_start=0, trim_end=0):
    """
    Trim a fixed number of samples from the start and end of a signal.

    Parameters
    ----------
    signal : WavSignal
        Audio signal (mono or multi-channel)
    trim_start : int
        Number of seconds to remove from the start
    trim_end : int
        Number of seconds to remove from the end
    """
    if trim_start < 0 or trim_end < 0:
        raise ValueError("trim_start and trim_end must be non-negative")

    duration = signal.get_duration()

    start = min(trim_start, duration)
    end = duration - min(trim_end, duration - start)

    # Transforming in samples
    start = int(start * signal.get_sampling_rate())
    end = int(end * signal.get_sampling_rate())

    signal.set_signal(signal.get_signal()[start:end])
