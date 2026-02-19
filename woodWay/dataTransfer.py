'''
Prints the main menu
'''
import asyncio
import splash_screen

#import serialUsb
import serialBle


# |/\/\/\/ MAIN \/\/\/\| #
async def main():
    splash_screen.display()

    print("> Which Communication Protocol is being used?")
    print("---------------------------------------------")
    print("1. Exit")
    print("2. Serial over USB")
    print("3. Serial over BLE")
    comm_proto_input = input(">> ")

    if comm_proto_input == "1":
        return
    #elif comm_proto_input == "2":
    #    await serialUsb.serial_usb()
    elif comm_proto_input == "3":
        await serialBle.serial_ble()
    else:
        print("Unknown choice.")

# Calling it like this lets you order functions differently above.
if __name__ == "__main__":
    asyncio.run(main())
