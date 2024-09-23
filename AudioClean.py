import numpy as np
import librosa
import librosa.display
from pydub import AudioSegment
from scipy.io.wavfile import write
import os
from spleeter.separator import Separator

def remove_noise(input_audio_path, output_audio_path, noise_reduction_level=0.1):
    """
    Remove background noise from audio.
    Args:
        input_audio_path (str): Path to the input audio file.
        output_audio_path (str): Path to save the noise-reduced audio file.
        noise_reduction_level (float): The amount of noise reduction (0 to 1).
    """
    # Load the audio file
    audio_data, sample_rate = librosa.load(input_audio_path, sr=None)
    
    # Perform noise reduction using spectral gating
    reduced_noise = librosa.effects.reduce_noise(y=audio_data, sr=sample_rate, prop_decrease=noise_reduction_level)
    
    # Save the noise-reduced audio file
    write(output_audio_path, sample_rate, (reduced_noise * 32767).astype(np.int16))
    print(f"Noise-reduced audio saved at {output_audio_path}")


def separate_vocals(input_audio_path, output_directory):
    """
    Separate vocals and instruments from audio.
    Args:
        input_audio_path (str): Path to the input audio file.
        output_directory (str): Path to save the separated audio files.
    """
    # Initialize Spleeter separator (2 stems: vocals and accompaniment)
    separator = Separator('spleeter:2stems')
    
    # Perform separation
    separator.separate_to_file(input_audio_path, output_directory)
    print(f"Separated vocals and instruments saved in {output_directory}")


if __name__ == "__main__":
    # Example usage
    input_audio = "your_audio_file.wav"
    
    # Remove background noise
    remove_noise(input_audio, "noise_reduced_audio.wav")

    # Separate vocals and instruments
    #separate_vocals(input_audio, "output_separated")
