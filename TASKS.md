# TASKS — stream-deck-icons

- ☐ Push to GitHub `Beennnn/stream-deck-icons` (create the remote repo) → sibling of stream-deck / stream-deck-profiles
- 🤔 Verify `.streamDeckIconPack` = plain zip by installing `dist/transport-demo-1.0.0.streamDeckIconPack` via double-click → confirms the convenience zip actually installs, or tells us Icon Pack Man is mandatory
- 🤔 Add a real first palette (the live-rig icons?) as `examples/` or a private pack → the toolkit's first real customer
- ☐ Optional: `pyproject.toml` + `pip install -e .` so `sdicons` is on PATH → nicer than `bin/sdicons` for daily use
- ☐ Optional: SVG viewBox squareness check in `validate` (warn on non-square vector sources → they render letterboxed at 144×144)
