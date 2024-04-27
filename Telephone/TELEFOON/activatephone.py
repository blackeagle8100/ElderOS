#!/usr/bin/env python3

import serial
import time
import subprocess
import os

user_home = os.path.expanduser("~")
global vastsysteem_path, btprofile

vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")
# Configure the serial port
port = '/dev/ttyUSB0'
ser = serial.Serial(port, 9600, timeout=1)
btprofile = 1,5 #set the correct bluetooth profile for your device(btscan number, btprofile(HFG))
# Wait for the serial port to initialize

pincode = "0000"#getting this value from the ini file plz
time.sleep(10)
# TEST AT
ser.write(b'AT\r\n')
response = ser.read(2000)  # Read response from the module
response = response.decode()
print('reactie: ', response)
if "OK" in response:
    print('Alles ok voer verder uit')
    # Kijk of de pincode moet ingevoerd worden
    ser.write(b'AT+CPIN?\r\n')
    response = ser.read(2000)  # Read response from the module
    response = response.decode()
    print('reactie: ', response)

    if "+CPIN: READY" in response:
        print("Sim unlocked. geen pincode meer nodig")
    else:
        print('Sim locked: Pincode vereist')
        print("Volgende pincode wordt gebruikt", pincode)
        ser.write(b'AT+CPIN=' + pincode.encode() + b'\r\n')
        response = ser.read(2000)  # Read response from the module
        response = response.decode()
        print('reactie: ', response)

    print("Bluetooth wordt gestart")
    ser.write(b'AT+BTPOWER=1\r\n')
    response = ser.read(2000)  # Read response from the module
    response = response.decode()
    print('reactie: ', response)


    if "OK" in response:
        print("bluetooth geactiveerd")
  
    elif "ERROR" in response: 
        print("Bluetooth was al actief")

    print("Bluetooth is gestart en gereed voor pairing")
    print("Bluetooth wordt gepaired")
    time.sleep(2)
    ser.write(b'AT+BTCONNECT='+str(btprofile)+'\r\n')
    response = ser.read(2000)  # Read response from the module
    response = response.decode()
    print('reactie: ', response)
    
    time.sleep(2)

    
    print("Alles actief. start monitor mode")
    ser.close
    subprocess.Popen(["python3", vastsysteem_path+"/Telephone/TELEFOON/serialreader.py"])




    
else:
    print('Iets mis met de AT. Controleer de verbinding op de juiste serial device port aub')
    
