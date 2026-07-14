# TASKS — stream-deck-icons (the toolkit)

Packs live in their own repos (e.g. streamdeck-stage-keys). This repo is the
`sdicons` tool only.

- ☐ Optional: `pyproject.toml` + `pip install -e .` so `sdicons` is on PATH (packs' bin/build.sh already look for it there)
- ☐ Optional: SVG viewBox squareness check in `validate` (warn on non-square sources → letterboxed at 144×144)

## Done
- ✅ Animated icons first-class: `render` resizes GIF/WEBP frame-by-frame (timing/loop/transparency kept), static rasters resized too, `--resample` flag, `validate` fps/duration warnings → turns WLED 72×72 effect GIFs into a 144×144 pack
- ✅ Public repo live: https://github.com/Beennnn/stream-deck-icons
- ✅ Toolkit (sdicons) end-to-end validated on examples/demo-pack
- ✅ Split content out: Stage Keys pack → https://github.com/Beennnn/streamdeck-stage-keys
- ✅ `package` emits the VERIFIED submit-ready container (`<id>.sdIconPack/` wrapper + previews)
- ✅ `repair` — fixes Icon Pack Man's dropped names/tags + License/URL
- ✅ `maker-media` — generates Maker Console upload assets (thumbnail 1920×960, 5 previews 144×144, gallery ≥3 at 1920×960)
- ✅ docs/publishing.md — full verified process: container + Icon Pack Man quirks + Maker Console submission wizard (maker.elgato.com, AI disclosure, media dims, release notes, auto-publish)
