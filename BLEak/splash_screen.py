"""
    splash_screen.py
    Library containing terminal colors and initial display information

    Author: Team ESEE [TeamESEE@tapconet.com]

    Dev Notes:
    ----------------------------------------------------------------------------
    LAST DEVELOPED DATE | SOFTWARE VERSION | COMMENTS
    ----------------------------------------------------------------------------
    February 24th 2025  |     v0.0.1       | Initial Commit

"""
import asyncio
import climage
import os
import subprocess
from sys import stdout

enable_color: bool = False

# Terminal Formatting (ANSI)
class format:
    PURPLE: str = "\033[95m"
    CYAN: str = "\033[96m"
    DARKCYAN: str = "\033[36m"
    BLUE: str = "\033[94m"
    GREEN: str = "\033[92m"
    YELLOW: str = "\033[93m"
    RED: str = "\033[91m"
    BOLD: str = "\033[1m"
    UNDERLINE: str = "\033[4m"
    END: str = "\033[0m"
    CLEAR_SCREEN: str = "\033[2J"

    def print_underline(string: str):
        global enable_color
        format_underline: str = ""
        format_end: str = ""
        if enable_color:
            format_underline = format.UNDERLINE
            format_end = format.END
        print(format_underline, end="")
        print(string)
        print(format_end, end="")

    def print_color(string: str, color):
        global enable_color
        format_color: str = ""
        format_end: str = ""
        if enable_color:
            format_color = color
            format_end = format.END
        print(format_color, end="")
        print(string)
        print(format_end, end="")

class company_logo:
    def draw_image(self):
        global enable_color
        if enable_color:
            print(format.CLEAR_SCREEN, end="")

    class ascii_art:
        arrow = [
            r"     __    ",
            r"     \ \   ",
            r" _____\ \  ",
            r"|_____   > ",
            r"      / /  ",
            r"     /_/   "
        ]
        tapco = [
            r".___________.   ___      .______     ______    ______      ",
            r"|           |  /   \     |   _  \   /      |  /  __  \     ",
            r"`---|  |----` /  ^  \    |  |_)  | |  ,----` |  |  |  |    ",
            r"    |  |     /  /_\  \   |   ___/  |  |      |  |  |  |    ",
            r"    |  |    /  _____  \  |  |      |  `----. |  `--`  |    ",
            r"    |__|   /__/     \__\ | _|       \______|  \______/     "
        ]
        ble = [
            r"     ________     ___            ____________ ",
            r"    |    _    \  |   |          |    ________|",
            r"    |   |_)   /  |   |          |   |________ ",
            r"    |    _    \  |   |          |    ________|",
            r"    |   |_)    | |   \-------\  |   |________ ",
            r"    |________ /  |___________|  |____________|"
        ]

    def display(self):
        global enable_color
        ascii_art = self.__class__.ascii_art()
        format_arrow: str = ""
        format_tapco: str = ""
        format_ble: str = ""
        format_end: str = ""
        if enable_color:
            format_arrow = format.BOLD + format.YELLOW;
            format_tapco = format.BOLD + format.BLUE
            format_ble = format.BOLD + format.BLUE
            format_end = format.END

        display_list: list[str] = []
        for index, item in enumerate(ascii_art.arrow):
            line: str = ""
            line += format_arrow
            line += str(item)
            line += format_end
            display_list.append(line)

        for index, item in enumerate(ascii_art.tapco):
            line: str = ""
            line += format_tapco
            line += str(item)
            line += format_end
            display_list[index] += line

        for index, item in enumerate(ascii_art.ble):
            line: str = ""
            line += format_ble
            line += str(item)
            line += format_end
            display_list[index] += line

        for item in display_list:
            print(item)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# *---------------- Public Fxns  --------------*
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def print_menu():
    logo = company_logo()
    logo.draw_image()
    logo.display()

    print()
    format.print_underline( "JSON || TPP BLE Payload testing utility")
    print()
    format.print_color("NOTE:  This is a Windows specific application.", format.PURPLE)
    format.print_color("Developed by Traffic and Parking Company, LLC [TAPCO].", format.CYAN)
    format.print_color("This software implements Bluetooth Low Energy platform Agnostic Klient [BLEak]", format.DARKCYAN)
    format.print_color("BLEak is a GATT client software, capable of connecting to BLE devices acting as GATT servers.", format.BLUE)
    format.print_color("TAPCO BLE Software Version v0.0.1", format.GREEN)
    format.print_color("Safe Travels...", format.YELLOW)
    print()
    print()
    format.print_color("> Make Sure you have a 2.4GHz Bluetooth Antenna connected to the RP-SMA port of the DUT", format.RED)
    print()

def powershell_supports_virtual_terminal() -> bool:
    try:
        result = subprocess.run(
            ["powershell", "-Command", "$Host.UI.SupportsVirtualTerminal"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().lower() == "true"
    except subprocess.CalledProcessError:
        return False

def terminal_auto_detect():
    global enable_color
    is_command_promt = (os.getenv('PROMPT', '') == '$P$G')
    is_powershell = (False == is_command_promt)
    if is_powershell:
        enable_color = powershell_supports_virtual_terminal()

def display():
    terminal_auto_detect()
    print_menu()

# **********************************************
# *---------- END splash_screen.py ------------*
# **********************************************
