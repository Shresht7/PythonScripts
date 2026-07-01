"""
A script to convert images from one format to another, with options for resizing and quality control
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pillow",
#  "defcmd @ git+https://github.com/Shresht7/defcmd.git@v0.5.1"
# ]
# ///

# Library
import os
import sys
from defcmd import cmd, Spec
import glob

from PIL import Image

from typing import Literal, Annotated

# CONVERT IMAGE
# -------------

def convert_image(input: str, output: str, resize: int | None = None, quality: int | None = None):
    """
    Converts an image from one format to another, with optional resizing and quality control.

    This function takes an input image and converts it to the desired output format.
    It can also resize the image and adjust the quality for JPEG files.

    #### Parameters:
        `input (str)`: Path to the input image file.
        `output (str)`: Path to save the converted image.
        `resize (int | None)`: The width to resize the image to (maintaining aspect ratio).
        `quality (int | None)`: Set the quality of the output image (1-100, for JPG/JPEG).

    #### Errors:
        Propagate exceptions from the Pillow library or file system operations to be handled by the caller.
    """

    # Check if the input path actually exists
    if not os.path.exists(input):
        raise FileNotFoundError(f"Input file not found at '{input}'")

    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

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

# MAIN
# ----

@cmd(epilog="Example: python scripts/images/convert.py 'images/*.jpg' 'converted/' --format png --resize 800 --quality 85")
def main(
        input: Annotated[str, Spec(help="Path to the input image file or a glob pattern for multiple files.")],
        output: Annotated[str, Spec(help="Path to save the converted image or a directory for bulk conversion.")],
        format: Annotated[Literal["png", "jpg", "jpeg", "bmp", "gif"] | None, Spec(short="f", help="The output format for bulk conversion.")] = None,
        resize: Annotated[int | None, Spec(short="r", help="Resize the output image to a specific width (maintaining aspect ratio).", prompt=False)] = None,
        quality: Annotated[int | None, Spec(short="q", help="Set the quality of the output image (1-100, for JPEG).", prompt=False)] = None
):
    """Main function to parse arguments and run the conversion"""

    # Get a list of files to convert
    input_files = glob.glob(input)

    # Check if any files were found
    if not input_files:
        print(f"Error: No input files found for pattern '{input}'", file=sys.stderr)
        sys.exit(1)

    bulk_output = os.path.isdir(output) or len(input_files) > 1

    # If the output is a directory, bulk convert
    if bulk_output:

        if os.path.exists(output) and not os.path.isdir(output):
            print(f"Error: Output path exists and is not a directory: '{output}'", file=sys.stderr)
            sys.exit(1)

        if not format:
            print("Error: Output format must be specified with --format for bulk conversion", file=sys.stderr)
            sys.exit(1)

        # Create the output directory if it doesn't exist
        os.makedirs(output, exist_ok=True)

        # Convert each file
        for input_path in input_files:
            # Create the output path
            basename = os.path.basename(input_path)
            filename, _ = os.path.splitext(basename)
            output_path = os.path.join(output, f"{filename}.{format}")
            # Convert the image
            convert_image(input_path, output_path, resize, quality)

        return

    # If there are multiple input files but the output is not a directory, exit
    if len(input_files) > 1:
        print("Error: Multiple input files detected, but the output is not a directory", file=sys.stderr)
        sys.exit(1)

    # Otherwise, convert the single file
    convert_image(input_files[0], output, resize, quality)

# The main entrypoint of the script
if __name__ == "__main__":
    main.run()
