# stream-deck-icons

**A toolkit to generate and publish Elgato Stream Deck icon packs.** Point it
at a folder of SVGs and it renders them to spec, writes the pack metadata,
lints everything against Elgato's requirements, builds a contact sheet, and
packages a `.streamDeckIconPack` ready for [Icon Pack Man](https://iconpackman.elgato.com/)
and the Marketplace.

The point isn't any one palette — it's the **tools** that turn any palette
into a publishable pack, every time, without hitting a review rejection.

## Pipeline

```
src/*.svg ──render──▶ MyPack/icons/*.png (144×144)
                      MyPack/icons.json   (names + tags)
                      MyPack/manifest.json
                      ├─ validate ▶ Elgato spec lint (blocks packaging on error)
                      ├─ contact  ▶ contact-sheet.png (eyeball the whole set)
                      └─ package  ▶ dist/<name>-<version>.streamDeckIconPack
```

## Requirements

- Python 3.9+ with [Pillow](https://python-pillow.org/) (`pip install pillow`)
- [`rsvg-convert`](https://gitlab.gnome.org/GNOME/librsvg) for SVG→PNG
  (macOS: `brew install librsvg`)

No install step for the toolkit itself — run it straight from a clone via
`bin/sdicons`.

## Quick start

```sh
# one-shot: render + metadata + validate + contact sheet + package
bin/sdicons build examples/demo-src examples/demo-pack

# or step by step
bin/sdicons new   MyPack --name "My Pack" --author "You"
bin/sdicons render src/ MyPack        # SVG → 144×144 PNG in MyPack/icons/
bin/sdicons meta   MyPack             # (re)generate icons.json
bin/sdicons validate MyPack           # lint against the Elgato spec
bin/sdicons contact  MyPack           # build contact-sheet.png
bin/sdicons package  MyPack           # → dist/*.streamDeckIconPack
```

Try it on the bundled demo:

```sh
bin/sdicons build examples/demo-src examples/demo-pack
# → dist/transport-demo-1.0.0.streamDeckIconPack  (valid, ready to install)
```

## Authoring metadata

Names and tags are derived from filenames by default (`power-on` → *Power On*).
Override per icon with a `tags.json` sidecar in the pack root — hand-tuned
values survive every `meta`/`build` re-run:

```json
{
    "power": { "name": "Power", "tags": ["control", "power", "transport"] }
}
```

## Commands

| Command | Does |
|---|---|
| `new`      | scaffold an empty, spec-shaped pack |
| `render`   | SVG source dir → 144×144 icons in `pack/icons/` |
| `meta`     | (re)generate `icons.json` from `icons/` + `tags.json` |
| `validate` | lint the pack against the Elgato spec (exit 1 on error) |
| `contact`  | build a contact-sheet PNG of the whole palette |
| `package`  | zip a validated pack into a `.streamDeckIconPack` |
| `build`    | all of the above, end to end |

## Publishing

The toolkit stops at a **validated folder + convenience zip**. For Marketplace
submission use Elgato's supported path — see [docs/publishing.md](docs/publishing.md).
The enforced spec is documented in [docs/spec.md](docs/spec.md).

## Related repos

- [stream-deck](https://github.com/Beennnn/stream-deck) — live-rig config, backups, VPN/BOME scripts
- [stream-deck-profiles](https://github.com/Beennnn/stream-deck-profiles) — the ProfilesV3 profiles

## License

MIT — see [LICENSE](LICENSE).
