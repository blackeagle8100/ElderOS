#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 15:01:37 2023
@author: meme
"""

import sys
import os
import subprocess
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QFont, QPixmap

from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
import configparser
import pyautogui
import requests
import threading
import pygame



# Create a ConfigParser object
config = configparser.ConfigParser()

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

# Read the INI file
config.read(vastsysteem_path + '/settings.ini')

global colorcode, gusername, gww
colorcode = config.get('Settings', 'colorcode')
gusername = config.get('Settings', 'glogin')
gww = config.get('Settings', 'gww')






decrypt_process = subprocess.Popen(["python3", vastsysteem_path + "/dencrypt.py", "decrypt", gww], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
decrypt_output, decrypt_error = decrypt_process.communicate() 
decrypted_text = decrypt_output.decode().strip()
switch = decrypted_text
gww = switch

decrypt_process = subprocess.Popen(["python3", vastsysteem_path + "/dencrypt.py", "decrypt", gusername], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
decrypt_output, decrypt_error = decrypt_process.communicate() 
decrypted_text = decrypt_output.decode().strip()
switch = decrypted_text
gusername = switch
screen_width = int(config.get('Settings', 'screen_width'))
screen_height = int(config.get('Settings', 'screen_height'))

kbstate = 0
vgstate = 0

url = "https://www.youtube.com/signin" # Facebook, Youtube, Manillen

global teller
teller = 0
global fbid
global volume

volume = 0
def set_volume(volume_level):
    # Calculate the volume value based on the desired level
    volume = int(volume_level)  # Range: 0-100

    # Set the volume using the 'amixer' command
    subprocess.run(["amixer", "-D", "default", "sset", "Master", f"{volume}%"])

class WebDialog(QDialog):
        
    def set_auto_zoom(self):
        # Set the zoom level to 100%
        self.browser.setZoomFactor(3)

    def autloginYT(self):
    # Execute the JavaScript code to automatically log in to YouTube
        script = """
        function wait(delay) {
            return new Promise(resolve => setTimeout(resolve, delay));
        }

        function vulaccin() {
            var identifierInput = document.getElementsByName('identifier')[0];
            identifierInput.value = '%s';
        }

        function vulwwin() {
            var passwordInput = document.getElementsByClassName('whsOnd zHQkBf')[0];
            passwordInput.value = '%s';
        }

        function volgendeclick() {
            var buttons = document.getElementsByTagName('button');
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].textContent.trim() === 'Volgende') {
                    buttons[i].click();
                    break;
                }
            }
        }
        vulaccin();
        volgendeclick();
        wait(3000).then(() => {
            vulwwin();
            volgendeclick();
        });
        """ % (gusername, gww)
        self.browser.page().runJavaScript(script)



    def Keyboard(self):
            global kbstate
            if kbstate == 0:
                subprocess.Popen("onboard")
                kbstate = 1
            elif kbstate == 1:
                kbstate = 0
                os.system("pkill onboard")
       
    def openmage(self):
            
            
            if self.mag_factor == 3:
                self.browser.setZoomFactor(1)
                self.mag_factor = 0
                print('Magnification factor set to 1.0')
            elif self.mag_factor == 0:
                self.browser.setZoomFactor(3)
                self.mag_factor = 3
                print('Magnification factor set to 2.0')
            else:
                print('Unexpected magnification factor:', self.mag_factor)

    def closeourway(self):
            os.system("pkill onboard")
            self.close()
            #subprocess.run(['gsettings', 'set', 'org.gnome.desktop.a11y.magnifier', 'mag-factor', '1.0'], bufsize=0)

    def DownloadYoutube(self):
            self.browser.page().toPlainText(self.onPlainText)
            self.lbldownload.setText("Aan het downloaden!")
            self.download_button.setEnabled(False)

    def onPlainText(self, plainText):
            url = self.browser.url().toString()  # Get the current URL
            print("Download URL:", url)
            # Add your download logic here
            process = subprocess.Popen(["python3", "youtube-downloader.py", str(url)])
            process.wait()  # Wait for the subprocess to finish
            if process.returncode == 0:
                print("Download ok")
                self.download_button.setEnabled(True)
                self.lbldownload.setText('Download OK')
            else:
                print("Subprocess error:", process.returncode)
                
    
                
    def volume_up(self):
        global volume
        if volume == 100:
            volume = 100
        else:    
            volume = volume +10
            set_volume(volume)

    def volume_down(self):
        global volume
        if volume == 0:
            volume = 0
        else:
            volume = volume -10
            set_volume(volume)

            
    def loadFinishedHandler(self):
        self.browser.loadFinished.disconnect(self.loadFinishedHandler)
         
    def executeYTLogin(self):
        self.autloginYT()
        
    def loadFinishedHandlerYT(self):
        self.browser.loadFinished.disconnect(self.loadFinishedHandlerYT)
        self.executeYTLogin()
       
    def __init__(self, url, parent=None):
        super(WebDialog, self).__init__(parent)
        self.setWindowTitle("Youtube")
        self.mag_factor = 0
        self.setGeometry(0, 0, screen_width, screen_height)
        outputstring = "background-color: " + colorcode + ";"
        self.setStyleSheet(outputstring)  # Set the style sheet for the dialog
        volume_layout = QHBoxLayout()
        volume_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        
        top_layout = QHBoxLayout()
        layout.addLayout(top_layout)
        
        # SLUITKNOP
        close_button = QPushButton("Sluiten", self)
        close_button.setFont(QFont('Arial black', 30))
        close_button.setFixedSize(200, 100)  # Set the size of the close button
        close_button.clicked.connect(self.closeourway)
        top_layout.addWidget(close_button)
        
        
        # VERGROOTKNOP
        vergroot_button = QPushButton("Vergroot", self)
        vergroot_button.setFont(QFont('Arial black', 30))
        vergroot_button.setFixedSize(200, 100)  # Set the size of the vergroot button
        vergroot_button.clicked.connect(self.openmage)
        top_layout.addWidget(vergroot_button)

        # TOETSENBORDKNOP
        kb_button = QPushButton("toetsenbord", self)
        kb_button.setFont(QFont('Arial black', 30))
        kb_button.setFixedSize(300, 100)  # Set the size of the kb button
        kb_button.clicked.connect(self.Keyboard)
        top_layout.addWidget(kb_button)

        # DownloadKnop
        self.download_button = QPushButton("Download", self)
        self.download_button.setFont(QFont('Arial black', 30))
        self.download_button.setFixedSize(200, 100)  # Set the size of the download button
        self.download_button.clicked.connect(self.DownloadYoutube)
        top_layout.addWidget(self.download_button)

        # Download Label
        self.lbldownload = QLabel("", self)
        self.lbldownload.setFont(QFont('Arial black', 30))
        self.lbldownload.setFixedSize(200, 100)
        top_layout.addWidget(self.lbldownload)
        
        # VOLUMEDOWNKNOP - 
        self.volume_down_button = QPushButton("-")
        self.volume_down_button.setFont(QFont('Arial black', 30))
        self.volume_down_button.setFixedSize(100, 100)  # Set the size of the volume down button
        self.volume_down_button.clicked.connect(self.volume_down)
        volume_layout.addWidget(self.volume_down_button)
        
        
        #SPEAKER ICON
        self.speaker = QLabel()
        speaker_path = os.path.join(vastsysteem_path + "/icons/Speaker.png")
        pixmap = QPixmap(speaker_path)
        pixmap = pixmap.scaled(100, 100) 
        self.speaker.setPixmap(pixmap)
        volume_layout.addWidget(self.speaker)
        
        # VOLUMEUPKNOP + 
        self.volume_up_button = QPushButton("+")
        self.volume_up_button.setFont(QFont('Arial black', 30))
        self.volume_up_button.setFixedSize(100, 100)  # Set the size of the volume up button
        self.volume_up_button.clicked.connect(self.volume_up)
        volume_layout.addWidget(self.volume_up_button)
        
        

        top_layout.addLayout(volume_layout)
        
        # Initialize the browser attribute
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        layout.addWidget(self.browser)
        #stacked_layout.addWidget(self.browser)
        self.showFullScreen()
        self.browser.loadFinished.connect(self.loadFinishedHandlerYT)
            
            
    
   
        

if __name__ == '__main__':
    app = QApplication([])
    dialog = WebDialog(url)
    app.exec()
