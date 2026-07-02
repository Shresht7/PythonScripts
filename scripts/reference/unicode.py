#!/usr/bin/env -S uv run

"""
Inspect and Search Unicode Characters using Python's unicodedata module.
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "requests",
#   "defcmd @ git+https://github.com/Shresht7/defcmd.git@v0.5.1"
# ]
# ///

import sys
import unicodedata
from defcmd import CLI, Spec
from defcmd.terminal import dim

# HELPER FUNCTIONS
# ----------------

def parse_char(s: str) -> str:
    """Parses a string representation of a character and returns the corresponding character"""
    s = s.strip()

    # If the string is a single character, return it as is
    if len(s) == 1:
        return s

    # The string is a Unicode code point (e.g., "U+1F600")
    if s.upper().startswith("U+"):
        return chr(int(s[2:], 16))
    
    # The string is a hexadecimal representation (e.g., "0x1F600")
    if s.startswith("0x") or s.startswith("0X"):
        return chr(int(s[2:], 16))

    # The string is a decimal representation (e.g., "128512")
    if s.isdigit():
        return chr(int(s))
    
    # If the string has more than one character, return the first character
    if len(s) > 1:
        return s[0]

    # If none of the above conditions are met, raise a ValueError    
    raise ValueError(f"Can't parse {s!r} as a character")


def char_info(ch: str) -> dict:
    """Returns a dictionary containing information about a Unicode character"""
    codepoint = ord(ch)
    try:
        name = unicodedata.name(chr(codepoint))
    except ValueError:
        name = None

    return {
        'codepoint': f"U+{codepoint:04X}",
        'character': ch,
        'name': name,
        'category': unicodedata.category(ch),
        'combining': unicodedata.combining(ch),
        'bidirectional': unicodedata.bidirectional(ch),
        'decomposition': unicodedata.decomposition(ch),
        'decimal': unicodedata.decimal(ch, None),
        'digit': unicodedata.digit(ch, None),
        'numeric': unicodedata.numeric(ch, None),
        'mirrored': unicodedata.mirrored(ch)
    }

# ---
# CLI
# ---

cli = CLI(description=__doc__)

@cli.subcmd(prompt_optional=False)
def info(char: str):
    """Show detailed information about a Unicode character"""
    ch = parse_char(char)
    info = char_info(ch)

    print(f"{info['codepoint']}  {ch}  {info['name'] or '<unnamed>'}")
    print(f"  Combining:        {info['combining']}")
    print(f"  Bidirectional:    {info['bidirectional']}")
    print(f"  Decomposition:    {info['decomposition'] or '<none>'}")
    print(f"  Decimal:          {info['decimal']}")
    print(f"  Digit:            {info['digit']}")
    print(f"  Numeric:          {info['numeric']}")


@cli.subcmd(prompt_optional=False)
def search(query: str, max: int = 20):
    """Search for Unicode characters by name"""
    query = query.lower()
    results = []

    for codepoint in range(sys.maxunicode + 1):
        try:
            name = unicodedata.name(chr(codepoint))
        except ValueError:
            continue

        if query in name.lower():
            results.append((codepoint, name))
            if max > 0 and len(results) >= max:
                break

    for codepoint, name in results:
        print(f"U+{codepoint:04X}  {chr(codepoint)}  {name}")

    if max > 0 and len(results) >= max:
        print(dim(f"  (Showing first {max} results)"))


# ----
# MAIN
# ----

if __name__ == "__main__":
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
