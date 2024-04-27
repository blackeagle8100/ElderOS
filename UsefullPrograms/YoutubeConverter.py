#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
import pytube
import moviepy
from moviepy.editor import AudioFileClip


def download_audio(url, folder):
    try:
        # Create a YouTube object with the provided URL
        youtube = pytube.YouTube(url)

        # Get the highest quality audio stream available
        audio_stream = youtube.streams.get_audio_only()

        # Set the download folder
        audio_file = audio_stream.download(output_path=folder)

        # Convert the audio file to MP3
        mp3_file = audio_file.replace(".mp4", ".mp3")
        audio = AudioFileClip(audio_file)
        audio.write_audiofile(mp3_file)

        result_label.configure(text="Audio downloaded and converted to MP3 successfully!")

    except Exception as e:
        result_label.configure(text=f"An error occurred: {str(e)}")

def download_video(url, folder):
    try:
        # Create a YouTube object with the provided URL
        youtube = pytube.YouTube(url)

        # Get the highest resolution stream available
        video_stream = youtube.streams.get_highest_resolution()

        # Set the download folder
        video_stream.download(output_path=folder)

        result_label.configure(text="Video downloaded successfully!")

    except Exception as e:
        result_label.configure(text=f"An error occurred: {str(e)}")

def select_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def download_button_clicked():
    video_url = url_entry.get()
    download_folder = folder_entry.get()

    if video_url and download_folder:
        if choice_var.get() == 1:
            download_audio(video_url, download_folder)
        else:
            download_video(video_url, download_folder)
    else:
        result_label.configure(text="Please provide a video URL and download folder path.")

# Create the main window
window = tk.Tk()
window.title("YouTube Downloader")

# Create and pack the URL label and entry
url_label = tk.Label(window, text="YouTube URL:")
url_label.pack()
url_entry = tk.Entry(window, width=50)
url_entry.pack()

# Create and pack the folder label, entry, and select button
folder_label = tk.Label(window, text="Download Folder:")
folder_label.pack()
folder_entry = tk.Entry(window, width=50)
folder_entry.pack(side=tk.LEFT)
select_button = tk.Button(window, text="Select Folder", command=select_folder)
select_button.pack(side=tk.LEFT)

# Create the radio buttons for audio and video choice
choice_var = tk.IntVar()
audio_radio = tk.Radiobutton(window, text="Audio", variable=choice_var, value=1)
audio_radio.pack()
video_radio = tk.Radiobutton(window, text="Video", variable=choice_var, value=2)
video_radio.pack()

# Create and pack the download button
download_button = tk.Button(window, text="Download", command=download_button_clicked)
download_button.pack()

# Create and pack the result label
result_label = tk.Label(window, text="")
result_label.pack()

# Start the main window's event loop
window.mainloop()
