#!/usr/bin/env -S uv run

"""
URL encode and decode data
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#  "defcmd @ git+https://github.com/Shresht7/defcmd.git@v0.5.1"
# ]
# ///

import urllib.parse
from defcmd import CLI


cli = CLI(description=__doc__)

@cli.subcmd
def encode(data: str):
    """URL encode data"""
    encoded_data = urllib.parse.quote(data)
    print(encoded_data)

@cli.subcmd
def decode(data: str):
    """URL decode data"""
    decoded_data = urllib.parse.unquote(data)
    print(decoded_data)


if __name__ == "__main__":
    try:
        cli.run()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
