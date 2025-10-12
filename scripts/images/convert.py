# Library
import os
import sys
import argparse

from PIL import Image

# CONVERT IMAGE
# -------------

def convert_image(input: str, output: str):
    """Converts an image from one format to another"""
    try:
        # Check if the input path actually exists
        if not os.path.exists(input):
            print(f"Error: Input file not found at '{input}'", file=sys.stderr)
            sys.exit(1)

        # Perform the conversion
        with Image.open(input) as img:
            print(f"Converting '{input}' to '{output}'... ", end="")
            img.save(output)
            print("Conversion Successful ☑️")

    # If the operation fails, show the error and exit
    except Exception as e:
        print("Conversion Failed ❌")
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

# MAIN
# ----

def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert an image from one format to another",
        epilog="Example: python convert.py input.jpg output.png"
    )
    parser.add_argument("input", help="Path to the input image file")
    parser.add_argument("output", help="Path to save the converted image")
    return parser.parse_args()

def main():
    """Main function to parse arguments and run the conversion"""
    args = parse_args()
    convert_image(args.input, args.output)

# The main entrypoint of the script
if __name__ == "__main__":
    main()
