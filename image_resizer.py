# python image_resizer.py "/Users/ellioe03/Downloads/alchemyrefiner_alchemymagic_0_cdc896ae-ace1-4b45-8496-276920d4c6a5_0.jpg"


import argparse
from PIL import Image


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


def main():
    parser = argparse.ArgumentParser(description="Resize an image to be at least 4500x4500 pixels")
    parser.add_argument('image_path', type=str, help="Path to the image file to resize")
    args = parser.parse_args()

    resized_image_path = resize_image_to_4500px(args.image_path)
    print("Resized image saved to:", resized_image_path)


if __name__ == "__main__":
    main()
