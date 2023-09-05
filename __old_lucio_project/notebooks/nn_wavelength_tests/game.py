import sounddevice as sd
import numpy as np
import sys
import json
from sklearn.decomposition import PCA
from scipy.signal import lfilter
import librosa


def compress_array(arr, output_size):
    original_size = len(arr)
    subarray_size = original_size // output_size

    # Reshape the array into sub-arrays
    reshaped_arr = arr[:subarray_size * output_size].reshape((output_size, subarray_size))

    # Compute the mean along the second axis (axis=1)
    compressed_arr = np.mean(reshaped_arr, axis=1)

    return (compressed_arr - np.mean(compressed_arr)) / np.std(compressed_arr)

def record_audio(duration, sample_rate):
	print("RECORDING STARTED")
	frames = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
	sd.wait()
	print("RECORDING ENDED")
	return frames.flatten()

def compute_mfcc(wave, sample_rate):
	# audio = np.asarray(wave * 32767, dtype=np.int16)
	mfccs = librosa.feature.mfcc(y=wave, sr=sample_rate, n_mfcc=13)
	mfccs = (mfccs - np.mean(mfccs)) / np.std(mfccs)
	return mfccs.flatten()
	# mfcc_coefficient = mfccs[mfcc_index, frame_index]


# Example usage:
duration = 2  # Duration in seconds
sample_rate =  44100# Sample rate in Hz

audio_data = record_audio(duration, sample_rate)

compressed_array = compute_mfcc(audio_data, sample_rate)
print(compressed_array.shape)

cmd = sys.argv[1]
with open(f"./{cmd}.csv", "a") as f:
	f.write(f"{json.dumps(compressed_array.tolist())}\n")
# Create an instance of PCA with the desired number of components
