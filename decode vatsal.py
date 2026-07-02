"""
Module 2 - LSB Decoding

Author: Vatsal Goel
Project: Steganography Tool

Purpose:
Extract a hidden message from a stego PNG/BMP image using
Least Significant Bit (LSB) decoding.
"""

from PIL import Image


END_MARKER = "#####END#####"


def load_image(image_path):
    """
    Opens the image and converts it to RGB.
    """

    try:
        image = Image.open(image_path)

        # Convert image to RGB if needed
        if image.mode != "RGB":
            image = image.convert("RGB")

        return image

    except FileNotFoundError:
        raise FileNotFoundError("Image file not found.")

    except Exception as e:
        raise Exception(f"Error opening image: {e}")


def extract_bits(image):
    """
    Extracts the Least Significant Bit (LSB) from every RGB channel
    and returns them as one long binary string.
    """

    bits = ""

    width, height = image.size

    for y in range(height):
        for x in range(width):

            r, g, b = image.getpixel((x, y))

            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

    return bits


def bits_to_text(bits):
    """
    Convert binary bits into readable text.
    """
    pass


def decode_message(image_path):
    """
    Main decoding function.
    """
    pass


if __name__ == "__main__":

    image = load_image("sample_images/test.png")

    bits = extract_bits(image)

    print(f"Total Bits: {len(bits)}")
    print(bits[:100])
   