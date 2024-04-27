#!/usr/bin/env python3



from PyQt6.QtWidgets import QGridLayout, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolButton
from PyQt6.QtCore import Qt, QEvent, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
import sys
import subprocess
import configparser
import time
import os
import pygame


pygame.init()
config = configparser.ConfigParser()
user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM/")
AIaudio_path = os.path.join(vastsysteem_path, "UsefullPrograms/SOUNDS/AIsounds/")
config.read(vastsysteem_path + '/settings.ini')
font_size = int(config.get('Settings', 'font_size'))
font_type = str(config.get('Settings', 'font_type'))

functies= ["MUZIEK",
           "MESSENGER",
           "WEER",
           "SPELEN-GAMES",
           "TV-RADIO",
           "GALLERIJ",
           'INSTELLINGEN',
           'INTERNET'
           ]
functiesuitleg = ["De Muziekspeler",
                  "Messenger telefoon",
                  "Weer-app",
                  "Open Spelletjes menu",
                  "Open je TV/Radio",
                  "Open je FOTOS",
                  "Open je instellingen",
                  "Open Internet Menu"
                  ]
speakers = []

class ClickableLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, function_name, parent=None):
        super().__init__(parent)
        self.function_name = function_name
       

    def mousePressEvent(self, event):
        self.clicked.emit(self.function_name)

class MainWindow(QMainWindow):    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("HELP")
        self.showFullScreen()
        outputstring = ("background-color: " + config.get('Settings', 'colorcode') + ";")
        self.setStyleSheet(outputstring)  # Set the background color

        self.btnsluiten = QToolButton(self)
        self.btnsluiten.setText("Sluiten")
        self.btnsluiten.setFont(QFont(font_type, font_size))
        self.btnsluiten.setFixedSize(200, font_size + 20)
        self.btnsluiten.clicked.connect(self.close)
        



        # Create layouts
        lichaam = QVBoxLayout()
        hoofd = QVBoxLayout()
        romp = QHBoxLayout()
        self.rompgrid = QGridLayout()
        voeten = QHBoxLayout()

        # Create labels
        lblheading = QLabel("Help functies")
        lblheading2 = QLabel("Gebruik 1 van de onderstaande functies of stel een andere vraag:")
        outputstring = f"font: {font_size}pt {config.get('Settings', 'font_type')}; font-weight: bold; color: black; background-color: {config.get('Settings', 'colorcode')};"


        lblheading.setStyleSheet(outputstring)
        lblheading2.setStyleSheet(outputstring)

        # Create icons
        size = 100        
        for function_name in functies:
            speaker = ClickableLabel(function_name)            
            speaker.setFixedSize(size, size)
            speaker.setStyleSheet("border: 1px solid black;")
            speaker.setPixmap(QPixmap("./icons/Speaker.png").scaled(size, size, Qt.AspectRatioMode.IgnoreAspectRatio))
            speaker.setMouseTracking(True)
            speaker.clicked.connect(self.speak)
            #speaker.mousePressEvent = self.speak(function_name)
            speakers.append(speaker)
        
        # Add labels and icons to the grid layout
        for i, (function_name, function_uitleg, speaker) in enumerate(zip(functies, functiesuitleg, speakers)):
            label = QLabel(function_name)
            label.setStyleSheet(outputstring)
            labeluitleg = QLabel(function_uitleg)
            labeluitleg.setStyleSheet(outputstring)

            self.rompgrid.addWidget(speaker, i, 0)
            self.rompgrid.addWidget(label, i, 1)
            self.rompgrid.addWidget(labeluitleg, i, 2)

        # Set up button icons
        btnVorige = QLabel()
        btnVolgende = QLabel()
        arrowheight = 550
        arrowwidth = 200
        btnVorige.setFixedSize(arrowwidth, arrowheight)
        btnVolgende.setFixedSize(arrowwidth, arrowheight)

        btnVorige.setPixmap(QPixmap("./icons/arrowleft.png").scaled(arrowwidth, arrowheight, Qt.AspectRatioMode.IgnoreAspectRatio))
        btnVolgende.setPixmap(QPixmap("./icons/arrowright.png").scaled(arrowwidth, arrowheight, Qt.AspectRatioMode.IgnoreAspectRatio))

        btnVolgende.setMouseTracking(True)
        btnVolgende.mousePressEvent = self.volgende
        btnVorige.setMouseTracking(True)
        btnVorige.mousePressEvent = self.vorige

        # Set up "Vraag me" and "Vraag een ander" icons
        iconsize = 300
        vraagme_icon = QLabel()
        vraagme_icon.setFixedSize(iconsize, iconsize)
        vraagme_icon.setPixmap(QPixmap("./icons/vraagmij.png").scaled(iconsize, iconsize, Qt.AspectRatioMode.IgnoreAspectRatio))
        vraagme_icon.setMouseTracking(True)
        vraagme_icon.mousePressEvent = self.vraagmij

        vraagander_icon = QLabel()
        vraagander_icon.setFixedSize(iconsize, iconsize)
        vraagander_icon.setPixmap(QPixmap("./icons/anderevraag.png").scaled(iconsize, iconsize, Qt.AspectRatioMode.IgnoreAspectRatio))
        vraagander_icon.setMouseTracking(True)
        vraagander_icon.mousePressEvent = self.vraagander

        # Add widgets to layouts
        hoofd.addWidget(self.btnsluiten, alignment = Qt.AlignmentFlag.AlignLeft)
        hoofd.addWidget(lblheading, alignment=Qt.AlignmentFlag.AlignHCenter)
        hoofd.addWidget(lblheading2, alignment=Qt.AlignmentFlag.AlignHCenter)
        romp.addWidget(btnVorige)
        romp.addLayout(self.rompgrid)
        romp.addWidget(btnVolgende)
        voeten.addWidget(vraagme_icon, alignment=Qt.AlignmentFlag.AlignHCenter)
        voeten.addWidget(vraagander_icon, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Set layout
        lichaam.addLayout(hoofd)
        lichaam.addLayout(romp)
        lichaam.addLayout(voeten)

        widget = QWidget()
        widget.setLayout(lichaam)
        self.setCentralWidget(widget)
        self.current_row = 0  # Variabele om huidige rij bij te houden
        self.update_grid_display()

        sound_path = (AIaudio_path + "helpintro.wav")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    
    def update_grid_display(self):
        # Verwijder bestaande widgets uit rompgrid
        for i in reversed(range(self.rompgrid.count())):
            self.rompgrid.itemAt(i).widget().setParent(None)

        # Voeg widgets toe voor de huidige 5 rijen
        for i in range(self.current_row, min(self.current_row + 5, len(functies))):
            outputstring = f"font: {font_size}pt {config.get('Settings', 'font_type')}; font-weight: bold; color: black; background-color: {config.get('Settings', 'colorcode')};"
            function_name = functies[i]
            function_uitleg = functiesuitleg[i]
            speaker = speakers[i]

            label = QLabel(function_name)
            label.setStyleSheet(outputstring)
            labeluitleg = QLabel(function_uitleg)
            labeluitleg.setStyleSheet(outputstring)

            self.rompgrid.addWidget(speaker, i - self.current_row, 0)
            self.rompgrid.addWidget(label, i - self.current_row, 1)
            self.rompgrid.addWidget(labeluitleg, i - self.current_row, 2)




    def speak(self, function_name):
        print("Deze functie moet worden uitgevoerd:", function_name)
        sound_path = (AIaudio_path + function_name + ".wav")
        print(sound_path)
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        time.sleep(2)
        sound_path = (AIaudio_path + function_name + "uitleg.wav")
        print(sound_path)
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
          
    def vorige(self, event=None):
        if self.current_row > 0:
            self.current_row -= 5  # Terug naar de vorige set rijen
            self.update_grid_display()

    def volgende(self, event=None):
        if self.current_row + 5 < len(functies):
            self.current_row += 5  # Ga naar de volgende set rijen
            self.update_grid_display()
    def vraagmij(self, event=None):
        print("vraag mij")
        weg = vastsysteem_path + "UsefullPrograms/googleAI/vraagmij.py"
        command = ["python3", weg]
        sound_path = (AIaudio_path + "helpintro.wav")
        print(sound_path)
        pygame.mixer.music.load(sound_path)
        time.sleep(0.5)
        pygame.mixer.music.play()
        time.sleep(1)
        subprocess.Popen(command)

    def vraagander(self, event=None):
        print("vraag ander")
        weg = vastsysteem_path + "UsefullPrograms/googleAI/vraagander.py"
        command = ["python3", weg]
        sound_path = (AIaudio_path + "helpintro.wav")
        print(sound_path)
        pygame.mixer.music.load(sound_path)
        time.sleep(0.5)
        pygame.mixer.music.play()
        time.sleep(1)
        subprocess.Popen(command)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())

