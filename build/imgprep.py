# -*- coding: utf-8 -*-
"""Measuring and trimming the photographs the client supplies.

The client asked for the borders off the pictures in docs/web 1.pptx and the
backgrounds left alone. That is one job with two halves, and both halves are
here so that every script preparing a client picture does them the same way:
find what the studio ground actually is, take off the border drawn or framed
around it, and resample to the size the page draws it at without inventing
detail.

Used by build/prep-client-imgs.py and build/relabel-band-cutaway.py.
"""
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage


def ground(a):
    """The colour of the studio ground, read off the outer ring.

    The mode of the ring, not the median. Several of these carry a sliver of
    white matte down one side where the client pasted the photograph onto a
    slide, and on the blue montage that sliver drags a median far enough off the
    blue that nothing downstream can tell ground from product.
    """
    ring = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    q = ring // 6
    key = q[:, 0] * 4096 + q[:, 1] * 64 + q[:, 2]
    vals, counts = np.unique(key, return_counts=True)
    return np.median(ring[key == vals[counts.argmax()]], axis=0)


def content(a, g, tol=10):
    """Everything that is not the ground, with single pixel speckle dropped.

    This is a colour test per pixel, never a flood fill. A flood fill walks from
    the border and can walk straight up a white lead; a colour test cannot,
    because it never asks what a pixel is connected to.
    """
    return ndimage.binary_opening(np.abs(a - g).max(axis=2) > tol, np.ones((3, 3)))


def _bbox(sub, g, tol):
    m = content(sub, g, tol)
    if not m.any():
        return None
    rows = np.where(m.any(axis=1))[0]
    cols = np.where(m.any(axis=0))[0]
    return int(rows[0]), int(rows[-1]) + 1, int(cols[0]), int(cols[-1]) + 1


def crop_borders(im, tol=10, pad_frac=0.012, max_frame=0.10):
    """Take the borders off, and nothing else.

    Two kinds turn up in this deck. One is the flat margin of ground the shot
    was framed with, which leaves the product small in the middle of a lot of
    nothing. The other is a rule the supplier drew round the picture, or the
    sliver of white matte left where the client pasted a photograph onto a
    coloured slide. Both come off. What sits between them and the product is the
    background, and that is left exactly as it was shot.

    The ground colour is read once, off the original, and then held. Re-reading
    it after each crop looks like the same thing and is not: once the margin has
    gone the ring is mostly product, the estimate follows it inward, and the box
    eats the part a slice at a time. That is how the first cut of this took the
    left hand probe off the grounded thermocouple.

    The two passes alternate because a drawn rule only reaches the edge once the
    outer margin has gone, and there is usually a second margin inside the rule.
    """
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    g = ground(a)
    t, b, l, r = 0, h, 0, w
    lim = max(3, int(min(h, w) * max_frame))
    cut = 0
    for _ in range(64):
        sub = a[t:b, l:r]
        if sub.shape[0] < 8 or sub.shape[1] < 8:
            break
        box = _bbox(sub, g, tol)
        if box is None:
            break
        if box != (0, sub.shape[0], 0, sub.shape[1]):
            y0, y1, x0, x1 = box
            t, b, l, r = t + y0, t + y1, l + x0, l + x1
            continue
        if cut >= lim:
            break
        # No ground left to trim, so every edge is either the product itself or
        # a border drawn over it. A drawn border runs the full length of its
        # side and holds one colour along it; a product that happens to reach
        # the edge does neither, which is what stops the pile of ceramic beads
        # that fills its own frame from being shaved a row at a time.
        m = content(sub, g, tol)
        moved = False
        for side in "tblr":
            line = {"t": sub[0], "b": sub[-1], "l": sub[:, 0], "r": sub[:, -1]}[side]
            hit = {"t": m[0], "b": m[-1], "l": m[:, 0], "r": m[:, -1]}[side]
            # Judge the middle of the line, not its ends. The rule round the
            # thermocouple group is a rounded rectangle, so the last tenth at
            # each end of every side is the corner radius and is ground; testing
            # the whole line scores that rule at 0.8 and leaves it on the page.
            n = len(line)
            core = slice(n // 10, n - n // 10) if n >= 20 else slice(None)
            line, hit = line[core], hit[core]
            if hit.mean() >= 0.95 and (line.max(axis=0) - line.min(axis=0)).max() <= 18:
                t, b, l, r = (t + 1, b, l, r) if side == "t" else \
                             (t, b - 1, l, r) if side == "b" else \
                             (t, b, l + 1, r) if side == "l" else (t, b, l, r - 1)
                moved = True
        if not moved:
            break
        cut += 1
    # Hand back a small even margin of the picture's own ground, so the product
    # is not flush against the edge of the box the page draws it in.
    pad = int(round(max(b - t, r - l) * pad_frac))
    return im.crop((max(0, l - pad), max(0, t - pad),
                    min(w, r + pad), min(h, b + pad)))


def enhance(im, target_h=None, target_w=None, max_up=1.4, cap=1600):
    """Resample to the size the page draws it at, then restore the edge.

    Never past max_up. These are 200 to 500 px originals and no resample adds
    detail; past about 1.4x the mask is sharpening its own interpolation, which
    reads as a crayon outline round every part. Small and sharp beats big and
    soft, which is the same rule the option catalogue is laid out under.
    """
    k = min(cap / max(im.size), max_up)
    if target_h:
        k = min(k, target_h / im.height)
    if target_w:
        k = min(k, target_w / im.width)
    if abs(k - 1) > 0.01:
        im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))),
                       Image.LANCZOS)
    # Scale the mask to how far it was stretched, and hold a threshold so the
    # flat ground does not come back as JPEG noise.
    pct = int(min(150, 60 + 110 * max(0.0, k - 1)))
    return im.filter(ImageFilter.UnsharpMask(radius=1.1, percent=pct, threshold=3))


def _hex(g):
    return "#%02x%02x%02x" % tuple(int(round(v)) for v in g)
