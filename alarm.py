#!/usr/bin/env python3


import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import *
import os
import pygame


user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

class AlarmApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        self.alarm_triggered = False
    def initUI(self):
        self.setWindowTitle('Alarm Window')
        self.setGeometry(100, 100, 300, 150)

        self.message_label = QLabel(self)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet('font-size: 16px;')

        layout = QVBoxLayout(self)
        layout.addWidget(self.message_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_alarms)
        
        pygame.init()
        
        self.alarms = [
            {"time": QTime(21, 48), "sound_path": user_home + "/Downloads/alarm.wav"},
            {"time": QTime(21, 52), "sound_path": user_home + "/Downloads/alarm.wav"},
            # Add more alarms as needed
        ]
        
    

    def check_alarms(self):
        current_time = QDateTime.currentDateTime().time()

        for alarm in self.alarms:
            if current_time >= alarm["time"] and not self.alarm_triggered:
                self.show_alarm_window(alarm["time"])
                self.play_alarm_sound(alarm["sound_path"])
                self.alarm_triggered = True

    def show_alarm_window(self, alarm_time):
        self.message_label.setText(f'Alarm at {alarm_time.toString()}!')
        self.show()

        
    def play_alarm_sound(self, sound_path):
        # Replace 'path/to/your/alarm.wav' with the actual path to your WAV file
        pygame.mixer.music.load(sound_path)

        pygame.mixer.music.play(loops=-1)
        
    def closeEvent(self, event):
        # Override the closeEvent to handle cleanup when the window is closed
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    alarm_app = AlarmApp()

    # Set the alarm time to 18:00
    current_time = QDateTime.currentDateTime().time()
    upcoming_alarms = [alarm["time"] for alarm in alarm_app.alarms if current_time < alarm["time"]]

    if upcoming_alarms:
        # Set the next upcoming alarm time
        alarm_app.timer.start(1000)  # Start the timer to check for the alarm
    else:
        print("No upcoming alarms.")

    sys.exit(app.exec())
