# /// script
# requires-python = ">=3.11"
# dependencies = [
#   pillow
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
    """Extract EXIF information from the given image"""
    try:
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
    
    # If the operation fails, show error and exit
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

# MAIN
# ----

def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract EXIF information from an image.",
        epilog="Example: python exif.py image.jpg",
    )
    parser.add_argument("input", help="Path to the input image file.")
    parser.add_argument('-f', '--format', help="The output format to use. (e.g. json or txt)")
    return parser.parse_args()

def main():
    """Main function to parse arguments and extract EXIF information"""
    args = parse_args()

    info = exif(args.input)
    
    if info:
        if args.format == "json":
            print(json.dumps(info, indent=4))
        else:
            for tag, value in info.items():
                print(f"{tag}: {value}")


# The main entrypoint of the script
if __name__ == "__main__":
    main()
