import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file if it exists
load_dotenv()

# Set your API key
os.environ['GROQ_API_KEY'] = "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"
groq_api_key = os.getenv('GROQ_API_KEY')

# Initialize the Groq client
client = Groq()

def perform_transcription(filename, username, audio_file_path):
    # Ensure the transcription directory exists
    transcription_dir = os.path.join("uploads", "transcription")
    if not os.path.exists(transcription_dir):
        os.makedirs(transcription_dir)

    # Initialize paths for saving results
    trans_filename = f"{username}_{filename}_transcription_result.txt"
    output_file = os.path.join(transcription_dir, trans_filename)

    try:
        # Read the audio file
        with open(audio_file_path, "rb") as audio_file:
            # Use the Groq API for audio transcription
            transcription_response = client.audio.transcriptions.create(
                file=(filename, audio_file.read()),
                model="whisper-large-v3",  # or your preferred model
                response_format="verbose_json"
            )
        
        # Access the transcribed text correctly
        transcribed_text = transcription_response.text  # Update this based on the actual API response structure
        
        # Save only the transcribed text to the file
        with open(output_file, "w") as f:
            f.write(transcribed_text)

        print(f"Transcription successfully saved to {output_file}")
        
        return output_file  # Return the file path of the transcription output
        
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

# Example usage
# perform_transcription("sample.wav", "user1", r"C:\Users\InfoBay\Desktop\backend-APIs\backend\test_audio.mp3")
