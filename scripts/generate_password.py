#!/usr/bin/env -S uv run

"""
Generate cryptographically secure passwords
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#  "defcmd @ git+https://github.com/Shresht7/defcmd.git@v0.5.1"
# ]
# ///

import sys
import secrets
from string import ascii_letters, digits, punctuation
from defcmd import cmd, Spec

from typing import Annotated

@cmd(prompt_optional=False)
def generate_password(

    length: Annotated[int, Spec(
        help="Length of the password to generate",
        short="l",
    )] = 20,

    count: Annotated[int, Spec(
        help="Number of passwords to generate",
        short="c",
    )] = 1,

    numbers: Annotated[bool, Spec(
        help="Include digits in the password",
        short="n",
    )] = True,

    symbols: Annotated[bool, Spec(
        help="Include symbols in the password",
        short="s",
    )] = True,
):
    """Generate cryptographically secure passwords."""

    # Define the character set based on user preferences
    char_set = ascii_letters
    if numbers:
        char_set += digits
    if symbols:
        char_set += punctuation

    # Generate the specified number of passwords
    for _ in range(count):
        password = ''.join(secrets.choice(char_set) for _ in range(length))
        print(password)


if __name__ == "__main__":
    try:
        generate_password.run()
    except Exception as e:
        print(f"\x1b[31mError: {e}\x1b[0m", file=sys.stderr)
        raise SystemExit(1)
