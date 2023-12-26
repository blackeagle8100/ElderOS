#!/bin/bash
password="Alotbso12"
echo "Installing..."
echo "$password" | su -c "apt install spyder python3-pygame python3-opencv htop python3-pip python3-mutagen python3-selenium xdotool python3-pyqt6 python3-pyqt6.qtwebengine python3-pyqt6.qtmultimedia scrot notepadqq -y"
echo "Finished"
