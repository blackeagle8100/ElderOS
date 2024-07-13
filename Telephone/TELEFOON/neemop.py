#!/usr/bin/env python3

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, 
                             QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton)
from PyQt6.QtCore import Qt, QTime, QTimer
from PyQt6.QtGui import QPixmap, QFont
from PIL.ImageQt import ImageQt
from PIL import Image
import subprocess
import os
import psutil
import time
import re
from pathlib import Path
import io
import requests
import configparser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError
import pygame
import configparser

pygame.init()
user_home = os.path.expanduser("~")
global vastsysteem_path
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

config = configparser.ConfigParser()
config.read(vastsysteem_path + '/settings.ini')

device_ip = config.get('Settings', 'smartip')


tokenpath = os.path.join(vastsysteem_path, "UsefullPrograms", "googleAI", "secrets" )
AIaudio_path = os.path.join(vastsysteem_path+"/Telephone/TELEFOON/ring.mp3")

config = configparser.ConfigParser()
config.read(vastsysteem_path + '/settings.ini')

global colorcode
colorcode = config.get('Settings', 'colorcode')
screen_width = int(config.get('Settings', 'screen_width'))
screen_height = int(config.get('Settings', 'screen_height'))
font_type = config.get('Settings', 'font_type')
font_size = int(config.get('Settings', 'font_size'))

bgcolor = ("background-color: " + config.get('Settings', 'colorcode') + ";")



bring = False



class MainWindow(QMainWindow):
    
    def __init__(self, telnr, credentials_path):

        telnr = str(telnr)
        self.credentials_path = Path(credentials_path)
        self.credentials = self.get_credentials()
        self.service = self.create_service()
        self.contacts = self.get_contacts()
        telnr = telnr.replace("/", "")   
        telnr = telnr.replace(" ", "")
        telnr = telnr.replace("+32","")
        if telnr[0] == "0":
            telnr = telnr[1:]
        print("Te controleren: ", telnr)
        print("Lijst: ", self.contacts)

        super().__init__()
        self.setWindowTitle("Opneemscherm")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(bgcolor)  # Set the background color
        self.setGeometry(0, 0, screen_width, screen_height)  # Set window size
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)



        #telnrlabel
        self.telnr_label = QLabel(f"U wordt gebeld: {sys.argv[1]}", self)
        self.telnr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.telnr_label.setFont(QFont(font_type, font_size))
        #groene neemop knop
        self.takecall_btn = QLabel("Pakt op", self)
        im = Image.open(vastsysteem_path+"/icons/neemop.png")
        newsize = (200,200)
        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.takecall_btn.setPixmap(pixmap)
        self.takecall_btn.setMouseTracking(True)
        self.takecall_btn.mousePressEvent = self.takecall
           
        #rode legtoe knop
        self.cancelcall_btn = QLabel("Leg toe")
        im = Image.open(vastsysteem_path+"/icons/legtoe.png")
        newsize = (200,200)
        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.cancelcall_btn.setPixmap(pixmap)
        self.cancelcall_btn.setMouseTracking(True)
        self.cancelcall_btn.mousePressEvent = self.cancelcall
        #gesprekstimer
        self.timerlabel = QLabel("Gespreksduur: Nog niet opgenomen")
        self.timerlabel.setFont(QFont(font_type, font_size))
        self.timerlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #naamlabel
        self.lblnaam =QLabel("")
        self.lblnaam.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblnaam.setFont(QFont(font_type, font_size))
        #image label
        self.lblimage =QLabel("")
        self.lblimage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblimage.setMouseTracking(True)
        self.lblimage.mousePressEvent = self.takecall
        #btn spacer
        self.spacing = QLabel("")
        self.spacing.setFixedWidth(screen_width -450)

        self.check_contact(telnr)
        

        # Layout 
        layout = QVBoxLayout()
        htop = QVBoxLayout()
        btn_layout = QHBoxLayout()

        htop.addWidget(self.telnr_label)
        htop.addWidget((self.timerlabel))

        mid = QVBoxLayout()
        mid.addWidget(self.lblnaam)
        mid.addWidget(self.lblimage)

        btn_layout.addWidget(self.takecall_btn)
        btn_layout.addWidget(self.spacing)
        btn_layout.addWidget(self.cancelcall_btn)


        htop.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        mid.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        

        layout.addLayout(htop)
        layout.addLayout(mid)
        layout.addLayout(btn_layout)

        self.central_widget.setLayout(layout)
        

        
        #serial monitor
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_serial_data)
        self.timer.start(100)  # Check for data every 100 milliseconds
        pygame.mixer.music.load(AIaudio_path)
        pygame.mixer.music.play()
        



 
    def check_contact(self, telnr):
        found_contact = None
        for contact in self.contacts:
            if contact[1] == telnr:
                found_contact = contact
                break

        if found_contact:
            name, phone, photo_url = found_contact
            print("Contact found:")
            print("Name:", name)
            self.lblnaam.setText(name)
            print("Phone number:", phone)
            if photo_url:
                print(photo_url)
                if photo_url:
                        photo_url = photo_url.replace("s100","s300")
                        print(photo_url)
                     # Download and display the image
                        response = requests.get(photo_url)
                        if response.status_code == 200:
                            image_data = response.content
                            
                            pixmap = QPixmap()
                            pixmap.loadFromData(image_data)
        
                            self.lblimage.setPixmap(pixmap)
                           
                            return
                        else:
                            print(f"Failed to download image for {name}")
                            return
                else:
                    print(f"No image URL available for {name}")
                    return
            else:
                print("No photo available")
        else:
            print("Contact not found for phone number:", telnr)

    def get_credentials(self):
        creds = None
        if self.credentials_path.exists():
            creds = Credentials.from_authorized_user_file(self.credentials_path)
        
        # Check if credentials are expired
        if creds and creds.expired:
            try:
                creds.refresh(Request())
            except RefreshError:
                flow = InstalledAppFlow.from_client_secrets_file(
                    tokenpath +'/client_secret.json',
                    ['https://www.googleapis.com/auth/contacts.readonly']
                )
                creds = flow.run_local_server(port=0)
            with open(self.credentials_path, 'w') as token:
                token.write(creds.to_json())
        
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                tokenpath +'/client_secret.json',
                ['https://www.googleapis.com/auth/contacts.readonly']
            )
            creds = flow.run_local_server(port=0)
            with open(self.credentials_path, 'w') as token:
                token.write(creds.to_json())
        
        return creds


    def create_service(self):
        return build('people', 'v1', credentials=self.credentials)

    def get_contacts(self):
        results = self.service.people().connections().list(
            resourceName='people/me',
            pageSize=10,
            personFields='names,phoneNumbers,photos').execute()
        connections = results.get('connections', [])
        contacts = []
        for person in connections:
            names = person.get('names', [])
            phoneNumbers = person.get('phoneNumbers', [])
            
            photos = person.get('photos', [])
            if names and phoneNumbers:
                name = names[0].get('displayName')
                phone = phoneNumbers[0].get('value')
                phone = phone.replace("/", "")   
                phone = phone.replace(" ", "")
                phone = phone.replace("+32","")
                if phone[0] == "0":
                    phone = phone[1:]
                print(phone)
                
                if photos:
                    photo_url = photos[0].get('url')
                    contacts.append((name, phone, photo_url))
                else:
                    contacts.append((name, phone, None))
     
        return contacts




        
    def check_serial_data(self):
        global bring
        if bring == False:
            callstate = subprocess.Popen(["adb","-s",device_ip, "shell", "dumpsys", "telephony.registry", "|", "grep", "mCallState"], stdout=subprocess.PIPE,universal_newlines=True)
            for line in callstate.stdout:
                print(line)
            # Handle the received data as needed,
            # e.g., update a label in your GUI or trigger other actions
                if "2" in line:
                   print("gesprek gestart. wacht op het gesprek om te stoppen")
                   pygame.mixer.music.stop()
                 
                elif "0" in line:
                    print("gesprek gestopt")
                    self.timer.stop()
                    self.timerlabel.setText("Gesprek gestopt.")
                    self.timerlabel.hide()
                    self.telnr_label.setText("GEMISTE OPROEP")
                    pygame.mixer.music.stop()
                    self.takecall_btn.mousePressEvent = self.redail
                    

                
                
              
        elif bring == True:
            self.timer.stop()
            print("Bring is waar; nieuwe calls kunnen ontvangen worden")
     
            time.sleep(0.5)
            
            if not self.check_process_running("serialreader.py"):
                subprocess.Popen(["python3", os.path.join(vastsysteem_path + "/Telephone/TELEFOON/serialreader.py")])
            else:
                print("serialreader.py is already running")
    def sluitaf(self, event= None):
        print("Sluit dit venster af")
        sys.exit()

    def redail(self, event=None):
       #cancelBTN back to cancelcall
        self.cancelcall_btn.mousePressEvent = self.cancelcall
        self.startklok()
        
        print("herbel het nummer", sys.argv[1])
        number = str(sys.argv[1])
       
        callback="adb -s "+ device_ip+ " shell am start -a android.intent.action.CALL -d tel:"+number
        subprocess.Popen([callback], shell=True)
        self.telnr_label.setText(number)
        self.timer_value = QTime(0, 0)
        self.timerlabel.show()

    def takecall(self, event=None):
        print("Taking the call...")
        subprocess.run(["adb", "-s", device_ip, "shell","input","keyevent","KEYCODE_CALL"])
        self.startklok()
    
    def startklok(self):
        # Create and start the timer
        self.klok = QTimer(self)
        self.klok.timeout.connect(self.update_timer)
        self.klok.start(1000)  # Update timer every 1 second
        # Initialize the timer value
        self.timer_value = QTime(0, 0)
        self.update_timer()
    
    def update_timer(self):
        # Update the timer value and display it on the label
        self.timer_value = self.timer_value.addSecs(1)
        waarde = self.timer_value.toString("mm:ss")
        self.timerlabel.setText("Aan het bellen. \nDuur van het gesprek: \n"+ waarde)
 
    def cancelcall(self, event=None):
        global port
        #herstart de serial communicatie
        #ser = serial.Serial(port, 9600, timeout=1)
        print("Call denied.")
        subprocess.run(["adb", "-s", device_ip, "shell", "input", "keyevent", "KEYCODE_ENDCALL"])
      
        # Check if serialreader.py is already running
        if not self.check_process_running("serialreader.py"):
            subprocess.Popen(["python3", os.path.join(vastsysteem_path + "/Telephone/TELEFOON/serialreader.py")])
        else:
            print("serialreader.py is already running")
        # End the current script
        print("Close neemop.py")
        sys.exit()

    def check_process_running(self, process_name):
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == process_name:
                return True
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 script.py [telephone number]")
        sys.exit(1)
    credentials_path = vastsysteem_path +'/UsefullPrograms/googleAI/secrets/multitoken.json'
    telnr = str(sys.argv[1])
    app = QApplication(sys.argv)
    window = MainWindow(telnr, credentials_path)
    window.show() 
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
