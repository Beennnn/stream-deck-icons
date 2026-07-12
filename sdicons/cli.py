"""Command-line dispatch for the icon-pack toolkit.

Subcommands (each maps to one cohesive module):
  new       scaffold an empty spec-shaped pack
  render    SVG source dir -> 144x144 icons in pack/icons/
  meta      (re)generate icons.json from icons/ + optional tags.json sidecar
  validate  lint the pack against the Elgato spec
  contact   build a contact-sheet PNG of the whole palette
  package   zip a validated pack into a .streamDeckIconPack
  build     render + meta + validate + contact + package, end to end
"""
import argparse
import sys

from . import __version__


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="sdicons",
        description="Generate & publish Elgato Stream Deck icon packs.")
    p.add_argument("--version", action="version", version=f"sdicons {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("new", help="scaffold an empty pack")
    sp.add_argument("pack"); sp.add_argument("--name"); sp.add_argument("--author")

    sp = sub.add_parser("render", help="render source SVGs into the pack")
    sp.add_argument("src"); sp.add_argument("pack")
    sp.add_argument("--keep-svg", action="store_true",
                    help="keep vector SVGs instead of rasterizing to PNG")

    sp = sub.add_parser("meta", help="regenerate icons.json")
    sp.add_argument("pack")

    sp = sub.add_parser("validate", help="lint the pack against the spec")
    sp.add_argument("pack")

    sp = sub.add_parser("contact", help="build a contact-sheet PNG")
    sp.add_argument("pack"); sp.add_argument("--out")

    sp = sub.add_parser("package", help="build a .streamDeckIconPack")
    sp.add_argument("pack"); sp.add_argument("--out-dir", default="dist")
    sp.add_argument("--zip", action="store_true", help="use .zip extension")

    sp = sub.add_parser("build", help="render+meta+validate+contact+package")
    sp.add_argument("src"); sp.add_argument("pack")
    sp.add_argument("--keep-svg", action="store_true")
    sp.add_argument("--out-dir", default="dist")
    sp.add_argument("--name"); sp.add_argument("--author")

    args = p.parse_args(argv)

    # Lazy imports keep each subcommand's deps out of unrelated invocations.
    if args.cmd == "new":
        from .scaffold import new_pack
        new_pack(args.pack, args.name, args.author)

    elif args.cmd == "render":
        from .render import render_dir
        render_dir(args.src, args.pack, keep_svg=args.keep_svg)

    elif args.cmd == "meta":
        from .meta import build_icons_json
        build_icons_json(args.pack)

    elif args.cmd == "validate":
        from .validate import validate, print_report
        errors, warnings = validate(args.pack)
        print_report(args.pack, errors, warnings)
        sys.exit(1 if errors else 0)

    elif args.cmd == "contact":
        from .contact import contact_sheet
        contact_sheet(args.pack, args.out)

    elif args.cmd == "package":
        from .package import package
        package(args.pack, args.out_dir, as_iconpack=not args.zip)

    elif args.cmd == "build":
        from .scaffold import ensure_skeleton
        from .render import render_dir
        from .meta import build_icons_json
        from .validate import validate, print_report
        from .contact import contact_sheet
        from .package import package
        print("→ scaffold"); ensure_skeleton(args.pack, args.name, args.author)
        print("→ render");   render_dir(args.src, args.pack, keep_svg=args.keep_svg)
        print("→ meta");     build_icons_json(args.pack)
        print("→ contact");  contact_sheet(args.pack)
        print("→ validate")
        errors, warnings = validate(args.pack)
        print_report(args.pack, errors, warnings)
        if errors:
            sys.exit(1)
        print("→ package");  package(args.pack, args.out_dir)


if __name__ == "__main__":
    main()
