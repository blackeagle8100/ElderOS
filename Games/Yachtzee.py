#!/usr/bin/env python3

import sys
from PyQt6.QtWidgets import (
    QSizePolicy, QApplication, QSpacerItem, QMainWindow, QWidget, QPushButton,
    QGridLayout, QCheckBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFrame)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from random import randint
import os
import configparser 
import time

config = configparser.ConfigParser()

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")
config.read(os.path.join(vastsysteem_path, 'settings.ini'))

colorcode = config.get('Settings', 'colorcode')
font_type = config.get('Settings', 'font_type')
font_size = config.get('Settings', 'font_size')
global pvp
pvp = 1
pcmode = "easy"
class YahtzeeGame:
    def __init__(self):
        self.dice = [0] * 5
        self.roll_count = 0
        self.held_dice = [False] * 5
        self.scores = {
            "Een": "0", "Twee": "0", "Drie": "0", "Vier": "0", "Vijf": "0", "Zes": "0",
            "Bonus": "0", "3 dezelfde": "0", "4 dezelfde": "0", "Full House": "0",
            "Kleine straat": "0", "Hoge straat": "0", "Yahtzee": "0", "Kans": "0"
        }

        self.scoreP1 = {key: "0" for key in self.scores}
        self.scoreP2 = {key: "0" for key in self.scores}

    def roll_dice(self):
        if self.roll_count < 3:
        
            self.dice = [randint(1, 6) if not held else die for die, held in zip(self.dice, self.held_dice)]
            
            self.roll_count += 1
            return True
        else:
            return False

    def reset_dice(self):
        self.dice = [0] * 5
        self.roll_count = 0
        self.held_dice = [False] * 5

    def set_score(self, category, value):
        self.scores[category] = value

class YahtzeeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.player = "P1"
        self.setWindowTitle("Yahtzee")
        self.showFullScreen()
        self.setStyleSheet(f"background-color: {colorcode}; color: black; font-size: {font_size}px;")
        self.score_grid_layout = QGridLayout() 
        self.yahtzee_game = YahtzeeGame()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.checkboxes_P1 = {}
        self.checkboxes_P2 = {}
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self.central_widget)

        self.label_dice = QLabel("Dice: ")
        self.label_result = QLabel("Resultaat: ")

        self.dices = [QLabel(self) for _ in range(5)]
        for i, dice_label in enumerate(self.dices):
            dice_label.setGeometry(i * 70, 10, 50, 50)

        self.lineedit_score = QLineEdit("0")
        self.lineedit_score.setReadOnly(True)

        self.buttons = [QPushButton(f"Dobbel {i + 1}") for i in range(5)]
        for i, button in enumerate(self.buttons):
            button.setGeometry(i * 60, 60, 50, 50)
            button.clicked.connect(self.toggle_hold)

        self.button_roll = QPushButton(f"Speler {self.player} aan de beurt! Rol")
        self.button_roll.setStyleSheet('color: red;' if self.player == "P1" else 'color: blue;')
        self.button_roll.clicked.connect(self.roll_dice)

        self.button_close = QPushButton("Sluiten")
        self.button_close.clicked.connect(exit)

        self.button_PVP = QPushButton("Spel tegen P2")
        self.button_PVP.clicked.connect(self.pvp)

        self.btnP1E = QPushButton("Gemakkelijk spel tegen PC")
        self.btnP1E.clicked.connect(self.P1Easy)

        self.btnP1M = QPushButton("Gemiddeld spel tegen PC")
        self.btnP1M.clicked.connect(self.P1Medium)

        self.btnP1H = QPushButton("Moeilijk spel tegen PC")
        self.btnP1H.clicked.connect(self.P1Hard)
        self.lblaantalrol = QLabel()
        
        self.lblaantalrol.setText("Aantal keer gerold: 0")
        self.lblaantalrol.setStyleSheet('color: red;' if self.player == "P1" else 'color: blue;')
        
        #TOP layout
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.button_close)
        top_layout.addWidget(self.button_PVP)
        top_layout.addWidget(self.btnP1E)
        top_layout.addWidget(self.btnP1M)
        top_layout.addWidget(self.btnP1H)

        main_layout.addLayout(top_layout)

        # Dice layout
        dices_layout = QHBoxLayout()
        for dice in self.dices:
            dices_layout.addWidget(dice)
        main_layout.addLayout(dices_layout)

        # Button layout
        buttons_layout = QHBoxLayout()
        for button in self.buttons:
            buttons_layout.addWidget(button)
        main_layout.addLayout(buttons_layout)

        # Roll, Reset, and Score button layout
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.button_roll)
        buttons_layout.addWidget(self.lblaantalrol)
               
        #buttons_layout.addWidget(self.button_reset)
        #buttons_layout.addWidget(self.button_score)
        main_layout.addLayout(buttons_layout)

        # Scoreboard layout
        scoreboard_frame = QFrame(self)
        scoreboard_frame.setObjectName("scoreboardFrame")
        scoreboard_frame.setStyleSheet("QFrame#scoreboardFrame { border: 2px solid black; }")
        scoreboard_layout = QVBoxLayout(scoreboard_frame)
        scoreboard_layout.setSpacing(1)
        self.score_labels = {}
        self.scoreboard_P1 = {}
        self.scoreboard_P2 = {}

        self.init_score_grid()
        scoreboard_layout.addLayout(self.score_grid_layout)
        scoreboard_layout.addStretch(1)
        main_layout.addWidget(scoreboard_frame)

        self.yahtzee_game.reset_dice()
        self.update_ui()

    def pvp(self):
        print('start spel voor 2 spelers')
        pvp = 1
    def P1Easy(self):
        print('Spel voor 1 speler easy')
        pvp = 0
        pcmode = "easy"
    def P1Medium(self):
        print('Spel voor 1 speler medium')
        pcmode = "normal"
        pvp = 0
    def P1Hard(self):
        print('Spel voor 1 speler hard')
        pcmode = "hard"
        pvp = 0
    def init_score_grid(self):
            categories = ["Score: P1 SCORE","Speler 1",  "", "Category", "Current Score", "", "Speler 2", "Score: P2 SCORE"]
            for col, label_text in enumerate(categories):
                label = QLabel(label_text, alignment=Qt.AlignmentFlag.AlignCenter)
                self.score_grid_layout.addWidget(label, 0, col)  
                if label_text == "Speler 1":
                    label.setStyleSheet("color: red;")  # Set red color for Speler 1 and Score: P1 SCORE
                elif label_text == "Score: P1 SCORE":
                    label.setStyleSheet("color: red;")
                    self.txtP1Score = label  
                elif label_text == "Speler 2":
                    label.setStyleSheet("color: blue;")  # Set blue color for Speler 2 and Score: P2SCORE
                elif label_text == "Score: P2 SCORE":
                    label.setStyleSheet("color: blue;")
                    self.txtP2Score = label
                # Draw a line above the heading
                line = QFrame(self)
                line.setFrameShape(QFrame.Shape.HLine)
                #line.setFrameShadow(QFrame.Shadow.Sunken)
                line.setStyleSheet("background-color: black;")
                self.score_grid_layout.addWidget(line, 1, 0, 1, len(categories))
                # Add an empty QLabel for spacing
                spacer_label = QLabel()
                self.score_grid_layout.addWidget(spacer_label, 2, 2)
                # Draw a vertical line between "Current Score" and "P1"
                separator_linea = QFrame(self)
                separator_linea.setFrameShape(QFrame.Shape.VLine)
                separator_linea.setFrameShadow(QFrame.Shadow.Sunken)
                separator_linea.setStyleSheet("background-color: black;")
                separator_line2 = QFrame(self)
                separator_line2.setFrameShape(QFrame.Shape.VLine)
                separator_line2.setFrameShadow(QFrame.Shadow.Sunken)
                separator_line2.setStyleSheet("background-color: black;")
                # Adjusted layout to include spacer, vertical line, and centering spacer
                self.score_grid_layout.addWidget(separator_linea, 2, 2, len(self.yahtzee_game.scores) + 2, 1)
                self.score_grid_layout.addWidget(separator_line2, 2, 5, len(self.yahtzee_game.scores) + 2, 1)
                # Add a horizontal spacer to draw the line on top of the row
                spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
                self.score_grid_layout.addItem(spacer, 3, 0, 1, len(categories))

            for row, category in enumerate(self.yahtzee_game.scores, start=2):
                line = QFrame(self)
                line.setFrameShape(QFrame.Shape.HLine)
                line.setFrameShadow(QFrame.Shadow.Sunken)     
                if row < len(self.yahtzee_game.scores) + 1:
                        self.score_grid_layout.addWidget(line, row, 0, 2, len(categories))
                label_category = QLabel(category, alignment=Qt.AlignmentFlag.AlignCenter)
                label_scoreP1 = QLabel("0", alignment=Qt.AlignmentFlag.AlignCenter)
                label_scoreP2 = QLabel("0", alignment=Qt.AlignmentFlag.AlignCenter)
                label_score = QLabel("0", alignment=Qt.AlignmentFlag.AlignCenter)
                self.score_labels[category] = label_score  # Store the label reference
                self.scoreboard_P1[category] = label_scoreP1
                self.scoreboard_P2[category] = label_scoreP2   
                
                checkbox_p1 = QCheckBox()
                checkbox_p2 = QCheckBox()

                # Styling for the checkboxes
                checkbox_p1.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px; }")
                checkbox_p2.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px; }")

                # Adding checkboxes to the layout
                self.score_grid_layout.addWidget(checkbox_p1, row, 1, alignment=Qt.AlignmentFlag.AlignCenter)
                self.score_grid_layout.addWidget(checkbox_p2, row, 6, alignment=Qt.AlignmentFlag.AlignCenter)

                # Storing references in dictionaries
                self.checkboxes_P1[category] = checkbox_p1
                self.checkboxes_P2[category] = checkbox_p2
                
                 # Enables all checkboxes for P1
                for p1_category_checkbox in self.checkboxes_P1.values():
                    p1_category_checkbox.setEnabled(True)               
                
                # Disable all checkboxes for P2
                for p2_category_checkbox in self.checkboxes_P2.values():
                    p2_category_checkbox.setEnabled(False)
                


                # Adjusted layout to add space around checkboxes and center them
                self.score_grid_layout.addWidget(checkbox_p1, row, 1, alignment=Qt.AlignmentFlag.AlignCenter )
                self.score_grid_layout.addWidget(label_scoreP1, row, 0, alignment=Qt.AlignmentFlag.AlignCenter)
                self.score_grid_layout.addWidget(spacer_label, row, 2, alignment=Qt.AlignmentFlag.AlignCenter)
                self.score_grid_layout.addWidget(label_category, row, 3)
                self.score_grid_layout.addWidget(label_score, row, 4)
                self.score_grid_layout.addWidget(spacer_label, row, 5, alignment=Qt.AlignmentFlag.AlignCenter)
                self.score_grid_layout.addWidget(checkbox_p2, row, 6, alignment=Qt.AlignmentFlag.AlignCenter)
                
                self.score_grid_layout.addWidget(label_scoreP2, row, 7)
              
                # Connecting checkboxes to the score_checkbox_changed method
                checkbox_p1.stateChanged.connect(lambda state, cat=category, cb=checkbox_p1: self.score_checkbox_changed(cat, state, cb, self.player))
                checkbox_p2.stateChanged.connect(lambda state, cat=category, cb=checkbox_p2: self.score_checkbox_changed(cat, state, cb, self.player))

    def toggle_hold(self):
        button = self.sender()
        index = self.buttons.index(button)
        self.yahtzee_game.held_dice[index] = not self.yahtzee_game.held_dice[index]
        button.setText(f"Dobbel {index + 1} {'VAST' if self.yahtzee_game.held_dice[index] else 'LOS'}")

    def roll_dice(self):
        if self.yahtzee_game.roll_dice():
            self.update_ui()
            self.button_roll.setText("Speler " + self.player + " aan beurt! Rol:" + str(self.yahtzee_game.roll_count))
            self.lblaantalrol.setText("Aantal keer gerold: "+str(self.yahtzee_game.roll_count))
            print(self.player)
            if self.yahtzee_game.roll_count >= 3:
                self.score()

    def reset_dice(self):
        self.yahtzee_game.reset_dice()
        for button in self.buttons:
            button.setText(button.text().replace('VAST', '').replace('LOS', ''))
        for category, label in self.score_labels.items():
           self.score_labels[category].setText("0")
        self.update_ui()

    def update_ui(self):
        for i in range(5):
            file_path = os.path.join(vastsysteem_path, "Games", "Dobbelsteen", f"DOBBEL{self.yahtzee_game.dice[i]}.png")
            self.dices[i].setPixmap(QPixmap(file_path))
            print(f"Loading image for dice {i + 1}: {file_path}")

        dice_text = "Dobbel: "
        result_text = f"Resultaat: {self.calculate_result()}"
        self.label_dice.setText(dice_text)
        self.label_result.setText(result_text)
        self.lineedit_score.setText(str(self.yahtzee_game.roll_count))

    def calculate_result(self):
        return "Resultaat"  # Replace with your logic

    def score(self):

        for category, label in self.score_labels.items():
            if category == "Een":
                value = 1 * self.yahtzee_game.dice.count(1)
            elif category == "Twee":
                value = 2 * self.yahtzee_game.dice.count(2)
            elif category == "Drie":
                value = 3 * self.yahtzee_game.dice.count(3)
            elif category == "Vier":
                value = 4 * self.yahtzee_game.dice.count(4)
            elif category == "Vijf":
                value = 5 * self.yahtzee_game.dice.count(5)
            elif category == "Zes":
                value = 6 * self.yahtzee_game.dice.count(6)
            elif category == "Bonus":
                som = 0
                if self.player == "P1":
                    som = som + int(self.yahtzee_game.scoreP1["Een"]) + int(self.yahtzee_game.scoreP1["Twee"]) + int(self.yahtzee_game.scoreP1["Drie"])+ int(self.yahtzee_game.scoreP1["Vier"])+ int(self.yahtzee_game.scoreP1["Vijf"])+ int(self.yahtzee_game.scoreP1["Zes"])
                    print("SOM: ", som)
                    if som >= 63:
                        value = 1000
                elif self.player == "P2":
                    som = som + int(self.yahtzee_game.scoreP2["Een"]) + int(self.yahtzee_game.scoreP2["Twee"]) + int(self.yahtzee_game.scoreP2["Drie"])+ int(self.yahtzee_game.scoreP2["Vier"])+ int(self.yahtzee_game.scoreP2["Vijf"])+ int(self.yahtzee_game.scoreP2["Zes"])
                    print("SOM: ", som)
                    if som >= 63:
                        value = 1000
                else:
                    print('ge kunt er nietn van XD')
                
            elif category == "3 dezelfde":
                value = sum(self.yahtzee_game.dice) if any(self.yahtzee_game.dice.count(dice) >= 3 for dice in self.yahtzee_game.dice) else 0
            elif category == "4 dezelfde":
                value = sum(self.yahtzee_game.dice) if any(self.yahtzee_game.dice.count(dice) >= 4 for dice in self.yahtzee_game.dice) else 0
            elif category == "Full House":
                counts = [self.yahtzee_game.dice.count(dice) for dice in set(self.yahtzee_game.dice)]
                value = 25 if 2 in counts and 3 in counts else 0
            elif category == "Kleine straat":
                sorted_dice = sorted(set(self.yahtzee_game.dice))
                straight_counts = [0, 0, 0, 0, 0, 0]

                for dice in sorted_dice:
                    if 1 <= dice <= 6:
                        straight_counts[dice - 1] = 1
                straight_found = any(sum(straight_counts[i:i+4]) == 4 for i in range(len(straight_counts) - 3))
                value = 30 if straight_found else 0
            elif category == "Hoge straat":
                sorted_dice = sorted(set(self.yahtzee_game.dice))
                # Check if the sorted_dice is a valid high straight
                straight_found = len(sorted_dice) == 5 and sorted_dice[-1] - sorted_dice[0] == 4
                value = 40 if straight_found else 0
            elif category == "Yahtzee":
                value = 50 if any(self.yahtzee_game.dice.count(dice) >= 5 for dice in self.yahtzee_game.dice) else 0
            elif category == "Kans":
                value = sum(self.yahtzee_game.dice)
            else:
                value = 0
            string = f"{category}: {value}"
            split = string.split(": ")
            nm = split[1]
            label.setText(nm)
            self.yahtzee_game.set_score(category, value)
            
    def score_checkbox_changed(self, category, state, checkbox, player):
        print(f"Checkbox changed for category {category} for player {player}")
        print("New state:", state)
        print(checkbox)
        som = 0
        if state == 2:
            #checkbox.setEnabled(False)
            points = int(self.score_labels[category].text())
            som = 0

            if self.player == "P1":
                 # Enables all checkboxes for P1
                for p1_category_checkbox in self.checkboxes_P1.values():
                    p1_category_checkbox.setEnabled(False)               
                # Disable all checkboxes for P2
                for p2_category_checkbox in self.checkboxes_P2.values():
                    p2_category_checkbox.setEnabled(True)
                self.yahtzee_game.scoreP1[category] = points
                self.scoreboard_P1[category].setText(str(points))
                self.scoreboard_P1[category].setStyleSheet("color: red;")
                self.button_roll.setStyleSheet('color: blue;')
                self.lblaantalrol.setStyleSheet('color: blue;')
                for cat, label in self.score_labels.items():
                    som += int(self.yahtzee_game.scoreP1[cat])     
                argument = "Totaal: " + str(som)
                self.txtP1Score.setText(argument)
                self.player = "P2"
            elif self.player == "P2" and pvp == 1:            
                 # Enables all checkboxes for P2
                for p2_category_checkbox in self.checkboxes_P2.values():
                    p2_category_checkbox.setEnabled(False)               
                # Disable all checkboxes for P1
                for p1_category_checkbox in self.checkboxes_P1.values():
                    p1_category_checkbox.setEnabled(True)
                self.yahtzee_game.scoreP2[category] = points
                self.scoreboard_P2[category].setText(str(points))
                self.scoreboard_P2[category].setStyleSheet("color: blue;")
                self.button_roll.setStyleSheet('color: red;')
                self.lblaantalrol.setStyleSheet('color: red;')
                for cat, label in self.score_labels.items():
                    som += int(self.yahtzee_game.scoreP2[cat])
                argument = "Totaal: " + str(som)
                self.txtP2Score.setText(argument)
                self.player = "P1"
            elif self.player == "P2" and pvp == 0:
                print('Spel gestart tegen pc.')
                # Disables all checkboxes 
                for p2_category_checkbox in self.checkboxes_P2.values():
                    p2_category_checkbox.setEnabled(False)               
                for p1_category_checkbox in self.checkboxes_P1.values():
                    p1_category_checkbox.setEnabled(False)

                if pcmode == "easy":
                    print("Easy game mode hier in voor PC")
                    self.roll_easydice_npc()
                elif pcmode == "normal":
                    print("Normal gamemode hier in voor PC")
                elif pcmode == "hard":
                    print("Hard gamemode hier in voor PC")
            self.reset_dice()
            self.update_ui()
            self.button_roll.setText("Speler " + self.player + " aan beurt! Rol:" + str(self.yahtzee_game.roll_count))
            self.lblaantalrol.setText("Aantal keer gerold: 0")

    #NPC PROGRAMMING FROM HERE!

    def npc_select_minscore(self):
        available_categories = [category for category, checkbox in self.checkboxes_P2.items() if checkbox.isEnabled()]
        return min(available_categories, key=lambda cat: int(self.score_labels[cat].text()))    
    
    def roll_easydice_npc(self):
        while self.yahtzee_game.roll_count < 3:
            self.yahtzee_game.roll_dice()
            self.update_ui()
            if self.yahtzee_game.roll_count >= 3:
                self.easyscore_npc()
                break
    def easyscore_npc(self):
        selected_category = self.npc_select_minscore()
        checkbox = self.checkboxes_P2[selected_category]
        checkbox.setChecked(True)  # Simulate the NPC selecting a score
        self.score_checkbox_changed(selected_category, 2, checkbox, "P2")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YahtzeeMainWindow()
    window.show()
    sys.exit(app.exec())