from mido import MidiFile, MidiTrack, Message

# Function to add a chord to a track
def add_chord(track, chord, time, duration):
    for note in chord:
        track.append(Message('note_on', note=note, velocity=64, time=time))
    for note in chord:
        track.append(Message('note_off', note=note, velocity=64, time=duration))

# Define the chords with their MIDI note values
chords = {
    'G': [55, 59, 62],
    'G7': [55, 59, 62, 65],
    'C': [48, 52, 55],
    'Bm7': [47, 50, 54, 57],
    'E7sus': [52, 57, 59, 62],
    'E7': [52, 56, 59, 62],
    'Am7': [45, 48, 52, 55],
    'Dsus': [50, 57, 62],
    'D7': [50, 54, 57, 60],
    'D7sus': [50, 54, 57, 59],  # Define D7sus separately
    'D': [50, 54, 57],
    'Cm7': [48, 51, 55, 58]
}

# Create a new MIDI file and track
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Add chords to the track
time = 0  # Start time for the first chord
duration = 50  # Duration for each chord (in ticks)
progression = [
    'G', 'C', 'Bm7', 'E7sus', 'E7',
    'Am7', 'Bm7', 'Am7', 'Dsus', 'D7',
    'G', 'C', 'Bm7', 'E7sus', 'E7', 'Am7',
    'Bm7', 'Am7', 'D7sus', 'D7',
    'G', 'C', 'Bm7', 'E7sus', 'E7',
    'Am7', 'Bm7', 'Am7', 'Dsus', 'D7',
    'G', 'C', 'Bm7', 'E7sus', 'E7', 'Am7',
    'Bm7', 'Am7', 'D7sus', 'D7',
    'Cm7', 'Bm7', 'Am7', 'D',
    'G', 'G7', 'Cm7', 'Bm7',
    'Am7', 'D', 'E7sus', 'E7',
    'Am7', 'Dsus', 'D7', 'G'
]

for chord_name in progression:
    chord = chords[chord_name]
    add_chord(track, chord, time, duration)
    time += duration

# Save the MIDI file
mid.save('guitar_progression.mid')
