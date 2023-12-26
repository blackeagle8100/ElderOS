#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 15:01:37 2023
@author: meme
"""

import sys
import os
import subprocess
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
import configparser
import pyautogui
import requests
import threading


# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the INI file
config.read('settings.ini')

global colorcode, gusername, gww
colorcode = config.get('Settings', 'colorcode')
gusername = config.get('Settings', 'glogin')
gww = config.get('Settings', 'gww')






decrypt_process = subprocess.Popen(["python3", "dencrypt.py", "decrypt", gww], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
decrypt_output, decrypt_error = decrypt_process.communicate() 
decrypted_text = decrypt_output.decode().strip()
switch = decrypted_text
gww = switch

decrypt_process = subprocess.Popen(["python3", "dencrypt.py", "decrypt", gusername], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
decrypt_output, decrypt_error = decrypt_process.communicate() 
decrypted_text = decrypt_output.decode().strip()
switch = decrypted_text
gusername = switch


screen_width = int(config.get('Settings', 'screen_width'))
screen_height = int(config.get('Settings', 'screen_height'))

kbstate = 0
vgstate = 0

url = sys.argv[1]
program = str(sys.argv[2])  # Facebook, Youtube, Manillen

global teller
teller = 0
global fbid



class WebDialog(QDialog):
    def deletemancss(self):
     
        elem = '.game > div:nth-child(1) > div:nth-child(1)'
        self.browser.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = '.game > div:nth-child(2) > div:nth-child(1)'
        self.browser.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = '.game > div:nth-child(3) > div:nth-child(1)'
        self.browser.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = '.login'
        self.browser.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = '.pre > i:nth-child(1)'
        self.browser.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = '.top-icon'
        self.browser.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = 'h2.font-cinzel:nth-child(3)'
        self.browser.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = 'button.flex:nth-child(5)'
        self.browser.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = '.icon-tools'
        self.browser.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        
        
    
    def set_auto_zoom(self):
        # Set the zoom level to 100%
       
        self.browser.setZoomFactor(3)

        
    
   
    def autloginYT(self):
        # JavaScript code to fill in the form fields
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
        
        
    def loadFinishedHandler(self):
        self.browser.loadFinished.disconnect(self.loadFinishedHandler)
        
        
    def executeYTLogin(self):
        self.autloginYT()
        
    def loadFinishedHandlerYT(self):
        self.browser.loadFinished.disconnect(self.loadFinishedHandlerYT)
        self.executeYTLogin()
       
    def __init__(self, url, parent=None):
        super(WebDialog, self).__init__(parent)
        self.setWindowTitle("Web Dialog")
        self.mag_factor = 0
        self.setGeometry(0, 0, 800, 600)
        
        outputstring = "background-color: " + colorcode + ";"
        self.setStyleSheet(outputstring)  # Set the style sheet for the dialog

        layout = QVBoxLayout()
        self.setLayout(layout)
        
        
        top_layout = QHBoxLayout()
        layout.addLayout(top_layout)
        

        # VERGROOTKNOP
        vergroot_button = QPushButton("Vergroot", self)
        vergroot_button.setFont(QFont('Arial black', 30))
        vergroot_button.setFixedSize(200, 45)  # Set the size of the vergroot button
        vergroot_button.clicked.connect(self.openmage)
        top_layout.addWidget(vergroot_button)

        # TOETSENBORDKNOP
        kb_button = QPushButton("toetsenbord", self)
        kb_button.setFont(QFont('Arial black', 30))
        kb_button.setFixedSize(300, 45)  # Set the size of the kb button
        kb_button.clicked.connect(self.Keyboard)
        top_layout.addWidget(kb_button)

        # DownloadKnop
        self.download_button = QPushButton("Download", self)
        self.download_button.setFont(QFont('Arial black', 30))
        self.download_button.setFixedSize(200, 45)  # Set the size of the download button
        self.download_button.clicked.connect(self.DownloadYoutube)
        top_layout.addWidget(self.download_button)

        # VoegToeKnop
        fbAdd_button = QPushButton("Voeg toe", self)
        fbAdd_button.setFont(QFont('Arial black', 30))
        fbAdd_button.setFixedSize(300, 45)  # Set the size of the voeg toe button
        fbAdd_button.clicked.connect(self.addContact)
        top_layout.addWidget(fbAdd_button)

        # SLUITKNOP
        close_button = QPushButton("Sluiten", self)
        close_button.setFont(QFont('Arial black', 30))
        close_button.setFixedSize(200, 45)  # Set the size of the close button
        close_button.clicked.connect(self.closeourway)
        top_layout.addWidget(close_button)
        
        # VOLUMEUPKNOP
        self.volume_up_button = QPushButton("+")
        self.volume_up_button.setFont(QFont('Arial black', 30))
        self.volume_up_button.setFixedSize(50, 45)  # Set the size of the volume up button
        self.volume_up_button.clicked.connect(self.increase_volume)
        top_layout.addWidget(self.volume_up_button)
        
        # VOLUMEDOWNKNOP
        self.volume_down_button = QPushButton("-")
        self.volume_down_button.setFont(QFont('Arial black', 30))

        self.volume_down_button.setFixedSize(50, 45)  # Set the size of the volume down button
        self.volume_down_button.clicked.connect(self.decrease_volume)
        top_layout.addWidget(self.volume_down_button)

        # Download Label
        self.lbldownload = QLabel("", self)
        self.lbldownload.setFont(QFont('Arial black', 30))
        self.lbldownload.setFixedSize(200, 45)
        top_layout.addWidget(self.lbldownload)
        
        
        
        
        
        
       
        
        
        # Initialize the browser attribute
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        layout.addWidget(self.browser)
        #stacked_layout.addWidget(self.browser)
        self.showFullScreen()

        if program == "Manillen":
            self.lbldownload.hide()
            close_button.show()
            fbAdd_button.hide()
            self.download_button.hide()
            kb_button.hide()
            vergroot_button.hide()
            self.volume_down_button.hide()
            self.volume_up_button.hide()
            
            # Use JavaScript to set the zoom level to 100%
            self.browser.loadFinished.connect(self.set_auto_zoom)
            self.browser.loadFinished.connect(self.deletemancss)
      
        elif program == "Youtube":
            self.lbldownload.show()
            close_button.show()
            fbAdd_button.hide()
            self.download_button.show()
            kb_button.show()
            vergroot_button.show()
            self.volume_down_button.show()
            self.volume_up_button.show()
            self.browser.loadFinished.connect(self.loadFinishedHandlerYT)
            
            
        elif program == "Bubble":
            self.lbldownload.hide()
            close_button.show()
            fbAdd_button.hide()
            self.download_button.hide()
            kb_button.hide()
            vergroot_button.hide()
            self.volume_down_button.hide()
            self.volume_up_button.hide()
        
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
            
    def increase_volume(self):
        # Implement logic to increase the volume
        self.browser.page().runJavaScript("document.querySelector('video').volume += 0.1;")

    def decrease_volume(self):
        # Implement logic to decrease the volume
        self.browser.page().runJavaScript("document.querySelector('video').volume -= 0.1;")   
        
    def addContact(self):
        try:
            os.system('clear')
            link = self.browser.url().toString()
            print("URL: " + link)
            
            # Get the HTML source code of the link
            html_content = requests.get(link).text

            print("-------------------------------------------------------------------")
            # print(html_content)
            print("-------------------------------------------------------------------")
            
            # Get Facebook ID
            if 'userID' in html_content:           
                pieces = html_content.split('userID":"')
                fbid = pieces[1]
                pieces = fbid.split('"')
                fbid = pieces[0]
                pieces = html_content.split('<title>')
                username = pieces[1]
                pieces = username.split('</title>')
                username = pieces[0]
                # Capture the entire screen
                savestate = True
            elif 'entity_id' in html_content:
                print('Deze code werkt op entity!')
                pieces = html_content.split('entity_id":"')
                fbid = pieces[1]
                pieces = fbid.split('"')
                fbid = pieces[0]
                pieces = link.split('https://www.facebook.com/')
                username = pieces[1]
                username = username.replace(".", " ")
                username = ''.join(char for char in username if not char.isdigit())
                username = username.title()
                savestate = True
            else:
                print('Hier is geen gebruikers ID te vinden.')
                fbid = 'None'
                username = 'None'
                savestate = False

            print('************************')
            print('ID')
            print(fbid)
            print('************************')
            print("**********************************")
            print('USERNAME')
            print(username)
            print("**********************************")
            
            if savestate:
                # SAVE STATS TO INI AND SAVE IMAGE
                config.clear()
                print('Opslaan')
                config.read('/home/meme/VASTSYSTEEM/Telephone/Contact/contacten.ini')
                # Update the desired values
                config.add_section(str(fbid))
                config.set(fbid, 'naam', str(username))
                config.set(fbid, 'id', str(fbid))
                config.set(fbid, 'type', 'facebook')
                # Save the changes back to the INI file
                with open('/home/meme/VASTSYSTEEM/Telephone/Contact/contacten.ini', 'w') as config_file:
                    config.write(config_file)
                pyautogui.click(200, 300)
                pyautogui.press('home')
                pyautogui.click(500, 600)
                delay_seconds = 1  # 5 seconds
                print('SAVED')
                self.lbldownload.setText('Opgeslagen!')
                
                # Create a timer to introduce the delay and call the delayed function
                timer = threading.Timer(delay_seconds, lambda: delayed_function())
                timer.start()

                def delayed_function():
                    global screenshot
                    print("ok")
                    screenshot = pyautogui.screenshot()
                    # Define the coordinates for cropping (left, top, right, bottom)
                    crop_coordinates = (400, 300, 1100, 1000)
                    # Perform any other actions with the screenshot here
                    # Crop the screenshot image
                    cropped_image = screenshot.crop(crop_coordinates)
                    cropped_image.save("/home/meme/Documenten/Telephone/Contact/" + fbid + '.png')
                    print("Screenshot captured.")   
                    pyautogui.press('esc')
            else:
                print('Niets opgeslagen')
                self.lbldownload.setText('Niet opgeslagen!')
          
        except Exception as e:
            print("Error:", e)
            self.lbldownload.setText('Niet opgeslagen!')
            print(e)

if __name__ == '__main__':
    app = QApplication([])
    dialog = WebDialog(url)
    app.exec_()
