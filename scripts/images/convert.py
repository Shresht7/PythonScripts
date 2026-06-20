"""
A script to convert images from one format to another, with options for resizing and quality control.

Usage:
```sh
python scripts/images/convert.py <input> <output> [-h] [-f FORMAT] [--resize RESIZE] [--quality QUALITY]
# or interactively:
python scripts/images/convert.py
```

Arguments:
- `input`: Path to the input image file or a glob pattern for multiple files.
- `output`: Path to save the converted image or a directory for bulk conversion.
- `-f, --format FORMAT`: The output format for bulk conversion (e.g., `png`, `jpg`).
- `--resize RESIZE`: Resize the output image to a specific width (maintaining aspect ratio).
- `--quality QUALITY`: Set the quality of the output image (1-100, for JPEG).

Example:
```sh
python scripts/images/convert.py "images/*.jpg" "converted/" --format png --resize 800 --quality 85
```

or interactively:

```sh
$ python scripts/images/convert.py
Input file or glob pattern: images/*.jpg
Output file or directory: converted/
format (required for directory output, e.g., png, jpg): png
Resize width (optional):
Quality (optional):
Converting 'images/photo1.jpg' to 'converted/photo1.png'... ☑️
...
```
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pillow"
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

# PARSE ARGS
# ----------

def need(value: str | None, label: str, parser: argparse.ArgumentParser) -> str:
    """
    Helper function to ensure a required value is provided, either as an argument or through user input.
    """

    # If the value is already provided, return it as is
    if value:
        return value
    
    # Non-interactive sessions should fail fast instead of waiting for input
    if not sys.stdin.isatty():
        parser.error(f"Missing required argument: {label}")

    # Prompt the user for input if not provided as an argument
    entered = input(f"{label}: ").strip()
    if not entered:
        parser.error(f"Missing required argument: {label}")

    return entered

def need_format(value: str | None) -> str:
    """Prompt for an output format when bulk conversion is requested."""
    if value:
        return value

    if not sys.stdin.isatty():
        print("Error: Output format must be specified with --format for bulk conversion", file=sys.stderr)
        sys.exit(1)

    entered = input("format (required for directory output, e.g., png, jpg): ").strip().lstrip(".")
    if not entered:
        print("Error: Output format must be specified with --format for bulk conversion", file=sys.stderr)
        sys.exit(1)

    return entered

def ask_optional_int(label: str) -> int | None:
    """Prompt for an optional integer value, allowing the user to leave it blank."""
    entered = input(f"{label} (optional - leave blank for default): ").strip()
    if not entered:
        return None

    try:
        return int(entered)
    except ValueError:
        print(f"Error: {label} must be an integer", file=sys.stderr)
        sys.exit(1)

def parse_args():
    """Parses the command-line arguments"""

    should_prompt_for_optional = len(sys.argv) == 1 # No arguments provided, so we will prompt for all values interactively

    parser = argparse.ArgumentParser(
        description="Convert an image from one format to another. Can also handle bulk conversion using glob patterns.",
    )
    parser.add_argument("input", nargs="?", help="Path to the input image file or a glob pattern for multiple files.")
    parser.add_argument("output", nargs="?", help="Path to save the converted image or a directory for bulk conversion.")
    parser.add_argument("-f", "--format", help="The output format to use for bulk conversion (e.g., png, jpg).")
    parser.add_argument("-r", "--resize", type=int, help="Resize the output image to a specific width (maintaining aspect ratio).")
    parser.add_argument("-q", "--quality", type=int, help="Set the quality of the output image (1-100, for JPEG).")
    args = parser.parse_args()

    # Ensure required arguments are provided, prompting the user if necessary
    args.input = need(args.input, "Input file or glob pattern", parser)
    args.output = need(args.output, "Output file or directory", parser)

    # When in interactive mode, also prompt for optional values if they were not provided as arguments
    if should_prompt_for_optional:
        if args.resize is None:
            args.resize = ask_optional_int("Resize width")
        if args.quality is None:
            args.quality = ask_optional_int("Quality")

    # If the output is a directory (or we have multiple input files), we need to ensure the format is specified
    if os.path.isdir(args.output) and not args.format:
        if should_prompt_for_optional and sys.stdin.isatty():
            entered = input("format (required for directory output, e.g., png, jpg): ").strip().lstrip(".")
            if entered:
                args.format = entered
        if not args.format:
            parser.error("Output format must be specified with --format for bulk conversion")

    return args

# MAIN
# ----

def main():
    """Main function to parse arguments and run the conversion"""
    args = parse_args()

    # Get a list of files to convert
    input_files = glob.glob(args.input)

    # Check if any files were found
    if not input_files:
        print(f"Error: No input files found for pattern '{args.input}'", file=sys.stderr)
        sys.exit(1)

    bulk_output = os.path.isdir(args.output) or len(input_files) > 1

    # If the output is a directory, bulk convert
    if bulk_output:

        # Make sure the format is specified
        args.format = need_format(args.format)

        if os.path.exists(args.output) and not os.path.isdir(args.output):
            print(f"Error: Output path exists and is not a directory: '{args.output}'", file=sys.stderr)
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
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)

    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
