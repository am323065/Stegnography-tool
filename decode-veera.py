from PIL import Image
import os

# Must be identical to encode.py
END_MARKER = "#####"


def load_image(image_path):
    """
    Load the encoded image and convert it to RGB.

    Args:
        image_path (str): Path to encoded image.

    Returns:
        Image: Pillow Image object.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    try:
        image = Image.open(image_path)

        if image.mode != "RGB":
            image = image.convert("RGB")

        # print("Image loaded successfully!")
        # print(f"Image Size : {image.size}")
        # print(f"Image Mode : {image.mode}")

        return image

    except Exception as e:
        raise Exception(f"Unable to load image.\n{e}")


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

    raise ValueError(
        "No hidden message found or image is corrupted."
    )


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


def main():

    # Load Encoded Image
    image_path = "output/encoded_image.png"

    try:

        image = load_image(image_path)

        # print("\nExtracting hidden message...")

        secret_message = decode_message(image)

        print("\n====================================")
        print(" Hidden Message Recovered ")
        print("====================================\n")
        print(secret_message)
        print("\n====================================")

    except Exception as error:

        print("\nERROR")
        print(f"❌ {error}")


if __name__ == "__main__":
    main()