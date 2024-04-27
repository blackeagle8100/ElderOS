#!/usr/bin/env python3

import os
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

import configparser
from PIL import Image
from PIL.ImageQt import ImageQt
import subprocess


user_home = os.path.expanduser("~")
global vastsysteem_path
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

config = configparser.ConfigParser()
config.read(vastsysteem_path + '/settings.ini')

global colorcode
colorcode = config.get('Settings', 'colorcode')
screen_width = int(config.get('Settings', 'screen_width'))
screen_height = int(config.get('Settings', 'screen_height'))
font_type = config.get('Settings', 'font_type')
font_size = int(config.get('Settings', 'font_size'))

bgcolor = ("background-color: " + config.get('Settings', 'colorcode') + ";")



class PhoneScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telefoon")
        self.setStyleSheet(bgcolor)  # Set the background color
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(0, 0, screen_width, screen_height)  # Set window size
        

        self.close_button = QPushButton("Sluiten")
        self.close_button.setFont(QFont(font_type, font_size))
        self.close_button.clicked.connect(self.close)
        self.close_button.setFixedWidth(screen_width - 20)
        
        # Create "numtel" button and head
        image_height = 300
        image_width = 300
        self.lblnumtel = QLabel("Telefoon")
        self.lblnumtel.setFixedWidth(image_width)
        self.lblnumtel.setFont(QFont(font_type, font_size))
        self.lblnumtel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btnnumtel = QLabel(" ", self)
        self.btnnumtel.setFixedSize(image_width , image_height)      
        im = Image.open(vastsysteem_path +"/icons/Telefoon.png") 
        newsize = (image_width, image_height)
        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.btnnumtel.setPixmap(pixmap)
          # Set button size to match the image size
        self.btnnumtel.setMouseTracking(True)
        self.btnnumtel.mousePressEvent = self.numtel

                # Create "Contacten" button
        self.lbltelboek = QLabel("Telefoonboek")
        self.lbltelboek.setFixedWidth(image_width)
        self.lbltelboek.setFont(QFont(font_type, font_size))
        self.lbltelboek.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btncontact = QLabel(" ", self)
        self.btncontact.setFixedSize(image_width , image_height)

        im = Image.open(vastsysteem_path +"/icons/Telefoonboek.png")  
        newsize = (image_width, image_height)
        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.btncontact.setPixmap(pixmap)
          # Set button size to match the image size
        self.btncontact.setMouseTracking(True)
        self.btncontact.mousePressEvent = self.callcontact


       
        # Create "FBCALL" button

        self.lblmessenger = QLabel("Messenger")
        self.lblmessenger.setFixedWidth(image_width)
        self.lblmessenger.setFont(QFont(font_type, font_size))
        self.lblmessenger.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btnfbcall = QLabel(" ", self)
        self.btnfbcall.setFixedSize(image_width , image_height)
        im = Image.open(vastsysteem_path +"/icons/Messenger.png")       
        
        newsize = (image_width, image_height)
        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.btnfbcall.setPixmap(pixmap)
          # Set button size to match the image size
        self.btnfbcall.setMouseTracking(True)
        self.btnfbcall.mousePressEvent = self.fbcall


        main_layout = QVBoxLayout()
      
        closebtnlo = QHBoxLayout()
        heading1 = QHBoxLayout()
        heading2 = QHBoxLayout()
        
        row1  = QHBoxLayout()
        row2 = QHBoxLayout()


        heading1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        heading2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        row1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        row2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        closebtnlo.addWidget(self.close_button)
        row1.addWidget(self.btnnumtel)
        row1.addWidget(self.btncontact)
        heading1.addWidget(self.lblnumtel)
        heading1.addWidget(self.lbltelboek)


        row2.addWidget(self.btnfbcall)
        heading2.addWidget(self.lblmessenger)

        main_layout.addLayout(closebtnlo)
        main_layout.addLayout(heading1)
        main_layout.addLayout(row1)
        main_layout.addLayout(heading2)
        main_layout.addLayout(row2)
        
        self.setLayout(main_layout)



    def fbcall(self, event=None):
        print("Open Facebook Caller")
        subprocess.Popen(["python3", vastsysteem_path+ "/Telephone/FBPHONE/telephone.py"])

    def callcontact(self, event=None):
        print("Open Telefoonboek")
        subprocess.Popen(["python3",vastsysteem_path+ "/Telephone/TELEFOON/telboek.py"])

    def numtel(self, event=None):
        print("Open numtel")
        subprocess.Popen(["python3",vastsysteem_path+ "/Telephone/TELEFOON/numphone.py"])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PhoneScreen()
    window.showFullScreen()
  
    sys.exit(app.exec())
