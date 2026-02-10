"""
    config.py
    Globals, inits, and objects for other subfiles of the test software.

    Author : Paul Farrell (Paulf@woodway.com)

    LAST DEVELOPED FOR: Python 3.10.8

"""

# ~~~~~ Imports ~~~~~
import time
import serial
import serial.tools.list_ports
import json

# serialConfig object
global serCfg
serCfg = serial.Serial()

def list_serial_ports():
    """List all available serial ports."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def initSerial(COMPORT,BAUD_RATE,TO):
    # instantiate port
    # ser.baudrate = baudrate_user_input # optional alternative.
    serCfg.baudrate = BAUD_RATE
    serCfg.port = "COM" + COMPORT
    serCfg.timeout = TO  # seconds
    serCfg.stopbits = 1
    serCfg.startbits = 1
    # ser.rtscts = 1

    print(serCfg)
