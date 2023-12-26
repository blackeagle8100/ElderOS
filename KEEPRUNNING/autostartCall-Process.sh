#!/bin/bash

cd ~/VASTSYSTEEM
./MemeOS-autoresize.py &
sleep 3
wmctrl -a Main
