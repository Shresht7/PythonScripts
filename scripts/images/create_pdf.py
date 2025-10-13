# Library
import os
import sys
import argparse
import glob

from PIL import Image

# CREATE PDF
# ----------

def create_pdf(image_files: list[str], output_path: str):
    """Creates a PDF from a list of image files."""
    try:
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

    except Exception as e:
        print(f"Error creating PDF: {e}", file=sys.stderr)

# MAIN
# ----

def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a PDF from a collection of images.",
        epilog="Example: python create_pdf.py \"images/*.png\" my_album.pdf",
    )
    parser.add_argument("input", help="Glob pattern for input images (e.g., \"images/*.png\").")
    parser.add_argument("output", help="Path to the output PDF file.")
    return parser.parse_args()

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
    main()
