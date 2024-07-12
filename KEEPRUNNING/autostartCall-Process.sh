#!/bin/bash

vastsysteem-call() {
    ~/VASTSYSTEEM/ElderOS.py
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
