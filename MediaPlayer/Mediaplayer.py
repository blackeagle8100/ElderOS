
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 19:47:58 2023

@author: meme
"""

import os
import pygame
from pygame import mixer
from PyQt6.QtCore import Qt, QTime, QTimer, QEventLoop, QSize
from PyQt6.QtGui import QIcon, QColor, QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QPushButton, QLabel, QScrollArea
from mutagen.mp3 import MP3
from PyQt6.QtGui import QPixmap
import configparser
from PIL.ImageQt import ImageQt
from PIL import Image

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the INI file
config.read(vastsysteem_path + '/settings.ini')

global colorcode, tumbsizew, thumbsizeh
colorcode = config.get('Settings', 'colorcode')


tumbsizew = 700
thumbsizeh = 450

class MusicPlayer(QMainWindow):
    def __init__(self):
        
        
        
        super().__init__()
        self.IsPaused = False
        self.setWindowTitle("Music Player")
        #self.setWindowFlags(Qt.FramelessWindowHint)  # Remove window frame
        self.showFullScreen()  # Show in full screen
        outputstring = ("background-color: " + colorcode + ";")
        self.setStyleSheet(outputstring)
        
        
        self.speaker = QLabel()
        speaker_path = os.path.join(vastsysteem_path + "/icons/Speaker.png")
        pixmap = QPixmap(speaker_path)
        pixmap = pixmap.scaled(100, 100) 
        self.speaker.setPixmap(pixmap)
        
        self.playlist = QListWidget()
        self.playlist.setFont(QFont('Arial black', 30))
        self.playlist.currentRowChanged.connect(self.play_selected_song)

        self.time_label = QLabel()

        self.close_button = QPushButton("Sluiten")
        self.close_button.setFont(QFont('Arial black', 30))

        self.play_button = QPushButton("Speel")
        self.play_button.setFont(QFont('Arial black', 30))
        self.play_button.setIcon(QIcon(vastsysteem_path + "/icons/MP/play1.png"))
        self.play_button.setIconSize(QSize(50, 50))  # Adjust the size of the icon as needed
        self.play_button.setStyleSheet("border: none;")  # Remove the border around the icon

        self.stop_button = QPushButton("Stop")
        self.stop_button.setFont(QFont('Arial black', 30))
        self.stop_button.setIcon(QIcon(vastsysteem_path + "/icons/MP/stop.png"))
        self.stop_button.setIconSize(QSize(50, 50))  # Adjust the size of the icon as needed
        self.stop_button.setStyleSheet("border: none;")  # Remove the border around the icon

        self.pause_button = QPushButton("Pauze")
        self.pause_button.setFont(QFont('Arial black', 30))
        self.pause_button.setIcon(QIcon(vastsysteem_path + "/icons/MP/pause.png"))
        self.pause_button.setIconSize(QSize(50, 50))  # Adjust the size of the icon as needed
        self.pause_button.setStyleSheet("border: none;")  # Remove the border around the icon

        self.back_button = QPushButton("Vorige")
        self.back_button.setFont(QFont('Arial black', 30))
        self.back_button.setIcon(QIcon(vastsysteem_path + "/icons/MP/mpback.png"))
        self.back_button.setIconSize(QSize(50, 50))  # Adjust the size of the icon as needed
        self.back_button.setStyleSheet("border: none;")  
        # Remove the border around the icon

        self.next_button = QPushButton("Volgende")
        self.next_button.setFont(QFont('Arial black', 30))
        self.next_button.setIcon(QIcon(vastsysteem_path + "/icons/MP/mpforward.png"))
        self.next_button.setIconSize(QSize(50, 50))  # Adjust the size of the icon as needed
        self.next_button.setStyleSheet("border: none;")  # Remove the border around the icon

        self.volume_up_button = QPushButton("+")
        self.volume_up_button.setFont(QFont('Arial black', 30))
        #self.volume_up_button.setIcon(QIcon("./icons/MP/mpforward.png"))
        #self.volume_up_button.setIconSize(QSize(50, 50))  # Adjust the size of the icon as needed
        #self.volume_up_button.setStyleSheet("border: none;")  # Remove the border around the icon
        

        self.volume_down_button = QPushButton("-")
        self.volume_down_button.setFont(QFont('Arial black', 30))
        #self.volume_down_button.setIcon(QIcon("./icons/MP/mpforward.png"))
        #self.volume_down_button.setIconSize(QSize(50, 50))  # Adjust the size of the icon as needed
        #self.volume_down_button.setStyleSheet("border: none;")  # Remove the border around the icon
        
        
        self.thumbnail_label = QLabel()  # Added thumbnail_label member variable
        self.thumbnail_label.setFixedSize(tumbsizew, thumbsizeh)  # Set fixed size for the thumbnail label
        volume_layout = QHBoxLayout()
        
        control_layout = QHBoxLayout()
        
        volume_layout.addWidget(self.volume_down_button)
        volume_layout.addWidget(self.speaker)
        volume_layout.addWidget(self.volume_up_button)
        volume_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        
        
        control_layout.addWidget(self.back_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.next_button)
        control_layout.addLayout(volume_layout)
        

        center_layout = QVBoxLayout()
        center_layout.addWidget(self.thumbnail_label)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        playlist_scroll_area = QScrollArea()
        playlist_scroll_area.setWidgetResizable(True)
        playlist_scroll_area.setMinimumHeight(400)
        playlist_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        playlist_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        playlist_scroll_area.setWidget(self.playlist)

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
        QScrollBar:horizontal {
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

                                     

        
        layout = QVBoxLayout()
        layout.addWidget(self.close_button)
        layout.addLayout(control_layout)
        layout.addLayout(center_layout)
        layout.addWidget(playlist_scroll_area)
        layout.addWidget(self.time_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.load_music()

        self.play_button.clicked.connect(self.play_music)
        self.stop_button.clicked.connect(self.stop_music)
        self.pause_button.clicked.connect(self.pause_music)
        self.back_button.clicked.connect(self.back_music)
        self.next_button.clicked.connect(self.next_music)
        self.close_button.clicked.connect(self.close)
        self.volume_up_button.clicked.connect(self.volume_up)
        self.volume_down_button.clicked.connect(self.volume_down)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_progress)

        self.current_song = None
        self.current_song_duration = 0

        # Set up the end event for music playback
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

    def closeEvent(self, event):
        self.stop_music()
        event.accept()

    def load_music(self):
        music_dir = user_home + "/Muziek"
        for filename in os.listdir(music_dir):
            if filename.endswith(".mp3"):
                item_text = os.path.splitext(filename)[0]  # Remove the file extension
                item = QListWidgetItem(item_text)
                self.playlist.addItem(item)

    def play_selected_song(self, row):
        filename = self.playlist.item(row).text()
        filename_with_extension = f"{filename}.mp3"  # Add the file extension back
        filepath = os.path.join(user_home + "/Muziek", filename_with_extension)

        if self.current_song:
            pygame.mixer.music.stop()

        pygame.mixer.music.load(filepath)
        self.current_song_duration = self.get_current_song_duration()

        self.time_label.setText("")
        pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set the end event for music playback

        # Load and display the thumbnail image
        directory = user_home + '/Muziek/CDHOES'
        if not os.path.exists(directory):
            
                # Create the directory if it doesn't exist
                os.makedirs(directory)
                
                
        thumbnail_path = os.path.join(user_home + "/Muziek/CDHOES", f"{filename}.jpg")
       
        
        
        pixmap = QPixmap(thumbnail_path)
        pixmap = pixmap.scaled(tumbsizew, thumbsizeh) 
        self.thumbnail_label.setPixmap(pixmap)

        self.play_music()  # Start playing the selected song

    def play_music(self):
        if self.IsPaused == True:
            pygame.mixer.music.unpause()
            self.IsPaused = False
            self.timer.start()  # Restart the timer
        else:
            current_row = self.playlist.currentRow()
            if current_row == -1:  # If no song is selected, play the first song in the list
                current_row = 0
                self.playlist.setCurrentRow(current_row)
                self.play_selected_song(current_row)
            pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set the end event for music playback
            pygame.mixer.music.play()
            self.timer.start()

    def stop_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.timer.stop()

    def pause_music(self):
        if self.IsPaused == False:
            pygame.mixer.music.pause()
            self.IsPaused = True
            self.timer.stop()

    def back_music(self):
        current_row = self.playlist.currentRow()
        if current_row > 0:
            self.playlist.setCurrentRow(current_row - 1)
            self.play_selected_song(current_row - 1)
            pygame.mixer.music.play()
            self.timer.start()
            

    def next_music(self):
        current_row = self.playlist.currentRow()
        if current_row < self.playlist.count() - 1:
            self.playlist.setCurrentRow(current_row + 1)
            self.play_selected_song(current_row + 1)
            pygame.mixer.music.play()
            self.timer.start()
            pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set the end event for music playback

    def update_progress(self):
        current_time = QTime(0, 0).addSecs(pygame.mixer.music.get_pos() // 1000)
        duration_time = QTime(0, 0).addSecs(self.current_song_duration)

        if current_time >= duration_time:
            self.timer.stop()
            self.next_music()  # Start playing the next song

        time_text = f"{current_time.toString('mm:ss')} / {duration_time.toString('mm:ss')}"
        self.time_label.setText(time_text)

    def get_current_song_duration(self):
        current_row = self.playlist.currentRow()
        filename = self.playlist.item(current_row).text()
        filename_with_extension = f"{filename}.mp3"
        filepath = os.path.join(user_home + "/Muziek", filename_with_extension)

        audio = MP3(filepath)
        return int(audio.info.length)

    def volume_up(self):
        current_volume = pygame.mixer.music.get_volume()
        if current_volume < 1.0:
            pygame.mixer.music.set_volume(current_volume + 0.1)

    def volume_down(self):
        current_volume = pygame.mixer.music.get_volume()
        if current_volume > 0.0:
            pygame.mixer.music.set_volume(current_volume - 0.1)


if __name__ == "__main__":
    pygame.mixer.init()
    app = QApplication([])
    music_player = MusicPlayer()
    music_player.show()
    app.exec()
