#!/usr/bin/env python3
"""CLI wrapper. Implementation lives in src/nzat/. Other tools still import this module."""

import sys

import _bootstrap  # noqa: F401
from nzat.colour.ciede2000 import ciede2000
from nzat.colour.composite import composite
from nzat.colour.contrast_ratio import contrast_ratio
from nzat.colour.parse_colour import parse_colour
from nzat.colour.red_light import red_light_reflectance
from nzat.colour.rel_luminance import rel_luminance
from nzat.colour.rgb_to_lab import rgb_to_lab
from nzat.colour.simulate import MACHADO, simulate
from nzat.colour.srgb import linear_to_srgb, srgb_to_linear
from nzat.paths import STYLE_PATH
from nzat.style.audit_main import main
from nzat.style.first_colour import first_colour
from nzat.style.is_style_path import is_style_path
from nzat.style.load_maplibre import load_maplibre
from nzat.style.lookup_style_path import lookup_style_path
from nzat.style.pair_audit import pair_audit
from nzat.style.resolve_colour_spec import resolve_colour_spec
from nzat.style.resolve_pairs import resolve_pairs
from nzat.style.text_audit import text_audit

CONFIG_PATH = str(STYLE_PATH)
load_style = load_maplibre

__all__ = [
    "CONFIG_PATH",
    "MACHADO",
    "ciede2000",
    "composite",
    "contrast_ratio",
    "first_colour",
    "is_style_path",
    "linear_to_srgb",
    "load_style",
    "lookup_style_path",
    "main",
    "pair_audit",
    "parse_colour",
    "red_light_reflectance",
    "rel_luminance",
    "resolve_colour_spec",
    "resolve_pairs",
    "rgb_to_lab",
    "simulate",
    "srgb_to_linear",
    "text_audit",
]


if __name__ == "__main__":
    sys.exit(main())
