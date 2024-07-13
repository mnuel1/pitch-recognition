import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import os
import csv
import json
from scipy.io import wavfile

# Set up logging
import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

print("tensorflow:", tf.__version__)

# Load the SPICE model
model = hub.load("https://tfhub.dev/google/spice/2")

def output2hz(pitch_output):
    PT_OFFSET = 25.58
    PT_SLOPE = 63.07
    FMIN = 10.0
    BINS_PER_OCTAVE = 12.0
    cqt_bin = pitch_output * PT_SLOPE + PT_OFFSET
    return FMIN * 2.0 ** (1.0 * cqt_bin / BINS_PER_OCTAVE)

def process_audio_file(file_path):
    sample_rate, audio_samples = wavfile.read(file_path, 'rb')
    
    audio_samples = audio_samples / float(np.iinfo(np.int16).max)
    
    model_output = model.signatures["serving_default"](tf.constant(audio_samples, tf.float32))
    pitch_outputs = model_output["pitch"]
    confidence_outputs = 1.0 - model_output["uncertainty"]
    
    confident_pitch_outputs = [
        output2hz(float(p)) for p, c in zip(pitch_outputs, confidence_outputs) if c >= 0.9
    ]
    
    return confident_pitch_outputs

# Specify the folder containing converted audio files
converted_folder = './audiotest'

# Prepare CSV file
csv_file = './csv/pitch_recognition_results.csv'
with open(csv_file, 'a', newline='') as file:
    writer = csv.writer(file)
    # writer.writerow(['File Name', 'Average Pitch (Hz)', 'All Pitches (Hz)'])

    # Process each converted audio file in the folder
    for filename in os.listdir(converted_folder):        
            file_path = os.path.join(converted_folder, filename)            
            try:
                pitch_values = process_audio_file(file_path)
                if pitch_values:
                    average_pitch = np.mean(pitch_values)
                    writer.writerow([
                        filename, 
                        average_pitch, 
                        json.dumps(pitch_values)  # Store all pitch values as JSON string
                    ])
                    print(f"Processed {filename}: Average Pitch = {average_pitch:.2f} Hz")
                else:
                    print(f"Could not determine pitch for {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

print(f"Results saved to {csv_file}")