from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"


def get_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()

        with open(KEY_FILE, "wb") as file:
            file.write(key)

    with open(KEY_FILE, "rb") as file:
        return file.read()


def encrypt_file(input_path, output_path):
    key = get_key()
    cipher = Fernet(key)

    with open(input_path, "rb") as file:
        data = file.read()

    encrypted_data = cipher.encrypt(data)

    with open(output_path, "wb") as file:
        file.write(encrypted_data)


def decrypt_file(input_path):
    key = get_key()
    cipher = Fernet(key)

    with open(input_path, "rb") as file:
        encrypted_data = file.read()

    return cipher.decrypt(encrypted_data)