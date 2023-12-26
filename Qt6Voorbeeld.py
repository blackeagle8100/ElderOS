#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:42:41 2023

@author: meme
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Example")
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel("Hello, PyQt6!", self)
        self.label.setGeometry(50, 50, 300, 30)

        self.button = QPushButton("Click Me", self)
        self.button.setGeometry(150, 150, 100, 30)
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        self.label.setText("Button Clicked!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
