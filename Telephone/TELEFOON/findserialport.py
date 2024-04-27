#!/usr/bin/env python3

import serial.tools.list_ports

# Get a list of all available serial ports
ports = serial.tools.list_ports.comports()

# Iterate over the list of ports and print information about each port
for port in ports:
    print(port)