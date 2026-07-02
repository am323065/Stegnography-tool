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
    Stops when END_MARKER is found.
    """

    message = ""

    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]

        if len(byte) < 8:
            break

        character = chr(int(byte, 2))
        message += character

        # Stop once the end marker is found
        if message.endswith(END_MARKER):
            return message[:-len(END_MARKER)]

    raise ValueError(
        "End marker not found. The image may not contain a valid hidden message."
    )

def decode_message(image_path):
    """
    Main decoding function.
    """

    image = load_image(image_path)

    bits = extract_bits(image)

    message = bits_to_text(bits)

    return message


if __name__ == "__main__":

    try:
        message = decode_message("sample_images/test.png")
        print("Recovered Message:")
        print(message)

    except Exception as e:
        print(f"Error: {e}")
