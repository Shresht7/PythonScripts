"""
Lookup a word definition using the Free Dictionary API
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "requests"  
# ]
# ///

import sys
import os
import requests
import json

def lookup(word: str):
    """
    Looks up the definition of a word using the Free Dictionary API.
    """
    api_url=f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    return response.json()

def print_definitions(entry):
    """
    Prints the definitions of a word entry.
    """
    word = entry.get("word", "")
    phonetics = entry.get("phonetics", [])
    meanings = entry.get("meanings", [])

    print(f"\n{BOLD}{INVERT} {word} {RESET}")
    if phonetics:
        print(f"\n{CYAN}{DIM}{', '.join(p.get('text', '') for p in phonetics)}{RESET}")
    
    for meaning in meanings:
        part_of_speech = meaning.get("partOfSpeech", "")
        definitions = meaning.get("definitions", [])
        for definition in definitions:
            definition_text = definition.get("definition", "")
            print(f"\n{YELLOW} * {MAGENTA}{DIM}({part_of_speech}){RESET} {definition_text}")
            example = definition.get("example", "")
            if example:
                underlined_example = example.replace(word, f"{BOLD}{UNDERLINE}{word}{RESET}{DIM}{ITALIC}")
                print(f"   {DIM}example: {ITALIC}\"{underlined_example}\"{RESET}")
    print()

# ANSI Escape Codes
BOLD="\033[1m"
DIM="\033[2m"
ITALIC="\033[3m"
UNDERLINE="\033[4m"
INVERT="\033[7m"
YELLOW="\033[33m"
CYAN="\033[36m"
MAGENTA="\033[35m"
RESET="\033[0m"

# MAIN
# ----

if __name__ == "__main__":
    # Check for help flag
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)

    # Check if a word is provided as an argument
    if len(sys.argv) < 2:
        print("Error: Please provide a word to look up.", file=sys.stderr)
        sys.exit(1)

    # Lookup the word provided as an argument
    word = sys.argv[1]
    result = lookup(word)

    # Print the result in JSON format if requested
    if '--json' in sys.argv or '-j' in sys.argv:
        print(json.dumps(result, indent=2))
        sys.exit(0)

    # Print the raw result if requested
    if '--raw' in sys.argv or '-r' in sys.argv:
        print(result)
        sys.exit(0)

    # Print the result
    for entry in result:
        print_definitions(entry)
