# CLAUDE.md — stream-deck-icons

Project-specific rules. The global `~/.claude/CLAUDE.md` still applies
(git workflow, storage tiers, autonomy, French chat, etc.).

## What this is

A **toolkit** (`sdicons`) that turns a folder of source icons into a
validated, Marketplace-ready Elgato Stream Deck **icon pack**. The goal is
the tooling, not any specific palette — palettes are just inputs. Sibling
of `stream-deck` (config/backups) and `stream-deck-profiles` in the `music`
group.

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

## Packaging honesty

`.streamDeckIconPack` is a zip; the toolkit builds one for local install/
testing. Elgato's **Icon Pack Man** (web) is the supported packager for
Marketplace submission — do NOT claim the direct zip is the official path.
`package.py` prints this caveat; keep it. See `docs/publishing.md`.

## Conventions

- Commits + README + docs in **English** (portfolio/tooling repo, pushed to
  GitHub `Beennnn/stream-deck-icons`). Chat with Benoît stays French.
- `validate` must exit non-zero on any spec error; `package`/`build` refuse
  to run on validation errors. Never weaken that to "ship anyway".
- Keep each `sdicons/*.py` under ~1000 LOC and single-responsibility.
