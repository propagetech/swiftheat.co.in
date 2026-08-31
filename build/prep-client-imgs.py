#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepare the photographs the client supplied in docs/web 1.pptx.

    python3 build/prep-client-imgs.py

The client marked up screenshots of the preview site in PowerPoint and dropped a
photograph onto each slot they wanted filled. Those photographs come out of the
deck as ppt/media/imageNN, which is what docs/uploads-2026-08-31/web1-ppt-images
holds. This turns them into the three shapes the site actually uses:

  imgs/cards/   one cutout per product family, for the family cards
  imgs/parts/   option thumbnails, matching the existing knocked out accessories
  imgs/photos/  the larger presentation images: hero, construction, selection

Nearly all of them arrive on a flat studio background: white for most, a blue
gradient for the products montage, a pale blue grey for the cartridge group.
Knocking that out to transparency is what lets one sit on a warm card surface
and the next on a sunk panel without three different rectangles showing. The
flood fill starts at the border and compares each candidate against the pixel it
came from, so it follows a smooth gradient outward but stops at the product edge.

image40.jpg is deliberately absent: it carries another supplier's watermark.
"""
import os
import warnings
from collections import deque

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SRC = os.path.join(ROOT, "docs", "uploads-2026-08-31", "web1-ppt-images")
CARDS = os.path.join(ROOT, "imgs", "cards")
PARTS = os.path.join(ROOT, "imgs", "parts")
PHOTOS = os.path.join(ROOT, "imgs", "photos")


def load(name):
    im = Image.open(os.path.join(SRC, name))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        flat = Image.new("RGBA", im.size, (255, 255, 255, 255))
        im = Image.alpha_composite(flat, im)
    return im.convert("RGB")


def _label(mask):
    """Label the True regions of mask with 1..n, background 0."""
    out = np.zeros(mask.shape, np.int32)
    n = 0
    h, w = mask.shape
    for sy in range(h):
        for sx in range(w):
            if not mask[sy, sx] or out[sy, sx]:
                continue
            n += 1
            q = deque([(sx, sy)])
            out[sy, sx] = n
            while q:
                x, y = q.popleft()
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < w and 0 <= ny < h and mask[ny, nx] and not out[ny, nx]:
                        out[ny, nx] = n
                        q.append((nx, ny))
    return out, n


def _components(mask):
    """Label the True regions of mask. Yields (indices, touches_border)."""
    h, w = mask.shape
    seen = np.zeros((h, w), bool)
    for sy in range(h):
        row = mask[sy]
        for sx in range(w):
            if not row[sx] or seen[sy, sx]:
                continue
            q = deque([(sx, sy)])
            seen[sy, sx] = True
            pts = []
            edge = False
            while q:
                x, y = q.popleft()
                pts.append((y, x))
                if x == 0 or y == 0 or x == w - 1 or y == h - 1:
                    edge = True
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < w and 0 <= ny < h and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((nx, ny))
            yield pts, edge


def knockout(im, local=30, glob=70, hole=180, hole_tol=12, blue=False):
    """Punch the studio background out to transparency.

    local  how far a neighbour may drift from the pixel it was reached from,
           which is what lets a gradient background come out in one piece
    glob   how far it may drift from the border colour overall, so a smooth
           ramp into the product does not carry the fill inside with it
    hole   an enclosed patch of background this size or larger also goes. The
           inside of a coil loop or a clamp is background too, and the border
           fill can never reach it. Small patches stay: those are specular
           highlights on steel, and punching them out drills holes in the part.
    blue   separate on hue instead of distance. Used for the one montage that
           arrives on a saturated blue gradient, where the products are grey
           and white and so are cleanly on the other side of the hue split.
    """
    rgb = np.asarray(im).astype(np.int16)
    h, w, _ = rgb.shape

    if blue:
        b = rgb[..., 2]
        warm = np.maximum(rgb[..., 0], rgb[..., 1])
        bg = (b - warm) > 22
    else:
        ref = np.median(np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]]), axis=0)
        bg = np.full((h, w), False)
        q = deque()
        for x in range(w):
            q.append((x, 0, rgb[0, x]))
            q.append((x, h - 1, rgb[h - 1, x]))
        for y in range(h):
            q.append((0, y, rgb[y, 0]))
            q.append((w - 1, y, rgb[y, w - 1]))
        while q:
            x, y, came = q.popleft()
            if x < 0 or y < 0 or x >= w or y >= h or bg[y, x]:
                continue
            px = rgb[y, x]
            if np.abs(px - came).max() > local or np.abs(px - ref).max() > glob:
                continue
            bg[y, x] = True
            q.append((x + 1, y, px)); q.append((x - 1, y, px))
            q.append((x, y + 1, px)); q.append((x, y - 1, px))

        # Enclosed background the border fill could not reach.
        flat = (np.abs(rgb - ref).max(axis=2) <= hole_tol) & ~bg
        for pts, _ in _components(flat):
            if len(pts) >= hole:
                ys, xs = zip(*pts)
                bg[list(ys), list(xs)] = True

    # Close pinholes: a handful of pixels of background surrounded by product is
    # compression noise, and it reads as dirt on the part.
    #
    # There is deliberately no pass in the other direction. Removing small
    # islands of product looks like the same tidying job, but a callout label is
    # made of small islands: it costs the dot of every i and the stem of every l,
    # and the first cut of this silently ate six words off the band heater
    # cutaway. Stray specks in the background are the cheaper mistake.
    for pts, edge in _components(bg):
        if not edge and len(pts) <= 12:
            ys, xs = zip(*pts)
            bg[list(ys), list(xs)] = False

    res = np.dstack([rgb.astype(np.uint8), np.where(bg, 0, 255).astype(np.uint8)])

    if blue:
        # Neutralise the blue that survives as a halo on the product edges.
        keep = ~bg
        b = res[..., 2].astype(np.int16)
        warm = np.maximum(res[..., 0], res[..., 1]).astype(np.int16)
        fringe = keep & ((b - warm) > 8)
        res[..., 2] = np.where(fringe, warm, b).astype(np.uint8)

    return Image.fromarray(res, "RGBA")


def trim(im, pad=0):
    box = im.split()[3].getbbox() if im.mode == "RGBA" else im.getbbox()
    if not box:
        return im
    if pad:
        box = (max(0, box[0] - pad), max(0, box[1] - pad),
               min(im.width, box[2] + pad), min(im.height, box[3] + pad))
    return im.crop(box)


def fit(im, w, h):
    """Contain im inside w by h without upscaling past 2x, keeping aspect."""
    scale = min(w / im.width, h / im.height)
    scale = min(scale, 2.0)
    return im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))),
                     Image.LANCZOS)


def flat_jpeg(im, path, quality=88):
    """Composite the cutout onto white and write it as a photograph.

    --surface is #fff, and every slot these land in is painted --surface, so the
    white ground is invisible and the transparency was never buying anything.
    What it cost was real: a photographic montage of steel forced through 256
    palette entries bands visibly across every smooth face, and on the band
    heater hero the palette PNG was both larger than this JPEG and six times
    further from the original. Cutouts still go out as PNG wherever the ground
    behind them is not white, which is the product cards on their sunk panel.
    """
    white = Image.new("RGBA", im.size, (255, 255, 255, 255))
    out = Image.alpha_composite(white, im.convert("RGBA")).convert("RGB")
    out.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    return path


def save_png(im, path, p95=4, worst=24, display_h=None):
    """Write the cutout, palettised only when that is smaller and near enough.

    Judge the loss where the image is opaque: a palette PNG carries one
    transparent index, so everything under the knocked out ground collapses to a
    single colour, which scores terribly and is never seen.

    The test is on the 95th percentile and the worst pixel, not the mean. The
    first cut of this allowed a mean of 12, which a photograph of brushed steel
    passes comfortably while banding right across the middle of every face:
    the mean is held down by the large flat areas that quantise perfectly, and
    it hides exactly the gradients that show. Line art and text pass this
    easily; photographs mostly do not, and should be going through flat_jpeg.
    """
    im.save(path, "PNG", optimize=True)
    plain = os.path.getsize(path)
    try:
        q = im.quantize(colors=256, method=Image.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG)
        alt = path + ".palette.png"
        q.save(alt, "PNG", optimize=True)
        keep = os.path.getsize(alt) < plain
        if keep and im.mode == "RGBA":
            with warnings.catch_warnings():
                # Reading back a palette PNG whose transparency is a byte string.
                warnings.simplefilter("ignore", UserWarning)
                back = Image.open(alt).convert("RGBA")
            ref, got = im, back
            if display_h:
                # Judge the loss at the size the browser will draw it, not at the
                # size it is stored. These are exported at twice their drawn
                # height, so the downscale averages dithering back out; scoring
                # the dither at full size rejects a palette that is in fact
                # indistinguishable on the page.
                k = display_h / im.height
                if k < 1:
                    wh = (max(1, round(im.width * k)), display_h)
                    ref = im.resize(wh, Image.LANCZOS)
                    got = back.resize(wh, Image.LANCZOS)
            a = np.asarray(ref.split()[3]).astype(np.int16)
            before = np.asarray(ref.convert("RGB"), dtype=np.int16)
            after = np.asarray(got.convert("RGB"), dtype=np.int16)
            solid = a > 200
            if solid.any():
                d = np.abs(before - after).max(axis=2)[solid]
                keep = np.percentile(d, 95) <= p95 and d.max() <= worst
        if keep:
            os.replace(alt, path)
        else:
            os.remove(alt)
    except (ValueError, OSError):
        pass
    return path


def cut_jpeg(name, out, dest, quality=88, **kw):
    """Cut the studio ground off, then flatten back onto white and ship a JPEG.

    The knockout still earns its keep here even though the result is opaque: it
    is what finds the edge of the product so the frame can be trimmed to it, and
    it removes the gradient and the drop shadows that the original was shot on.
    """
    im, size = _prepare(name, **kw)
    os.makedirs(dest, exist_ok=True)
    return flat_jpeg(im, os.path.join(dest, out), quality), size


def _prepare(name, local=30, glob=70, cap=1600, crop=None, blue=False,
             hole=180, hole_tol=12, cap_h=None):
    im = load(name)
    if crop:
        im = im.crop(crop)
    im = trim(knockout(im, local, glob, hole=hole, hole_tol=hole_tol, blue=blue))
    # Cap the longest side, not the width: these are exported at about twice the
    # size they are drawn at, and several of them are portrait.
    longest = max(im.size)
    k = min(cap / longest, 1.0)
    if cap_h:
        # What the CSS actually constrains on a card and an option shot is the
        # height, so that is what decides the export size. Capping the long side
        # alone leaves a tall part carrying three times the pixels it can show.
        k = min(k, cap_h / im.height)
    if k < 1:
        im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    return im, im.size


def cutout(name, out, dest, display_h=None, **kw):
    """A cutout that keeps its transparency, for the ground that is not white.

    The option catalogue and the product cards both sit on --paper or
    --surface-sunk rather than white, so these cannot be flattened the way the
    presentation photographs are: a white rectangle would show.
    """
    im, size = _prepare(name, **kw)
    os.makedirs(dest, exist_ok=True)
    return save_png(im, os.path.join(dest, out), display_h=display_h), size


def collage(names, out, dest, cell=(760, 700), gutter=64, pad=48, local=30, glob=70, cap=1000):
    """Two or more cutouts on one transparent canvas, each fitted to an equal
    cell and centred in it. Equal cells rather than a shared scale: these arrive
    at unrelated magnifications, so matching the frames reads as deliberate
    where matching the pixels would just look accidental."""
    parts = [trim(knockout(load(n), local, glob)) for n in names]
    parts = [fit(p, *cell) for p in parts]
    n = len(parts)
    W = pad * 2 + cell[0] * n + gutter * (n - 1)
    H = pad * 2 + cell[1]
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for i, p in enumerate(parts):
        cx = pad + i * (cell[0] + gutter) + (cell[0] - p.width) // 2
        cy = pad + (cell[1] - p.height) // 2
        canvas.paste(p, (cx, cy), p)
    canvas = trim(canvas, pad=pad // 2)
    longest = max(canvas.size)
    if longest > cap:
        k = cap / longest
        canvas = canvas.resize((round(canvas.width * k), round(canvas.height * k)), Image.LANCZOS)
    os.makedirs(dest, exist_ok=True)
    return flat_jpeg(canvas, os.path.join(dest, out)), canvas.size


def photo_collage(names, out, dest, size=(1800, 1200), gutter=12, quality=80):
    """Several photographs butted together into one frame.

    Not the same job as collage(): these are rooms and buildings, not parts on a
    studio ground, so there is no background to knock out and nothing to centre.
    Each one is centre cropped to a single cell and the cells are laid side by
    side, which is how the two collages already on the site are built. Portrait
    cells, because every one of these came off a phone held upright and cropping
    them to landscape throws away the half that shows what the place is.
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
    os.makedirs(dest, exist_ok=True)
    path = os.path.join(dest, out)
    canvas.save(path, "JPEG", optimize=True, quality=quality, progressive=True)
    return path, canvas.size


def panel(name, out, dest, box, cap=1000, sat=26):
    """A rectangle lifted out of a composite the client assembled themselves.

    The panels are white cards with rounded corners on a blue to red gradient, so
    a rectangular crop keeps four slivers of that gradient in the corners. They
    read as purple and crimson flecks against the page.

    Whiten only the blobs of colour that actually contain a corner pixel. The
    first attempt whitened everything saturated within a margin of the edge,
    which is the same idea done bluntly, and it cost the end of "Element" and of
    "Electrical Connection" on the cartridge panel: those labels run close to the
    edge, and there is no margin wide enough to catch a rounded corner that does
    not also reach them. A corner sliver is connected to its corner and the
    labels are not, so connectivity separates them and crop tightness stops
    mattering.
    """
    im = load(name).crop(box)
    a = np.asarray(im).astype(np.int16).copy()
    h, w, _ = a.shape
    coloured = (a.max(axis=2) - a.min(axis=2)) > sat
    lab, _ = _label(coloured)
    corners = {lab[0, 0], lab[0, w - 1], lab[h - 1, 0], lab[h - 1, w - 1]} - {0}
    if corners:
        a[np.isin(lab, list(corners))] = (255, 255, 255)
    im = Image.fromarray(a.astype(np.uint8), "RGB")
    if im.width > cap:
        im = im.resize((cap, round(im.height * cap / im.width)), Image.LANCZOS)
    os.makedirs(dest, exist_ok=True)
    path = os.path.join(dest, out)
    im.save(path, optimize=True, quality=88)
    return path, im.size


def photo(name, out, dest, box=None, cap=2000, quality=82):
    im = load(name)
    if box:
        im = im.crop(box)
    if im.width > cap:
        im = im.resize((cap, round(im.height * cap / im.width)), Image.LANCZOS)
    os.makedirs(dest, exist_ok=True)
    path = os.path.join(dest, out)
    im.save(path, optimize=True, quality=quality, progressive=True)
    return path, im.size


# ---- one cutout per product family, for the cards on home and products ------
# image16 arrives as a rounded white card on white: the border fill stops at the
# card outline and leaves it drawn on the page, so crop inside the outline first.
FAMILY_CARDS = [
    ("image9.jpg", "cartridge-heaters.png", {}),
    ("image10.jpg", "coil-heaters.png", {}),
    ("image11.png", "band-heaters.png", {}),
    ("image12.png", "nozzle-heaters.png", {}),
    ("image14.jpg", "strip-heaters.png", {}),
    ("image15.jpg", "tubular-heaters.png", {}),
    ("image16.jpg", "thermocouples-and-sensors.png", {"crop": (13, 13, 387, 317)}),
    ("image17.jpeg", "ceramic-infrared-heaters.png", {"local": 26, "glob": 60}),
]

# ---- option thumbnails, to sit beside the existing knocked out accessories --
OPTION_PARTS = [
    ("image31.jpg", "ch-straight.png", {}),
    ("image33.jpg", "ch-ceramic-beading.png", {"local": 22, "glob": 58}),
    ("image35.jpg", "ch-thermocouple-j.png", {"hole_tol": 26}),
    ("image36.jpg", "ch-thermocouple-k.png", {}),
    ("image37.png", "ch-thermocouple-grounded.png", {}),
    ("image38.png", "ch-strain-clamp.png", {}),
    ("image48.png", "co-exit-tangential.png", {}),
    ("image49.png", "co-exit-radial.png", {}),
    ("image50.png", "co-exit-axial.png", {}),
    ("image51.jpg", "co-thermocouple-none.png", {}),
    # Soft shadow inside the braided loop, so the enclosed background
    # needs a looser match than a flat studio ground.
    ("image52.jpg", "co-thermocouple-j.png", {"hole_tol": 34}),
    ("image53.jpg", "co-thermocouple-k.png", {}),
]

# ---- the larger presentation images ----------------------------------------
#
# All of these are photographs, so they go out as JPEG flattened onto white
# rather than as palettised cutouts. See flat_jpeg for why.
#
# band-construction is not here: it is a line drawing with callout labels, it
# wants lossless, and build/relabel-band-cutaway.py owns it because the labels
# are reset into Inter on the way through.
PRESENTATION = [
    ("image57.jpg", "band-hero.jpg", {}),
    ("image22.png", "products-hero.jpg", {"blue": True}),
    ("image43.png", "coil-construction.jpg", {}),
    ("image55.jpg", "coil-selection.jpg", {}),
]


def main():
    for label, dest, table, cap, drawn in (("family cards -> imgs/cards", CARDS, FAMILY_CARDS, 420, 116),
                                    ("option thumbnails -> imgs/parts", PARTS, OPTION_PARTS, 300, 132)):
        print(label)
        for name, out, kw in table:
            kw = dict(kw)
            kw.setdefault("cap", cap)
            kw.setdefault("cap_h", drawn * 2)
            p, size = cutout(name, out, dest, display_h=drawn, **kw)
            print("  %-34s %-32s %dx%d %7d B"
                  % (name, out, size[0], size[1], os.path.getsize(p)))

    print("presentation -> imgs/photos")
    for name, out, kw in PRESENTATION:
        kw = dict(kw)
        kw.setdefault("cap", 1000)
        p, size = cut_jpeg(name, out, PHOTOS, **kw)
        print("  %-34s %-32s %dx%d %7d B"
              % (name, out, size[0], size[1], os.path.getsize(p)))

    # The client's own composite: three cutaway panels on a blue to red
    # gradient. The gradient fights every colour on the site, and the third
    # panel is a tubular heater, so the panels come out on their own. The
    # cartridge crop starts below the Swiftheat logo the client put at the top
    # of their first panel: the masthead already carries it, and a second one
    # inside a figure reads as a stock graphic rather than as our own drawing.
    print("client composite image26.jpeg -> panels")
    for out, box in [("cartridge-construction.jpg", (86, 268, 1379, 872)),
                     ("tubular-construction.jpg", (96, 911, 1367, 1582))]:
        p, size = panel("image26.jpeg", out, PHOTOS, box)
        print("  %-34s %-32s %dx%d %6d B" % ("image26.jpeg", out, size[0], size[1],
                                             os.path.getsize(p)))

    # Two photographs for one slot: the band heater application shot.
    print("collage -> imgs/photos")
    p, size = collage(["image65.jpg", "image66.jpg"], "band-selection.jpg", PHOTOS)
    print("  %-34s %-32s %dx%d %6d B" % ("image65+image66", "band-selection.jpg",
                                         size[0], size[1], os.path.getsize(p)))

    # The home page hero. The client piled six photographs of the works onto
    # this one slot: three of the building, two of the floor, one of an engineer
    # at his desk. Three of them are already carrying the about and quality
    # pages, so this takes one frame from each of the three registers rather
    # than repeating either of those collages wholesale.
    print("home hero collage -> imgs/photos")
    p, size = photo_collage(["image1.jpeg", "image5.jpeg", "image7.jpeg"],
                            "home-hero-works.jpg", PHOTOS, size=(1100, 733))
    print("  %-34s %-32s %dx%d %7d B" % ("image1+image5+image7", "home-hero-works.jpg",
                                         size[0], size[1], os.path.getsize(p)))

    # Photographs rather than cutouts.
    #
    # image24 was a cutout first and it cost the leads: the pale blue grey
    # studio ground runs from 215 to 255, the white braided fibreglass leads sit
    # inside that range, and no distance or hue threshold separates them without
    # eating the leads a strand at a time. A clean rectangle inside the hero
    # figure beats a cutout with its wiring nibbled off.
    #
    # image30 is a seamless grey sweep, which is a photograph by any measure.
    print("photographs -> imgs/photos")
    p, size = photo("image24.jpg", "cartridge-hero.jpg", PHOTOS, cap=1000, quality=84)
    print("  %-34s %-32s %dx%d %7d B" % ("image24.jpg", "cartridge-hero.jpg",
                                         size[0], size[1], os.path.getsize(p)))
    p, size = photo("image30.jpeg", "cartridge-double-ended.jpg", PHOTOS,
                    box=(300, 250, 3450, 2300), cap=1200)
    print("  %-34s %-32s %dx%d %6d B" % ("image30.jpeg", "cartridge-double-ended.jpg",
                                         size[0], size[1], os.path.getsize(p)))


if __name__ == "__main__":
    main()
