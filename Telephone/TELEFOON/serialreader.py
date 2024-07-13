#!/usr/bin/env python3

import subprocess
import re
import sys
import time
import os
import configparser


config = configparser.ConfigParser()

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")


config.read(vastsysteem_path + '/settings.ini')
device_ip = config.get('Settings', 'smartip')
print(device_ip)

def processcheck(process):
    try:
        # Run the shell command to check for the process
        result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, text=True)
        # Filter the result to check for the process name
        if process in result.stdout:
            print(f"{process} is running")
            return True
        else:
            print(f"{process} is not running")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def monitor_serial_port():
    try:
        # Run the shell command to check for the process
        result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, text=True)
        # Filter the result to check for the process name
        if device_ip in result.stdout:
            print("ADB is started")
        else:
            print("ADB is not running")
            print("Check if adb is running on the watch")
            result = subprocess.run(['adb', 'connect', device_ip], stdout=subprocess.PIPE, text=True)
            print(result)
            if "connected" in result.stdout:
                print("ADB connected to the device")
            else:
                subprocess.run(['adb', 'connect', device_ip])
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        print("Monitoring")

        while True:
            callstate = subprocess.Popen(["adb", "-s", device_ip, "shell", "dumpsys", "telephony.registry"], stdout=subprocess.PIPE, universal_newlines=True)
            for line in callstate.stdout:
                if "mCallState" in line:
                    callstate_value = line.split("=")[1].strip()
                    if callstate_value == "1":
                        print("Call received")
                        number_process = subprocess.Popen(["adb", "-s", device_ip, "shell", "dumpsys", "telephony.registry"], stdout=subprocess.PIPE, universal_newlines=True)
                        for num_line in number_process.stdout:
                            if "mCallIncomingNumber" in num_line:
                                nummer = num_line.split("=")[1].strip()
                                print("Incoming call from:", nummer)
                                subprocess.Popen(["python3", vastsysteem_path+ "/Telephone/TELEFOON/neemop.py", nummer])
                                sys.exit()
            time.sleep(1) # Short time.sleep to reduce CPU usage
    except Exception as e:
        print("Error:", e)
        print("Something went wrong, closing this process and restarting serialreader")
        time.sleep(1)
        subprocess.Popen(["python3", vastsysteem_path+ "/Telephone/TELEFOON/serialreader.py"])
        sys.exit()

if __name__ == "__main__":
    monitor_serial_port()
