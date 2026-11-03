def hierarchy_ratios(ranks):
    """Return the size ratio of each rank to the rank before it."""
    sizes = [rank["size_px"] for rank in ranks]
    return [sizes[i + 1] / sizes[i] for i in range(len(sizes) - 1)]
