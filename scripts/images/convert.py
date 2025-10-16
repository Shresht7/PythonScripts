# /// script
# requires-python = ">=3.11"
# dependencies = [
#   pillow
# ]
# ///

# Library
import os
import sys
import argparse
import glob

from PIL import Image

# CONVERT IMAGE
# -------------

def convert_image(input: str, output: str, resize: int | None = None, quality: int | None = None):
    """
    Converts an image from one format to another, with optional resizing and quality control
    
    #### Parameters:
        `input (str)`: Path to the input image file.
        `output (str)`: Path to save the converted image.
        `resize (int | None)`: The width to resize the image to (maintaining aspect ratio).
        `quality (int | None)`: Set the quality of the output image (1-100, for JPG/JPEG).


    #### Errors:
        FileNotFoundError: If the input file does not exist.
    """

    # Check if the input path actually exists
    if not os.path.exists(input):
        raise FileNotFoundError(f"Input file not found at '{input}'")

    try:
        # Perform the conversion
        with Image.open(input) as img:
            # Resize the image if a width is provided
            if resize:
                width, height = img.size
                aspect_ratio = height / width
                new_width = resize
                new_height = int(new_width * aspect_ratio)
                img = img.resize((new_width, new_height))

            print(f"Converting '{input}' to '{output}'... ", end="")

            # Set quality if provided (for JPEG)
            if quality and output.lower().endswith(('.jpg', '.jpeg')):
                img.save(output, quality=quality)
            else:
                img.save(output)

            print("☑️")

    # If the operation fails, show the error and exit
    except Exception as e:
        print("❌")
        raise e

# MAIN
# ----

def parse_args():
    """Parses the command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Convert an image from one format to another. Can also handle bulk conversion using glob patterns.",
    )
    parser.add_argument("input", help="Path to the input image file or a glob pattern for multiple files.")
    parser.add_argument("output", help="Path to save the converted image or a directory for bulk conversion.")
    parser.add_argument("-f", "--format", help="The output format to use for bulk conversion (e.g., png, jpg).")
    parser.add_argument("-r", "--resize", type=int, help="Resize the output image to a specific width (maintaining aspect ratio).")
    parser.add_argument("-q", "--quality", type=int, help="Set the quality of the output image (1-100, for JPEG).")
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
            convert_image(input_path, output_path, args.resize, args.quality)

        return

    # If there are multiple input files but the output is not a directory, exit
    if len(input_files) > 1:
        print("Error: Multiple input files detected, but the output is not a directory", file=sys.stderr)
        sys.exit(1)

    # Otherwise, convert the single file
    convert_image(input_files[0], args.output, args.resize, args.quality)

# The main entrypoint of the script
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
