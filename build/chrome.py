# -*- coding: utf-8 -*-
"""The page shell: head, chrome, footer, and the components more than one page needs.

Every URL written here is relative and depth aware, so the whole site can be
served from a subdirectory, from a file:// path or from the domain root without
a single link changing.
"""
import html
import os
import re

from .data import COMPANY, FAMILIES, INDUSTRIES, PREVIEW_NOINDEX, TBD

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "art")

NAV = [
    ("products/", "Products"),
    ("applications/", "Applications"),
    ("capabilities/", "Capabilities"),
    ("quality/", "Quality"),
    ("resources/", "Resources"),
    ("about/", "About"),
    ("contact/", "Contact"),
]
NAV_CTA = ("build-a-list/", "Build a list")


def esc(s):
    return html.escape(str(s), quote=False)


def rel(depth, target):
    """A link from a page `depth` directories below the root to a root relative target."""
    if target.startswith(("#", "mailto:", "tel:", "http")):
        return target
    prefix = "../" * depth
    if target == "":
        return prefix + "index.html" if depth else "index.html"
    return prefix + target


def art(name, label):
    """One of the drawings the list builder renders, saved out as static artwork.

    The builder writes an aria-label describing the configuration in front of the
    person using it. On a product page there is no configuration, so the label is
    replaced with one that describes the picture.
    """
    with open(os.path.join(ART, name + ".svg"), encoding="utf-8") as fh:
        svg = fh.read().strip()
    return re.sub(r'aria-label="[^"]*"', 'aria-label="%s"' % html.escape(label, quote=True), svg, count=1)


# ---------------------------------------------------------------- components

def tscale(lo, hi, note=None):
    """The one device that recurs across the whole site: where a family sits on
    a temperature scale. Axis is fixed at 0 to 1200 C so families compare."""
    top = 1200.0
    left = max(0.0, lo / top) * 100
    width = max(2.0, (hi - lo) / top * 100)
    cap = note or ("Indicative range for this element type, not a Swiftheat rating. "
                   "Confirmed figures replace this before publication.")
    return (
        '<div class="tscale">\n'
        '  <div class="track"><div class="span" style="left:%.1f%%;width:%.1f%%"></div></div>\n'
        '  <ul class="ticks"><li>0</li><li>300</li><li>600</li><li>900</li><li>1200 &deg;C</li></ul>\n'
        '  <p class="cap">%s</p>\n'
        '</div>\n' % (left, width, esc(cap))
    )


ZONE_FILL = ["hsl(215 55% 88%)", "hsl(45 90% 86%)", "hsl(28 92% 80%)", "hsl(10 78% 76%)"]
ZONE_EDGE = ["hsl(215 40% 52%)", "hsl(42 74% 44%)", "hsl(24 78% 46%)", "hsl(8 70% 44%)"]
ZONE_NAME = ["Coolest", "Warm", "Hot", "Hottest"]


def flow(zones, title):
    """Process flow diagram for an industry page: the machine as a row of heated
    zones, coloured by how hot the zone runs. This is the section every site in
    the international benchmark set is missing."""
    zones = [z for z in zones if z[2] != "-"]
    n = len(zones)
    boxw, gap, padx, pady, boxh = 152, 34, 16, 22, 104
    w = padx * 2 + n * boxw + (n - 1) * gap
    h = pady + boxh + 40
    parts, labels = [], []
    for i, (name, duty, temp, band, slug, why) in enumerate(zones):
        x = padx + i * (boxw + gap)
        parts.append(
            '<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="%s" stroke="%s" stroke-width="1.6"/>'
            % (x, pady, boxw, boxh, ZONE_FILL[band], ZONE_EDGE[band]))
        lines = _wrapfit(name, 20, 2)
        tspans = "".join('<tspan x="%d" dy="%d">%s</tspan>' % (x + 12, 0 if j == 0 else 16, esc(l))
                         for j, l in enumerate(lines))
        labels.append('<text y="%d" font-size="13" font-weight="600" fill="hsl(214 32%% 11%%)">%s</text>'
                      % (pady + 22, tspans))
        dl = _wrapfit(duty, 23, 1)[0].rstrip(",")
        labels.append('<text x="%d" y="%d" font-size="12.5" fill="hsl(214 14%% 40%%)">%s</text>'
                      % (x + 12, pady + 62, esc(dl)))
        labels.append('<text x="%d" y="%d" font-size="13" font-weight="600" fill="hsl(16 86%% 34%%)" '
                      'style="font-variant-numeric:tabular-nums">%s</text>'
                      % (x + 12, pady + 84, esc(temp)))
        labels.append('<text x="%d" y="%d" font-size="12.5" fill="hsl(214 12%% 46%%)" '
                      'letter-spacing="1.2">ZONE %02d</text>' % (x + 12, pady + boxh + 22, i + 1))
        if i < n - 1:
            ax = x + boxw + 6
            mid = pady + boxh / 2
            parts.append('<path d="M%d %dh%d M%d %dl-7 -5 M%d %dl-7 5" fill="none" '
                         'stroke="hsl(214 16%% 62%%)" stroke-width="1.6"/>'
                         % (ax, mid, gap - 12, ax + gap - 12, mid, ax + gap - 12, mid))
    return ('<div class="scroller">\n'
            '<svg viewBox="0 0 %d %d" style="min-width:%dpx" role="img" aria-label="%s" '
            'font-family="Inter, sans-serif">\n%s\n%s\n</svg>\n</div>'
            % (w, h, w, html.escape(title, quote=True), "\n".join(parts), "\n".join(labels)))


def _wrapfit(text, width, maxlines):
    """Greedy word wrap. SVG has no text flow, so the lines are worked out here
    and emitted as tspans, which keeps every label inside its box."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if len(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
        if len(lines) == maxlines:
            break
    if cur and len(lines) < maxlines:
        lines.append(cur)
    return lines or [text[:width]]


def flow_legend():
    items = "".join(
        '<li><span class="sw" style="background:%s;border-color:%s"></span>%s</li>' % (
            ZONE_FILL[i], ZONE_EDGE[i], ZONE_NAME[i]) for i in range(4))
    return '<ul class="legend">%s</ul>' % items


ICON_CREDITS = {
    "noun-technical-drawing-8436969.svg": "technical drawing by Ali Nur Rohman from Noun Project (CC BY 3.0)",
    "noun-caliper-8419059.svg": "caliper by Muhammad Nur Auliady Pamungkas from Noun Project (CC BY 3.0)",
    "noun-prototype-8201949.svg": "prototype by diyah farida from Noun Project (CC BY 3.0)",
    "noun-box-stack-8142643.svg": "box stack by Suharsono from Noun Project (CC BY 3.0)",
    "noun-multimeter-8419064.svg": "multimeter by Muhammad Nur Auliady Pamungkas from Noun Project (CC BY 3.0)",
    "noun-high-voltage-8368320.svg": "high voltage by Uswa KDT from Noun Project (CC BY 3.0)",
    "noun-insulation-5848062.svg": "insulation by Andi Nur Abdillah from Noun Project (CC BY 3.0)",
    "noun-micrometer-8419029.svg": "micrometer by Muhammad Nur Auliady Pamungkas from Noun Project (CC BY 3.0)",
}


def icon_cards(depth, items, numbered=False):
    """items: (icon file, title, body). The icon is decorative and the card
    reads identically without it. CC BY attribution rides on every image, and
    one consolidated comment goes at the end of the list."""
    li = []
    for n, (icon, title, body) in enumerate(items, 1):
        num = '<span class="n">%02d</span>' % n if numbered else ""
        li.append('<li>%s<img src="%s" width="44" height="44" alt="" title="%s">'
                  '<h3>%s</h3><p>%s</p></li>'
                  % (num, rel(depth, "icons/" + icon), html.escape(ICON_CREDITS[icon], quote=True),
                     esc(title), esc(body)))
    used = "\n".join("       " + ICON_CREDITS[i] for i, _, _ in items)
    return ('<ul class="iconcards">%s</ul>\n<!-- Concept icons, Noun Project:\n%s\n-->'
            % ("".join(li), used))


def cards(depth, items):
    """items: (href, title, blurb)"""
    li = "".join(
        '<li><a href="%s"><strong>%s</strong><span>%s</span></a></li>' % (
            rel(depth, h), esc(t), esc(b)) for h, t, b in items)
    return '<ul class="cards">%s</ul>' % li


def product_cards(depth, slugs, facets=False):
    from .data import FAMILY_BY_SLUG
    out = []
    for slug in slugs:
        f = FAMILY_BY_SLUG[slug]
        data_attrs = ""
        if facets:
            data_attrs = " ".join('data-%s="%s"' % (k, v) for k, v in sorted(f["facets"].items()))
            data_attrs = " " + data_attrs
        # A photograph of the family where the client has supplied one, the line
        # drawing where they have not. The card names the family in words
        # directly underneath either way, so the image is decorative.
        if f.get("card"):
            picture = ('<img src="%s" width="%d" height="%d" alt="" loading="lazy">'
                       % (rel(depth, "imgs/cards/" + f["card"][0]), f["card"][1], f["card"][2]))
            art_class = "art art-photo"
        else:
            picture = art(f["art"], "Drawing of a %s" % f["name"].lower())
            art_class = "art"
        out.append(
            '<li%s>\n  <a href="%s">\n    <span class="%s">%s</span>\n'
            '    <strong>%s</strong>\n    <span>%s</span>\n'
            '    <span class="meta">Part code %s</span>\n  </a>\n</li>'
            % (data_attrs, rel(depth, "products/%s/" % slug), art_class, picture,
               esc(f["name"]), esc(f["summary"]), esc(f["code"])))
    return '<ul class="pcards" id="productList">\n%s\n</ul>' % "\n".join(out)


def enquiry(depth, heading, subject, intro, extra_fields="", scope_note=""):
    """The scoped enquiry block. Specification first, identity last, exactly as
    the international benchmark said no leader does."""
    return """<section class="band rfq" id="enquiry">
  <div class="wrap">
    <h2>%(h2)s</h2>
    <p>%(intro)s</p>
    <form class="two" id="rfqForm" data-to="%(to)s" data-subject="%(subject)s" data-heading="%(heading)s">
      <div>
        <fieldset>
          <legend><span class="idx">01</span> What you need</legend>
          <div class="fields">
            <div class="field">
              <label for="etype">Enquiry type</label>
              <select id="etype" name="Enquiry type">
                <option value="">Choose one</option>
                <option>New design</option>
                <option>Replacement of an existing element</option>
                <option>Repeat order</option>
                <option>Technical advice</option>
              </select>
            </div>
            <div class="field">
              <label for="qty">Quantity</label>
              <input id="qty" name="Quantity" type="number" min="1" max="99999" placeholder="e.g. 24">
            </div>
            <div class="field">
              <label for="need">Required by</label>
              <input id="need" name="Required by" type="text" placeholder="e.g. 2 weeks">
            </div>
          </div>
        </fieldset>
%(extra)s
        <fieldset>
          <legend><span class="idx">%(n)s</span> Your details</legend>
          <div class="fields">
            <div class="field"><label for="cname">Name</label><input id="cname" name="Name" type="text" autocomplete="name"></div>
            <div class="field"><label for="ccomp">Company</label><input id="ccomp" name="Company" type="text" autocomplete="organization"></div>
            <div class="field"><label for="cmail">Email</label><input id="cmail" name="Email" type="email" autocomplete="email"></div>
            <div class="field"><label for="cphone">Phone or WhatsApp</label><input id="cphone" name="Phone" type="tel" autocomplete="tel"></div>
            <div class="field field-wide">
              <label for="q_notes">Anything else, and please attach your drawing to the email</label>
              <textarea id="q_notes" name="Notes" placeholder="Cutouts, special features, the part number you are replacing"></textarea>
            </div>
          </div>
        </fieldset>
      </div>
      <div>
        <div class="preview">
          <h3>The email Swiftheat receives</h3>
          <p class="cap">Updates as you type. Nothing is stored anywhere and there is no account to
            create. Attach your drawing in your own mail application before sending.</p>
          <pre id="mailPreview">Fill in the form and the enquiry appears here.</pre>
          <button class="btn" type="button" id="composeBtn">Open this in my email</button>
          <p class="cap" style="margin:16px 0 0">%(scope)s Or <a href="%(builder)s">build a list</a>
            if you need more than one item.</p>
        </div>
      </div>
    </form>
  </div>
</section>
""" % {
        "h2": esc(heading),
        "intro": intro,
        "to": COMPANY["email"],
        "subject": html.escape(subject, quote=True),
        "heading": html.escape(subject.upper(), quote=True),
        "extra": extra_fields,
        "n": "03" if extra_fields else "02",
        "scope": esc(scope_note),
        "builder": rel(depth, "build-a-list/"),
    }


# ---------------------------------------------------------------- the shell

def _nav(depth, active):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if active == href else ""
        out.append('<li><a href="%s"%s>%s</a></li>' % (rel(depth, href), cur, esc(label)))
    href, label = NAV_CTA
    cur = ' aria-current="page"' if active == href else ""
    out.append('<li class="cta"><a href="%s"%s>%s</a></li>' % (rel(depth, href), cur, esc(label)))
    return "\n        ".join(out)


def _footer(depth):
    prod = "".join('<li><a href="%s">%s</a></li>' % (rel(depth, "products/%s/" % f["slug"]), esc(f["name"]))
                   for f in FAMILIES)
    ind = "".join('<li><a href="%s">%s</a></li>' % (rel(depth, "applications/%s/" % i["slug"]), esc(i["name"]))
                  for i in INDUSTRIES[:6])
    comp = "".join('<li><a href="%s">%s</a></li>' % (rel(depth, h), esc(t)) for h, t in [
        ("about/", "About Swiftheat"),
        ("capabilities/", "Custom solutions and capabilities"),
        ("quality/", "Quality and testing"),
        ("resources/", "Resources and downloads"),
        ("build-a-list/", "Build a requirement list"),
        ("contact/", "Contact and get a quote"),
    ])
    return """<footer class="site">
  <div class="wrap">
    <div class="cols">
      <div>
        <h3>%(name)s</h3>
        <p>%(street)s,<br>%(area)s,<br>%(city)s %(pin)s</p>
        <p><a href="mailto:%(email)s">%(email)s</a><br>
          <span class="tbd">Phone number and registered address to be confirmed before publication.</span></p>
      </div>
      <div><h3>Products</h3><ul>%(prod)s</ul></div>
      <div><h3>Applications</h3><ul>%(ind)s<li><a href="%(allind)s">All industries</a></li></ul></div>
      <div><h3>Company</h3><ul>%(comp)s</ul></div>
    </div>
    <div class="legal">
      <p>&copy; 2026 %(name)s. Industrial heating elements made in Peenya, Bengaluru.</p>
      <p>Built as static files. No cookies, no tracking, no third party scripts.</p>
    </div>
  </div>
</footer>
""" % {
        "name": esc(COMPANY["name"]),
        "street": esc(COMPANY["street"]),
        "area": esc(COMPANY["area"]),
        "city": esc(COMPANY["city"]),
        "pin": esc(COMPANY["pin"]),
        "email": COMPANY["email"],
        "prod": prod, "ind": ind, "comp": comp,
        "allind": rel(depth, "applications/"),
    }


def crumbs(depth, trail):
    """trail: list of (href_or_None, label). The last item is the current page."""
    items = []
    for href, label in trail:
        if href is None:
            items.append("<li>%s</li>" % esc(label))
        else:
            items.append('<li><a href="%s">%s</a></li>' % (rel(depth, href), esc(label)))
    return ('<nav class="crumb" aria-label="Breadcrumb"><div class="wrap"><ol>%s</ol></div></nav>\n'
            % "".join(items))


def page(path, title, description, body, active="", depth=None, jsonld=None, jump=None, crumb=None,
         extra_css=None, extra_js=None):
    if depth is None:
        depth = len([p for p in path.split("/") if p and not p.endswith(".html")])
    canonical = COMPANY["origin"] + "/" + (path if path != "index.html" else "")
    canonical = canonical.replace("/index.html", "/")
    css = ['<link rel="stylesheet" href="%s">' % rel(depth, "css/site.css")]
    for c in (extra_css or []):
        css.append('<link rel="stylesheet" href="%s">' % rel(depth, c))
    scripts = ['<script src="%s"></script>' % rel(depth, "js/site.js")]
    for j in (extra_js or []):
        scripts.append('<script src="%s"></script>' % rel(depth, j))
    ld = ""
    if jsonld:
        import json
        ld = '<script type="application/ld+json">%s</script>\n' % json.dumps(jsonld, indent=None, ensure_ascii=False)
    jumpnav = ""
    if jump:
        links = "".join('<li><a href="#%s">%s</a></li>' % (a, esc(b)) for a, b in jump)
        jumpnav = ('<nav class="jump" aria-label="On this page"><div class="wrap"><ul>%s</ul></div></nav>\n'
                   % links)
    return """<!DOCTYPE html>
<html lang="en-IN" class="nojs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
%(robots)s<link rel="canonical" href="%(canonical)s">
<link rel="icon" href="%(icon)s" type="image/svg+xml">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:type" content="website">
<meta property="og:url" content="%(canonical)s">
<meta name="theme-color" content="#0d1620">
<link rel="preload" href="%(f1)s" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="%(f2)s" as="font" type="font/woff2" crossorigin>
%(css)s
%(ld)s</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<div class="topbar">
  <div class="wrap">
    <span class="where">%(area)s, %(city)s %(pin)s</span>
    <a href="%(builder)s">Build a list</a>
    <a href="%(resources)s">Downloads</a>
    <a href="mailto:%(email)s">%(email)s</a>
  </div>
</div>

<header class="masthead">
  <div class="wrap">
    <a class="logo" href="%(home)s"><img src="%(logo)s" alt="Swiftheat" width="2154" height="361"><small>Thermal Technologies</small></a>
    <button class="navtoggle" type="button" aria-expanded="false" aria-controls="mainnav">
      <svg width="18" height="14" viewBox="0 0 18 14" aria-hidden="true"><g stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 1h16M1 7h16M1 13h16"/></g></svg>
      Menu
    </button>
    <nav class="mainnav" id="mainnav" aria-label="Main">
      <ul>
        %(nav)s
      </ul>
    </nav>
  </div>
</header>
%(crumbs)s%(jump)s
<main id="main">
%(body)s
</main>

%(footer)s
%(scripts)s
</body>
</html>
""" % {
        "title": html.escape(title, quote=True),
        "desc": html.escape(description, quote=True),
        "canonical": canonical,
        "robots": ('<meta name="robots" content="noindex, nofollow">\n'
                   if PREVIEW_NOINDEX else ""),
        "icon": rel(depth, "favicon.svg"),
        "f1": rel(depth, "fonts/archivo-narrow-latin-700-normal.woff2"),
        "f2": rel(depth, "fonts/inter-latin-400-normal.woff2"),
        "css": "\n".join(css),
        "ld": ld,
        "area": esc(COMPANY["area"]),
        "city": esc(COMPANY["city"]),
        "pin": esc(COMPANY["pin"]),
        "email": COMPANY["email"],
        "builder": rel(depth, "build-a-list/"),
        "resources": rel(depth, "resources/"),
        "home": rel(depth, ""),
        "logo": rel(depth, "imgs/swiftheat-logo.svg"),
        "nav": _nav(depth, active),
        "crumbs": crumbs(depth, crumb) if crumb else "",
        "jump": jumpnav,
        "body": body,
        "footer": _footer(depth),
        "scripts": "\n".join(scripts),
    }
