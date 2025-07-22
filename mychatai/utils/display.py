""" Helpers for streaming token display in notebooks or CLI"""

import sys
from typing import Generator

def stream_to_stdout(chunks: Generator[str, None, None]) -> None:
    """ Print each token immediately for nicer UX."""
    for token in chunks:
        sys.stdout.write(token) # push raw token to console
        sys.stdout.flush()      # force it to appear right away
    print()                     # final newline