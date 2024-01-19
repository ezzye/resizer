# python script_name.py /path/to/directory

import os
import wave
from wav_divider import split_wav  # Assuming split_wav.py is in the same directory
import math


def get_wav_files(directory):
    """Get a list of WAV files in the specified directory."""
    return [file for file in os.listdir(directory) if file.endswith('.wav')]


def calculate_segments(file_path, target_duration=50):
    """Calculate the number of segments for a given WAV file."""
    with wave.open(file_path, 'rb') as wav_file:
        n_frames = wav_file.getnframes()
        framerate = wav_file.getframerate()
        duration = n_frames / float(framerate)
        print(f"Duration: {duration} seconds")
        print(f"Target duration: {target_duration} seconds")
        print(f"Number of segments: {math.ceil(duration / target_duration)}")
        return max(1, math.ceil(duration / target_duration))


def main(directory):
    wav_files = get_wav_files(directory)
    for wav_file in wav_files:
        file_path = os.path.join(directory, wav_file)
        num_segments = calculate_segments(file_path)
        print(f"Processing '{wav_file}' into {num_segments} segments...")
        split_wav(file_path, num_segments)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Split all WAV files in a directory into 50-second segments.')
    parser.add_argument('directory', type=str, help='Path to the directory containing WAV files')

    args = parser.parse_args()
    main(args.directory)
