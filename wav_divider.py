# python wav_divider.py my_music.wav 8

import wave
import argparse
import os


def get_filename_without_extension(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]


def get_output_path(input_path, output_file_name):
    # Extract the directory from the input path
    directory = os.path.dirname(input_path)

    # If the input was a file name without a directory, `directory` will be empty
    if not directory:
        # In this case, just return the output file name
        return output_file_name
    else:
        # Otherwise, join the directory with the output file name
        return os.path.join(directory, output_file_name)


def split_wav(input_file, num_segments):
    with wave.open(input_file, 'rb') as wav_file:
        # Read parameters from the input file
        n_channels, sampwidth, framerate, n_frames, comptype, compname = wav_file.getparams()

        # Calculate duration of each segment
        segment_length = n_frames // num_segments

        filename = get_filename_without_extension(input_file)

        for i in range(num_segments):
            # Set file name for the segment
            output_file = f'{filename}-segment_{i + 1}.wav'
            output_file = get_output_path(input_file, output_file)

            with wave.open(output_file, 'wb') as output:
                output.setnchannels(n_channels)
                output.setsampwidth(sampwidth)
                output.setframerate(framerate)
                output.setcomptype(comptype, compname)

                # Start and end frames for the segment
                start = i * segment_length
                end = min(start + segment_length, n_frames)

                wav_file.setpos(start)
                frames = wav_file.readframes(end - start)
                output.writeframes(frames)

            print(f'Segment {i + 1} written to {output_file}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split a WAV file into smaller segments.')
    parser.add_argument('input_file', type=str, help='Path to the input WAV file')
    parser.add_argument('num_segments', type=int, help='Number of segments to split the file into')

    args = parser.parse_args()
    split_wav(args.input_file, args.num_segments)
