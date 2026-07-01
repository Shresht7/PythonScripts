"""
Lookup a word definition using the Free Dictionary API (https://dictionaryapi.dev/)
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "requests",
#   "defcmd @ git+https://github.com/Shresht7/defcmd.git@v0.5.1"
# ]
# ///

import sys
import os
import requests
import json
from defcmd import cmd, Spec
from typing import Literal, Annotated


def lookup(word: str):
    """Looks up the definition of a word using the Free Dictionary API"""
 
    api_url=f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)

    if response.status_code != 200:
        print(f"Error: Unable to fetch definition for '{word}'. HTTP Status Code: {response.status_code}", file=sys.stderr)
        print(f"Response: {response.text}", file=sys.stderr)
        sys.exit(1)

    return response.json()


def print_definitions(entry):
    """Prints the definitions of a word entry"""

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

            synonyms = definition.get("synonyms", [])
            if synonyms:
                print(f"   {DIM}synonyms: {GREEN}{', '.join(synonyms)}{RESET}")
            antonyms = definition.get("antonyms", [])
            if antonyms:
                print(f"   {DIM}antonyms: {RED}{', '.join(antonyms)}{RESET}")
    print()


# ANSI Escape Codes
BOLD="\033[1m"
DIM="\033[2m"
ITALIC="\033[3m"
UNDERLINE="\033[4m"
INVERT="\033[7m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
CYAN="\033[36m"
MAGENTA="\033[35m"
RESET="\033[0m"


# MAIN
# ----

@cmd
def dictionary(
        word:   Annotated[str,                              Spec(help="The word to look up"                         )], 
        format: Annotated[Literal["text", "raw", "json"],   Spec(help="The output format",              prompt=False)]  = "text", 
        color:  Annotated[bool,                             Spec(help="Enable or disable color output", prompt=False)]  = True
    ):
    """Command-line interface to look up word definitions using the Free Dictionary API"""

    # Lookup the word and get the api results
    result = lookup(word)

    # Print the result in JSON format if requested
    if format == "json":
        print(json.dumps(result, indent=2))
        return
    
    # Print the raw result if requested
    if format == "raw":
        print(result)
        return
    
    # Disable color if requested or if output is not a terminal
    if not color or not sys.stdout.isatty() or os.environ.get("NO_COLOR") is not None:
        global BOLD, DIM, ITALIC, UNDERLINE, INVERT, RED, GREEN, YELLOW, CYAN, MAGENTA, RESET
        BOLD = DIM = ITALIC = UNDERLINE = INVERT = RED = GREEN = YELLOW = CYAN = MAGENTA = RESET = ""

    # Print the result
    for entry in result:
        print_definitions(entry)


if __name__ == "__main__":
    try:
        dictionary.run()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
