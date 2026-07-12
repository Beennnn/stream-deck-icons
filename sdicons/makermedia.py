"""Generate the marketing media the Elgato Maker Console asks for at submit.

Verified 2026-07-12 against the real submission wizard. The "Upload media"
step requires, at exact dimensions:
  - Thumbnail   : 1 image, 1920×960 (2:1), png/jpg ≤5 MB
  - Icon previews: up to 5 images, 144×144 (1:1), png/jpg ≤2 MB
  - Gallery     : ≥3 images, 1920×960 (or mp4), png/jpg ≤10 MB

Hand-making these is fiddly, so this builds all of them from a pack's icons:
a titled hero thumbnail, 5 icon-preview tiles, and gallery banners paginating
the whole palette. Output lands in `maker-media/` ready to drag into the
console. See docs/publishing.md for the full submission walkthrough.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from . import spec
from .util import ok, warn

_FONTS = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]
_BG = (18, 18, 22)
_TILE = (30, 30, 36)
_TILE_EDGE = (54, 54, 62)
_FG = (240, 240, 246)
_MUTED = (150, 152, 162)


def _font(size):
    for p in _FONTS:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _tile(icon_path, size):
    """One icon on a rounded dark tile (matches how it looks on a Stream Deck)."""
    pad = int(size * 0.07)
    ic = Image.open(icon_path).convert("RGBA").resize((size - 2 * pad, size - 2 * pad))
    t = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * 0.16),
                        fill=_TILE + (255,), outline=_TILE_EDGE + (255,), width=2)
    t.alpha_composite(ic, (pad, pad))
    return t


def _icons(pack: Path):
    d = pack / spec.DIR_ICONS
    return sorted(p for p in d.iterdir()
                  if p.suffix.lower() in spec.ICON_FORMATS and not p.name.startswith("."))


def _grid(img, icons, y0, cols=6, tile=250, gap=30, margin=90, max_rows=None):
    W = img.width
    gx = (W - 2 * margin - cols * tile) // (cols - 1)
    for i, ic in enumerate(icons):
        r, c = divmod(i, cols)
        if max_rows and r >= max_rows:
            break
        x = margin + c * (tile + gx)
        y = y0 + r * (tile + gap)
        img.paste(_tile(ic, tile).convert("RGB"), (x, y))


def maker_media(pack_dir, out_dir="maker-media", title=None, subtitle=None,
                previews=None):
    pack = Path(pack_dir)
    manifest = json.loads((pack / spec.FILE_MANIFEST).read_text())
    title = title or manifest.get("Name", "Icon Pack")
    icons = _icons(pack)
    if not icons:
        raise SystemExit("no icons to build media from")
    by_stem = {p.stem: p for p in icons}
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # --- 5 icon previews (144×144) ---
    prev = ([by_stem[s] for s in previews if s in by_stem] if previews
            else icons)[:5]
    for i, ic in enumerate(prev, 1):
        _tile(ic, spec.MAKER_PREVIEW_SIZE).convert("RGB").save(out / f"preview-{i}.png")

    # --- thumbnail (1920×960 hero) ---
    W, H = spec.MAKER_HERO_SIZE
    im = Image.new("RGB", (W, H), _BG)
    d = ImageDraw.Draw(im)
    d.text((90, 90), title, font=_font(84), fill=_FG)
    if subtitle:
        d.text((92, 205), subtitle, font=_font(40), fill=_MUTED)
    _grid(im, icons[:18], y0=320 if subtitle else 240, max_rows=2)
    im.save(out / "thumbnail-1920x960.png")

    # --- gallery banners (1920×960), paginate the whole palette, ≥3 ---
    per = 18
    pages = max(3, (len(icons) + per - 1) // per)
    for pg in range(pages):
        chunk = icons[pg * per:(pg + 1) * per] or icons[:per]
        g = Image.new("RGB", (W, H), _BG)
        dd = ImageDraw.Draw(g)
        dd.rectangle([0, 0, W, 150], fill=_TILE)
        dd.text((80, 42), f"{title} — {pg + 1}/{pages}", font=_font(60), fill=_FG)
        _grid(g, chunk, y0=250, max_rows=3)
        g.save(out / f"gallery-{pg + 1}.png")

    print(ok(f"maker media → {out}/  (thumbnail + {len(prev)} previews "
             f"+ {pages} gallery, all at Maker Console dimensions)"))
    print(warn("  drag these into the console's Upload-media step; see "
               "docs/publishing.md"))
    return out
