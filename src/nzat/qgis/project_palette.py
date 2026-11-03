def project_palette(root):
    """Return (name, colour text) pairs from the project palette."""
    for props in root.iter("properties"):
        if props.get("name") != "Palette":
            continue
        labels = colors = None
        for child in props:
            if child.get("name") == "Labels":
                labels = [value.text or "" for value in child.findall("value")]
            elif child.get("name") == "Colors":
                colors = [value.text or "" for value in child.findall("value")]
        if labels and colors and len(labels) == len(colors):
            return list(zip(labels, colors, strict=True))
    return []
