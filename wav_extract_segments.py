# python extract_segments.py wav_my_music.wav 0:30,1:45 2:00,3:30

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


def time_to_frames(time_str, framerate):
    """Convert time in 'minutes:seconds' format to frames."""
    minutes, seconds = map(int, time_str.split(':'))
    return (minutes * 60 + seconds) * framerate


def extract_segment(input_file, output_file, start_time, end_time, params):
    """Extract a segment from the input file."""
    n_channels, sampwidth, framerate, _, comptype, compname = params
    start_frame = time_to_frames(start_time, framerate)
    end_frame = time_to_frames(end_time, framerate)


    with wave.open(input_file, 'rb') as wav_file:
        wav_file.setpos(start_frame)
        frames = wav_file.readframes(end_frame - start_frame)

    with wave.open(output_file, 'wb') as output:
        output.setnchannels(n_channels)
        output.setsampwidth(sampwidth)
        output.setframerate(framerate)
        output.setcomptype(comptype, compname)
        output.writeframes(frames)

    print(f'Segment written to {output_file}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract segments from a WAV file.')
    parser.add_argument('input_file', type=str, help='Path to the input WAV file')
    parser.add_argument('segments', type=str, nargs='+',
                        help='Segments to extract in the format start_min:start_sec,end_min:end_sec')

    args = parser.parse_args()

    # Read parameters from the input file
    with wave.open(args.input_file, 'rb') as wav_file:
        params = wav_file.getparams()

    for i, segment in enumerate(args.segments):
        start_time, end_time = segment.split(',')
        start = start_time.replace(':', '_')
        end = end_time.replace(':', '_')

        filename = get_filename_without_extension(args.input_file)
        # Set file name for the segment
        output_file = f'{filename}-extract_{start}__{end}.wav'
        output_file = get_output_path(filename, output_file)

        extract_segment(args.input_file, output_file, start_time, end_time, params)
