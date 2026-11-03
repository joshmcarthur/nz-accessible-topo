from nzat.style.resolve_colour_spec import resolve_colour_spec


def resolve_pairs(pairs, rules):
    """Return pairs whose colours are literal. Paths are read from rules."""
    out = []
    for pair in pairs:
        resolved = dict(pair)
        resolved["a"] = dict(pair["a"])
        resolved["b"] = dict(pair["b"])
        resolved["a"]["colour"] = resolve_colour_spec(pair["a"], rules)
        resolved["b"]["colour"] = resolve_colour_spec(pair["b"], rules)
        resolved["a"].pop("alpha", None)
        resolved["b"].pop("alpha", None)
        out.append(resolved)
    return out
