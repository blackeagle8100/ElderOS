#!/usr/bin/env python3

from pydub import AudioSegment
import os


#Maak een nieuwe audiofile met googlesamples-assistant-pushtotalk -o /home/sbe/Downloads/testaudio.test
# te runnen vanaf /Downloads/assistant-sdk-python/google-assistant-sdk/googlesamples/assistant/grpc/pushtotalk.py
#

 
# Specify the folder containing the wav files
folder_path = "/home/sbe/VASTSYSTEEM/UsefullPrograms/SOUNDS/"

# List all files in the specified folder
files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

# Iterate over each file
for file_name in files:
    # Create the full path to the file
    file_path = os.path.join(folder_path, file_name)

    # Load the audio file
    audio = AudioSegment.from_file(file_path, format="wav")

    # Set the end time to 1.3 seconds (1300 milliseconds)
    end_time = 1300

    # Cut the audio file
    cut_audio = audio[end_time:]

    # Export the cut audio to a new file
    cut_audio.export(folder_path+ "AIsounds/" + f"{file_name}", format="wav")
    os.remove(file_path)
