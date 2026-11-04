def _pair_key(pair):
    return tuple(sorted((pair["a"], pair["b"])))


def new_collisions(accessible_pairs, stock_pairs, min_area_m2=0):
    """Collisions between two different names that the stock face does not have.

    A pair is two label texts. Largest overlap first.
    """
    stock = {_pair_key(pair) for pair in stock_pairs if pair["a"] != pair["b"]}
    found = [
        pair
        for pair in accessible_pairs
        if pair["a"] != pair["b"]
        and pair["area"] > min_area_m2
        and _pair_key(pair) not in stock
    ]
    return sorted(found, key=lambda pair: -pair["area"])
