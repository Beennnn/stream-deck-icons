"""Assemble a validated pack into a distributable archive.

IMPORTANT — honesty about the format: Elgato's *supported* packaging path
is the Icon Pack Man web tool (https://iconpackman.elgato.com), which
emits the official `.streamDeckIconPack`. That extension is (as of
2026-07) a zip archive of the pack folder, so this function builds the
same zip as a convenience for local install/testing — but it is
best-effort and NOT a substitute for Maker Console submission. The CLI
prints this caveat every time. See docs/publishing.md.

Packaging refuses to run if `validate` reports any error.
"""
import zipfile
from pathlib import Path

from . import spec
from .validate import validate
from .util import ok, warn, err

# Files/dirs that belong in the shipped pack (everything else is dev cruft).
_INCLUDE = {spec.FILE_MANIFEST, spec.FILE_ICONS_JSON, spec.FILE_LICENSE}
_INCLUDE_PREFIX = (spec.DIR_ICONS + "/",)


def package(pack_dir, out_dir="dist", as_iconpack=True):
    pack = Path(pack_dir)
    errors, _ = validate(pack)
    if errors:
        raise SystemExit(err(f"refusing to package: {len(errors)} validation "
                             f"error(s). Run `sdicons validate {pack}` first."))

    import json
    manifest = json.loads((pack / spec.FILE_MANIFEST).read_text())
    from .util import slug
    stem = f"{slug(manifest['Name'])}-{manifest['Version']}"
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    ext = spec.PACK_EXT if as_iconpack else ".zip"
    archive = out / f"{stem}{ext}"

    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        # Always include the pack thumbnail referenced by manifest Icon.
        icon_rel = manifest.get("Icon")
        wanted = set(_INCLUDE)
        if icon_rel:
            wanted.add(icon_rel)
        for f in sorted(pack.rglob("*")):
            if f.is_dir() or f.name.startswith("."):
                continue
            rel = f.relative_to(pack).as_posix()
            if rel in wanted or rel.startswith(_INCLUDE_PREFIX):
                z.write(f, rel)

    print(ok(f"built {archive}"))
    print(warn("  note: Icon Pack Man (iconpackman.elgato.com) is the "
               "supported packager for Marketplace — see docs/publishing.md"))
    return archive
