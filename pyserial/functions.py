"""
functions.py

    Holds functions

    Author : Paul Farrell (Paulf@woodway.com)

    LAST DEVELOPED FOR: Python 3.10.8

"""
# ~~~~ Imports ~~~~
import serial
import sys
import time
import config  # custom file for the serial configs to share global serial object.

def manual_write():
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

        # read response gets rid of 3s
        response = config.serCfg.readline()
        hex_response = response.hex()
        if response:
            print(f"Received Val: {response}")
            print(f"Received Hex: {hex_response}")
        else:
            print("No response received")

    except KeyboardInterrupt:
        print("Operation cancelled by user.")
        print("Closing COM port...")
        config.serCfg.close()
        print("Exiting...")
        sys.exit(1)
