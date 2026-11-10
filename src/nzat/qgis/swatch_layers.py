"""Copy applied map layers onto memory layers that hold sample features.

The legend swatches and the symbol test tiles both draw through this, so a
sample draws the way the map draws that class.
"""

import os

from nzat.qgis.legend_swatch_marker import set_svg_marker_size_mm
from nzat.qgis.legend_wkt import legend_wkt


def _table(source):
    return os.path.basename(source.split("|")[0]).removesuffix(".parquet")


def known_swatch_attrs(field_names, attrs):
    """Keep only attributes the memory layer has. Extra keys (feature_type) are ignored."""
    names = set(field_names)
    return {key: value for key, value in attrs.items() if key in names}


def extra_swatch_field_names(field_names, rows):
    """Fields to add so swatch attrs stick. Do not invent feature_type.

    structure_line and landuse categorize on feature_type, but the parquet
    column is type. A new feature_type field matches unique QGIS mint colours
    that the sheet never paints (the map hits the NULL category instead).
    """
    present = set(field_names)
    extra = []
    for _table_name, attrs, _wkt in rows:
        for name in attrs:
            if name == "feature_type" or name in present:
                continue
            extra.append(name)
            present.add(name)
    return extra


def prefer_map_layer(layer_name, table, candidate_names):
    """Use `{table} map` when Map5View-all also turns on a non-map copy."""
    map_name = f"{table} map"
    if map_name in candidate_names:
        return layer_name == map_name
    return True


def enable_inactive_swatch_rules(table):
    """Turn on stock checkstate=0 rules. Other layers keep the theme's rule state."""
    return table in {"relief_line", "bridge_line"}


def _enable_all_renderer_rules(layer):
    from qgis.core import QgsRuleBasedRenderer  # noqa: E402

    renderer = layer.renderer()
    if not isinstance(renderer, QgsRuleBasedRenderer):
        return

    def walk(rule):
        rule.setActive(True)
        for child in rule.children():
            walk(child)

    walk(renderer.rootRule())


def _string_field(name):
    from qgis.core import QgsField  # noqa: E402
    from qgis.PyQt.QtCore import QMetaType, QVariant  # noqa: E402

    try:
        return QgsField(name, QMetaType.Type.QString)
    except (AttributeError, TypeError):
        return QgsField(name, QVariant.String)


def _add_swatch_fields(copy, rows):
    extra = [
        _string_field(name)
        for name in extra_swatch_field_names(
            [field.name() for field in copy.fields()], rows
        )
    ]
    if extra:
        copy.dataProvider().addAttributes(extra)
        copy.updateFields()


def swatch_layers(
    map_layers, features, metres_per_px, labels=True, marker_size_mm=None
):
    """Copy each map layer that reads a swatch table onto a memory layer.

    The copy keeps the layer filter and the whole layer style, so
    the swatch draws the way the map draws that class. Map order is kept.
    """
    from qgis.core import (  # noqa: E402
        QgsFeature,
        QgsGeometry,
        QgsVectorLayer,
        QgsWkbTypes,
    )
    from qgis.PyQt.QtXml import QDomDocument  # noqa: E402

    matched = []
    for layer in map_layers:
        if not isinstance(layer, QgsVectorLayer):
            continue
        rows = [f for f in features if f[0] == _table(layer.source())]
        if rows:
            matched.append((layer, rows))
    names = [layer.name() for layer, _rows in matched]
    layers = []
    for layer, rows in matched:
        table = _table(layer.source())
        if not prefer_map_layer(layer.name(), table, names):
            continue
        kind = QgsWkbTypes.displayString(layer.wkbType())
        copy = QgsVectorLayer(f"{kind}?crs=EPSG:2193", layer.name(), "memory")
        copy.dataProvider().addAttributes(layer.fields().toList())
        copy.updateFields()
        if layer.subsetString() and not copy.setSubsetString(layer.subsetString()):
            raise RuntimeError(f"filter not set on {layer.name()}")
        # A renderer clone drew no state highway number. The whole style does.
        style = QDomDocument()
        error = layer.exportNamedStyle(style)
        if error:
            raise RuntimeError(f"style not read from {layer.name()}: {error}")
        ok, error = copy.importNamedStyle(style)
        if not ok:
            raise RuntimeError(f"style not set on {layer.name()}: {error}")
        if enable_inactive_swatch_rules(table):
            _enable_all_renderer_rules(copy)
        _add_swatch_fields(copy, rows)
        added = []
        for _table_name, attrs, wkt in rows:
            feature = QgsFeature(copy.fields())
            for name, value in known_swatch_attrs(
                [field.name() for field in copy.fields()], attrs
            ).items():
                feature[name] = value
            geometry = QgsGeometry.fromWkt(legend_wkt(wkt, metres_per_px))
            if QgsWkbTypes.isMultiType(layer.wkbType()):
                geometry.convertToMultiType()
            feature.setGeometry(geometry)
            added.append(feature)
        if not copy.dataProvider().addFeatures(added)[0]:
            raise RuntimeError(f"swatch features not added to {layer.name()}")
        if marker_size_mm is not None:
            set_svg_marker_size_mm(copy, marker_size_mm)
        if not labels:
            copy.setLabelsEnabled(False)
        layers.append(copy)
    return layers
