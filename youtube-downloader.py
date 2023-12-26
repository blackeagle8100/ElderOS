import sys
import os
import urllib.request
import requests
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pytube import YouTube
from moviepy.editor import AudioFileClip

app = QApplication(sys.argv)
webview = QWebEngineView()

def on_load_finished(ok):
    if ok:
        # Get the current URL of the webview
        url = webview.page().url().toString()

        # Check if the URL is a valid YouTube video URL
        if "youtube.com/watch?" in url:
            try:
                # Extract the YouTube video ID
                video_id = url.split("?v=")[1]

                # Create a YouTube object and get the audio streams
                youtube = YouTube(f"https://www.youtube.com/watch?v={video_id}")
                audio_streams = youtube.streams.filter(only_audio=True).all()
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                response = requests.get(url, headers=headers)
                # Find the highest quality audio stream
                highest_quality_stream = None
                for stream in audio_streams:
                    print(stream)
                    
                    if highest_quality_stream is None or stream.abr > highest_quality_stream.abr:
                        highest_quality_stream = stream

                if highest_quality_stream is not None:
                    # Set the download path to /home/meme/Muziek
                    download_path = "/home/meme/Muziek"

                   
                    directory = '/home/meme/Muziek/CDHOES'
                    if not os.path.exists(directory):
                        
                            # Create the directory if it doesn't exist
                            os.makedirs(directory)
                    # Get the video title
                    video_title = youtube.title

                    # Download the audio stream
                    audio_filename = f"{video_title}.mp4"
                    audio_path = os.path.join(download_path, audio_filename)
                    highest_quality_stream.download(output_path=download_path, filename=audio_filename)

                    # Convert the audio to MP3 format
                    mp3_filename = f"{video_title}.mp3"
                    mp3_path = os.path.join(download_path, mp3_filename)
                    audio_clip = AudioFileClip(audio_path)
                    audio_clip.write_audiofile(mp3_path)
                    audio_clip.close()

                    # Remove the original audio file
                    os.remove(audio_path)
                    
                    # Download the thumbnail
                    thumbnail_url = youtube.thumbnail_url
                    thumbnail_file = os.path.join(download_path, "CDHOES", video_title + ".jpg")
                    urllib.request.urlretrieve(thumbnail_url, thumbnail_file)

                    print("Download complete!")
                else:
                    print("No suitable audio stream found.")
            except Exception as e:
                print("Error:", str(e))
        else:
            print("Invalid YouTube video URL.")

        # Quit the application
        app.quit()

# Retrieve the URL from the command-line argument
if len(sys.argv) > 1:
    url = sys.argv[1]

    # Set up the webview and load the YouTube page
    webview.load(QUrl(url))
    webview.loadFinished.connect(on_load_finished)

    # Execute the application
    sys.exit(app.exec_())
else:
    print("Please provide a YouTube video URL as a command-line argument.")
