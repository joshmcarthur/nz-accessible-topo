import re


def sheet_file_name(code, suffix=".tif"):
    """Return a file name for a sheet code. Codes such as "AS21/AS22" hold a slash or commas."""
    return re.sub(r"[^A-Za-z0-9]+", "_", code) + suffix
