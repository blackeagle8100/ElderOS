#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 02:54:30 2023
"""

import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import pyautogui
import subprocess
import os
root = tk.Tk()

# Create FirefoxOptions object



firefox_options = Options()

firefox_options.profile = webdriver.FirefoxProfile()

firefox_options.set_preference("permissions.default.microphone", 1)
firefox_options.set_preference("permissions.default.camera", 1)
firefox_options.set_preference("privacy.webrtc.legacyGlobalIndicator", False)
# Set the path to your GeckoDriver executable
geckodriver_path = "/home/meme/VASTSYSTEEM/geckodriver"
# Create the Service object
service = Service(executable_path=geckodriver_path)
# Create the WebDriver instance with the Service object and FirefoxOptions
driver = webdriver.Firefox(service=service, options=firefox_options)
driver.set_window_size(1920, 1080) 
# Navigate to Facebook
driver.get('https://www.facebook.com')
# Perform login
username_input = driver.find_element(By.ID, 'email')
password_input = driver.find_element(By.ID, 'pass')
login_button = driver.find_element(By.NAME, 'login')
button_text = "Alle cookies toestaan"
button_element = driver.find_element(By.XPATH, f"//button[contains(text(), '{button_text}')]")
button_element.click()
username_input.send_keys('georgette.vandewaetere@gmail.com')
password_input.send_keys('Groenestraat#13')
login_button.click()
driver.minimize_window()
knopstatus = 0
root.withdraw()

def set_focus_on_firefox(window_title):
    try:
        # Use xdotool to activate the Firefox window by title
        subprocess.run(["xdotool", "search", "--name", window_title, "windowactivate"])
    except Exception as e:
        print("Error setting focus on Firefox window:", str(e))

def close_button_click():
    # Switch to the new window (which is the second window)
    driver.switch_to.window(driver.window_handles[1])
    # Close the window if the title matches
    driver.close()
    #time.sleep(0.3)
    root.withdraw()

# Create the close button GUI


close_button = tk.Button(root, text="Sluiten", command=close_button_click, width=1920, height=100)
close_button.pack()
root.attributes("-topmost", True)
root.geometry("1920x100")  # Set the window to stay on top
root.overrideredirect(True)

call_notification = None  # Define the variable outside the loop

while True:
    print('Awaiting call')

    try:
        call_notification = driver.find_element(By.CSS_SELECTOR, 'div.x5ib6vp:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)')
        
        if call_notification.is_displayed():
            print('You have a call!')
            try:
                subprocess.call('pkill' , 'mjpg_streamer')
            except Exception as e:
                print(e)
                print('cant kill the process. probably cause its not running anymore')
            call_notification.click()
            time.sleep(2)
            
            window_title = "Messenger-oproep"
            set_focus_on_firefox(window_title)
            driver.switch_to.window(driver.window_handles[1])
            driver.set_window_size(1920, 1080)
            print(driver.title)
            
            root.deiconify()
            
            # Maximize the call window
            print('gestopt')
    except Exception:
        print("knop niet gevonden")
    
    root.update()  # Update the tkinter window
    time.sleep(5)  # Wait for 5 seconds before checking again

root.mainloop()
