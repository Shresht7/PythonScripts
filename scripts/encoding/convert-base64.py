#!/usr/bin/env -S uv run

"""
Encode and decode data with Base64
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#  "defcmd @ git+https://github.com/Shresht7/defcmd.git@v0.5.1"
# ]
# ///

import sys
import base64
from defcmd import CLI


cli = CLI(description=__doc__)

@cli.subcmd(aliases=["enc"], prompt_optional=False)
def encode(data: str, url_safe: bool = False):
    """Encode data in Base64"""
    bytes = data.encode('utf-8')
    encoder = base64.urlsafe_b64encode if url_safe else base64.b64encode
    encoded_data = encoder(bytes).decode('utf-8')
    print(encoded_data)

@cli.subcmd(aliases=["dec"], prompt_optional=False)
def decode(data: str, url_safe: bool = False):
    """Decode Base64 data"""
    bytes = data.encode('utf-8')
    decoder = base64.urlsafe_b64decode if url_safe else base64.b64decode
    decoded_data = decoder(bytes).decode('utf-8')
    print(decoded_data)


if __name__ == "__main__":
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
