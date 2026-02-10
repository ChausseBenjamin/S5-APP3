import copy
from code.signalFFT import SignalFFT
from code.wavSignal import WavSignal

import numpy

NOTES = {
    "SILENCE": 0,
    # 3rd octave (lower)
    "Bb3": 233.08,
    "C3": 130.81,
    "C#3": 138.59,
    "D3": 146.83,
    "Eb3": 155.56,
    "E3": 164.81,
    "F3": 174.61,
    "F#3": 185.00,
    "G3": 196.00,
    "Ab3": 207.65,
    "A3": 220.00,
    "Bb3": 233.08,
    "B3": 246.94,
    # 4th octave (original)
    "C": 261.63,
    "C#": 277.18,
    "D": 293.66,
    "Eb": 311.13,
    "E": 329.63,
    "F": 349.23,
    "F#": 369.99,
    "G": 392.00,
    "Ab": 415.30,
    "A": 440.00,
    "Bb": 466.16,
    "B": 493.88,
    # other names
    "DO": 261.63,
    "DO#": 277.18,
    "RÉ": 293.66,
    "RÉ#": 311.13,
    "MI": 329.63,
    "FA": 349.23,
    "FA#": 369.99,
    "SOL": 392.00,
    "SOL#": 415.30,
    "LA": 440.00,
    "LA#": 466.16,
    "SI": 493.88,
}


BEAT = 60 / 35
WHOLE = BEAT
HALF = WHOLE / 2
QUARTER = WHOLE / 4
DOT_QUARTER = 1.5 * QUARTER
EIGHT = WHOLE / 8
SIXTEEN = WHOLE / 16

AMONG_US = [
    {"note": "C", "duration": EIGHT},
    {"note": "Eb", "duration": EIGHT},
    {"note": "F", "duration": EIGHT},
    {"note": "F#", "duration": EIGHT},
    {"note": "F", "duration": EIGHT},
    {"note": "Eb", "duration": EIGHT},
    {"note": "C", "duration": DOT_QUARTER},
    {"note": "Bb3", "duration": SIXTEEN},
    {"note": "D", "duration": SIXTEEN},
    {"note": "C", "duration": HALF},
    {"note": "C", "duration": EIGHT},
    {"note": "Eb", "duration": EIGHT},
    {"note": "F", "duration": EIGHT},
    {"note": "F#", "duration": EIGHT},
    {"note": "F", "duration": EIGHT},
    {"note": "Eb", "duration": EIGHT},
    {"note": "F#", "duration": HALF},
    {"note": "F#", "duration": EIGHT},
    {"note": "F", "duration": EIGHT},
    {"note": "Eb", "duration": EIGHT},
    {"note": "F#", "duration": EIGHT},
    {"note": "F", "duration": EIGHT},
    {"note": "Eb", "duration": EIGHT},
    {"note": "C", "duration": WHOLE},
]

BEAT = 60 / 90
WHOLE = BEAT
HALF = WHOLE / 2
QUARTER = WHOLE / 4
DOT_QUARTER = 1.5 * QUARTER
EIGHT = WHOLE / 8
DOT_EIGHT = 1.5 * EIGHT
SIXTEEN = WHOLE / 16
DOT_SIXTEEN = 1.5 * SIXTEEN
THIRTY_TWO = WHOLE / 32

BETHOVEN = [
    {"note": "SOL", "duration": QUARTER},
    {"note": "SOL", "duration": QUARTER},
    {"note": "SOL", "duration": QUARTER},
    {"note": "MI", "duration": WHOLE * 1.5},
    {"note": "FA", "duration": QUARTER},
    {"note": "FA", "duration": QUARTER},
    {"note": "FA", "duration": QUARTER},
    {"note": "RÉ", "duration": WHOLE * 3},
]

BEAT = 138 / 60
WHOLE = BEAT
HALF = WHOLE / 2
QUARTER = WHOLE / 4
DOT_QUARTER = 1.5 * QUARTER
EIGHT = WHOLE / 8
DOT_EIGHT = 1.5 * EIGHT
SIXTEEN = WHOLE / 16
DOT_SIXTEEN = 1.5 * SIXTEEN
THIRTY_TWO = WHOLE / 32

TRICKY = [
    # # PART 1
    {"note": "Eb", "duration": DOT_SIXTEEN / 1.25},
    {"note": "Eb", "duration": SIXTEEN / 1.40},
    {"note": "Eb", "duration": SIXTEEN / 1.40},
    {"note": "Eb", "duration": DOT_EIGHT},
    # REPEAT Part 1
    {"note": "Eb", "duration": DOT_SIXTEEN / 1.25},
    {"note": "Eb", "duration": SIXTEEN / 1.40},
    {"note": "Eb", "duration": SIXTEEN / 1.40},
    {"note": "Eb", "duration": DOT_EIGHT},
    # PART 2
    {"note": "Eb", "duration": DOT_SIXTEEN / 1.25},
    {"note": "Eb", "duration": DOT_SIXTEEN / 1.25},
    {"note": "Eb", "duration": DOT_SIXTEEN / 1.25},
    {"note": "Eb", "duration": DOT_SIXTEEN / 1.25},
    {"note": "Eb", "duration": DOT_SIXTEEN / 1.25},
    {"note": "Eb", "duration": SIXTEEN / 1.40},
    {"note": "Eb", "duration": SIXTEEN / 1.40},
    {"note": "Eb", "duration": QUARTER},
    # PART 3
    {"note": "Eb3", "duration": DOT_EIGHT},
    {"note": "Eb3", "duration": DOT_EIGHT},
    {"note": "Eb3", "duration": DOT_EIGHT},
    {"note": "Eb3", "duration": DOT_EIGHT},
    {"note": "Eb3", "duration": EIGHT / 1.15},
    {"note": "E3", "duration": DOT_EIGHT / 1.25},
    {"note": "F3", "duration": EIGHT / 1.25},
    {"note": "F#3", "duration": DOT_EIGHT},
    {"note": "F#3", "duration": DOT_QUARTER},
    # PART 4
    {"note": "Bb3", "duration": DOT_EIGHT},
    {"note": "Bb3", "duration": DOT_EIGHT},
    {"note": "Bb3", "duration": DOT_EIGHT},
    {"note": "Bb3", "duration": EIGHT},
    {"note": "A3", "duration": EIGHT},
    {"note": "Ab3", "duration": EIGHT},
    {"note": "G3", "duration": EIGHT},
    {"note": "F#3", "duration": QUARTER / 1.25},
    # Copy of part 3 and 4
    # PART 3
    {"note": "Eb3", "duration": DOT_EIGHT},
    {"note": "Eb3", "duration": DOT_EIGHT},
    {"note": "Eb3", "duration": DOT_EIGHT},
    {"note": "Eb3", "duration": DOT_EIGHT},
    {"note": "Eb3", "duration": EIGHT / 1.15},
    {"note": "E3", "duration": DOT_EIGHT / 1.25},
    {"note": "F3", "duration": EIGHT / 1.25},
    {"note": "F#3", "duration": DOT_EIGHT},
    {"note": "F#3", "duration": DOT_QUARTER},
    # PART 4
    {"note": "Bb3", "duration": DOT_EIGHT},
    {"note": "Bb3", "duration": DOT_EIGHT},
    {"note": "Bb3", "duration": DOT_EIGHT},
    {"note": "Bb3", "duration": EIGHT},
    {"note": "A3", "duration": EIGHT},
    {"note": "Ab3", "duration": EIGHT},
    {"note": "G3", "duration": EIGHT},
    {"note": "F#3", "duration": QUARTER},
]


def optimized_build_synthesized_note(
    harmonics_frequency_indexes,
    harmonics_peaks,
    enveloppe: WavSignal,
    originalSignal: WavSignal,
    k: float = 1,
):
    fft = SignalFFT(originalSignal)

    sample_count = originalSignal.get_sample_count()
    sampling_rate = originalSignal.get_sampling_rate()

    # Copy signal metadata only
    new_signal = copy.deepcopy(originalSignal)
    new_signal.set_name(f"synthesized {originalSignal.get_name()}")

    # Time axis (seconds)
    t = numpy.arange(sample_count) / sampling_rate

    # Fetch FFT data ONCE
    frequencies = fft.get_frequencies_axis()[harmonics_frequency_indexes]
    phases = fft.get_phases()[harmonics_frequency_indexes]
    amplitudes = numpy.asarray(harmonics_peaks)

    # Envelope
    envelope = enveloppe.get_signal().astype(numpy.float64)

    # Build harmonics matrix: shape (num_harmonics, num_samples)
    # Each row is one harmonic over time
    harmonics = amplitudes[:, None] * numpy.sin(
        2 * numpy.pi * frequencies[:, None] * t * k + phases[:, None]
    )

    # Sum all harmonics
    synthesized = harmonics.sum(axis=0)

    # Apply envelope
    synthesized *= envelope[: len(synthesized)]

    # Normalize
    max_val = numpy.max(numpy.abs(synthesized))
    if max_val > 0:
        synthesized /= max_val

    # Match original signal scale
    max_old = numpy.max(numpy.abs(originalSignal.get_signal()))
    synthesized *= max_old

    # Convert to int16
    new_signal.set_signal(synthesized.astype(numpy.int16))

    return new_signal


def build_synthesized_note(
    harmonics_frequency_indexes,
    harmonics_peaks,
    enveloppe: WavSignal,
    originalSignal: WavSignal,
):
    """
    This is built from the sum of harmonics sins.

    The formula is as followed:
    $$
    e[n] * \\sum_{i=0}^{31} A[i] * \\sin(2*pi*f_i\\pi*n*Te + phase[i])
    $$
    """
    fft = SignalFFT(originalSignal)
    amount_of_harmonics = len(harmonics_frequency_indexes)
    sampling_period = originalSignal.get_sampling_rate()
    new_signal = copy.deepcopy(originalSignal)
    new_signal.set_name(f"synthesized {originalSignal.get_name()}")

    # IMPORTANT: convert signal buffer to float
    new_signal.set_signal(new_signal.get_signal().astype(numpy.float64))

    max_val = numpy.max(numpy.abs(new_signal.get_signal()))

    if max_val > 0:
        new_signal.set_signal(new_signal.get_signal() / max_val)

    sample_count = originalSignal.get_sample_count()

    print("Computing synthesized signal... This may take a while...")
    for n in range(sample_count):
        enveloppe_value = enveloppe.get_signal()[n]
        sum = 0
        for i in range(amount_of_harmonics):
            amplitude = harmonics_peaks[i]
            frequency_index = harmonics_frequency_indexes[i]
            frequency = fft.get_frequencies_axis()[frequency_index]
            phase = fft.get_phases()[frequency_index]

            sum = sum + amplitude * numpy.sin(
                2 * numpy.pi * frequency * n * (1 / sampling_period) + phase
            )

        original = new_signal.get_signal()
        original[n] = enveloppe_value * sum
        new_signal.set_signal(original)

    print("finished! Converting to 16 bits...")
    max_new_signal = numpy.max(numpy.abs(new_signal.get_signal()))
    max_old_signal = numpy.max(numpy.abs(originalSignal.get_signal()))
    difference = max_old_signal / max_new_signal

    new_signal.set_signal(numpy.int16(new_signal.get_signal() * difference))

    return new_signal


def get_music(
    synthesized_note: WavSignal,
    original_frequency: int,
    harmonics_frequency_indexes,
    harmonics_peaks,
    enveloppe: WavSignal,
    originalSignal: WavSignal,
    music=AMONG_US,
):
    generated = []

    for n in music:
        name = n["note"]
        duration = n["duration"]

        freq = NOTES[name]
        # note = shift_pitch_resample(
        #     original_frequency, freq, synthesized_note, duration
        # )
        ratio = freq / original_frequency
        note = optimized_build_synthesized_note(
            harmonics_frequency_indexes,
            harmonics_peaks,
            enveloppe,
            originalSignal,
            ratio,
        )
        signal = note.get_signal()[
            6000 : int(duration * note.get_sampling_rate()) + 6000
        ]
        generated.append(signal)

    # Concatenate everything ONCE (much cleaner)
    full_signal = numpy.concatenate(generated)

    music_wav = copy.deepcopy(synthesized_note)
    music_wav.set_signal(full_signal)
    return music_wav
