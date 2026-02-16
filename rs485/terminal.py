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
                # modbus request
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
                int_torque_nm = int(hex_response_torque.strip(), 16)/100   # hex to decimal conversion of torque in Nm
                int_torque_ftlbs = 0.73756*int_torque_nm
                int_rpm = int(hex_response_rpm.strip(), 16)         # hex to decimal conversion of angular velocity in rpm
                int_pwr = int(hex_response_pwr.strip(), 16)         # hex to decimal conversion of power in watts
                if response:
                    #print(f"Received Val: {response}")      # ascii
                    #print(f"Received Hex: {hex_response}")  # hex
                    #print(f"Received Index: {hex_response_index}")
                    print(f"Received Torque [Nm]: {int_torque_nm}")
                    print(f"Received Torque [Ft*Lbs]: {int_torque_ftlbs:.2f}")
                    print(f"Received Angular Velocity [RPM]: {int_rpm}")
                    print(f"Received Power [W]: {int_pwr}")
                else:
                    print("No response received")
                
                time.sleep(1)   # one second delay before sending command again

            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                print("Closing COM port...")
                config.serCfg.close()
                print("Exiting...\n\n")
                is_writing = False
                sys.exit(1)

    elif ~config.serCfg.is_open:
        print("Unable to open com port.\n")

    print("\nPort COM" + comport_user_input + " closed.\nExiting...\n")
    config.serCfg.close()

if __name__ == "__main__":
    main()
        