#!/usr/bin/env python3

import os
import sys
import configparser
import pyautogui
import psutil
import subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QCheckBox, QFrame, QWidget
)


user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

screen_width, screen_height = pyautogui.size()

filename = 'settings.ini'
filepath = os.path.join(vastsysteem_path, filename)
config = configparser.ConfigParser()
config.read('settings.ini')
if not os.path.isfile(filepath):
 if 'Settings' not in config:
    basecolor = '#D38DB3'
    config.add_section('Settings')
    config.set('Settings', 'colorcode', str(basecolor))
    config.set('Settings', 'fblogin', 'O2pRozvVW9hl5VhTBbJxAxJp0sbHtCdjDEVNTA69F1M=' )
    config.set('Settings', 'fbww', 'O2pRozvVW9hl5VhTBbJxAxJp0sbHtCdjDEVNTA69F1M=')
    config.set('Settings', 'glogin', 'O2pRozvVW9hl5VhTBbJxAxJp0sbHtCdjDEVNTA69F1M=')
    config.set('Settings', 'gww', 'O2pRozvVW9hl5VhTBbJxAxJp0sbHtCdjDEVNTA69F1M=')  
    config.set('Settings', 'screen_width', str(screen_width))
    config.set('Settings', 'screen_height', str(screen_height))
    config.set('Settings', 'font_type', 'Arial black')
    config.set('Settings', 'font_size', '30')
    with open(filepath, 'w') as config_file:
       config.write(config_file)

global colorcode, changebgcolor, fblogin, fbww, glogin, gww, fontsize, fonttype
global crypterpath
crypterpath = "dencrypt.py"

colorcode = config.get('Settings', 'colorcode')
changebgcolor = ("background-color: " + colorcode)
fblogin = config.get('Settings', 'fblogin')
fbww = config.get('Settings', 'fbww')
glogin = config.get('Settings', 'glogin')
gww = config.get('Settings', 'gww')
fontsize = int(config.get('Settings', 'font_size'))
fonttype = config.get('Settings', 'font_type')


class MainWindow(QMainWindow):

    def __init__(self):
       super(MainWindow, self).__init__()
       self.setWindowTitle("Settings")
       self.showFullScreen()
       self.setStyleSheet(changebgcolor)
       
       #GUI INTERFACE SETTUP
       MainLayer = QVBoxLayout()
       Htoplayer = QHBoxLayout()
   
       
    
       settingkleur = QHBoxLayout()
       fbsettings = QVBoxLayout()
       goosettings = QVBoxLayout()
       buttonsavelayer = QVBoxLayout()
       settingsHlayer1 = QHBoxLayout()
       settingsHlayer2 = QHBoxLayout()
       settingsVlayer = QVBoxLayout()
       btnclose = QPushButton("Sluiten", self)
       btnclose.setFont(QFont(fonttype , fontsize))
       Htoplayer.addWidget(btnclose , alignment=Qt.AlignTop , stretch=1  )
       MainLayer.addLayout(Htoplayer)
       
       lblkleur = QLabel("Kleur vensters: ", self)
       lblkleur.setFont(QFont(fonttype , fontsize))
       btnRed = QPushButton("ROOD", self)
       btnBlue = QPushButton("BLAUW", self)
       btnPink = QPushButton("ROZE", self)
       btnGreen = QPushButton("GROEN", self)
       
      
     
       
       btnRed.setMinimumHeight(200)
       btnBlue.setMinimumHeight(200)
       btnPink.setMinimumHeight(200)
       btnGreen.setMinimumHeight(200)
       
       btnRed.setFont(QFont(fonttype , fontsize))
       btnBlue.setFont(QFont(fonttype , fontsize))
       btnPink.setFont(QFont(fonttype , fontsize))
       btnGreen.setFont(QFont(fonttype , fontsize))
       btnRed.setStyleSheet("background-color: #ba7373")
       btnBlue.setStyleSheet("background-color: #739bba")
       btnPink.setStyleSheet("background-color: #D38DB3")
       btnGreen.setStyleSheet("background-color: #68bd7c")
       settingkleur.addWidget(lblkleur)
       settingkleur.addWidget(btnRed)
       settingkleur.addWidget(btnBlue)
       settingkleur.addWidget(btnPink)
       settingkleur.addWidget(btnGreen)
       settingsHlayer1.addLayout(settingkleur)  # Add the settingkleur layout
       settingsVlayer.addLayout(settingsHlayer1)
       
       
       self.lblfbg = QLabel("Facebook-account:")
       self.txtfbg = QLineEdit()
       self.lblfbww = QLabel("Facebook wachtwoord:")
       self.txtfbww = QLineEdit()
       self.box = QCheckBox('Wachtwoorden weergeven')
       self.box.setFont(QFont(fonttype , fontsize))
       self.box.setStyleSheet("QCheckBox::indicator { width: 80px; height: 80px; }")
       self.box.clicked.connect(self.print_checkbox_state)
       self.lblfbg.setFont(QFont(fonttype , fontsize))
       self.txtfbg.setFont(QFont(fonttype , fontsize))
       self.lblfbww.setFont(QFont(fonttype , fontsize))
       self.txtfbww.setFont(QFont(fonttype , fontsize))
       self.lblgooac = QLabel("Google-account:")
       self.txtgooac = QLineEdit()
       self.lblgooww = QLabel("Google wachtwoord:")
       self.txtgooww = QLineEdit()
       self.txtgooww.setEchoMode(QLineEdit.Password)
       self.txtfbww.setEchoMode(QLineEdit.Password)
       self.lblgooac.setFont(QFont(fonttype , fontsize))
       self.txtgooac.setFont(QFont(fonttype , fontsize))
       self.lblgooww.setFont(QFont(fonttype , fontsize))
       self.txtgooww.setFont(QFont(fonttype , fontsize))
       fbsettings.addWidget(self.lblfbg)  
       fbsettings.addWidget(self.txtfbg)
       fbsettings.addWidget(self.lblfbww)
       fbsettings.addWidget(self.txtfbww)
       goosettings.addWidget(self.lblgooac)
       goosettings.addWidget(self.txtgooac)
       goosettings.addWidget(self.lblgooww)
       goosettings.addWidget(self.txtgooww)
       btnSave = QPushButton("Opslaan", self)
       btnSave.setFont(QFont(fonttype , fontsize))
      
       buttonsavelayer.addWidget(self.box)  
       buttonsavelayer.addWidget(btnSave)
       settingsHlayer2.addLayout(fbsettings)
       settingsHlayer2.addLayout(goosettings)
       
       
       settingsHlayer2.addLayout(buttonsavelayer)
       
       separator = QFrame()
       separator.setFrameShape(QFrame.HLine)
       #separator.setFrameShadow(QFrame.Sunken)
       separator.setLineWidth(15)
       
       palette = QPalette()
       pink_color = QColor(0, 0, 0)  # RGB values for pink
       palette.setColor(QPalette.WindowText, pink_color)
       separator.setPalette(palette)
       
       settingsVlayer.addSpacing(100)
       settingsVlayer.addWidget(separator)
       settingsVlayer.addSpacing(100)
       
       
       btngevorderd = QPushButton("Gevorderde instellingen", self)
       btngevorderd.setMinimumHeight(200)
       btngevorderd.setFont(QFont(fonttype , fontsize))
       btngevorderd.clicked.connect(self.gevorderd)
       settingsVlayer.addWidget(btngevorderd)
      
       
       
       settingsVlayer.addLayout(settingsHlayer2)
       MainLayer.addLayout(settingsVlayer)
       widget = QWidget()
       widget.setLayout(MainLayer)
       self.setCentralWidget(widget)
     
       
       decrypt_process = subprocess.Popen(["python3", crypterpath , "decrypt", fblogin], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       decrypt_output, decrypt_error = decrypt_process.communicate() 
       decrypted_text = decrypt_output.decode().strip()
       dcfblogin = decrypted_text
       self.txtfbg.setText(str(dcfblogin))

       decrypt_process = subprocess.Popen(["python3", crypterpath , "decrypt", fbww], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       decrypt_output, decrypt_error = decrypt_process.communicate() 
       decrypted_text = decrypt_output.decode().strip()
       decryptfbww = decrypted_text
       self.txtfbww.setText(str(decryptfbww))
       
       decrypt_process = subprocess.Popen(["python3", crypterpath , "decrypt", glogin], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       decrypt_output, decrypt_error = decrypt_process.communicate() 
       decrypted_text = decrypt_output.decode().strip()
       decryptglogin = decrypted_text
       self.txtgooac.setText(str(decryptglogin))
       
       decrypt_process = subprocess.Popen(["python3", crypterpath, "decrypt", gww], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       decrypt_output, decrypt_error = decrypt_process.communicate() 
       decrypted_text = decrypt_output.decode().strip()
       decryptgww = decrypted_text       
       self.txtgooww.setText(str(decryptgww))
       
       
       
       
#------------ end setup-----------------
#-----------control setup---------------
       btnclose.clicked.connect(self.close)
       btnSave.clicked.connect(self.savestats)   
       btnRed.clicked.connect(self.chred)
       btnBlue.clicked.connect(self.chblue)
       btnPink.clicked.connect(self.chpink)
       btnGreen.clicked.connect(self.chgreen)
#------------end control setup----------
#------------defines--------------------
    def gevorderd(self):
        print('gevorderd')
        subprocess.Popen(['python3', './AdvancedSettings.py'])
    def print_checkbox_state(self):
        if self.box.isChecked():
            print("Checkbox is checked.")
            self.txtgooww.setEchoMode(QLineEdit.Normal)
            self.txtfbww.setEchoMode(QLineEdit.Normal)
        else:
            print("Checkbox is unchecked.")
            self.txtgooww.setEchoMode(QLineEdit.Password)
            self.txtfbww.setEchoMode(QLineEdit.Password)
    def chred(self):
        global colorcode
        print('ROOD!')
        colorcode = '#ba7373'
        changebgcolor = ("background-color: " + colorcode)
        self.setStyleSheet(changebgcolor)
        
    def chblue(self):
        global colorcode
        print('BLAUW!')
        colorcode = '#739bba'
        changebgcolor = ("background-color: " + colorcode)
        self.setStyleSheet(changebgcolor)
       
    def chpink(self):
        global colorcode
        print('ROZE!')
        colorcode = '#D38DB3'
        changebgcolor = ("background-color: " + colorcode)
        self.setStyleSheet(changebgcolor)
       
    def chgreen(self):
        global colorcode
        print('GROEN!')
        colorcode = '#68bd7c'
        changebgcolor = ("background-color: " + colorcode)
        self.setStyleSheet(changebgcolor)
    def savestats(self):
         print('Save statics')
      
         googleac = self.txtgooac.text()    
         googlepswd = self.txtgooww.text()    
         fbacc = self.txtfbg.text()
         fbww = self.txtfbww.text()
         # Update the desired values
         config.set('Settings', 'colorcode', str(colorcode))
    
         encrypt_process = subprocess.Popen(["python3", crypterpath, "encrypt", fbacc], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         encrypt_output, decrypt_error = encrypt_process.communicate() 
         encrypted_text = encrypt_output.decode().strip()
         encryptfblogin = encrypted_text
         config.set('Settings', 'fblogin', str(encryptfblogin))
         
         encrypt_process = subprocess.Popen(["python3", crypterpath, "encrypt", fbww], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         encrypt_output, decrypt_error = encrypt_process.communicate() 
         encrypted_text = encrypt_output.decode().strip()
         cryptfbww = encrypted_text
         config.set('Settings', 'fbww', str(cryptfbww))
         
         encrypt_process = subprocess.Popen(["python3", crypterpath, "encrypt", googleac], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         encrypt_output, decrypt_error = encrypt_process.communicate() 
         encrypted_text = encrypt_output.decode().strip()
         cryptgoogleac = encrypted_text
         config.set('Settings', 'glogin', str(cryptgoogleac))
         
         encrypt_process = subprocess.Popen(["python3", crypterpath, "encrypt", googlepswd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         encrypt_output, decrypt_error = encrypt_process.communicate() 
         encrypted_text = encrypt_output.decode().strip()
         cryptgooglepswd = encrypted_text
         config.set('Settings', 'gww', str(cryptgooglepswd))
         
         config.set('Settings', 'screen_width', str(screen_width))
         config.set('Settings', 'screen_height', str(screen_height))
         config.set('Settings', 'font_type', 'Arial black')
         config.set('Settings', 'font_size', '30')

        # Save the changes back to the INI file
         with open('settings.ini', 'w') as config_file:
            config.write(config_file)
            
            
            
            
            
        #pkill memeos
         command_line_to_kill = "python3 ElderOS.py"
         for process in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
             try:
                 if process.info['cmdline'] and ' '.join(process.info['cmdline']) == command_line_to_kill:
                     # Kill the process with the matching command line
                     process.terminate()
                     print(f"Process with command line '{command_line_to_kill}' has been terminated.")
             except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
               pass

        
        #open ELDEROS
         subprocess.Popen(['python3', 'ElderOS.py'])

         self.close()
         #close settings
         
 
         
                 
        
#------------end defines----------------

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()