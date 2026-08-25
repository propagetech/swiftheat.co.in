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
from .chrome import (art, cards, crumbs, enquiry, esc, flow, flow_legend, page,
                     product_cards, rel, tscale)
from .data import COMPANY, FAMILIES, FAMILY_BY_SLUG, FORMS, INDUSTRIES, INDUSTRY_BY_SLUG, TBD


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


def _options(f):
    out = []
    for n, (title, opts) in enumerate(f["options"], 1):
        li = []
        for code, name, why, rating in opts:
            rate = ""
            if rating == TBD:
                rate = '<span class="rating">Temperature rating to confirm</span>'
            elif rating:
                rate = '<span class="rating">Rated to %s</span>' % esc(rating)
            li.append('<li><span class="code">%s</span><h4>%s</h4><p>%s</p>%s</li>'
                      % (esc(code), esc(name), esc(why), rate))
        out.append('<div class="optgroup"><h3><span class="idx">%02d</span> %s</h3>'
                   '<ul class="opts">%s</ul></div>' % (n, esc(title), "".join(li)))
    return "".join(out)


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
    prod = "".join("<option>%s</option>" % esc(FAMILY_BY_SLUG[s]["name"]) for s in ind["products"])
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
            ("applications", "Applications"), ("downloads", "Downloads"), ("enquiry", "Request a quote")]

    sel = "".join("<h3>%s</h3><p>%s</p>" % (esc(t), esc(b)) for t, b in f["selection"])
    fails = cards(depth, [("#enquiry", t, b) for t, b in f["failures"]])
    apps = cards(depth, [("applications/%s/" % s, INDUSTRY_BY_SLUG[s]["name"], INDUSTRY_BY_SLUG[s]["lede"])
                         for s in f["industries"]])
    rel_products = product_cards(depth, f["related"])
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
      <figure class="drawing">
        %(art)s
        <figcaption>The same drawing the list builder produces. Every number on it is a box you
          fill in, and every option you choose changes the picture.</figcaption>
      </figure>
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
    <div class="shot">
      <span class="label">Photograph required</span>
      <p>%(name)s, three quarter view on white, macro. Minimum 2000 px wide. One of a set of four
        for this family.</p>
    </div>
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
        <figcaption>Numbered callouts match the numbered boxes in the
          <a href="%(builder)s">list builder</a>. Not to scale.</figcaption>
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
  </div>
</section>

<section class="band" id="selection">
  <div class="wrap two">
    <div>
      <h2>Choosing the right heater</h2>
      %(selection)s
    </div>
    <div class="shot shot-sm">
      <span class="label">Photograph required</span>
      <p>%(name)s installed on a customer machine. One application shot per family.</p>
    </div>
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

<section class="band alt" id="downloads">
  <div class="wrap two">
    <div>
      <h2>Downloads</h2>
      <p>Free, and never behind a form. A buyer should be able to forward a datasheet to their
        purchase department in one click without giving up an email address first.</p>
      <ul class="dl">
        <li><span aria-disabled="true"><span>%(name)s datasheet</span><span class="meta">PDF, to be produced</span></span></li>
        <li><span aria-disabled="true"><span>Dimensional drawing</span><span class="meta">PDF, to be produced</span></span></li>
        <li><span aria-disabled="true"><span>Installation and removal guide</span><span class="meta">PDF, to be produced</span></span></li>
        <li><span aria-disabled="true"><span>Printable order form</span><span class="meta">PDF, to be produced</span></span></li>
      </ul>
      <p>Until the PDFs exist, the <a href="%(builder)s">list builder</a> generates a printable
        requirement document from whatever you specify.</p>
    </div>
    <div>
      <h2>Related products</h2>
      %(related)s
    </div>
  </div>
</section>

%(enquiry)s
""" % {
        "name": esc(f["name"]),
        "lede": esc(f["lede"]),
        "chips": _chips(f["chips"]),
        "builder": rel(depth, "build-a-list/"),
        "art": art(f["art"], "Drawing of a %s, with the principal dimensions called out" % f["name"].lower()),
        "art2": art(f["art"], "Dimensioned drawing of a %s" % f["name"].lower()),
        "construction": "".join("<p>%s</p>" % esc(p) for p in f["construction"]),
        "tscale": tscale(lo, hi),
        "spec": _spec_table(f),
        "dims": _dim_table(f),
        "dimkeys": esc(f["dim_keys"]),
        "options": _options(f),
        "optnote": esc(f["options_note"]),
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
        rows.append('<tr><th scope="row">%s</th><td>%s</td><td>%s</td>'
                    '<td><a href="%s">%s</a></td><td>%s</td></tr>'
                    % (esc(name), esc(duty), esc(temp), rel(depth, "products/%s/" % prodslug),
                       esc(p["name"]), esc(why)))
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
  <div class="wrap grid">
    <div>
      <p class="eyebrow">Industry</p>
      <h1>%(name)s</h1>
      <p class="lede">%(lede)s</p>
      <p>%(problem)s</p>
      <div class="actions">
        <a class="btn" href="#zones">See the zone by zone table</a>
        <a class="btn btn-onink" href="#enquiry">Request a quote</a>
      </div>
    </div>
    <div class="shot">
      <span class="label">Photograph required</span>
      <p>A real %(lname)s machine in a customer plant, with Swiftheat elements fitted. Landscape,
        minimum 2400 px wide.</p>
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
  <div class="wrap two">
    <div>
      <h2>Application notes</h2>
      %(notes)s
    </div>
    <div class="shot shot-sm">
      <span class="label">Photograph required</span>
      <p>Close up of a heated zone on a %(lname)s machine: barrel, tool face or sealing station.</p>
    </div>
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
        "products": product_cards(depth, ind["products"]).replace(' id="productList"', ""),
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
