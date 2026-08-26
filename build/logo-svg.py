#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Trace the Swiftheat logo into a two colour SVG.

    python3 build/logo-svg.py

Swiftheat have never had a vector logo. What exists is raster: a 625 x 208 PNG
in the old site's media library, a 535 x 180 JPEG the client sent on
26 Aug 2026, and the impression printed on the brochure. All three are the same
artwork, so the PNG wins on being the largest and the only one that is not JPEG
compressed.

This is a trace of the client's own artwork, not a redesign. The letterforms,
the flame, the crossing rules and the two colours are theirs. If the original
vector ever turns up, throw this away and use that instead.

The two colours are traced separately and composed into one coordinate system,
which is why the crop is computed once over both masks rather than per mask.
Cropping each one independently would shift them relative to each other.
"""
import os
import re
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "archive-old-site", "assets", "swiftheat-logo.png")
OUT = os.path.join(HERE, "..", "imgs", "swiftheat-logo.svg")

# Sampled off the source: it is raw primary blue and raw primary red, which is
# what a logo drawn in an office application looks like. Published as found.
BLUE = "#0000ff"
RED = "#ff0000"

SCALE = 4          # upsample before thresholding, see masks()
INK = 150          # luminance below this is artwork
BIAS = 4           # how far r and b must differ before a pixel picks a side
SPECK = 24         # potrace turdsize, in upsampled pixels


def masks(path):
    """Split the artwork into a blue layer and a red layer.

    Every non white pixel goes to whichever of red or blue is stronger. The
    flame and the rule crossover are a blend of the two, so the boundary falls
    where the blend crosses half way, which is where the eye puts it too.

    The source is only 625 px wide and heavily antialiased, so it is upsampled
    first. Thresholding the original directly picks up the pale edge pixels and
    fattens every stroke until the counters of the e and the a close up and the
    flame turns into a blob. Upsampling puts the threshold on the true edge.
    """
    im = Image.open(path).convert("RGB")
    im = im.resize((im.width * SCALE, im.height * SCALE), Image.LANCZOS)
    w, h = im.size
    px = im.load()
    blue = Image.new("L", (w, h), 0)
    red = Image.new("L", (w, h), 0)
    bp, rp = blue.load(), red.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if (r * 299 + g * 587 + b * 114) // 1000 > INK:
                continue
            if b - r > BIAS:
                bp[x, y] = 255
            elif r - b > BIAS:
                rp[x, y] = 255
            # A pixel that is neither is the purple of the gradient where the
            # two rules cross under the flame. It belongs to neither layer.
            # Handing it to one of them draws a crescent that is not in the
            # artwork, so it is left out and the two traces meet at it.
    return blue, red


def union_box(*layers):
    boxes = [m.getbbox() for m in layers if m.getbbox()]
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


def trace(mask, tmp, tag):
    """One mask to potrace geometry, in the mask's own pixel coordinates."""
    # potrace traces black on white, so invert.
    bw = mask.point(lambda v: 0 if v else 255).convert("1")
    pbm = os.path.join(tmp, "%s.pbm" % tag)
    svg = os.path.join(tmp, "%s.svg" % tag)
    bw.save(pbm)
    subprocess.run(["potrace", "-s", "-o", svg, "-a", "1.0", "-O", "0.2", "-t", str(SPECK),
                    "--flat", pbm], check=True)
    doc = open(svg, encoding="utf-8").read()
    g = re.search(r"(<g[^>]*>)(.*?)</g>", doc, re.S)
    if not g:
        raise RuntimeError("unexpected potrace output for %s" % tag)
    body = re.sub(r'\s(?:fill|stroke)="[^"]*"', "", g.group(2).strip())
    tr = re.search(r'transform="([^"]+)"', g.group(1))
    return tr.group(1) if tr else "", body


def main():
    if not os.path.isfile(SRC):
        sys.exit("source logo not found: %s" % SRC)
    tmp = os.path.join(HERE, ".logo-tmp")
    os.makedirs(tmp, exist_ok=True)

    blue, red = masks(SRC)
    box = union_box(blue, red)
    blue, red = blue.crop(box), red.crop(box)
    w, h = blue.size

    b_tr, b_body = trace(blue, tmp, "blue")
    r_tr, r_body = trace(red, tmp, "red")

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img"\n'
        '     aria-label="Swiftheat">\n'
        '  <title>Swiftheat</title>\n'
        '  <g fill="%s" transform="%s">%s</g>\n'
        '  <g fill="%s" transform="%s">%s</g>\n'
        '</svg>\n' % (w, h, BLUE, b_tr, b_body, RED, r_tr, r_body)
    )
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(svg)

    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
    print("%s  %d x %d  %d bytes" % (os.path.relpath(OUT, os.path.join(HERE, "..")), w, h, len(svg)))


if __name__ == "__main__":
    sys.exit(main())
