#!/usr/bin/env -S uv run

"""
A script to extract EXIF information from an image
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pillow",
#   "defcmd @ git+https://github.com/Shresht7/defcmd.git@v0.5.1"
# ]
# ///

# Library
import sys
from PIL import Image
from PIL.ExifTags import TAGS
import json
from defcmd import cmd, Spec
from typing import Literal, Annotated
from pathlib import Path

# EXIF
# ----

@cmd
def main(
        path: Annotated[Path, Spec(
            help="Path to the image file",
            validate=lambda p: p.is_file()
        )],
        
        format: Annotated[Literal["json", "text"], Spec(
            short="f",
            help="The output format for EXIF information",
        )] = "text",
    ):

    """Extract EXIF information from an image"""

    # Extract EXIF info from the image
    exif_info = exif(str(path))

    # If no EXIF info is found, exit silently
    if not exif_info:
        return

    # Output the EXIF info in the desired format    
    if format == "json":
        print(json.dumps(exif_info, indent=4))
    else:
        for tag, value in exif_info.items():
            print(f"{tag}: {value}")


def exif(path: str):
    """
    Extracts EXIF information from the given image.

    This function opens an image file, extracts its EXIF metadata, and returns it as a dictionary.
    It handles different data types, including byte strings, to ensure the output is clean.

    #### Parameters:
        `path (str)`: The path to the input image file.

    #### Returns:
        `dict`: A dictionary containing the EXIF data, where keys are the tag names and values are the corresponding values.

    #### Errors:
        Propagate exceptions from the Pillow library or file system operations to be handled by the caller.
    """
    ret = {}
    with Image.open(path) as img:
        info = img._getexif()
        if info:
            for tag, value in info.items():
                tag_name = TAGS.get(tag, tag)
                if isinstance(value, bytes):
                    # For bytes, try to decode, otherwise store as repr
                    try:
                        ret[tag_name] = value.decode('utf-8')
                    except UnicodeDecodeError:
                        ret[tag_name] = repr(value)
                else:
                    ret[tag_name] = value
    return ret

# MAIN
# ----

# The main entrypoint of the script
if __name__ == "__main__":
    try:
        main.run()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
