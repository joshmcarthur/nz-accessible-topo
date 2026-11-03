from nzat.style.floor_text_size import floor_text_size


def resolved_text_size(size, floor, rank_size):
    """Return the size after the floor. A place rank replaces that size."""
    sized = floor_text_size(size, floor)
    if rank_size is None:
        return sized
    return floor_text_size(rank_size, floor)
