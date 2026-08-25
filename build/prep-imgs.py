#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepare the accessory photographs from the old site for the option catalogue.

    python3 build/prep-imgs.py

These are small photographs of real accessories: right angle exits, flanges,
threaded fittings and the three lead protections. They arrive on off white
studio backgrounds of three slightly different shades, which would show as three
different rectangles against the warm card surface. This knocks the background
out to transparency, trims the empty margin and writes the result back.

Flood fill from the border only, so a light area inside the product does not get
punched out with it.
"""
import os
from collections import deque

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "archive-old-site", "assets")
OUT = os.path.join(HERE, "..", "imgs")

FILES = [
    "Right-angle-exit.png", "Flange.png", "Heater-with-Spl-mountable-threads.png",
    "Silicon-coated-Fibreglass-sleeve.png", "Braided-Metal-sleeve.png", "Armour.png",
    "Flexible-Tubular-heaters.png",
]
TOL = 26          # how far from the border colour still counts as background


def knockout(im):
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    # The border colour is the median of the four corners, which is more robust
    # than any single corner on a photograph with a soft vignette.
    corners = [px[0, 0], px[w - 1, 0], px[0, h - 1], px[w - 1, h - 1]]
    opaque = [c[:3] for c in corners if c[3] > 16]
    if opaque:
        ref = tuple(sorted(c[i] for c in opaque)[len(opaque) // 2] for i in range(3))
    else:
        # Already transparent at the edges, but one of these was cut out around a
        # white studio card that is still in the frame. Chase the white too.
        ref = (255, 255, 255)
    if min(ref) < 200:            # not a light studio background, leave it alone
        return im
    seen = [[False] * w for _ in range(h)]
    q = deque()
    for x in range(w):
        q.append((x, 0)); q.append((x, h - 1))
    for y in range(h):
        q.append((0, y)); q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        if x < 0 or y < 0 or x >= w or y >= h or seen[y][x]:
            continue
        r, g, b, a = px[x, y]
        if a > 16 and (abs(r - ref[0]) > TOL or abs(g - ref[1]) > TOL or abs(b - ref[2]) > TOL):
            continue
        seen[y][x] = True
        px[x, y] = (r, g, b, 0)
        q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    for name in FILES:
        im = knockout(Image.open(os.path.join(SRC, name)))
        box = im.split()[3].getbbox()
        if box:
            im = im.crop(box)
        path = os.path.join(OUT, name)
        im.save(path, optimize=True)
        print("%-42s %4dx%-4d %6d bytes" % (name, im.width, im.height, os.path.getsize(path)))


if __name__ == "__main__":
    main()
