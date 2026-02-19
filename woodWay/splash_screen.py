import asyncio
import climage
from climage import color_to_flags, color_types, convert
from PIL import Image


import os
import subprocess
from sys import stdout

version_number : str = "0.0.0.1"

#enable_color: bool = False
enable_color: bool = True

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

class company_logo:
    def draw_image(self):
        global enable_color
        if enable_color:
            print(format.CLEAR_SCREEN, end="")

            #does not look good so getting removed
            #filename_logo = 'C:/PYTHON/woodWay/woodway_logo.png'

            # color_to_flags allows you to easily define the color option required by
            # convert. Accepts a value from the `color_types` enum, which has the following
            # options:
            #   - color_types.truecolor
            #   - color_types.color256
            #   - color_types.color16
            #   - color_types.color8
            #image_logo = climage.convert(filename_logo, is_unicode=True, **color_to_flags(color_types.truecolor))
            #image_logo = climage.convert(filename_logo, is_unicode=True, width=50)
            #print(image_logo)

    class ascii_art:
        arrow = [
            r"     __    ",
            r"     \ \   ",
            r" _____\ \  ",
            r"|_____   > ",
            r"      / /  ",
            r"     /_/   "
        ]
        woodway = [
            r"___      ___      ___   ______     ______    ______    ___      ___      ___    ___    ___     ___",
            r"\  \    /   \    /  /  /  __  \   /  __  \  |   __  \  \  \    /   \    /  /   /   \   \  \   /  /",
            r" \  \  /  ^  \  /  /  |  |  |  | |  |  |  | |  |  |  |  \  \  /  ^  \  /  /   /  ^  \   \  \ /  / ",
            r"  \  \/  / \  \/  /   |  |  |  | |  |  |  | |  |  |  |   \  \/  / \  \/  /   /  /_\  \    \   /   ",
            r"   \    /   \    /    |  `--`  | |  `--`  | |  `--`  |    \    /   \    /   /  _____  \    |  |   ",
            r"    \__/     \__/      \______/   \______/  |_______/      \__/     \__/   /__/     \__\   |__|   "
        ]

    def display(self):
        global enable_color
        ascii_art = self.__class__.ascii_art()
        format_arrow: str = ""
        format_woodway: str = ""
        format_end: str = ""
        if enable_color:
            format_arrow = format.BOLD + format.GREEN;
            format_woodway = format.BOLD + format.BLUE
            format_end = format.END

        display_list: list[str] = []
        for index, item in enumerate(ascii_art.arrow):
            line: str = ""
            line += format_arrow
            line += str(item)
            line += format_end
            display_list.append(line)

        for index, item in enumerate(ascii_art.woodway):
            line: str = ""
            line += format_woodway
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
    format.print_underline( "WOODWAY USA, Inc. Payload testing utility")
    print("NOTE:  This is a Windows specific application.")
    print(f"Version: {version_number}")
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
