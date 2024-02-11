# python trim_wav_cli.py input.wav 17

import os
import argparse
from pydub import AudioSegment


def trim_wav(input_file, trim_seconds, channels, sample_rate, sample_width):
    # Load the WAV file
    audio = AudioSegment.from_wav(input_file)

    # Calculate the duration to trim
    trim_milliseconds = trim_seconds * 1000

    # Trim the audio by removing the last trim_milliseconds
    trimmed_audio = audio[:-trim_milliseconds]

    # Get the directory of the input file
    output_dir = os.path.dirname(input_file)

    # Get the filename without extension
    filename = os.path.splitext(os.path.basename(input_file))[0]

    # Construct the output file path
    output_file = os.path.join(output_dir, f"{filename}_trimmed.wav")

    # Export the trimmed audio to a new file with PCM format and matching parameters
    trimmed_audio.export(output_file, format="wav",
                         parameters=["-ac", channels, "-ar", sample_rate, "-sample_fmt", sample_width])

    return output_file


def get_wav_properties(input_file):
    # Load the WAV file
    audio = AudioSegment.from_wav(input_file)

    # Get properties of the WAV file
    channels = audio.channels
    sample_width = audio.sample_width
    frame_rate = audio.frame_rate

    return str(channels), sample_width, str(frame_rate)


if __name__ == "__main__":
    # Create the command-line parser
    parser = argparse.ArgumentParser(description="Trim silence from the end of a WAV file.")
    parser.add_argument("input_file", help="Path to the input WAV file.")
    parser.add_argument("trim_seconds", type=int, help="Number of seconds to trim from the end of the WAV file.")

    # Parse the command-line arguments
    args = parser.parse_args()

    channels, sample_width, frame_rate = get_wav_properties(args.input_file)

    # Convert the sample width to a string representation
    if sample_width == 1:
        sample_format = "u8"  # unsigned 8-bit integer
    elif sample_width == 2:
        sample_format = "s16"  # signed 16-bit integer
    elif sample_width == 3:
        sample_format = "s16"  # signed 24-bit integer
    elif sample_width == 4:
        sample_format = "s16"  # signed 32-bit integer
    else:
        raise ValueError("Unsupported sample width")

    print("Channels:", channels)
    print("sample_format:", sample_format)
    print("Frame Rate:", frame_rate)

    # Trim the WAV file
    trimmed_file = trim_wav(args.input_file, args.trim_seconds, channels, frame_rate, sample_format)

    print(f"Trimmed file saved as: {trimmed_file}")
