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
import requests

def lookup(word: str):
    """
    Looks up the definition of a word using the Free Dictionary API.
    """
    api_url=f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    return response.json()

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

    # Print the result
    print(result)
