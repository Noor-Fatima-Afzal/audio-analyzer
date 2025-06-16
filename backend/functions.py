from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import matplotlib.pyplot as plt
from io import BytesIO
import librosa
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')

# Ensure the directory exists
FEATURES_DIR = os.path.join('uploads', 'features')
os.makedirs(FEATURES_DIR, exist_ok=True)

def get_bitrate(file_path):
    try:
        if file_path.lower().endswith('.mp3'):
            audio = MP3(file_path)
            bitrate = audio.info.bitrate
        elif file_path.lower().endswith('.wav'):
            audio = WAVE(file_path)
            # For WAV files, we need to calculate the bitrate
            bitrate = audio.info.sample_rate * audio.info.bits_per_sample * audio.info.channels
        else:
            raise ValueError('Unsupported file format')
        
        return bitrate
    except Exception as e:
        print(f"Error: {e}")
        return None

def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)
    return y, sr

def plot_waveform_with_sampling_rate(file_path, filename, username):
    # Load the audio file
    audio_data, sampling_rate = load_audio(file_path)

    # Time axis for the waveform
    time = np.linspace(0, len(audio_data) / sampling_rate, num=len(audio_data))

    # Plot the waveform
    plt.figure(figsize=(10, 4))
    plt.plot(time, audio_data, label='Audio waveform')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.title(f'Audio Waveform and Sampling Rate: {sampling_rate} Hz')
    plt.grid(True)
    plt.legend()

    # Annotate the sampling rate
    plt.text(0.5, max(audio_data), f'Sampling Rate: {sampling_rate} Hz', 
             horizontalalignment='center', verticalalignment='top', fontsize=12, color='red')

    # Save the plot as an image file
    plot_filename = f"{username}_{filename}_waveform_with_sampling_rate.png"
    img_path = os.path.join(FEATURES_DIR, plot_filename)
    
    plt.savefig(img_path)
    plt.close()

    return img_path

def calculate_decibels_with_sampling_rate(file_path, sampling_rate, reference_pressure=20e-6):
    # Load audio file
    audio_data, _ = load_audio(file_path)
    
    # Calculate RMS
    rms = np.sqrt(np.mean(audio_data**2))
    
    # Calculate decibels using the RMS value and reference pressure
    decibels = 20 * np.log10(rms / reference_pressure)
    
    return decibels.tolist()

def get_loudness(file_path):
    y, sr = librosa.load(file_path)
    S = np.abs(librosa.stft(y))
    loudness = librosa.amplitude_to_db(S, ref=np.max)
    return loudness.tolist(), sr

def plot_loudness(file_path, filename, username):
    loudness, sr = get_loudness(file_path)

    plt.figure(figsize=(10, 6))
    plt.imshow(loudness, aspect='auto', origin='lower', cmap='viridis')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Loudness Heatmap')
    plt.xlabel('Time')
    plt.ylabel('Frequency (Hz)')
    plot_filename = f"{username}_{filename}_loudness_plot.png"
    output_path = os.path.join(FEATURES_DIR, plot_filename)
    
    plt.savefig(output_path)
    plt.close()
    return output_path

def plot_waveform_with_peak(file_path, filename, username):
    y, sr = librosa.load(file_path)
    t = np.arange(0, len(y)) / sr
    peak_value = np.max(np.abs(y))
    peak_index = np.argmax(np.abs(y))

    plt.figure(figsize=(10, 6))
    plt.plot(t, y, color='blue')
    plt.scatter(t[peak_index], y[peak_index], color='red', label=f'Peak Value: {peak_value:.2f}', zorder=5)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Audio Waveform with Peak Value')
    plt.legend()
    plt.grid(True)
    plot_filename = f"{username}_{filename}_waveform_with_peak.png"
    output_path = os.path.join(FEATURES_DIR, plot_filename)
    
    plt.savefig(output_path)
    plt.close()
    return output_path

def get_silence_speech_ratio(file_path, silence_thresh=-40):
    y, sr = librosa.load(file_path)
    intervals = librosa.effects.split(y, top_db=-silence_thresh)
    total_duration = librosa.get_duration(y=y, sr=sr)
    speech_duration = np.sum(np.diff(intervals, axis=1)) / sr
    silence_duration = total_duration - speech_duration
    ratio = silence_duration / speech_duration
    return ratio, speech_duration, silence_duration

def plot_silence_speech_ratio_pie(file_path, filename, username):
    ratio, speech_duration, silence_duration = get_silence_speech_ratio(file_path)

    total_duration = speech_duration + silence_duration
    speech_percentage = (speech_duration / total_duration) * 100
    silence_percentage = (silence_duration / total_duration) * 100

    labels = ['Speech', 'Silence']
    sizes = [speech_duration, silence_duration]
    colors = ['skyblue', 'lightgray']
    explode = (0.1, 0)
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Speech and Silence Duration')
    plot_filename = f"{username}_{filename}_silence_speech_ratio.png"
    output_path = os.path.join(FEATURES_DIR, plot_filename)
    
    plt.savefig(output_path)
    plt.close()
    return output_path

def calculate_file_size(file_path):
    if os.path.exists(file_path):
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)
        return file_size_mb
    else:
        return None

def get_harmonicity(file_path):
    y, sr = librosa.load(file_path)
    y_harm, y_perc = librosa.effects.hpss(y)
    harmonicity = librosa.feature.rms(y=y_harm)
    return harmonicity[0]

def plot_harmonicity(file_path, filename, username):
    harmonicity = get_harmonicity(file_path)
    
    plt.figure(figsize=(10, 6))
    plt.plot(harmonicity)
    plt.title('Harmonicity')
    plt.xlabel('Frame')
    plt.ylabel('RMS Energy')
    plt.grid(True)
    plot_filename = f"{username}_{filename}_harmonicity.png"
    output_path = os.path.join(FEATURES_DIR, plot_filename)
    
    plt.savefig(output_path)
    plt.close()
    return output_path

def plot_frequency_spectrum(file_path, filename, username):
    y, sr = librosa.load(file_path)
    D = librosa.stft(y)
    magnitude = np.abs(D)
    magnitude_db = librosa.amplitude_to_db(magnitude, ref=np.max)

    plt.figure(figsize=(10, 6))
    librosa.display.specshow(magnitude_db, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Frequency Spectrum')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plot_filename = f"{username}_{filename}_plot_path_sr.png"
    output_path = os.path.join(FEATURES_DIR, plot_filename)
    
    plt.savefig(output_path)
    plt.close()
    return output_path

def estimate_tempo(audio_file):
    y, sr = librosa.load(audio_file)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return tempo.tolist()
