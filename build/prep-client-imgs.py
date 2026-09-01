#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepare the photographs the client supplied in docs/web 1.pptx.

    python3 build/prep-client-imgs.py

The client marked up screenshots of the preview site in PowerPoint and dropped a
photograph onto each slot they wanted filled. Those photographs come out of the
deck as ppt/media/imageNN, which is what docs/uploads-2026-08-31/web1-ppt-images
holds, byte for byte. This turns them into the three shapes the site uses:

  imgs/cards/   one per product family, for the family cards
  imgs/parts/   option thumbnails for the option catalogue
  imgs/photos/  the larger presentation images: hero, construction, selection

The background stays. An earlier cut of this knocked the studio ground out to
transparency so one picture could sit on a warm card and the next on a sunk
panel, and it cost real product: the white braided lead off the Type K
thermocouple, the fine wire off the grounded probe, and most of the pile of
ceramic beads, which came out as confetti. A flood fill cannot tell a white lead
on a white sweep from the sweep. So nothing is erased here. What comes off is
the border, and where the ground that is left is not the colour of the panel it
lands on, the panel is repainted to match it: every output records its own
ground colour in imgs/client-imgs.json and the build reads it back.

Sharpening is the other half. Most of these arrive between 200 and 500 px, which
is at or just under the size the page draws them at on a 2x screen, so they go
up by at most 1.4x on Lanczos and take an unsharp mask scaled to how far they
were stretched. That does not invent detail. It recovers the edge contrast the
resample costs, which is the part that reads as blur.

image40.jpg is deliberately absent: it carries another supplier's watermark.
"""
import json
import os
import sys
import warnings

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from imgprep import _hex, crop_borders, enhance, ground  # noqa: E402

ROOT = os.path.join(HERE, "..")
SRC = os.path.join(ROOT, "docs", "uploads-2026-08-31", "web1-ppt-images")
IMGS = os.path.join(ROOT, "imgs")
CARDS = os.path.join(IMGS, "cards")
PARTS = os.path.join(IMGS, "parts")
PHOTOS = os.path.join(IMGS, "photos")
META = os.path.join(IMGS, "client-imgs.json")

# Crops the client set in PowerPoint, as the deck records them: a fraction of
# each side, in hundred thousandths. Honouring them is not a nicety. On the coil
# selection shot the client cropped away half the frame, and a build that reads
# only ppt/media ships the half they cut.
PPT_CROP = {
    "image26.jpeg": {"l": 5461, "t": 12122, "r": 5598, "b": 5454},
    "image55.jpg": {"t": 26500, "b": 26917},
    "image65.jpg": {"t": 28584, "r": -2, "b": 18244},
    "image66.jpg": {"l": 25969, "r": 18744, "b": -1},
}

_meta = {}


def load(name, ppt_crop=True):
    im = Image.open(os.path.join(SRC, name))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        flat = Image.new("RGBA", im.size, (255, 255, 255, 255))
        im = Image.alpha_composite(flat, im)
    im = im.convert("RGB")
    if ppt_crop and name in PPT_CROP:
        im = _srcrect(im, PPT_CROP[name])
    return im


def _srcrect(im, c):
    """Apply a PowerPoint srcRect. Negative values are bleed, not a crop."""
    w, h = im.size
    return im.crop((int(w * max(0, c.get("l", 0)) / 100000),
                    int(h * max(0, c.get("t", 0)) / 100000),
                    w - int(w * max(0, c.get("r", 0)) / 100000),
                    h - int(h * max(0, c.get("b", 0)) / 100000)))


def save(im, path, quality=88, line_art=False, has_ground=True):
    """Write the picture and record its size and its ground colour.

    JPEG for a photograph. The one exception is the three coil exit drawings,
    which are pen on white: a palette PNG of those is both smaller than the
    JPEG and lossless, where a JPEG rings visibly along every line.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if line_art:
        q = im.quantize(colors=256, method=Image.FASTOCTREE)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            q.save(path, "PNG", optimize=True)
    else:
        im.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    # A photograph of a room has no studio ground, so it records none: it is
    # drawn cover, filling its box edge to edge, and there is no panel showing
    # round it that would need repainting to match.
    g = _hex(ground(np.asarray(im).astype(np.int16))) if has_ground else None
    key = os.path.relpath(path, IMGS).replace(os.sep, "/")
    _meta[key] = {"w": im.width, "h": im.height, "ground": g}
    return path, im.size, g


def prep(name, out, dest, target_h=None, target_w=None, max_up=1.4, cap=1600,
         crop=None, quality=88, line_art=False, tol=10, pad_frac=0.012):
    im = load(name)
    if crop:
        im = im.crop(crop)
    im = enhance(crop_borders(im, tol=tol, pad_frac=pad_frac),
                 target_h=target_h, target_w=target_w, max_up=max_up, cap=cap)
    return save(im, os.path.join(dest, out), quality=quality, line_art=line_art)


def pair(names, out, dest, target_h=None, gutter=14, quality=88):
    """Two photographs butted together with a gutter, for the one slot the
    client filled twice. Each keeps its own ground, so the gutter is drawn in
    the lighter of the two and the seam reads as two pictures rather than one
    picture with a tide line across it."""
    parts = [crop_borders(load(n)) for n in names]
    h = max(p.height for p in parts)
    parts = [p.resize((max(1, round(p.width * h / p.height)), h), Image.LANCZOS)
             if p.height != h else p for p in parts]
    grounds = [ground(np.asarray(p).astype(np.int16)) for p in parts]
    seam = tuple(int(v) for v in max(grounds, key=lambda g: g.mean()))
    W = sum(p.width for p in parts) + gutter * (len(parts) - 1)
    canvas = Image.new("RGB", (W, h), seam)
    x = 0
    for p in parts:
        canvas.paste(p, (x, 0))
        x += p.width + gutter
    return save(enhance(canvas, target_h=target_h, max_up=1.0), os.path.join(dest, out),
                quality=quality)


def panel(name, out, dest, box, cap=1000, sat=26, quality=88):
    """A rectangle lifted out of a composite the client assembled themselves.

    The panels are white cards with rounded corners on a blue to red gradient,
    so a rectangular crop keeps four slivers of that gradient in the corners.
    They read as purple and crimson flecks against the page.

    Whiten only the blobs of colour that actually contain a corner pixel. The
    first attempt whitened everything saturated within a margin of the edge,
    which is the same idea done bluntly, and it cost the end of "Element" and of
    "Electrical Connection" on the cartridge panel: those labels run close to the
    edge, and there is no margin wide enough to catch a rounded corner that does
    not also reach them. A corner sliver is connected to its corner and the
    labels are not, so connectivity separates them and crop tightness stops
    mattering.
    """
    im = load(name, ppt_crop=False).crop(box)
    a = np.asarray(im).astype(np.int16).copy()
    h, w, _ = a.shape
    lab, _ = ndimage.label((a.max(axis=2) - a.min(axis=2)) > sat)
    corners = {lab[0, 0], lab[0, w - 1], lab[h - 1, 0], lab[h - 1, w - 1]} - {0}
    if corners:
        a[np.isin(lab, list(corners))] = (255, 255, 255)
    im = crop_borders(Image.fromarray(a.astype(np.uint8), "RGB"))
    return save(enhance(im, target_w=cap, max_up=1.0), os.path.join(dest, out),
                quality=quality)


def photo(name, out, dest, box=None, cap=2000, quality=84):
    """A photograph of a room or a building. No ground to find and no border to
    take off, so it is only cropped and sized."""
    im = load(name)
    if box:
        im = im.crop(box)
    if im.width > cap:
        im = im.resize((cap, round(im.height * cap / im.width)), Image.LANCZOS)
    return save(im, os.path.join(dest, out), quality=quality, has_ground=False)


def photo_collage(names, out, dest, size=(1800, 1200), gutter=12, quality=80):
    """Several photographs butted together into one frame.

    Not the same job as pair(): these are rooms and buildings, not parts on a
    studio ground, so there is nothing to centre. Each is centre cropped to a
    single cell and the cells are laid side by side. Portrait cells, because
    every one of these came off a phone held upright and cropping them to
    landscape throws away the half that shows what the place is.
    """
    n = len(names)
    W, H = size
    cw = (W - gutter * (n - 1)) // n
    canvas = Image.new("RGB", (W, H), (255, 255, 255))
    for i, name in enumerate(names):
        im = load(name)
        scale = max(cw / im.width, H / im.height)
        im = im.resize((max(cw, round(im.width * scale)), max(H, round(im.height * scale))),
                       Image.LANCZOS)
        left = (im.width - cw) // 2
        top = (im.height - H) // 2
        canvas.paste(im.crop((left, top, left + cw, top + H)), (i * (cw + gutter), 0))
    return save(canvas, os.path.join(dest, out), quality=quality, has_ground=False)


# ---- one per product family, for the cards on home and products ------------
#
# Drawn 116 px tall inside a card that is at least 250 px wide, so 232 by about
# 440 covers a 2x screen. The width cap is the one that usually binds: a phone
# goes single column and draws these wider than the desktop grid does.
FAMILY_CARDS = [
    ("image9.jpg", "cartridge-heaters.jpg", {}),
    ("image10.jpg", "coil-heaters.jpg", {}),
    ("image11.png", "band-heaters.jpg", {}),
    ("image12.png", "nozzle-heaters.jpg", {}),
    ("image14.jpg", "strip-heaters.jpg", {}),
    ("image15.jpg", "tubular-heaters.jpg", {}),
    # The only one whose border is not found by measurement. It is a rounded
    # rule, so the last tenth of every side is corner radius and reads as
    # ground, and JPEG has left a warm three by three smudge in each of the four
    # corners outside it, which is far enough off white to be product and so
    # holds the box out past the rule. Crop inside the rule and the general
    # trim finishes the job.
    ("image16.jpg", "thermocouples-and-sensors.jpg", {"crop": (13, 13, 387, 317)}),
    ("image17.jpeg", "ceramic-infrared-heaters.jpg", {}),
]

# ---- option thumbnails, drawn in a 132 px slot -----------------------------
OPTION_PARTS = [
    ("image31.jpg", "ch-straight.jpg", {}),
    ("image33.jpg", "ch-ceramic-beading.jpg", {}),
    ("image35.jpg", "ch-thermocouple-j.jpg", {}),
    ("image36.jpg", "ch-thermocouple-k.jpg", {}),
    ("image37.png", "ch-thermocouple-grounded.jpg", {}),
    ("image38.png", "ch-strain-clamp.jpg", {}),
    ("image48.png", "co-exit-tangential.png", {"line_art": True}),
    ("image49.png", "co-exit-radial.png", {"line_art": True}),
    ("image50.png", "co-exit-axial.png", {"line_art": True}),
    ("image51.jpg", "co-thermocouple-none.jpg", {}),
    ("image52.jpg", "co-thermocouple-j.jpg", {}),
    ("image53.jpg", "co-thermocouple-k.jpg", {}),
]

# ---- the larger presentation images ----------------------------------------
#
# band-construction is not here: it is a line drawing with callout labels, it
# wants lossless, and build/relabel-band-cutaway.py owns it because the labels
# are reset into Inter on the way through.
PRESENTATION = [
    ("image57.jpg", "band-hero.jpg", {"cap": 1000}),
    ("image22.png", "products-hero.png", {"cap": 820, "max_up": 1.2}),
    ("image43.png", "coil-construction.jpg", {"target_h": 420}),
    ("image55.jpg", "coil-selection.jpg", {"cap": 900}),
    ("image24.jpg", "cartridge-hero.jpg", {"cap": 1000, "quality": 86}),
]


def main():
    print("family cards -> imgs/cards")
    for name, out, kw in FAMILY_CARDS:
        kw = dict(kw)
        kw.setdefault("target_h", 232)
        kw.setdefault("target_w", 440)
        p, size, g = prep(name, out, CARDS, **kw)
        print("  %-14s %-32s %4dx%-4d %7d B  ground %s"
              % (name, out, size[0], size[1], os.path.getsize(p), g))

    print("option thumbnails -> imgs/parts")
    for name, out, kw in OPTION_PARTS:
        kw = dict(kw)
        kw.setdefault("target_h", 264)
        kw.setdefault("target_w", 400)
        p, size, g = prep(name, out, PARTS, **kw)
        print("  %-14s %-32s %4dx%-4d %7d B  ground %s"
              % (name, out, size[0], size[1], os.path.getsize(p), g))

    print("presentation -> imgs/photos")
    for name, out, kw in PRESENTATION:
        p, size, g = prep(name, out, PHOTOS, **dict(kw))
        print("  %-14s %-32s %4dx%-4d %7d B  ground %s"
              % (name, out, size[0], size[1], os.path.getsize(p), g))

    # The client's own composite: three cutaway panels on a blue to red
    # gradient. The gradient fights every colour on the site, and the third
    # panel is a tubular heater, so the panels come out on their own. The
    # cartridge crop starts below the Swiftheat logo the client put at the top
    # of their first panel: the masthead already carries it, and a second one
    # inside a figure reads as a stock graphic rather than as our own drawing.
    print("client composite image26.jpeg -> panels")
    for out, box in [("cartridge-construction.jpg", (86, 268, 1379, 872)),
                     ("tubular-construction.jpg", (96, 911, 1367, 1582))]:
        p, size, g = panel("image26.jpeg", out, PHOTOS, box)
        print("  %-14s %-32s %4dx%-4d %7d B  ground %s"
              % ("image26.jpeg", out, size[0], size[1], os.path.getsize(p), g))

    # Two photographs for one slot: the band heater application shot. Both carry
    # a crop the client set in PowerPoint, which is where the framing came from.
    print("pair -> imgs/photos")
    p, size, g = pair(["image65.jpg", "image66.jpg"], "band-selection.jpg", PHOTOS)
    print("  %-14s %-32s %4dx%-4d %7d B  ground %s"
          % ("image65+66", "band-selection.jpg", size[0], size[1], os.path.getsize(p), g))

    # The home page hero. The client piled six photographs of the works onto
    # this one slot: three of the building, two of the floor, one of an engineer
    # at his desk. Three of them are already carrying the about and quality
    # pages, so this takes one frame from each of the three registers rather
    # than repeating either of those collages wholesale.
    print("home hero collage -> imgs/photos")
    p, size, g = photo_collage(["image1.jpeg", "image5.jpeg", "image7.jpeg"],
                               "home-hero-works.jpg", PHOTOS, size=(1100, 733))
    print("  %-14s %-32s %4dx%-4d %7d B  ground %s"
          % ("image1+5+7", "home-hero-works.jpg", size[0], size[1], os.path.getsize(p), g))

    print("photographs -> imgs/photos")
    p, size, g = photo("image30.jpeg", "cartridge-double-ended.jpg", PHOTOS,
                       box=(300, 250, 3450, 2300), cap=1200)
    print("  %-14s %-32s %4dx%-4d %7d B  ground %s"
          % ("image30.jpeg", "cartridge-double-ended.jpg", size[0], size[1],
             os.path.getsize(p), g))

    with open(META, "w", encoding="utf-8") as fh:
        json.dump(dict(sorted(_meta.items())), fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("\n%s  %d entries" % (os.path.relpath(META, ROOT), len(_meta)))


if __name__ == "__main__":
    main()
