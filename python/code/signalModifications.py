from code.wavSignal import WavSignal

import numpy


def applyAbsolute(signal: WavSignal, newName: str = None):
    """
    Transforms a WavSignal object into its absolute.
    Direct application of the absolute.
    """
    signal.set_signal(numpy.abs(signal.get_signal()))

    if newName is None:
        signal.set_name(f"abs of {signal.get_name()}")
    else:
        signal.set_name(newName)
