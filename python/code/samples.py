from scipy.io import wavfile

samples_path = "inputs"
audio_inputs = {
    "bassoon": "note_basson_plus_sinus_1000_hz.wav",
    "guitar": "note_guitare_lad.wav",
}


def load(inst="bassoon"):
    path = samples_path
    if inst in audio_inputs:
        path += audio_inputs[inst]
    else:
        path += f"/{inst}"
    return wavfile.read(path)


def save(path):
    wavfile.read()
