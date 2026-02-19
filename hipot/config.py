"""
config.py

    Globals, inits, and objects for other subfiles of the test software.

    Author : Paul Farrell (@OMINOUS1) (Paulf@woodway.com)

    LAST DEVELOPED FOR: Python 3.14.2

"""

# ~~~~~ Imports ~~~~~
import time
import serial
import serial.tools.list_ports

# serialConfig object
global serCfg
serCfg = serial.Serial()

# ~~~~ functionsS

# function to automatically detect and list available com ports
def list_serial_ports():
    """List all available serial ports."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# function to initialize serial port with user input parameters
def initSerial(COMPORT,BAUD_RATE,TO):
    # instantiate port
    serCfg.baudrate = BAUD_RATE
    serCfg.port = "COM" + COMPORT
    serCfg.timeout = TO  # seconds
    serCfg.stopbits = 1
    serCfg.startbits = 1
    serCfg.rtscts = 1

    print(serCfg)
