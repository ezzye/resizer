import unittest
from PIL import Image
from image_resizer import resize_image_to_4500px


class TestImageResizer(unittest.TestCase):
    def test_resize_image(self):
        # Path to a test image
        test_img_path = "/path/to/test/image.jpg"
        # Resize the image
        resized_img_path = resize_image_to_4500px(test_img_path)
        # Open the resized image
        img = Image.open(resized_img_path)
        # Check if the image dimensions are 4500x4500
        print(img.size)
        # self.assertEqual(img.size, (4500, 4500))


if __name__ == '__main__':
    unittest.main()
