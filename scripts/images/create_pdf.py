"""
A script to create a PDF file from a collection of images
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
import glob
from defcmd import cmd, Spec
from typing import Annotated

from PIL import Image

@cmd
def main(
        input: Annotated[str, Spec(
            help="Glob pattern for input images (e.g., \"images/*.png\").",
            prompt="Input glob pattern (e.g., \"images/*.png\")",
        )],
    
        output: Annotated[str, Spec(
            help="Path to the output PDF file.",
            prompt="Output PDF path",
        )] = "output.pdf",
    ):

    """A script to create a PDF file from a collection of images."""

    # Get and sort the input files
    input_files = sorted(glob.glob(input))

    if not input_files:
        print(f"\x1b[31mError: No input files found for pattern '{input}'\x1b[0m", file=sys.stderr)
        raise SystemExit(1)

    create_pdf(input_files, output)

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

# MAIN
# ----

# The main entrypoint of the script
if __name__ == "__main__":
    main.run()
