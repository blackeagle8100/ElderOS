#!/usr/bin/env python3

import subprocess
import tkinter as tk
import time
import tkinter.font as tkfont
import os


user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

subprocess.Popen([vastsysteem_path+"/UsefullPrograms/blinkenfull.sh"])
time.sleep(0.3)
root = tk.Tk()

def close():
    subprocess.run(['pkill', "blinken"])
    exit()
     
screen_width = root.winfo_screenwidth()
# Set the width of the window to the screen width
root.geometry(f"{screen_width}x60")
root.title("Blinken")
root.attributes("-topmost", True)  # Set the window to stay on top of other windows
button_height = 30
button_font_size = 36
button_font = tkfont.Font(family="Arial Black", size=button_font_size)

 #Remove the window frame and borders
root.overrideredirect(True)

btnclose = tk.Button(root, text="Sluiten", command=close, font=button_font )
btnclose.config(height=button_height)
btnclose.pack(side=tk.LEFT) 

# Start the Tkinter event loop
root.mainloop()
