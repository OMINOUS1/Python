"""
 serial.py
 Python script that communicates with an RS‑232 device connected via a
 USB‑to‑Serial adapter using PySerial.

"""

# ~~~~ Imports ~~~~
import serial
import sys
import time
import config  # custom file for the serial configs to share global serial object.

isRunningSerialUsb = False

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
                print("Pleaceholder")

            elif user_test_choice == "3":
                while True:
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
            else:
                print("Unknown choice.")

    elif ~config.serCfg.is_open:
        print("Unable to open com port.\n")

    print("\nPort COM" + comport_user_input + " closed.\nExiting...\n")
    config.serCfg.close()

#*******************************************************************************

if __name__ == "__main__":
    main()
