import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
from scipy.io import wavfile
from scipy import signal
from code.rawSignals import get_bassoon


def gen_notch(f0=1000):
    fs = 44100  # Use actual sampling rate of bassoon signal
    N = 4410  # 0.1 seconds at 44100 Hz - reasonable filter length
    x = np.linspace(0, N / fs, N)
    H = np.ones(N, dtype=complex)
    f0_idx = int(f0 * (N / fs))
    H[f0_idx] = 0  # zero amplitude at 1 kHz
    H[N - f0_idx] = 0  # symmetric bin for negative frequency
    amps = ifft(H).real
    plt.plot(x, amps)
    # plt.plot(x, phi)
    plt.show(block=True)
    return amps


def gen_sound():
    """
    Generate sound by convolving bassoon signal with the filter impulse response from sandbox()
    """
    # Get the impulse response (filter) from sandbox
    h = gen_notch()

    # Load the bassoon signal
    bassoon_signal = get_bassoon()
    bassoon_data = bassoon_signal.get_signal()
    fs = bassoon_signal.get_sampling_rate()

    print(f"Bassoon signal: {len(bassoon_data)} samples at {fs} Hz")
    print(f"Filter impulse response: {len(h)} samples")

    # Check the filter's frequency response at 1kHz
    H_freq = fft(h, n=len(bassoon_data))
    freqs = np.fft.fftfreq(len(bassoon_data), 1 / fs)
    freq_1khz_idx = np.argmin(np.abs(freqs - 1000))
    print(f"Filter response at 1kHz: {np.abs(H_freq[freq_1khz_idx]):.6f}")

    # Convolve the bassoon signal with the impulse response
    filtered_signal = np.convolve(bassoon_data, h, mode="same")

    # Check the frequency content of the filtered signal
    filtered_fft = fft(filtered_signal)
    print(
        f"Filtered signal amplitude at 1kHz: {np.abs(filtered_fft[freq_1khz_idx]):.6f}"
    )

    # Normalize to prevent clipping
    filtered_signal = filtered_signal / np.max(np.abs(filtered_signal)) * 0.8

    # Convert to int16 for wav file
    filtered_signal_int = (filtered_signal * 32767).astype(np.int16)

    # Save as out.wav
    wavfile.write("out.wav", fs, filtered_signal_int)

    print(f"Generated out.wav with {len(filtered_signal)} samples at {fs} Hz")

    # Plot the final sanitized bassoon (freq+phase+wave)
    from code.saveFigure import save_plot

    # Create time array for waveform plot
    t = np.linspace(0, len(filtered_signal) / fs, len(filtered_signal))

    # Compute FFT for frequency and phase analysis
    filtered_fft = fft(filtered_signal)
    freqs = np.fft.fftfreq(len(filtered_signal), 1 / fs)

    # Only take positive frequencies for plotting
    positive_freqs = freqs[: len(filtered_signal) // 2]
    magnitude = np.abs(filtered_fft[: len(filtered_signal) // 2])
    phase = np.angle(filtered_fft[: len(filtered_signal) // 2])

    plt.figure()

    # 1. Waveform - show the full time domain signal
    plt.subplot(3, 1, 1)
    plt.plot(t, filtered_signal, label="Sanitized Bassoon")
    plt.title("Signal temporel - Basson sanitisé")
    plt.xlabel("Temps (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)

    # 2. Frequency Response (Magnitude)
    plt.subplot(3, 1, 2)
    plt.plot(positive_freqs, magnitude, label="Amplitude")
    plt.title("Spectre d'amplitude - Basson sanitisé")
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)

    # 3. Phase Response
    plt.subplot(3, 1, 3)
    plt.plot(positive_freqs, phase, label="Phases")
    plt.title("Spectre de phase - Basson sanitisé")
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Phase (rad)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    save_plot("sanitized_bassoon_analysis")
    plt.close()

    print("Sanitized bassoon analysis plots saved as sanitized_bassoon_analysis.png")

    return filtered_signal


def sandbox_2():
    """
    Convolve guitar signal with a proper reverb impulse response (multiple reflections + exponential decay).
    Output is saved as convolved.wav
    """
    # Get the guitar signal using the helper function from rawSignals
    from code.rawSignals import get_guitar

    guitar_signal = get_guitar()
    guitar_data = guitar_signal.get_signal()
    fs = guitar_signal.get_sampling_rate()

    print(f"Guitar signal: {len(guitar_data)} samples at {fs} Hz")

    # Create a proper reverb impulse response over 4 seconds
    duration_s = 4.0  # 4 seconds reverb tail
    num_samples = int(fs * duration_s)

    # Create time array
    t = np.linspace(0, duration_s, num_samples)

    # 1. Start with white noise for dense reflections
    np.random.seed(42)  # For reproducible results
    noise = np.random.randn(num_samples)

    # 2. Apply exponential decay envelope
    tau = duration_s / 4.6  # Decay time constant
    decay_envelope = np.exp(-t / tau)

    # 3. Create the diffuse reverb tail (starts immediately but at low level)
    reverb_tail = noise * decay_envelope * 0.2  # Lower level for tail

    # 4. Add early reflections (including some immediate ones)
    early_reflections = np.zeros(num_samples)

    # Include immediate reflections to avoid dry gap
    reflection_delays = [
        int(0.005 * fs),  # 5ms - very early reflection
        int(0.012 * fs),  # 12ms
        int(0.025 * fs),  # 25ms
        int(0.045 * fs),  # 45ms
        int(0.070 * fs),  # 70ms
        int(0.100 * fs),  # 100ms
        int(0.140 * fs),  # 140ms
    ]
    reflection_gains = [0.4, 0.5, 0.6, 0.4, 0.3, 0.25, 0.2]

    for delay, gain in zip(reflection_delays, reflection_gains):
        if delay < num_samples:
            early_reflections[delay] = gain

    # 5. Combine everything
    final_impulse = np.zeros(num_samples)

    # Direct sound (original)
    final_impulse[0] = 1.0

    # Add early reflections
    final_impulse += early_reflections

    # Add diffuse tail starting from beginning (but builds up over time)
    final_impulse += reverb_tail

    print(f"Reverb impulse: {len(final_impulse)} samples ({duration_s} s)")
    print(f"Early reflections: {len(reflection_delays)} discrete reflections")
    print(f"First reflection at: {reflection_delays[0] / fs * 1000:.1f} ms")
    print(f"Decay time constant τ = {tau:.3f} s")

    # Convolve the guitar signal with the reverb impulse
    convolved_signal = np.convolve(guitar_data, final_impulse, mode="full")

    print(f"Convolved signal: {len(convolved_signal)} samples")

    # Normalize to prevent clipping
    max_val = np.max(np.abs(convolved_signal))
    if max_val > 0:
        convolved_signal = convolved_signal / max_val * 0.8

    # Convert to int16 for wav file
    convolved_signal_int = (convolved_signal * 32767).astype(np.int16)

    # Save as convolved.wav
    wavfile.write("convolved.wav", fs, convolved_signal_int)

    print(f"Generated convolved.wav with {len(convolved_signal)} samples at {fs} Hz")
    return convolved_signal


def plot_reverb_analysis():
    """
    Plot the reverb impulse response, frequency response, and phase response.
    """
    from code.saveFigure import save_plot

    # Recreate the same reverb impulse from sandbox_2 for analysis
    fs = 44100  # Standard sample rate
    duration_s = 4.0
    num_samples = int(fs * duration_s)

    # Create time array
    t = np.linspace(0, duration_s, num_samples)

    # Generate the same reverb impulse
    np.random.seed(42)  # Same seed for reproducibility
    noise = np.random.randn(num_samples)
    tau = duration_s / 4.6
    decay_envelope = np.exp(-t / tau)
    reverb_tail = noise * decay_envelope * 0.2

    early_reflections = np.zeros(num_samples)
    reflection_delays = [
        int(0.005 * fs),
        int(0.012 * fs),
        int(0.025 * fs),
        int(0.045 * fs),
        int(0.070 * fs),
        int(0.100 * fs),
        int(0.140 * fs),
    ]
    reflection_gains = [0.4, 0.5, 0.6, 0.4, 0.3, 0.25, 0.2]

    for delay, gain in zip(reflection_delays, reflection_gains):
        if delay < num_samples:
            early_reflections[delay] = gain

    final_impulse = np.zeros(num_samples)
    final_impulse[0] = 1.0
    final_impulse += early_reflections
    final_impulse += reverb_tail

    # Compute frequency response
    impulse_fft = fft(final_impulse)
    freqs = np.fft.fftfreq(num_samples, 1 / fs)

    # Only take positive frequencies for plotting
    positive_freqs = freqs[: num_samples // 2]
    magnitude = np.abs(impulse_fft[: num_samples // 2])
    phase = np.angle(impulse_fft[: num_samples // 2])

    # Create plots
    plt.figure(figsize=(15, 10))

    # 1. Impulse Response (first 500ms)
    plt.subplot(3, 1, 1)
    time_ms = t * 1000
    plot_samples = int(0.5 * fs)  # First 500ms
    plt.plot(time_ms[:plot_samples], final_impulse[:plot_samples])
    plt.title("Reverb Impulse Response (First 500ms)")
    plt.xlabel("Time (ms)")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)

    # 2. Frequency Response (Magnitude)
    plt.subplot(3, 1, 2)
    plt.semilogx(
        positive_freqs[1:], 20 * np.log10(magnitude[1:] + 1e-12)
    )  # Skip DC, add small value to avoid log(0)
    plt.title("Frequency Response (Magnitude)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.grid(True, alpha=0.3)
    plt.xlim(20, fs / 2)  # Audio range

    # 3. Phase Response
    plt.subplot(3, 1, 3)
    plt.semilogx(
        positive_freqs[1:], np.unwrap(phase[1:]) * 180 / np.pi
    )  # Convert to degrees
    plt.title("Phase Response")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase (degrees)")
    plt.grid(True, alpha=0.3)
    plt.xlim(20, fs / 2)

    plt.tight_layout()
    save_plot("reverb_analysis")
    plt.close()

    print("Reverb analysis plots saved as reverb_analysis.png")
    print(f"Impulse length: {len(final_impulse)} samples ({duration_s} s)")
    print(f"Sample rate: {fs} Hz")
    print(f"Frequency resolution: {fs / num_samples:.2f} Hz/bin")
