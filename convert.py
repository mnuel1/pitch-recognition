import os
from pydub import AudioSegment

# Specify the folders
audio_folder = './downloads'
converted_folder = './audiotest'

# Create converted_folder if it doesn't exist
os.makedirs(converted_folder, exist_ok=True)

EXPECTED_SAMPLE_RATE = 16000

def convert_audio_for_model(user_file, output_file):
    audio = AudioSegment.from_file(user_file)
    audio = audio.set_frame_rate(EXPECTED_SAMPLE_RATE).set_channels(1)
    audio.export(output_file, format="wav")
    return output_file

# Process each audio file in the folder
for filename in os.listdir(audio_folder):
    if filename.endswith(('.wav', '.mp3', '.ogg')):  # Add more audio formats if needed
        file_path = os.path.join(audio_folder, filename)
        converted_file_name = f"converted_{filename.rsplit('.', 1)[0]}.wav"
        converted_file_path = os.path.join(converted_folder, converted_file_name)
        
        try:
            convert_audio_for_model(file_path, converted_file_path)
            print(f"Converted {filename} to {converted_file_name}")
        except Exception as e:
            print(f"Error converting {filename}: {str(e)}")

print("All files converted.")