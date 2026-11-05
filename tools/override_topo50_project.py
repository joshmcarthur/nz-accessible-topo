#!/usr/bin/env python3
"""Apply the research-frame overrides to a Topo50 QGIS project.

The print layout (legend, sheet index, scale, title) is left alone.
Changes are on the map layers the research names:

- labels: upright Atkinson Hyperlegible Next Macron, size floor (R-05, R-06, R-09)
- labels: draw the buffer already on the text style, cap it at halo_max_mm, and darken ink below the contrast floor and the red-light floor (R-07, R-11)
- labels: a multiline carto_text name is split onto the forward passes of a folded baseline
- labels: stretch-to-fit curved modes keep the stock spread only on a one-line name whose baseline is longer than the name, so the larger type is not squeezed
- labels: flat one-line carto_text names sit on a short horizontal line around the stock label, so QGIS can slide or flip a name that collides
- labels: a flat carto_text name listed in carto_fit.json beside the project is drawn at its fitted point and line count
- labels: a black carto_text name listed in urban_text.json beside the project takes an urban-fill halo (R-07, G4)
- contour: index vs intermediate ink, width, stroke alpha, plus an index-ink casing on intermediates (R-04, R-01)
- track_line map: closed tracks get a heavier line and cross-bars (R-11)
- track_line map: track access is a reserved unpainted casing_colour channel (R-12)
- water_point: hot and cold springs get different glyphs (R-17)
- vegetation map: native forest and scrub use a larger lightness step (R-10, R-17)
- vegetation map: native tree markers use vegetation.native.marker (R-10)
- vegetation map: draws below contour so the darker fills do not hide relief (R-04)
- water_line map, shelterbelt, grid: stock RGB becomes the owned reference inks (R-01)
- water_line map: rivers and canals draw at water.stream_width_mm, drains at water.drain_width_mm (F-31)
- track_line map: closed-track gap marks are an × (R-11)
- road fills: PMS151 two-lane and sealed fills become reference_inks.project_road (R-01)
- nztopo50_carto_symbol: contour_number FontMarkers use the index contour ink, upright (R-17 P7, R-05)
- nztopo50_carto_symbol_label: state highway numbers read the symbol source and draw in a white shield above the road, in a darkened highway ink (R-07, R-06)
- hillshade: optional overlay at 337.5°. Turns on when dem.tif sits beside the project (R-03)

Usage: python3 tools/override_topo50_project.py IN.qgs OUT.qgs

Colour, type size, font family, and symbol rules come from
tools/style-topo50.json.
"""

import sys

import _bootstrap  # noqa: F401
from nzat.qgis.apply import apply
from nzat.qgis.capped_buffer_mm import capped_buffer_mm
from nzat.qgis.carto_fit_text_expression import carto_fit_text_expression
from nzat.qgis.carto_fit_value import carto_fit_value
from nzat.qgis.carto_flat_line_expression import carto_flat_line_expression
from nzat.qgis.carto_flat_wrap_expression import carto_flat_wrap_expression
from nzat.qgis.carto_text_width_expression import carto_text_width_expression
from nzat.qgis.closed_bar_placement import closed_bar_placement
from nzat.qgis.colour_expression import colour_expression
from nzat.qgis.curved_label_mode_expression import curved_label_mode_expression
from nzat.qgis.defaults import (
    ABOVE_BELOW_MAP_ORIENTED,
    CARTO_FIT_FILE,
    CARTO_FLAT_TEXT,
    CARTO_POINT_FILTER,
    CARTO_TEXT_LAYER,
    CURVED_ONLY_PROPERTIES,
    DEM_LAYER_ID,
    DEM_LAYER_NAME,
    FAMILY,
    MULTILINE_CENTRE,
    PMS151_RGB,
    SHEET_SCALE,
    STYLE,
    STYLE_PATH,
    WHITE,
    WRAP_HEADING_DEG,
    WRAP_TURN_DEG,
)
from nzat.qgis.dem_path import dem_path
from nzat.qgis.draw_configured_buffer import draw_configured_buffer
from nzat.qgis.expr import expr
from nzat.qgis.format_buffer_mm import format_buffer_mm
from nzat.qgis.format_qgis_colour import format_qgis_colour
from nzat.qgis.hillshade_rules import hillshade_rules
from nzat.qgis.hillshade_should_paint import hillshade_should_paint
from nzat.qgis.is_owned_road_layer import is_owned_road_layer
from nzat.qgis.label_behind import label_behind
from nzat.qgis.load_carto_fit import load_carto_fit
from nzat.qgis.override_main import main
from nzat.qgis.parse_qgis_colour import parse_qgis_colour
from nzat.qgis.patch_contour import patch_contour
from nzat.qgis.patch_contour_numbers import patch_contour_numbers
from nzat.qgis.patch_draw_order import patch_draw_order
from nzat.qgis.patch_hillshade import patch_hillshade
from nzat.qgis.patch_label_contrast import patch_label_contrast
from nzat.qgis.patch_labels import patch_labels
from nzat.qgis.patch_road_fills import patch_road_fills
from nzat.qgis.patch_springs import patch_springs
from nzat.qgis.patch_tracks import patch_tracks
from nzat.qgis.patch_vegetation import patch_vegetation
from nzat.qgis.patch_wrap_baseline import patch_wrap_baseline
from nzat.qgis.project_palette import project_palette
from nzat.qgis.properties_map import properties_map
from nzat.qgis.put_expr import put_expr
from nzat.qgis.rgb_key import rgb_key
from nzat.qgis.rgba import alpha_byte, rgb_call, rgba, rgba_call
from nzat.qgis.set_option import set_option
from nzat.qgis.size_floor import size_floor
from nzat.qgis.split_wrap_baseline import split_wrap_baseline
from nzat.qgis.upright_style_name import upright_style_name
from nzat.qgis.wrap_baseline_expression import wrap_baseline_expression
from nzat.style.load_rules import load_rules as load_style

_expr = expr
_rgb_key = rgb_key
_properties_map = properties_map
_set_option = set_option
_rgba = rgba
_rgba_call = rgba_call
_rgb_call = rgb_call
_alpha_byte = alpha_byte

__all__ = [
    "ABOVE_BELOW_MAP_ORIENTED",
    "CARTO_FIT_FILE",
    "CARTO_FLAT_TEXT",
    "CARTO_POINT_FILTER",
    "CARTO_TEXT_LAYER",
    "CURVED_ONLY_PROPERTIES",
    "DEM_LAYER_ID",
    "DEM_LAYER_NAME",
    "FAMILY",
    "MULTILINE_CENTRE",
    "PMS151_RGB",
    "SHEET_SCALE",
    "STYLE",
    "STYLE_PATH",
    "WHITE",
    "WRAP_HEADING_DEG",
    "WRAP_TURN_DEG",
    "_alpha_byte",
    "_expr",
    "_properties_map",
    "_rgb_call",
    "_rgb_key",
    "_rgba",
    "_rgba_call",
    "_set_option",
    "alpha_byte",
    "apply",
    "capped_buffer_mm",
    "carto_fit_text_expression",
    "carto_fit_value",
    "carto_flat_line_expression",
    "carto_flat_wrap_expression",
    "carto_text_width_expression",
    "closed_bar_placement",
    "colour_expression",
    "curved_label_mode_expression",
    "dem_path",
    "draw_configured_buffer",
    "expr",
    "format_buffer_mm",
    "format_qgis_colour",
    "hillshade_rules",
    "hillshade_should_paint",
    "is_owned_road_layer",
    "label_behind",
    "load_carto_fit",
    "load_style",
    "main",
    "parse_qgis_colour",
    "patch_contour",
    "patch_contour_numbers",
    "patch_draw_order",
    "patch_hillshade",
    "patch_label_contrast",
    "patch_labels",
    "patch_road_fills",
    "patch_springs",
    "patch_tracks",
    "patch_vegetation",
    "patch_wrap_baseline",
    "project_palette",
    "properties_map",
    "put_expr",
    "rgb_call",
    "rgb_key",
    "rgba",
    "rgba_call",
    "set_option",
    "size_floor",
    "split_wrap_baseline",
    "upright_style_name",
    "wrap_baseline_expression",
]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: override_topo50_project.py IN.qgs OUT.qgs", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
