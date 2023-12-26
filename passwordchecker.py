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



global colorcode, fontsize, fonttype, screen_height

config = configparser.ConfigParser()
config.read('/home/meme/VASTSYSTEEM/settings.ini')

colorcode = config.get('Settings', 'colorcode')
fonttype = config.get('Settings', 'font_type')
fontsize = config.get('Settings', 'font_size')
screen_height = config.get('Settings', 'screen_height')
changebgcolor = ("background-color: " + colorcode)


class MainWindow(QMainWindow):

    def __init__(self):
       super(MainWindow, self).__init__()
       self.setWindowTitle("Password")
       self.showFullScreen()
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
       self.txtww.setEchoMode(QLineEdit.Password)
       
       
       
       self.chkww.setFont(QFont(fonttype , int(fontsize)))
       self.chkww.setStyleSheet("QCheckBox::indicator { width: 50px; height: 50px; }")
       self.chkww.clicked.connect(self.print_checkbox_state)
       btnbevestig.setFont(QFont(fonttype , int(fontsize)))
       self.lblcorrect.setFont(QFont(fonttype , int(fontsize)))
       
       
       Htoplayer.addWidget(btnclose , alignment=Qt.AlignTop , stretch=1  )
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
       
       #--------------------definitions--------------------------
       
    def print_checkbox_state(self):
        if self.chkww.isChecked():
            print("Checkbox is checked.")
            self.txtww.setEchoMode(QLineEdit.Normal)
            #self.txtfbww.setEchoMode(QLineEdit.Normal)
        else:
            print("Checkbox is unchecked.")
            self.txtww.setEchoMode(QLineEdit.Password)
            #self.txtfbww.setEchoMode(QLineEdit.Password)
            
    def savestats(self):
        print('Bevestig')
        if self.txtww.text() == "slayer":
            self.lblcorrect.setText('Wachtwoord correct.')
            # If you want to open the 'gevorderd menu', you can do it here.
            #self.close()
        else:
            self.lblcorrect.setText('Wachtwoord niet correct.')


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()


