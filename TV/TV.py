#!/usr/bin/env python3


import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import configparser
import os
import subprocess
from PIL.ImageQt import ImageQt
from PIL import Image

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

config = configparser.ConfigParser()
config.read(vastsysteem_path + '/settings.ini')

colorcode = config.get('Settings', 'colorcode')
screen_width = int(config.get('Settings', 'screen_width'))
screen_height = int(config.get('Settings', 'screen_height'))
font_size = int(config.get('Settings', 'font_size'))
font_type = config.get('Settings', 'font_type')


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        

class MainWindow(QMainWindow):
    def load_images(self):
       folder_path = vastsysteem_path + "/TV/icons"  # Update the folder path here

       if folder_path:
           self.images = []

           for filename in sorted(
               os.listdir(folder_path),
               key=lambda x: os.path.basename(x),  # Sort by file name (alphabetically)
           ):
               if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
                   image_path = os.path.join(folder_path, filename)
                   self.images.append(image_path)

           self.show_current_batch()
           
          
    def goto(self, image_path):
        split = image_path.split('/')
        naam = split[6]  
        split = naam.split('.')
        naam = split[0]
        split = naam.split('_')
        naam = split[1]
        print(naam)
        subprocess.call(["python3",vastsysteem_path + "/TV/TVbrowser.py", naam])
        
        
        
    
  
    def show_current_batch(self):
        image_height = 340
        image_width = 550
    
        # Clear the grid layout before adding new widgets
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)
    
        total_images = len(self.images)
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                image_index = self.current_batch_start + index
                if image_index < total_images:
                    image_path = self.images[image_index]
                    image_label = QLabel(self)
                    pixmap = QPixmap(image_path).scaled(image_width, image_height)
                    image_label.setPixmap(pixmap)
                    image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    image_label.mousePressEvent = lambda event, path=image_path: self.goto(path)
                    self.grid_layout.addWidget(image_label, i, j)
                else:
                    # If there are fewer than 9 images in the current batch, fill the rest with Color widgets
                    color_widget = Color(colorcode)
                    color_widget.setFixedSize(image_width, image_height)# You can change 'red' to any color you want
                    self.grid_layout.addWidget(color_widget, i, j)


    def show_previous_batch(self, event=None):
        if self.current_batch_start > 0:
            self.current_batch_start -= 9
            self.current_batch_end -= 9
            self.grid_layout.deleteLater()
            self.grid_layout = QGridLayout()
            self.create_widgets()
            self.show_current_batch()

    def show_next_batch(self, event=None):
        if self.current_batch_end < len(self.images):
            self.current_batch_start += 9
            self.current_batch_end += 9
            self.grid_layout.deleteLater()
            self.grid_layout = QGridLayout()
            self.create_widgets()
            self.show_current_batch()
        




    def create_widgets(self):
        # CLOSE BUTTON AANMAKEN
        self.close_button = QPushButton("Sluiten", self)
        self.close_button.setFont(QFont(font_type, font_size))
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("background-color: %s;" % colorcode)

        # BACK BUTTON AANMAKEN
        self.path2 = vastsysteem_path + "/icons/arrowleft.png"
        self.back_button = QLabel("", self)
        self.back_button.setFont(QFont(font_type, font_size))
        #self.back_button.clicked.connect(self.show_previous_batch)
        im = Image.open(vastsysteem_path + r"/icons/arrowleft.png") 
        newsize = (115,screen_height-50)
        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.back_button.setPixmap(pixmap)   
        self.back_button.setMouseTracking(True)
        #self.labelUitvoeren.setCursor(Qt.PointingHandCursor)
        # Connect the label's clicked event to the uitvoeren method
        self.back_button.mousePressEvent = self.show_previous_batch
        self.back_button.setStyleSheet("background-color: %s;" % colorcode)

        # FORWARD BUTTON AANMAKEN
        self.path3 = vastsysteem_path + "/icons/arrowright.png"
        self.forward_button = QLabel("", self)
        self.forward_button.setFont(QFont(font_type, font_size))
        #self.forward_button.clicked.connect(self.show_next_batch)
        pixmap = QPixmap(self.path3)
        
        im = Image.open(vastsysteem_path + r"/icons/arrowright.png") 
        newsize = (115,screen_height-50)
        cropped_image = im.resize(newsize)
    
       
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image) 
        
        self.forward_button.setPixmap(pixmap)   
        self.forward_button.setMouseTracking(True)
        #self.labelUitvoeren.setCursor(Qt.PointingHandCursor)
        # Connect the label's clicked event to the uitvoeren method
        self.forward_button.mousePressEvent = self.show_next_batch
       
        self.forward_button.setStyleSheet("background-color: %s;" % colorcode)

        self.grid_layout = QGridLayout()

        lh = QHBoxLayout()
        lh.addStretch()
        lh.addWidget(self.back_button)
        lh.addLayout(self.grid_layout)
        lh.addWidget(self.forward_button)

        lv = QVBoxLayout()
        lv.addWidget(self.close_button)
        lv.addLayout(lh)

        layout = QVBoxLayout()
        layout.addLayout(lv)

        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.showFullScreen()
        self.setWindowTitle("TV and music")

        self.images = []
        self.current_batch_start = 0
        self.current_batch_end = 8

        self.create_widgets()
        self.load_images()

        self.setStyleSheet("background-color: %s;" % colorcode)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
