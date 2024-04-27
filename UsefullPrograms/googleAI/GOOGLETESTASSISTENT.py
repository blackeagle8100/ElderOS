#!/usr/bin/env python3

import sys
import subprocess
import pygame
import time
import os


user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

pygame.init()



def main(input):
    sound_path = (vastsysteem_path+"/UsefullPrograms/SOUNDS/AIsounds/ok.wav")
    pygame.mixer.music.load(sound_path)
    print("nu run ik zeker")
    if "firefox" in input:
        print("open firefox")  
        subprocess.Popen(["firefox"])
        pygame.mixer.music.play()
        time.sleep(2)

    

    elif "waar_is_lisa" in input:
        print("open chatgpt")
        subprocess.Popen(['firefox', 'https://chat.openai.com/'])
        pygame.mixer.music.play()
        time.sleep(2)

#APP CONTROLLS ITSELF
    elif "muziek" in input:
        print('open de muziekspeler')
        weg = "/home/sbe/VASTSYSTEEM/MediaPlayer/Mediaplayer.py"
        subprocess.Popen(['python3',weg ])
        pygame.mixer.music.play()
        time.sleep(2)

    elif "weer" in input:
        print("open de weer app")
        weg = "/home/sbe/VASTSYSTEEM/WEER/weer.py"
        subprocess.Popen(['python3',weg ])
        pygame.mixer.music.play()
        time.sleep(2)

    elif "facebook" in input:
        print("open facebook")
        subprocess.Popen(["python3","/home/sbe/VASTSYSTEEM/Internet/Facebook.py"])
        pygame.mixer.music.play()
        time.sleep(2)

    elif "telefoon" in input or ("messenger" in input):
        print("open telefoon app")
        weg = "/home/sbe/VASTSYSTEEM/Telephone/telephone.py"
        subprocess.Popen(['python3',weg ])
        pygame.mixer.music.play()
        time.sleep(2)

    elif ("games" in input) or ("spell" in input):
        print("open de games")
        weg = "/home/sbe/VASTSYSTEEM/GamesMenu.py"
        subprocess.Popen(['python3',weg ])
        pygame.mixer.music.play()
        time.sleep(2)
    
    elif ("tv" in input) or ("visie" in input) or ("radio" in input):
        print("open de TV app")
        weg = "/home/sbe/VASTSYSTEEM/TV/TV.py"
        subprocess.Popen(['python3',weg ])
        pygame.mixer.music.play()
        time.sleep(2)

    elif "youtube" in input:
        weg = "/home/sbe/VASTSYSTEEM/Internet/Youtube.py"
        subprocess.Popen(['python3',weg ])
        pygame.mixer.music.play()
        time.sleep(2)
    elif ("foto" in input) or ("galer" in input):
        weg = "/home/sbe/VASTSYSTEEM/Gallery/gallery.py"
        subprocess.Popen(['python3',weg ])
        pygame.mixer.music.play()
        time.sleep(2)
    elif ("instellingen" in input) or ("settings" in input):
        weg = "/home/sbe/VASTSYSTEEM/FULLSETTINGS.py"
        subprocess.Popen(['python3',weg ])
        pygame.mixer.music.play()
        time.sleep(2)
    elif ("internet" in input):
        weg = "/home/sbe/VASTSYSTEEM/InternetMenu.py"
        subprocess.Popen(['python3',weg ])
        pygame.mixer.music.play()
        time.sleep(2)
    else:
        sound_path = ("/home/sbe/VASTSYSTEEM/UsefullPrograms/SOUNDS/AIsounds/begrijphetniet.wav")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        time.sleep(2)
        sound_path = ("/home/sbe/VASTSYSTEEM/UsefullPrograms/SOUNDS/AIsounds/voorstelandereknop.wav")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()  
        time.sleep(4)
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 GOOGLETESTASSISTENT.py <variabel zonder spaties>")
        sys.exit(1)

    input = str(sys.argv[1])
    main(input)
