#!/usr/bin/env python3
import psutil
import subprocess
import time
import os
import cv2


def check_usb_webcam():
    # Iterate through the available video devices
    for i in range(10):
        # Try to open the video capture for the device
        cap = cv2.VideoCapture(i)
        
        # Check if the video capture is successfully opened
        if cap.isOpened():
            print(f"USB webcam found at device {i}")
            
            # Release the video capture
            cap.release()
            return True
    
    # No USB webcam found
    print("No USB webcam found")
    return False

def check_process(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

def start_process(process_path):
    subprocess.Popen(process_path)

def run_command(command):
    subprocess.run(command, shell=True)
def check_window_title(window_title):
    command = f'xdotool search --name "{window_title}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return bool(result.stdout.strip())


def main():
    process_name = 'mjpg_streamer'  # Replace with the name of your process
    process_path = '/home/meme/VASTSYSTEEM/KEEPRUNNING/mjpg-streamer-master/mjpg-streamer-experimental'
    command1 = f'cd {process_path}'
    command2 = './mjpg_streamer -i "input_uvc.so -d /dev/video0" -o "output_http.so -p 8081 -w ./www"'
    
    
    while True:
        
        window_title = "Messenger-oproep"
        is_open = check_window_title(window_title)

        if is_open:
            print(f"The window with title '{window_title}' is open.")
            
        else:
            print(f"The window with title '{window_title}' is not open.")
            #subprocess.Popen(['python3' , 'CallChecker.py'])
        
        
        if not check_process(process_name):
            check = check_usb_webcam()
            print(check)
            if check == True:
                run_command(command1)
                os.chdir(process_path)
                run_command(command2)
                print("Process started.")
            else:
                print('Camera reeds in gebruik. Meme is nog aan het bellen waarschijnlijk.')
        else:
            print("Process is already running.")
            
        time.sleep(300)  # Sleep for 5 minutes (300 seconds)

if __name__ == '__main__':
    main()
