from nzat.qgis.wrap_baseline_expression import wrap_baseline_expression


def patch_wrap_baseline(layer):
    """Put each line of a folded carto_text name on its own forward pass."""
    placement = layer.find("./labeling/settings/placement")
    if placement is None:
        return
    placement.set("geometryGenerator", wrap_baseline_expression())
    placement.set("geometryGeneratorEnabled", "1")
    placement.set("geometryGeneratorType", "LineGeometry")
