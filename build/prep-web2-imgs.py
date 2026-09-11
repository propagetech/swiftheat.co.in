#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepare photographs the client dropped onto docs/web 2.pptx.

    python3 build/prep-web2-imgs.py

Merges new entries into imgs/client-imgs.json. Skips assets that are not
publishable as Swiftheat photography: the stock quality-assurance graphic
(image58), the Google Street View of an unrelated shopfront (image75), the
third-party thermocouple infographic (image41), and the rod-end part that was
misplaced on the tubular options slide (image23).
"""
import json
import os
import sys
import warnings

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from imgprep import _hex, crop_borders, enhance, ground  # noqa: E402

ROOT = os.path.join(HERE, "..")
SRC = os.path.join(ROOT, "docs", "uploads-2026-09-11", "web2-ppt-images")
# Prefer the labelled Website images folder when the same frame exists there.
WEB = os.path.join(ROOT, "docs", "Website images")
IMGS = os.path.join(ROOT, "imgs")
PARTS = os.path.join(IMGS, "parts")
PHOTOS = os.path.join(IMGS, "photos")
META = os.path.join(IMGS, "client-imgs.json")

_meta = {}
if os.path.exists(META):
    with open(META, encoding="utf-8") as fh:
        _meta.update(json.load(fh))


def load(name, folder=SRC):
    path = os.path.join(folder, name)
    if not os.path.exists(path) and folder == SRC:
        # Fall back to Website images / extracted media names.
        alt = os.path.join(WEB, name)
        if os.path.exists(alt):
            path = alt
    im = Image.open(path)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        flat = Image.new("RGBA", im.size, (255, 255, 255, 255))
        im = Image.alpha_composite(flat, im)
    return im.convert("RGB")


def load_web(name):
    return load(name, WEB)


def save(im, path, quality=88, line_art=False, has_ground=True):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if line_art:
        q = im.quantize(colors=256, method=Image.FASTOCTREE)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            q.save(path, "PNG", optimize=True)
    else:
        im.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    g = _hex(ground(np.asarray(im).astype(np.int16))) if has_ground else None
    key = os.path.relpath(path, IMGS).replace(os.sep, "/")
    _meta[key] = {"w": im.width, "h": im.height, "ground": g}
    return path, im.size, g


def prep_file(im, out, dest, target_h=None, target_w=None, max_up=1.4, cap=1600,
              quality=88, has_ground=True, tol=10, pad_frac=0.012):
    im = enhance(crop_borders(im, tol=tol, pad_frac=pad_frac),
                 target_h=target_h, target_w=target_w, max_up=max_up, cap=cap)
    return save(im, os.path.join(dest, out), quality=quality, has_ground=has_ground)


def prep(name, out, dest, folder=SRC, **kw):
    return prep_file(load(name, folder), out, dest, **kw)


def pair(ims, out, dest, target_h=None, gutter=14, quality=88):
    parts = [crop_borders(im) for im in ims]
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
    return save(enhance(canvas, target_h=target_h, max_up=1.0),
                os.path.join(dest, out), quality=quality)


def photo_room(im, out, dest, cap=1600, quality=84):
    """Works / plant photograph: cover fill, no studio ground."""
    if im.width > cap:
        im = im.resize((cap, round(im.height * cap / im.width)), Image.LANCZOS)
    return save(im, os.path.join(dest, out), quality=quality, has_ground=False)


def log(src, out, size, path, g):
    print("  %-28s %-36s %4dx%-4d %7d B  ground %s"
          % (src, out, size[0], size[1], os.path.getsize(path), g))


def main():
    print("strip heaters")
    p, size, g = prep("image6.jpg", "strip-hero.jpg", PHOTOS, cap=1000)
    log("image6.jpg", "strip-hero.jpg", size, p, g)
    # Prefer the labelled Website file when present (same frame as image9).
    src9 = "Strip heater 2.jpg" if os.path.exists(os.path.join(WEB, "Strip heater 2.jpg")) else "image9.jpg"
    folder9 = WEB if src9.startswith("Strip") else SRC
    p, size, g = prep(src9 if folder9 == WEB else "image9.jpg", "strip-construction.jpg",
                      PHOTOS, folder=folder9, cap=900)
    log(src9, "strip-construction.jpg", size, p, g)
    p, size, g = prep("image14.jpg", "strip-selection.jpg", PHOTOS, cap=900)
    log("image14.jpg", "strip-selection.jpg", size, p, g)
    p, size, g = prep("image11.png", "sh-plain.jpg", PARTS, target_h=264, target_w=400)
    log("image11.png", "sh-plain.jpg", size, p, g)
    finned = os.path.join(WEB, "Finned Strip heater.jpg")
    if os.path.exists(finned):
        p, size, g = prep_file(load_web("Finned Strip heater.jpg"), "sh-finned.jpg", PARTS,
                               target_h=264, target_w=400)
        log("Finned Strip heater.jpg", "sh-finned.jpg", size, p, g)

    print("tubular heaters")
    p, size, g = prep("image17.png", "tubular-hero.jpg", PHOTOS, cap=900)
    log("image17.png", "tubular-hero.jpg", size, p, g)
    p, size, g = pair([load("image24.jpg"), load("image30.jpg"), load("image31.png")],
                      "tubular-selection.jpg", PHOTOS, target_h=420)
    log("image24+30+31", "tubular-selection.jpg", size, p, g)
    p, size, g = prep("image24.jpg", "th-u-form.jpg", PARTS, target_h=264, target_w=400)
    log("image24.jpg", "th-u-form.jpg", size, p, g)
    p, size, g = prep("image25.jpg", "th-w-form.jpg", PARTS, target_h=264, target_w=400)
    log("image25.jpg", "th-w-form.jpg", size, p, g)
    p, size, g = prep("image32.jpg", "th-coiled.jpg", PARTS, target_h=264, target_w=400)
    log("image32.jpg", "th-coiled.jpg", size, p, g)
    # Line-art bend-form sheet the client put on the construction slot: keep as
    # a parts reference rather than replacing the cutaway construction photo.
    p, size, g = prep("image19.png", "th-bend-forms.jpg", PHOTOS, cap=900, max_up=1.2)
    log("image19.png", "th-bend-forms.jpg", size, p, g)

    print("thermocouples and sensors")
    p, size, g = prep("image35.jpg", "sensors-hero.jpg", PHOTOS, cap=1000)
    log("image35.jpg", "sensors-hero.jpg", size, p, g)
    p, size, g = pair([load("image37.jpg"), load("image38.png")],
                      "sensors-construction.jpg", PHOTOS, target_h=420)
    log("image37+38", "sensors-construction.jpg", size, p, g)
    # Selection: client GIF is a third-party infographic. Use their own product
    # stills from the Website images set instead.
    sel_names = []
    for n in ("Thermocouples.jpg", "Thermocouples1.jpg", "thermocouple4.jpg"):
        if os.path.exists(os.path.join(WEB, n)):
            sel_names.append(n)
    if len(sel_names) >= 2:
        p, size, g = pair([load_web(n) for n in sel_names[:3]],
                          "sensors-selection.jpg", PHOTOS, target_h=420)
        log("+".join(sel_names[:3]), "sensors-selection.jpg", size, p, g)
    else:
        p, size, g = prep("image38.png", "sensors-selection.jpg", PHOTOS, cap=900)
        log("image38.png", "sensors-selection.jpg", size, p, g)

    print("ceramic infrared")
    ir_hero = "Ceramic ir heater.jpeg"
    if os.path.exists(os.path.join(WEB, ir_hero)):
        p, size, g = prep(ir_hero, "ir-hero.jpg", PHOTOS, folder=WEB, cap=800, max_up=1.6)
        log(ir_hero, "ir-hero.jpg", size, p, g)
    else:
        p, size, g = prep("image44.jpeg", "ir-hero.jpg", PHOTOS, cap=800, max_up=1.6)
        log("image44.jpeg", "ir-hero.jpg", size, p, g)
    p, size, g = prep("image46.jpg", "ir-construction.jpg", PHOTOS, folder=SRC, cap=1400)
    # Prefer the high-res Website file when present.
    if os.path.exists(os.path.join(WEB, "ceramic-infrared-heater.jpg")):
        p, size, g = prep("ceramic-infrared-heater.jpg", "ir-construction.jpg", PHOTOS,
                          folder=WEB, cap=1400)
        log("ceramic-infrared-heater.jpg", "ir-construction.jpg", size, p, g)
    else:
        log("image46.jpg", "ir-construction.jpg", size, p, g)
    p, size, g = prep("image50.png", "ir-selection.jpg", PHOTOS, cap=900)
    log("image50.png", "ir-selection.jpg", size, p, g)
    if os.path.exists(os.path.join(WEB, "ceramic-infrared-heater2.jpg")):
        p, size, g = prep("ceramic-infrared-heater2.jpg", "ir-flat-panel.jpg", PARTS,
                          folder=WEB, target_h=264, target_w=400)
        log("ceramic-infrared-heater2.jpg", "ir-flat-panel.jpg", size, p, g)

    print("capabilities")
    p, size, g = prep("image53.png", "capabilities-hero.jpg", PHOTOS, cap=1000)
    log("image53.png", "capabilities-hero.jpg", size, p, g)
    p, size, g = prep("image56.png", "capabilities-engineering.jpg", PHOTOS, cap=900)
    log("image56.png", "capabilities-engineering.jpg", size, p, g)

    print("resources gallery (slide 33)")
    gallery = [
        ("image65.jpeg", "works-gallery-1.jpg"),
        ("image64.jpeg", "works-gallery-2.jpg"),
        ("image68.jpeg", "works-gallery-3.jpg"),
        ("image67.jpeg", "works-gallery-4.jpg"),
        ("image66.jpeg", "works-gallery-5.jpg"),
        ("image69.jpeg", "works-gallery-6.jpg"),
    ]
    for src, out in gallery:
        p, size, g = photo_room(load(src), out, PHOTOS, cap=1200)
        log(src, out, size, p, g)

    # Resources hero: product range collage already on capabilities; reuse a
    # works floor frame that is not the CCTV chrome shot.
    p, size, g = photo_room(load("image65.jpeg"), "resources-hero.jpg", PHOTOS, cap=1200)
    log("image65.jpeg", "resources-hero.jpg", size, p, g)

    # Contact: premises signage. Prefer the existing building collage if the
    # slide-33 signboard is weaker; still publish the client's frame.
    p, size, g = photo_room(load("image69.jpeg"), "contact-frontage.jpg", PHOTOS, cap=1200)
    log("image69.jpeg", "contact-frontage.jpg", size, p, g)

    with open(META, "w", encoding="utf-8") as fh:
        json.dump(dict(sorted(_meta.items())), fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("\n%s  %d entries" % (os.path.relpath(META, ROOT), len(_meta)))


if __name__ == "__main__":
    main()
