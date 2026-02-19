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
import commands

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

    ser2 = serial.Serial(comport_user_input,baudrate_user_input,timeout = timeout_user_input)
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

# control commands
def ctrl_cmd():

    isRunningCtrl = True

    while isRunningCtrl:
        # Here you can optionally decide full test or cherry picked tests w/ custom payloads.
        print("\n\n-----------------------------------------")
        print("|\tControl Commands Main Menu\t|")
        print("-----------------------------------------")
        print("1. Exit\n" \
        "2. Start Belt with WatchDog\n" \
        "3. Start Belt\n" \
        "4. Disengage Belt\n" \
        "5. Belt Speed\n" \
        "6. Belt Elevation\n" \
        "7. Engage Belt\n" \
        "8. Auto Stop")

        user_test_choice = input(">> ")

        if user_test_choice == "1":
            print("Operation cancelled by user.")
            print("Exiting...")
            isRunningCtrl = False

        elif user_test_choice == "2":
            commands.ctrl_start_belt_wd()
        
        elif user_test_choice == "3":
            commands.ctrl_start_belt()
        
        elif user_test_choice == "4":
            commands.ctrl_disengage_belt()
        
        elif user_test_choice == "5":
            commands.ctrl_belt_speed()
        
        elif user_test_choice == "6":
            commands.ctrl_belt_elevation()
        
        elif user_test_choice == "7":
            commands.ctrl_belt_engage()
        
        elif user_test_choice == "8":
            commands.ctrl_belt_stop()

        else:
            print("Unknown choice.")

        #commands.ctrl_start_belt_wd()

# status query
def status_qry():
    while True:
        # Here you can optionally decide full test or cherry picked tests w/ custom payloads.
        print("\n\n-------------------------")
        print("|\tStatus Query Main Menu\t|")
        print("-------------------------")
        print("1. Exit\n2. Read\n3. Write\n4. Multiport\n5. Control Commands\n6. Status Query")

        #commands.query()
