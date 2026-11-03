import json

from nzat.paths import UPSTREAM
from nzat.style.builder import Builder
from nzat.style.load_rules import load_rules
from nzat.style.paint_closed_tracks import paint_closed_tracks
from nzat.style.paint_contours import paint_contours
from nzat.style.paint_hillshade import paint_hillshade
from nzat.style.paint_springs import paint_springs
from nzat.style.paint_sprite_meta import paint_sprite_meta
from nzat.style.paint_text import paint_text
from nzat.style.paint_vegetation import paint_vegetation


def build(multidirectional=False):
    variant = "v0-multidir" if multidirectional else "v0"
    rules = load_rules()
    with open(UPSTREAM, encoding="utf-8") as handle:
        catalog = json.load(handle)
    builder = Builder(catalog)
    paint_hillshade(builder, rules, multidirectional)
    paint_contours(builder, rules)
    paint_vegetation(builder, rules)
    paint_springs(builder, rules)
    paint_closed_tracks(builder, rules)
    paint_text(builder, rules)
    paint_sprite_meta(builder, variant)
    return variant, builder
