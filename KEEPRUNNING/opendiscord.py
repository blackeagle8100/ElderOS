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

    # Wait for Discord to start
    time.sleep(10)

    # Check if Discord is started
    while not checkstate:
        if is_window_running(window_class):
            # Use xdotool to bring the most recently used Discord window to the front
            #next command lets the person auto join the room
            subprocess.run(["xdotool", "keydown", "Control","keydown","Shift","key","L","keyup","Control","keyup","Shift"])
            
            # Additional delay to ensure the window is fully activated
            time.sleep(1)
            subprocess.run(['wmctrl','-a','MAIN'])
            checkstate = True
        else:
            # Discord window not found, wait and try again
            checkstate = False
            time.sleep(10)

if __name__ == "__main__":
    bring_discord_to_front()
