# python image_resizer.py "/Users/ellioe03/Downloads/second_spotify"
# python image_resizer.py "/Users/errolelliott/IdeaProjects/resizer/soundcloud_images"


import argparse
from PIL import Image
import os


def resize_image_to_4500px(img_path):
    # Load the image from the given file path
    img = Image.open(img_path)

    # Check if the image is already at least 4500 x 4500 pixels
    if img.size[0] < 4500 or img.size[1] < 4500:
        # Calculate the scaling factor needed for the smallest dimension to be 4500 pixels
        scale_factor = max(4500 / img.size[0], 4500 / img.size[1])

        # Scale both dimensions accordingly to maintain aspect ratio
        new_size = (int(img.size[0] * scale_factor), int(img.size[1] * scale_factor))

        # Resize the image
        img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
    else:
        img_resized = img

    # Save the resized image
    resized_img_path = img_path.split('.')[0] + '_resized.jpg'
    img_resized.save(resized_img_path)

    # Return the path of the resized image
    return resized_img_path


def resize_images_in_directory(directory_path):
    # List all files in the given directory
    for filename in os.listdir(directory_path):
        # Construct full file path
        file_path = os.path.join(directory_path, filename)
        # Check if it's a file and has a JPEG or PNG extension
        if os.path.isfile(file_path) and file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Resizing {filename}...")
            resized_image_path = resize_image_to_4500px(file_path)
            print("Resized image saved to:", resized_image_path)


def main():
    parser = argparse.ArgumentParser(description="Resize all images in a directory to 4500x4500 pixels")
    parser.add_argument('directory_path', type=str, help="Path to the directory containing image files")
    args = parser.parse_args()

    resize_images_in_directory(args.directory_path)


if __name__ == "__main__":
    main()
