"""
    serialBle.py
    Testing script for opening BLE NUS GATT service and dumping json packets to test kenobi controller.

    Author : Paul Farrell (@FarrellPaul) (paul.farrell@tapconet.com)

"""
import asyncio
import time
import sys
#import autoTest
#import manualTest
#import eepromTest
#import kashmirJSON as kj # FOR DEBUGGING IN DEVELOP_TEST()
from itertools import count, takewhile
from typing import Iterator
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

isRunningSerialBle = False

async def serial_ble():
    isRunningSerialBle = True
    #kj.comm_state = "comms_ble"

    print()
    #print("> Make Sure you have a 2.4GHz Bluetooth Antenna connected to the RP-SMA port of the DUT")
    #print("> Scanning for TAPCO BLE Advertising Peripherals . . .")
    print("> Scanning for BLE Advertising Peripherals . . .")
    print()

    #devices = await BleakScanner.discover(timeout = 15, service_uuids = [UART_SERVICE_UUID])
    #devices = await BleakScanner.discover(timeout = 15)
    devices = await BleakScanner.discover()

    for device in devices:
        print(device)

    print()
    print()
    print("> Enter the Advertising Name of the BLE Device or END to exit")

#******************************NEW**********************************************
    #BLE addresss
    #target_address = "78:5E:CC:EC:8C:8D"
    #time_out = 15.0

    #print(f"Scanning for device with address: {target_address} ...")
    #device = await BleakScanner.find_device_by_address(
    #    target_address,
    #    timeout=time_out  # seconds
    #)

    #if device:
    #    print(f"✅ Found device: {device.name} ({device.address})")
    #else:
    #    print("❌ Device not found within timeout.")
#*******************************************************************************
    loop = asyncio.get_running_loop()

    while True:
        data = await loop.run_in_executor(None, sys.stdin.buffer.readline)
        stripped_data = str(data.strip(), encoding ='utf-8')

        if (stripped_data.lower() == "end"):
            print("\n\n\t\t> Exiting . . .")
            sys.exit(1)
        else:
            advertising_name = stripped_data
            break

        print("***************************** Cannot get here. *****************************")
        if not data:
            break

    device = await BleakScanner.find_device_by_name(name = advertising_name, timeout = 15)
    #kj.device_kj = device

    if device is None:
        print("\n\n\t\t> Advertising Name: {adv_name} Not Found".format(adv_name = advertising_name))
        sys.exit(1)

    def handle_disconnect(_: BleakClient):
        print("\t\t> Disconnected from: {adv_name}\n\t\t> Bye Felicia.\n\n\n".format(adv_name = advertising_name))

    async with BleakClient(device, disconnected_callback = handle_disconnect) as client:
        kj.client = client

        print("\n\t> Connected To: {adv_name}\n\n".format(adv_name = advertising_name))

        while isRunningSerialBle:
            # Here you can optionally decide full test or cherry picked tests w/ custom payloads.
            print("\n\n-------------------------")
            print("|\tMain Menu\t|")
            print("-------------------------")
            print("1. Exit")
            print("2. Automatic Tests")
            print("3. Manual Tests")
            print("4. EEPROM Tests")
            user_test_choice = input(">> ")

            if user_test_choice == "1":
                await client.disconnect()
                isRunningSerialBle = False
            elif user_test_choice == "2":
                await autoTest.auto_test_menu()
            elif user_test_choice == "3":
                await manualTest.manual_test_menu()
            elif user_test_choice == "4":
                await eepromTest.eeprom_test_menu()
            else:
                print("Unknown choice.")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# *---------------- Public Fxns  --------------*
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# TIP: you can get this function and more from the ``more-itertools`` package.
def sliced(data: bytes, n: int) -> Iterator[bytes]:
    """
    Slices *data* into chunks of size *n*. The last slice may be smaller than
    *n*.
    """
    return takewhile(len, (data[i : i + n] for i in count(0, n)))

async def serial_ble_write(client, payload, delay_seconds: int = 0):
    data_list = []

    def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
        """Simple notification handler which prints the data received."""
        data_list.append(data.decode())
        # print("\t> Received from {char}:\t\t{rx}".format(char=characteristic.description, rx=data.decode()))

    await client.start_notify(UART_TX_CHAR_UUID, notification_handler)
    nus = client.services.get_service(UART_SERVICE_UUID)
    rx_char = nus.get_characteristic(UART_RX_CHAR_UUID)
    for s in sliced(payload, rx_char.max_write_without_response_size):
        await client.write_gatt_char(rx_char, s, response=True)

    await asyncio.sleep(.010)   # sleep to make sure response is not missed
    time.sleep(delay_seconds)  # Additional sleep time, if requested.
    await client.stop_notify(UART_TX_CHAR_UUID)

    string_list = ''.join(data_list)
    print(f"\t> Received {len(string_list)} bytes from NUS UART TX:\t\t{string_list}")
    data_list.clear()

if __name__ == "__main__":
    try:
        asyncio.run(serial_ble())
    except asyncio.CancelledError:
        # task is cancelled on disconnect, so we ignore this error
        pass
