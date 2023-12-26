# dencrypt.py
import os
import sys
import base64
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import configparser

sleutel = configparser.ConfigParser()

sleutel.read('/home/meme/VASTSYSTEEM/encryptiesleutel.ini')
key = sleutel.get('Settings', 'sleutel')
encryption_key_bytes = key.encode('utf-8')



def pad_message(message):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message) + padder.finalize()
    return padded_data

def unpad_message(padded_message):
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_message) + unpadder.finalize()
    return data

def encrypt(plaintext, key):
    backend = default_backend()
      
    iv = os.urandom(16)  # Use a random 16-byte IV for CFB mode
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)  # Use CFB mode
    encryptor = cipher.encryptor()
    padded_message = pad_message(plaintext.encode())
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()  # Include IV in the output and decode to string

def decrypt(ciphertext, key):
    backend = default_backend()
    decoded_ciphertext = base64.b64decode(ciphertext)
    iv = decoded_ciphertext[:16]  # Extract the first 16 bytes as the IV
    ciphertext = decoded_ciphertext[16:]  # The remaining part is the actual ciphertext
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)  # Use CFB mode
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(ciphertext) + decryptor.finalize()
    return unpad_message(padded_message).decode()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 dencrypt.py [encrypt/decrypt] [text]")
        sys.exit(1)

    action = sys.argv[1]
    text = sys.argv[2]

    
    

    if action == "encrypt":
        result = encrypt(text, encryption_key_bytes)
        print(result)
    elif action == "decrypt":
        result = decrypt(text, encryption_key_bytes)
        print(result)
    else:
        print("Invalid action. Use 'encrypt' or 'decrypt'.")
        sys.exit(1)
