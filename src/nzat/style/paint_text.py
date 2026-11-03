from nzat.colour.composite import composite
from nzat.colour.contrast_ratio import contrast_ratio
from nzat.colour.darken import darken_for_text
from nzat.colour.parse_colour import parse_colour
from nzat.colour.red_light import red_light_reflectance
from nzat.colour.rel_luminance import rel_luminance
from nzat.style.floor_text_size import floor_text_size
from nzat.style.fmt import fmt
from nzat.style.label_floor_px import label_floor_px
from nzat.style.lookup_style_path import lookup_style_path
from nzat.style.place_rank_size import place_rank_size
from nzat.style.resolved_text_size import resolved_text_size
from nzat.style.vector_params import P

WHITE = (255, 255, 255)


def paint_text(builder, rules):
    for layer in builder.style["layers"]:
        if layer["type"] != "symbol":
            continue
        lay, paint = layer.setdefault("layout", {}), layer.setdefault("paint", {})
        lid = layer["id"]
        shield = "Highway-Labels" in lid

        fonts = lay.get("text-font")
        if (
            isinstance(fonts, list)
            and fonts
            and all(isinstance(item, str) for item in fonts)
        ):
            new_fonts = [P["deitalicise"].get(item, item) for item in fonts]
            if new_fonts != fonts:
                lay["text-font"] = new_fonts
                builder.note("R-05", lid, f"font {fonts[0]} → {new_fonts[0]}")

        if lay.get("text-field") in (None, ""):
            continue

        floor = label_floor_px(lid, lay.get("text-field"), rules)
        ts = lay.get("text-size")
        rank_size = place_rank_size(lid, rules)
        if isinstance(ts, (int, float)) and not isinstance(ts, bool):
            new_ts = resolved_text_size(ts, floor, rank_size)
            if new_ts != ts:
                lay["text-size"] = new_ts
                builder.note("R-09", lid, f"text-size {ts} → {new_ts}")
        elif isinstance(ts, dict) and "stops" in ts:
            new = [
                [z, floor_text_size(v, floor)]
                if isinstance(v, (int, float)) and not isinstance(v, bool)
                else [z, v]
                for z, v in ts["stops"]
            ]
            if new != ts["stops"]:
                ts["stops"] = new
                builder.note("R-09", lid, f"text-size stops floored at {floor}")

        spacing = lookup_style_path(rules, "labels.letter_spacing_em")
        if not shield and "text-letter-spacing" not in lay:
            lay["text-letter-spacing"] = spacing
            builder.note("R-08", lid, f"letter-spacing +{spacing} em (provisional)")

        if shield:
            continue
        tc = paint.get("text-color")
        tcol = parse_colour(tc) if isinstance(tc, str) else None
        if not tcol:
            continue

        contrast_floor = lookup_style_path(rules, "label_contrast.min_ratio")
        target_alpha = lookup_style_path(rules, "label_contrast.halo_alpha")
        hc = paint.get("text-halo-color")
        hcol = parse_colour(hc) if isinstance(hc, str) else None
        if hcol and hcol[3] < target_alpha:
            paint["text-halo-color"] = fmt(hcol[:3], target_alpha)
            builder.note("R-07", lid, f"halo alpha {hcol[3]:g} → {target_alpha:g}")
            hcol = (*hcol[:3], float(target_alpha))
        behind = composite(hcol, WHITE) if hcol else WHITE
        fg = composite(tcol, behind)
        red_floor = lookup_style_path(rules, "label_contrast.red_light_min")

        before_cr = contrast_ratio(rel_luminance(fg), rel_luminance(behind))
        before_rl = contrast_ratio(
            red_light_reflectance(fg), red_light_reflectance(behind)
        )
        new = darken_for_text(fg, behind, contrast_floor, red_floor)
        if new != fg:
            paint["text-color"] = fmt(new)
            if "text-opacity" in paint and isinstance(
                paint["text-opacity"], (int, float)
            ):
                paint["text-opacity"] = 1
            after_cr = contrast_ratio(rel_luminance(new), rel_luminance(behind))
            after_rl = contrast_ratio(
                red_light_reflectance(new), red_light_reflectance(behind)
            )
            why = []
            if before_cr < contrast_floor:
                why.append(f"contrast {before_cr:.2f}→{after_cr:.2f}")
            if before_rl < red_floor:
                why.append(f"red-light {before_rl:.2f}→{after_rl:.2f}")
            rid = "R-07" if before_cr < contrast_floor else "R-11"
            builder.note(
                rid,
                lid,
                f"text {tc} → {fmt(new)} (L* lowered, hue kept; {', '.join(why)})",
            )
