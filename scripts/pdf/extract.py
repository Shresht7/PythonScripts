"""
A script to extract text, images, and metadata from PDF files
"""

# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pypdf",
#   "pillow",
#   "defcmd @ git+https://github.com/Shresht7/defcmd.git@v0.5.1"
# ]
# ///


# Library
import os
import sys
import glob
import json
from defcmd import cmd, Spec
from pypdf import PdfReader
from typing import Annotated

# EXTRACT TEXT
# ------------

def extract_text(input_path: str, output_dir: str):
    """
    Extracts all text from a given PDF file and saves it to a text file.

    The text file will has the same name as the input PDF, but with a `.txt` extension.
    It is saved in the specified output directory.

    #### Parameters:
        `input_path (str)`: The path to the input PDF file.
        `output_dir (str)`: The directory where the output text file will be saved.

    #### Errors:
        Propagate exceptions from the `pypdf` library or file system operations to be handled by the caller.
    """
    reader = PdfReader(input_path)

    # Extract text from each page
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    # Create the output path
    basename = os.path.basename(input_path)
    filename, _ = os.path.splitext(basename)
    output_path = os.path.join(output_dir, f"{filename}.txt")

    # Save the text to a file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Successfully extracted text from '{input_path}' to '{output_path}'")

# EXTRACT IMAGES
# --------------

def extract_images_from_pdf(input_path: str, output_dir: str):
    """
    Extracts all images from a given PDF file and saves them to a directory.

    The images are saved in the specified output directory. The directory will be
    created if it does not exist.

    #### Parameters:
        `input_path (str)`: The path to the input PDF file.
        `output_dir (str)`: The directory where the extracted images will be saved.

    #### Errors:
        Propagate exceptions from the `pypdf` library or file system operations to be handled by the caller.
    """
    reader = PdfReader(input_path)
    
    # Create the output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Extract images from the PDF pages and write them to disk
    image_count = 0
    for page_num, page in enumerate(reader.pages):
        for image_file_object in page.images:
            with open(os.path.join(output_dir, f"page{page_num+1}_{image_file_object.name}"), "wb") as fp:
                fp.write(image_file_object.data)
                image_count += 1
    
    if image_count > 0:
        print(f"Successfully extracted {image_count} images from '{input_path}' to '{output_dir}'")

# EXTRACT METADATA
# ----------------

def extract_metadata(input_path: str, output_dir: str):
    """
    Extracts metadata from a given PDF file and saves it to a JSON file.

    The metadata is saved in a JSON file with the same name as the input PDF,
    but with a `.metadata.json` extension. The file will be saved in the
    specified output directory.

    #### Parameters:
        `input_path (str)`: The path to the input PDF file.
        `output_dir (str)`: The directory where the output JSON file will be saved.

    #### Errors:
        Propagate exceptions from the `pypdf` library or file system operations to be handled by the caller.
    """
    reader = PdfReader(input_path)

    # Retrieve the metadata from the PDF reader
    metadata = reader.metadata

    # Parse it into a dictionary    
    meta_dict = {}
    if metadata:
        for key, value in metadata.items():
            meta_dict[key] = str(value)

    if not meta_dict:
        print(f"No metadata found for '{input_path}'")
        return

    # Create the output path
    basename = os.path.basename(input_path)
    filename, _ = os.path.splitext(basename)
    output_path = os.path.join(output_dir, f"{filename}.metadata.json")

    # Save the metadata to a JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(meta_dict, f, indent=4)

    print(f"Successfully extracted metadata from '{input_path}' to '{output_path}'")

# MAIN
# ----

@cmd(epilog="Example: python extract.py \"docs/*.pdf\" extracted_content/ --images --metadata")
def main(
        input: Annotated[str, Spec(help="Path or glob pattern for input PDF files")],
        output: Annotated[str, Spec(help="Path to the output directory to save the extracted content")],
        images: Annotated[bool, Spec(help="Extract images from the PDF files")] = True,
        metadata: Annotated[bool, Spec(help="Extract metadata from the PDF files")] = True,
    ):
    """Extract text, images, and metadata from PDF files"""

    # Get a list of input files
    input_files = glob.glob(input)

    # Check if any files were found
    if not input_files:
        print(f"Error: No input files found for pattern '{input}'", file=sys.stderr)
        sys.exit(1)

    # Create the output directory if it doesn't exist
    os.makedirs(output, exist_ok=True)

    # Process each file
    for input_file in input_files:
        if input_file.lower().endswith(".pdf"):
            # Extract text
            extract_text(input_file, output)

            # Extract images if requested
            if images:
                basename = os.path.basename(input_file)
                filename, _ = os.path.splitext(basename)
                image_output_dir = os.path.join(output, filename)
                extract_images_from_pdf(input_file, image_output_dir)

            # Extract metadata if requested
            if metadata:
                extract_metadata(input_file, output)
        else:
            print(f"Skipping non-PDF file: '{input_file}'", file=sys.stderr)

# The main entrypoint of the script
if __name__ == "__main__":
    main.run()
