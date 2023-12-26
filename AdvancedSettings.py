#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 14:15:25 2023

@author: lemmy
"""
import os
import sys
import configparser
import pyautogui
import subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QCheckBox, QFrame, QWidget
)



screen_width, screen_height = pyautogui.size()
directory = '/home/meme/VASTSYSTEEM'
filename = 'settings.ini'
filepath = os.path.join(directory, filename)
config = configparser.ConfigParser()
config.read('settings.ini')
if not os.path.isfile(filepath):
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
    
    config.set('Settings', 'vfb', '1')
    config.set('Settings', 'vtel', '1')
    config.set('Settings', 'vyt', '1')
    config.set('Settings', 'vgal', '1')
    config.set('Settings', 'vtv', '1')
    config.set('Settings', 'vmusic', '1')
    config.set('Settings', 'vgames', '1')
    
    
    with open(filepath, 'w') as config_file:
       config.write(config_file)

global colorcode, changebgcolor, fblogin, fbww, glogin, gww, fontsize, fonttype
global vchkfb, vchktel, vchkyt, vchkgal, vchktv, vchkmusic, vchkgames
global crypterpath
crypterpath = "dencrypt.py"


    

vchkfb = int(config.get('Settings', 'vfb'))
vchktel = int(config.get('Settings', 'vtel'))
vchkyt = int(config.get('Settings', 'vyt'))
vchkgal = int(config.get('Settings', 'vgal'))
vchktv = int(config.get('Settings', 'vtv'))
vchkmusic = int(config.get('Settings', 'vmusic'))
vchkgames = int(config.get('Settings', 'vgames'))



colorcode = config.get('Settings', 'colorcode')
changebgcolor = ("background-color: " + colorcode)
fblogin = config.get('Settings', 'fblogin')
fbww = config.get('Settings', 'fbww')
glogin = config.get('Settings', 'glogin')
gww = config.get('Settings', 'gww')
fontsize = int(config.get('Settings', 'font_size'))
fonttype = config.get('Settings', 'font_type')


class CustomSeparator(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setLineWidth(15)
        palette = QPalette()
        color = QColor(0, 0, 0)  # RGB values for pink
        palette.setColor(QPalette.WindowText, color)
        self.setPalette(palette)
        

class MainWindow(QMainWindow):

    def __init__(self):
       super(MainWindow, self).__init__()
       self.setWindowTitle("Settings")
       self.showFullScreen()
       self.setStyleSheet(changebgcolor)
       
       #GUI INTERFACE SETTUP
       MainLayer = QVBoxLayout()
       Htoplayer = QHBoxLayout()
       menulayer = QHBoxLayout()
       applayer = QVBoxLayout()
       fbsettings = QVBoxLayout()
       goosettings = QVBoxLayout()
       lettergrotelayer = QHBoxLayout()
       lettertypelayer = QHBoxLayout()
       letterlayer = QVBoxLayout()
       savelayer = QHBoxLayout()
       
       
       settingsHlayer2 = QHBoxLayout()
       settingsVlayer = QVBoxLayout()
       btnclose = QPushButton("Sluiten", self)
       btnclose.setFont(QFont(fonttype , fontsize))
       
       self.lblfonttype = QLabel('Font type: ')
       self.lblfontsize = QLabel('Font grootte: ')
       self.txtfonttype = QLineEdit()
       self.txtfonttype.setText(fonttype)
       self.txtfonttype.setReadOnly(True)
       self.txtfontsize = QLineEdit()
       self.txtfontsize.setText(str(fontsize))   
       
       
       self.lblapps = QLabel("Apps in- / uitschakelen:")
       self.lblfbg = QLabel("Facebook-account:")
       self.txtfbg = QLineEdit()
       self.lblfbww = QLabel("Facebook wachtwoord:")
       self.txtfbww = QLineEdit()
       self.box = QCheckBox('Wachtwoorden weergeven')
       
       self.chkfb = QCheckBox('Facebook')
       self.chktel = QCheckBox('Telefoon')
       self.chkyt = QCheckBox('Youtube')
       self.chkgal = QCheckBox('Gallerij')
       self.chktv = QCheckBox('Radio/TV')
       self.chkmusic = QCheckBox('Muziekspeler')
       self.chkgames = QCheckBox('Games')
       
        
       checkbox_size = fontsize + 20
       checkbox_style = f"QCheckBox::indicator {{ width: {checkbox_size}px; height: {checkbox_size}px; }}"
       
       self.chkfb.setFont(QFont(fonttype, fontsize))
       self.chkfb.setStyleSheet(checkbox_style)
      
       self.chkfb.setChecked(vchkfb)
       
       self.chktel.setFont(QFont(fonttype, fontsize))
       self.chktel.setStyleSheet(checkbox_style)
       self.chktel.setChecked(vchktel)
       
       self.chkgal.setFont(QFont(fonttype, fontsize))
       self.chkgal.setStyleSheet(checkbox_style)
       self.chkgal.setChecked(vchkgal)
       
       self.chktv.setFont(QFont(fonttype, fontsize))
       self.chktv.setStyleSheet(checkbox_style)
       self.chktv.setChecked(vchktv)
       
       self.chkyt.setFont(QFont(fonttype, fontsize))
       self.chkyt.setStyleSheet(checkbox_style)
       self.chkyt.setChecked(vchkyt)
       
       self.chkmusic.setFont(QFont(fonttype, fontsize))
       self.chkmusic.setStyleSheet(checkbox_style)
       self.chkmusic.setChecked(vchkmusic)
       
       self.chkgames.setFont(QFont(fonttype, fontsize))
       self.chkgames.setStyleSheet(checkbox_style)
       self.chkgames.setChecked(vchkgames)
       
       self.box.setFont(QFont(fonttype, fontsize))
       self.box.setStyleSheet(checkbox_style)
       self.chkfb.setChecked(vchkfb)
       
       self.box.clicked.connect(self.print_checkbox_state)
       self.lblapps.setFont(QFont(fonttype , fontsize))
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
       
       self.lblfonttype.setFont(QFont(fonttype , fontsize))
       self.lblfontsize.setFont(QFont(fonttype , fontsize))
       self.txtfonttype.setFont(QFont(fonttype , fontsize))
       self.txtfontsize.setFont(QFont(fonttype , fontsize))
       
       self.txtfonttype.setMaximumWidth(300)
       self.txtfontsize.setMaximumWidth(300)
       
       
       
       #-------------CREATE GUI LAYERS
       
       btnSave = QPushButton("Opslaan", self)
       btnSave.setFont(QFont(fonttype , fontsize))
       
       Htoplayer.addWidget(btnclose , alignment=Qt.AlignTop , stretch=1  )
       menulayer.addWidget(self.box)
       savelayer.addWidget(btnSave)
      
       fbsettings.addWidget(self.lblfbg)  
       fbsettings.addWidget(self.txtfbg)
       fbsettings.addWidget(self.lblfbww)
       fbsettings.addWidget(self.txtfbww)
       goosettings.addWidget(self.lblgooac)
       goosettings.addWidget(self.txtgooac)
       goosettings.addWidget(self.lblgooww)
       goosettings.addWidget(self.txtgooww)
       
       settingsHlayer2.addLayout(fbsettings)
       settingsHlayer2.addLayout(goosettings)
       settingsVlayer.addLayout(settingsHlayer2)
       
       applayer.addWidget(self.lblapps)
       applayer.addWidget(self.chkfb)
       applayer.addWidget(self.chktel)
       applayer.addWidget(self.chkyt)
       applayer.addWidget(self.chkgal)
       applayer.addWidget(self.chktv)
       applayer.addWidget(self.chkmusic)
       applayer.addWidget(self.chkgames)
       

      
       
       lettergrotelayer.addWidget(self.lblfontsize, alignment=Qt.AlignRight)
       lettergrotelayer.addWidget(self.txtfontsize, alignment=Qt.AlignLeft)
      
       lettertypelayer.addWidget(self.lblfonttype, alignment=Qt.AlignRight)
       lettertypelayer.addWidget(self.txtfonttype, alignment=Qt.AlignLeft)
       
       letterlayer.addLayout(lettertypelayer)
       letterlayer.addLayout(lettergrotelayer)
       
       
       separator = CustomSeparator()
       separator1 = CustomSeparator()
       separator2 = CustomSeparator()
       separator3 = CustomSeparator()
     
       
       
       MainLayer.addLayout(Htoplayer)
     
       MainLayer.addLayout(menulayer)
       MainLayer.addWidget(separator1)
       MainLayer.addLayout(settingsVlayer)
       MainLayer.addWidget(separator2)
       MainLayer.addLayout(applayer)
       MainLayer.addWidget(separator)
       MainLayer.addLayout(letterlayer)
       MainLayer.addWidget(separator3)
       MainLayer.addLayout(savelayer)
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
     
#------------end control setup----------
#------------defines--------------------
    
    def print_checkbox_state(self):
        if self.box.isChecked():
          
            self.txtgooww.setEchoMode(QLineEdit.Normal)
            self.txtfbww.setEchoMode(QLineEdit.Normal)
        else:
           
            self.txtgooww.setEchoMode(QLineEdit.Password)
            self.txtfbww.setEchoMode(QLineEdit.Password)
   
    def savestats(self):
         print('Save statics')
          #-------------get the values   
         googleac = self.txtgooac.text()    
         googlepswd = self.txtgooww.text()    
         fbacc = self.txtfbg.text()
         fbww = self.txtfbww.text()
         vfontsize = str(self.txtfontsize.text())    #NEEDS TO BE VALIDATED ON INTEGERS
         
         if self.chkfb.isChecked():
             vchkfb = 1 
         else:
             vchkfb = 0
 			
         if self.chktel.isChecked():
                     vchktel = 1 
         else:
                     vchktel = 0
         
         if self.chkyt.isChecked():
                     vchkyt = 1 
         else:
                     vchkyt = 0
         
         if self.chkgal.isChecked():
                     vchkgal = 1 
         else:
                     vchkgal = 0
         
         if self.chktv.isChecked():
                     vchktv = 1 
         else:
                     vchktv = 0
         
         if self.chkmusic.isChecked():
                     vchkmusic = 1 
         else:
                     vchkmusic = 0
         if self.chkgames.isChecked():
                     vchkgames = 1 
         else:
                     vchkgames = 0
        #Validating values
         config.set('Settings', 'vfb', str(vchkfb))
         config.set('Settings', 'vtel', str(vchktel))
         config.set('Settings', 'vyt', str(vchkyt))
         config.set('Settings', 'vgal', str(vchkgal))
         config.set('Settings', 'vtv', str(vchktv))
         config.set('Settings', 'vmusic', str(vchkmusic))
         config.set('Settings', 'vgames', str(vchkgames))
         
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
         config.set('Settings', 'font_size', vfontsize)

        # Save the changes back to the INI file
         with open('settings.ini', 'w') as config_file:
            config.write(config_file)
#------------end defines----------------

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()