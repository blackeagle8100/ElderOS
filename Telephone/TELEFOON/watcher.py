#!/usr/bin/env python3


import subprocess
import time
import configparser
import os


user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")


config = configparser.ConfigParser()
config.read(vastsysteem_path + '/settings.ini')
device_ip = config.get('Settings', 'smartip')






def is_device_online(ip_address):
    try:
        # Run the ping command
        response = subprocess.run(
            ["ping", "-c", "1", ip_address],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Return True if ping was successful
        return response.returncode == 0
    except Exception as e:
        print(f"An error occurred while pinging: {e}")
        return False

def adb_connect(ip_address):
    try:
        # Run the adb connect command
        response = subprocess.run(
            ["adb", "connect", ip_address],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output = response.stdout.decode()
        print(output)
        return "connected to" in output.lower()
    except Exception as e:
        print(f"An error occurred while running adb connect: {e}")
        return False

def main():
      
    while True:
        # Check if the device is online
        if is_device_online(device_ip):
            print("Device "+ device_ip + "is online. Attempting to connect with adb.")
            if adb_connect(device_ip):
                print("Successfully connected to the device.")
            else:
                print("Failed to connect to the device.")
        else:
            print("Device "+ device_ip +" is offline. Waiting for it to come back online.")
        
        time.sleep(300)  

if __name__ == "__main__":
    main()
