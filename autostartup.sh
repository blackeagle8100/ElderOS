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
}
watcher() {
    cd ~/VASTSYSTEEM/Telephone/TELEFOON
    ./watcher.py 
}
batt() {
    cd ~/VASTSYSTEEM/Telephone/TELEFOON
    ./battchecker.py
}


vastsysteem-call &
cordenhance &
phone &
watcher &
batt &

sleep 20
wmctrl -a MAIN
cordbot

