"""
 serial_terminal.py

    Python script that communicates with an RS‑232 device connected via a
    USB‑to‑Serial adapter using PySerial.

    Author : Paul Farrell (@OMINOUS1) (Paulf@woodway.com)

    LAST DEVELOPED FOR: Python 3.14.2

"""

# ~~~~ Imports ~~~~
import serial
import sys
import time
import config  # custom file for the serial configs to share global serial object.
import functions

isRunningSerialUsb = False

# main running script
def main():
    print("\nScanning for available serial ports...")
    ports = config.list_serial_ports()

    if not ports:
        print("\nNo serial ports found. Please check your RS232-to-USB adapter.")
        sys.exit(1)

    print("\nAvailable ports:")
    for i, p in enumerate(ports):
        print(f"{i}: {p}")

    isRunningSerialUsb = True

    print("\nWhich COMPORT is the controller connected to?")
    comport_user_input = input(">> COM")

    print("\nWhat baud rate is the controller set at?")
    baudrate_user_input = input()

    print("\nWhat timeout will the controller use [s]?")
    timeout_user_input = int(input())

    config.initSerial(comport_user_input,baudrate_user_input,timeout_user_input)

    config.serCfg.open()

    if config.serCfg.is_open:
        while isRunningSerialUsb:
            # Here you can optionally decide full test or cherry picked tests w/ custom payloads.
            print("\n\n-------------------------")
            print("|\tMain Menu\t|")
            print("-------------------------")
            print("1. Exit\n2. Placeholder\n3. Manual Write")

            user_test_choice = input(">> ")

            if user_test_choice == "1":
                isRunningSerialUsb = False

            elif user_test_choice == "2":
                functions.read()

            elif user_test_choice == "3":
                while True:
                    functions.write()

            else:
                print("Unknown choice.")

    elif ~config.serCfg.is_open:
        print("Unable to open com port.\n")

    print("\nPort COM" + comport_user_input + " closed.\nExiting...\n")
    config.serCfg.close()

#*******************************************************************************

if __name__ == "__main__":
    main()
