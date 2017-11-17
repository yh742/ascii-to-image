import os
import datetime
from PIL import Image, ImageDraw

ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image):
    return image.convert('L')

def map_pixels_to_ascii_chars(image, range_width=25):
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """

    pixels_in_image = list(image.getdata())
    pixels_to_chars = [ASCII_CHARS[int(pixel_value/range_width)] for pixel_value in
            pixels_in_image]

    return "".join(pixels_to_chars)


def convert_image_to_ascii(image, width=100):
    """Given an image, and a target width, we generate an ASCII string
    """
    image = scale_image(image, width)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + width] for index in
            range(0, len_pixels_to_chars, width)]

    # convert to dimensions from font
    # these are calculated from the base font used
    new_width = width * 6 
    new_height = len(image_ascii) * 15

    return new_width, new_height, "\n".join(image_ascii)


def convert_ascii_to_image(ascii, width, height):
    """Given a string, and a set of dimensions we create a new image
    """
    image = Image.new('RGB', (width, height), (0, 0, 0) )

    draw = ImageDraw.Draw(image)
    draw.text((0,0), ascii, fill=(255, 255, 255))

    path = os.path.join(os.path.dirname(__file__), 'processed/' + datetime.datetime.now().isoformat() + '.png')
    image.save(path, 'PNG')

    return path


def handle_image_conversion(image_filepath):
    """Function that handles the conversion and returns the path to the 
    processed file
    """
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print("Unable to open image file {image_filepath}.".format(image_filepath=image_filepath))
        print(e)
        return

    width, height, image_ascii = convert_image_to_ascii(image)
    processed_image_filepath = convert_ascii_to_image(image_ascii, width, height)
    
    return processed_image_filepath
