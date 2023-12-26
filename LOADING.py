import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import configparser
import sys
import os

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

config = configparser.ConfigParser()

config.read('settings.ini')
colorcode = config.get('Settings', 'colorcode')

def animate_gif(label, frame_index, gif_frames):
    frame = gif_frames[frame_index]
    image = ImageTk.PhotoImage(frame)
    label.configure(image=image)
    label.image = image
    
    frame_index += 1
    if frame_index >= len(gif_frames):
        frame_index = 0

    # Call the animate_gif function again after a delay (in milliseconds)
    label.after(100, animate_gif, label, frame_index, gif_frames)

def main(duration):
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("GIF Image Viewer")
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", 1)  # Set the window to always on top
    root.configure(bg=colorcode)

    # Load the GIF image using PIL (Pillow)
    gif_path = vastsysteem_path + "/icons/loading.gif"  # Replace with the correct path to your GIF file
    gif_image = Image.open(gif_path)

    # Split the GIF into individual frames
    gif_frames = [frame.copy() for frame in ImageSequence.Iterator(gif_image)]

    # Create a label to display the GIF image
    label = tk.Label(root, bg=colorcode)
    label.pack()
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Start animating the GIF
    animate_gif(label, 0, gif_frames)

    # Create a label for the text "Even geduld aub"
    text_label = tk.Label(root, text="Even geduld aub", bg=colorcode, font=("Helvetica", 16))
    text_label.pack()
    text_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    # Start the main event loop
    root.after(duration * 1000, root.destroy)  # Close the window after the specified duration (in seconds)
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 LOADING.py <duration_in_seconds>")
        sys.exit(1)

    duration = int(sys.argv[1])
    main(duration)
