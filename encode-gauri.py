from PIL import Image
import os

# End marker to identify end of secret message
END_MARKER = "#####"

def load_image(image_path):
    image = Image.open(image_path)
    # Convert to RGB to ensure we have exactly 3 channels (R, G, B)
    image = image.convert("RGB")
    print("Image loaded successfully!")
    print("Image Size:", image.size)
    print("Image Mode:", image.mode)
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

def main():
    # 1. Load Image
    image_path = "sample_images/sample_image1.png"
    image = load_image(image_path)
    
    # 2. Get Secret Message
    secret_message = input("\nEnter your secret message: ")
    binary_message = text_to_binary(secret_message)
    print("\nTotal Bits to hide:", len(binary_message))
    
    # 3. Check Capacity
    capacity = calculate_capacity(image)
    print("\n========== IMAGE CAPACITY ==========")
    print("Image can store", capacity, "bits")
    
    if len(binary_message) > capacity:
        print("\n❌ ERROR: Message is too large for this image.")
        print("Please use a larger image or a shorter message.")
        return
    
    print("\n✅ SUCCESS: Image has enough space to hide the message.")
    
    # 4. Encode Message
    print("\nEncoding message into image...")
    encoded_image = encode_message(image, binary_message)
    
    # 5. Save Encoded Image
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir) # Creates the folder if it doesn't exist
        
    output_path = os.path.join(output_dir, "encoded_image.png")
    encoded_image.save(output_path)
    
    print(f"\n🎉 Encoding Complete!")
    print(f"✅ Encoded image saved at: {output_path}")
    print("You can now share this image. The message is secretly hidden inside it!")

if __name__ == "__main__":
    main()