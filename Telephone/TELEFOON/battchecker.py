#!/usr/bin/env python3

import subprocess
import time
import pygame
import os
import threading
import configparser
config = configparser.ConfigParser()

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")
config.read(vastsysteem_path + '/settings.ini')
# Initialize pygame and the mixer for audio
pygame.init()
pygame.mixer.init()

ip = config.get('Settings', 'smartip')
port = "5555"
battcommand = f"adb -s {ip} shell dumpsys battery"


AIaudio_path = os.path.join(user_home, "VASTSYSTEEM/Telephone/TELEFOON/")
sound_path = os.path.join(AIaudio_path, "opladen.wav")

battdata = subprocess.run(battcommand, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
output = battdata.stdout.strip()
print(output)
lines = output.split("\n")
decharge = False
for line in lines:
    if "USB" in line:
        charging = line.split(":")[1].strip()
        print("Charge status: " + str(charging))
        if charging == "true":
            decharge = False
        else:
            decharge = True
print("decharge status: "+ str(decharge))
while True:
    while decharge:
            battdata = subprocess.run(battcommand, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
            output = battdata.stdout.strip()
            print(output)
            lines = output.split("\n")
            for line in lines:
                if "level:" in line:
                    procent = line.split(":")[1].strip()
                    procent = int(procent)
                    print("Battery level: " + str(procent))
            if procent >= 90:
                print("Battery level over 90%.")
                time.sleep(3600)
            elif 80 <= procent < 90:
                print("Battery level is high (80-90%).")
                print("Wait 1 hour for next measurement")
                time.sleep(3600)
            elif 50 <= procent < 80:
                print("Battery level is medium (50-79%).")
                print("Wait half hour for next measurement")
                time.sleep(1800)
            elif 15 <= procent < 50:
                print("Battery level is low (20-49%).")
                print("Wait quarter hour for next measurement")
                time.sleep(900)
            else:
                print("Battery level is very low (below 20%).")
                if decharge:
                    while decharge:
                        pygame.mixer.music.load(sound_path)
                        pygame.mixer.music.play()
                        for i in range(60):
                            time.sleep(1)
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                    print("Hello from the enter side")
                        battdata = subprocess.run(battcommand, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
                        output = battdata.stdout.strip()
                        if "USB powered:" in output:
                            charging = output.split(":")[1].strip()
                            if charging == "false":
                                decharge = True
                            else:
                                decharge = False
                    
    while not decharge:
            print("I'm charging")
            battdata = subprocess.run(battcommand, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
            output = battdata.stdout.strip()
            lines = output.split("\n")
            for line in lines:
                if "USB powered:" in line:
                    charging = line.split(":")[1].strip()
                    if charging == "true":
                        print("Charging")
                        decharge = False
                    else:
                        decharge = True
                        break
                elif "level:" in line:
                    procent = line.split(":")[1].strip()
                    procent = int(procent)
                    print("Battery level: " + str(procent) + ", charging.")
            
                    if procent == 99 and charging == "true":
                        print("Fully charged")
                        fullcharged_sound_path = os.path.join(AIaudio_path, "fullcharged.wav")
                        pygame.mixer.music.load(fullcharged_sound_path)
                        pygame.mixer.music.play()
                        
                    if charging == "false":
                        print("Decharging again")
                        decharge = True
                    time.sleep(300)
        
