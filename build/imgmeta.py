# -*- coding: utf-8 -*-
"""What build/prep-client-imgs.py measured off each client photograph.

The client asked for the borders off the pictures they supplied and the
backgrounds left alone, and where a background is not the colour of the panel
the site draws it on, for the panel to be repainted to match. So the panel
colour is not a design token here: it is a property of the photograph, measured
when the picture is prepared and carried through to the page.

imgs/client-imgs.json is generated. Run build/prep-client-imgs.py after touching
anything in it.
"""
import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, "..", "imgs", "client-imgs.json")

with open(META, encoding="utf-8") as _fh:
    IMGS = json.load(_fh)


def meta(rel):
    """rel is the path under imgs/, e.g. "cards/band-heaters.jpg"."""
    return IMGS.get(rel)


_SIZES = {}


def size(rel):
    """The picture's own pixel size, for the width and height attributes.

    Falls back to opening the file for anything this build did not prepare: the
    accessory photographs carried over from the old site are still referenced
    from the option catalogue, and they need intrinsic dimensions as much as the
    new ones do. Without them the option grid reserves no space and the row
    jumps as each thumbnail arrives.
    """
    m = IMGS.get(rel)
    if m:
        return m["w"], m["h"]
    if rel not in _SIZES:
        path = os.path.join(HERE, "..", "imgs", rel)
        with Image.open(path) as im:
            _SIZES[rel] = im.size
    return _SIZES[rel]


def bg(rel, pad=False):
    """The style attribute that repaints the panel behind the picture.

    Empty for a photograph drawn cover, which fills its box and leaves no panel
    showing. Never empty just because the ground came out white: white is the
    answer on the warm sunk panel the product cards use, and on the alt band
    where the card itself is --paper.

    pad=True also closes the panel's own padding up. A picture that keeps its
    background already carries an even margin of it, put there when the border
    was trimmed, so the panel's padding is a second margin drawn in a flat
    colour. On the products montage that is visible: its ground runs from blue
    at the top to purple at the bottom, no flat colour matches both ends, and
    the mismatch shows exactly where the padding is. With the padding closed the
    picture's own ground reaches the edge of the panel and there is nothing to
    match.
    """
    m = IMGS.get(rel)
    if not m or not m.get("ground"):
        return ""
    return ' style="--art-bg:%s%s"' % (m["ground"], ";--art-pad:0" if pad else "")
