# Python Scripts

A collection of semi-useful python scripts.

## Scripts

### 1. Image Converter

A script to convert images from one format to another, with options for resizing and quality control.

**Location:** `scripts/images/convert.py`

**Usage:**

```sh
python scripts/images/convert.py <input> <output> [-h] [-f FORMAT] [--resize RESIZE] [--quality QUALITY]
```

**Arguments:**
- `input`: Path to the input image file or a glob pattern for multiple files.
- `output`: Path to save the converted image or a directory for bulk conversion.
- `-f, --format FORMAT`: The output format for bulk conversion (e.g., `png`, `jpg`).
- `--resize RESIZE`: Resize the output image to a specific width (maintaining aspect ratio).
- `--quality QUALITY`: Set the quality of the output image (1-100, for JPEG).

**Example:**

```sh
python scripts/images/convert.py "images/*.jpg" "converted/" --format png --resize 800 --quality 85
```

### 2. PDF Extractor

A script to extract text, images, and metadata from PDF files.

**Location:** `scripts/pdf/extract.py`

**Usage:**

```sh
python scripts/pdf/extract.py <input> <output> [-h] [--images] [--metadata]
```

**Arguments:**
- `input`: Path to the input PDF file or a glob pattern for multiple files.
- `output`: Path to the output directory to save the extracted content.
- `--images`: Extract images from the PDF files.
- `--metadata`: Extract metadata from the PDF files.

**Example:**

```sh
python scripts/pdf/extract.py "docs/*.pdf" "extracted_content/" --images --metadata
```

### 3. Collate Images into a PDF

A script to create a PDF file from a collection of images.

**Location:** `scripts/images/create_pdf.py`

**Usage:**

```sh
python scripts/images/create_pdf.py <input> <output> [-h]
```

**Arguments:**
- `input`: Glob pattern for input images (e.g., `"images/*.png"`).
- `output`: Path to the output PDF file.

**Example:**

```sh
python scripts/images/create_pdf.py "scans/*.jpg" "my_document.pdf"
```

## 📕 References 

- [Inline Script Metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata)

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE)
