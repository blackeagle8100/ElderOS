#!/bin/bash

SCRIPT1_PATH="/home/meme/VASTSYSTEEM/MemeOS-autoresize.py"
SCRIPT2_PATH="/home/meme/VASTSYSTEEM/KEEPRUNNING/processchecker.py"

while true; do
    # Check if script1 is already running
    if pgrep -f "$SCRIPT1_PATH" >/dev/null; then
        echo "Script 1 is already running."
    else
        echo "Script 1 is not running. Starting it now..."
        python3 "$SCRIPT1_PATH" &
    fi

    # Check if script2 is already running
    if pgrep -f "$SCRIPT2_PATH" >/dev/null; then
        echo "Script 2 is already running."
    else
        echo "Script 2 is not running. Starting it now..."
        python3 "$SCRIPT2_PATH" &
    fi
    
    # Introduce a delay between checks (e.g., 5 seconds)
    sleep 5
done

exit 0