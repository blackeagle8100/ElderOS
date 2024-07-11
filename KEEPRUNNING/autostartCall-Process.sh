#!/bin/bash

vastsysteem-call() {
    ~/VASTSYSTEEM/MemeOS-autoresize.py
}
cordenhance() {
    cd ~/VASTSYSTEEM/KEEPRUNNING
    ./cordEnhance.sh
}

cordbot() {
    cd ~/VASTSYSTEEM/KEEPRUNNING
    ./cordbot.py
}

vastsysteem-call &
cordenhance

sleep 20
wmctrl -a MAIN
cordbot
