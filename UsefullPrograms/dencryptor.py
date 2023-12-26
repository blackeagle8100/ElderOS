

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 13:27:21 2023

@author: meme
"""



# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 14:15:25 2023

@author: lemmy
"""
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import configparser
import pyautogui
import base64
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
# Create a ConfigParser object


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
    iv = os.urandom(16)  # Use a random 16-byte IV for CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)  # Change CBC to CFB
    encryptor = cipher.encryptor()
    padded_message = pad_message(plaintext.encode())
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()  # Include IV in the output and decode to string


def decrypt(ciphertext, key):
    backend = default_backend()
    decoded_ciphertext = base64.b64decode(ciphertext)
    iv = decoded_ciphertext[:16]  # Extract the first 16 bytes as the IV
    ciphertext = decoded_ciphertext[16:]  # The remaining part is the actual ciphertext
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)  # Change CBC to CFB
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(ciphertext) + decryptor.finalize()
    return unpad_message(padded_message).decode()    




sleutel = configparser.ConfigParser()

sleutel.read('../encryptiesleutelhard.ini')

key = sleutel.get('Settings', 'sleutel')
encryption_key_bytes = key.encode('utf-8')

print(key)
text = ('georgette.vandewaetere@gmail.com')

print('normale text: ', text)
crypt= encrypt(text, encryption_key_bytes)
print('Encrypted:        ', crypt)
txtdecrypt = decrypt(crypt, encryption_key_bytes)
print('Decrypted:    ', txtdecrypt)





     


     