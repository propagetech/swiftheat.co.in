# -*- coding: utf-8 -*-
"""Turns the data into the two page types that carry the site: the product
family page and the industry page.

The product family page follows the blueprint synthesised in the international
benchmark: breadcrumb, hero with headline specification chips, an action bar
above the fold, construction and why it matters, technical data, dimensions, a
coded and diagrammed option catalogue, selection guidance, failure modes,
applications, downloads, related products, and an enquiry already scoped to the
family.

The industry page carries the thing no site in that benchmark set has: a process
diagram with the heated zones called out, and a zone by zone table mapping the
machine to the element type.
"""
from . import imgmeta
from .chrome import (art, cards, crumbs, enquiry, esc, flow, flow_legend, page,
                     product_cards, rel, tscale)
from .data import (COMPANY, FAMILY_BY_SLUG, FAMILY_PHOTOS, FORMS, INDUSTRIES,
                   INDUSTRY_BY_SLUG, TBD)


def _photo(slug, key):
    return FAMILY_PHOTOS.get(slug, {}).get(key)


def _img_rel(name):
    """A file under imgs/."""
    return name.rsplit("/", 1)[-1]


def _img(shot, depth, eager=False, extra_style=""):
    """A client photograph, never drawn larger than the pixels it has.

    Several of these arrive around 300 px and the panels they sit in are 750 px
    wide, so left to fill their box they are drawn at two and a half times their
    own resolution and read as blurred. The cap only bites on the small ones:
    the band hero is a thousand pixels wide and fills its panel either way.

    min() and not a bare pixel cap. The inline style wins over the stylesheet,
    so a bare cap also cancels the max-width:100% the panels rely on, and a
    picture wider than its panel then runs out past the edge and is clipped by
    it. The cutaways are a thousand pixels wide and the two column panel they
    sit in is not, so this is the difference between a whole cutaway and a
    cropped one.
    """
    f, w, h, alt = shot[:4]
    style = "max-width:min(100%%,%dpx)" % w
    if extra_style:
        style += ";" + extra_style
    return ('<img src="%s" width="%d" height="%d" style="%s" loading="%s"\n'
            '        alt="%s">'
            % (rel(depth, "imgs/" + _img_rel(f)), w, h, style,
               "eager" if eager else "lazy", esc(alt)))


def _bg(shot, pad=False):
    """Repaint the panel behind a photograph to the ground it was shot on."""
    return imgmeta.bg(_img_rel(shot[0]), pad=pad)


def _after_options(slug, depth):
    """Extra product shots pasted onto the options block in web 2.pptx."""
    shots = FAMILY_PHOTOS.get(slug, {}).get("after_options") or []
    if not shots:
        return ""
    grid, rest = [], []
    for shot in shots:
        is_full = len(shot) > 4 and shot[4] == "full"
        extra = "max-height:none;width:100%" if is_full else ""
        block = _lightbox_shot(shot, depth, "shot", extra_style=extra)
        (rest if is_full else grid).append(block)
    html = ""
    if grid:
        html += '<div class="two">\n      %s\n    </div>\n    ' % "\n      ".join(grid)
    html += "\n    ".join(rest)
    return html


def _hero_figure(f, slug, depth):
    """A photograph of the family where the client supplied one, otherwise the
    drawing. The dimensioned drawing still appears further down the page in the
    Dimensions section, so nothing is lost by giving the hero to a photograph."""
    shot = _photo(slug, "hero")
    if shot:
        href = rel(depth, "imgs/" + _img_rel(shot[0]))
        return ('<figure class="drawing figure-photo" data-gallery="%s"%s>\n'
                '        <a href="%s">\n        %s\n        </a>\n'
                '        <figcaption>%s, made to order in Peenya. Every dimension and option on '
                'this page is one you choose. Click the photograph to enlarge.</figcaption>\n'
                '      </figure>'
                % (esc(f["name"]), _bg(shot), href, _img(shot, depth, eager=True),
                   esc(f["name"])))
    # The explanatory caption was marked "Not required" by the client on web 2.pptx
    # slides 2 and 15. The drawing stays; only the sentence under it goes.
    return ('<figure class="drawing">\n        %s\n      </figure>' % art(
                f["art"], "Drawing of a %s, with the principal dimensions called out"
                % f["name"].lower()))


def _shot(slug, key, depth, classes, placeholder):
    shot = _photo(slug, key)
    if not shot:
        return ('<div class="%s">\n      <span class="label">Photograph required</span>\n'
                '      <p>%s</p>\n    </div>' % (classes, placeholder))
    # contain, not cover: these are parts on a knocked out ground, and cropping
    # one to fill a box cuts the ends off the product.
    #
    # The panel keeps its 24 px padding. These grounds are a single measured
    # colour, so the panel is painted the same colour as the picture and the
    # padding does not read as a band around it: it reads as breathing room
    # between the part and the panel edge, which is what a cutaway running to
    # the border was missing. Only the products montage closes the padding up,
    # because its ground is a gradient no flat colour can match.
    return ('<div class="%s filled shot-part"%s>\n      %s\n    </div>'
            % (classes, _bg(shot), _img(shot, depth)))


def _lightbox_shot(shot, depth, classes, extra_style=""):
    """A single photograph that still opens the gallery dialog on click.

    Without JavaScript the wrapping link opens the picture. With it, the same
    dialog as the collage, minus the previous and next controls.
    """
    href = rel(depth, "imgs/" + _img_rel(shot[0]))
    return ('<div class="%s filled shot-part" data-gallery%s>\n'
            '      <a href="%s">\n        %s\n      </a>\n    </div>'
            % (classes, _bg(shot), href, _img(shot, depth, extra_style=extra_style)))


def _collage_item(shot, depth, extra_class=""):
    href = rel(depth, "imgs/" + _img_rel(shot[0]))
    cls = "collage-item" + ((" " + extra_class) if extra_class else "")
    return ('<a class="%s"%s href="%s">\n        %s\n      </a>'
            % (cls, _bg(shot), href, _img(shot, depth)))


def _collage(primary, extras, depth):
    """Clickable tiles. Without JavaScript each is still a link to the picture.
    With it, they open one gallery that slides left and right.

    Two photographs stack at lead size so neither is a leftover half-cell.
    A wide tile is for a form sheet that has to stay readable.
    """
    items = [_collage_item(primary, depth, "collage-lead")]
    lone_extra = len(extras) == 1
    for shot in extras:
        if len(shot) > 4 and shot[4] == "wide":
            extra_class = "collage-wide"
        elif lone_extra:
            extra_class = "collage-lead"
        else:
            extra_class = ""
        items.append(_collage_item(shot, depth, extra_class))
    return ('<figure class="collage" data-gallery>\n      %s\n'
            '      <figcaption>Click a photograph to enlarge.</figcaption>\n'
            '    </figure>' % "\n      ".join(items))


def _selshot(slug, depth, placeholder):
    """Selection photograph. Extra forms become a collage; a single shot still
    opens the gallery so a labelled chart can be read at full size."""
    extras = FAMILY_PHOTOS.get(slug, {}).get("gallery") or []
    primary = _photo(slug, "selection")
    if extras and primary:
        return _collage(primary, extras, depth)
    if primary:
        return _lightbox_shot(primary, depth, "shot shot-sm")
    return _shot(slug, "selection", depth, "shot shot-sm", placeholder)


def _conshot(slug, depth, placeholder):
    """Construction photograph, or a clickable collage when extra forms exist.

    A single shot still opens the gallery so labelled cutaways can be read at
    full size.
    """
    extras = FAMILY_PHOTOS.get(slug, {}).get("construction_gallery") or []
    primary = _photo(slug, "construction")
    if extras and primary:
        return _collage(primary, extras, depth)
    if primary:
        return _lightbox_shot(primary, depth, "shot")
    return _shot(slug, "construction", depth, "shot", placeholder)


def _selection_table(table):
    head = "".join('<th scope="col">%s</th>' % esc(c) for c in table["cols"])
    rows = []
    for row in table["rows"]:
        cells = "".join("<td>%s</td>" % esc(c) for c in row[1:])
        rows.append('<tr><th scope="row">%s</th>%s</tr>' % (esc(row[0]), cells))
    return ('<div class="tablewrap" style="margin-top:32px"><table>\n'
            '<caption>%s</caption>\n'
            '<thead><tr>%s</tr></thead>\n<tbody>%s</tbody>\n</table></div>'
            % (esc(table["caption"]), head, "".join(rows)))


def _val(v):
    return '<span class="tbd">%s</span>' % esc(v) if v == TBD else esc(v)


def _chips(chips):
    li = "".join('<li><b%s>%s</b><span>%s</span></li>'
                 % (' class="tbd"' if t else "", esc(v), esc(l)) for v, l, t in chips)
    return '<ul class="chips">%s</ul>' % li


def _spec_table(f):
    head = "".join('<th scope="col">%s</th>' % esc(c) for c in f["spec_cols"])
    rows = []
    for row in f["spec_rows"]:
        cells = "".join("<td>%s</td>" % _val(c) for c in row[1:])
        rows.append('<tr><th scope="row">%s</th>%s</tr>' % (esc(row[0]), cells))
    return ('<div class="tablewrap"><table>\n<caption>%s, published specification</caption>\n'
            '<thead><tr>%s</tr></thead>\n<tbody>%s</tbody>\n</table></div>'
            % (esc(f["name"]), head, "".join(rows)))


def _dim_table(f):
    head = "".join('<th scope="col">%s</th>' % esc(c) for c in f["dim_cols"])
    rows = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % _val(c) for c in row) for row in f["dim_rows"])
    return ('<div class="tablewrap"><table>\n<caption>%s</caption>\n<thead><tr>%s</tr></thead>\n'
            '<tbody>%s</tbody>\n</table></div>' % (esc(f["dim_caption"]), head, rows))


def _options(f, depth=2):
    out = []
    has_photos = False
    for n, (title, opts) in enumerate(f["options"], 1):
        li = []
        # Only some options have a photograph. Where any in the group does, the
        # rest reserve the same slot, so the code badge and the option name sit
        # on one line across the row instead of stepping up and down.
        any_shot = any(len(o) > 4 and o[4] for o in opts)
        if any_shot:
            has_photos = True
        for opt in opts:
            code, name, why, rating = opt[:4]
            img = opt[4] if len(opt) > 4 else None
            rate = ""
            if rating == TBD:
                rate = '<span class="rating">Temperature rating to confirm</span>'
            elif rating:
                rate = '<span class="rating">Rated to %s</span>' % esc(rating)
            # Empty alt: the card names the option in the heading below. The
            # link caption is what the gallery dialog reads aloud.
            if img:
                w, h = imgmeta.size(img) or (0, 0)
                href = rel(depth, "imgs/" + img)
                caption = "%s. %s" % (code, name)
                shot = ('<a class="optshot" href="%s"%s data-caption="%s" '
                        'aria-label="Enlarge: %s"><img src="%s" width="%d" '
                        'height="%d" alt="" loading="lazy"></a>'
                        % (href, imgmeta.bg(img), esc(caption), esc(caption),
                           href, w, h))
            elif any_shot:
                shot = '<span class="optshot"></span>'
            else:
                shot = ""
            li.append('<li><span class="code">%s</span>%s<h4>%s</h4><p>%s</p>%s</li>'
                      % (esc(code), shot, esc(name), esc(why), rate))
        gallery = ' data-gallery="%s"' % esc(title) if any_shot else ""
        out.append('<div class="optgroup"%s><h3><span class="idx">%02d</span> %s</h3>'
                   '<ul class="opts">%s</ul></div>' % (gallery, n, esc(title), "".join(li)))
    hint = ('<p class="cap">Click a photograph to enlarge.</p>\n    '
            if has_photos else "")
    return hint + "".join(out)


def _form_fields(slug):
    fields = []
    for fid, label, kind, extra in FORMS[slug]:
        if kind == "select":
            opts = '<option value="">Choose one</option>' + "".join(
                "<option>%s</option>" % esc(o) for o in extra)
            control = '<select id="q_%s" name="%s">%s</select>' % (fid, esc(label), opts)
            hint = ""
        elif kind == "number":
            lo, hi, unit = extra
            control = ('<input id="q_%s" name="%s" type="number" min="%s" max="%s" placeholder="%s">'
                       % (fid, esc(label), lo, hi, esc(unit)))
            hint = '<span class="hint">%s to %s %s</span>' % (lo, hi, esc(unit))
        else:
            control = ('<input id="q_%s" name="%s" type="text" placeholder="%s">'
                       % (fid, esc(label), esc(extra)))
            hint = ""
        fields.append('<div class="field"><label for="q_%s">%s</label>%s%s</div>'
                      % (fid, esc(label), control, hint))
    return ("""        <fieldset>
          <legend><span class="idx">02</span> Specification</legend>
          <div class="fields">%s</div>
        </fieldset>
""" % "".join(fields))


def _industry_fields(slug):
    ind = INDUSTRY_BY_SLUG[slug]
    names = []
    seen = set()
    for s in ind["products"]:
        p = FAMILY_BY_SLUG[s]
        target = p.get("redirect") or s
        if target in seen:
            continue
        seen.add(target)
        names.append(FAMILY_BY_SLUG[target]["name"])
    prod = "".join("<option>%s</option>" % esc(n) for n in names)
    checks = "".join("<option>%s</option>" % esc(c) for c in [])
    return """        <fieldset>
          <legend><span class="idx">02</span> The application</legend>
          <div class="fields">
            <div class="field">
              <label for="q_prod">Product family</label>
              <select id="q_prod" name="Product family">
                <option value="">Not sure, please advise</option>%(prod)s
              </select>
            </div>
            <div class="field">
              <label for="q_machine">Machine or equipment</label>
              <input id="q_machine" name="Machine" type="text" placeholder="make, model and size">
            </div>
            <div class="field">
              <label for="q_zone">Which zone</label>
              <input id="q_zone" name="Zone" type="text" placeholder="from the table above">
            </div>
            <div class="field">
              <label for="q_temp">Operating temperature</label>
              <input id="q_temp" name="Operating temperature" type="text" placeholder="degrees C">
            </div>
            <div class="field">
              <label for="q_volt">Voltage</label>
              <select id="q_volt" name="Voltage"><option value="">Choose one</option>
                <option>110 V</option><option>230 V</option><option>240 V</option><option>415 V</option></select>
            </div>
            <div class="field">
              <label for="q_duty">Duty conditions</label>
              <select id="q_duty" name="Duty conditions"><option value="">Choose one</option>
                <option>Continuous</option><option>Cyclic</option><option>Moisture or washdown</option>
                <option>Oil or plastic contamination</option><option>Vibration</option>
                <option>Food contact</option></select>
            </div>
            <div class="field field-wide">
              <label for="q_sizes">Sizes you already know</label>
              <input id="q_sizes" name="Sizes" type="text"
                placeholder="diameters, lengths, widths, wattage, whatever you have">
            </div>
          </div>
        </fieldset>
%(unused)s""" % {"prod": prod, "unused": checks}


# ---------------------------------------------------------------- product page

def product_page(f):
    depth = 2
    slug = f["slug"]
    lo, hi = f["temps"]
    jump = [("construction", "Construction"), ("data", "Technical data"), ("dimensions", "Dimensions"),
            ("options", "Options"), ("selection", "Selection guide"), ("failure", "Failure modes"),
            ("applications", "Applications"), ("enquiry", "Request a quote")]

    sel = "".join("<h3>%s</h3><p>%s</p>" % (esc(t), esc(b)) for t, b in f["selection"])
    fails = cards(depth, [("#enquiry", t, b) for t, b in f["failures"]])
    apps = cards(depth, [("applications/%s/" % s, INDUSTRY_BY_SLUG[s]["name"], INDUSTRY_BY_SLUG[s]["lede"])
                         for s in f["industries"]])
    rel_products = product_cards(depth, [s for s in f["related"]
                                         if FAMILY_BY_SLUG[s].get("listed", True)])
    # Related products reuse the finder markup but must not carry its id twice.
    rel_products = rel_products.replace(' id="productList"', "")

    body = """
<section class="hero">
  <div class="wrap grid">
    <div>
      <p class="eyebrow">Product family</p>
      <h1>%(name)s</h1>
      <p class="lede">%(lede)s</p>
      %(chips)s
      <div class="actions">
        <a class="btn" href="%(builder)s">Configure and request a quote</a>
        <a class="btn btn-ghost" href="#enquiry">Send a specification</a>
      </div>
    </div>
    <div>
      %(herofig)s
    </div>
  </div>
</section>

<section class="band" id="construction">
  <div class="wrap two">
    <div>
      <h2>How it is built, and why that matters</h2>
      %(construction)s
      <h3>Where this family sits on temperature</h3>
      %(tscale)s
    </div>
    %(conshot)s
  </div>
</section>

<section class="band alt" id="data">
  <div class="wrap">
    <h2>Technical data</h2>
    <div class="note">
      <p><strong>Figures marked "to confirm" are not published yet.</strong> The structure of this
        table is settled; the numbers come from Swiftheat's engineers and nothing appears here until
        they are confirmed. Published tolerances are worth having: to a die and mould buyer, a stated
        diameter tolerance says more about process control than any badge.</p>
    </div>
    %(spec)s
  </div>
</section>

<section class="band" id="dimensions">
  <div class="wrap two">
    <div>
      <h2>Dimensions</h2>
      <p>Every dimension we need in order to quote, named the same way on the drawing, in the table
        and in the enquiry form. A buyer should never have to guess what we call something.</p>
      %(dims)s
      <p class="cap"><strong>Key.</strong> %(dimkeys)s</p>
    </div>
    <div>
      <figure class="drawing">
        %(art2)s
      </figure>
    </div>
  </div>
</section>

<section class="band alt" id="options">
  <div class="wrap">
    <h2>Options</h2>
    <p>Everything you can order, given a code, a description and a rating. No Indian heater
      manufacturer publishes this today. It is what turns a quotation phone call into a part
      number, and every code here is the code that appears on your requirement document.</p>
    %(options)s
    <p>%(optnote)s</p>
    %(afteropts)s
  </div>
</section>

<section class="band" id="selection">
  <div class="wrap">
    <div%(selwrap)s>
      <div>
        <h2>Choosing the right %(noun)s</h2>
        %(selection)s
      </div>
      %(selshot)s
    </div>
    %(seltable)s
  </div>
</section>

<section class="band alt" id="failure">
  <div class="wrap">
    <h2>Why these fail early</h2>
    <p>Telling a buyer how a product fails is the most credible thing a manufacturer can publish,
      and it is the fastest way to stop the same failure arriving twice.</p>
    %(failures)s
  </div>
</section>

<section class="band" id="applications">
  <div class="wrap">
    <h2>Where these are used</h2>
    <p>Each one links to the industry page, which shows the heating zones on the machine and the
      element type for each zone.</p>
    %(apps)s
  </div>
</section>

<section class="band alt" id="related">
  <div class="wrap">
    <h2>Related products</h2>
    %(related)s
  </div>
</section>

%(enquiry)s
""" % {
        "name": esc(f["name"]),
        # web 2.pptx slide 18: the client wrote "Sensor" over "Choosing the right
        # heater" on the sensors page. A thermocouple is not a heater.
        "noun": f.get("noun", "heater"),
        "lede": esc(f["lede"]),
        "chips": _chips(f["chips"]),
        "builder": rel(depth, "build-a-list/"),
        "herofig": _hero_figure(f, slug, depth),
        "conshot": _conshot(slug, depth,
                            "%s, three quarter view on white, macro. Minimum 2000 px wide. One of a "
                            "set of four\n        for this family." % esc(f["name"])),
        "selwrap": ' class="two"' if (not f.get("selection_table") or _photo(slug, "selection")) else "",
        "selshot": "" if f.get("selection_table") and not _photo(slug, "selection") else
                   _selshot(slug, depth,
                            "%s installed on a customer machine. One application shot per family."
                            % esc(f["name"])),
        "seltable": (_selection_table(f["selection_table"]) if f.get("selection_table") else ""),
        "art2": art(f["art"], "Dimensioned drawing of a %s" % f["name"].lower()),
        "construction": "".join("<p>%s</p>" % esc(p) for p in f["construction"]),
        "tscale": tscale(lo, hi,
                         note="The upper limit is Swiftheat's confirmed rating from the specification "
                              "table below. The lower end is indicative for this element type."),
        "spec": _spec_table(f),
        "dims": _dim_table(f),
        "dimkeys": esc(f["dim_keys"]),
        "options": _options(f, depth),
        "optnote": esc(f["options_note"]),
        "afteropts": _after_options(slug, depth),
        "selection": sel,
        "failures": fails,
        "apps": apps,
        "related": rel_products,
        "enquiry": enquiry(
            depth,
            "Request a quote for %s" % f["name"].lower(),
            "%s enquiry" % f["name"],
            "Fill in what you know and leave the rest. The whole specification arrives at the works "
            "as a single readable email, and anything you leave blank our engineers will propose.",
            extra_fields=_form_fields(slug),
            scope_note="This enquiry is already scoped to %s." % f["name"].lower()),
    }

    ld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": f["name"],
        "description": f["meta"],
        "category": "Industrial heating elements",
        "brand": {"@type": "Brand", "name": COMPANY["short"]},
        "manufacturer": {
            "@type": "Organization",
            "name": COMPANY["name"],
            "address": {
                "@type": "PostalAddress",
                "streetAddress": COMPANY["street"],
                "addressLocality": COMPANY["city"],
                "addressRegion": COMPANY["state"],
                "postalCode": COMPANY["pin"],
                "addressCountry": COMPANY["country"],
            },
        },
    }
    return page(
        "products/%s/index.html" % slug,
        "%s | %s" % (f["name"], COMPANY["name"]),
        f["meta"],
        body,
        active="products/",
        depth=depth,
        jsonld=ld,
        jump=jump,
        crumb=[("", "Home"), ("products/", "Products"), (None, f["name"])],
    )


# ---------------------------------------------------------------- industry page

def industry_page(ind):
    depth = 2
    slug = ind["slug"]
    jump = [("process", "The process"), ("zones", "Heating zones"), ("products", "Products"),
            ("notes", "Application notes"), ("send", "What to send us"), ("enquiry", "Request a quote")]

    rows = []
    for name, duty, temp, band, prodslug, why in ind["zones"]:
        p = FAMILY_BY_SLUG[prodslug]
        target = p.get("redirect") or prodslug
        shown = FAMILY_BY_SLUG[target]
        rows.append('<tr><th scope="row">%s</th><td>%s</td><td>%s</td>'
                    '<td><a href="%s">%s</a></td><td>%s</td></tr>'
                    % (esc(name), esc(duty), esc(temp), rel(depth, "products/%s/" % target),
                       esc(shown["name"]), esc(why)))
    zone_table = (
        '<div class="tablewrap"><table>\n'
        '<caption>Heating zones on a typical %s line, and the element type each one wants</caption>\n'
        '<thead><tr><th scope="col">Zone</th><th scope="col">Duty</th>'
        '<th scope="col">Typical temperature</th><th scope="col">Swiftheat product</th>'
        '<th scope="col">Why this element</th></tr></thead>\n<tbody>%s</tbody>\n</table></div>'
        % (esc(ind["name"].lower()), "".join(rows)))

    notes = "".join("<h3>%s</h3><p>%s</p>" % (esc(t), esc(b)) for t, b in ind["notes"])
    checks = "".join("<li>%s</li>" % esc(c) for c in ind["checklist"])

    body = """
<section class="hero hero-dark">
  <div class="wrap">
    <p class="eyebrow">Industry</p>
    <h1>%(name)s</h1>
    <p class="lede">%(lede)s</p>
    <p>%(problem)s</p>
    <div class="actions">
      <a class="btn" href="#zones">See the zone by zone table</a>
      <a class="btn btn-onink" href="#enquiry">Request a quote</a>
    </div>
  </div>
</section>

<section class="band" id="process">
  <div class="wrap">
    <h2>The process, and where the heat goes in</h2>
    <p>Read left to right. Each block is a place on the machine that has to be held at a
      temperature, coloured by how hot it runs.</p>
    <figure class="flow">
      %(flow)s
      <p class="hint">Scroll the diagram sideways to see every zone.</p>
      %(legend)s
      <figcaption>Typical process temperatures for %(lname)s, not Swiftheat ratings. Your machine
        and your material decide the real numbers.</figcaption>
    </figure>
  </div>
</section>

<section class="band alt" id="zones">
  <div class="wrap">
    <h2>Zone by zone</h2>
    <p>This table is the whole argument for the page. It maps the machine you already have to the
      element type that suits each position on it, and every product name links to the family page
      with the sizes, the options and the codes.</p>
    %(zones)s
    <p>Temperatures are typical for the process and are given as a starting point. Send us the
      zone temperatures your machine actually runs at and we will work back to a safe loading.</p>
  </div>
</section>

<section class="band" id="products">
  <div class="wrap">
    <h2>Products for %(lname)s</h2>
    <p>A shortlist, not the whole catalogue.</p>
    %(products)s
  </div>
</section>

<section class="band alt" id="notes">
  <div class="wrap">
    <h2>Application notes</h2>
    %(notes)s
  </div>
</section>

<section class="band" id="send">
  <div class="wrap two">
    <div>
      <h2>What to send us</h2>
      <p>An enquiry with these in it can be quoted the same day. An enquiry without them takes three
        phone calls first.</p>
      <ul class="check">%(checks)s</ul>
      <p>A photograph of the old element next to a tape measure is worth more than a paragraph of
        description, and a drawing is worth more than both.</p>
    </div>
    <div>
      <h2>Build the list instead</h2>
      <p>If you are replacing several elements at once, the list builder walks through each one,
        draws it as you specify it, and produces a single printable document you can send by email
        or on WhatsApp.</p>
      <p><a class="btn" href="%(builder)s">Open the list builder</a></p>
    </div>
  </div>
</section>

%(enquiry)s
""" % {
        "name": esc(ind["name"]),
        "lname": esc(ind["name"].lower()),
        "lede": esc(ind["lede"]),
        "problem": esc(ind["problem"]),
        "flow": flow(ind["zones"], "Process flow for %s showing each heated zone and its typical temperature"
                     % ind["name"].lower()),
        "legend": flow_legend(),
        "zones": zone_table,
        "products": product_cards(depth, [s for s in ind["products"]
                                          if FAMILY_BY_SLUG[s].get("listed", True)]).replace(' id="productList"', ""),
        "notes": notes,
        "checks": checks,
        "builder": rel(depth, "build-a-list/"),
        "enquiry": enquiry(
            depth,
            "Request a quote for %s" % ind["name"].lower(),
            "%s enquiry" % ind["name"],
            "Tell us the machine and the zone. If you are not sure which element type suits it, leave "
            "the product blank and our engineers will propose one.",
            extra_fields=_industry_fields(slug),
            scope_note="This enquiry is already scoped to %s." % ind["name"].lower()),
    }

    ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "%s heating" % ind["name"],
        "description": ind["meta"],
        "about": {"@type": "Thing", "name": ind["name"]},
        "publisher": {"@type": "Organization", "name": COMPANY["name"]},
    }
    return page(
        "applications/%s/index.html" % slug,
        "Heaters for %s | %s" % (ind["name"], COMPANY["name"]),
        ind["meta"],
        body,
        active="applications/",
        depth=depth,
        jsonld=ld,
        jump=jump,
        crumb=[("", "Home"), ("applications/", "Applications"), (None, ind["name"])],
    )


def redirect_page(f):
    """A static stand-in for a family that has been clubbed into another page."""
    target = f["redirect"]
    dest = FAMILY_BY_SLUG[target]
    depth = 2
    href = rel(depth, "products/%s/" % target)
    dest_url = COMPANY["origin"] + "/products/%s/" % target
    body = """
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">This page has moved</p>
    <h1>%(name)s are listed with %(dest)s</h1>
    <p class="lede">Ceramic and mica nozzle heaters use the same construction as band heaters, at
      nozzle proportions. They now live on one page.</p>
    <div class="actions">
      <a class="btn" href="%(href)s">Open %(dest)s</a>
    </div>
  </div>
</section>
""" % {"name": esc(f["name"]), "dest": esc(dest["name"]), "href": href}
    html = page(
        "products/%s/index.html" % f["slug"],
        "%s | %s" % (f["name"], COMPANY["name"]),
        dest["meta"],
        body,
        active="products/",
        depth=depth,
        crumb=[("", "Home"), ("products/", "Products"), (None, f["name"])],
    )
    html = html.replace(
        '<meta charset="utf-8">',
        '<meta charset="utf-8">\n<meta http-equiv="refresh" content="0;url=%s">' % href,
    )
    old_canon = COMPANY["origin"] + "/products/%s/" % f["slug"]
    html = html.replace(
        'rel="canonical" href="%s"' % old_canon,
        'rel="canonical" href="%s"' % dest_url,
    )
    html = html.replace(
        'property="og:url" content="%s"' % old_canon,
        'property="og:url" content="%s"' % dest_url,
    )
    return html

