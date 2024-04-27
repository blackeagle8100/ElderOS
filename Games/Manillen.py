#!/usr/bin/env python3

import os
import sys
from PyQt6.QtCore import QUrl, QTimer, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
import configparser
global harten_count, pieken_count, klavers_count, koeken_count

# Initialize suit counters

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

config = configparser.ConfigParser()
config.read(vastsysteem_path + '/settings.ini')
global colorcode, font_size, font_type, url

colorcode = config.get('Settings', 'colorcode')
font_size = int(config.get('Settings', 'font_size'))
font_type = config.get('Settings', 'font_type')
screen_height = int(config.get('Settings', 'screen_height'))
screen_width = int(config.get('Settings', 'screen_width'))

url = QUrl('https://www.whisthub.com/manille')



class MainWindow(QMainWindow):
    def __init__(self):
        self.troef = [0, 0, 0, 0, 0]
        
        
        super().__init__()
        self.showFullScreen()
        self.setWindowTitle("Manillen")
        outputstring = "background-color: " + colorcode + ";"
        self.setStyleSheet(outputstring)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(0,0,screen_width,screen_height)
        
        # Set up the web view
        self.web_view = QWebEngineView(self)
        self.page_url = url
        self.web_view.loadFinished.connect(self.on_load_finished)
        self.web_view.load(self.page_url)

        # Set up the close button
        self.close_button = QPushButton("Sluiten", self)
        self.close_button.setFont(QFont(font_type, font_size))
        self.close_button.setFixedSize(200, font_size + 20)
        self.close_button.clicked.connect(self.close)
        
        # lbltroef Label
        self.lbltroef = QLabel("", self)
        self.lbltroef.setFont(QFont(font_type, font_size))
        self.lbltroef.setFixedSize(200, 45)
        self.lbltroef.setText('Selecteer troef')
        
        # lbltroeftext Label
        self.lbltroeftext = QLabel("", self)
        self.lbltroeftext.setFont(QFont(font_type, font_size))
        self.lbltroeftext.setFixedSize(200, 45)
        self.lbltroeftext.setText('Troef: ')
        
        #Layout
        layout = QVBoxLayout()
        toplayout = QHBoxLayout()
        toplayout.addWidget(self.close_button)
        toplayout.addStretch() 
        
        toplayout.addWidget(self.lbltroeftext)
        toplayout.addWidget(self.lbltroef)
        layout.addLayout(toplayout)
        layout.addWidget(self.web_view)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_var)
        self.timer.start(5000)
    
    def deletemancss(self):
        elem = '.game > div:nth-child(1) > div:nth-child(1)'
        self.web_view.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = '.game > div:nth-child(2) > div:nth-child(1)'
        self.web_view.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = '.game > div:nth-child(3) > div:nth-child(1)'
        self.web_view.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = '.login'
        self.web_view.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = '.pre > i:nth-child(1)'
        self.web_view.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = '.top-icon'
        self.web_view.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = 'h2.font-cinzel:nth-child(3)'
        self.web_view.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = 'button.flex:nth-child(5)'
        self.web_view.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = '.icon-tools'
        self.web_view.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
    
    def set_auto_zoom(self):
        # Set the zoom level to 100%  
        self.web_view.setZoomFactor(3)
    
    def on_load_finished(self):
        print("Page loaded")
        self.deletemancss()
        self.set_auto_zoom()

    def check_var(self):
        self.web_view.page().runJavaScript('document.querySelectorAll(".choice").length;', self.handle_choice_elements)

    def handle_choice_elements(self, num_elements):
        num_elements = int(num_elements)

        for index in range(1, num_elements + 1):
            self.web_view.page().runJavaScript(f'document.querySelectorAll(".choice")[{index - 1}].innerText;', self.handle_choice_text)

    def handle_choice_text(self, choice_text):
     kleur = 'black'
     try:
       # choice_text = choice_text.strip()
        print(choice_text)
        if 'No trump' in choice_text:
            self.troef[4] = int(self.troef[4]) + 1
            self.jasje = 'Mule'
            kleur = 'black'
        elif '♣' in choice_text: 
            self.troef[0] = int(self.troef[0]) + 1
            self.jasje = '♣'
            kleur = 'black'     
        elif '♦' in choice_text:
            self.troef[1] = int(self.troef[1]) + 1
            self.jasje = '♦'
            kleur = 'red'
        elif '♠' in choice_text:
            self.troef[2] = int(self.troef[2]) + 1
            self.jasje = '♠'
            kleur = 'black'  
        elif '♥' in choice_text:
           # print(choice_text)
            self.jasje = '♥'
            kleur = 'red'
            self.troef[3] = int(self.troef[3]) + 1
        
        print('TROEF OFFICIEEL: ', self.jasje)
        self.lbltroef.setText(self.jasje)
        self.lbltroef.setStyleSheet(f"color: {kleur};")
            
     except Exception as e:
                    print(e)
                    print('error: ' , choice_text)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    window.show()
    sys.exit(app.exec())
