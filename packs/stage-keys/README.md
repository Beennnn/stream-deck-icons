# Stage Keys — icon pack

Full-colour **sound-select** icons for the live keyboardist. One Stream Deck
key per stage-piano voice; recognise the sound at a glance under stage
lighting — no menu-diving, no patch numbers.

![Stage Keys palette](preview.png)

## Why a keyboardist needs this

A keyboard player rarely holds a single sound through a whole song. The verse
is on a **Rhodes**, the chorus opens up on a **synth pad**, the bridge moves to
**strings**, the solo jumps to **organ**, the intro was **acoustic piano**. In
the studio there's time; **live, the change has to land exactly on the beat,
without looking away from the keys**.

This pack turns a Stream Deck into a dedicated **sound selector** beside the
keyboard:

- **One physical key = one voice.** No scrolling through programs, no aiming at
  a tiny screen mid-phrase.
- **Read the sound by shape + colour, not text.** Under low light and stress you
  recognise an object (an organ, a sax, the red Rhodes rail) far faster than an
  abstract colour code or a patch name — which is exactly why these are
  full-colour illustrations, not monochrome silhouettes.
- **See the sound before you press it.** No landing on the wrong program at the
  wrong moment.

## General MIDI / XP coverage

The pack is organised around the **General MIDI (GM 1) sound map** — the same
16 banks a Roland XP / SC / GS and any GM workstation expose. 54 dedicated
icons cover **all 112 melodic GM programs (1–112)**; variations within a family
share one icon (all four saxes → `saxophone`), and the percussive/SFX tail
reuses the nearest. Full program-by-program table: **[GM-MAP.md](GM-MAP.md)**.

## What's inside (54 icons, 16 GM families)

- **Piano** — grand, upright, Rhodes, Wurlitzer, FM/DX
- **Chromatic percussion** — celesta, glockenspiel, music box, vibraphone,
  marimba, xylophone, tubular bells
- **Organ** — drawbar, combo/rock, church/pipe, accordion, harmonica
- **Guitar** — acoustic (nylon/steel), electric (clean/distortion)
- **Bass** — electric (fingered/slap), acoustic/double bass
- **Strings** — violin/fiddle, viola, cello, ensemble, harp, timpani
- **Ensemble** — choir/voice, orchestra hit
- **Brass** — trumpet, trombone, tuba, french horn, brass section
- **Reed** — saxophone, oboe, english horn, bassoon, clarinet
- **Pipe** — piccolo, flute, recorder, pan flute
- **Synth** — lead, pad, brass, bass
- **Ethnic** — sitar, banjo, koto, kalimba
- **Percussive** — steel drums

## Build it

```sh
bin/sdicons build packs/stage-keys/src packs/stage-keys
# → dist/stage-keys-0.1.0.streamDeckIconPack
```

Licence: CC-BY-4.0 (see `license.txt`). Packaging for the Marketplace goes
through Elgato's Icon Pack Man — see [../../docs/publishing.md](../../docs/publishing.md).
