"""
    auto.py
    Library for passing a software accessible serial number

    Author: Team ESEE [TeamESEE@tapconet.com]

    Dev Notes:
    ----------------------------------------------------------------------------
    LAST DEVELOPED DATE | SOFTWARE VERSION | COMMENTS
    ----------------------------------------------------------------------------
    February 24th 2025  |     v0.0.1       | Initial Commit

"""
import asyncio
from splash_screen import format

# pass a known serial number here
def get_serial_number():
    serial_num = "7BC8E7A7"   # pass a known serial number here
    return serial_num

# if serial number is already known and user input is not required
async def serial_number():
    serialNumber = get_serial_number()
    advertising_name = "tapco_" + str(serialNumber)
    format.print_color("\n\n> Attempting to establish a BLE connection with TAPCO Peripheral: {adv_name}".format(adv_name = advertising_name), format.BLUE)
    return advertising_name

# **********************************************
# *-------------- END auto.py -----------------*
# **********************************************
