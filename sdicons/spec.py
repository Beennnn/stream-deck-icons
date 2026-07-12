"""Verified Elgato Stream Deck Icon Pack specification.

Single source of truth for every constraint the validator enforces.
Facts distilled from the official Elgato Maker docs (fetched 2026-07-12):
  - https://docs.elgato.com/stream-deck/icons/getting-started/
  - https://docs.elgato.com/stream-deck/icons/api/
Keep this module data-only — no logic. If Elgato changes the spec, this
is the ONE place to update, and docs/spec.md mirrors it in prose.
"""

# Canvas: every icon must be exactly 144 x 144 px (raster). SVGs are
# rendered onto this canvas; static rasters are checked against it.
ICON_SIZE = 144

# The pack thumbnail (manifest "Icon") is recommended at 56 x 56 px.
THUMBNAIL_SIZE = 56

# Allowed icon file formats. Static vs animated split matters only for
# guidance (fps/duration), not for pack validity.
STATIC_FORMATS = (".svg", ".png", ".jpg", ".jpeg")
ANIMATED_FORMATS = (".gif", ".webp")
ICON_FORMATS = STATIC_FORMATS + ANIMATED_FORMATS

# Elgato caps icon filenames at 80 characters (basename incl. extension).
MAX_FILENAME_LEN = 80

# Animated-icon guidance (soft — warnings, not errors).
ANIM_FPS_RANGE = (10, 20)
ANIM_MAX_SECONDS = 5
ANIM_MAX_BYTES = 1_000_000  # ~1 MB preferred ceiling

# manifest.json required + optional fields (exact casing Elgato expects).
MANIFEST_REQUIRED = ("Name", "Author", "Version", "Icon")
MANIFEST_OPTIONAL = ("Description", "URL", "Licence", "License")

# Version must be three numeric components, e.g. "1.0.2".
VERSION_RE = r"^\d+\.\d+\.\d+$"

# icons.json: array of objects, each with these keys.
ICON_ENTRY_REQUIRED = ("path", "name", "tags")

# Canonical pack layout produced by the toolkit.
FILE_MANIFEST = "manifest.json"
FILE_ICONS_JSON = "icons.json"
FILE_LICENSE = "license.txt"
DIR_ICONS = "icons"
DIR_PREVIEWS = "previews"   # optional store-preview images (png/jpg, up to 3)

# Container format (verified 2026-07-12 against an Icon Pack Man export):
# the shippable file is a ZIP named `<id>.streamDeckIconPack` whose single
# top-level entry is a folder `<id>.sdIconPack/` holding the pack. Stream
# Deck derives the pack identity from that folder name (reverse-domain id).
PACK_EXT = ".streamDeckIconPack"   # extension of the shippable zip
SDICONPACK_SUFFIX = ".sdIconPack"  # suffix of the required wrapper folder
