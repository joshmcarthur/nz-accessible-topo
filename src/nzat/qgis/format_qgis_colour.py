def format_qgis_colour(rgb, alpha=255):
    red, green, blue = (int(round(channel)) for channel in rgb[:3])
    return f"{red},{green},{blue},{int(alpha)}"
