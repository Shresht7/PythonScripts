"""
A script to create a PDF file from a collection of images.

Usage:
```sh
python scripts/images/create_pdf.py <input> <output> [-h]
# or interactively:
python scripts/images/create_pdf.py
```

Arguments:
- `input`: Glob pattern for input images (e.g., `"images/*.png"`).
- `output`: Path to the output PDF file.

Example:
```sh
python scripts/images/create_pdf.py "scans/*.jpg" "my_document.pdf"
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
import glob

from PIL import Image

# CREATE PDF
# ----------

def create_pdf(image_files: list[str], output_path: str):
    """
    Creates a PDF from a list of image files.

    This function takes a list of image file paths and combines them into a single PDF document.
    The images are appended in the order they appear in the input list.

    #### Parameters:
        `image_files (list[str])`: A list of paths to the image files.
        `output_path (str)`: The path to save the output PDF file.

    #### Errors:
        `FileNotFoundError`: If any of the input image files cannot be found.
        `Exception`: Catches and reports other potential errors during PDF creation.
    """
    # Ensure there are images to process
    if not image_files:
        print("No image files found.", file=sys.stderr)
        return

    # Open all images
    images = [Image.open(f) for f in image_files]

    # Get the first image
    first_image = images[0]

    # Get the rest of the images
    other_images = images[1:]

    # Save the first image as a PDF, and append the rest
    first_image.save(output_path, "PDF", resolution=100.0, save_all=True, append_images=other_images)

    print(f"Successfully created PDF: {output_path} ☑️")

# PARSE ARGS
# ----------

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

def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a PDF from a collection of images.",
        epilog="Example: python create_pdf.py \"images/*.png\" my_album.pdf",
    )
    parser.add_argument("input", nargs="?", help="Glob pattern for input images (e.g., \"images/*.png\").")
    parser.add_argument("output", nargs="?", help="Path to the output PDF file.")
    args = parser.parse_args()

    # Ensure required arguments are provided
    args.input = need(args.input, "Input glob pattern", parser)
    args.output = need(args.output, "Output PDF path", parser)

    return args

# MAIN
# ----

def main():
    """Main function to parse arguments and run the PDF creation."""
    args = parse_args()

    # Get and sort the input files
    input_files = sorted(glob.glob(args.input))

    if not input_files:
        print(f"Error: No input files found for pattern '{args.input}'", file=sys.stderr)
        sys.exit(1)

    create_pdf(input_files, args.output)

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
