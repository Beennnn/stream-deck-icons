# TASKS — stream-deck-icons

## Toolkit
- 🤔 Verify `.streamDeckIconPack` = plain zip by installing a built pack via double-click → confirms the convenience zip installs, or tells us Icon Pack Man is mandatory
- ☐ Optional: `pyproject.toml` + `pip install -e .` so `sdicons` is on PATH
- ☐ Optional: SVG viewBox squareness check in `validate` (warn on non-square sources → letterboxed at 144×144)

## Instruments icon pack (packs/instruments/) — flagship pack
- 🤔 Style greenlight: full-colour flat pilot (piano/guitar/sax/drums/trumpet/violin) shown 2026-07-12 — confirm before drawing the full range
- 🤔 Decision: keep 100% hand-drawn SVG (versionable) vs inject AI-generated raster PNG for the richly detailed ones (toolkit accepts PNG) → affects fidelity vs reproducibility
- ☐ Draw the wide range (~79), by family — see backlog below
- ☐ Real pack thumbnail icon.svg (currently reuses saxophone)
- ☐ Decide publish target: Marketplace submission via Icon Pack Man + Maker Console

### Instrument backlog by family (draw in waves)
- Keys: grand piano✔ · upright piano · electric piano (Rhodes) · synthesizer · Hammond organ · accordion · harpsichord · clavinet · melodica
- Plucked strings: acoustic guitar · electric guitar✔ · bass guitar · double bass · banjo · mandolin · ukulele · harp · sitar · lute
- Bowed strings: violin✔ · viola · cello · contrabass
- Brass: trumpet✔ · trombone · french horn · tuba · cornet · sousaphone
- Woodwind: alto sax✔ · tenor sax · clarinet · flute · oboe · bassoon · piccolo · recorder · harmonica
- Drums & mallets: drum kit✔ · snare · kick · tom · cymbal · hi-hat · timpani · xylophone · vibraphone · glockenspiel
- Hand/world perc: congas · bongos · djembe · cajon · tambourine · maracas · cowbell · triangle · timbales · steelpan
- World/folk: bagpipes · didgeridoo · kalimba · balalaika · bouzouki · erhu · koto · shamisen · oud
- Electronic/studio: synth keyboard · drum machine · MPC/sampler · turntable · DJ mixer · studio mic · modular synth · theremin
- Voice/util: vocal mic · metronome · tuning fork · headphones

## Done
- ✅ Public repo live: https://github.com/Beennnn/stream-deck-icons
- ✅ Toolkit (sdicons) end-to-end validated on demo + instruments pilot
