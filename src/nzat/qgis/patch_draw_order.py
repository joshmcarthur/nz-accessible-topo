from nzat.qgis.defaults import STYLE


def _tree_layer_parent(group, name):
    """Return (parent, node) for a layer-tree-layer with this name."""
    for child in list(group):
        if child.tag == "layer-tree-layer" and child.get("name") == name:
            return group, child
        if child.tag == "layer-tree-group":
            found = _tree_layer_parent(child, name)
            if found is not None:
                return found
    return None


def patch_draw_order(root, style=None):
    """Move named layer-tree nodes so each sits immediately under its pair."""
    style = style or STYLE
    rules = style.get("draw_order") or []
    if not rules:
        return
    tree = root.find("layer-tree-group")
    if tree is None:
        raise RuntimeError("project has no layer-tree-group")
    for rule in rules:
        moving_name = rule["name"]
        below_name = rule["below"]
        moving_found = _tree_layer_parent(tree, moving_name)
        below_found = _tree_layer_parent(tree, below_name)
        if moving_found is None or below_found is None:
            continue
        parent, moving = moving_found
        below_parent, below = below_found
        parent.remove(moving)
        index = list(below_parent).index(below)
        below_parent.insert(index + 1, moving)
