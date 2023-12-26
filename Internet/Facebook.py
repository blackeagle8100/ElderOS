#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 15:25:07 2023

@author: meme
"""
import os
import pyautogui
import requests
import threading
import sys
import configparser
import subprocess
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QFont
from PyQt6 import QtWidgets

from PyQt6.QtWebEngineWidgets import QWebEngineView

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the INI file
config.read( vastsysteem_path + '/settings.ini')

global colorcode, gusername, gww, fbusername, fbww, font_size, font_type, url
colorcode = config.get('Settings', 'colorcode')
screen_height = int(config.get('Settings', 'screen_height'))
screen_width = int(config.get('Settings', 'screen_width'))
fbusername = config.get('Settings', 'fblogin')

decrypt_process = subprocess.Popen(["python3", vastsysteem_path + "/dencrypt.py", "decrypt", fbusername], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
decrypt_output, decrypt_error = decrypt_process.communicate() 
decrypted_text = decrypt_output.decode().strip()
switch = decrypted_text
fbusername = switch

fbww = config.get('Settings', 'fbww')

decrypt_process = subprocess.Popen(["python3", vastsysteem_path + "/dencrypt.py", "decrypt", fbww], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
decrypt_output, decrypt_error = decrypt_process.communicate() 
decrypted_text = decrypt_output.decode().strip()

switch = decrypted_text
fbww = switch





font_size = int(config.get('Settings', 'font_size'))
font_type = config.get('Settings', 'font_type')

url = QUrl('https://www.facebook.com')

global mag_factor
mag_factor = 0
        

class MainWindow(QtWidgets.QMainWindow):
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
                config.read( vastsysteem_path + '/Telephone/Contact/contacten.ini')
                # Update the desired values
                config.add_section(str(fbid))
                config.set(fbid, 'naam', str(username))
                config.set(fbid, 'id', str(fbid))
                config.set(fbid, 'type', 'facebook')
                # Save the changes back to the INI file
                with open( vastsysteem_path + '/Telephone/Contact/contacten.ini', 'w') as config_file:
                    config.write(config_file)
                pyautogui.click(200, 300)
                pyautogui.press('home')
                pyautogui.click(950, 891)
                delay_seconds = 1  # 5 seconds
                print('SAVED')
                self.lbltoegevoegd.setText('Opgeslagen!')
                
                # Create a timer to introduce the delay and call the delayed function
                timer = threading.Timer(delay_seconds, lambda: delayed_function())
                timer.start()

                def delayed_function():
                    global screenshot
                    print("ok")
                    screenshot = pyautogui.screenshot()
                    # Define the coordinates for cropping (left, top, right, bottom)
                    crop_coordinates = (700, 212, 1200, 712)
                    
                    
                    #coord x1 : 700, 1200
                    #coord x2 : 212, 712
                    # Perform any other actions with the screenshot here
                    # Crop the screenshot image
                    cropped_image = screenshot.crop(crop_coordinates)
                    
                    
                    cropped_image.save( vastsysteem_path + "/Telephone/Contact/" + fbid + '.png')
                    print("Screenshot captured.")
                    
                    pyautogui.press('esc')
                    
                    
            else:
                print('Niets opgeslagen')
                self.lbltoegevoegd.setText('Niet opgeslagen!')
          
        except Exception as e:
            print("Error:", e)
            self.lbltoegevoegd.setText('Niet opgeslagen!')
            print(e)
    
    def on_load_finished(self, ok): 
        
        if ok:
           
            # JavaScript code to fill in the form fields
            script = """
            function wait(delay) {
                return new Promise(resolve => setTimeout(resolve, delay));
            }
            function vulaccin() {    
                var identifierInput = document.getElementsByName('email')[0];      
                identifierInput.value = '%s';
            }
            function vulwwin() {   
                var passwordInput = document.getElementsByName('pass')[0];
                passwordInput.value = '%s';
            }
            function volgendeclick() {
                var buttons = document.getElementsByTagName('button');
                for (var i = 0; i < buttons.length; i++) {
                    if (buttons[i].textContent.trim() === 'Aanmelden') {
                        buttons[i].click();
                        break;
                    }
                }
            }
            function acceptcookies() {
                var buttons = document.getElementsByTagName('button');
                for (var i = 0; i < buttons.length; i++) {
                    if (buttons[i].textContent.trim() === 'Alle cookies toestaan') {
                        buttons[i].click();
                        break;
                    }
                }
            }
            acceptcookies()
            vulaccin();
            vulwwin();
            volgendeclick();
            
            """ % (fbusername, fbww)
            
            self.browser.page().runJavaScript(script)
            # Inject CSS styles to hide selected elements using JavaScript
            css_selector = '.xb57i2i.x1q594ok.x5lxg6s.x78zum5.xdt5ytf.x6ikm8r.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.x1iyjqo2.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1e4zzel.x1n2onr6.xq1qtft'
            self.browser.page().runJavaScript(f"document.querySelectorAll('{css_selector}').forEach(el => el.style.display = 'none');")         
            css_selector = '.xb57i2i.x1q594ok.x5lxg6s.x78zum5.xdt5ytf.x6ikm8r.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.xx8ngbg.xwo3gff.x1n2onr6.x1oyok0e.x1odjw0f.x1e4zzel.x5yr21d'
            self.browser.page().runJavaScript(f"document.querySelectorAll('{css_selector}').forEach(el => el.style.display = 'none');")       
            css_selector = '.x9f619.x78zum5.x1s65kcs.xixxii4.x13vifvy.xhtitgo.xds687c.x90ctcv.x12dzrxb.xiimyba.xqmrbw9.x1h737yt'
            self.browser.page().runJavaScript(f"document.querySelectorAll('{css_selector}').forEach(el => el.style.display = 'none');")        
            css_selector = '.x6s0dn4.x78zum5.x15zctf7.x1s65kcs.x1n2onr6.x1ja2u2z'
            self.browser.page().runJavaScript(f"document.querySelectorAll('{css_selector}').forEach(el => el.style.display = 'none');")        
            css_selector = '.xuk3077.x78zum5.x1iyjqo2.xl56j7k.x1p8ty84.x1na7pl.x88anuq'
            self.browser.page().runJavaScript(f"document.querySelectorAll('{css_selector}').forEach(el => el.style.display = 'none');")        
            css_selector = '.xds687c.xixxii4.x17qophe.x13vifvy.x1vjfegm'
            self.browser.page().runJavaScript(f"document.querySelectorAll('{css_selector}').forEach(el => el.style.display = 'none');")     
            css_selector = '.x9f619.x1s65kcs.x16xn7b0.xixxii4.x17qophe.x13vifvy.xj35x94.xhtitgo.xkreb8t'
            self.browser.page().runJavaScript(f"document.querySelectorAll('{css_selector}').forEach(el => el.style.display = 'none');")       
            css_selector = '.x78zum5.x1q0g3np.x1a2a7pz'
            self.browser.page().runJavaScript(f"document.querySelectorAll('{css_selector}').forEach(el => el.style.display = 'none');")        
            css_selector = '.x1lliihq.x1k90msu.x2h7rmj.x1qfuztq'
            self.browser.page().runJavaScript(f"document.querySelectorAll('{css_selector}').forEach(el => el.style.display = 'none');")        
            css_selector = '.x1a2a7pz.x1qjc9v5.xnwf7zb.x40j3uw.x1s7lred.x15gyhx8.x9f619.x78zum5.x1fns5xo.x1n2onr6.xh8yej3.x1ba4aug.xmjcpbm'
            self.browser.page().runJavaScript(f"document.querySelectorAll('{css_selector}').forEach(el => el.style.display = 'none');")         
            css_selector = '.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xl56j7k.x1qjc9v5.xozqiw3.x1q0g3np.x1ve1bff.xvo6coq.x2lah0s'
            self.browser.page().runJavaScript(f"document.querySelectorAll('{css_selector}').forEach(el => el.style.display = 'none');")         
            css_selector = '.x1i10hfl.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x1ypdohk.xe8uvvx.x1hl2dhg.xggy1nq.x87ps6o.x1lku1pv.x1a2a7pz.xjyslct.x1qhmfi1.x1a2cdl4.xnhgr82.x1qt0ttw.xgk8upj.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.xquyuld.x9f619.x1lliihq.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x6ikm8r.x10wlt62.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.xh8yej3.x1ja2u2z.xk4oym4'
            self.browser.page().runJavaScript(f"document.querySelectorAll('{css_selector}').forEach(el => el.style.display = 'none');")        
            css_selector = '.x9f619.x1n2onr6.x1ja2u2z.x2bj2ny.x1qpq9i9.xdney7k.xu5ydu1.xt3gfkd.xh8yej3.x6ikm8r.x10wlt62.xquyuld'
            self.browser.page().runJavaScript(f"document.querySelectorAll('{css_selector}').forEach(el => el.style.display = 'none');")
            css_selector = '.x4k7w5x.x1h91t0o.x1h9r5lt.x1jfb8zj.xv2umb2.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1qrby5j'
            self.browser.page().runJavaScript(f"document.querySelectorAll('{css_selector}').forEach(el => el.style.display = 'none');")
           
           
            
    def closeourway(self):
            #os.system("pkill mage")
           # os.system("pkill onboard")
            self.close()
            #subprocess.run(['gsettings', 'set', 'org.gnome.desktop.a11y.magnifier', 'mag-factor', '1.0'], bufsize=0)
    
    def openmage(self):
        if self.mag_factor  == 3:
            self.browser.setZoomFactor(1)
            self.mag_factor = 0
            print('Magnification factor set to 1.0')
        elif self.mag_factor  == 0:
            self.browser.setZoomFactor(2.5)
            self.mag_factor = 3
            print('Magnification factor set to 2.0')
        else:
            print('Unexpected magnification factor:', self.mag_factor)
    def gohome(self):
        print('home')
        self.browser.load(url)
        
    def __init__(self):
        super(MainWindow, self).__init__()
        self.mag_factor = 0
        self.setWindowTitle("Facebook")
        outputstring = "background-color: " + colorcode + ";"
        self.setStyleSheet(outputstring)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(0, #setX
                         0,  #setY
                         screen_width, #Width
                         screen_height) #Height
        
        
        
        self.browser = QWebEngineView()
        self.browser.load(url)
        
        self.browser.loadFinished.connect(self.on_load_finished)
        
        # SLUITKNOP
        self.close_button = QtWidgets.QPushButton("Sluiten", self)
        self.close_button.setFont(QFont(font_type , font_size))
        #close_button.setStyleSheet(f"QPushButton {{ background-color: white; }} ")
        self.close_button.setFixedSize(200, font_size+20)  # Set the size of the close button
        self.close_button.clicked.connect(self.closeourway)
        
        # VERGROOTKNOP
        vergroot_button = QtWidgets.QPushButton("Vergrootglas", self)
        vergroot_button.setFont(QFont( font_type , font_size))
        #vergroot_button.setStyleSheet(f"QPushButton {{ background-color: white; }} ")
        vergroot_button.setFixedSize(350, font_size+20)  # Set the size of the vergroot button
        vergroot_button.clicked.connect(self.openmage)
        
        # HOME
        self.home_button = QtWidgets.QPushButton("HOME", self)
        self.home_button.setFont(QFont( font_type , font_size))
        #vergroot_button.setStyleSheet(f"QPushButton {{ background-color: white; }} ")
        self.home_button.setFixedSize(350, font_size+20)  # Set the size of the vergroot button
        self.home_button.clicked.connect(self.gohome)
        
        #VOEG TOE
        fbAdd_button = QtWidgets.QPushButton("Voeg toe", self)
        fbAdd_button.setFont(QFont(font_type, font_size))
        fbAdd_button.setFixedSize(350, font_size+20)  # Set the size of the voeg toe button
        fbAdd_button.clicked.connect(self.addContact)
        
        
        
        self.lbltoegevoegd = QtWidgets.QLabel("", self)
        self.lbltoegevoegd.setFont(QFont( font_type , font_size))
        self.lbltoegevoegd.setFixedSize(500, font_size+20)
        
#------------LAYOUT----------------

        
        mainlayer = QtWidgets.QVBoxLayout()
        
        lwebview = QtWidgets.QVBoxLayout()
        lh = QtWidgets.QHBoxLayout()
        lh.addWidget(self.close_button)
        lh.addWidget(vergroot_button)
        lh.addWidget(self.home_button)
        lh.setAlignment(Qt.AlignmentFlag.AlignLeft)
        lh.addWidget(fbAdd_button)
        lh.addWidget(self.lbltoegevoegd)
        lwebview.addWidget(self.browser)
        
        mainlayer.addLayout(lh)
        mainlayer.addLayout(lwebview)
        
        

        
        widget = QtWidgets.QWidget()
        widget.setLayout(mainlayer)
        self.setCentralWidget(widget)
        self.browser.setZoomFactor(2.5)
#-------------------------------------
        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()

window.show()
app.exec()