def rgb_key(rgb):
    return tuple(int(round(channel)) for channel in rgb[:3])
