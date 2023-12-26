import requests
import os

def download_video(url):
    # Maak een HTTP-verzoek naar de YouTube-API
    response = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={url}")

    # Controleer of het verzoek is geslaagd
    if response.status_code == 200:
        # Extraheer de video-inhoud uit de reactie
        data = response.json()
        video_content = data["items"][0]["contentDetails"]["videoDetails"]["url"]

        # Download de video-inhoud
        with open(os.path.basename(url) + ".mp4", "wb") as f:
            f.write(requests.get(video_content).content)

    else:
        print("Fout bij het downloaden van de video:", response.status_code)

# Voer de functie uit voor de gegeven URL
download_video("https://www.youtube.com/watch?v=smWb8dj1Jgs")
