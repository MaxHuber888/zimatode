import librosa
import soundfile as sf
import numpy as np

def analyze_audio(audio_path, n_mels=128):
    """
    Analyzes audio file and returns beat times and frequency band energies over time.
    """
    # Load audio
    data, sr = sf.read(audio_path)
    y = librosa.util.buf_to_float(data)

    # Parameters for analysis
    hop_length = 512  # Number of samples between successive frames

    # Get beat times (keeping this for reference)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop_length)

    # Compute mel spectrogram
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, hop_length=hop_length)

    # Convert to dB scale
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

    # Define frequency band ranges (in mel bands)
    low_band = slice(0, n_mels // 4)  # Lower 25% of frequencies
    mid_band = slice(n_mels // 4, 3 * n_mels // 4)  # Middle 50%
    high_band = slice(3 * n_mels // 4, n_mels)  # Upper 25%

    # Calculate energy in each band over time
    low_energy = np.mean(mel_spec_db[low_band], axis=0)
    mid_energy = np.mean(mel_spec_db[mid_band], axis=0)
    high_energy = np.mean(mel_spec_db[high_band], axis=0)

    # Normalize energies to [0, 1] range
    def normalize(x):
        return (x - np.min(x)) / (np.max(x) - np.min(x))

    energies = {
        'low': normalize(low_energy),
        'mid': normalize(mid_energy),
        'high': normalize(high_energy),
        'times': librosa.frames_to_time(np.arange(len(low_energy)), sr=sr, hop_length=hop_length)
    }

    return beat_times, energies

def get_current_energy(current_time, frequency_energies, energy_threshold, impulse_strength):
    """Get energy values for the current time."""

    # Find the closest time index
    times = frequency_energies['times']
    time_idx = np.searchsorted(times, current_time)
    if time_idx >= len(times):
        return 0, 0, 0, 0

    # Get raw energy values
    low_energy = frequency_energies['low'][time_idx]
    mid_energy = frequency_energies['mid'][time_idx]
    high_energy = frequency_energies['high'][time_idx]

    # Apply threshold
    low_energy = low_energy if low_energy > energy_threshold else 0
    mid_energy = mid_energy if mid_energy > energy_threshold else 0
    high_energy = high_energy if high_energy > energy_threshold else 0

    # Calculate combined energy
    combined_energy = (low_energy + mid_energy + high_energy) / 3

    # Scale by impulse strength
    return (
        low_energy * impulse_strength,
        mid_energy * impulse_strength,
        high_energy * impulse_strength,
        combined_energy * impulse_strength
    )