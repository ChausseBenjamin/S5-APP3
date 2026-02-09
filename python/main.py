from code.rawSignals import get_guitar, plot_raw_signals
from code.sandbox import sandbox
from code.signalFFT import SignalFFT
from code.signalModifications import apply_absolute


import numpy as np
from datetime import datetime


def main():
    print(datetime.now())
    plot_raw_signals()
    sandbox()

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
        * np.hanning(len(guitar.get_signal()))
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
