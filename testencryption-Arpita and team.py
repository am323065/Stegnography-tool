"""
Test Script

"""

from encryption import encrypt_message, decrypt_message


def main():

    message = input("\nEnter the secret message: ")

    password = input("Enter password (Leave blank for no encryption): ")

    # Encrypt
    encrypted = encrypt_message(message, password)

    print("\nEncrypted Message:")
    print(encrypted)

    # Password for decryption
    decrypt_password = input("\nEnter password to decrypt: ")

    try:
        decrypted = decrypt_message(encrypted, decrypt_password)

        print("\nDecrypted Message:")
        print(decrypted)

        if decrypted == message:
            print("\nEncryption and Decryption Successful!")

    except ValueError as e:
        print(f"\n {e}")


if __name__ == "__main__":
    main()