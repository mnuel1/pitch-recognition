import numpy as np
import librosa

# Function to load and parse pitch array from text file
def load_pitch_array(file_path):
    with open(file_path, 'r') as file:
        # Read the content as a single string and strip whitespace
        content = file.read().strip()
        
        # Remove the leading '[' and trailing ']' and split by ','
        values_str = content[1:-1].split(',')
        
        # Convert the string values to float
        pitch_array = np.array([float(value.strip()) for value in values_str])
    
    return pitch_array

def normalize_pitch_array(pitch_array):
    min_pitch = np.min(pitch_array)
    max_pitch = np.max(pitch_array)
    return (pitch_array - min_pitch) / (max_pitch - min_pitch)

def calculate_mse(array1, array2):
    min_length = min(len(array1), len(array2))
    array1 = array1[:min_length]
    array2 = array2[:min_length]
    mse = np.mean((array1 - array2) ** 2)
    return mse

def calculate_dtw(array1, array2):
    dtw_distance, _ = librosa.sequence.dtw(array1, array2)
    return np.mean(dtw_distance)

# Load the pitch arrays
music_pitch_array = load_pitch_array('kungsyaman.txt')
user_pitch_array = load_pitch_array('mine.txt')

# Normalize the pitch arrays
music_pitch_array = normalize_pitch_array(music_pitch_array)
user_pitch_array = normalize_pitch_array(user_pitch_array)

# Calculate similarity
mse = calculate_mse(music_pitch_array, user_pitch_array)
dtw_distance = calculate_dtw(music_pitch_array, user_pitch_array)

print(f"Mean Squared Error: {mse}")
print(f"DTW Distance: {dtw_distance}")
