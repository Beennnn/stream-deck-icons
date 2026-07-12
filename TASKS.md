# TASKS — stream-deck-icons

## Toolkit
- 🤔 Verify `.streamDeckIconPack` = plain zip by installing a built pack via double-click → confirms the convenience zip actually installs, or tells us Icon Pack Man is mandatory
- ☐ Optional: `pyproject.toml` + `pip install -e .` so `sdicons` is on PATH → nicer than `bin/sdicons` for daily use
- ☐ Optional: SVG viewBox squareness check in `validate` (warn on non-square vector sources → they render letterboxed at 144×144)

## OpenLamp icon pack (first real customer — packs/openlamp/)
- 🤔 Style greenlight: amber-line pilot (Power/Brightness/Effect/Blackout) shown 2026-07-12 — confirm before drawing the full set
- ☐ Draw the remaining 10 of 14 categories: Toggle, Color, White/CCT, Palette, Scene, Snapshot, Fade, Group, Nightlight, Discover
- ☐ Design a proper pack thumbnail icon.svg (currently reuses brightness)
- 🤔 Where to publish the built pack: openlamp org repo vs Marketplace vs both — pack is EUPL-1.2 to align with LumiDeck/WLED
- ☐ Wire a `bin/publish` for the openlamp pack (mirror lumideck/bin/publish-openlamp.sh pattern) once destination decided

## Done
- ✅ Public repo live: https://github.com/Beennnn/stream-deck-icons
