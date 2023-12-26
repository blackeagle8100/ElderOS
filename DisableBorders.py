#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pyautogui
import win32api

# Define the width of the border in pixels
border_width = 10

# Get the screen resolution
screen_width, screen_height = pyautogui.size()

# Define the region where mouse clicks will be blocked (right side of the screen)
block_region = (screen_width - border_width, 0, screen_width, screen_height)

while True:
    x, y = win32api.GetCursorPos()
    
    # Check if the mouse cursor is within the blocked region
    if block_region[0] <= x <= block_region[2]:
        # Disable mouse click events by suppressing left mouse button clicks
        pyautogui.FAILSAFE = False  # Disable the failsafe feature
        pyautogui.mouseDown = lambda *args, **kwargs: None
        pyautogui.mouseUp = lambda *args, **kwargs: None
    else:
        # Restore the normal mouse click behavior
        pyautogui.FAILSAFE = True  # Re-enable the failsafe feature
        pyautogui.mouseDown = pyautogui._mouseDown
        pyautogui.mouseUp = pyautogui._mouseUp


