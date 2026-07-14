"""Render source icons to the Elgato 144x144 canvas.

Three source kinds, one output size:
  - SVG      -> PNG via rsvg-convert (vector fits the 144x144 box).
  - static raster (PNG/JPEG) -> resized to 144x144 (Elgato rejects off-size).
  - animated (GIF/WEBP) -> every frame resized to 144x144, timing/loop/
    transparency preserved. This is what lets a folder of small LED-matrix
    effect GIFs (e.g. ~/dev/music/wled-assets, 72x72) become a spec-conformant
    animated pack without hand-editing each file.

Resample defaults are picked per source: LANCZOS for smooth static art
(gradients, illustrations), NEAREST for animated pixel-art so an integer
upscale doubles pixels crisply instead of blurring the LED grid. Override
with the `resample` argument / `--resample` CLI flag. Animated GIF output is
always NEAREST in palette (P) mode — interpolating palette indices is
meaningless, so a smooth resample on animation only applies to WEBP output.
"""
import subprocess
from pathlib import Path

from PIL import Image, ImageSequence

from . import spec
from .util import require_tool, slug, ok, dim


# Pillow resample filters, exposed by name so the CLI can pass a string.
RESAMPLE = {
    "nearest": Image.NEAREST,
    "bilinear": Image.BILINEAR,
    "bicubic": Image.BICUBIC,
    "lanczos": Image.LANCZOS,
}


def render_svg(svg_path: Path, out_path: Path, size=spec.ICON_SIZE):
    """Rasterize one SVG onto a size x size transparent canvas."""
    require_tool("rsvg-convert")
    # -w/-h force the output box; rsvg fits the SVG viewBox into it.
    subprocess.run(
        ["rsvg-convert", "-w", str(size), "-h", str(size),
         "-o", str(out_path), str(svg_path)],
        check=True,
    )


def _resize_static(src: Path, dst: Path, size, resample):
    """Resize a single-frame raster to size x size, keeping alpha."""
    with Image.open(src) as im:
        frame = im.convert("RGBA").resize((size, size), resample)
    frame.save(dst)


def _resize_gif(im: Image.Image, dst: Path, size):
    """Resize an animated GIF in palette mode — exact colours, kept alpha.

    Each frame is composited (seek resolves disposal) then NEAREST-resized in
    P mode, so palette indices — including the transparency index — are copied
    verbatim. For an integer upscale (72->144) this is a lossless pixel double.
    """
    transparency = im.info.get("transparency")
    loop = im.info.get("loop", 0)
    frames, durations = [], []
    for i in range(getattr(im, "n_frames", 1)):
        im.seek(i)
        durations.append(im.info.get("duration", 100))
        frames.append(im.copy().resize((size, size), Image.NEAREST))
    save_kw = dict(save_all=True, append_images=frames[1:],
                   duration=durations, loop=loop, disposal=2, optimize=False)
    if transparency is not None:
        save_kw["transparency"] = transparency
    frames[0].save(dst, **save_kw)


def _resize_webp(im: Image.Image, dst: Path, size, resample):
    """Resize an animated (or static) image to WEBP, RGBA throughout."""
    loop = im.info.get("loop", 0)
    frames, durations = [], []
    for frame in ImageSequence.Iterator(im):
        durations.append(frame.info.get("duration", im.info.get("duration", 100)))
        frames.append(frame.convert("RGBA").resize((size, size), resample))
    frames[0].save(dst, format="WEBP", save_all=True, append_images=frames[1:],
                   duration=durations, loop=loop)


def _resize_animated(src: Path, dst: Path, size, resample):
    im = Image.open(src)
    if dst.suffix.lower() == ".gif":
        _resize_gif(im, dst, size)
    else:
        _resize_webp(im, dst, size, resample)


def render_dir(src_dir, pack_dir, keep_svg=False, size=spec.ICON_SIZE,
               resample=None):
    """Render/resize every source icon in src_dir into pack_dir/icons/.

    `resample` (a RESAMPLE key) overrides the per-kind default. Returns the
    list of icon basenames written (relative to icons/).
    """
    src, pack = Path(src_dir), Path(pack_dir)
    icons_dir = pack / spec.DIR_ICONS
    icons_dir.mkdir(parents=True, exist_ok=True)

    override = RESAMPLE[resample] if resample else None
    written = []
    for f in sorted(src.iterdir()):
        if f.is_dir() or f.name.startswith("."):
            continue
        ext = f.suffix.lower()
        base = slug(f.stem)
        if ext == ".svg":
            if keep_svg:
                dst = icons_dir / f"{base}.svg"
                dst.write_bytes(f.read_bytes())
            else:
                dst = icons_dir / f"{base}.png"
                render_svg(f, dst, size)
        elif ext in spec.ANIMATED_FORMATS:
            dst = icons_dir / f"{base}{ext}"
            _resize_animated(f, dst, size, override or Image.NEAREST)
        elif ext in spec.STATIC_FORMATS:
            dst = icons_dir / f"{base}.png"
            _resize_static(f, dst, size, override or Image.LANCZOS)
        else:
            print(dim(f"  skip (unsupported): {f.name}"))
            continue
        written.append(dst.name)
        print(ok(f"  rendered {dst.name}"))
    return written
