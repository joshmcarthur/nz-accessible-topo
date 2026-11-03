#!/usr/bin/env python3
"""CLI wrapper. Implementation lives in src/nzat/. Other tools still import this module."""

import sys

import _bootstrap  # noqa: F401
from nzat.colour.darken import darken_for_text
from nzat.colour.lab_to_rgb import lab_to_rgb
from nzat.paths import ROOT as ROOT_PATH
from nzat.paths import STYLE_PATH as STYLE_PATH_OBJ
from nzat.paths import UPSTREAM as UPSTREAM_PATH
from nzat.style.build import build
from nzat.style.build_main import main
from nzat.style.builder import Builder
from nzat.style.closed_track_casing import closed_track_casing as _closed_track_casing
from nzat.style.floor_text_size import floor_text_size
from nzat.style.fmt import fmt
from nzat.style.hierarchy_ratios import hierarchy_ratios
from nzat.style.index_line_width import index_line_width as _index_line_width
from nzat.style.intermediate_casing_width import (
    intermediate_casing_width as _intermediate_casing_width,
)
from nzat.style.is_place_name import is_place_name
from nzat.style.label_floor_px import label_floor_px as _label_floor_px
from nzat.style.load_rules import load_rules
from nzat.style.lookup_style_path import lookup_style_path
from nzat.style.place_rank_size import place_rank_size as _place_rank_size
from nzat.style.resolved_text_size import resolved_text_size
from nzat.style.spring_colour import spring_colour as _spring_colour
from nzat.style.vector_params import SPRITE_ID, P
from nzat.style.vegetation_fill import vegetation_fill as _vegetation_fill
from nzat.style.write_changes import write_changes

ROOT = str(ROOT_PATH)
UPSTREAM = str(UPSTREAM_PATH)
STYLE_PATH = str(STYLE_PATH_OBJ)
WHITE = (255, 255, 255)
load_style_rules = load_rules
RULES = load_rules()


def label_floor_px(layer_id, text_field, rules=None):
    return _label_floor_px(layer_id, text_field, rules or RULES)


def place_rank_size(layer_id, rules=None):
    return _place_rank_size(layer_id, rules or RULES)


def vegetation_fill(kind, rules=None):
    return _vegetation_fill(kind, rules or RULES)


def spring_colour(kind, rules=None):
    return _spring_colour(kind, rules or RULES)


def closed_track_casing(rules=None):
    return _closed_track_casing(rules or RULES)


def index_line_width(rules=None):
    return _index_line_width(rules or RULES)


def intermediate_casing_width(rules=None):
    return _intermediate_casing_width(rules or RULES)


def text_contrast_min(rules=None):
    return lookup_style_path(rules or RULES, "label_contrast.min_ratio")


def halo_alpha(rules=None):
    return lookup_style_path(rules or RULES, "label_contrast.halo_alpha")


def red_light_min(rules=None):
    return lookup_style_path(rules or RULES, "label_contrast.red_light_min")


def track_access_reserved_channel(rules=None):
    return lookup_style_path(rules or RULES, "tracks.access.reserved_channel")


def track_access_painted(rules=None):
    return lookup_style_path(rules or RULES, "tracks.access.painted")


def contour_colour(kind, rules=None):
    return lookup_style_path(rules or RULES, f"contours.{kind}.colour")


def contour_opacity(kind, rules=None):
    return lookup_style_path(rules or RULES, f"contours.{kind}.alpha")


def intermediate_casing_colour(rules=None):
    return lookup_style_path(rules or RULES, "contours.intermediate.casing_colour")


def letter_spacing_em(rules=None):
    return lookup_style_path(rules or RULES, "labels.letter_spacing_em")


def hillshade_azimuth(rules=None):
    return lookup_style_path(rules or RULES, "hillshade.azimuth_deg")


def hillshade_fill_azimuths(rules=None):
    return lookup_style_path(rules or RULES, "hillshade.fill_azimuths_deg")


def hillshade_painted(rules=None):
    return lookup_style_path(rules or RULES, "hillshade.painted")


__all__ = [
    "Builder",
    "P",
    "ROOT",
    "RULES",
    "SPRITE_ID",
    "STYLE_PATH",
    "UPSTREAM",
    "WHITE",
    "build",
    "closed_track_casing",
    "contour_colour",
    "contour_opacity",
    "darken_for_text",
    "floor_text_size",
    "fmt",
    "halo_alpha",
    "hierarchy_ratios",
    "hillshade_azimuth",
    "hillshade_fill_azimuths",
    "hillshade_painted",
    "index_line_width",
    "intermediate_casing_colour",
    "intermediate_casing_width",
    "is_place_name",
    "lab_to_rgb",
    "label_floor_px",
    "letter_spacing_em",
    "load_style_rules",
    "main",
    "place_rank_size",
    "red_light_min",
    "resolved_text_size",
    "spring_colour",
    "text_contrast_min",
    "track_access_painted",
    "track_access_reserved_channel",
    "vegetation_fill",
    "write_changes",
]


if __name__ == "__main__":
    sys.exit(main())
