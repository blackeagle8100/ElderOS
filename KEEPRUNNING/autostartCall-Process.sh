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

phone() {
    cd ~/VASTSYSTEEM/Telephone/TELEFOON
    ./activatephone.py
    ./watcher.py
    ./battchecker.py
}

vastsysteem-call &
cordenhance
phone

sleep 20
wmctrl -a MAIN
cordbot
