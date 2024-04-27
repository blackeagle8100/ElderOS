#!/usr/bin/env python3

import os
import sys
from PyQt6.QtWidgets import (
    QWidget, QMainWindow, QLabel, QGridLayout, QPushButton, QVBoxLayout, 
    QHBoxLayout, QDialog, QGraphicsView, QGraphicsScene, QApplication)
from PyQt6.QtGui import QPalette, QColor, QFont, QPixmap, QTransform
from PyQt6.QtCore import Qt, QRectF
import configparser
from PIL.ImageQt import ImageQt
from PIL import Image

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

config = configparser.ConfigParser()
config.read(vastsysteem_path + '/settings.ini')

global colorcode, screen_width, screen_height, font_size, font_type


colorcode = str(config.get('Settings', 'colorcode'))
screen_width = int(config.get('Settings', 'screen_width'))
screen_height = int(config.get('Settings', 'screen_height')) 
font_size = int(config.get('Settings', 'font_size'))
font_type = str(config.get('Settings', 'font_type')) 
adjust = 25


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


#-----------------------------------MAINMENU-------------------------
class PhotoGallery(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Gallery")
        self.setGeometry(0,0,screen_width,screen_height)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        #self.showFullScreen()
        self.setStyleSheet("background-color: "+colorcode+";")  # Set background color to colorcode
        self.images = []
        self.current_batch_start = 0
        self.current_batch_end = 8

        self.create_widgets()
        self.load_images()

    def create_widgets(self):
        self.grid_layout = QGridLayout()
        adjust = 25
        self.path3 = vastsysteem_path + "/icons/arrowright.png"

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
#SLUITEN KNOP AANMAKEN
        self.close_button = QPushButton("Sluiten", self)
        self.close_button.setFont(QFont(font_type, font_size))
        self.close_button.clicked.connect(self.close)
        self.close_button.setFixedHeight(font_size * 2)
        
#back_button KNOP AANMAKEN
        self.back_button = QLabel("", self)
        self.back_button.setFont(QFont(font_type, font_size))
        self.back_button.setFixedWidth(((screen_width // 5) // 2)+adjust)
        self.back_button.setMouseTracking(True)
        self.back_button.mousePressEvent = self.show_previous_batch
        im = Image.open(vastsysteem_path + r"/icons/arrowleft.png") 
        newsize = (200,screen_height-20)
        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.back_button.setPixmap(pixmap)  
        
#next_button KNOP AANMAKEN
        self.next_button = QLabel("", self)
        self.next_button.setFont(QFont(font_type, font_size))
        
        self.next_button.setFixedWidth(((screen_width // 5) // 2)+adjust)
        self.next_button.setMouseTracking(True)
        self.next_button.mousePressEvent = self.show_next_batch
        im = Image.open(vastsysteem_path + r"/icons/arrowright.png") 
        newsize = (200,screen_height-20)
        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.next_button.setPixmap(pixmap)
        
        
#LAYOUT SETUP
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.close_button)

        main_layout.addLayout(top_layout)
        main_layout.addStretch()
        
        middle_layout = QHBoxLayout()
        middle_layout.setContentsMargins(0, 0, 0, 0)
        middle_layout.setSpacing(0)

        #middle_layout.addStretch()
        middle_layout.addWidget(self.back_button)
        middle_layout.addLayout(self.grid_layout)
        middle_layout.addWidget(self.next_button, stretch=1)
        #middle_layout.addStretch()
        main_layout.addLayout(middle_layout)
        main_layout.addStretch()
        
        
       
    def load_images(self):
        folder_path = user_home + "/Afbeeldingen"  # Update the folder path here

        if folder_path:
            self.images = []

            for filename in sorted(
                os.listdir(folder_path),
                key=lambda x: os.path.getmtime(os.path.join(folder_path, x)),
                reverse=True,
            ):
                if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
                    image_path = os.path.join(folder_path, filename)
                    self.images.append(image_path)

            self.show_current_batch()

    def show_current_batch(self):
        image_height = 340
        image_width = 500 # Adjust the image size here
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                image_index = self.current_batch_start + index
                if image_index < len(self.images):
                    image_path = self.images[image_index]
                    image_label = QLabel(self)
                    image_label.setPixmap(QPixmap(image_path).scaled(image_width,image_height ))
                    image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.grid_layout.addWidget(image_label, i, j)
                    image_label.mousePressEvent = self.create_lambda(image_path)
                else:
                    # If there are fewer than 9 images in the current batch, fill the rest with Color widgets
                    color_widget = Color(colorcode)
                    color_widget.setFixedSize(image_width, image_height)# You can change 'colorcode' to any color you want
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

    def create_lambda(self, image_path):
        return lambda event: self.show_image(image_path)

    def show_image(self, image_path):
        image_viewer = ImageViewer(image_path, self.images)
        image_viewer.exec()




class ImageViewer(QDialog):
    
    def __init__(self, image_path, images):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setGeometry(0,0,screen_width, screen_height)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        #self.showFullScreen()
        outputstring = ("background-color: "+colorcode+";")
        self.setStyleSheet(outputstring)  # Set the background color

        self.images = images
        self.current_index = self.images.index(image_path)
        self.zoom_factor = 1.0

        self.path2 = vastsysteem_path + "/icons/arrowleft.png"
        self.path3 = vastsysteem_path + "/icons/arrowright.png"
        
        self.close_button = QPushButton("Sluiten", self)
        self.close_button.setFont(QFont(font_type, font_size))
        self.close_button.clicked.connect(self.close)

        self.rotate_button = QPushButton("Draaien", self)
        self.rotate_button.setFont(QFont(font_type, font_size))
        self.rotate_button.clicked.connect(self.rotate_image)

        


        self.back_button = QLabel("", self)
        self.back_button.setFont(QFont(font_type, font_size))
        self.back_button.setMouseTracking(True)
        self.back_button.mousePressEvent = self.show_previous_image

        im = Image.open(vastsysteem_path + r"/icons/arrowleft.png") 
        newsize = (200,screen_height-20)
        cropped_image = im.resize(newsize)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.back_button.setPixmap(pixmap)  
       

        self.graphics_view = QGraphicsView(self)
        self.graphics_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)
        
         # Enable drag and drop
      
        self.graphics_view.setInteractive(True)
        

        self.next_button = QLabel("", self)
        self.next_button.setFont(QFont(font_type, font_size))
        self.next_button.setMouseTracking(True)
        self.next_button.mousePressEvent = self.show_next_image
        im = Image.open(vastsysteem_path + r"/icons/arrowright.png") 
        newsize = (200,screen_height-20)
        cropped_image = im.resize(newsize)
       
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.next_button.setPixmap(pixmap)

        self.back_button.setFixedSize(int(screen_width / 3)-400, screen_height)
        self.next_button.setFixedSize(int(screen_width / 3)-400, screen_height)
    
        #LAYOUT
        
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        top_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        main_layout.addLayout(top_layout)
        main_layout.addStretch(1)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        

        top_layout.addWidget(self.close_button)
        top_layout.addWidget(self.rotate_button)
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.graphics_view)
        button_layout.addWidget(self.next_button)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()


        self.load_image(image_path)

        
        
    #definitions
    
    def show_previous_image(self, event=None):
        if self.current_index > 0:
            self.current_index -= 1
            image_path = self.images[self.current_index]
            self.load_image(image_path)

    def show_next_image(self, event=None):
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            image_path = self.images[self.current_index]
            self.load_image(image_path)

    def load_image(self, image_path):
        image = QPixmap(image_path)
        scaled_image = image.scaled(screen_height, screen_width, Qt.AspectRatioMode.KeepAspectRatio)
        self.graphics_scene.clear()
        self.graphics_scene.addPixmap(scaled_image)
        self.graphics_view.setSceneRect(QRectF(scaled_image.rect()))
        self.graphics_view.resetTransform()

    def rotate_image(self):
        self.graphics_view.rotate(90)

    def wheelEvent(self, event):
        # Zoom in or out based on the scroll wheel delta
        zoom_delta = event.angleDelta().y() / 120  # Normalize the delta value
        zoom_factor_change = 0.1  # Amount to change the zoom factor

        if zoom_delta > 0:
            self.zoom_factor += zoom_factor_change
        else:
            self.zoom_factor -= zoom_factor_change
            if self.zoom_factor < zoom_factor_change:
                self.zoom_factor = zoom_factor_change
        self.graphics_view.setTransform(QTransform().scale(self.zoom_factor, self.zoom_factor))




app = QApplication([])
window = PhotoGallery()
window.show()
sys.exit(app.exec())
