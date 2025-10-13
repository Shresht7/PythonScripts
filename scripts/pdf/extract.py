# Library
import os
import sys
import argparse
import glob

from pypdf import PdfReader

# EXTRACT TEXT
# ------------

def extract_text(input_path: str, output_dir: str):
    """Extracts text from a PDF and saves it to a text file."""
    try:
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

    except Exception as e:
        print(f"Error extracting text from '{input_path}': {e}", file=sys.stderr)

# MAIN
# ----

def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract text from PDF files.",
        epilog="Example: python extract.py \"docs/*.pdf\" extracted_text/",
    )
    parser.add_argument("input", help="Path to the input PDF file or a glob pattern for multiple files.")
    parser.add_argument("output", help="Path to the output directory to save the text files.")
    return parser.parse_args()

def main():
    """Main function to parse arguments and run the extraction."""
    args = parse_args()

    # Get a list of input files
    input_files = glob.glob(args.input)

    # Check if any files were found
    if not input_files:
        print(f"Error: No input files found for pattern '{args.input}'", file=sys.stderr)
        sys.exit(1)

    # Create the output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    # Process each file
    for input_file in input_files:
        if input_file.lower().endswith(".pdf"):
            extract_text(input_file, args.output)
        else:
            print(f"Skipping non-PDF file: '{input_file}'", file=sys.stderr)

# The main entrypoint of the script
if __name__ == "__main__":
    main()
