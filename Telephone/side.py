#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import configparser
import subprocess
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextBrowser, QHBoxLayout, QLabel
from PyQt6.QtGui import QFont, QPixmap


import pygame
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

# Read configuration settings
config = configparser.ConfigParser()
config.read(vastsysteem_path + '/settings.ini')
screen_width = int(config.get('Settings', 'screen_width'))
colorcode = config.get('Settings', 'colorcode')
# Create the main application window
class BrowserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.setWindowFlag(Qt.WindowStaysOnTopHint)
        outputstring = ("background-color: " + colorcode + ";")
        self.setStyleSheet(outputstring)
        
        self.initUI()
        self.load_settings()
        self.load_webpage()

    def initUI(self): 
        self.setWindowTitle("MessengerOproep")
        
        self.setGeometry(0, 0, screen_width, 100)
        
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        
        
        
        # Create a vertical layout for the central widget
        layout = QVBoxLayout(self.centralWidget)
        
        self.textBrowser = QTextBrowser()
        #layout.addWidget(self.textBrowser)
        
        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()
        music_layout = QHBoxLayout()
        music_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        
        # Close button
        self.close_button = QPushButton("Sluiten", self)
        self.close_button.clicked.connect(self.close_browser)
        self.close_button.setFixedSize(200, 100)
        button_layout.addWidget(self.close_button)
        
        # Volume control buttons
        self.volume_down_button = QPushButton("-", self)
        self.volume_down_button.setFont(QFont('Arial black', 30))
        self.volume_down_button.clicked.connect(self.volume_down)
        self.volume_down_button.setFixedSize(100, 100)
        music_layout.addWidget(self.volume_down_button)

        self.speaker = QLabel()
        speaker_path = os.path.join(vastsysteem_path + "/icons/Speaker.png")
        pixmap = QPixmap(speaker_path)
        pixmap = pixmap.scaled(100, 100) 
        self.speaker.setPixmap(pixmap)
        music_layout.addWidget(self.speaker)

        self.volume_up_button = QPushButton("+", self)
        self.volume_up_button.setFont(QFont('Arial black', 30))
        self.volume_up_button.clicked.connect(self.volume_up)
        self.volume_up_button.setFixedSize(100, 100)
        music_layout.addWidget(self.volume_up_button)
        button_layout.addLayout(music_layout)
        
        layout.addLayout(button_layout)

        self.load_font_settings()

    def close_browser(self):
        self.close()
        self.driver.quit()
        
        

    def load_settings(self):
        self.colorcode = config.get('Settings', 'colorcode')
        self.fbusername = config.get('Settings', 'fblogin')
        self.fbww = config.get('Settings', 'fbww')
        
        # Decrypt Facebook login information
        self.fbusername = self.decrypt_config_value(self.fbusername)
        self.fbww = self.decrypt_config_value(self.fbww)

    def decrypt_config_value(self, encrypted_value):
        decrypt_process = subprocess.Popen(["python3", vastsysteem_path + "/dencrypt.py", "decrypt", encrypted_value], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        decrypt_output, decrypt_error = decrypt_process.communicate()
        decrypted_text = decrypt_output.decode().strip()
        return decrypted_text

    def volume_up(self):
        current_volume = pygame.mixer.music.get_volume()
        if current_volume < 1.0:
            pygame.mixer.music.set_volume(current_volume + 0.1)

    def volume_down(self):
        current_volume = pygame.mixer.music.get_volume()
        if current_volume > 0.0:
            pygame.mixer.music.set_volume(current_volume - 0.1)
                
    def load_font_settings(self):
        font_type = config.get('Settings', 'font_type')
        font_size = int(config.get('Settings', 'font_size'))

        button_font = QFont(font_type, font_size)
        self.close_button.setFont(button_font)

    def load_webpage(self):
        
        if len(sys.argv) > 1:
            url = sys.argv[1]
            

            self.textBrowser.append(f"URL: {url}")

            firefox_options = Options()
            firefox_options.set_preference("permissions.default.microphone", 1)
            firefox_options.set_preference("permissions.default.camera", 1)
            firefox_options.set_preference("privacy.webrtc.legacyGlobalIndicator", False)

            geckodriver_path = vastsysteem_path + "/geckodriver"
            service = Service(executable_path=geckodriver_path)

            self.driver = webdriver.Firefox(service=service, options=firefox_options)
            self.driver.maximize_window()
            self.driver.get(url)

            try:
                button_text = "Allow all cookies"
                button_element = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{button_text}')]")
                button_element.click()
            except Exception as e:
                print("Error:", e)

            try:
                button_text = "Alle cookies toestaan"
                button_element = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{button_text}')]")
                button_element.click()
            except Exception as e:
                print("Error:", e)

            try:
                username_element = self.driver.find_element(By.ID, "email")
                username_element.send_keys(self.fbusername)
            except Exception as e:
                print("Error:", e)

            try:
                password_element = self.driver.find_element(By.ID, "pass")
                password_element.send_keys(self.fbww)
            except Exception as e:
                print("Error:", e)

            try:
                password_element.send_keys(Keys.RETURN)
            except Exception as e:
                print("Error:", e)
        else:
            self.textBrowser.append("No URL provided.")

def main():
    app = QApplication(sys.argv)
    window = BrowserApp()
    window.activateWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
