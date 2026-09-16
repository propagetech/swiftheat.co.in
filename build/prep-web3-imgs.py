#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepare photographs the client dropped onto anotherpptanddocuments/web 3.pptx.

    python3 build/prep-web3-imgs.py

Merges new entries into imgs/client-imgs.json. The thermocouple type/range chart
is data, not a photograph, and is published as an HTML table instead.
"""
import json
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from imgprep import _hex, crop_borders, enhance, ground  # noqa: E402

ROOT = os.path.join(HERE, "..")
SRC = os.path.join(ROOT, "unused", "imgs", "client-suggested-web3")
IMGS = os.path.join(ROOT, "imgs")
META = os.path.join(IMGS, "client-imgs.json")

_meta = {}
if os.path.exists(META):
    with open(META, encoding="utf-8") as fh:
        _meta.update(json.load(fh))


def load(name):
    im = Image.open(os.path.join(SRC, name))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        flat = Image.new("RGBA", im.size, (255, 255, 255, 255))
        im = Image.alpha_composite(flat, im)
    return im.convert("RGB")


def save(im, path, quality=88):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if path.lower().endswith(".png"):
        im.save(path, "PNG", optimize=True)
    else:
        im.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    g = _hex(ground(np.asarray(im).astype(np.int16)))
    key = os.path.relpath(path, IMGS).replace(os.sep, "/")
    _meta[key] = {"w": im.width, "h": im.height, "ground": g}
    return path, im.size, g


def prep(name, out, **kw):
    im = enhance(crop_borders(load(name)), **kw)
    return save(im, os.path.join(IMGS, out))


def log(src, out, size, path, g):
    print("  %-44s %-36s %4dx%-4d %7d B  ground %s"
          % (src, out, size[0], size[1], os.path.getsize(path), g))


def main():
    print("web 3.pptx photographs")
    jobs = [
        ("slide1-cartridge-heaters-selection.png", "cartridge-heaters-selection.png"),
        ("slide2-coil-heaters-hero.jpg", "coil-heaters-hero.png"),
        ("slide3-coil-heaters-construction.jpg", "coil-heaters-construction.png"),
    ]
    for src, out in jobs:
        path, size, g = prep(src, out)
        log(src, out, size, path, g)

    with open(META, "w", encoding="utf-8") as fh:
        json.dump(_meta, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote", os.path.relpath(META, ROOT))


if __name__ == "__main__":
    main()
