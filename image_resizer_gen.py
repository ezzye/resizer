# python image_resizer_gen.py "image.jpg" 50
# python image_resizer_gen.py "image.jpg" -30

import argparse
from PIL import Image
import os


def resize_image(img_path, scale_percent):
    # Load the image from the given file path
    img = Image.open(img_path)

    # Handle different image modes
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Calculate the new dimensions
    new_width = int(img.size[0] * (1 + scale_percent / 100))
    new_height = int(img.size[1] * (1 + scale_percent / 100))

    # Resize the image
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Prepare the file path for the resized image
    file_root, file_ext = os.path.splitext(img_path)
    resized_img_path = f"{file_root}_resized{file_ext}"

    # Save the resized image in the same format as the original
    img_resized.save(resized_img_path)

    # Return the path of the resized image
    return resized_img_path


def main():
    parser = argparse.ArgumentParser(description="Resize an image by a specified percentage")
    parser.add_argument('image_path', type=str, help="Path to the image file to resize")
    parser.add_argument('scale_percent', type=float, help="Percentage to scale the image (positive or negative)")
    args = parser.parse_args()

    resized_image_path = resize_image(args.image_path, args.scale_percent)
    print("Resized image saved to:", resized_image_path)


if __name__ == "__main__":
    main()
