import json


def carto_fit_value(fit, key):
    """Expression for one fitted value of this row; NULL for a row with no fit."""
    literal = json.dumps(fit, separators=(",", ":")).replace("'", "''")
    return f"map_get(map_get(json_to_map('{literal}'), \"id\"), '{key}')"
