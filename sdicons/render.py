"""Render source SVGs to 144x144 icons; copy already-conformant rasters.

SVG -> PNG via rsvg-convert (same stack as ~/dev/music/wled-assets, which
already renders on a 144x144 canvas — the exact Elgato icon size). We keep
SVG sources as-is when the caller wants vector icons (Elgato accepts SVG),
but default to PNG so every pack ships a predictable raster.
"""
import subprocess
from pathlib import Path

from . import spec
from .util import require_tool, slug, ok, dim


def render_svg(svg_path: Path, out_path: Path, size=spec.ICON_SIZE):
    """Rasterize one SVG onto a size x size transparent canvas."""
    require_tool("rsvg-convert")
    # -w/-h force the output box; rsvg fits the SVG viewBox into it.
    subprocess.run(
        ["rsvg-convert", "-w", str(size), "-h", str(size),
         "-o", str(out_path), str(svg_path)],
        check=True,
    )


def render_dir(src_dir, pack_dir, keep_svg=False, size=spec.ICON_SIZE):
    """Render/copy every source icon in src_dir into pack_dir/icons/.

    Returns the list of icon basenames written (relative to icons/).
    """
    src, pack = Path(src_dir), Path(pack_dir)
    icons_dir = pack / spec.DIR_ICONS
    icons_dir.mkdir(parents=True, exist_ok=True)

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
        elif ext in spec.ICON_FORMATS:
            # Already an accepted format — copy verbatim; validate() will
            # flag it if the raster isn't 144x144.
            dst = icons_dir / f"{base}{ext}"
            dst.write_bytes(f.read_bytes())
        else:
            print(dim(f"  skip (unsupported): {f.name}"))
            continue
        written.append(dst.name)
        print(ok(f"  rendered {dst.name}"))
    return written
