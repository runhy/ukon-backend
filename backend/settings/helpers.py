import os
from urllib.parse import urlparse, urlunparse


def parse_boolean(s):
    """Takes a string and returns the equivalent as a boolean value."""
    s = s.strip().lower()
    if s in ("yes", "true", "on", "1"):
        return True
    elif s in ("no", "false", "off", "0", "none"):
        return False
    else:
        raise ValueError("Invalid boolean value %r" % s)


def int_or_none(value):
    if value is None:
        return value

    return int(value)