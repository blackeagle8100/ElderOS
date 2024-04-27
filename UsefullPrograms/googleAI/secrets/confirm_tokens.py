#!/usr/bin/env python3

import time
import pyautogui

# Function to confirm tokens in the browser
def confirm_tokens():
    # Example: Assuming tokens are confirmed by clicking a button with coordinates (x, y)
    # Wait for the browser to open and load
    time.sleep(6)
    # Click the button to confirm tokens
    pyautogui.click(912, 553) #select account 
    time.sleep(2)
    pyautogui.click(789, 635)  #select doorgaan
    time.sleep(2) 
    pyautogui.click(1070, 927) #select accepteren
    time.sleep(2)
    pyautogui.click(1903, 54) #sluit browser
    time.sleep(5)
    
if __name__ == "__main__":
    confirm_tokens()