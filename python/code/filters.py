import numpy


def normalized_frequency():
    """
    returns the normalized frequency
    which is pi/1000
    """
    return numpy.pi / 1000


def normalized_to_hertz(normalized, sampling_rate):
    sampling_frequency = 1 / sampling_rate
    return (normalized * sampling_frequency) / (2 * numpy.pi)


def hertz_to_normalized(hertz, sampling_rate):
    return (2 * numpy.pi * hertz) / (1 / sampling_rate)


def best_sliding_average_low_pass_coefficient(
    wanted_gain_dB: int,
    max_tries: int = 1000,
    lowest_coefficient: int = 1,
    highest_coefficient: int = 1000,
    normalized_frequency: float = normalized_frequency(),
):
    """
    Automatically finds the best N order for a sliding average
    low pass filter through trial and errors.

    It's possible that the best N is a float, the closest is returned
    if that's the case.

    :param wanted_gain: Description
    :type wanted_gain: int - 3
    """
    # To optimize the testing of N values, we test N in the middle of the allowed range.
    # Then, if its above, we test a new middle, so on and so forth until the 2 N values
    # are 1 appart, meaning it can't get closer than that.
    current_try = 0
    wanted_gain_dB = numpy.abs(wanted_gain_dB)

    print(
        f"Calculating best N order for a sliding average low-pass filter for a gain of {wanted_gain_dB}dB at normalized frequency: {normalized_frequency}"
    )

    while current_try < max_tries:
        current_try = current_try + 1

        tested_filter_order = numpy.round(
            (highest_coefficient + lowest_coefficient) / 2
        )
        gain_at_tested_order = sliding_average_low_pass_response(
            tested_filter_order, normalized_frequency=normalized_frequency
        )

        gain_db = numpy.abs(20 * numpy.log10(gain_at_tested_order))

        # Set new low and high thresholds depending on if we overshot or undershot the wanted gain.
        if gain_db > wanted_gain_dB:
            highest_coefficient = tested_filter_order
        else:
            lowest_coefficient = tested_filter_order

        # testing is finished once the difference between the lowest and the highest coefficient is below 1.
        if (highest_coefficient - lowest_coefficient) <= 1:
            print(
                f"\tG: N = {tested_filter_order}, gain = {gain_db}dB, attempt = {current_try}"
            )
            return tested_filter_order
        print(
            f"\tX: N = {tested_filter_order}, gain = {gain_db}dB, attempt = {current_try}"
        )

    print(
        f"FATAL! Exceeded the maximum amount of tries: {max_tries} to obtain the N order of the filter!"
    )
    return 0


def sliding_average_low_pass_response(
    coefficient_count: int, normalized_frequency: float = normalized_frequency()
):
    """
    Lyons low pass filter formula.
    Gets the gain at a given normalized frequency for an N order.
    The response is calculated through the frequency response, which requires a sum.
    It would be possible to not need the sum by using the geometric series to
    simplify it, but python just allows us to do a sum. So... why not.

    Formula is the following:
    $$
    H=\\frac{1}{N}\\sum^{N-1}_{n=0}e^{-j\\bar\\omega}
    $$
    """
    all_N = numpy.arange(coefficient_count)
    average = 1 / coefficient_count

    gain = average * numpy.sum(numpy.exp(-1j * normalized_frequency * all_N))
    return numpy.abs(gain)


def sliding_average_low_pass_frequency_response(coefficient_count: int, fe):
    filter_order = int(coefficient_count)
    # h = numpy.ones(filter_order)
    # reponse_impuls = (1 / (filter_order)) * h
    Fc = numpy.pi / 1000 * fe / (2 * numpy.pi)
    K = (Fc * 2 * filter_order / fe) + 1
    n = numpy.linspace(
        -(filter_order - 1) / 2, (filter_order - 1) / 2 + 1, filter_order
    )
    num = numpy.sin(numpy.pi * n * K / filter_order)
    denum = numpy.sin(numpy.pi * n / filter_order)
    reponse_impuls = (1 / filter_order) * (num / denum)

    fft = numpy.fft.rfft(reponse_impuls)
    amplitudes = numpy.abs(fft)

    impuls_db = 20 * numpy.log10(amplitudes)
    freq = numpy.fft.rfftfreq(filter_order, 1 / fe)

    return freq, impuls_db
