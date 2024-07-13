import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import sounddevice as sd
import logging

# Set up logging
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

def process_audio_samples(audio_samples):
    audio_samples = audio_samples / float(np.iinfo(np.int16).max)
    
    model_output = model.signatures["serving_default"](tf.constant(audio_samples, tf.float32))
    pitch_outputs = model_output["pitch"]
    confidence_outputs = 1.0 - model_output["uncertainty"]
    
    confident_pitch_outputs = [
        output2hz(float(p)) for p, c in zip(pitch_outputs, confidence_outputs) if c >= 0.9
    ]
    
    return confident_pitch_outputs

def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_data = np.array(indata[:, 0], dtype=np.float32)
    pitch_values = process_audio_samples(audio_data)
    if pitch_values:
        average_pitch = np.mean(pitch_values)
        print(f"Average Pitch = {average_pitch:.2f} Hz")
    else:
        print("No confident pitch detected")

# Open audio stream
samplerate = 44100  # Sample rate for the audio
blocksize = 2048   # Size of each audio block (in samples)

with sd.InputStream(callback=callback, channels=1, samplerate=samplerate, blocksize=blocksize):
    print("Listening... Press Ctrl+C to stop.")
    sd.sleep(-1)  # Keep the stream open
