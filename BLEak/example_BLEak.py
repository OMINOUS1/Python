"""
    example_BLEak.py
    BLEak example implemented in Python
    Bluetooth Low Energy platform Agnostic Klient

    Author: Team ESEE [TeamESEE@tapconet.com]

    Dev Notes:
    ----------------------------------------------------------------------------
    LAST DEVELOPED DATE | SOFTWARE VERSION | COMMENTS
    ----------------------------------------------------------------------------
    February 24th 2025  |     v0.0.1       | Initial Commit

"""
import asyncio
import splash_screen
import auto
import manual
import ble

async def example_BLEak():
    splash_screen.display()
    await main()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# *---------------- Public Fxns  --------------*
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
async def main():
    print("> What is the State of the Serial Number?")
    print("---------------------------------------------")
    print("1. Exit")
    print("2. Serial Number stored in software accessible variable")
    print("3. Serial Number requires manual entry through software")
    comm_proto_input = input(">> ")

    if comm_proto_input == "1":
        return

    elif comm_proto_input == "2":
        advertising_name = await auto.serial_number()
        await ble.connection(advertising_name)

    elif comm_proto_input == "3":
        advertising_name = await manual.serial_number()
        await ble.connection(advertising_name)

    else:
        print("Unknown choice.")

if __name__ == "__main__":
    try:
        asyncio.run(example_BLEak())
    except asyncio.CancelledError:
        # task is cancelled on disconnect, so we ignore this error
        pass

# **********************************************
# *-------------- END BLEak.py ----------------*
# **********************************************
