# python folder_video_splitter.py <input_folder> <segment_duration> <output_dir>

import os
import argparse
from moviepy.editor import VideoFileClip


def split_video(video_path, segment_duration, output_dir):
    # Load the video clip
    video = VideoFileClip(video_path)

    # Calculate the number of segments
    num_segments = int(video.duration // segment_duration) + 1

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Split the video into segments
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = min((i + 1) * segment_duration, video.duration)

        # Create a new video clip for the segment
        segment = video.subclip(start_time, end_time)

        # Create a folder for the segment
        segment_folder = os.path.join(output_dir, f"segment_{i + 1}")
        os.makedirs(segment_folder, exist_ok=True)

        # Write the segment to a file
        output_path = os.path.join(segment_folder, f"segment_{i + 1}.mp4")
        segment.write_videofile(output_path)

    # Close the video clip
    video.close()


def process_folder(input_folder, segment_duration, output_dir):
    # Iterate through the files in the input folder
    for filename in os.listdir(input_folder):
        # Check if the file is a video (assuming MP4 format)
        if filename.endswith(".mp4"):
            video_path = os.path.join(input_folder, filename)

            # Create a folder for the video segments
            video_output_dir = os.path.join(output_dir, os.path.splitext(filename)[0])

            # Split the video into segments
            split_video(video_path, segment_duration, video_output_dir)


if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Split videos in a folder into segments.")
    parser.add_argument("input_folder", help="Path to the input folder containing video files.")
    parser.add_argument("segment_duration", type=float, help="Duration of each segment in seconds.")
    parser.add_argument("output_dir", help="Path to the output directory.")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the process_folder function with the provided arguments
    process_folder(args.input_folder, args.segment_duration, args.output_dir)
