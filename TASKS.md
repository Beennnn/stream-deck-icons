# TASKS — stream-deck-icons

## Publish Stage Keys (NEXT — was paused for GM integration)
- ☐ Package via Icon Pack Man (iconpackman.elgato.com) from packs/stage-keys/ → official .streamDeckIconPack
- ☐ Test install: double-click the pack, confirm it appears in Stream Deck Icon Library
- ☐ Submit through Maker Console (console.elgato.com) — licence CC-BY-4.0, follow branding guidelines

## Stage Keys — GM/XP gaps flagged ⧗ (optional dedicated icons)
Currently reuse the nearest icon; draw dedicated ones to reach 1:1 GM coverage:
- ☐ Ethnic/pipe: bagpipe, shamisen, shakuhachi, blown bottle, whistle, ocarina
- ☐ Chromatic: dulcimer
- ☐ Percussive (GM 113–120): agogo, woodblock, taiko, melodic tom, synth drum, reverse cymbal
- ☐ Synth FX (GM 97–104): dedicated crystal/atmosphere/sci-fi art (currently → synth-pad)
- 🤔 SFX bank (GM 121–128: seashore, bird, telephone, helicopter, applause, gunshot) — out of scope as instrument voices; add a small SFX sub-set only if wanted

## Stage Keys — polish
- 🤔 Per-icon polish if wanted: grand piano a touch dark; oboe/clarinet & violin/viola/cello read similar (expected within a family)

## Toolkit
- 🤔 Verify `.streamDeckIconPack` = plain zip by installing a built pack via double-click
- ☐ Optional: `pyproject.toml` + `pip install -e .` so `sdicons` is on PATH
- ☐ Optional: SVG viewBox squareness check in `validate`

## Done
- ✅ Public repo live: https://github.com/Beennnn/stream-deck-icons
- ✅ Toolkit (sdicons) end-to-end validated
- ✅ Stage Keys: 54 icons covering the full GM melodic map (1–112) + GM-MAP.md
