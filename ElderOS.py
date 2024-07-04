#!/usr/bin/env python3

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTime, QTimer, QDate
from PyQt6.QtGui import QPixmap
import sys
import subprocess
import configparser
from PIL.ImageQt import ImageQt
from PIL import Image
import os
import pygame
# Create a ConfigParser object
config = configparser.ConfigParser()
pygame.init()
user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")
AIaudio_path = os.path.join(vastsysteem_path, "UsefullPrograms/SOUNDS/AIsounds/")
# Read the INI file
config.read(vastsysteem_path + '/settings.ini')
screen_height = int(config.get('Settings', 'screen_height'))
screen_width = int(config.get('Settings', 'screen_width'))
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("MAIN")
        outputstring = ("background-color: " + config.get('Settings', 'colorcode') + ";")
        self.setStyleSheet(outputstring)  # Set the background color
       # self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        
        # Create a list of enabled apps based on configuration settings
        self.enabled_apps = []
        self.enabled_apps.append("Help")
        self.uitvoer = "Help"
        if int(config.get('Settings', 'vweer')) == 1:
            self.enabled_apps.append("Weer")
            self.uitvoer = 'Weer'
        if int(config.get('Settings', 'vinternet')) == 1:
            self.enabled_apps.append("Internet")
            self.utvoer = 'Internet'
        if int(config.get('Settings', 'vinstellingen')) == 1:
            self.enabled_apps.append("Instellingen")
            self.uitvoer = 'Instellingen'
        if int(config.get('Settings', 'vtel')) == 1:
            self.enabled_apps.append("Telefoon")
            self.uitvoer = 'Telefoon'
        if int(config.get('Settings', 'vgal')) == 1:
            self.enabled_apps.append("Galerij") 
            self.uitvoer = 'Galerij'
        if int(config.get('Settings', 'vtv')) == 1:
            self.enabled_apps.append("TVFM")
            self.uitvoer = 'TVFM'
        if int(config.get('Settings', 'vmusic')) == 1:
            self.enabled_apps.append("Muziekspeler")
            self.uitvoer = 'Music'
        if int(config.get('Settings', 'vgames')) == 1:
            self.enabled_apps.append("Games")
            self.uitvoer = 'Games'
        if int(config.get('Settings', 'vkalender')) == 1:
            self.enabled_apps.append("Kalender")
            self.uitvoer = 'Kalender'

        if int(config.get('Settings', 'vwekker')) == 1:
            self.enabled_apps.append("Wekker")
            self.uitvoer = 'Wekker'
        # Initialize the current app index
        self.current_app_index = 0
        
        # Create a QLabel to display the app name
        self.labelProgram = QLabel(self)
        self.labelProgram.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_size = int(config.get('Settings', 'font_size'))
        outputstring = f"font: {font_size}pt {config.get('Settings', 'font_type')}; font-weight: bold; background-color: {config.get('Settings', 'colorcode')};"
        self.labelProgram.setStyleSheet(outputstring)
       # self.labelProgram.setFixedSize(screen_width - 900, font_size+30)
        #self.labelProgram.setMargin(60)
        # Create a QLabel to display the app icon
        self.labelUitvoeren = QLabel(self)
        self.labelUitvoeren.setFixedSize(900, 900)
        self.labelUitvoeren.setMouseTracking(True)
        self.labelUitvoeren.mousePressEvent = self.uitvoeren
        self.labelUitvoeren.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Create a QLabel to display clock
        self.labelKlok = QLabel(self)
        self.labelKlok.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelKlok.setStyleSheet(outputstring)
        #self.labelKlok.setMargin(40)

        # Create "Next" and "Back" buttons
        self.btnVolgende = QLabel(" ", self)
        self.btnVolgende.setFixedSize(200, screen_height - 20)
      
        im = Image.open(r"./icons/arrowleft.png") 
        newsize = (200, screen_height - 20)
        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.btnVolgende.setPixmap(pixmap)   
          # Set button size to match the image size
        self.btnVolgende.setMouseTracking(True)
        self.btnVolgende.mousePressEvent = self.volgende
        
        
        # Create "Next" and "Back" buttons
        self.btnVorige = QLabel(" ", self)
        self.btnVorige.setFixedSize(200, screen_height - 20)
      
        im = Image.open(r"./icons/arrowright.png") 
        newsize = (200, screen_height - 20)
        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.btnVorige.setPixmap(pixmap)
          # Set button size to match the image size
        self.btnVorige.setMouseTracking(True)
        self.btnVorige.mousePressEvent = self.vorige
        
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)  # 1000 milliseconds = 1 second
        
        # Initial update
        self.update_clock()
        
        # Initialize the displayed app
        self.update_displayed_app()
        
        # Create layouts
        mainlayout = QHBoxLayout()
        middlelayout  = QVBoxLayout()
        htoplayout = QVBoxLayout()
        
        htoplayout.setContentsMargins(0,0,0,0)
        mainlayout.setContentsMargins(0, 0, 0, 0)
        middlelayout.setContentsMargins(0, 0, 0, 0)
        
        
        middlelayout.addWidget(self.labelKlok, alignment=Qt.AlignmentFlag.AlignHCenter)
        middlelayout.addWidget(self.labelProgram, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        #middlelayout.addLayout(htoplayout)
        #middlelayout.addWidget(self.labelUitvoeren)
        middlelayout.addWidget(self.labelUitvoeren, alignment=Qt.AlignmentFlag.AlignHCenter)
       
       
        mainlayout.addWidget(self.btnVolgende)
        mainlayout.addLayout(middlelayout)
        mainlayout.addWidget(self.btnVorige)
       
       
        widget = QWidget()
        widget.setLayout(mainlayout)
        self.setCentralWidget(widget)

    
    
    def uitvoeren(self, event=None):
        print(self.uitvoer)
        
        #self.labelUitvoeren.setEnabled(False)
        if self.uitvoer == 'Instellingen':
            subprocess.Popen(["python3", "LOADING.py", "1"])
            subprocess.Popen(["python3", "FULLSETTINGS.py", "5"])
            self.url = "https://www.facebook.com"
            
        elif self.uitvoer == 'Facebook':
            subprocess.Popen(["python3", "LOADING.py", "5"])
            self.url = "https://www.facebook.com"
            subprocess.Popen(["python3", "./Facebook/Facebook.py", str(self.url), str(self.uitvoer)])
            
        elif self.uitvoer == 'Youtube':
            subprocess.Popen(["python3", "LOADING.py", "5"])
            self.url = "https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Dnl%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=nl&ec=65620"
            subprocess.Popen(["python3", "ExternBrowser.py", str(self.url), str(self.uitvoer)])
            
        elif self.uitvoer == 'Telefoon':
            subprocess.Popen(["python3", "LOADING.py", "2"])
            self.openmessenger()
            
        elif self.uitvoer == "Manillen":
            subprocess.Popen(["python3", "LOADING.py", "3"])
            self.openManillen()
            
        elif self.uitvoer == 'Galerij':
            subprocess.Popen(["python3", "LOADING.py", "3"])
            self.openGallery()
            print("Foto's")
            
        elif self.uitvoer == 'Muziekspeler':
            self.openSpeler()
            print("MUZIEK!")
           
        elif self.uitvoer == 'Patience':
            self.openPatience()
            
        elif self.uitvoer == 'TVFM':    
            print('TV')
            subprocess.Popen(["python3", "./TV/TV.py"])
        elif self.uitvoer == 'Weer':    
            print('Weer')
            subprocess.Popen(["python3", "./WEER/weer.py"])
        elif self.uitvoer == 'Internet':    
            subprocess.Popen(["python3", "InternetMenu.py"])
        elif self.uitvoer == 'Games':    
            subprocess.Popen(["python3", "GamesMenu.py"])
        elif self.uitvoer == "Help":
            subprocess.Popen(["python3","./helptest.py"])
        elif self.uitvoer == "Wekker":
            print(("Open de wekker"))
            sound_path = (AIaudio_path + "unavailable.wav")
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        elif self.uitvoer =="Kalender":
            print("Open de kalender")
            sound_path = (AIaudio_path + "unavailable.wav")
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
       
    
    def volgende(self, event=None):
        self.current_app_index += 1
        
        # Check if we've reached the end of the list, loop back if necessary
        if self.current_app_index >= len(self.enabled_apps):
            self.current_app_index = 0
        
        # Update the displayed app based on the current index
        self.update_displayed_app()
    
    def vorige(self, event=None):
        self.current_app_index -= 1
        
        # Check if we've gone below 0, wrap around if necessary
        if self.current_app_index < 0:
            self.current_app_index = len(self.enabled_apps) - 1
        
        # Update the displayed app based on the current index
        self.update_displayed_app()
    
    def update_displayed_app(self):
        # Get the app name based on the current index
        app_name = self.enabled_apps[self.current_app_index]
        
        # Update the label to display the selected app
        self.labelProgram.setText(app_name)
        self.uitvoer = (app_name)
        print(self.uitvoer)
        # Load and set the pixmap based on app_name

        im = Image.open(f"{vastsysteem_path}/icons/{app_name}") 
        newsize = (900, 900)
        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap

        #pixmap = QPixmap(f"{vastsysteem_path}/icons/{app_name}")
        self.labelUitvoeren.setPixmap(pixmap)

    def update_clock(self):
        current_date = QDate.currentDate()
        current_time = QTime.currentTime()
        formatted_datetime = current_date.toString("dd/MM") + " " + current_time.toString("hh:mm:ss")
        self.labelKlok.setText(formatted_datetime)
        
    def openManillen(self):
        subprocess.Popen(['python3','./Games/Manillen.py'])
    def openPatience(self):
        subprocess.Popen(['python3','./Games/Patience.py'])
    def openmessenger(self):
        subprocess.Popen(['python3','./Telephone/MAINphone.py'])
    def openGallery(self):
        subprocess.Popen(['python3', './Gallery/gallery.py'])
    def openSpeler(self):
        subprocess.Popen(['python3', './MediaPlayer/Mediaplayer.py']) 
    def openSettings(self):
        subprocess.Popen(['python3', './settingsGUICOMPLETE.py']) 
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
