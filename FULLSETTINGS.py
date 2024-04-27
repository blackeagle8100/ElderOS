#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import psutil
import os
import sys
import configparser
import pyautogui
import subprocess
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QCheckBox, QFrame, QWidget
)

   
       
def gevorderd(self):
    print('gevorderd')
    subprocess.Popen(['python3', './AdvancedSettings.py'])

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

  


class CustomSeparator(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setLineWidth(15)
        palette = QPalette()
        color = QColor(0, 0, 0)  # RGB values for pink
        palette.setColor(QPalette.ColorRole.WindowText, color)
        self.setPalette(palette)
        

class PasswordWindow(QMainWindow):
    def __init__(self):
        super(PasswordWindow, self).__init__()
        self.setWindowTitle("Password")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(0,0,screen_width, screen_height)
        self.setStyleSheet(changebgcolor)
        
        #GUI INTERFACE SETUP
        MainLayer = QVBoxLayout()
        Htoplayer = QHBoxLayout()
        PassLayer = QHBoxLayout()
        ButtonLayer = QHBoxLayout()
        
        btnclose = QPushButton("Sluiten", self)
        lblww = QLabel("Wachtwoord: ")
        self.txtww = QLineEdit()
        self.chkww = QCheckBox('Wachtwoord weergeven')
        btnbevestig = QPushButton("Bevestig", self)
        btnbevestig.clicked.connect(self.savestats)
        self.lblcorrect = QLabel('')
        
        
        btnclose.setFont(QFont(fonttype , int(fontsize)))
        lblww.setFont(QFont(fonttype , int(fontsize)))
        self.txtww.setFont(QFont(fonttype , int(fontsize)))
        self.txtww.setEchoMode(QLineEdit.EchoMode.Password)
        
        
        
        self.chkww.setFont(QFont(fonttype , int(fontsize)))
        self.chkww.setStyleSheet("QCheckBox::indicator { width: 50px; height: 50px; }")
        self.chkww.clicked.connect(self.print_checkbox_state)
        btnbevestig.setFont(QFont(fonttype , int(fontsize)))
        self.lblcorrect.setFont(QFont(fonttype , int(fontsize)))
        
        
        Htoplayer.addWidget(btnclose , alignment=Qt.AlignmentFlag.AlignTop , stretch=1  )
        PassLayer.addWidget(lblww)
        PassLayer.addWidget(self.txtww)
        PassLayer.addWidget(self.chkww)
        ButtonLayer.addWidget(btnbevestig)
    
        MainLayer.addLayout(Htoplayer)
        MainLayer.addLayout(PassLayer)
        MainLayer.addLayout(ButtonLayer)
        MainLayer.addWidget(self.lblcorrect)
        calc = int(screen_height)//2
        MainLayer.addSpacing(calc)
        widget = QWidget()
        widget.setLayout(MainLayer)
        self.setCentralWidget(widget)
        #------------button actions----------------
        btnclose.clicked.connect(self.close)
        
        # Your password window code here

    def savestats(self):
             print('Bevestig')
             if self.txtww.text() == "slayer":
                 self.lblcorrect.setText('Wachtwoord correct.')
                 self.hide()
                 advanced_window.show()
                 
                 #self.close()
             else:
                 self.lblcorrect.setText('Wachtwoord niet correct.')
    def print_checkbox_state(self):
        if self.chkww.isChecked():
            print("Checkbox is checked.")
            self.txtww.setEchoMode(QLineEdit.EchoMode.Normal)
            self.txtww.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            print("Checkbox is unchecked.")
            self.txtww.setEchoMode(QLineEdit.EchoMode.Password)
            self.txtww.setEchoMode(QLineEdit.EchoMode.Password)
            
class SettingsWindow(QMainWindow):
    def __init__(self):
        super(SettingsWindow, self).__init__()
     
        self.setWindowTitle("Settings")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(0,0,screen_width,screen_height)
        self.setStyleSheet(changebgcolor)
        
        #GUI INTERFACE SETTUP
        MainLayer = QVBoxLayout()
        Htoplayer = QHBoxLayout()
    
        
     
        settingkleur = QHBoxLayout()
        
     
        buttonsavelayer = QVBoxLayout()
        settingsHlayer1 = QHBoxLayout()
        settingsHlayer2 = QHBoxLayout()
        settingsVlayer = QVBoxLayout()
        btnclose = QPushButton("Sluiten", self)
        btnclose.setFont(QFont(fonttype , fontsize))
        btnclose.setMinimumHeight(200)
        Htoplayer.addWidget(btnclose , alignment=Qt.AlignmentFlag.AlignTop , stretch=1  )
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
        
        btnSave = QPushButton("Opslaan", self)
        btnSave.setMinimumHeight(200)
        btnSave.setFont(QFont(fonttype , fontsize))
        buttonsavelayer.addWidget(btnSave)
        settingsHlayer2.addLayout(buttonsavelayer)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        #separator.setFrameShadow(QFrame.Sunken)
        separator.setLineWidth(15)
        
        palette = QPalette()
        pink_color = QColor(0, 0, 0)  # RGB values for pink
        palette.setColor(QPalette.ColorRole.WindowText, pink_color)
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
         password_window.show()
         self.hide()
    def print_checkbox_state(self):
         if self.box.isChecked():
             print("Checkbox is checked.")
             self.txtgooww.setEchoMode(QLineEdit.EchoMode.Normal)
             self.txtfbww.setEchoMode(QLineEdit.EchoMode.Normal)
         else:
             print("Checkbox is unchecked.")
             self.txtgooww.setEchoMode(QLineEdit.EchoMode.Password)
             self.txtfbww.setEchoMode(QLineEdit.EchoMode.Password)
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
          # Update the desired values
          config.set('Settings', 'colorcode', str(colorcode)) 
          config.set('Settings', 'screen_width', str(screen_width))
          config.set('Settings', 'screen_height', str(screen_height))   
         # Save the changes back to the INI file
          with open('settings.ini', 'w') as config_file:
             config.write(config_file)    
         #pkill memeos
          command_line_to_kill = "python3 MemeOS-autoresize.py"
          for process in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
              try:
                  if process.info['cmdline'] and ' '.join(process.info['cmdline']) == command_line_to_kill:
                      # Kill the process with the matching command line
                      process.terminate()
                      print(f"Process with command line '{command_line_to_kill}' has been terminated.")
              except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
          subprocess.Popen(['python3', 'MemeOS-autoresize.py'])  #open MEMEOS
          self.close() #close settings
class AdvancedWindow(QMainWindow):
    def __init__(self):
        super(AdvancedWindow, self).__init__()
        self.setWindowTitle("Settings")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(0,0,screen_width, screen_height)
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
        self.txtgooww.setEchoMode(QLineEdit.EchoMode.Password)
        self.txtfbww.setEchoMode(QLineEdit.EchoMode.Password)
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
      
        
        Htoplayer.addWidget(btnclose , alignment=Qt.AlignmentFlag.AlignTop , stretch=1  )
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
        

       
        
        lettergrotelayer.addWidget(self.lblfontsize, alignment=Qt.AlignmentFlag.AlignRight)
        lettergrotelayer.addWidget(self.txtfontsize, alignment=Qt.AlignmentFlag.AlignLeft)
       
        lettertypelayer.addWidget(self.lblfonttype, alignment=Qt.AlignmentFlag.AlignRight)
        lettertypelayer.addWidget(self.txtfonttype, alignment=Qt.AlignmentFlag.AlignLeft)
        
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
        
        crypterpath = "dencrypt.py"
        
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
           
             self.txtgooww.setEchoMode(QLineEdit.EchoMode.Normal)
             self.txtfbww.setEchoMode(QLineEdit.EchoMode.Normal)
         else:
            
             self.txtgooww.setEchoMode(QLineEdit.EchoMode.Password)
             self.txtfbww.setEchoMode(QLineEdit.EchoMode.Password)
    
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
          crypterpath = "dencrypt.py"
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
             
        #pkill memeos
          command_line_to_kill = "python3 MemeOS-autoresize.py"
          for process in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
             try:
                 if process.info['cmdline'] and ' '.join(process.info['cmdline']) == command_line_to_kill:
                     # Kill the process with the matching command line
                     process.terminate()
                     print(f"Process with command line '{command_line_to_kill}' has been terminated.")
             except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
               pass
       
          subprocess.Popen(['python3', 'MemeOS-autoresize.py'])  #open MEMEOS
          self.close() #close settings
 #------------end defines--------------
        
 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Read settings from the configuration file
    screen_width, screen_height = pyautogui.size()
    directory = '/home/sbe/VASTSYSTEEM'
    filename = 'settings.ini'
    filepath = os.path.join(directory, filename)
    config = configparser.ConfigParser()
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
        
        with open(filepath, 'w') as config_file:
           config.write(config_file)
    config.read('settings.ini')       
    colorcode = config.get('Settings', 'colorcode')
    changebgcolor = ("background-color: " + colorcode)
    fblogin = config.get('Settings', 'fblogin')
    fbww = config.get('Settings', 'fbww')
    glogin = config.get('Settings', 'glogin')
    gww = config.get('Settings', 'gww')
    fontsize = int(config.get('Settings', 'font_size'))
    fonttype = config.get('Settings', 'font_type')    
    
    vchkfb = int(config.get('Settings', 'vfb'))
    vchktel = int(config.get('Settings', 'vtel'))
    vchkyt = int(config.get('Settings', 'vyt'))
    vchkgal = int(config.get('Settings', 'vgal'))
    vchktv = int(config.get('Settings', 'vtv'))
    vchkmusic = int(config.get('Settings', 'vmusic'))
    vchkgames = int(config.get('Settings', 'vgames'))

    # Create instances of your windows
    password_window = PasswordWindow()
    settings_window = SettingsWindow()
    advanced_window = AdvancedWindow()
    # Show the first window
    password_window.hide() #ok 
    settings_window.show() #ok
    advanced_window.hide()


    sys.exit(app.exec())


