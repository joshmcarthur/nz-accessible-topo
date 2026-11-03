import re


def parse_colour(s):
    """Parse 'rgba(r,g,b,a)', 'rgb(r,g,b)', '#rrggbb' -> (r,g,b,a) with r,g,b 0-255."""
    if not isinstance(s, str):
        return None
    s = s.strip()
    m = re.match(r"rgba?\(([^)]*)\)", s)
    if m:
        parts = [p.strip() for p in m.group(1).split(",")]
        r, g, b = (float(p) for p in parts[:3])
        a = float(parts[3]) if len(parts) > 3 else 1.0
        return (r, g, b, a)
    m = re.match(r"#([0-9a-fA-F]{6})$", s)
    if m:
        h = m.group(1)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
    return None
