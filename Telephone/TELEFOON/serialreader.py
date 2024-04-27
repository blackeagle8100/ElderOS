#!/usr/bin/env python3

import serial
import subprocess
import re
import sys
import time
import os

user_home = os.path.expanduser("~")
global vastsysteem_path
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

def monitor_serial_port(port='/dev/ttyUSB0', baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate)
        print(f"Monitoring {port}... from serialreader.py")
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode().strip()
                print("Received:", data)
                if "RING" in data:
                    print("Ring ontdekt in data")
                    data = ser.readline().decode().strip()
                    #print("Gebelde data 1:", data)
                    data = ser.readline().decode().strip()
                    print("Closing serialreader")
                    ser.close()
                    #print("Gebelde data 2:", data)
                    split =data.split(",")
                    telnr= split[0]
                    split = telnr.split(' ')
                    telnr= split[1]
                    telnr = telnr.replace('"', "")
                    telnr = telnr.replace(' ', "")
                    #telnr = re.sub(r'\D', '', telnr)
                    print("TEL:",telnr)
                    subprocess.Popen(["python3",vastsysteem_path +"/Telephone/TELEFOON/neemop.py", telnr])
                    print("Exit serialReader")
                    sys.exit()
                elif '+BTDISCONN' in data:
                    print("bluetooth disconnected; try connecting again")
                    ser.write(b'AT+BTCONNECT=1,5\r\n')
            time.sleep(0.1) #korte time.sleep nodig want anders draait de controle te snel ==> te veel cpu verbruik voor nix
 
    except serial.SerialException as e:
        print("Error:", e)
        print("Iets ging mis sluit dit process en start serialreader opnieuw")
        ser.close()
        time.sleep(0.5)
        subprocess.Popen(["python3", vastsysteem_path+"/Telephone/TELEFOON/serialreader.py"])
        sys.exit()

if __name__ == "__main__":
    monitor_serial_port()