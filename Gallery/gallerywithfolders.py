import os
import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import configparser
from PIL.ImageQt import ImageQt
from PIL import Image

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

config = configparser.ConfigParser()
config.read(vastsysteem_path + '/settings.ini')

global colorcode, screen_width, screen_height, font_size, font_type,adjust

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
        self.current_folder_path = None
        self.setStyleSheet("background-color: "+colorcode+";")  # Set background color to black
        self.images = []
        self.current_batch_start = 0
        self.current_batch_end = 8

        self.create_widgets()
        self.load_images()
        self.showFullScreen()
    def create_widgets(self):
        self.grid_layout = QGridLayout()
        adjust = 25
        #self.path2 = "/home/meme/VASTSYSTEEM/icons/arrowleft.png"
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
                file_path = os.path.join(folder_path, filename)
                
                if os.path.isfile(file_path):
                    # If it's a file, check if it's an image file
                    if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
                        self.images.append(file_path)
                elif os.path.isdir(file_path):
                    # If it's a directory, add it to the images list as a special entry
                    self.images.append(file_path + os.path.sep)

            self.show_current_batch()

    def show_current_batch(self):
        image_height = 340
        image_width = 500 # Adjust the image size here
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                image_index = self.current_batch_start + index
                if image_index < len(self.images):
                    item_path = self.images[image_index]

                    if os.path.isfile(item_path):
                        # If it's a file, load the image
                        image_label = QLabel(self)
                        image_label.setPixmap(QPixmap(item_path).scaled(image_width, image_height))
                        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.grid_layout.addWidget(image_label, i, j)
                        image_label.mousePressEvent = self.create_lambda(item_path)
                    elif os.path.isdir(item_path):
                        # If it's a directory, create a button to represent it
                        folder_button = QPushButton(os.path.basename(item_path), self)
                        folder_button.setFont(QFont(font_type, font_size))
                        folder_button.clicked.connect(lambda _, folder=item_path: self.enter_folder(folder))
                        folder_button.setFixedSize(image_width, image_height)
                        self.grid_layout.addWidget(folder_button, i, j)
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

    def create_lambda(self, image_path):
        return lambda event: self.show_image(image_path)
    
    def enter_folder(self, folder_path):
        self.current_folder_path = folder_path
        self.load_images()

    def show_image(self, image_path):
        image_viewer = ImageViewer(image_path, self.images)
        image_viewer.exec()




class ImageViewer(QDialog):
    def resize_window(self, width, height):
        self.setGeometry(0,0  , width, height)

    def __init__(self, image_path, images):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.showFullScreen()
        #self.setWindowFlags(Qt.WindowFlags.FramelessWindowHint)  # Remove window frame
        self.resize_window(1920, 1080)
        outputstring = ("background-color: "+colorcode+";")
        self.setStyleSheet(outputstring)  # Set the background color

        self.images = images
        self.current_index = self.images.index(image_path)
        self.zoom_factor = 1.0

        self.path2 = vastsysteem_path + "/icons/arrowleft.png"
        self.path3 = vastsysteem_path + "/icons/arrowright.png"

        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        #self.setGeometry(QApplication.desktop().availableGeometry())
        

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        top_layout = QHBoxLayout()

        self.close_button = QPushButton("Sluiten", self)
        self.close_button.setFont(QFont(font_type, font_size))
        self.close_button.clicked.connect(self.close)
        #self.close_button.setFixedSize(300, 40) 
        top_layout.addWidget(self.close_button)

        self.rotate_button = QPushButton("Draaien", self)
        self.rotate_button.setFont(QFont(font_type, font_size))
        self.rotate_button.clicked.connect(self.rotate_image)
        #self.rotate_button.setFixedSize(300, 40) 
        top_layout.addWidget(self.rotate_button)

        main_layout.addLayout(top_layout)
        main_layout.addStretch(1)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        button_layout = QHBoxLayout()

        self.back_button = QLabel("", self)
        self.back_button.setFont(QFont(font_type, font_size))
        #self.back_button.clicked.connect(self.show_previous_image)
        #pixmap = QPixmap(self.path2)
        #self.back_button.setIcon(QIcon(pixmap))
        #self.back_button.setIconSize(pixmap.size())
       # self.back_button.setFixedWidth(((screen_width//3)))
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
        #self.graphics_view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.graphics_view.setInteractive(True)
        

        self.next_button = QLabel("", self)
        self.next_button.setFont(QFont(font_type, font_size))
        #self.next_button.clicked.connect(self.show_next_image)
        #pixmap = QPixmap(self.path3)
        #self.next_button.setIcon(QIcon(pixmap))
        #self.next_button.setIconSize(pixmap.size())
        self.next_button.setMouseTracking(True)
        self.next_button.mousePressEvent = self.show_next_image
        im = Image.open(vastsysteem_path + r"/icons/arrowright.png") 
        newsize = (200,screen_height-20)
        cropped_image = im.resize(newsize)
        #angle = 180  # Replace with the desired rotation angle
        #rotated_image = cropped_image.rotate(angle)
        q_image = ImageQt(cropped_image)  # Convert PIL image to QImage
        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap     
        self.next_button.setPixmap(pixmap)

        self.back_button.setFixedSize(int(screen_width / 3)-400, screen_height)
        self.next_button.setFixedSize(int(screen_width / 3)-400, screen_height)
        #self.showFullScreen()

        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.graphics_view)
        button_layout.addWidget(self.next_button)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        self.load_image(image_path)
        #self.showFullScreen()  # Show the dialog in full screen
        
        #self.setGeometry(app.desktop().availableGeometry())
        

    
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
