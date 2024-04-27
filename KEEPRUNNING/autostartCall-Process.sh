#!/bin/bash

cd ~/VASTSYSTEEM
./ElderOS.py &
cd KEEPRUNNING
./opendiscord.py
./discordbot.py &
./cordEnhance.sh


wmctrl -a MAIN
