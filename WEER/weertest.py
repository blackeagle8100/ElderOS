#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QScrollArea
from PyQt6.QtWebEngineWidgets import QWebEngineView
import configparser
import pyautogui
import threading
import time




# Initialize suit counters

config = configparser.ConfigParser()
config.read('/home/meme/VASTSYSTEEM/settings.ini')
global colorcode, font_size, font_type, url

colorcode = config.get('Settings', 'colorcode')
font_size = int(config.get('Settings', 'font_size'))
font_type = config.get('Settings', 'font_type')
screen_width = int(config.get('Settings', 'screen_width'))
screen_height = int(config.get('Settings', 'screen_height'))
url = QUrl('https://www.vrt.be/vrtnws/nl/services/weer/')



class MainWindow(QMainWindow):
    # Function to create a delay
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Weer")
        outputstring = "background-color: " + colorcode + ";"
        self.setStyleSheet(outputstring)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(0, #setX
                         0,  #setY
                         screen_width, #Width
                         screen_height) #Height

        # Set up the web view
        self.web_view = QWebEngineView(self)
        
        self.web_view.enableJavaScript = True
        self.clearCookies()
      
        self.page_url = url
        self.web_view.load(self.page_url)
        self.web_view.loadFinished.connect(self.on_load_finished)
       
        
        
        
        
        # Set up the close button
        self.close_button = QPushButton("Sluiten", self)
        self.close_button.setFont(QFont(font_type, font_size))
        self.close_button.setFixedSize(200, font_size + 20)
        self.close_button.clicked.connect(self.close)
        
        
        


        
        
        layout = QVBoxLayout()
        toplayout = QHBoxLayout()
        toplayout.addWidget(self.close_button)
        toplayout.addStretch() 
        
        layout.addLayout(toplayout)
        layout.addWidget(self.web_view)
        

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
    
    
       
       
    def clearCookies(self):
        self.web_view.page().profile().cookieStore().deleteAllCookies()
    
    
    def deleteCSS(self):
     
        elem = '.vrtnws-page__top-header'
        self.web_view.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = '.vrtnws-page__side-nav'
        self.web_view.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        elem = '.vrtnws-page__footer'
        self.web_view.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        
        elem = '.weather-teaser'
        self.web_view.page().runJavaScript(f"document.querySelectorAll('{elem}').forEach(el => el.style.display = 'none');")
        
    
   
    def set_auto_zoom(self):
        # Set the zoom level to 100%
       
        self.web_view.setZoomFactor(3)
    
    def clickaccepteer(self):
        
        pyautogui.click(1160,800)
    
    def on_load_finished(self):
        def delay_function(seconds):
            print(f"Delaying for {seconds} seconds...")
            time.sleep(seconds) 
            print("Delay completed!")
            
        print("Page loaded")
      
        # Create a thread to delay for 5 seconds
        delay_thread = threading.Thread(target=delay_function, args=(5,))
       
        # Start the thread
        delay_thread.start()
        # Wait for the thread to finish (optional)
        delay_thread.join() 
        
        self.clickaccepteer()
        self.deleteCSS()
      
        
        
        
        self.set_auto_zoom()
        self.set_background_color()
        self.set_scrollbar_stylesheet()
    def set_background_color(self):
    # JavaScript code to change the background color
        js_code = f"""
    var colorcode = '{colorcode}';
    document.body.style.backgroundColor = colorcode;
    """
        self.web_view.page().runJavaScript(js_code)  
    
    def set_scrollbar_stylesheet(self):
        # JavaScript code to replace scrollbar buttons with custom images
        js_code = """
        var style = document.createElement('style');
        style.type = 'text/css';
        style.innerHTML = `
            ::-webkit-scrollbar {
                width: 50px;
                height: 10px;
            }
            
            /* Styles for the vertical scrollbar up and down arrows */
            ::-webkit-scrollbar-button:vertical {
                width: 50px; /* Set the width of the arrow buttons */
                height: 100px; /* Set the height of the arrow buttons */
                background-image: url('/home/meme/VASTSYSTEEM/icons/arrowup200.png'); /* Path to your up arrow image */
                background-repeat: no-repeat;
                background-position: center;
            }
            `;
        document.head.appendChild(style);
        """
        self.web_view.page().runJavaScript(js_code)



        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
