# Python Scripts

A collection of semi-useful Python utility scripts. 

## Usage

```sh
uv run scripts/<path/to/script>.py <arguments>
```

Or with Python directly if dependencies are installed:

```sh
python scripts/<path/to/script>.py <arguments>
```

## Scripts

### Encoding

| Script                       | Description                                  |
| ---------------------------- | -------------------------------------------- |
| `encoding/convert-base64.py` | Encode/decode Base64 (standard and URL-safe) |
| `encoding/convert-url.py`    | URL-encode and URL-decode strings            |

### Images

| Script                 | Description                                                     |
| ---------------------- | --------------------------------------------------------------- |
| `images/convert.py`    | Convert images between formats with optional resize and quality |
| `images/create_pdf.py` | Combine multiple images into a single PDF                       |
| `images/exif.py`       | Extract EXIF metadata from image files                          |

### PDF

| Script           | Description                                       |
| ---------------- | ------------------------------------------------- |
| `pdf/extract.py` | Extract text, images, and metadata from PDF files |

### Reference

| Script                    | Description                                          |
| ------------------------- | ---------------------------------------------------- |
| `reference/dictionary.py` | Look up word definitions via the Free Dictionary API |

### Utility

| Script                 | Description                                  |
| ---------------------- | -------------------------------------------- |
| `generate_password.py` | Generate cryptographically secure passwords  |
| `find_esp32.py`        | List serial ports and identify ESP32 devices |

## Development

Run `uv sync` to install all script dependencies into `.venv` for IDE support
(autocomplete, type checking, linting).

Each script uses [PEP 723 inline script metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/) to declare its own dependencies, so they can be run independently without a global install.

## License

[MIT](./LICENSE)
