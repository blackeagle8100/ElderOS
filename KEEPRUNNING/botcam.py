#!/usr/bin/env python3


import subprocess
import time
import pyautogui

def is_window_running(window_class):
    try:
        # Use xdotool to search for the window class
        subprocess.check_output(['xdotool', 'search', '--class', window_class])
        return True
    except subprocess.CalledProcessError:
        return False

def bring_discord_to_front():
    # Replace 'discord' with the actual class of the Discord window
    window_class = 'discord'
    checkstate = False



    # Check if Discord is started
    while not checkstate:
        if is_window_running(window_class):
            # Use xdotool to bring the most recently used Discord window to the front
            subprocess.run(['xdotool', 'search', '--class', window_class, 'windowactivate', '%@'])
            print("Activate discord")

            # Additional delay to ensure the window is fully activated
            time.sleep(1)

            pyautogui.click(100, 1000)
            print("Click camera")
            
            # Additional delay to ensure the window is fully activated
            time.sleep(1)
            
            # Click the reconnect button
            #pyautogui.click(1150, 50)
            #print("Click reconnect")
            
            # Additional delay to ensure the window is fully activated
            #time.sleep(1)

            # Click the camera button
            #pyautogui.click(100, 1000)
            #print("Click camera")
            
            # Additional delay to ensure the window is fully activated
            #time.sleep(1)
            subprocess.run(['wmctrl','-a','MAIN'])
            checkstate = True
        else:
            # Discord window not found, wait and try again
            checkstate = False
            time.sleep(2)

if __name__ == "__main__":
    bring_discord_to_front()
