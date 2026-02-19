"""
    ble.py
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
from itertools import count, takewhile
from typing import Iterator
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from splash_screen import format

NUS_UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
NUS_UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
NUS_UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

isRunningBle = False

# TIP: you can get this function and more from the ``more-itertools`` package.
def sliced(data: bytes, n: int) -> Iterator[bytes]:
    """
    Slices *data* into chunks of size *n*. The last slice may be smaller than
    *n*.
    """
    return takewhile(len, (data[i : i + n] for i in count(0, n)))

# BLE write and read from NUS SERVICE UUID
async def ble_write(client, payload):
    data_list = []

    def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
        """Simple notification handler which appends the data received."""
        data_list.append(data.decode())

    await client.start_notify(NUS_UART_TX_CHAR_UUID, notification_handler)
    nus = client.services.get_service(NUS_UART_SERVICE_UUID)
    rx_char = nus.get_characteristic(NUS_UART_RX_CHAR_UUID)
    for s in sliced(payload, rx_char.max_write_without_response_size):
        await client.write_gatt_char(rx_char, s, response=True)

    await asyncio.sleep(.010)   # sleep to make sure response is not missed
    await client.stop_notify(NUS_UART_TX_CHAR_UUID)

    string_list = ''.join(data_list)
    format.print_color(f"\n\t> Received {len(string_list)} bytes from NUS UART TX:\n\t{string_list}", format.GREEN)
    data_list.clear()

# BLE custum payload menu
async def custom_payload_menu():
    format.print_color("\n\n**************Custom Payload Format****************", format.YELLOW)
    format.print_color("\nJSON Structure", format.YELLOW)
    format.print_color('\nRead-All Values: {"group":""}', format.YELLOW)
    format.print_color('\nReading Specific Values: {"group":{"field":""}}', format.YELLOW)
    format.print_color('\nWriting Specific Values: {"group":{"field":"value"}}', format.YELLOW)
    format.print_color('\nExamples:', format.YELLOW)
    format.print_color('\n\t{"deviceStatus":""}', format.YELLOW)
    format.print_color('\n\t{"deviceInfo":{"serialNumber":""}}', format.YELLOW)
    format.print_color('\n\t{"deviceSetup":{"deviceType":"blinkersign"}}', format.YELLOW)
    format.print_color("\n\n***************************************************", format.YELLOW)

# BLE custum payload write
async def custom_payload(client):
    while True:
        print("\nEnter your custom JSON || TPP payload, or type END to exit.")
        user_payload = input(">> ")

        # custom test loop termination.
        # The only payload you can't send the micro is any variation of "end"
        if user_payload.lower() == "end":
            break

        payload = bytes(user_payload, "utf-8")
        format.print_color("\n\t> BLE Packet Sent:\n\t{tx}".format(tx=payload.decode()), format.BLUE)
        await ble_write(client, payload)

# BLE connection
async def connection(advertising_name):
    isRunningBle = True
    device = await BleakScanner.find_device_by_name(name = advertising_name, timeout = 15)

    if device is None:
        format.print_color("\n\n> Advertising Name: {adv_name} Not Found".format(adv_name = advertising_name), format.RED)
        sys.exit(1)

    def handle_disconnect(_: BleakClient):
        format.print_color("\n\n> Disconnected and unpaired from: {adv_name}\n\t\t> Bye Felicia.\n\n\n".format(adv_name = advertising_name), format.RED)

    async with BleakClient(device, disconnected_callback = handle_disconnect) as client:
        await client.pair()
        format.print_color("\n\n> Connected and paired to: {adv_name}".format(adv_name = advertising_name), format.GREEN)
        format.print_color("> On-Board BLE Status LED illuminated solid RED", format.GREEN)
        format.print_color("> BLE Security Level 2 - Encyrpted and Unathenticated", format.GREEN)
        while isRunningBle:
            # Here you can optionally decide full test or cherry picked tests w/ custom payloads.
            format.print_color("\n\n-------------------------", format.BLUE)
            format.print_color("|\tBLE Main Menu\t|", format.BLUE)
            format.print_color("-------------------------", format.BLUE)
            print("1. Disconnect\n2. Enter Custom Payload")
            user_test_choice = input(">> ")

            if user_test_choice == "1":
                await client.disconnect()
                await client.unpair()
                isRunningBle = False

            elif user_test_choice == "2":
                await custom_payload_menu()
                await custom_payload(client)

            else:
                print("Unknown choice.")

# **********************************************
# *-------------- END ble.py ------------------*
# **********************************************
