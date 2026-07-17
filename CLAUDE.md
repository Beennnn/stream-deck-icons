# CLAUDE.md — stream-deck-icons

Project-specific rules. The global `~/.claude/CLAUDE.md` still applies
(git workflow, storage tiers, autonomy, French chat, etc.).

## What this is

A **toolkit** (`sdicons`) that turns a folder of source icons into a
validated, Marketplace-ready Elgato Stream Deck **icon pack**. The goal is
the tooling, not any specific palette — palettes are just inputs. Sibling
of `stream-deck` (config/backups) and `stream-deck-profiles` in the `music`
group.

**This repo is the TOOL only.** Actual icon packs live in their own repos and
are *built with* this toolkit — e.g.
[streamdeck-stage-keys](https://github.com/Beennnn/streamdeck-stage-keys)
(`~/dev/music/streamdeck-stage-keys`, the 83-icon GM/XP keyboardist pack).
Decided 2026-07-12: keep the generic MIT tool separate from CC-BY content
packs (own versioning, own Marketplace home, tool stays lean). New packs =
new sibling repos, not folders here. This repo keeps only its tiny
`examples/demo-pack` to prove the pipeline.

## Stack & layout

- **Python 3.9+** package `sdicons/`, one concern per file:
  `render` (SVG→144px via `rsvg-convert`; static rasters resized via Pillow;
  animated GIF/WEBP resized frame-by-frame — timing/loop/transparency kept),
  `scaffold`, `meta` (icons.json),
  `validate` (spec linter), `contact` (contact sheet), `package` (zip),
  `cli` (argparse dispatch), `spec.py` (verified Elgato constants — the ONE
  place to update if the spec changes), `util`.
- Run from a clone: `bin/sdicons <cmd>` (no install). Deps: Pillow + `rsvg-convert`.
- `examples/demo-src/` (committed SVGs) + `examples/demo-pack/` (committed
  authored metadata: `manifest.json`, `tags.json`, `icon.svg`, `license.txt`).
  Generated outputs (`icons/`, `icons.json`, `contact-sheet.png`, `dist/`)
  are **gitignored** — reproduce with `bin/sdicons build examples/demo-src examples/demo-pack`.

## The Elgato spec is verified, not guessed

`sdicons/spec.py` + `docs/spec.md` were distilled from the official Maker
docs (fetched 2026-07-12): icons are **144×144**, formats SVG/PNG/JPEG (+GIF/
WEBP animated), filenames ≤80 chars, `manifest.json` needs Name/Author/
Version(`x.y.z`)/Icon, `icons.json` is an array of `{path,name,tags}`. If you
change any constraint, update `spec.py` and mirror it in `docs/spec.md`.

## Packaging & publishing — VERIFIED knowledge (2026-07-12)

Learned by building, exporting through Icon Pack Man, inspecting the bytes,
and submitting. All encoded in `docs/publishing.md` + `sdicons` itself:

- **Container**: the shippable `.streamDeckIconPack` is a ZIP whose single
  top-level entry is a wrapper folder `<id>.sdIconPack/` holding
  manifest.json, icons.json, icon.svg, license.txt, icons/, previews/.
  `<id>` is reverse-domain (`com.beennnn.stagekeys`) — Stream Deck reads the
  pack identity from that folder name. Our OLD packager put files at the zip
  root (no wrapper) — wrong. `package.py` now writes the wrapper; it's
  **submit-ready**, Icon Pack Man is optional.
- **Icon Pack Man quirks**: the web tool IGNORES `name`/`tags` from a
  dragged-in icons.json (names become "trombone.png", tags empty, "Mapping
  file loaded" shows red ✗); it stamps `License: MIT`; it DOES read
  manifest.json + previews/. Its loose-file drag can't be automated (native
  Finder→page), so that step is manual. `sdicons repair <export> --tags
  tags.json` re-injects names/tags + fixes License/URL, preserving the
  container.
- **Maker Console** = **maker.elgato.com** (NOT console.elgato.com — that
  errors). Needs the user's Elgato login (+ org + Maker Agreement first time —
  legal, their action). Submission wizard: Details (AI-content disclosure
  REQUIRED — check it for AI art; Type/Theme/Color multi-selects are flaky;
  Style=Illustrated; not-animated; Free/Paid locked after submit) → Upload
  media (thumbnail 1920×960, 5 previews 144×144, gallery ≥3 at 1920×960 —
  native file drops the human must do) → Submit for review (release notes
  REQUIRED, auto-publish toggle; Submit is the human's final click). Full
  walkthrough in `docs/publishing.md`.
- **`sdicons maker-media <pack>`** generates all those upload assets at the
  exact dimensions (thumbnail/previews/gallery). Constants in `spec.py`
  (MAKER_URL, MAKER_HERO_SIZE, MAKER_PREVIEW_SIZE).
- Do NOT claim things about the format you haven't verified against a real
  export/submission. If Elgato changes it, re-verify and update `spec.py` +
  `publishing.md`.

## Animated icons (added 2026-07-14)

`render` handles animated GIF/WEBP as first-class, not just static rasters:
- **GIF** → each frame composited to RGBA via `seek` (disposal resolved),
  NEAREST-resized (×2 upscale of WLED 72→144 is a lossless pixel double), then
  re-quantized to a palette with index 255 reserved for transparency.
  - ⚠️ **Transparency gotcha (fixed 2026-07-14):** the earlier version copied
    P-mode frames verbatim (`im.copy()`), which kept transparency on frame 0
    but DROPPED it on frames 1..n — the palette key colour (green, index 255)
    then flashed **opaque** mid-loop on the deck. Symptom surfaced in the
    animated maker-media montage (green tiles). Fix = composite→RGBA→requantize
    with a reserved transparent index (`_rgba_to_p`), applied to every frame.
    Verify with: seek each frame, `convert("RGBA").getpixel((0,0))[3]` must be
    0 on transparent-corner icons. Never revert to the verbatim-copy path.
- **WEBP** → RGBA throughout, honours the `--resample` filter.
- Static PNG/JPEG are now **resized** to 144×144 (were copied verbatim, which
  left off-size rasters for `validate` to reject).
- `validate` adds soft fps/duration warnings (`ANIM_FPS_RANGE`,
  `ANIM_MAX_SECONDS` in spec.py) on top of the existing ~1 MB byte budget.
- `--resample {nearest,bilinear,bicubic,lanczos}` overrides the per-kind
  default (lanczos static / nearest animated). GIF stays NEAREST regardless —
  interpolating palette indices is meaningless.

Built to turn `~/dev/music/wled-assets` effect GIFs into a Marketplace pack —
see the WLED pack repo (sibling, built with this toolkit).

## Maker Console gallery — content must FIT the frame, not just the file (2026-07-14)

Both WLED packs were **rejected** the same day they were submitted with:
*"ensure there was no cropping of information, please ensure all media for
Marketplace is 1920×960."* The files WERE 1920×960 — the bug was that the
gallery generator laid out **content that overflowed** the canvas: 3 rows of
6 tiles at `tile=250, gap=30, y0=250` put the 3rd row at y 810..1060, so its
bottom ~100 px was sliced off by the 960 px edge. The reviewer reads a sliced
bottom row as "cropped information", even though the file dimensions are exact.

- **Rule**: a hero/gallery banner is only valid if every drawn row fits fully
  inside 960 px. The fit is `y0 + rows·tile + (rows-1)·gap ≤ 960`. The thumbnail
  was fine because it used `max_rows=2`; only the 3-row gallery overflowed.
- **Fix** (`makermedia.py`): gallery tiles 250→220, `y0` 250→190 → 3 full rows
  fit (`190 + 3·220 + 2·24 = 898 ≤ 960`). Keeps 18 icons/page. Verify any layout
  change by eyeballing `gallery-2.png` — the bottom row must have a margin below
  it, never touch the edge.
- **Verify programmatically**: file dims via `sips`/Pillow catch the wrong
  *canvas* size, NOT overflowing content. There's no substitute for looking at
  a regenerated banner. Add a `validate`-style content-fit assertion here if
  this recurs.

## Animated icons ship as GIF, not WebP (verified 2026-07-16 — a rejection)

Stage Keys v1.2 was **rejected**: the reviewer couldn't get the WebP animated
icons to play on keys. PIL-optimised (partial-frame) animated WebP is valid per
spec but Stream Deck's key decoder won't play it. **Ship animated icons as GIF**
(`<slug>-playing.gif`) — the format every working animated pack of ours uses
(WLED Effects, 216 GIFs, live). `save_animated`'s GIF branch now applies
`render._rgba_to_p` per frame (else alpha survives only on frame 0 — key colour
flashes opaque mid-loop). Full detail in `docs/publishing.md`.

## Media + version-update gotchas (verified 2026-07-16, Stage Keys v1.2)

Learned shipping the Stage Keys v1.2 update. Full detail in `docs/publishing.md`
("Updating a published product" + "Media gotchas"). The three that cost time:

1. **Icon previews must be transparent RGBA, not opaque RGB.** The Maker Console
   "Icon previews" slot silently rejects an opaque upload — it blanks out
   ("previews disappear"). `makermedia.py` now emits previews as resized RGBA
   (was baking a dark tile + RGB-converting). Hero/gallery banners stay RGB.
2. **Static+animated packs duplicated every montage tile** — `<x>.png` AND
   `<x>-playing.webp` both listed (identical frozen). `_icons()` now dedupes to
   one per base icon, preferring the static.
3. **Updating a published product** = Product → Versions → Create version
   (minimal modal: pack file + release notes + auto-publish + Submit). Media is
   product-level (Media tab), editable anytime — NOT in the version modal.
   "Create version" is blocked only while a prior version is Pending review.
   The release-notes rich editor silently drops em-dashes — use ASCII hyphens.

## Animated icons MUST ship a companion poster PNG (verified 2026-07-17)

**The #1 way an animated pack gets rejected.** Maker Console rejected Stage Keys
1.2 on 2026-07-17: *"the preview images of the GIFs aren't loading, please ensure
this icon pack is packaged correctly via iconpackman."* Root cause, found by
reverse-engineering iconpackman.elgato.com's own export JS:

- The Stream Deck **Icon Library** renders each grid cell from a STATIC image and
  only plays the animation on hover. A GIF with no static poster shows a broken
  tile.
- iconpackman guarantees the poster: for every `icons/<base>.gif`, it looks for a
  sibling `icons/<base>.png` and, if absent, GENERATES one from the GIF's first
  frame (`canvas.drawImage(gif,0,0) → toDataURL("image/png")`). The poster is
  **NOT listed in icons.json** — the Library resolves it by same-base-name.
- Our earlier `sdicons package` copied the GIFs but wrote no posters → the
  rejection. Fixed: `posters.py` generates them, `package` calls `ensure_posters`
  before zipping, and `verify` FAILS a pack whose animations lack posters.

Never hand-remove the `<base>.png` posters from `icons/`, and never add them to
icons.json (that would double every animated icon in the grid).

## `verify` — the pre-publication gate (run before EVERY submission)

`validate` = "is this structurally valid?". `verify` = "will Maker Console accept
this?" — a strict superset that also catches the real rejections:

```
bin/sdicons verify MyPack                 # exit 1 on any ERROR
bin/sdicons verify MyPack --fix           # generate missing posters, then verify
bin/sdicons verify MyPack --strict        # warnings become blocking
bin/sdicons verify dist/foo.streamDeckIconPack   # verify the SHIPPED bytes
bin/sdicons posters MyPack                # just (re)generate companion posters
```

Checks (each finding is `[code]`-tagged, ERROR/WARN/INFO): `missing-poster`,
`poster-size`/`poster-format`, `bad-tag` (iconpackman rejects `", "` in a tag),
`dup-path`/`dup-name`, `filename-case`/`-space`, manifest store-quality
(`no-description`/`no-url`/`no-licence`), `too-many-previews`, `empty-pack`, plus
all structural errors folded in. `verify_container` unzips a `.streamDeckIconPack`
and checks the real bytes — run it on `dist/` right before uploading to catch a
stale container built before a fix. Tests: `tests/test_verify*.py`,
`tests/test_posters.py` (49 tests, ~96% coverage — `python3 -m pytest tests/`).

## Conventions

- Commits + README + docs in **English** (portfolio/tooling repo, pushed to
  GitHub `Beennnn/stream-deck-icons`). Chat with Benoît stays French.
- `validate` must exit non-zero on any spec error; `package`/`build` refuse
  to run on validation errors. Never weaken that to "ship anyway".
- Keep each `sdicons/*.py` under ~1000 LOC and single-responsibility.
