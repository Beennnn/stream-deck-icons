# Publishing an icon pack to the Elgato Marketplace

Everything below is **verified** by actually doing it (2026-07-12): building
a pack, exporting through Elgato's Icon Pack Man, inspecting the bytes, and
submitting. The gotchas are real and cost hours the first time — they're
encoded here (and in `sdicons` itself) so the next palette is a one-liner.

## TL;DR — the fast path (Icon Pack Man not required)

`sdicons package` now emits the **exact container Elgato expects**, so for a
pack built with this toolkit you can skip the Icon Pack Man web tool:

```sh
sdicons build src/ MyPack --id com.you.mypack
# → dist/com.you.mypack.streamDeckIconPack  (double-click to install; upload to Maker Console)
```

Then just submit that file (see "Maker Console" below). Use the Icon Pack Man
route only if you *want* the official web tool in the loop — in which case
read the quirks section, because it will mangle your names and tags.

## The container format (verified)

The shippable file is a **ZIP** named `<id>.streamDeckIconPack` whose single
top-level entry is a **wrapper folder** `<id>.sdIconPack/`:

```
com.you.mypack.streamDeckIconPack        ← zip, this is what you ship
└── com.you.mypack.sdIconPack/           ← REQUIRED wrapper (Stream Deck reads the id from this name)
    ├── manifest.json
    ├── icons.json
    ├── icon.svg                         ← pack thumbnail (manifest.Icon)
    ├── license.txt
    ├── icons/        (144×144 png/svg/…)
    └── previews/     (optional, up to 3 store previews, png/jpg)
```

- `<id>` is **reverse-domain**, lowercase alnum, e.g. `com.beennnn.stagekeys`.
- The wrapper folder is **not optional**. Our first packager put files at the
  zip root with no wrapper — that is NOT what Icon Pack Man produces and does
  not install cleanly. `sdicons package` now writes the wrapper (see
  `sdicons/package.py`).
- Set the id with `--id`, a `"Id"` key in `manifest.json`, or let it derive
  as `com.<author>.<name>`.

## manifest.json / icons.json

See [spec.md](spec.md). Key point for icons.json: each entry is
`{ "path": "<file>.png", "name": "<display name>", "tags": ["…"] }`, `path`
relative to `icons/`. Tags drive Stream Deck's icon-library search — worth
getting right.

## Store previews

Put up to **3** PNG/JPG images in a `previews/` folder inside the pack. Icon
Pack Man *does* pick these up on drag, and `sdicons package` includes them.
They're the marketing images on the Marketplace listing.

## Icon Pack Man quirks (if you use the web tool)

<https://iconpackman.elgato.com/> is client-side (no login). It works, but:

1. **It ignores `name` and `tags` from a dragged-in `icons.json`.** On import
   every icon's name becomes its **filename** (`trombone.png`) and tags come
   out **empty** — even though your icons.json is valid and matches the exact
   schema it exports. The "Mapping file loaded" line shows a **red ✗** (zero
   matches). Flattening the folder vs using an `icons/` subfolder makes no
   difference — it just doesn't apply them on import.
2. **It stamps `"License": "MIT"`** into the exported manifest.json by default,
   regardless of what you typed. Fix it after export (or with `sdicons repair`).
3. **It does read `manifest.json`** (Name/Version/Description/Author/URL/Icon
   populate correctly) and **does read `previews/`**.
4. Loose-file dragging is a native Finder→page drag — it **cannot be
   automated** by browser tools, and the native folder picker ("Open Icon
   Pack…") can't be driven either. This step is inherently manual.

### Fixing an Icon Pack Man export

Export from Icon Pack Man (set the IconPack ID + drag a thumbnail onto the
"Icon" box first), then repair the names/tags/license in place:

```sh
sdicons repair ~/Downloads/com.you.mypack.streamDeckIconPack \
  --tags MyPack/tags.json --license CC-BY-4.0 --url https://github.com/you/mypack
```

It re-injects `name` + `tags` by matching each icon's filename stem to your
`tags.json`, fixes the manifest License/URL, and re-zips preserving the
wrapper. Verified round-trip in `sdicons/repair.py`.

## Install & test locally

Double-click the `.streamDeckIconPack` → it installs into Stream Deck. In the
app: set a key's image → **Icon Library** → open your pack → confirm the icons
have real **names** and that a **tag search** (e.g. "organ", "sax", "808")
surfaces the right ones.

## Submit via Maker Console

- Maker Console: <https://console.elgato.com/> (requires an Elgato login).
- Upload the `.streamDeckIconPack`, fill title / description / category /
  preview images, follow the product & branding guidelines. Published after
  review.
- Docs: <https://docs.elgato.com/stream-deck/icons/getting-started/>

## Pre-submission checklist

- [ ] Every icon is 144 × 144 px (`sdicons validate` enforces).
- [ ] `manifest.json`: real Name / Author / URL / Version (`x.y.z`) / License.
- [ ] `icon.svg` thumbnail is on-brand (~56 × 56).
- [ ] Every icon has meaningful `tags` (Marketplace search).
- [ ] `previews/` has up to 3 attractive images.
- [ ] Pack installs by double-click and shows names + tags in Stream Deck.
