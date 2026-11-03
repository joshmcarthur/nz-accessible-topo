from nzat.style.closed_track_casing import closed_track_casing
from nzat.style.lookup_style_path import lookup_style_path
from nzat.style.vector_params import SPRITE_ID


def paint_closed_tracks(builder, rules):
    if lookup_style_path(rules, "tracks.access.painted"):
        raise RuntimeError("track access is reserved and must not be painted")
    builder.note(
        "R-12",
        "(tracks.access)",
        f"reserved {lookup_style_path(rules, 'tracks.access.reserved_channel')} channel is not painted (F-25)",
    )
    casing = closed_track_casing(rules)
    for lid in (
        "Transport-ClosedFootTracks-Shadow",
        "Transport-ClosedFootRouteTracks-Shadow",
    ):
        builder.layer(lid)["paint"]["line-color"] = casing
        builder.note(
            "R-11", lid, f"red 40% shadow → dark casing {casing} (lightness, not hue)"
        )
    for lid in ("All-ClosedFootTrack-Labels", "All-ClosedFootRouteTrack-Labels"):
        paint = builder.layer(lid)["paint"]
        paint["text-halo-color"] = "rgba(255, 255, 255, 1)"
        paint["text-opacity"] = 1
        if "icon-halo-color" in paint:
            paint["icon-halo-color"] = "rgba(255, 255, 255, 1)"
        builder.note(
            "R-11", lid, "red translucent halo → opaque white (restores text contrast)"
        )
    anchor = "Transport-FootTracks"
    for subclass in ("foot_route_closed", "foot_closed"):
        src = builder.layer("Transport-ClosedFootTracks-Shadow")
        bar = {
            "id": f"NZAT-Closed-{subclass}-Crossbar",
            "type": "line",
            "source": src["source"],
            "source-layer": src["source-layer"],
            "filter": ["all", ["==", "kind", "track"], ["==", "subclass", subclass]],
            "minzoom": 12,
            "paint": {
                "line-pattern": f"{SPRITE_ID}:closed_crossbar",
                "line-width": {"stops": [[12, 5], [15, 7], [19, 10]]},
            },
        }
        builder.insert_after(
            anchor, bar, "R-11", "cross-bar pattern: closed status carried by shape"
        )
