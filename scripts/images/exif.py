"""
A script to extract EXIF information from an image.

Usage:
```sh
python scripts/images/exif.py <input> [-f FORMAT]
# or interactively:
python scripts/images/exif.py
```

Arguments:
- `input`: Path to the input image file.
- `-f, --format FORMAT`: The output format to use (e.g., `json` or `txt`).

Example:
```sh
python scripts/images/exif.py "images/my_photo.jpg" --format json
```
"""

# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pillow"
# ]
# ///


# Library
import sys
import argparse
import json

from PIL import Image
from PIL.ExifTags import TAGS

# EXIF
# ----

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

def need(value: str | None, label: str, parser: argparse.ArgumentParser) -> str:
    """
    Helper function to ensure a required value is provided, either as an argument or through user input.
    """
    # If a value is already provided (e.g., through command-line arguments), return it as is
    if value:
        return value
    
    # If we're in a non-interactive environment, we can't prompt the user, so we should raise an error
    if not sys.stdin.isatty():
        parser.error(f"Missing required argument: {label}")

    # Prompt the user for input if not provided as an argument
    entered = input(f"{label}: ").strip()
    if not entered:
        parser.error(f"Missing required argument: {label}")

    return entered


def ask_optional_text(label: str) -> str | None:
    """Prompt for an optional text value, allowing the user to leave it blank."""
    entered = input(f"{label} (optional - leave blank for default): ").strip()
    return entered or None

def parse_args():
    should_prompt_for_optional = len(sys.argv) == 1

    parser = argparse.ArgumentParser(
        description="Extract EXIF information from an image.",
        epilog="Example: python exif.py image.jpg",
    )
    parser.add_argument("input", nargs="?", help="Path to the input image file.")
    parser.add_argument('-f', '--format', help="The output format to use. (e.g. json or txt)")
    args = parser.parse_args()

    # Ensure required arguments are provided
    args.input = need(args.input, "Input image file", parser)

    if should_prompt_for_optional and args.format is None:
        args.format = ask_optional_text("Output format")

    return args

def main():
    """Main function to parse arguments and extract EXIF information"""
    args = parse_args()

    info = exif(args.input)
    
    if info:
        if args.format and args.format.lower() == "json":
            print(json.dumps(info, indent=4))
        else:
            for tag, value in info.items():
                print(f"{tag}: {value}")


# The main entrypoint of the script
if __name__ == "__main__":
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)

    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

