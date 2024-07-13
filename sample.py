import tkinter as tk
import csv
import json
import numpy as np
import threading
import tensorflow as tf
import tensorflow_hub as hub
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

# Function to read the first entry from the CSV and return its pitch data
def read_first_entry(csv_file):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            return row['File Name'], json.loads(row['All Pitches (Hz)'])

# Normalize pitch values to the range 0-1
def normalize_pitches(pitches):
    min_pitch = 1
    max_pitch = 800
    return [(pitch - min_pitch) / (max_pitch - min_pitch) for pitch in pitches]

# GUI Application for the Piano Tiles Game
class PianoTilesGame(tk.Tk):
    def __init__(self, csv_file):
        super().__init__()
        self.title("Piano Tiles Game")
        self.geometry("800x600")
        self.csv_file = csv_file

        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.tile_width = 50
        self.tile_height = 20

        self.load_data()
        self.create_tiles()

        self.marker_y = 580
        self.marker_height = 20
        self.create_marker()

        self.speed = 5
        self.update_game()

        self.audio_thread = threading.Thread(target=self.capture_audio)
        self.audio_thread.daemon = True
        self.audio_thread.start()

    def load_data(self):
        self.file_name, self.pitch_values = read_first_entry(self.csv_file)
        self.normalized_pitches = normalize_pitches(self.pitch_values)
        self.times = np.arange(len(self.pitch_values))

    def create_tiles(self):
        self.tiles = []
        for i, pitch in enumerate(self.normalized_pitches):
            x = int(pitch * (800 - self.tile_width))  # Normalize pitch to canvas width (800) minus tile width
            y = -i * self.tile_height  # Stack the tiles vertically
            tile = self.canvas.create_rectangle(x, y, x + self.tile_width, y + self.tile_height, fill="white")
            self.tiles.append(tile)

    def create_marker(self):
        marker_width = 5  # Adjust width of the marker as needed
        marker_position = int((800 - marker_width) / 2)  # Center of the canvas
        self.marker = self.canvas.create_rectangle(marker_position, self.marker_y, marker_position + marker_width, self.marker_y + self.marker_height, fill="red")


    def update_game(self):
        for tile in self.tiles:
            self.canvas.move(tile, 0, self.speed)
            coords = self.canvas.coords(tile)
            if coords[3] >= 600:
                self.canvas.move(tile, 0, -600)

        self.after(50, self.update_game)

    def update_marker(self, pitch_value):
        if not self.normalized_pitches:
            return  # If there are no normalized pitches, return without updating marker
        if pitch_value == 0 : 
            marker_position = int((800 - 5) / 2)
        else : 
            normalized_pitch = (pitch_value - 1) / (800 - 1)
            
            marker_position = int(normalized_pitch * (800 - self.tile_width))
            print(marker_position)
        self.canvas.coords(self.marker, marker_position, self.marker_y, marker_position + self.tile_width, self.marker_y + self.marker_height)

    def capture_audio(self):
        def callback(indata, frames, time, status):
            if status:
                print(status)
            audio_data = np.array(indata[:, 0], dtype=np.float32)
            pitch_values = process_audio_samples(audio_data)
            if pitch_values:                
                average_pitch = np.mean(pitch_values)
                # print(f"Pitch = {average_pitch:.2f} Hz")
                self.update_marker(average_pitch)
            # else:
            #     # self.update_marker(0)
            #     # print("No confident pitch detected")

        # Open audio stream
        samplerate = 44100  # Sample rate for the audio
        blocksize = 2048    # Size of each audio block (in samples)

        with sd.InputStream(callback=callback, channels=1, samplerate=samplerate, blocksize=blocksize):
            print("Listening... Press Ctrl+C to stop.")
            sd.sleep(-1)  # Keep the stream open

# Path to your CSV file
csv_file = 'csv\pitch_recognition_results.csv'

# Create and run the GUI application
app = PianoTilesGame(csv_file)
app.mainloop()
