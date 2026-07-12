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
  `render` (SVG→144px via `rsvg-convert`), `scaffold`, `meta` (icons.json),
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

## Conventions

- Commits + README + docs in **English** (portfolio/tooling repo, pushed to
  GitHub `Beennnn/stream-deck-icons`). Chat with Benoît stays French.
- `validate` must exit non-zero on any spec error; `package`/`build` refuse
  to run on validation errors. Never weaken that to "ship anyway".
- Keep each `sdicons/*.py` under ~1000 LOC and single-responsibility.
