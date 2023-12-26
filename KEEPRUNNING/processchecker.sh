#!/bin/bash

function check_usb_webcam() {
    for ((i=0; i<10; i++)); do
        cap=$(v4l2-ctl --list-devices | grep "video$i")
        if [ $? -eq 0 ]; then
            echo "USB webcam found at device $i"
            return 0
        fi
    done
    
    echo "No USB webcam found"
    return 1
}

function check_process() {
    process_name=$1
    if pgrep -x "$process_name" >/dev/null; then
        return 0
    fi
    return 1
}

function start_process() {
    process_path=$1
    "$process_path" &
}

function run_command() {
    command=$1
    eval "$command"
}

function check_window_title() {
    window_title=$1
    window_id=$(xdotool search --name "$window_title")
    if [ -n "$window_id" ]; then
        echo "The window with title '$window_title' is open."
    else
        echo "The window with title '$window_title' is not open."
        python3 CallChecker.py
    fi
}

process_name='mjpg_streamer'
process_path='/home/meme/Documenten/KEEPRUNNING/mjpg-streamer-master/mjpg-streamer-experimental'
command1="cd $process_path"
command2="./mjpg_streamer -i 'input_uvc.so -d /dev/video0' -o 'output_http.so -p 8081 -w ./www'"

while true; do
    window_title="Messenger-oproep"
    check_window_title "$window_title"

    if ! check_process "$process_name"; then
        check_usb_webcam
        if [ $? -eq 0 ]; then
            run_command "$command1"
            run_command "$command2"
            echo "Process started."
        else
            echo "Camera is already in use. Meme is probably still on a call."
        fi
    else
        echo "Process is already running."
    fi

    sleep 300
	
	current_time=$(date +"%H:%M")
	
	if [ "$current_time" == "01:00" ]; then
		password=slayer
		expect -c "
            spawn su -c 'apt update && apt full-upgrade -y'
            expect \"Password:\"
            send \"$password\r\"
            interact
        "
	fi
	
	if [ "$current_time" == "01:30" ]; then
		systemctl reboot
	fi
	
done
