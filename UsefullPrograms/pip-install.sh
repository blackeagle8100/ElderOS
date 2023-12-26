#!/bin/bash
password="Alotbso12"
echo "Installing..."
echo "$password" | su -c "pip install --break-system-packages pytube pyautogui moviepy"
echo "Finished"
echo "Copying Cipher.py"
echo "$password" | su -c "cp cipher.py /usr/local/lib/python3.11/dist-packages/pytube"
echo "Finished Copying"

