"""
terminal.py

    Python script to run Woodway USA, Inc. Hipot Vitrek V74 Test

    Test Sequence:

        Test 1: Ground Bond (GB), 25A, 6sec, 100mOhm max
            Performs resistance measurment to ensure resistance is within limit

        Test 2: AC Voltage Withstand (ACW), 1500VAC, 60sec, Breakdown Only
            Performas measurment on dielectric breakdown

    ASCII Commands:
        RUN         Runs the test sequence

    ASCII Query Commands:
        STAT?       Response with string of pass/fail state
                    P   Pass
                    F   Fail
                    -   Not Performed
                    ?   In Process

        RSLT?       Responds with integer indicating fail status
                    0       No failure
                    1       V7X Internal Fault
                    2       Over voltage output
                    4       Line too low to implement configured voltage/current
                    8       DUT Breakdown detected
                    16      HOLD step timeout occured
                    32      User aborted the sequence
                    64      GB step was over-compliance
                    128     Arc Detected
                    256     < maximum limit
                    512     > maximum limit
                    1024    IR test result NOT USED
                    2048    INTERLOCK failure
                    4096    Switch Matrix erroor
                    8192    VX7 Overheated
                    16384   DUT voltage or current could not be controlled
                    32769   Wiring error detected in GB step
                    65536   1. Drive voltage not stabalized during ramp
                            2. Leakage current (or resistance) varying

        State Machine:
            Detect and initalize com port connection
            RUN the test from user input ENTER
            Time delay for test completion
            STAT?
                IF P, print PASS
                IF F, print FAILURE
                    RSLT?, print results

    Author : Paul Farrell (@OMINOUS1) (Paulf@woodway.com)

    LAST DEVELOPED FOR: Python 3.14.2


"""

# ~~~~ Imports ~~~~
import serial
import sys
import time
import config  # custom API for the serial configs to share global serial object
import fnc

isRunningSerialUsb = False

# main running script***********************************************************
def main():
    print("\nScanning for available serial ports...")
    ports = config.list_serial_ports()

    if not ports:
        print("\nNo serial ports found. Check your RS232-to-USB adapter.")
        sys.exit(1)

    print("\nAvailable ports:")
    for i, p in enumerate(ports):
        print(f"{i}: {p}")

    print("\nWhich COMPORT is the Hipot connected to?")
    comport_user_input = input(">> COM")

    print("\nWhat baud rate is the Hipot set at? (Default - 115200)")
    baudrate_user_input = input()

    print("\nWhat timeout will the controller use [s]? (Default 1)")
    timeout_user_input = int(input())

    config.initSerial(comport_user_input,baudrate_user_input,timeout_user_input)

    config.serCfg.open()

    isRunningSerialUsb = True

    if config.serCfg.is_open:
        while isRunningSerialUsb:

            print("\n\n-------------------------")
            print("|\tMain Menu\t|")
            print("-------------------------")
            print("1. Exit\n2. Run Hipot GB and ACW Test\n")

            user_test_choice = input(">> ")

            if user_test_choice == "1":
                print("Operation cancelled by user.")
                print("Closing COM port...")
                config.serCfg.close()
                print("Exiting...")
                isRunningSerialUsb = False

            elif user_test_choice == "2":
                fnc.run()

            else:
                print("Unknown choice.")

    elif not config.serCfg.is_open:
        print("Unable to open com port.\n")

    print("\nPort COM" + comport_user_input + " closed.\nExiting...\n")
    config.serCfg.close()

#*******************************************************************************

if __name__ == "__main__":
    main()
