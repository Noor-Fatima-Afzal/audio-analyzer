import whisper
import os
from pyannote.audio import Pipeline
import torchaudio
import torch
from matplotlib import cm
import matplotlib.pyplot as plt

# Preprocess audio without trimming or padding, keeping the same save path
def preprocess_audio(input_audio_path):
    # Load the audio file using torchaudio
    waveform, sample_rate = torchaudio.load(input_audio_path)

    # Save the preprocessed audio for further use without trimming or padding
    preprocessed_audio_path = input_audio_path.replace(".mp3", "_preprocessed.wav")
    torchaudio.save(preprocessed_audio_path, waveform, sample_rate)

    return preprocessed_audio_path

# Main function for speaker diarization with no trimming or padding
def perform_speaker_diarization(filename, username, input_audio_path):
    # Ensure the diarization directory exists
    diarization_dir = os.path.join("uploads", "diarization")
    if not os.path.exists(diarization_dir):
        os.makedirs(diarization_dir)

    # Initialize paths for saving results
    dia_filename = f"{username}_{filename}_diarization_result.txt"
    output_file = os.path.join(diarization_dir, dia_filename)
    dia_graph = f"{username}_{filename}_diarization_graph.png"
    graph_output = os.path.join(diarization_dir, dia_graph)

    try:
        # Step 1: Preprocess audio without trimming or padding
        print(f"Preprocessing audio: {input_audio_path}")
        preprocessed_audio_path = preprocess_audio(input_audio_path)

        # Step 2: Perform transcription
        print(f"Performing transcription on: {preprocessed_audio_path}")
        model = whisper.load_model("base")
        result = model.transcribe(preprocessed_audio_path)
        transcription_text, transcription_segments = result['text'], result['segments']

        # Step 3: Perform diarization
        print(f"Performing diarization on: {preprocessed_audio_path}")
        auth_token = os.getenv('AUTH_TOKEN')
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=auth_token)
        diarization = pipeline(preprocessed_audio_path)

        # Step 4: Process diarization and transcription results
        speaker_segments = []
        speakers = set()
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speaker_segments.append((turn.start, turn.end, speaker))
            speakers.add(speaker)

        # Create a color map for the speakers
        colors = cm.get_cmap('tab10', len(speakers))
        speaker_colors = {speaker: colors(i) for i, speaker in enumerate(speakers)}

        # Match transcription segments to speaker segments
        speaker_transcriptions = []
        for segment in transcription_segments:
            start, end, text = segment['start'], segment['end'], segment['text']
            matching_speaker = "SPEAKER_00"
            for (s_start, s_end, speaker) in speaker_segments:
                if max(start, s_start) < min(end, s_end):
                    matching_speaker = speaker
                    break
            speaker_transcriptions.append((matching_speaker, start, end, text))

        # Step 5: Save the combined diarization and transcription results to a file
        print(f"Saving speaker-wise transcription to: {output_file}")
        with open(output_file, "w") as f:
            for speaker, start, end, text in speaker_transcriptions:
                f.write(f"Speaker {speaker} from {start:.1f}s to {end:.1f}s: {text}\n")

        # Step 6: Plot and save the diarization timeline graph
        print(f"Saving diarization timeline graph to: {graph_output}")
        plt.figure(figsize=(10, 3))
        plotted_speakers = set()
        for segment in speaker_segments:
            start, end, speaker = segment
            plt.plot([start, end], [1, 1], color=speaker_colors[speaker], linewidth=10, label=speaker if speaker not in plotted_speakers else "")
            plt.text((start + end) / 2, 1.5, str(speaker), horizontalalignment='center', fontsize=10)
            plotted_speakers.add(speaker)

        plt.yticks([])
        plt.title("Speaker Diarization Timeline")
        plt.xlabel("Time (seconds)")
        plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1))
        plt.savefig(graph_output)
        plt.close()

        print(f"Speaker-wise transcription saved to {output_file}")
        return output_file, graph_output

    except Exception as e:
        print(f"Error during speaker diarization: {e}")
        return None, None
