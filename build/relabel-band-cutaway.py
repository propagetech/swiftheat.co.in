#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reset the callout labels on the band heater cutaway into the site's own type.

    python3 build/relabel-band-cutaway.py

image59.png is a supplier drawing the client supplied for the band heater
construction section. The drawing itself is fine; the labels are set in a heavy
condensed face at 290 px that matches nothing else on the site, and every other
drawing here labels in Inter. So the glyphs come off and go back on in Inter,
at three times the size, leaving the artwork and the red leader arrows alone.

Only the text pixels are erased, not the boxes around them: the leader arrows
run right up to the labels and a rectangular wipe clips their tips.

The one wording change is Fiber to Fibre, because the paragraph beside this
picture says "ceramic fibre insulation blanket" and a drawing that contradicts
the prose it illustrates is worse than a drawing set in the wrong font.
"""
import colorsys
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from imgprep import crop_borders  # noqa: E402

ROOT = os.path.join(HERE, "..")
SRC = os.path.join(ROOT, "docs", "uploads-2026-08-31", "web1-ppt-images", "image59.png")
DEST = os.path.join(ROOT, "imgs", "photos", "band-construction.png")
WOFF = os.path.join(ROOT, "fonts", "inter-latin-600-normal.woff2")

SCALE = 3
# Blocks found by clustering the text pixels, then read off the drawing. Each is
# (x0, y0, x1, y1) at the source's own 290 px scale, with the lines that sit in
# it. Every one of them is centred in its block on the original.
LABELS = [
    ((168, 16, 241, 30), ["Terminal Box"]),
    ((69, 22, 156, 47), ["Nickel-Chrome", "Resistance Wire"]),
    ((2, 63, 78, 89), ["Ceramic Fibre", "Insulation"]),
    ((224, 158, 282, 205), ["Stainless", "Steel", "Screw", "Terminals"]),
    ((163, 236, 282, 252), ["Stainless Steel Housing"]),
    ((4, 245, 79, 270), ["Strap Welded", "Barrel Nuts"]),
]
# The widest single line, used to size the face so the new labels take up the
# room the old ones did rather than whatever Inter's metrics happen to give.
GAUGE = ("Stainless Steel Housing", 163, 282)
LINE = 1.14


def ink(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l, s)
    return (round(r * 255), round(g * 255), round(b * 255))


INK = ink(214, 0.26, 0.18)          # --ink-800, the colour of the body text


def load_rgb():
    im = Image.open(SRC)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        flat = Image.new("RGBA", im.size, (255, 255, 255, 255))
        im = Image.alpha_composite(flat, im)
    return im.convert("RGB")


def text_mask(a):
    """The label glyphs: dark, not red, and sitting in a mostly white field."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    red = (r > 120) & (r - np.maximum(g, b) > 40)
    white = a.min(axis=2) > 232
    return (a.max(axis=2) < 140) & ~red & (ndimage.uniform_filter(
        white.astype(float), size=19) > 0.55)


def load_font(size):
    from fontTools.ttLib import TTFont
    ttf = os.path.join(HERE, "__pycache__", "inter-600.ttf")
    if not os.path.isfile(ttf):
        os.makedirs(os.path.dirname(ttf), exist_ok=True)
        f = TTFont(WOFF)
        f.flavor = None
        f.save(ttf)
    return ImageFont.truetype(ttf, size)


def measure(font, s):
    l, t, r, b = font.getbbox(s)
    return r - l, b - t


def main():
    src = load_rgb()
    a = np.asarray(src).astype(int)

    # 1. lift the glyphs off, leaving the artwork and the arrows.
    #
    # Erase everything that is not the red of an arrow inside the blocks the
    # labels occupy, rather than the glyph mask alone. The glyph mask finds the
    # solid centre of each letter but not the antialiased rim, and the rim is
    # light enough to survive a threshold and dark enough to read as a grey
    # smudge once the new text is over it. Confining the wipe to the blocks is
    # what makes it safe to be this blunt: the arrows cross their edges, so they
    # are protected by colour, and the drawing is nowhere near them.
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    red = (r > 120) & (r - np.maximum(g, b) > 40)
    red = ndimage.binary_dilation(red, np.ones((3, 3)))
    blocks = np.zeros(a.shape[:2], bool)
    pad = 3
    for (x0, y0, x1, y1), _ in LABELS:
        blocks[max(0, y0 - pad):y1 + pad + 1, max(0, x0 - pad):x1 + pad + 1] = True
    cleaned = np.asarray(src).copy()
    cleaned[blocks & ~red] = (255, 255, 255)
    big = Image.fromarray(cleaned, "RGB").resize(
        (src.width * SCALE, src.height * SCALE), Image.LANCZOS)

    # 2. size Inter so the gauge line occupies the width the old one did
    want = (GAUGE[2] - GAUGE[1] + 1) * SCALE
    size = 10
    while measure(load_font(size + 1), GAUGE[0])[0] <= want and size < 200:
        size += 1
    font = load_font(size)

    # 3. set the labels back, centred in the blocks they came out of
    draw = ImageDraw.Draw(big)
    asc, desc = font.getmetrics()
    step = round((asc + desc) * LINE)
    for (x0, y0, x1, y1), lines in LABELS:
        cx = (x0 + x1 + 1) / 2 * SCALE
        cy = (y0 + y1 + 1) / 2 * SCALE
        top = cy - (step * len(lines)) / 2
        for i, line in enumerate(lines):
            draw.text((cx, top + i * step), line, font=font, fill=INK, anchor="ma")

    # 4. take the supplier's border off.
    #
    # Two columns of pale grey rule down the right hand edge, and nothing on the
    # other three sides. At 243 it is light enough to look like paper and dark
    # enough to survive the knockout below, so it came through onto the page as
    # a hairline down the side of the drawing. The crop happens here rather than
    # on the source because the label blocks are measured in the source's own
    # coordinates and a crop before they are set would shift every one of them.
    big = crop_borders(big)

    # 5. knock the white ground back out, so it sits on any surface
    arr = np.asarray(big).astype(int)
    ground = arr.min(axis=2) > 244
    lab, n = ndimage.label(ground)
    keep = np.zeros_like(ground)
    edge = set(lab[0].tolist() + lab[-1].tolist() + lab[:, 0].tolist() + lab[:, -1].tolist())
    for i in edge:
        if i:
            keep |= lab == i
    out = np.dstack([np.asarray(big), np.where(keep, 0, 255).astype(np.uint8)])
    im = Image.fromarray(out, "RGBA")
    box = im.split()[3].getbbox()
    if box:
        im = im.crop(box)
    im.save(DEST, "PNG", optimize=True)
    print("%s  %dx%d  %d bytes  (Inter 600 at %dpx)"
          % (os.path.relpath(DEST, ROOT), im.width, im.height,
             os.path.getsize(DEST), size))


if __name__ == "__main__":
    main()
