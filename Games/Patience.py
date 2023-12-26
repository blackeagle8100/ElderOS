#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 23:50:18 2023

@author: meme
"""

import subprocess
import tkinter as tk
import time
import tkinter.font as tkfont
import pyautogui

subprocess.Popen(["sol"])
time.sleep(0.3)
root = tk.Tk()
global processid 
global windowid

time.sleep(0.3)
pyautogui.hotkey('winleft', 'up')


print('getting process id')
window_name = 'Klondike'
cmd = ['xdotool', 'search', '--name', window_name]
windowid = subprocess.run(cmd, capture_output=True, text=True)
window_ids = windowid.stdout.strip().split('\n')
if window_ids:
    windowid = window_ids[0]
else:
    print('Process not active')
print("windowid: ", windowid)

cmd = ['xprop', '-id', windowid, '_NET_WM_PID']
processid = subprocess.run(cmd, capture_output=True, text=True)
output = processid.stdout.strip().split(' = ')

if output:
        processid = output[1]
else:
       print('Process not active')
print("Process id: ", processid)


# Use xdotool to activate the window
subprocess.run(['xdotool', 'windowactivate', windowid])


def close():
    root.destroy()
    subprocess.run(['kill', str(processid)])
    
def Newgame():
    print('nieuw spel')
    pyautogui.hotkey('ctrl', 'n')
    
    
screen_width = root.winfo_screenwidth()
# Set the width of the window to the screen width
root.geometry(f"{screen_width}x60")
root.title("Patience")
root.attributes("-topmost", True)  # Set the window to stay on top of other windows
button_height = 30
button_font_size = 36
button_font = tkfont.Font(family="Arial Black", size=button_font_size)

 #Remove the window frame and borders
root.overrideredirect(True)

btnnew = tk.Button(root, text="Nieuw spel", command=Newgame, font=button_font )
btnnew.config(height=button_height)
btnnew.pack(side=tk.LEFT) # Set the button width to the maximum available width


btnclose = tk.Button(root, text="Sluiten", command=close, font=button_font )
btnclose.config(height=button_height)
btnclose.pack(side=tk.LEFT) 








    



# Start the Tkinter event loop
root.mainloop()
