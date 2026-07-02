"""
Module 2 - LSB Decoding
Steganography Tool

Author: Veera
Project: Steganography Tool

Purpose:
Extract a hidden message from a stego PNG/BMP image using
Least Significant Bit (LSB) decoding.
"""

from PIL import Image

# Must be identical to encode.py
END_MARKER = "#####"


def extract_binary_data(image):
    """
    Extract all Least Significant Bits (LSBs)
    from every RGB channel.

    Args:
        image (Image): Encoded image.

    Returns:
        str: Binary data extracted from image.
    """

    width, height = image.size
    pixels = image.load()

    binary_data = []

    for y in range(height):
        for x in range(width):

            r, g, b = pixels[x, y]

            binary_data.append(str(r & 1))
            binary_data.append(str(g & 1))
            binary_data.append(str(b & 1))

    return "".join(binary_data)


def binary_to_text(binary_data):
    """
    Convert binary string into readable text.

    Stops immediately once END_MARKER is found.

    Args:
        binary_data (str)

    Returns:
        str
    """

    message = []

    for i in range(0, len(binary_data), 8):

        byte = binary_data[i:i + 8]

        if len(byte) < 8:
            break

        character = chr(int(byte, 2))
        message.append(character)

        decoded = "".join(message)

        if decoded.endswith(END_MARKER):
            return decoded[:-len(END_MARKER)]

    return ""


def decode_message(image):
    """
    Complete decoding pipeline.

    Args:
        image (Image)

    Returns:
        str
    """

    binary_data = extract_binary_data(image)

    secret_message = binary_to_text(binary_data)

    return secret_message
