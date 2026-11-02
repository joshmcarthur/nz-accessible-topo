# Change log: accessible-v0-multidir (generated)

Every change `tools/build_style.py` made to `upstream/linz-topographic-v2.json`, grouped by recommendation.
Total changes: 200.

## R-01 (1)

- `NZAT-Contours-All-Casing` — added after `Contours-Index-Halo` — index-ink casing under intermediate fill so the line meets 3:1 under red light

## R-03 (1)

- `hillshade` — multidirectional: primary 337.5° + weaker 292.5/22.5° fill lights (F-16). Colours are provisional — tune visually (OQ-07)

## R-04 (5)

- `Contours-Index` — colour → #8A4F1C (opaque), width ↑
- `Contours-Index-Halo` — hidden — darker index line no longer needs a 10% offset shadow
- `Contours-All` — colour → #C4814B (opaque)
- `Contours-Designated` — colour → #C4814B (opaque)
- `Contours-Natural` — colour → #C4814B (opaque)

## R-05 (39)

- `Height-Point-Labels` — font Open Sans Italic → Open Sans Regular
- `Poi-Beacon` — font Open Sans Italic → Open Sans Regular
- `Poi-Beacon-Lighthouse` — font Open Sans Italic → Open Sans Regular
- `Poi-FishFarm-Label` — font Roboto Bold Italic → Roboto Bold
- `Poi-Mine-Pt` — font Open Sans Bold Italic → Open Sans Bold
- `Poi-Monument` — font Open Sans Italic → Open Sans Regular
- `Poi-Quarry-Poly-NoName` — font Open Sans Bold Italic → Open Sans Bold
- `Poi-Quarry-Poly-Name` — font Open Sans Bold Italic → Open Sans Bold
- `Poi-Railway-Symbol` — font Open Sans Bold Italic → Open Sans Bold
- `Poi-Showground-Symbol` — font Open Sans Bold Italic → Open Sans Bold
- `Poi-SportsField-Label` — font Open Sans Bold Italic → Open Sans Bold
- `Poi-Trig-Elevation` — font Open Sans Italic → Open Sans Regular
- `Poi-Trig-Symbol` — font Open Sans Bold Italic → Open Sans Bold
- `Poi-Well` — font Open Sans Italic → Open Sans Regular
- `Poi-Windmill` — font Open Sans Italic → Open Sans Regular
- `Poi-Wreck` — font Open Sans Italic → Open Sans Regular
- `Orchard-Label` — font Open Sans Italic → Open Sans Regular
- `Vineyard-Label` — font Open Sans Italic → Open Sans Regular
- `Landuse-Dam-Label` — font Roboto Black Italic → Roboto Black
- `Landuse-Landfill-Symbol` — font Roboto Italic → Open Sans Regular
- `Landuse-MarineFarm-Label` — font Roboto Bold Italic → Roboto Bold
- `Landcover-GolfCourse-Symbol` — font Open Sans Italic → Open Sans Regular
- `Landcover-Swamp-Name` — font Open Sans Light Italic → Open Sans Regular
- `Landcover-Swamp-Symbol` — font Open Sans Light Italic → Open Sans Regular
- `Housenumber` — font Roboto Bold Italic → Roboto Bold
- `Waterway-Flume-Name` — font Open Sans Italic → Open Sans Regular
- `Waterway-Rapid-Names` — font Open Sans Italic → Open Sans Regular
- `Aeroway-Aerodrome-Label` — font Open Sans Bold Italic → Open Sans Bold
- `All-Reef-Names` — font Open Sans Italic → Open Sans Regular
- `All-Lake-Names` — font Open Sans Italic → Open Sans Regular
- `All-Canal-Names` — font Open Sans Italic → Open Sans Regular
- `All-River-Names` — font Open Sans Italic → Open Sans Regular
- `All-Waterway-Canal-Names` — font Open Sans Italic → Open Sans Regular
- `All-Waterway-Drain-Names` — font Open Sans Italic → Open Sans Regular
- `All-Waterway-River-Names` — font Open Sans Italic → Open Sans Regular
- `Place-Label-Lake` — font Open Sans Bold Italic → Open Sans Bold
- `Place-Label-Sea-5` — font Open Sans Bold Italic → Open Sans Bold
- `Place-Label-Sea` — font Open Sans Bold Italic → Open Sans Bold
- `Place-Label-Lake-7` — font Open Sans Bold Italic → Open Sans Bold

## R-07 (34)

- `Contours-Label` — text rgba(193, 104, 9, 1) → rgba(140, 61, 0, 1) (L* lowered, hue kept; contrast 3.60→6.78, red-light 1.62→3.02)
- `Poi-Beacon` — text rgba(224, 168, 33, 1) → rgba(149, 104, 0, 1) (L* lowered, hue kept; contrast 2.14→4.93, red-light 1.32→3.00)
- `Poi-FishFarm-Label` — text rgba(0, 140, 204, 1) → rgba(0, 110, 171, 1) (L* lowered, hue kept; contrast 3.25→4.80)
- `Poi-Racetrack-Label` — text rgba(129, 123, 123, 1) → rgba(118, 112, 112, 1) (L* lowered, hue kept; contrast 4.16→4.88)
- `Poi-Raceway-Label` — text rgba(129, 123, 123, 1) → rgba(118, 112, 112, 1) (L* lowered, hue kept; contrast 4.16→4.88)
- `Poi-Well` — text rgba(133, 112, 112, 1) → rgba(121, 101, 101, 1) (L* lowered, hue kept; contrast 4.12→4.86)
- `Orchard-Label` — halo alpha 0.59 → 1
- `Vineyard-Label` — halo alpha 0.59 → 1
- `Landuse-Landfill-Symbol` — halo alpha 0.75 → 1
- `Landuse-MarineFarm-Label` — text rgba(0, 140, 204, 1) → rgba(0, 110, 171, 1) (L* lowered, hue kept; contrast 3.25→4.80)
- `Housenumber` — halo alpha 0.7 → 1
- `Waterway-Rapid-Names` — halo alpha 0.8 → 1
- `Waterway-Rapid-Names` — text rgba(0, 140, 204, 1) → rgba(0, 110, 171, 1) (L* lowered, hue kept; contrast 3.25→4.80)
- `Transport-Tunnel-Label` — halo alpha 0.5 → 1
- `Aeroway-Aerodrome-Label` — text rgba(129, 123, 123, 1) → rgba(118, 112, 112, 1) (L* lowered, hue kept; contrast 4.16→4.88)
- `All-Reef-Names` — text rgba(0, 140, 204, 1) → rgba(0, 110, 171, 1) (L* lowered, hue kept; contrast 3.25→4.80)
- `All-Lake-Names` — text rgba(0, 140, 204, 1) → rgba(0, 110, 171, 1) (L* lowered, hue kept; contrast 3.25→4.80)
- `All-Canal-Names` — halo alpha 0.8 → 1
- `All-Canal-Names` — text rgba(0, 140, 204, 1) → rgba(0, 110, 171, 1) (L* lowered, hue kept; contrast 3.25→4.80)
- `All-River-Names` — halo alpha 0.8 → 1
- `All-River-Names` — text rgba(0, 140, 204, 1) → rgba(0, 110, 171, 1) (L* lowered, hue kept; contrast 3.25→4.80)
- `All-Waterway-Canal-Names` — halo alpha 0.8 → 1
- `All-Waterway-Canal-Names` — text rgba(0, 140, 204, 1) → rgba(0, 110, 171, 1) (L* lowered, hue kept; contrast 3.25→4.80)
- `All-Waterway-Drain-Names` — halo alpha 0.8 → 1
- `All-Waterway-Drain-Names` — text rgba(0, 140, 204, 1) → rgba(0, 110, 171, 1) (L* lowered, hue kept; contrast 3.25→4.80)
- `All-Waterway-River-Names` — halo alpha 0.8 → 1
- `All-Waterway-River-Names` — text rgba(0, 140, 204, 1) → rgba(0, 110, 171, 1) (L* lowered, hue kept; contrast 3.25→4.80)
- `Waterway-Waterfall-Label` — text rgba(0, 140, 204, 1) → rgba(0, 110, 171, 1) (L* lowered, hue kept; contrast 3.25→4.80)
- `Waterway-Waterfall-Pt` — text rgba(0, 140, 204, 1) → rgba(0, 105, 165, 1) (L* lowered, hue kept; contrast 3.05→4.82)
- `Place-Label-Lake` — text rgba(0, 140, 204, 1) → rgba(0, 118, 180, 1) (L* lowered, hue kept; contrast 3.66→4.82)
- `Place-Label-Bay` — text rgba(0, 140, 204, 1) → rgba(0, 118, 180, 1) (L* lowered, hue kept; contrast 3.66→4.82)
- `Place-Label-Sea-5` — text rgba(0, 140, 204, 1) → rgba(0, 120, 182, 1) (L* lowered, hue kept; contrast 3.73→4.84)
- `Place-Label-Sea` — text rgba(0, 140, 204, 1) → rgba(0, 120, 182, 1) (L* lowered, hue kept; contrast 3.73→4.84)
- `Place-Label-Lake-7` — text rgba(0, 140, 204, 1) → rgba(0, 118, 180, 1) (L* lowered, hue kept; contrast 3.66→4.82)

## R-08 (79)

- `Contours-Label` — letter-spacing +0.05 em (provisional)
- `Height-Point-Labels` — letter-spacing +0.05 em (provisional)
- `All-ClosedFootRouteTrack-Labels` — letter-spacing +0.05 em (provisional)
- `All-ClosedFootTrack-Labels` — letter-spacing +0.05 em (provisional)
- `All-CycleTrack-Labels` — letter-spacing +0.05 em (provisional)
- `All-FootTrack-Labels` — letter-spacing +0.05 em (provisional)
- `Poi-Beacon` — letter-spacing +0.05 em (provisional)
- `Poi-Beacon-Lighthouse` — letter-spacing +0.05 em (provisional)
- `Poi-Bivouac-Rock` — letter-spacing +0.05 em (provisional)
- `Poi-Bivouac` — letter-spacing +0.05 em (provisional)
- `Poi-Buoy` — letter-spacing +0.05 em (provisional)
- `Poi-Cave-Pt` — letter-spacing +0.05 em (provisional)
- `Poi-Cemetery-Pt` — letter-spacing +0.05 em (provisional)
- `Poi-FishFarm-Label` — letter-spacing +0.05 em (provisional)
- `Poi-Flare` — letter-spacing +0.05 em (provisional)
- `Poi-Floodgate` — letter-spacing +0.05 em (provisional)
- `Poi-GasValve` — letter-spacing +0.05 em (provisional)
- `Poi-GeoBore-Label` — letter-spacing +0.05 em (provisional)
- `Poi-Historic-Site` — letter-spacing +0.05 em (provisional)
- `Poi-Hut-Label` — letter-spacing +0.05 em (provisional)
- `Poi-Kiln` — letter-spacing +0.05 em (provisional)
- `Poi-Ladder` — letter-spacing +0.05 em (provisional)
- `Poi-Ladder-Pt` — letter-spacing +0.05 em (provisional)
- `Poi-Mine-Pt` — letter-spacing +0.05 em (provisional)
- `Poi-Monument` — letter-spacing +0.05 em (provisional)
- `Poi-Quarry-Poly-NoName` — letter-spacing +0.05 em (provisional)
- `Poi-Quarry-Poly-Name` — letter-spacing +0.05 em (provisional)
- `Poi-Racetrack-Label` — letter-spacing +0.05 em (provisional)
- `Poi-Raceway-Label` — letter-spacing +0.05 em (provisional)
- `Poi-Railway-Symbol` — letter-spacing +0.05 em (provisional)
- `Poi-SportsField-Label` — letter-spacing +0.05 em (provisional)
- `Poi-Trig-Elevation` — letter-spacing +0.05 em (provisional)
- `Poi-Trig-Symbol` — letter-spacing +0.05 em (provisional)
- `Poi-Well` — letter-spacing +0.05 em (provisional)
- `Poi-Wreck` — letter-spacing +0.05 em (provisional)
- `Orchard-Label` — letter-spacing +0.05 em (provisional)
- `Vineyard-Label` — letter-spacing +0.05 em (provisional)
- `Landuse-Dam-Label` — letter-spacing +0.05 em (provisional)
- `Landuse-Landfill-Symbol` — letter-spacing +0.05 em (provisional)
- `Landuse-MarineFarm-Label` — letter-spacing +0.05 em (provisional)
- `Landuse-PumicePit-Label` — letter-spacing +0.05 em (provisional)
- `Landcover-Fumarole` — letter-spacing +0.05 em (provisional)
- `Landcover-GolfCourse-Symbol` — letter-spacing +0.05 em (provisional)
- `Landcover_RockOutcrop` — letter-spacing +0.05 em (provisional)
- `Landcover-Swamp-Name` — letter-spacing +0.05 em (provisional)
- `Landcover-Swamp-Symbol` — letter-spacing +0.05 em (provisional)
- `Housenumber` — letter-spacing +0.05 em (provisional)
- `Waterway-Rapid-Names` — letter-spacing +0.05 em (provisional)
- `Water-Spring-Cold` — letter-spacing +0.05 em (provisional)
- `Water-Spring-Hot` — letter-spacing +0.05 em (provisional)
- `All-Road-Labels` — letter-spacing +0.05 em (provisional)
- `Transport-Tunnel-Label` — letter-spacing +0.05 em (provisional)
- `Aeroway-Aerodrome-Label` — letter-spacing +0.05 em (provisional)
- `Aeroway-Runway-Grass-Label` — letter-spacing +0.05 em (provisional)
- `All-Reef-Names` — letter-spacing +0.05 em (provisional)
- `All-Lake-Names` — letter-spacing +0.05 em (provisional)
- `All-Canal-Names` — letter-spacing +0.05 em (provisional)
- `All-River-Names` — letter-spacing +0.05 em (provisional)
- `All-Waterway-Canal-Names` — letter-spacing +0.05 em (provisional)
- `All-Waterway-Drain-Names` — letter-spacing +0.05 em (provisional)
- `All-Waterway-River-Names` — letter-spacing +0.05 em (provisional)
- `Waterway-Waterfall-Label` — letter-spacing +0.05 em (provisional)
- `Waterway-Waterfall-Pt` — letter-spacing +0.05 em (provisional)
- `Place-Label-Lake` — letter-spacing +0.05 em (provisional)
- `Place-Label-Bay` — letter-spacing +0.05 em (provisional)
- `Place-Label-Peak-16` — letter-spacing +0.05 em (provisional)
- `Place-Label-Suburb` — letter-spacing +0.05 em (provisional)
- `Place-Label-Locality` — letter-spacing +0.05 em (provisional)
- `Place-Label-Town` — letter-spacing +0.05 em (provisional)
- `Place-Label-City-14` — letter-spacing +0.05 em (provisional)
- `Place-Label-Island-12` — letter-spacing +0.05 em (provisional)
- `Place-Label-Sea-5` — letter-spacing +0.05 em (provisional)
- `Place-Label-Sea` — letter-spacing +0.05 em (provisional)
- `Place-Label-Lake-7` — letter-spacing +0.05 em (provisional)
- `Place-Label-City-7` — letter-spacing +0.05 em (provisional)
- `Place-Label-Island-8` — letter-spacing +0.05 em (provisional)
- `Place-Label-Island-6` — letter-spacing +0.05 em (provisional)
- `Place-Label-Peak-11` — letter-spacing +0.05 em (provisional)
- `Place-Label-Island-4` — letter-spacing +0.05 em (provisional)

## R-09 (25)

- `Contours-Label` — text-size stops floored at 10
- `Height-Point-Labels` — text-size stops floored at 10
- `All-ClosedFootRouteTrack-Labels` — text-size stops floored at 10
- `All-ClosedFootTrack-Labels` — text-size stops floored at 10
- `All-CycleTrack-Labels` — text-size stops floored at 10
- `All-FootTrack-Labels` — text-size stops floored at 10
- `Poi-Beacon` — text-size 8 → 10
- `Poi-GasValve` — text-size stops floored at 10
- `Poi-Monument` — text-size 9 → 10
- `Poi-SportsField-Label` — text-size 9 → 10
- `Poi-Trig-Elevation` — text-size 9 → 10
- `Landuse-PumicePit-Label` — text-size stops floored at 10
- `Landcover-GolfCourse-Symbol` — text-size 9 → 10
- `Housenumber` — text-size stops floored at 10
- `All-Highway-Labels-three` — text-size stops floored at 10
- `All-Highway-Labels-standard` — text-size stops floored at 10
- `All-Road-Labels` — text-size stops floored at 10
- `Waterway-Waterfall-Pt` — text-size stops floored at 10
- `Place-Label-Lake` — text-size 10 → 11
- `Place-Label-Bay` — text-size 10 → 11
- `Place-Label-Suburb` — text-size 10 → 11
- `Place-Label-Town` — text-size 12 → 14
- `Place-Label-City-14` — text-size 15 → 17
- `Place-Label-Lake-7` — text-size 10 → 11
- `Place-Label-City-7` — text-size 15 → 17

## R-10 (3)

- `Vegetation-Scrub` — fill → rgba(163, 204, 144, 1)
- `Vegetation-Scatteredscrub` — fill → rgba(224, 237, 216, 1)
- `NZAT-Vegetation-Scatteredscrub-Stipple` — added after `Vegetation-Scatteredscrub` — stipple so scattered scrub survives greyscale and CVD

## R-11 (8)

- `Transport-ClosedFootTracks-Shadow` — red 40% shadow → dark casing rgba(26, 26, 26, 0.55) (lightness, not hue)
- `Transport-ClosedFootRouteTracks-Shadow` — red 40% shadow → dark casing rgba(26, 26, 26, 0.55) (lightness, not hue)
- `All-ClosedFootTrack-Labels` — red translucent halo → opaque white (restores text contrast)
- `All-ClosedFootRouteTrack-Labels` — red translucent halo → opaque white (restores text contrast)
- `NZAT-Closed-foot_route_closed-Crossbar` — added after `Transport-FootTracks` — cross-bar pattern: closed status carried by shape
- `NZAT-Closed-foot_closed-Crossbar` — added after `Transport-FootTracks` — cross-bar pattern: closed status carried by shape
- `Poi-Historic-Site` — text rgba(203, 12, 12, 1) → rgba(149, 0, 0, 1) (L* lowered, hue kept; red-light 1.62→3.00)
- `Landcover-Fumarole` — text rgba(176, 0, 0, 1) → rgba(148, 0, 0, 1) (L* lowered, hue kept; red-light 2.17→3.04)

## R-12 (1)

- `(tracks.access)` — reserved casing_colour channel is not painted (F-25)

## R-17 (3)

- `Vegetation-Native` — fill → rgba(225, 234, 195, 1)
- `Water-Spring-Hot` — text → rgba(20, 20, 20, 1); icon stays spring_hot_pnt
- `Water-Spring-Cold` — icon+text → rgba(0, 92, 143, 1); icon stays spring_cold_pnt

## infra (1)

- `(style)` — sprite → multi-sprite: LINZ default + `nzat` (patterns for R-10/R-11)
