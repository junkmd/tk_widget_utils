import re
import unicodedata as ucd


def is_empty(v: str) -> bool:
    """Returns `True` if the value was empty string."""
    return bool(re.match(r"^$", v))


def is_int(v: str) -> bool:
    """Returns `True` if the value consists of
    numerical characters and minus sign.
    """
    return bool(re.match(r"\-?\d+$", v))


def is_dblbyte_char(c: str) -> bool:
    """Returns `True` if the char is encoded in two bytes."""
    return ucd.east_asian_width(c) in "FWA"


def get_bytelen(v: str) -> int:
    """Returns sum of byte length of the value."""
    return sum((2 if is_dblbyte_char(c) else 1 for c in v))
