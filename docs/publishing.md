# Publishing an icon pack to the Elgato Marketplace

`sdicons` takes you all the way to a **validated pack folder** and a
best-effort `.streamDeckIconPack` zip. The last mile — official packaging
and Marketplace submission — goes through Elgato's own tools. This is the
checklist.

## 1. Build & validate locally

```sh
bin/sdicons build path/to/src path/to/MyPack
```

This renders icons, writes `icons.json`, builds a contact sheet, runs the
validator, and (if clean) emits `dist/<name>-<version>.streamDeckIconPack`.
Iterate until `validate` reports `✓ pack is valid`.

## 2. Eyeball the palette

Open `MyPack/contact-sheet.png`. The set should read as one visual system —
consistent stroke weight, padding, and colour language across every icon.

## 3. Package officially with Icon Pack Man

The `.streamDeckIconPack` this toolkit emits is a plain zip of the pack
folder, fine for **local install/testing** (double-click to install into
Stream Deck's Icon Library). For **Marketplace submission**, use the
supported packager so the archive matches exactly what review expects:

- Icon Pack Man: <https://iconpackman.elgato.com/>
- Point it at your validated `MyPack/` folder; it emits the official
  `.streamDeckIconPack`.

> Why not fully automate this? Elgato documents Icon Pack Man as *the*
> packaging path and does not publish a stable CLI/zip contract for
> `.streamDeckIconPack`. Rather than hard-code an unverified internal
> format, the toolkit stops at a validated folder + convenience zip.

## 4. Submit via Maker Console

- Maker Console: <https://console.elgato.com/> (Marketplace maker area)
- Follow the product & branding guidelines; packs are published after review.
- Docs: <https://docs.elgato.com/stream-deck/icons/getting-started/>

## Pre-submission checklist

- [ ] Every icon is 144 × 144 px (validator enforces).
- [ ] `manifest.json` has real Name / Author / URL / Version (`x.y.z`).
- [ ] `icon.svg` thumbnail is on-brand (~56 × 56).
- [ ] Every icon has meaningful `tags` (drives Marketplace search).
- [ ] `license.txt` reflects the real licence.
- [ ] Contact sheet looks visually coherent.
- [ ] Pack installs cleanly by double-clicking the `.streamDeckIconPack`.
