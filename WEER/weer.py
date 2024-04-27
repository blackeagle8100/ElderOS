#!/usr/bin/env python3

import sys
from PyQt6.QtCore import QUrl, Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QScrollArea
from PyQt6.QtWebEngineWidgets import QWebEngineView
import configparser
import os
import pyautogui
import subprocess
import time
# Initialize suit counters

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

config = configparser.ConfigParser()
config.read(vastsysteem_path + '/settings.ini')
global colorcode, font_size, font_type, url

colorcode = config.get('Settings', 'colorcode')
font_size = int(config.get('Settings', 'font_size'))
font_type = config.get('Settings', 'font_type')
screen_width = int(config.get('Settings', 'screen_width'))
screen_height = int(config.get('Settings', 'screen_height'))
url = QUrl('https://www.vrt.be/vrtnws/nl/services/weer/')



class MainWindow(QMainWindow):
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
        self.web_view.loadFinished.connect(self.on_load_finished)
        self.web_view.load(self.page_url)
        

        # Set up the close button
        self.close_button = QPushButton("Sluiten", self)
        self.close_button.setFont(QFont(font_type, font_size))
        self.close_button.setFixedSize(200, font_size + 20)
        self.close_button.clicked.connect(self.close)
        
        browser = QWidget()
        browser.setLayout(QVBoxLayout())
        
        playlist_scroll_area = QScrollArea()
        playlist_scroll_area.setWidgetResizable(True)
        playlist_scroll_area.setMinimumHeight(300)
        playlist_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        playlist_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        playlist_scroll_area.setWidget(self.web_view)
     
# Set the stylesheet for the QScrollArea and its contents (playlist)
        
        
        
        playlist_scroll_area.setStyleSheet("""
            /* Styles for the QScrollArea */
          
        /* Styles for the vertical scrollbar up and down arrows */
        QScrollBar::add-line:vertical {
            subcontrol-position: bottom;
            image: url(/home/meme/VASTSYSTEEM/icons/arrowup200.png); /* Replace with the path to your arrow image */
            }
        QScrollBar::sub-line:vertical {
            subcontrol-position: top;
            image: url(/home/meme/VASTSYSTEEM/icons/arrowdown200.png); /* Replace with the path to your arrow image */
            }
        QScrollBar:hoizontal {
        height: 0px; /* Hide the horizontal scrollbar */
    }
                QScrollBar:vertical {
        width: 200px; /* Increase the width of the vertical scrollbar */
    }
    QScrollBar::handle:vertical {
        background : none;
        width: 200px;
    }
   
              
""")
        
        
        browser.layout().addWidget(self.web_view)
        layout = QVBoxLayout()
        toplayout = QHBoxLayout()
        toplayout.addWidget(self.close_button)
        toplayout.addStretch() 
        
        layout.addLayout(toplayout)
        layout.addWidget(self.web_view)
        #layout.addWidget(playlist_scroll_area)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        #playlist_scroll_area.setWidget(central_widget)
        self.setCentralWidget(central_widget)


    
     

        
    def resize_test_element(self):
        # This JavaScript code will be executed on the loaded page
        js_code = """
        var testElement = document.querySelectorAll('a.vrt-weather-widget__map-selector__link:nth-child(1)');
        if (testElement) {
            testElement.style.fontSize = "50px";  // Change the font size as needed
            
        }
        """
        self.web_view.page().runJavaScript(js_code)

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
    
    def on_load_finished(self):
        print("Page loaded")

        
        self.deleteCSS()
  
        self.resize_test_element()
        
        self.set_auto_zoom()
        self.set_background_color()
        
        QTimer.singleShot(2000, self.acceptcookies)
        QTimer.singleShot(4000,self.pushdown)
        
    def pushdown(self):
        print("Down down down")
        pyautogui.press('down', presses=8)
        #subprocess.run(["xdotool","key", "Down"])
        
    def acceptcookies(self):
        print('ik zou nu de cookiesbutton klikken')
        pyautogui.click(500,500)
        pyautogui.press('pagedown')
        time.sleep(0.3)
        pyautogui.click(1500,800)
        print("hopelijk is timing nu wel ok")
        time.sleep(0.3)

       
    def set_background_color(self):
    # JavaScript code to change the background color
        js_code = f"""
    var colorcode = '{colorcode}';
    document.body.style.backgroundColor = colorcode;
    """
        self.web_view.page().runJavaScript(js_code) 
        

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())




