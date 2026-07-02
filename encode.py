"""
Module 1 - LSB Encoding
Steganography Tool

Author: Gauri
Project: Steganography Tool

Purpose:
Hide a secret text message inside a PNG/BMP image using
Least Significant Bit (LSB) encoding technique.
"""

from PIL import Image

# End marker to identify end of secret message
END_MARKER = "#####"


def load_image(image_path):
    image = Image.open(image_path)
    # Convert to RGB to ensure we have exactly 3 channels (R, G, B)
    image = image.convert("RGB")
    return image


def text_to_binary(message):
    message = message + END_MARKER
    binary = ""
    for character in message:
        binary += format(ord(character), "08b")
    return binary


def modify_pixel_value(value, bit):
    """
    Change only the Least Significant Bit (LSB)
    """
    if bit == "0":
        return value & ~1  # Clears the last bit (makes it even)
    else:
        return value | 1   # Sets the last bit (makes it odd)


def calculate_capacity(image):
    width, height = image.size
    total_pixels = width * height
    # Every pixel has R, G, B = 3 values
    capacity = total_pixels * 3
    return capacity


def encode_message(image, binary_message):
    """
    Hides the binary message into the image pixels using LSB.
    """
    width, height = image.size
    pixels = image.load()

    bit_index = 0
    total_bits = len(binary_message)

    # Loop through every pixel in the image
    for y in range(height):
        for x in range(width):
            if bit_index >= total_bits:
                break

            # Get current pixel colors (Red, Green, Blue)
            r, g, b = pixels[x, y]

            # Hide 1 bit in Red
            if bit_index < total_bits:
                r = modify_pixel_value(r, binary_message[bit_index])
                bit_index += 1

            # Hide 1 bit in Green
            if bit_index < total_bits:
                g = modify_pixel_value(g, binary_message[bit_index])
                bit_index += 1

            # Hide 1 bit in Blue
            if bit_index < total_bits:
                b = modify_pixel_value(b, binary_message[bit_index])
                bit_index += 1

            # Update the pixel with the new modified values
            pixels[x, y] = (r, g, b)

        if bit_index >= total_bits:
            break

    return image
