from scipy.io import wavfile

inputs_path = "inputs"
outputs_path = "outputs"
audio_inputs = {
    "bassoon": "note_basson_plus_sinus_1000_hz.wav",
    "guitar": "note_guitare_lad.wav",
}


def load(inst):
    path = f"{inputs_path}/"
    if inst in audio_inputs:
        path += audio_inputs[inst]
    else:
        path += inst
    return wavfile.read(path)


def save(rate, data, filename):
    # Normalize to prevent clipping and convert to 16-bit integers
    import numpy as np

    # Normalize to [-1, 1] range
    max_val = np.max(np.abs(data))
    if max_val > 0:
        normalized_data = data / max_val
    else:
        normalized_data = data

    # Convert to 16-bit integer range [-32768, 32767]
    data_16bit = (normalized_data * 32767).astype(np.int16)

    # Use outputs_path internally
    full_path = f"{outputs_path}/{filename}"
    wavfile.write(full_path, rate, data_16bit)
