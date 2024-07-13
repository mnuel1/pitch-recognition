import librosa
import numpy as np

# Load audio file
file_path = 'downloads/Harana by Parokya Ni Edgar  Acoustic Guitar Karaoke  Singalong  Instrumental  No Vocals.mp3'
y, sr = librosa.load(file_path, sr=44100, mono=True)

# Extract chroma feature
chromagram = librosa.feature.chroma_stft(y=y, sr=sr)

# Find the most prominent pitch class for each frame
chroma_max = np.argmax(chromagram, axis=0)

# Map pitch class index to note names
note_names = librosa.core.note_to_midi(['C',    'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])

# Print the detected notes
detected_notes = [librosa.midi_to_note(note_names[idx]) for idx in chroma_max]
print(detected_notes)
