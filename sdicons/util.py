"""Shared helpers: slugging, colored console output, tool discovery."""
import re
import shutil
import sys

# ANSI colours — only when stdout is a TTY so piped output stays clean.
_TTY = sys.stdout.isatty()


def _c(code, s):
    return f"\033[{code}m{s}\033[0m" if _TTY else s


def ok(s):    return _c("32", s)   # green
def warn(s):  return _c("33", s)   # yellow
def err(s):   return _c("31", s)   # red
def dim(s):   return _c("2", s)    # dim


def slug(name):
    """Filesystem-safe, grep-friendly slug for an icon basename."""
    s = re.sub(r"[^\w-]+", "-", name.strip().lower())
    return re.sub(r"-+", "-", s).strip("-")


def require_tool(name):
    """Fail loudly if an external binary (e.g. rsvg-convert) is missing."""
    path = shutil.which(name)
    if not path:
        sys.exit(err(f"required tool '{name}' not found on PATH. "
                     f"Install it (macOS: brew install librsvg for rsvg-convert)."))
    return path
