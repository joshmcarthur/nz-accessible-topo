def lookup_style_path(rules, path):
    """Return the value at a dotted path. Raise KeyError if a part is missing."""
    cur = rules
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(path)
        cur = cur[part]
    return cur
