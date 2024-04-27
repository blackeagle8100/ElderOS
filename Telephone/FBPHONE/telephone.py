#!/usr/bin/env python3

import os
import sys
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal
import subprocess
import configparser

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

config = configparser.ConfigParser()
config.read(vastsysteem_path + '/settings.ini')

global colorcode
colorcode = config.get('Settings', 'colorcode')
screen_width = int(config.get('Settings', 'screen_width'))
screen_height = int(config.get('Settings', 'screen_height'))
font_type = config.get('Settings', 'font_type')
font_size = int(config.get('Settings', 'font_size'))



img_size = 1000
label_width = 600


class ContactViewer(QtWidgets.QWidget):
    # Define a custom signal for image clicks
    imageClicked = pyqtSignal(str)  # Add a parameter for image_path

    def __init__(self):
        super().__init__()
        outputstring = ("background-color: " + colorcode + ";")
        self.setStyleSheet(outputstring)

        # Read contacts from contacten.ini file
        self.contacts = []  
        with open(vastsysteem_path + '/Telephone/FBPHONE/Contact/contacten.ini', 'r') as file:
            contact_lines = file.read().split('\n\n')
            for line in contact_lines:
                contact = {}
                for item in line.split('\n'):
                    try:
                        key, value = item.split(' = ')
                        contact[key] = value
                    except ValueError:
                        continue  # Skip lines that don't match expected format
                if contact:
                    self.contacts.append(contact)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Contact Viewer")
        
        self.close_button = QtWidgets.QPushButton("Sluiten")
        self.close_button.setFont(QFont(font_type, font_size))
        self.close_button.clicked.connect(self.close)
        self.close_button.setFixedWidth(screen_width - 20)

        # Create listbox
        self.contact_listbox = QtWidgets.QListWidget()
        self.contact_listbox.setFixedWidth(label_width)
        self.contact_listbox.itemClicked.connect(self.on_select)
        self.contact_listbox.setFont(QFont(font_type, font_size))

        # Populate listbox with contact names
        for contact in self.contacts:
            name = contact['naam']
            self.contact_listbox.addItem(name)

        # Create image display area
        self.image_label = QtWidgets.QLabel()
        self.image_label.setFixedSize(img_size, img_size)

        # Create layout and add widgets
        closebtnlo = QtWidgets.QHBoxLayout()
        MainLayout = QtWidgets.QVBoxLayout()
        closebtnlo.addWidget(self.close_button)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.contact_listbox)
        layout.addWidget(self.image_label)
        MainLayout.addLayout(closebtnlo)
        MainLayout.addLayout(layout)

        self.setLayout(MainLayout)

    def on_select(self, item):
        selected_index = self.contact_listbox.currentRow()
        selected_contact = self.contacts[selected_index]
        image_path = f"{vastsysteem_path}/Telephone/FBPHONE/Contact/{selected_contact['id']}.png"
        image = QtGui.QPixmap(image_path)
        self.image_label.setPixmap(image.scaled(img_size, img_size))

    def emit_image_clicked(self, event):
        selected_index = self.contact_listbox.currentRow()
        selected_contact = self.contacts[selected_index]
        image_id = selected_contact['id']
        
        self.imageClicked.emit(image_id)

    def startcall(self, image_id):
        subprocess.Popen(["python3", vastsysteem_path + "/LOADING.py", "15"])
        print('bellen naar:', image_id)
        call_url = f"https://www.facebook.com/groupcall/ROOM:/?call_id=&has_video=true&initialize_video=true&users_to_ring[0]={image_id}&use_joining_context=true&peer_id={image_id}"
        print(call_url)
        subprocess.call(["python3", vastsysteem_path + "/Telephone/FBPHONE/side.py", call_url])
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ContactViewer()

    # Connect the imageClicked signal to the startcall function
    window.imageClicked.connect(window.startcall)

    # Set the mousePressEvent of the image_label to emit the imageClicked signal
    window.image_label.mousePressEvent = window.emit_image_clicked

    window.showFullScreen()
    sys.exit(app.exec())
