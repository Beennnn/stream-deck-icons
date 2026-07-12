# TASKS — stream-deck-icons (the toolkit)

Packs now live in their own repos (e.g. streamdeck-stage-keys). This repo is
the `sdicons` tool only.

- 🤔 Verify `.streamDeckIconPack` = plain zip by installing a built pack via double-click → confirms the convenience zip installs, or tells us Icon Pack Man is mandatory
- ☐ Optional: `pyproject.toml` + `pip install -e .` so `sdicons` is on PATH (packs' bin/build.sh already look for it there)
- ☐ Optional: SVG viewBox squareness check in `validate` (warn on non-square sources → letterboxed at 144×144)

## Done
- ✅ Public repo live: https://github.com/Beennnn/stream-deck-icons
- ✅ Toolkit (sdicons) end-to-end validated on examples/demo-pack
- ✅ Split content out: Stage Keys pack → https://github.com/Beennnn/streamdeck-stage-keys
