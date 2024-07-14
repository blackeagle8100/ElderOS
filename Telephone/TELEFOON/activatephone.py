#!/usr/bin/env python3

import time
import subprocess
import os
import configparser
import pygame
config = configparser.ConfigParser()
pygame.init()
pygame.mixer.init()
user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")
AIaudio_path = os.path.join(user_home, "VASTSYSTEEM/Telephone/TELEFOON/")
sound_path = os.path.join(AIaudio_path, "aansluiten.wav")
config.read(vastsysteem_path + '/settings.ini')
device_ip = config.get('Settings', 'smartip')

#DEFINITIES
def adb_device(ip):
     output = subprocess.check_output(['adb', 'devices'], universal_newlines=True)
     print(output)
     if device_ip in output:
        if "offline" not in output:
             
            print("ADB is running")
            return True
        else:
             print("adb is running but not online... needs to restart")
             subprocess.run(["adb", "disconnect"])
             return False
     else:
          return False
#MAIN
adb_result  = adb_device(device_ip)
if adb_result == False:
        print("Kijk om adb opnieuw op te starten aub")
        output = subprocess.check_output(['adb', 'connect', device_ip], universal_newlines=True)
        print(output)
        if "failed" in output:
            print("kan adb niet starten omdat deze moet geactiveerd worden via usb...")
            print("vraag om watch aan te sluiten...") 
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            #commando nodig om te kijken of watch aangesloten is... ADB devices?
            concheck = False
            while concheck != True:
                output = subprocess.check_output(['adb', 'devices'], universal_newlines=True)
                split = output.split("\n")
                if "device" in split[1]:
                     print("watch aangesloten!")
                     concheck = True
                else:
                    print("Sluit watch aan")
                    concheck = False
                time.sleep(1)
            time.sleep(20)
            subprocess.run(["adb", "tcpip", "5555"])
            time.sleep(1)
            subprocess.run(["adb", "connect", device_ip])
            time.sleep(1)
        subprocess.Popen(["python3",user_home +"/VASTSYSTEEM/Telephone/TELEFOON/serialreader.py"])
        subprocess.Popen(["python3",user_home +"/VASTSYSTEEM/Telephone/TELEFOON/battchecker.py"])
        subprocess.Popen(["python3",user_home +"/VASTSYSTEEM/Telephone/TELEFOON/watcher.py"])
else:           
     print("alles ok ")
     subprocess.Popen(["python3",user_home +"/VASTSYSTEEM/Telephone/TELEFOON/serialreader.py"])
     subprocess.Popen(["python3",user_home +"/VASTSYSTEEM/Telephone/TELEFOON/battchecker.py"])
     subprocess.Popen(["python3",user_home +"/VASTSYSTEEM/Telephone/TELEFOON/watcher.py"])
