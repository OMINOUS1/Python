"""
    manual.py
    Library for entering a serial number manualy

    Author: Team ESEE [TeamESEE@tapconet.com]

    Dev Notes:
    ----------------------------------------------------------------------------
    LAST DEVELOPED DATE | SOFTWARE VERSION | COMMENTS
    ----------------------------------------------------------------------------
    February 24th 2025  |     v0.0.1       | Initial Commit

"""
import sys
import asyncio
from splash_screen import format

# user input to enter device serial number through comms port
async def serial_number():
    print()
    print()
    print("> Enter the Serial Number of the TAPCO BLE Device or END to exit")

    loop = asyncio.get_running_loop()

    while True:
        data = await loop.run_in_executor(None, sys.stdin.buffer.readline)
        stripped_data = str(data.strip(), encoding ='utf-8')

        if (stripped_data.lower() == "end"):
            print("\n\n\t\t> Exiting . . .")
            sys.exit(1)
        else:
            advertising_name = "tapco_" + str(stripped_data)
            format.print_color("\n\n> Attempting to establish a BLE connection with TAPCO Peripheral: {adv_name}".format(adv_name = advertising_name), format.BLUE)
            return advertising_name
            break

        print("***************************** Cannot get here. *****************************")
        if not data:
            break

# **********************************************
# *------------ END manual.py -----------------*
# **********************************************
