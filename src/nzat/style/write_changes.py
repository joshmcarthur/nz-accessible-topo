def write_changes(variant, builder, path):
    by = {}
    for rid, lid, what in builder.log:
        by.setdefault(rid, []).append((lid, what))
    out = [
        f"# Change log: accessible-{variant} (generated)",
        "",
        "Owned paint `tools/build_style.py` wrote from `tools/style-topo50.json` onto the Shortbread catalog, grouped by recommendation.",
        f"Total changes: {len(builder.log)}.",
        "",
    ]
    for rid in sorted(by):
        out.append(f"## {rid} ({len(by[rid])})\n")
        out += [f"- `{lid}` — {what}" for lid, what in by[rid]]
        out.append("")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(out))
