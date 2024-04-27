#!/usr/bin/env python3

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QPixmap, QFont, QColor, QPalette
import os
import sys
import subprocess
import configparser
from PIL.ImageQt import ImageQt
from PIL import Image

# Create a ConfigParser object
config = configparser.ConfigParser()

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

# Read the INI file
config.read(vastsysteem_path + '/settings.ini')
screen_height = int(config.get('Settings', 'screen_height'))
screen_width = int(config.get('Settings', 'screen_width'))
font_type = config.get('Settings', 'font_type')
font_size = int(config.get('Settings', 'font_size'))
colorcode = config.get('Settings', 'colorcode')

vyoutube = int(config.get('Settings', 'vyt')) == 1
vfacebook = int(config.get('Settings', 'vfb')) == 1

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        

class Internet(QMainWindow):
   
    def __init__(self, *args, **kwargs):
        super(Internet, self).__init__(*args, **kwargs)
        self.setWindowTitle("Internet")
        outputstring = ("background-color: " + config.get('Settings', 'colorcode') + ";")
        self.current_batch_start = 0
        self.current_batch_end = 8
        self.enabled_apps = []
        self.create_widgets()
        self.load_images()
        
        
        self.setStyleSheet(outputstring)  # Set the background color
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(0, #setX
                         0,  #setY
                         screen_width, #Width
                         screen_height) #Height
    def create_widgets(self):
        self.close_button = QtWidgets.QPushButton("Sluiten")
        self.close_button.setFont(QFont(font_type, font_size))
        self.close_button.clicked.connect(self.close)
        adjust = 25
        
    #back_button KNOP AANMAKEN
        self.back_button = QLabel("", self)
        self.back_button.setFont(QFont(font_type, font_size))
            
        self.back_button.setFixedWidth(((screen_width // 5) // 2)+adjust)
           #self.back_button.setFixedHeight(screen_height-(font_size*2))
            #pixmap = QPixmap(self.path2)
            #self.back_button.setIcon(QIcon(pixmap))
            #self.back_button.setIconSize(pixmap.size())
        self.back_button.setMouseTracking(True)
        self.back_button.mousePressEvent = self.show_previous_batch
        im = Image.open(vastsysteem_path + r"/icons/arrowleft.png") 
        newsize = (200,screen_height-20)
        cropped_image = im.resize(newsize)
        #angle = 180  # Replace with the desired rotation angle
        #rotated_image = cropped_image.rotate(angle)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.back_button.setPixmap(pixmap)  
    #next_button KNOP AANMAKEN
        self.next_button = QLabel("", self)
        self.next_button.setFont(QFont(font_type, font_size))
        #self.next_button.clicked.connect(self.show_next_batch)
        self.next_button.setFixedWidth(((screen_width // 5) // 2)+adjust)
        #self.next_button.setFixedHeight(screen_height)
        #pixmap = QPixmap(self.path3)
        #self.next_button.setIcon(QIcon(pixmap))
        #self.next_button.setIconSize(pixmap.size())
        self.next_button.setMouseTracking(True)
        self.next_button.mousePressEvent = self.show_next_batch
        im = Image.open(vastsysteem_path + r"/icons/arrowright.png") 
        newsize = (200,screen_height-20)
        cropped_image = im.resize(newsize)
        #angle = 180  # Replace with the desired rotation angle
        #rotated_image = cropped_image.rotate(angle)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.next_button.setPixmap(pixmap) 


    
        #------------------------------------
        #LAYER SETUP
        #-------------------------------------
        mainlayer = QtWidgets.QVBoxLayout()
        toplayer = QtWidgets.QHBoxLayout()
        midlayer = QtWidgets.QHBoxLayout()
        self.grid_layout = QtWidgets.QGridLayout()
                
                
        toplayer.addWidget(self.close_button)
        toplayer.setAlignment(Qt.AlignmentFlag.AlignTop)
                
        #midlayer.addWidget(self.back_button)
        midlayer.addLayout(self.grid_layout)
        #midlayer.addWidget(self.next_button)
                
                
        mainlayer.addLayout(toplayer)
        mainlayer.addLayout(midlayer)
        widget = QWidget()
        widget.setLayout(mainlayer)
        self.setCentralWidget(widget)
        #-------------------------------------------------------
        
       
        
#------------------------------------
# DEF SETUPS
#---------------------------------
    def goto(self, image_path):
        split = image_path.split('/')
        naam = split[6]  
        split = naam.split('.')
        naam = split[0]
        print(naam)
        if naam =='Facebook':
            subprocess.call(["python3",vastsysteem_path + "/Internet/Facebook.py"])
        elif naam == 'Youtube':
            subprocess.call(["python3",vastsysteem_path + "/Internet/Youtube.py"])
        else:
            print('Ik heb geen idee wa je hier wilt mee opstarten: ', naam)
            
    def show_current_batch(self):
        image_height = 340
        image_width = 340
    
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
        
    def load_images(self):
           folder_path = vastsysteem_path + "/Internet/icons"  # Update the folder path here

           if folder_path:
               self.images = []

               for filename in sorted(
                   os.listdir(folder_path),
                   key=lambda x: os.path.basename(x),  # Sort by file name (alphabetically)
               ):
                   if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
                       image_path = os.path.join(folder_path, filename)
                       split = image_path.split('/')
                       naam = split[6]  
                       split = naam.split('.')
                       naam = split[0]
                       if vyoutube == 1 and naam == "Youtube":
                           self.images.append(image_path)
                       if vfacebook == 1 and naam == "Facebook":
                           self.images.append(image_path)
                       
                           
                       

               self.show_current_batch()   
        
        
    
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Internet()
    window.show()
    sys.exit(app.exec())
    