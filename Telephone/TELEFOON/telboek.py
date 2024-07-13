#!/usr/bin/env python3

from PyQt6.QtWidgets import (QApplication,QWidget,QVBoxLayout,
                              QListWidget, QLabel, QHBoxLayout, 
                              QGridLayout, QPushButton, QListWidgetItem, QScrollArea)
from PyQt6.QtGui import QPixmap, QFont, QImage
from PyQt6.QtCore import Qt, QTime, QTimer
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError
import time
import subprocess
import re
import psutil
import configparser
import os 
import sys
from pathlib import Path
import requests
from PIL.ImageQt import ImageQt
from PIL import Image
import io

user_home = os.path.expanduser("~")
global vastsysteem_path
global imagesize
imagesize = 300

vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

config = configparser.ConfigParser()
config.read(vastsysteem_path + '/settings.ini')

global colorcode
colorcode = config.get('Settings', 'colorcode')
screen_width = int(config.get('Settings', 'screen_width'))
screen_height = int(config.get('Settings', 'screen_height'))
font_type = config.get('Settings', 'font_type')
font_size = int(config.get('Settings', 'font_size'))
device_ip =  config.get('Settings', 'smartip')
bgcolor = ("background-color: " + config.get('Settings', 'colorcode') + ";")

bring = False

class GoogleContactsWidget(QWidget):
    def __init__(self, credentials_path):
        super().__init__()
        self.setWindowTitle("Telefoonboek")
        self.setStyleSheet(bgcolor)  # Set the background color
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(0, 0, screen_width, screen_height)  # Set window size
        

        self.credentials_path = Path(credentials_path)
        self.credentials = self.get_credentials()
        self.service = self.create_service()
        self.contacts = self.get_contacts()
        
        self.init_ui()

    def get_credentials(self):
        creds = None
        if self.credentials_path.exists():
            creds = Credentials.from_authorized_user_file(self.credentials_path)
            print(creds)
        # Check if credentials are expired
        if creds and creds.expired:
            print("iets mis")
        return creds


    def create_service(self):
        return build('people', 'v1', credentials=self.credentials)

    def get_contacts(self):
        results = self.service.people().connections().list(
            resourceName='people/me',
            pageSize=100,
            personFields='names,phoneNumbers,photos').execute()
        connections = results.get('connections', [])
        print(connections)
        contacts = []
        for person in connections:
            
            names = person.get('names', [])
            phoneNumbers = person.get('phoneNumbers', [])
            photos = person.get('photos', [])
            if names and phoneNumbers:
                name = names[0].get('displayName')
                phone = phoneNumbers[0].get('value')
                if photos:
                    photo_url = photos[0].get('url')
                    contacts.append((name, phone, photo_url))
                else:
                    contacts.append((name, phone, None))
        return contacts
    
    def startreading(self, event=None):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_serial_data)
        self.timer.start(100)  # Check for data every 100 milliseconds


    def check_serial_data(self):
        global bring
        if bring == False:
            data = ser.readline().decode().strip()
            print("Ontvangen:", data)
            # Handle the received data as needed,
            # e.g., update a label in your GUI or trigger other actions
           
            if "+ESPEECH: 1,1,0" in data:
                print("gesprek gestart. wacht op het gesprek om te stoppen")
                self.startklok()
            elif "+ESPEECH: 0,1,0" in data:
                self.timerlabel.setText("Gesprek gestopt. Druk ROOD om te SLUITEN \n Groen om een nieuw gesprek te starten.")
                self.klok.stop()
                print("Gesprek gestopt.\n vang de fake carrier op:")
                data = ser.readline().decode().strip()
                print("Ontvangen nix:", data)
                data = ser.readline().decode().strip()
                print("Fake carrier:", data)
                print("Stuur ATH command om gesprek te sluiten")
                ser.write(b'ATH\r\n')
                data = ser.readline().decode().strip()
                print("ontvangen: ", data )
                bring = True
               
            
            elif "CARRIER" in data:
                bring = True

        elif bring == True:
            self.timer.stop()
            print("Bring is waar; nieuwe calls kunnen ontvangen worden")
           
            time.sleep(0.5)

            if not self.check_process_running("serialreader.py"):
                subprocess.Popen(["python3", os.path.join(vastsysteem_path, "/Telephone/TELEFOON/serialreader.py")])
            else:
                print("serialreader.py is already running")
        

    def check_process_running(self, process_name):
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == process_name:
                return True
        return False
    
    def takecall(self, event=None):
        selected_item = self.contact_list.currentItem()
        if selected_item:
            data = selected_item.text()
            print("Selected Contact:", data)
            split = data.split(":")
            naam = split[0]
            print("naam: ", naam)
            data = split[1]
            nummer = data.replace(" ", "")
            nummer = nummer.replace("/", "")
            print("Nummer: ", nummer)
            # Further processing with the selected contact data
            print("Start het gesprek")
            try:
                print("try call")
                subprocess.run(["adb", "-s", device_ip, "shell", "am", "start", "-a", "android.intent.action.CALL", "-d", "tel:"+nummer])
                self.startklok()
            except Exception as e:
                print("error "+e)
        else:
            print("Geen contactpersoon geselecteerd.")
            self.timerlabel.setText("Selecteer eerst naar wie je wilt bellen.")
    def cancelcall(self, event=None):
        print("Stop call")
        subprocess.run(["adb", "-s", device_ip, "shell", "input", "keyevent", "KEYCODE_ENDCALL"])
        try:
             script_path = vastsysteem_path+"/Telephone/TELEFOON/serialreader.py"
             self.kill_script_by_path(script_path)
        except:
            print("serialreader was niet aan het draaien")
        # Start a new terminal with serialreader.py
        subprocess.Popen(["python3", vastsysteem_path+"/Telephone/TELEFOON/serialreader.py"])
        # End the current script
        sys.exit()

    def startklok(self):
        # Create and start the timer
        self.klok = QTimer(self)
        self.klok.timeout.connect(self.update_timer)
        self.klok.start(1000)  # Update timer every 1 second
        # Initialize the timer value
        self.timer_value = QTime(0, 0)
        self.update_timer()
    
    def alphabet_button_clicked(self, char):
        # Handle alphabet button click
        print("gedrukt op " + char)

        self.lblfoto.setText("Selecteer\nwie je\nwilt\nbellen")
        
        # Clear the existing items in the contact list
        self.contact_list.clear()
        
        for button in self.findChildren(QPushButton):
            button.setStyleSheet("background-color: black; color: white;")
        self.sender().setStyleSheet("background-color: white; color: black;")
        # Filter the contacts that start with the clicked character
        filtered_contacts = [(name, phone, image) for name, phone, image in self.contacts if name.startswith(char)]
        if not filtered_contacts:
            print("Geen contactpersonen weer te geven voor de letter", char)
            self.contact_list.addItem(f'Geen contacten gevonden voor de letter  {char}')
        else:
            # Add filtered contacts to the contact_list
            for name, phone, image in filtered_contacts:
                telnr = phone.replace(" ", "")
                telnr = telnr.replace("+32", "0")
                char_count = len(telnr)
                if char_count == 9:
                    telnr = telnr[0] + telnr[1] + telnr[2] + "/" + telnr[3] + telnr[4] + " " + telnr[5] + telnr[6] + " " + telnr[7] + telnr[8]
                elif char_count == 10:
                    telnr = telnr[0] + telnr[1] + telnr[2] + telnr[3] + "/" + telnr[4]  + telnr[5] + " " + telnr[6]  + telnr[7] + " " + telnr[8] + telnr[9]
                self.contact_list.addItem(f'{name}: {telnr}')
                


    def display_contact_image(self):
        print("DISPLAY IMAGE")
        selected_item = self.contact_list.currentItem()
        if selected_item:
            contact_details = selected_item.text()
            # Split the contact details into name and phone
            name, phone = contact_details.split(":")
            # Search for the selected contact in the contacts list
            for contact in self.contacts:
                if name in contact:
                    name, phone, image_url = contact
                    # Display the image if the URL is available
                    if image_url:
                        image_url = image_url.replace("s100","s300")
                        print(image_url)
                        # Download and display the image
                        response = requests.get(image_url)
                        
                        if response.status_code == 200:
                            image_data = response.content
                            pixmap = QPixmap()
                            pixmap.loadFromData(image_data)
        
                        
                            self.lblfoto.setPixmap(pixmap)
                            return
                        else:
                            print(f"Failed to download image for {name}")
                            return
                    else:
                        print(f"No image URL available for {name}")
                        return
            print(f"Contact {name} not found in the contacts list")
        else:
            print("No contact selected")



    def resetlist(self):
        print("reset the list")
        for button in self.findChildren(QPushButton):
            button.setStyleSheet("background-color: black; color: white;")
        self.contact_list.clear()
        self.lblfoto.setText("Selecteer\nwie je\nwilt\nbellen")
        for name, phone, foto in self.contacts:
            telnr = phone.replace(" ", "")
            telnr = telnr.replace("+32", "0")
            char_count = len(telnr)
            if char_count == 9:
                #print("Vast nummer")
                telnr = telnr[0] + telnr[1] + telnr[2] + "/" + telnr[3] + telnr[4] + " " + telnr[5] + telnr[6] + " " + telnr[7] + telnr[8]
            elif char_count == 10:
                #print("GSM nr")
                telnr = telnr[0] + telnr[1] + telnr[2] + telnr[3] + "/" + telnr[4]  + telnr[5] + " " + telnr[6]  + telnr[7] + " " + telnr[8] + telnr[9]
            else:
                print("Ongekend nummer")
            #print(char_count)
            self.contact_list.addItem(f'{name}: {telnr}')


    
    
    def update_timer(self):
        # Update the timer value and display it on the label
        self.timer_value = self.timer_value.addSecs(1)
        waarde = self.timer_value.toString("mm:ss")
        self.timerlabel.setText("Duur van het gesprek: "+ waarde)

    def kill_script_by_path(self, script_path):
        try:
            # Execute the command to kill the process
            subprocess.run(['pkill', '-f', script_path], check=True)
            print(f"Process associated with {script_path} terminated successfully.")
        except subprocess.CalledProcessError:
            print(f"Failed to terminate process associated with {script_path}.")

    def init_ui(self):
        self.contacts.sort(key=lambda contact: contact[0])
        self.contact_list = QListWidget()
        for name, phone, foto in self.contacts:
            telnr = phone.replace(" ", "")
            telnr = telnr.replace("+32", "0")
            char_count = len(telnr)
            if char_count == 9:
                #print("Vast nummer")
                telnr = telnr[0] + telnr[1] + telnr[2] + "/" + telnr[3] + telnr[4] + " " + telnr[5] + telnr[6] + " " + telnr[7] + telnr[8]
            elif char_count == 10:
                #print("GSM nr")
                telnr = telnr[0] + telnr[1] + telnr[2] + telnr[3] + "/" + telnr[4]  + telnr[5] + " " + telnr[6]  + telnr[7] + " " + telnr[8] + telnr[9]
            else:
                print("Ongekend nummer")
            #print(char_count)
            self.contact_list.addItem(f'{name}: {telnr}')
        #layout.addWidget(self.contact_list)
        
        self.contact_list.setFont(QFont(font_type, font_size))
        self.contact_list.setFixedWidth(int(screen_width/2))
      
        self.contact_list.itemClicked.connect(self.display_contact_image)
  
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        grid_layout.setRowStretch(0, 0)
        grid_layout.setColumnStretch(0, 0)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        row, col = 0, 0
        for char in alphabet:
            button = QPushButton(char)
            button.setFont(QFont(font_type, font_size))
          
            button.setStyleSheet("background-color: black; color: white;")
            button.setFixedSize(80, 80)  # Adjust size as needed
            
            button.clicked.connect(lambda checked, ch=char: self.alphabet_button_clicked(ch))
            button.setContentsMargins(0, 0, 0, 0)
            grid_layout.addWidget(button, row, col)
            col += 1
            if col == 7:
                col = 0
                row += 1
  

        self.takecall_btn = QLabel(" ")
        im = Image.open(vastsysteem_path+"/icons/neemop.png")
        newsize = (200,200)
        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.takecall_btn.setPixmap(pixmap)
        self.takecall_btn.setMouseTracking(True)
        self.takecall_btn.mousePressEvent = self.takecall

        self.spacing = QLabel("")
        self.spacing.setFixedWidth(screen_width -450)

        self.cancelcall_btn = QLabel(" ")
        im = Image.open(vastsysteem_path+"/icons/legtoe.png")
        newsize = (200,200)
        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.cancelcall_btn.setPixmap(pixmap)
        self.cancelcall_btn.setMouseTracking(True)
        self.cancelcall_btn.mousePressEvent = self.cancelcall

        self.timerlabel = QLabel("Gespreksduur: Gesprek nog niet gestart.")

        self.timerlabel.setFont(QFont(font_type, font_size))


        self.lblcontacten = QLabel("Contacten")
    
        self.lblcontacten.setFont(QFont(font_type, font_size))
        self.lblzoeken = QLabel("Zoeken")
        self.lblzoeken.setFont(QFont(font_type, font_size))
    
        
        self.btnreset = QPushButton("Toon alle contacten")
        self.btnreset.clicked.connect(self.resetlist)
        self.btnreset.setFont(QFont(font_type, font_size))
        self.btnreset.setStyleSheet("background-color: black; color: white;")
     
        self.lblfoto = QLabel("Selecteer\nwie je\nwilt\nbellen")
        self.lblfoto.setFont(QFont(font_type, font_size))
        self.lblfoto.setMouseTracking(True)
        self.lblfoto.mousePressEvent = self.takecall
        self.lblfoto.setFixedSize(imagesize,imagesize)
 

     
        #LAYOUT
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter |Qt.AlignmentFlag.AlignTop)

        middel = QHBoxLayout()
        middel1 = QVBoxLayout()
        middel2 = QVBoxLayout()
        

        lotimer = QHBoxLayout()
        loimage = QHBoxLayout()

        loimage.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        lotimer.setAlignment(Qt.AlignmentFlag.AlignCenter) 

        middel.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        middel1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        middel2.setAlignment(Qt.AlignmentFlag.AlignCenter)
         

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        middel1.addWidget(self.lblcontacten)
        middel1.addWidget(self.contact_list)

        middel2.addWidget(self.lblzoeken)
        middel2.addLayout(grid_layout)
        middel2.addWidget(self.btnreset)
        loimage.addWidget(self.lblfoto)

        middel2.addLayout(loimage)
        

        btn_layout.addWidget(self.takecall_btn)
        btn_layout.addWidget(self.spacing)
        btn_layout.addWidget(self.cancelcall_btn)
        middel.addLayout(middel1)
        middel.addLayout(middel2)
        
        layout.addLayout(middel)

        lotimer.addWidget(self.timerlabel)
        layout.addLayout(lotimer)

        layout.addLayout(btn_layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    credentials_path = vastsysteem_path +'/UsefullPrograms/googleAI/secrets/multitoken.json'
    print(credentials_path)
    widget = GoogleContactsWidget(credentials_path)  # Pass credentials_path here
    widget.show()
    sys.exit(app.exec())
