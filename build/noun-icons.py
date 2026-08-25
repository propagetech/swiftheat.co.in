#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch the chosen Noun Project icons and prepare them for the site.

    python3 build/noun-icons.py

House workflow (skills/site-rebuild/reference-noun-icons.md): CC BY or public
domain only, download the clean PNG, vectorise with potrace, crop the viewBox to
the artwork, recolour to a brand token, and carry the attribution.

Every icon here is decorative. They are marked aria-hidden and no information
depends on them, so a blocked image costs nothing.
"""
import os
import subprocess
import sys
import urllib.request

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "icons")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
FILL = "#a1340c"          # --heat-700, hsl(16 86% 34%)

# slot -> (noun id, slug, creator, licence)
ICONS = [
    ("custom-design",   8436969, "technical-drawing", "Ali Nur Rohman", "CC BY 3.0"),
    ("reverse-engineer", 8419059, "caliper", "Muhammad Nur Auliady Pamungkas", "CC BY 3.0"),
    ("prototype",       8201949, "prototype", "diyah farida", "CC BY 3.0"),
    ("small-batch",     8142643, "box-stack", "Suharsono", "CC BY 3.0"),
    ("resistance",      8419064, "multimeter", "Muhammad Nur Auliady Pamungkas", "CC BY 3.0"),
    ("high-voltage",    8368320, "high-voltage", "Uswa KDT", "CC BY 3.0"),
    ("insulation",      5848062, "insulation", "Andi Nur Abdillah", "CC BY 3.0"),
    ("dimensional",     8419029, "micrometer", "Muhammad Nur Auliady Pamungkas", "CC BY 3.0"),
]


def fetch(nid):
    for url in ("https://static.thenounproject.com/png/%d-512.png" % nid,
                "https://static.thenounproject.com/png/%d-200.png" % nid):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}),
                                          timeout=30).read()
        except Exception:
            continue
    raise RuntimeError("could not fetch icon %d" % nid)


def vectorise(png_bytes, tmp):
    """Alpha channel to a bitmap, cropped to the artwork, then potrace to SVG.

    Cropping before tracing is what tightens the viewBox: potrace sizes its
    output from the bitmap, so a bitmap with no transparent margin produces an
    SVG with no empty margin."""
    raw = os.path.join(tmp, "in.png")
    open(raw, "wb").write(png_bytes)
    im = Image.open(raw).convert("RGBA")
    # The artwork is dark on transparent. Anything with alpha is ink.
    mask = im.split()[3].point(lambda a: 255 if a > 40 else 0).convert("L")
    box = mask.getbbox()
    if box:
        mask = mask.crop(box)
    # potrace traces black on white, so invert.
    mask = mask.point(lambda v: 0 if v else 255).convert("1")
    pbm = os.path.join(tmp, "in.pbm")
    mask.save(pbm)
    svg = os.path.join(tmp, "out.svg")
    subprocess.run(["potrace", "-s", "-o", svg, "-a", "1.0", "-O", "0.2", "--flat", pbm], check=True)
    return open(svg, encoding="utf-8").read()


def clean(svg, title):
    """potrace writes a full document with its own metadata and a transform on a
    group. Keep the geometry and the coordinate system, drop the rest."""
    import re
    vb = re.search(r'viewBox="([^"]+)"', svg)
    g = re.search(r"(<g[^>]*>)(.*?)</g>", svg, re.S)
    if not (vb and g):
        raise RuntimeError("unexpected potrace output")
    body = g.group(2).strip()
    body = re.sub(r'\sfill="[^"]*"', "", body)
    body = re.sub(r'\sstroke="[^"]*"', "", body)
    x, y, w, h = [float(v) for v in vb.group(1).split()]
    transform = re.search(r'transform="([^"]+)"', g.group(1))
    tr = ' transform="%s"' % transform.group(1) if transform else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %g %g" fill="%s" '
            'role="img" aria-label="%s">\n<g%s>%s</g>\n</svg>\n'
            % (w, h, FILL, title, tr, body))


def main():
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(OUT, ".tmp")
    os.makedirs(tmp, exist_ok=True)
    credits = []
    for slot, nid, slug, creator, lic in ICONS:
        svg = clean(vectorise(fetch(nid), tmp), slug.replace("-", " "))
        path = os.path.join(OUT, "noun-%s-%d.svg" % (slug, nid))
        open(path, "w", encoding="utf-8").write(svg)
        credits.append((slot, slug, nid, creator, lic))
        print("%-18s %-22s %6d bytes  %s" % (slot, os.path.basename(path), len(svg), creator))
    with open(os.path.join(OUT, "CREDITS.md"), "w", encoding="utf-8") as fh:
        fh.write("# Icon credits\n\nConcept icons from the Noun Project, used under the licence "
                 "shown. Each one is traced from the published PNG, cropped to the artwork and "
                 "recoloured to the brand accent. Regenerate with `python3 build/noun-icons.py`.\n\n"
                 "| Slot | Icon | Creator | Licence | File |\n| --- | --- | --- | --- | --- |\n")
        for slot, slug, nid, creator, lic in credits:
            fh.write("| %s | %s | %s | %s | `icons/noun-%s-%d.svg` |\n"
                     % (slot, slug.replace("-", " "), creator, lic, slug, nid))
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
    print("wrote icons/CREDITS.md")


if __name__ == "__main__":
    sys.exit(main())
