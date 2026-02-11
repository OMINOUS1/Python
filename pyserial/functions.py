"""
functions.py

    Holds functions for serial terminal

    Author : Paul Farrell (@OMINOUS1) (Paulf@woodway.com)

    LAST DEVELOPED FOR: Python 3.14.2

"""
# ~~~~ Imports ~~~~
import serial
import sys
import time
import config  # custom file for the serial configs to share global serial object.

is_writing = False
is_reading = False

# ~~~ Functions ~~~

# write function to send user input hex values over serial
def write():

    is_writing = True

    while is_writing:
        try:
            # get hex input from user
            user_input = input("\n>>Enter a hex command (e.g, 0x1A or 1A): ").strip()

            # remove '0x' if present
            if user_input.lower().startswith("0x"):
                user_input = user_input[2:]

            # adding bounds
            if not all(c in "0123456789abcdefABCDEF" for c in user_input):
                print("Invalid hex value. only 0-9 and A-F are allowed.")
                config.serCfg.close()
                sys.exit(1)

            # convert hex string bytes
            hex_value = bytes.fromhex(user_input)
            config.serCfg.write(hex_value)
            print(f"Sent: {user_input}")

            # read response prints ascii and hex
            response = config.serCfg.readline()
            hex_response = response.hex()
            if response:
                print(f"Received Val: {response}")      # ascii
                print(f"Received Hex: {hex_response}")  # hex
            else:
                print("No response received")

        except KeyboardInterrupt:
            print("Operation cancelled by user.")
            print("Closing COM port...")
            config.serCfg.close()
            print("Exiting...")
            is_writing = False
            sys.exit(1)
        
# read function to read serial input
def read():

    is_reading = True

    while is_reading:
        print("\nReading from serial port...")
        try:
            while True:
                if config.serCfg.in_waiting > 0:

                    # read response prints ascii and hex
                    response = config.serCfg.readline()
                    hex_response = response.hex()
                    print(f"\nReceived Val: {response}")      # ascii
                    print(f"Received Hex: {hex_response}")  # hex

        except KeyboardInterrupt:
            print ("\nStopped by user")
            return

        finally:
            print("Operation cancelled by user.")
            print("Closing COM port...")
            config.serCfg.close()
            print("Exiting...")
            is_writing = False
            sys.exit(1)

# dual read function to read serial input
def multiport():

    print("\nWhich COMPORT is the second controller connected to?")
    comport_user_input = input(">> COM")

    print("\nWhat baud rate is the second controller set at?")
    baudrate_user_input = input()

    print("\nWhat timeout will the second controller use [s]?")
    timeout_user_input = int(input())

    #config.initSerial(comport_user_input,baudrate_user_input,timeout_user_input)
    #config.serCfg.open()

    ser2 = serial.Serial(comport_user_input,baudrate_user_input,timeout_user_input)
    ser2.open()

    print("\nReading from serial port...")
    try:
        while True:
            if config.serCfg.in_waiting > 0:
            
                # read response from first comport, prints ascii and hex
                response1 = config.serCfg.readline()
                hex_response1 = response1.hex()
                print(f"\nReceived Val: {response1}")      # ascii
                print(f"Received Hex: {hex_response1}")     # hex
                
                # read response from second comport, prints ascii and hex
                response2 = ser2.readline()
                hex_response2 = response2.hex()
                print(f"\nReceived Val: {response2}")      # ascii
                print(f"Received Hex: {hex_response2}")     # hex

    except KeyboardInterrupt:
        print ("\nStopped by user")
        return
    
    finally:
        print("Operation cancelled by user.")
        print("Closing COM port...")
        config.serCfg.close()
        print("Exiting...")
        is_writing = False
        sys.exit(1)