# coding=utf8
"""Part of sopel-spongemock

Copyright 2022 dgw, technobabbl.es
"""
from __future__ import print_function, division, unicode_literals, absolute_import

import random

# Python built-in unicodedata uses UCD version 13 (as of Python 3.10)
# unicodedata2 can provide a more recent version, so we use that if present
# See also: https://docs.python.org/3/library/unicodedata.html
try:
    import unicodedata2 as unicodedata
except ImportError:
    import unicodedata


def mock_case(text, *args, **kwargs):
    # args & kwargs ignored; they are there to allow calls to `mock()` from the
    # `spongemock` package to work here, even if the results aren't identical
    text = text.strip()

    out = text[0].lower()
    lower = True
    repeat = 1

    for char in text[1:]:
        lo = char.lower()
        up = char.upper()

        if unicodedata.category(char) not in {'Lu', 'Ll'} or lo == up:
            # characters whose case cannot be reliably transformed shouldn't
            # affect the case-repetition counter
            out += char
            continue

        if repeat == 2:
            repeat = 1
            lower = not lower
            out += lo if lower else up
        else:
            which = random.choice([True, False])
            if which:
                out += lo
            else:
                out += up
            if lower == which:
                repeat += 1
            else:
                repeat = 1
                lower = which

    return out
