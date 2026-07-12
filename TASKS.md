# TASKS — stream-deck-icons

## Publish Stage Keys (NEXT — GM coverage now complete)
- ☐ Package via Icon Pack Man (iconpackman.elgato.com) from packs/stage-keys/ → official .streamDeckIconPack
- ☐ Test install: double-click the pack, confirm it appears in Stream Deck Icon Library
- ☐ Submit through Maker Console (console.elgato.com) — licence CC-BY-4.0, follow branding guidelines
- 🤔 Driving Icon Pack Man + Maker Console needs Benoît's Elgato login — do it together via browser, or hand off with the step-by-step

## Stage Keys — optional polish
- 🤔 Per-icon polish if wanted: grand piano a touch dark; oboe/clarinet & violin/viola/cello read similar (expected within a family); gunshot vs orchestra-hit are both bursts

## Toolkit
- 🤔 Verify `.streamDeckIconPack` = plain zip by installing a built pack via double-click
- ☐ Optional: `pyproject.toml` + `pip install -e .` so `sdicons` is on PATH
- ☐ Optional: SVG viewBox squareness check in `validate`

## Done
- ✅ Public repo live: https://github.com/Beennnn/stream-deck-icons
- ✅ Toolkit (sdicons) end-to-end validated
- ✅ Stage Keys: 76 icons — full General MIDI / XP coverage (all 128 programs) + GM-MAP.md
