"""
 terminal.py

    Python script that communicates with an RS‑485 device connected via a
    USB‑to‑Serial adapter using PySerial.

    Author : Paul Farrell (@OMINOUS1) (Paulf@woodway.com)

    LAST DEVELOPED FOR: Python 3.14.2

"""

#~~~~~ Imports ~~~~~
import time
import sys
import config
import csv
import os
from datetime import datetime

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
            try:

                # getting the current date and time
                current_time = datetime.now()

                # getting the timestamp
                timestamp = current_time.timestamp()

                # modbus read request
                cmd = bytes.fromhex("01 03 00 00 00 06 C5 C8")

                config.serCfg.write(cmd)
                print(f"\nSent: {cmd}")

                # read response prints ascii and hex
                response = config.serCfg.readline()
                hex_response = response.hex()

                hex_response_index = hex_response[0:6]              # first 4 bytes of modbus response
                hex_response_torque = hex_response[6:14]            # bytes 7-14 for torque response
                hex_response_rpm = hex_response[14:22]              # bytes 15-22 for angular velocity response 
                hex_response_pwr = hex_response[22:30]              # bytes 23-30 for power response
                int_torque_nm = int(hex_response_torque.strip(), 16)#/100   # hex to decimal conversion of torque in Nm

                bits = 32   #bit value of each element
                
                #if sign bit is set, 2s compliment and absolute value
                if int_torque_nm & (1 << (bits - 1)):                 # 2s compliment
                    # mask to ensure value fits in the given bit width
                    mask = (1 << bits) -1
                    int_torque_nm = (~int_torque_nm +1) & mask
                
                int_torque_nm = int_torque_nm/100

                int_torque_ftlbs = 0.73756*int_torque_nm            # convert Nm to lb*ft 
                int_trq_ftlbs = round(int_torque_ftlbs, 2)          # rount value to nearest 2 decimal places
                int_rpm = int(hex_response_rpm.strip(), 16)         # hex to decimal conversion of angular velocity in rpm
                int_pwr = int(hex_response_pwr.strip(), 16)         # hex to decimal conversion of power in watts
                
                # title block to be written to the csv file
                title_block = ['Torque [lb*ft]',
                               'Angular Velocity [RPM]',
                               'Power [W]',
                               'Date and Time']
                
                # data to be written to the csv file
                data = [int_trq_ftlbs,
                        int_rpm,
                        int_pwr,
                        current_time]
                
                # file path
                file_path = 'output.csv'

                # check if file exists and is non-empty
                file_exists = os.path.isfile(file_path)
                file_empty = not file_exists or os.path.getsize(file_path) == 0

                # open the csv file for writing
                with open('output.csv', 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter = ',')

                    # write header only if the file is empty
                    if file_empty:
                        csvwriter.writerow(title_block)

                    # write the data rows to the csv file
                    csvwriter.writerow(data)

                if response:
                    #print(f"Received Val: {response}")      # ascii
                    #print(f"Received Hex: {hex_response}")  # hex
                    #print(f"Received Index: {hex_response_index}")
                    #print(f"Received Torque [Nm]: {int_torque_nm}")
                    print(f"Received Torque [lb*ft]: {int_trq_ftlbs}")
                    print(f"Received Angular Velocity [RPM]: {int_rpm}")
                    print(f"Received Power [W]: {int_pwr}")
                    #print("Current Time: ", current_time)
                    #print("Timestamp: ", timestamp)

                else:
                    print("No response received")
                
                #time.sleep(1)   # one second delay before sending command again

            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                print("Closing COM port...")
                config.serCfg.close()
                print("Exiting...\n\n")
                is_writing = False
                sys.exit(1)

    elif  not config.serCfg.is_open:
        print("Unable to open com port.\n")

    print("\nPort COM" + comport_user_input + " closed.\nExiting...\n")
    config.serCfg.close()

if __name__ == "__main__":
    main()
        