#!/usr/bin/env python3
"""Entrypoint for the make.fun bounty news-image-20261122.

Ships the front page of Sunday 22 November 2026 (entry.png, drawn by
render.py from news.json) to /output/entry.png. Set OUT to pick a
different destination.

Standard library only, deliberately: the grader runs
`python3 -P -s /bot/main.py` inside a bare python:3.13-slim container
with no Pillow and no system fonts, so this file may import nothing
beyond the stdlib. The picture itself is drawn at build time by
render.py; this file only copies it. Copying is deterministic — the
bytes written are exactly the bytes committed in entry.png.
"""
import os
import shutil
import sys

IMAGE = "entry.png"


def ship():
    """Copy entry.png from beside this file into /output/entry.png."""
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, IMAGE)
    if not os.path.isfile(src):
        print("error: entry image not found at %s; it must be committed "
              "in the repo next to main.py" % src, file=sys.stderr)
        return 1
    dest = os.environ.get("OUT", os.path.join("/output", IMAGE))
    parent = os.path.dirname(dest)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(src, dest)
    got = os.path.getsize(dest)
    want = os.path.getsize(src)
    if got != want:
        print("error: wrote %d bytes, expected %d" % (got, want),
              file=sys.stderr)
        return 1
    print("wrote", dest, got, "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(ship())
