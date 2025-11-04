"""
A script to list serial ports and identify potential ESP32 devices.
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyserial"
# ]
# ///

# Library
from serial.tools.list_ports import comports
import sys

if __name__ == "__main__":
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)

    for port in comports():
        # ? Maybe show other information from port
        print(f"{port.device} - {port.description}", end="")
        if "CP210" in port.description or "CH340" in port.description:
            print("    🌟 Likely ESP32!")
        print()
