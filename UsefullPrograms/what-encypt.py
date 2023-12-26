#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 16:50:17 2023

@author: meme
"""

import subprocess
import configparser

config = configparser.ConfigParser()
config.read('/home/meme/VASTSYSTEEM/settings.ini')

global fbusername
fbusername = config.get('Settings', 'fblogin')
decrypt_process = subprocess.Popen(["python3", "/home/meme/VASTSYSTEEM/UsefullPrograms/dencrypt.py", "decrypt", fbusername], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
decrypt_output, decrypt_error = decrypt_process.communicate() 
decrypted_text = decrypt_output.decode().strip()
switch = decrypted_text
fbusername = switch

global fbww
fbww = config.get('Settings', 'fbww')
decrypt_process = subprocess.Popen(["python3", "/home/meme/VASTSYSTEEM/UsefullPrograms/dencrypt.py", "decrypt", fbww], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
decrypt_output, decrypt_error = decrypt_process.communicate() 
decrypted_text = decrypt_output.decode().strip()
switch = decrypted_text
fbww = switch

print(fbusername)
print(fbww)