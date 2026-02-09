import copy
from code.signalFFT import SignalFFT
from code.wavSignal import WavSignal

import numpy
from scipy.signal import resample

NOTES = {
    "SILENCE": 0,
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
    "DO": 261.6,
    "DO#": 277.2,
    "RÉ": 293.7,
    "RÉ#": 311.1,
    "MI": 329.6,
    "FA": 349.2,
    "FA#": 370.0,
    "SOL": 392.0,
    "SOL#": 415.3,
    "LA": 440.0,
    "LA#": 446.2,
    "SI": 493.9,
}

BEAT = 90 / 60
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
    {"note": "Bb", "duration": SIXTEEN},
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


# def shift_pitch_resample(wav_in, wav_out, original_freq, target_freq):
def shift_pitch_resample(
    original_frequency: float, new_frequency: float, original_note: WavSignal, duration
):
    """
    Shifts pitch using resampling. Resulting duration changes naturally.
    """
    audio = original_note.get_signal().astype(numpy.float64)
    sr = original_note.get_sampling_rate()

    # Compute new length to match desired pitch
    ratio = original_frequency / new_frequency
    new_length = int(len(audio) * ratio)

    # Resample once — pitch changes, duration changes naturally
    shifted = resample(audio, new_length)

    # Return a new WavSignal
    new_note = copy.deepcopy(original_note)
    new_note.set_signal(shifted.astype(audio.dtype))
    return new_note


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

        if name != "SILENCE":
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
            print(duration)
            signal = note.get_signal()[
                6000 : int(duration * note.get_sampling_rate()) + 6000
            ]
            generated.append(signal)
        else:
            silence_samples = int(duration * synthesized_note.get_sampling_rate())
            generated.append(numpy.zeros(silence_samples))

    # Concatenate everything ONCE (much cleaner)
    full_signal = numpy.concatenate(generated)

    music_wav = copy.deepcopy(synthesized_note)
    music_wav.set_signal(full_signal)
    return music_wav
