import copy
import uuid
import xml.etree.ElementTree as ET

from nzat.qgis.carto_abbreviation_expression import carto_abbreviation_expression
from nzat.qgis.carto_fit_text_expression import carto_fit_text_expression
from nzat.qgis.carto_fit_value import carto_fit_value
from nzat.qgis.carto_flat_line_expression import carto_flat_line_expression
from nzat.qgis.carto_flat_wrap_expression import carto_flat_wrap_expression
from nzat.qgis.defaults import (
    ABOVE_BELOW_MAP_ORIENTED,
    CARTO_BIVOUAC_NAME,
    CARTO_FLAT_TEXT,
    CARTO_POINT_FILTER,
    CURVED_ONLY_PROPERTIES,
    MULTILINE_CENTRE,
    SHEET_SCALE,
    STYLE,
)
from nzat.qgis.put_expr import put_expr
from nzat.qgis.settings_props import settings_props


def carto_bivouac_distance_expression(style=None):
    style = style or STYLE
    offset_mm = style["labels"]["carto_point"]["offset_mm"]
    return f"CASE WHEN {CARTO_BIVOUAC_NAME} THEN {offset_mm:g} ELSE 0 END"


def _rule(settings, filter_expression, description):
    rule = ET.Element(
        "rule",
        {
            "description": description,
            "filter": filter_expression,
            "key": "{" + str(uuid.uuid4()) + "}",
        },
    )
    rule.append(settings)
    return rule


def patch_carto_point_labels(layer, style=None, fit=None):
    """Let QGIS slide a flat one-line carto_text name a short way, or flip it below its baseline.

    A dual name breaks after its slash and a long single name wraps, so the label is narrower and easier to place.
    A row in fit is drawn at its fitted bottom-centre point, on one line or in the default form.
    """
    style = style or STYLE
    labeling = layer.find("labeling")
    if labeling is None or labeling.get("type") != "simple":
        return
    settings = labeling.find("settings")
    if settings is None or settings.find("placement") is None:
        return
    point = copy.deepcopy(settings)
    carto = style["labels"]["carto_point"]
    placement = point.find("placement")
    placement.set("placement", "2")
    placement.set("placementFlags", str(ABOVE_BELOW_MAP_ORIENTED))
    placement.set("overrunDistance", str(carto["overrun_mm"]))
    placement.set("overrunDistanceUnit", "MM")
    placement.set("geometryGenerator", carto_flat_line_expression(style))
    placement.set("geometryGeneratorEnabled", "1")
    placement.set("geometryGeneratorType", "LineGeometry")
    placement.set("multipartBehavior", "LabelLargestPartOnly")
    text_style = point.find("text-style")
    if text_style is not None:
        text_style.set(
            "fieldName", carto_fit_text_expression(fit) if fit else CARTO_FLAT_TEXT
        )
        text_style.set("isExpression", "1")
        text_style.set("multilineHeight", str(carto["line_height"]))
        text_style.set("multilineHeightUnit", "Percentage")
    text_format = point.find("text-format")
    if text_format is not None:
        text_format.set("multilineAlign", MULTILINE_CENTRE)
        text_format.set("useMaxLineLengthForAutoWrap", "1")
    props = settings_props(point)
    if props is not None:
        for child in list(props):
            if child.get("name") in CURVED_ONLY_PROPERTIES:
                props.remove(child)
        wrap = carto_flat_wrap_expression(style)
        if fit:
            wrap = (
                f"CASE WHEN {carto_fit_value(fit, 'lines')} = 1 THEN 0 ELSE {wrap} END"
            )
        put_expr(props, "AutoWrapLength", wrap)
        put_expr(props, "Distance", carto_bivouac_distance_expression(style))
        if fit:
            offset_m = carto["offset_mm"] * SHEET_SCALE / 1000
            put_expr(props, "PositionX", carto_fit_value(fit, "x"))
            put_expr(
                props,
                "PositionY",
                f"{carto_fit_value(fit, 'y')} + CASE WHEN {CARTO_BIVOUAC_NAME} THEN {offset_m:g} ELSE 0 END",
            )
            put_expr(props, "Hali", "'Center'")
            put_expr(props, "Vali", "'Bottom'")
    baseline_text = settings.find("text-style")
    if baseline_text is not None:
        baseline_text.set("fieldName", carto_abbreviation_expression(style))
        baseline_text.set("isExpression", "1")
    labeling.remove(settings)
    labeling.set("type", "rule-based")
    rules = ET.SubElement(labeling, "rules", {"key": "{" + str(uuid.uuid4()) + "}"})
    rules.append(_rule(settings, f"NOT ({CARTO_POINT_FILTER})", "Baseline"))
    rules.append(_rule(point, CARTO_POINT_FILTER, "Flat one-line"))
