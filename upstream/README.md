# Vendored upstream

| File | Origin |
|---|---|
| `linz-topographic-v2.json` | `linz/basemaps-config` @ `581b44a87dfbd946ced1027c610b586ffa71c838`, path `config/style/topographic-v2.json` |
| `LICENSE-linz-basemaps-config` | MIT licence, Crown copyright LINZ — must accompany derived styles |

Vendored (not fetched at build time) so builds are reproducible offline and
upstream changes arrive as reviewable diffs. To update:

```sh
git clone --depth 1 https://github.com/linz/basemaps-config /tmp/bc
cp /tmp/bc/config/style/topographic-v2.json upstream/linz-topographic-v2.json
# record the new SHA in this file, rebuild, re-run the audit, review diffs
```
