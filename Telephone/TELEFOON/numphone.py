#!/usr/bin/env python3

import sys
import serial
import time
import configparser
import os
import subprocess
import re

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QTime, QTimer

from PIL.ImageQt import ImageQt
from PIL import Image



# Create a ConfigParser object
config = configparser.ConfigParser()



user_home = os.path.expanduser("~")
global vastsysteem_path
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

# Read the INI file
config.read(vastsysteem_path + '/settings.ini')
pincode = int(config.get('Settings', 'pincode'))

global colorcode
colorcode = config.get('Settings', 'colorcode')
screen_width = int(config.get('Settings', 'screen_width'))
screen_height = int(config.get('Settings', 'screen_height'))
font_type = config.get('Settings', 'font_type')
font_size = int(config.get('Settings', 'font_size'))

bgcolor = ("background-color: " + config.get('Settings', 'colorcode') + ";")

serial_port = '/dev/ttyUSB0'  # Change this to match your serial port
baud_rate = 9600
# Initialize the serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)




class PhoneApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.stream = None
        self.speaker_stream = None

    def initUI(self):
        self.setWindowTitle('Phone App')
        self.setStyleSheet(bgcolor)  # Set the background color
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(0, 0, screen_width, screen_height)  # Set window size

        # Create grid layout for phone buttons
        grid_layout = QGridLayout()

        grid_layout.setRowStretch(0, 0)
        grid_layout.setColumnStretch(0, 0)
        grid_layout.setSpacing(0)
        buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']
        positions = [(i, j) for i in range(4) for j in range(3)]
        for position, button_text in zip(positions, buttons):
            button = QPushButton(button_text)
            button.setFont(QFont(font_type, font_size))
            button.setContentsMargins(0, 0, 0, 0)
            button.setStyleSheet("background-color: black; color: white;")
            button.setFixedSize(200, 100)  # Adjust size as needed
            button.clicked.connect(lambda _, text=button_text: self.btnsend(text))
            grid_layout.addWidget(button, *position)

        
        
        self.call_button = QLabel('')
        im = Image.open(vastsysteem_path+"/icons/neemop.png")
        newsize = (200,200)
        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.call_button.setPixmap(pixmap)
        self.call_button.setMouseTracking(True)
        self.call_button.mousePressEvent = self.call_number

        self.end_call_button = QLabel("Cancel Call")
        im = Image.open(vastsysteem_path+"/icons/legtoe.png")
        newsize = (200,200)

        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.end_call_button.setPixmap(pixmap)
        self.end_call_button.setMouseTracking(True)
        self.end_call_button.mousePressEvent = self.end_call

        self.spacing = QLabel("")
        self.spacing.setFixedWidth(screen_width -450)

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.call_button)
        hbox_layout.addWidget(self.spacing)
        hbox_layout.addWidget(self.end_call_button)

        # Create label for displaying clicked numbers
        self.label = QLabel("Voer het nummer in \n of druk op rood om af te sluiten.")
        self.label.setFont(QFont(font_type, font_size))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nummerlabel = QLabel()
        self.nummerlabel.setText('')
        self.nummerlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nummerlabel.setFont(QFont(font_type, font_size))

        #btndelete
        self.btndelete = QPushButton("Verwijder")
        
        self.btndelete.setFixedWidth(600)
        button.setStyleSheet("background-color: black; color: white;")
        self.btndelete.clicked.connect(self.delete)
        self.btndelete.setFont(QFont(font_type, font_size))
        self.btndelete.setStyleSheet("background-color: black; color: white;")
        # Create vertical layout to organize the grid, buttons, and label
        
        
        
        vbox_layout = QVBoxLayout()
        vmid = QVBoxLayout()
        vmid.setAlignment(Qt.AlignmentFlag.AlignHCenter |Qt.AlignmentFlag.AlignTop)

        vbox_layout.addWidget(self.label)
        vbox_layout.addWidget(self.nummerlabel)
        
        vmid.addLayout(grid_layout)
        vmid.addWidget(self.btndelete)

        vbox_layout.addLayout(vmid)
        
        vbox_layout.addLayout(hbox_layout)
        
        
        
        
        self.setLayout(vbox_layout)
        self.show()
    
    def delete(self):
        text = self.nummerlabel.text()
        print("string to adjust: ", text)
        if text:
            text = text[:-1] 
            self.nummerlabel.setText(text)
        


    def btnsend(self, button):
        print("send the button ", button)
        text =  self.nummerlabel.text()
        print("ontvangen text", text)
        text = text + button
        print('nieuw: ', text)
        self.nummerlabel.setText(text)
    

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
        self.label.setText("Aan het bellen. \nDuur van het gesprek: \n"+ waarde)


    def call_number(self,event= None):
        number = self.nummerlabel.text()
        if number:
            if number.startswith('0'):
                # Replace the '0' with '+32'
                number = '+32' + number[1:]
                print("International format:", number)
                # Handle the response as needed
                print("Start Gesprek naar:", number)
                try:
                    ser.write(('ATD' + number + ';\r\n').encode())  # Encode the string before writing
                    response = ser.read(100)  # Read response from the module
                    if response:
                        response = response.decode(encoding='latin-1')
                        print('reactie: ',response)
                        self.startklok()
                        
                    else:
                        print("No response received from the device.")
                except serial.serialutil.SerialException as e:
                    print("Serial communication error:", e)
            else:
                # Number doesn't start with '0', it may already be in international format
                print("Nummer is niet geldig: ", number)

    def end_call(self, event=None):
        print("Call denied.")
        ser.write(b'ATH\r\n') 
        # Close serial port
        ser.close()
        # End the current script
        sys.exit()
  

   


def main():
    app = QApplication(sys.argv)
    phone_app = PhoneApp()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()