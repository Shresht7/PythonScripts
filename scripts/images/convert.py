# Library
import os
import sys
import argparse
import glob

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
        description="Convert an image from one format to another. Can also handle bulk conversion using glob patterns.",
        epilog="Examples:\n  python convert.py input.jpg output.png\n  python convert.py \"images/*.jpg\" converted/ --format png",
    )
    parser.add_argument("input", help="Path to the input image file or a glob pattern for multiple files.")
    parser.add_argument("output", help="Path to save the converted image or a directory for bulk conversion.")
    parser.add_argument("-f", "--format", help="The output format to use for bulk conversion (e.g., png, jpg).")
    return parser.parse_args()

def main():
    """Main function to parse arguments and run the conversion"""
    args = parse_args()

    # Get a list of files to convert
    input_files = glob.glob(args.input)

    # Check if any files were found
    if not input_files:
        print(f"Error: No input files found for pattern '{args.input}'", file=sys.stderr)
        sys.exit(1)

    # If the output is a directory, bulk convert
    if os.path.isdir(args.output):

        # Make sure the format is specified
        if not args.format:
            print("Error: Output format must be specified with --format for bulk conversion", file=sys.stderr)
            sys.exit(1)

        # Create the output directory if it doesn't exist
        os.makedirs(args.output, exist_ok=True)

        # Convert each file
        for input_path in input_files:
            # Create the output path
            basename = os.path.basename(input_path)
            filename, _ = os.path.splitext(basename)
            output_path = os.path.join(args.output, f"{filename}.{args.format}")
            # Convert the image
            convert_image(input_path, output_path)

        return

    # If there are multiple input files but the output is not a directory, exit
    if len(input_files) > 1:
        print("Error: Multiple input files detected, but the output is not a directory", file=sys.stderr)
        sys.exit(1)

    # Otherwise, convert the single file
    convert_image(input_files[0], args.output)

# The main entrypoint of the script
if __name__ == "__main__":
    main()
