import librosa
import soundfile as sf

def load_beat_times(audio_path):
    data, sr = sf.read(audio_path)
    y = librosa.util.buf_to_float(data)
    hop_length = 512
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=22050, hop_length=hop_length)
    beat_times = librosa.frames_to_time(beat_frames, sr=22050, hop_length=hop_length)

    return beat_times