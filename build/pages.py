# -*- coding: utf-8 -*-
"""The pages that are not one of the two repeating types."""
from .chrome import (art, cards, enquiry, esc, icon_cards, page, product_cards, rel, tscale, NAV)
from .data import COMPANY, FAMILIES, FAMILY_BY_SLUG, INDUSTRIES, INDUSTRY_BY_SLUG, TBD

ADDRESS = {
    "@type": "PostalAddress",
    "streetAddress": COMPANY["street"],
    "addressLocality": COMPANY["city"],
    "addressRegion": COMPANY["state"],
    "postalCode": COMPANY["pin"],
    "addressCountry": COMPANY["country"],
}

ORG = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": COMPANY["name"],
    "alternateName": COMPANY["short"],
    "url": COMPANY["origin"] + "/",
    "email": COMPANY["email"],
    "address": ADDRESS,
    "areaServed": "IN",
    "description": "Manufacturer of industrial heating elements in Peenya Industrial Area, "
                   "Bengaluru: cartridge, coil, band, nozzle, strip, tubular and ceramic infrared "
                   "heaters, and temperature sensors.",
}


def _general_fields():
    prod = "".join("<option>%s</option>" % esc(f["name"]) for f in FAMILIES)
    ind = "".join("<option>%s</option>" % esc(i["name"]) for i in INDUSTRIES)
    return """        <fieldset>
          <legend><span class="idx">02</span> What you are heating</legend>
          <div class="fields">
            <div class="field">
              <label for="q_prod">Product family</label>
              <select id="q_prod" name="Product family">
                <option value="">Not sure, please advise</option>%(prod)s
              </select>
            </div>
            <div class="field">
              <label for="q_ind">Industry</label>
              <select id="q_ind" name="Industry"><option value="">Choose one</option>%(ind)s</select>
            </div>
            <div class="field">
              <label for="q_machine">Machine or equipment</label>
              <input id="q_machine" name="Machine" type="text" placeholder="make, model and size">
            </div>
            <div class="field">
              <label for="q_heated">What is being heated</label>
              <select id="q_heated" name="What is being heated"><option value="">Choose one</option>
                <option>Metal block, platen or mould</option><option>Barrel or cylinder</option>
                <option>Nozzle or manifold</option><option>Air or gas</option>
                <option>Liquid</option><option>A radiant surface</option></select>
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
            <div class="field field-wide">
              <label for="q_sizes">Sizes you already know</label>
              <input id="q_sizes" name="Sizes" type="text"
                placeholder="diameters, lengths, widths, wattage, whatever you have">
            </div>
          </div>
        </fieldset>
""" % {"prod": prod, "ind": ind}


# ---------------------------------------------------------------- home

def home():
    depth = 0
    prods = product_cards(depth, [f["slug"] for f in FAMILIES]).replace(' id="productList"', "")
    inds = cards(depth, [("applications/%s/" % i["slug"], i["name"], i["lede"]) for i in INDUSTRIES])
    body = """
<section class="hero hero-dark">
  <div class="wrap grid">
    <div>
      <p class="eyebrow">Peenya Industrial Area, Bengaluru</p>
      <h1>Industrial heating elements, made to your drawing.</h1>
      <p class="lede">Cartridge, coil, band, nozzle, strip, tubular and ceramic infrared heaters, and
        the sensors that control them. Designed around the machine you already have, not picked from
        a shelf.</p>
      <div class="actions">
        <a class="btn" href="build-a-list/">Build a requirement list</a>
        <a class="btn btn-onink" href="#enquiry">Send a specification</a>
      </div>
      <ul class="chips">
        <li><b>8</b><span>Product families</span></li>
        <li><b>9</b><span>Industries served</span></li>
        <li><b>%(codes)d</b><span>Coded options published</span></li>
        <li><b>%(founded)s</b><span>Manufacturing since</span></li>
      </ul>
    </div>
    <div class="shot">
      <span class="label">Photograph required</span>
      <p>The Peenya works: winding, assembly or the test bench, with people in shot. Landscape,
        minimum 2400 px wide. This is the picture the whole home page rests on.</p>
    </div>
  </div>
</section>

<section class="band alt">
  <div class="wrap">
    <div class="sechead">
      <h2>What we make</h2>
      <p>Eight families. Every one of them is made to a size, a wattage and a set of options you
        choose, and every option carries a code that follows the part from enquiry to delivery.</p>
    </div>
    %(prods)s
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sechead">
      <h2>Which machine are you heating?</h2>
      <p>Each industry page carries a process diagram with the heated zones marked and a table that
        maps the machine, zone by zone, to the element type that suits it.</p>
    </div>
    %(inds)s
  </div>
</section>

<section class="band ink">
  <div class="wrap two">
    <div>
      <h2>An enquiry should arrive as a specification</h2>
      <p>A general contact form asks for a name, a phone number and a message. Ours asks for a
        heater: diameter, length, heated length, wattage, voltage, termination, lead protection,
        thermocouple, and the bore tolerance in your own part.</p>
      <p>That is the difference between a quotation that takes three phone calls and one that goes
        out the same day.</p>
      <div class="actions">
        <a class="btn" href="build-a-list/">Build a requirement list</a>
        <a class="btn btn-onink" href="contact/">Talk to an engineer</a>
      </div>
    </div>
    <div>
      <ol class="steps">
        <li><h3>Pick the family</h3><p>The sizes, the options and the drawing all change to suit
          it.</p></li>
        <li><h3>Set the sizes</h3><p>The drawing redraws as you type, so you can see the part you
          are asking for before you send it.</p></li>
        <li><h3>Send the document</h3><p>Print it, email it or send it on WhatsApp. Nothing is
          stored on a server and there is no account to create.</p></li>
      </ol>
    </div>
  </div>
</section>

<section class="band alt">
  <div class="wrap two">
    <div>
      <h2>Where each family sits on temperature</h2>
      <p>One scale, used the same way on every product page, so families can be compared at a
        glance rather than read one table at a time.</p>
      %(scales)s
      <p class="cap">Indicative ranges for each element type, not Swiftheat ratings. Confirmed
        figures replace these before publication.</p>
    </div>
    <div>
      <h2>Made here, not traded</h2>
      <p>Swiftheat manufactures in Peenya Industrial Area, which is the difference between an
        element built to your drawing and one bought in and relabelled. It is also why a prototype
        can be made and tested before a production quantity is committed.</p>
      %(madecards)s
    </div>
  </div>
</section>

%(enquiry)s
""" % {
        "founded": COMPANY["founded"],
        "madecards": icon_cards(0, [
            ("noun-technical-drawing-8436969.svg", "Custom design",
             "Built to your drawing, your bore and your fit."),
            ("noun-caliper-8419059.svg", "Reverse engineering",
             "Send the old element and we will match it."),
            ("noun-prototype-8201949.svg", "Prototypes",
             "One off, made and tested, before a batch is committed."),
            ("noun-multimeter-8419064.svg", "Tested before despatch",
             "Resistance, high voltage and dimensional checks."),
        ]),
        "codes": sum(len(o) for f in FAMILIES for _, o in f["options"]),
        "prods": prods,
        "inds": inds,
        "scales": "".join(
            '<h3 style="margin-bottom:8px"><a href="products/%s/">%s</a></h3>%s'
            % (f["slug"], esc(f["name"]), tscale(f["temps"][0], f["temps"][1], note=" "))
            for f in FAMILIES),
        "enquiry": enquiry(
            depth, "Tell us what you need heated", "Website enquiry",
            "If you know the specification, fill it in. If you do not, describe the machine and the "
            "temperature and our engineers will propose an element.",
            extra_fields=_general_fields(),
            scope_note="Every product page carries an enquiry already scoped to that family."),
    }
    ld = dict(ORG)
    return page("index.html", "%s | Industrial heating elements, Peenya, Bengaluru" % COMPANY["short"],
                "Swiftheat Thermal Technologies manufactures cartridge, coil, band, nozzle, strip, "
                "tubular and ceramic infrared heaters and temperature sensors in Peenya, Bengaluru. "
                "Built to your drawing.",
                body, active="", depth=0, jsonld=ld)


# ---------------------------------------------------------------- products index

def products_index():
    depth = 1
    body = """
<section class="hero">
  <div class="wrap grid">
    <div>
      <p class="eyebrow">Products</p>
      <h1>Eight families, every one made to order</h1>
      <p class="lede">Every family page carries the construction, the specification table, the
        dimensions, the full option catalogue with codes, the selection guidance and the failure
        modes. Nothing is held back for a phone call.</p>
      <div class="actions">
        <a class="btn" href="../build-a-list/">Build a requirement list</a>
        <a class="btn btn-ghost" href="../applications/">Browse by industry instead</a>
      </div>
    </div>
    <div class="shot">
      <span class="label">Photograph required</span>
      <p>The full range laid out together on a clean surface, shot from above. One picture that
        shows the breadth in a single frame.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <form class="finder" id="finder">
      <h2>Find the right family</h2>
      <p>Narrow the list by what you are heating, or by the industry you are in.</p>
      <div class="facets">
        <div>
          <label for="f_heats">What are you heating?</label>
          <select id="f_heats" data-facet="heats">
            <option value="">Anything</option>
            <option value="metal">Metal: a tool, a barrel or a platen</option>
            <option value="air">Air or gas</option>
            <option value="liquid">A liquid</option>
            <option value="radiant">A surface, radiantly</option>
            <option value="sensor">Nothing, I need to measure it</option>
          </select>
        </div>
        <div>
          <label for="f_industry">Which industry?</label>
          <select id="f_industry" data-facet="industry">
            <option value="">Any industry</option>
            %(indopts)s
          </select>
        </div>
        <div>
          <label for="f_form">How does it fit?</label>
          <select id="f_form" data-facet="form">
            <option value="">Any way</option>
            <option value="insert">Into a bore</option>
            <option value="wrap">Around a cylinder</option>
            <option value="surface">Onto a flat surface</option>
            <option value="immersion">Into air or liquid</option>
            <option value="radiant">Facing the work</option>
            <option value="sensor">It measures</option>
          </select>
        </div>
      </div>
      <p class="count" id="finderCount">Showing all %(n)d product families.</p>
      <p><button class="btn btn-ghost" type="button" id="finderReset">Clear the filters</button></p>
    </form>
    %(prods)s
  </div>
</section>

<section class="band alt">
  <div class="wrap two">
    <div>
      <h2>Not sure which one?</h2>
      <p>Describe the machine and the temperature and leave the product blank. Our engineers will
        propose an element type and tell you why, which is usually faster than working through the
        catalogue.</p>
      <p><a class="btn" href="../contact/">Ask an engineer</a></p>
    </div>
    <div>
      <h2>Ordering more than one</h2>
      <p>The list builder takes several different heaters in one pass, draws each one as you specify
        it, and produces a single document. Your own maintenance team can use it, and so can our
        sales desk while you are on the phone.</p>
      <p><a class="btn btn-ghost" href="../build-a-list/">Open the list builder</a></p>
    </div>
  </div>
</section>
""" % {
        "indopts": "".join('<option value="%s">%s</option>' % (i["slug"], esc(i["name"])) for i in INDUSTRIES),
        "n": len(FAMILIES),
        "prods": product_cards(depth, [f["slug"] for f in FAMILIES], facets=True),
    }
    ld = {"@context": "https://schema.org", "@type": "CollectionPage",
          "name": "Products", "description": "Eight families of industrial heating element.",
          "publisher": {"@type": "Organization", "name": COMPANY["name"]}}
    return page("products/index.html", "Products | %s" % COMPANY["name"],
                "Cartridge, coil, ceramic and mica band, nozzle, strip, tubular and ceramic infrared "
                "heaters and temperature sensors, made to order in Peenya, Bengaluru.",
                body, active="products/", depth=1, jsonld=ld,
                crumb=[("", "Home"), (None, "Products")])


# ---------------------------------------------------------------- applications index

def applications_index():
    depth = 1
    body = """
<section class="hero hero-dark">
  <div class="wrap grid">
    <div>
      <p class="eyebrow">Applications</p>
      <h1>Nine industries, mapped zone by zone</h1>
      <p class="lede">Most heater sites list industries and stop there. Each of these pages carries a
        process diagram with the heated zones marked, and a table that maps the machine you already
        have to the element type each position wants.</p>
      <div class="actions">
        <a class="btn" href="../build-a-list/">Build a requirement list</a>
        <a class="btn btn-onink" href="../products/">Browse by product instead</a>
      </div>
    </div>
    <div class="shot">
      <span class="label">Photograph required</span>
      <p>A customer plant floor, machines running. Landscape, minimum 2400 px wide.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sechead">
      <h2>Pick your process</h2>
      <p>If yours is not here, the last one covers it. One off industrial heating is most of what a
        works like this actually does.</p>
    </div>
    %(inds)s
  </div>
</section>

<section class="band alt">
  <div class="wrap two">
    <div>
      <h2>Why the zone table exists</h2>
      <p>An injection moulding machine has at least six places that have to be held at a
        temperature, and each one wants a different element. A band heater on a barrel, a coil on a
        manifold and a cartridge in a platen are three different specifications, three different
        failure modes and three different things to get wrong.</p>
      <p>Putting them in one table, against the zone they belong to, is the fastest way for a
        maintenance engineer to work out what to order.</p>
    </div>
    <div>
      <h2>Send us the machine, not the part number</h2>
      <p>Old part numbers do not travel between suppliers. The machine make and model, the zone, the
        measured diameter and the temperature do. A photograph of the old element beside a tape
        measure is usually enough to start.</p>
      <p><a class="btn" href="../contact/">Send us a photograph</a></p>
    </div>
  </div>
</section>
""" % {"inds": cards(depth, [("applications/%s/" % i["slug"], i["name"], i["lede"]) for i in INDUSTRIES])}
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Applications",
          "description": "Nine industries, mapped zone by zone to the element type each position wants.",
          "publisher": {"@type": "Organization", "name": COMPANY["name"]}}
    return page("applications/index.html", "Applications | %s" % COMPANY["name"],
                "Heaters for injection moulding, extrusion, blow moulding, packaging, die and mould, "
                "food, pharmaceutical machinery, rubber and general industrial heating.",
                body, active="applications/", depth=1, jsonld=ld,
                crumb=[("", "Home"), (None, "Applications")])


# ---------------------------------------------------------------- about

def about():
    body = """
<section class="hero">
  <div class="wrap grid">
    <div>
      <p class="eyebrow">About Swiftheat</p>
      <h1>A heater works is a machine shop with a wire in it</h1>
      <p class="lede">Swiftheat Thermal Technologies designs and manufactures industrial heating
        elements and temperature sensors at Peenya Industrial Area in Bengaluru, and supplies them
        to plastics, packaging, food, pharmaceutical and general engineering plant across India.</p>
      <div class="actions">
        <a class="btn" href="../capabilities/">What we can make</a>
        <a class="btn btn-ghost" href="../contact/">Come and see the works</a>
      </div>
    </div>
    <div class="shot">
      <span class="label">Photograph required</span>
      <p>The works from the shop floor, wide, with people at the benches. Landscape, minimum
        2400 px wide.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap two">
    <div>
      <h2>What the company does</h2>
      <p>Almost every industrial process that changes the shape of a material puts heat into it
        first. Plastic is melted, film is sealed, rubber is cured, air is dried, liquid is brought up
        to temperature. The element that does that work is rarely a catalogue part, because the
        machine it goes into was designed by somebody else, has been running for years, and has worn.</p>
      <p>Swiftheat makes those elements to order: cartridge, coil, ceramic and mica band, nozzle,
        strip, tubular and ceramic infrared heaters, along with the thermocouples and RTDs that
        control them. The company designs to a customer drawing, reverse engineers an element that
        no longer has a drawing, and makes prototypes before a production quantity is committed.</p>
      <p>Manufacturing happens in Peenya, which matters more than it sounds. An element built in the
        same city as the machine it serves can be measured, made, fitted and corrected inside a week.</p>
    </div>
    <div>
      <h2>The facts, as they are confirmed</h2>
      <div class="contactcard">
        <dl>
          <dt>Registered name</dt><dd>%(name)s</dd>
          <dt>Works and registered office</dt>
          <dd>%(street)s,<br>%(area)s,<br>%(city)s %(pin)s<br>
            <span class="tbd">Address to be confirmed against the letterhead before publication.</span></dd>
          <dt>Year founded</dt><dd>%(founded_long)s</dd>
          <dt>CIN</dt><dd>%(cin)s</dd>
          <dt>Plant area</dt><dd class="tbd">%(tbd)s</dd>
          <dt>People</dt><dd>%(staff)s</dd>
          <dt>Certifications</dt><dd class="tbd">%(tbd)s. Nothing is claimed here until the
            certificate itself has been supplied.</dd>
          <dt>GST and Udyam</dt><dd class="tbd">%(tbd)s</dd>
        </dl>
      </div>
      <p class="cap">Every item marked "to confirm" is waiting on a document from Swiftheat, not on
        a decision. Claims that cannot be evidenced are not published.</p>
    </div>
  </div>
</section>

<section class="band alt">
  <div class="wrap">
    <div class="sechead">
      <h2>How we work</h2>
      <p>Four things that decide whether an element lasts, and all four are settled before anything
        is made.</p>
    </div>
    <ol class="steps">
      <li><h3>Measure, do not assume</h3><p>Barrels wear and bores are re-machined. The dimension
        that matters is the one on the machine today, not the one on the original drawing.</p></li>
      <li><h3>Specify the duty, not just the size</h3><p>Continuous or cyclic, washdown or dry,
        clamped to metal or hanging in air. The same dimensions in two different duties are two
        different heaters.</p></li>
      <li><h3>Code every option</h3><p>Termination, lead protection, sheath, sensor and mounting all
        carry a code. The code travels from the enquiry to the drawing to the label, so a repeat
        order is one line, not another conversation.</p></li>
      <li><h3>Test before it leaves</h3><p>Resistance, high voltage and dimensional checks on every
        element, recorded against the order.</p></li>
    </ol>
  </div>
</section>

<section class="band">
  <div class="wrap two">
    <div>
      <h2>Industries served</h2>
      <p>Named specifically, because "all industries" tells a buyer nothing.</p>
      %(inds)s
    </div>
    <div>
      <h2>What we would rather you asked</h2>
      <p>Most enquiries arrive as a product name and a quantity. The useful ones arrive as a
        problem: this zone will not hold temperature, this element fails every three months, this
        tool heats unevenly at one end.</p>
      <p>Those are answerable. Often the answer is a different element type, a different watt
        density or a different fit, and it costs less than the part that was originally asked for.</p>
      <p><a class="btn" href="../contact/">Describe the problem instead</a></p>
    </div>
  </div>
</section>
""" % {
        "name": esc(COMPANY["name"]), "street": esc(COMPANY["street"]), "area": esc(COMPANY["area"]),
        "city": esc(COMPANY["city"]), "pin": esc(COMPANY["pin"]), "tbd": TBD,
        "founded_long": esc(COMPANY["founded_long"]), "cin": esc(COMPANY["cin"]),
        "staff": esc(COMPANY["staff"]),
        "inds": cards(1, [("applications/%s/" % i["slug"], i["name"], i["problem"]) for i in INDUSTRIES]),
    }
    return page("about/index.html", "About | %s" % COMPANY["name"],
                "Swiftheat Thermal Technologies designs and manufactures industrial heating elements "
                "and temperature sensors in Peenya Industrial Area, Bengaluru.",
                body, active="about/", depth=1, jsonld=dict(ORG),
                crumb=[("", "Home"), (None, "About")])


# ---------------------------------------------------------------- capabilities

def capabilities():
    body = """
<section class="hero">
  <div class="wrap grid">
    <div>
      <p class="eyebrow">Custom solutions and capabilities</p>
      <h1>Most of what we make has never been made before</h1>
      <p class="lede">Custom design, reverse engineering, prototypes and small batches. A works that
        can make one of something is a works that can fix a machine nobody else will touch.</p>
      <div class="actions">
        <a class="btn" href="../contact/">Send us the problem</a>
        <a class="btn btn-ghost" href="../build-a-list/">Specify it yourself</a>
      </div>
    </div>
    <div class="shot">
      <span class="label">Photograph required</span>
      <p>A winding machine or a press mid operation, hands in shot. Portrait or landscape, minimum
        2000 px wide.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sechead">
      <h2>Four things we are asked for</h2>
    </div>
    %(capcards)s
  </div>
</section>

<section class="band alt">
  <div class="wrap two">
    <div>
      <h2>How an order actually runs</h2>
      <ol>
        <li><strong>The enquiry.</strong> A specification, a drawing, a photograph of the old part,
          or a description of the problem. Any of those is enough to start.</li>
        <li><strong>The proposal.</strong> An element type, a size, a wattage and a set of coded
          options, with the reasoning for each. If a cheaper element would do the job, that is what
          gets proposed.</li>
        <li><strong>Confirmation.</strong> The coded specification is agreed. That code is what
          appears on the works order and on the label.</li>
        <li><strong>Manufacture.</strong> <span class="tbd">Lead times to be confirmed.</span></li>
        <li><strong>Test and despatch.</strong> Resistance, high voltage and dimensional checks
          recorded against the order.</li>
      </ol>
    </div>
    <div>
      <h2>Machinery and infrastructure</h2>
      <p>Buyers in this category read a machine list as a proxy for what a works can actually hold to.
        Swiftheat's list will be published here in full once supplied.</p>
      <div class="contactcard">
        <dl>
          <dt>Winding and coiling</dt><dd class="tbd">%(tbd)s</dd>
          <dt>Swaging and compaction</dt><dd class="tbd">%(tbd)s</dd>
          <dt>Welding</dt><dd class="tbd">%(tbd)s</dd>
          <dt>Press and forming</dt><dd class="tbd">%(tbd)s</dd>
          <dt>Machining</dt><dd class="tbd">%(tbd)s</dd>
          <dt>Test equipment</dt><dd class="tbd">%(tbd)s</dd>
          <dt>Plant area</dt><dd class="tbd">%(tbd)s</dd>
        </dl>
      </div>
      <p class="cap">Published as a list of named machines, not as an adjective.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap two">
    <div>
      <h2>Engineering and design</h2>
      <p>The useful part of a heater manufacturer is rarely the winding. It is knowing that a
        cartridge in a loose bore will fail regardless of how well it was made, that a rubber barrel
        wants a lower watt density than a plastics one, and that a manifold thermocouple in the wrong
        place will hold a temperature the melt never sees.</p>
      <p>That judgement is what the option codes and the selection guidance on every product page are
        for: to put as much of it as possible in front of the buyer before they enquire.</p>
    </div>
    <div class="shot shot-sm">
      <span class="label">Photograph required</span>
      <p>A drawing on the bench beside the finished element. Shows the design to part relationship in
        one frame.</p>
    </div>
  </div>
</section>
""" % {"tbd": TBD, "capcards": icon_cards(1, [
        ("noun-technical-drawing-8436969.svg", "Custom design",
         "An element designed around your drawing, your bore, your clearance and your duty. Most of "
         "the catalogue exists to give that conversation a starting point, not to be ordered from "
         "directly."),
        ("noun-caliper-8419059.svg", "Reverse engineering",
         "An element with no drawing, no supplier and a label that has burned off. Send the old part. "
         "Dimensions, resistance and construction come off it, and the replacement is made to match."),
        ("noun-prototype-8201949.svg", "Prototype development",
         "One piece, made and tested, before a production quantity is committed. Cheaper than finding "
         "out at quantity that the fit was wrong."),
        ("noun-box-stack-8142643.svg", "Small batch manufacturing",
         "Six of one size and four of another is a normal order here. Maintenance stores do not buy "
         "in hundreds."),
    ], numbered=True)}
    return page("capabilities/index.html", "Custom solutions and capabilities | %s" % COMPANY["name"],
                "Custom heater design, reverse engineering, prototype development and small batch "
                "manufacturing at Peenya, Bengaluru.",
                body, active="capabilities/", depth=1,
                crumb=[("", "Home"), (None, "Capabilities")])


# ---------------------------------------------------------------- quality

def quality():
    body = """
<section class="hero">
  <div class="wrap grid">
    <div>
      <p class="eyebrow">Quality and testing</p>
      <h1>What is tested, and what you receive</h1>
      <p class="lede">In this category a certificate on the wall proves less than a test record
        against your order number. This page will carry both, and neither is claimed until the
        evidence exists.</p>
      <div class="actions">
        <a class="btn" href="../contact/">Ask for a sample certificate</a>
      </div>
    </div>
    <div class="shot">
      <span class="label">Photograph required</span>
      <p>The test bench in use: an element connected, meter reading visible. Minimum 2000 px wide.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sechead">
      <h2>The electrical tests</h2>
      <p>Four named tests, each with what it catches. The equipment used and the pass criteria are
        published once Swiftheat confirms them.</p>
    </div>
    %(testcards)s
    <div class="tablewrap" style="margin-top:32px">
      <table>
        <caption>Equipment used and the criterion applied, per test</caption>
        <thead><tr><th scope="col">Test</th><th scope="col">Equipment</th>
          <th scope="col">Criterion</th><th scope="col">Recorded against the order</th></tr></thead>
        <tbody>
          <tr><th scope="row">Resistance</th><td class="tbd">%(tbd)s</td><td class="tbd">%(tbd)s</td>
            <td class="tbd">%(tbd)s</td></tr>
          <tr><th scope="row">High voltage</th><td class="tbd">%(tbd)s</td><td class="tbd">%(tbd)s</td>
            <td class="tbd">%(tbd)s</td></tr>
          <tr><th scope="row">Insulation resistance</th><td class="tbd">%(tbd)s</td>
            <td class="tbd">%(tbd)s</td><td class="tbd">%(tbd)s</td></tr>
          <tr><th scope="row">Dimensional inspection</th><td class="tbd">%(tbd)s</td>
            <td class="tbd">%(tbd)s</td><td class="tbd">%(tbd)s</td></tr>
        </tbody>
      </table>
    </div>
    <div class="note">
      <p><strong>Why insulation resistance is worth publishing.</strong> A cartridge heater that has
        sat in a damp store reads low on insulation resistance and can often be recovered by baking
        it out at low temperature rather than being scrapped. A manufacturer that measures it can
        tell you that. One that does not will simply replace the element.</p>
    </div>
  </div>
</section>

<section class="band alt">
  <div class="wrap two">
    <div>
      <h2>Material traceability</h2>
      <p>Sheath material, resistance wire and insulation are the three things a buyer cannot verify
        by looking. What is recorded against a batch, and what can be produced afterwards, will be
        published here.</p>
      <div class="contactcard">
        <dl>
          <dt>Sheath material records</dt><dd class="tbd">%(tbd)s</dd>
          <dt>Resistance wire records</dt><dd class="tbd">%(tbd)s</dd>
          <dt>Batch identification on the part</dt><dd class="tbd">%(tbd)s</dd>
          <dt>Retention period</dt><dd class="tbd">%(tbd)s</dd>
        </dl>
      </div>
    </div>
    <div>
      <h2>What arrives with the delivery</h2>
      <p>The paperwork matters as much as the part on a plant that has to prove what it fitted.</p>
      <ul class="check">
        <li>The coded specification, matching the enquiry</li>
        <li>Measured resistance for each element</li>
        <li>High voltage test result</li>
        <li>Dimensional check against the drawing</li>
        <li><span class="tbd">Certificate format to be confirmed</span></li>
      </ul>
      <p>If you need a redacted sample certificate before ordering, ask and we will send one.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap two">
    <div>
      <h2>Certifications</h2>
      <p>Nothing appears in this section without the certificate behind it. That is deliberate: an
        unlabelled scan of a certificate is one of the commonest things on Indian heater sites and it
        proves nothing.</p>
      <div class="contactcard">
        <dl>
          <dt>ISO 9001</dt><dd class="tbd">%(tbd)s</dd>
          <dt>Udyam or MSME registration</dt><dd class="tbd">%(tbd)s</dd>
          <dt>GST</dt><dd class="tbd">%(tbd)s</dd>
          <dt>CIN</dt><dd>%(cin)s</dd>
        </dl>
      </div>
    </div>
    <div>
      <h2>How elements are checked in service</h2>
      <p>Two measurements catch almost every heater fault on a plant, and both can be taken with a
        multimeter and an insulation tester.</p>
      <p><strong>Resistance.</strong> Compare against the value on the test record. A reading that
        has climbed means the element is failing. An open circuit means it has already gone.</p>
      <p><strong>Insulation resistance.</strong> A low reading against earth usually means moisture
        or contamination, not a dead element. Bake it out before scrapping it.</p>
      <p><a href="../contact/">Ask us what a reading means</a> before ordering a replacement. It is
        often cheaper for both sides.</p>
    </div>
  </div>
</section>
""" % {"tbd": TBD, "cin": COMPANY["cin"], "testcards": icon_cards(1, [
        ("noun-multimeter-8419064.svg", "Resistance",
         "Catches the wrong wattage, a wrong turn count and a bad joint. It is also the number you "
         "measure against later, on the plant, to tell a failing element from a dead one."),
        ("noun-high-voltage-8368320.svg", "High voltage",
         "Catches insulation that would hold at working voltage and break down in service. The test "
         "that stops an element becoming a shock hazard on a machine frame."),
        ("noun-insulation-5848062.svg", "Insulation resistance",
         "Catches moisture in the magnesium oxide and contamination in the sheath. A low reading is "
         "often recoverable by baking out rather than scrapping."),
        ("noun-micrometer-8419029.svg", "Dimensional inspection",
         "Catches a diameter or a length that will not fit the bore it was made for. On a cartridge "
         "heater this is the measurement that decides how long it lasts."),
    ])}
    return page("quality/index.html", "Quality and testing | %s" % COMPANY["name"],
                "Resistance, high voltage, insulation resistance and dimensional testing on every "
                "element, with what arrives alongside the delivery.",
                body, active="quality/", depth=1,
                crumb=[("", "Home"), (None, "Quality")])


# ---------------------------------------------------------------- resources

def resources():
    fam_rows = "".join(
        '<li><span aria-disabled="true"><span>%s datasheet</span>'
        '<span class="meta">PDF, to be produced</span></span></li>' % esc(f["name"]) for f in FAMILIES)
    body = """
<section class="hero">
  <div class="wrap grid">
    <div>
      <p class="eyebrow">Resources</p>
      <h1>Downloads, drawings and the works gallery</h1>
      <p class="lede">Everything here is free and none of it sits behind a form. A buyer should be
        able to forward a datasheet to their purchase department in one click without giving up an
        email address first.</p>
      <div class="actions">
        <a class="btn" href="../build-a-list/">Build a requirement list</a>
        <a class="btn btn-ghost" href="../contact/">Ask for something specific</a>
      </div>
    </div>
    <div class="shot">
      <span class="label">Photograph required</span>
      <p>A printed catalogue and a datasheet on the bench. Used as the section image here and on the
        home page.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap two">
    <div>
      <h2>Product datasheets</h2>
      <p>One per family: construction, specification table, dimensions and the full option list with
        codes. These are produced from the same source as the product pages, so they cannot drift
        apart from what the site says.</p>
      <ul class="dl">%(fams)s</ul>
    </div>
    <div>
      <h2>Company documents</h2>
      <ul class="dl">
        <li><span aria-disabled="true"><span>Full product catalogue</span><span class="meta">PDF, to be produced</span></span></li>
        <li><span aria-disabled="true"><span>Printable order form</span><span class="meta">PDF, to be produced</span></span></li>
        <li><span aria-disabled="true"><span>Installation and removal guide</span><span class="meta">PDF, to be produced</span></span></li>
        <li><span aria-disabled="true"><span>ISO certificate</span><span class="meta">Awaiting the certificate</span></span></li>
        <li><span aria-disabled="true"><span>Sample test certificate, redacted</span><span class="meta">Awaiting a sample</span></span></li>
      </ul>
      <div class="note">
        <p><strong>Nothing is published as a download until it exists.</strong> A dead link to a
          catalogue costs more trust than an honest note saying it is coming.</p>
      </div>
    </div>
  </div>
</section>

<section class="band alt">
  <div class="wrap">
    <div class="sechead">
      <h2>The works</h2>
      <p>A gallery of the plant, the machinery and the people. This is the single strongest thing a
        real manufacturer can show, and it is what separates a works from a trading company.</p>
    </div>
    <div class="three">
      <div class="shot"><span class="label">Photograph required</span><p>Winding: the machine and the
        operator, mid run.</p></div>
      <div class="shot"><span class="label">Photograph required</span><p>Assembly bench with parts
        laid out in progress.</p></div>
      <div class="shot"><span class="label">Photograph required</span><p>Test bench: element
        connected, instrument reading visible.</p></div>
      <div class="shot"><span class="label">Photograph required</span><p>Finished goods packed and
        labelled for despatch.</p></div>
      <div class="shot"><span class="label">Photograph required</span><p>Product range group shot on
        a clean surface, from above.</p></div>
      <div class="shot"><span class="label">Photograph required</span><p>The building and the
        signage, so a first time visitor can find it.</p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap two">
    <div>
      <h2>Technical drawings</h2>
      <p>Every product page carries a dimensioned drawing with the same names used in the table and
        in the enquiry form. The list builder draws your own configuration live and the document it
        produces carries that drawing with it.</p>
      <p><a class="btn btn-ghost" href="../products/">See the product pages</a></p>
    </div>
    <div>
      <h2>Reference data</h2>
      <p>Watt density guidance, bore fit tables, thermocouple type comparison and failure diagnosis
        will be published here as reference pages rather than as gated PDFs.</p>
      <p class="tbd">To be written once the specification ranges are confirmed.</p>
    </div>
  </div>
</section>
""" % {"fams": fam_rows}
    return page("resources/index.html", "Resources and downloads | %s" % COMPANY["name"],
                "Datasheets, catalogues, drawings and the works gallery. Free, and never behind a "
                "form.",
                body, active="resources/", depth=1,
                crumb=[("", "Home"), (None, "Resources")])


# ---------------------------------------------------------------- contact

def contact():
    maps = ("https://www.google.com/maps/search/?api=1&query="
            + "+".join((COMPANY["street"] + " " + COMPANY["area"] + " " + COMPANY["city"] + " "
                        + COMPANY["pin"]).replace(",", "").split()))
    body = """
<section class="hero">
  <div class="wrap grid">
    <div>
      <p class="eyebrow">Contact and get a quote</p>
      <h1>Peenya Industrial Area, 1st Phase</h1>
      <p class="lede">Send a specification and it is quoted from directly. Send a photograph of the
        old element and we will work it out. Either way it reaches an engineer, not a form inbox.</p>
      <div class="actions">
        <a class="btn" href="#enquiry">Send a specification</a>
        <a class="btn btn-ghost" href="../build-a-list/">Build a requirement list</a>
      </div>
    </div>
    <div>
      <div class="contactcard">
        <dl>
          <dt>Works and office</dt>
          <dd>%(street)s,<br>%(area)s,<br>%(city)s %(pin)s</dd>
          <dt>Email</dt><dd><a href="mailto:%(email)s">%(email)s</a></dd>
          <dt>Phone</dt><dd class="tbd">%(tbd)s</dd>
          <dt>WhatsApp</dt><dd class="tbd">%(tbd)s</dd>
          <dt>Hours</dt><dd class="tbd">%(tbd)s</dd>
          <dt>Directions</dt><dd><a href="%(maps)s" rel="noopener">Open in Google Maps</a></dd>
        </dl>
      </div>
      <p class="cap">The phone number on the previous site was a placeholder that nobody could call.
        No number goes back on the site until it has been dialled and answered.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap two">
    <div>
      <h2>What to send</h2>
      <p>The more of this that arrives with the first message, the fewer phone calls it takes.</p>
      <ul class="check">
        <li>Which element type, or a description of what needs heating</li>
        <li>Dimensions: diameter, length, width, or the bore in your own part</li>
        <li>Wattage and voltage, or the temperature you need to reach</li>
        <li>The machine make and model, and which zone on it</li>
        <li>Duty: continuous or cyclic, wet or dry, moving or static</li>
        <li>Quantity, and when you need it</li>
        <li>A drawing or a photograph of the old element beside a tape measure</li>
      </ul>
    </div>
    <div>
      <h2>Finding the works</h2>
      <p>Peenya Industrial Area 1st Phase, near SVC Co-operative Bank. Come and see the plant if you
        are specifying anything unusual: half an hour on the shop floor settles more than a week of
        email.</p>
      <div class="shot shot-sm">
        <span class="label">Photograph required</span>
        <p>The unit frontage and signage from the road, so a first time visitor recognises it.</p>
      </div>
      <p class="cap" style="margin-top:16px">No map is embedded here on purpose. An embedded map
        loads third party scripts and sets cookies, which would mean a consent banner on every page
        of an otherwise cookie free site.</p>
    </div>
  </div>
</section>

%(enquiry)s
""" % {
        "street": esc(COMPANY["street"]), "area": esc(COMPANY["area"]), "city": esc(COMPANY["city"]),
        "pin": esc(COMPANY["pin"]), "email": COMPANY["email"], "tbd": TBD, "maps": maps,
        "enquiry": enquiry(
            1, "Send a specification", "Website enquiry",
            "Fill in what you know and leave the rest. The message is composed in your own mail "
            "application, so you can attach a drawing before you send it, and nothing is stored on "
            "any server.",
            extra_fields=_general_fields(),
            scope_note="Every product and industry page carries the same form, already scoped."),
    }
    ld = dict(ORG)
    ld["@type"] = "LocalBusiness"
    return page("contact/index.html", "Contact and get a quote | %s" % COMPANY["name"],
                "Swiftheat Thermal Technologies, Peenya Industrial Area 1st Phase, Bengaluru 560058. "
                "Send a heater specification and it is quoted from directly.",
                body, active="contact/", depth=1, jsonld=ld,
                crumb=[("", "Home"), (None, "Contact")])


# ---------------------------------------------------------------- list builder

BUILDER_BODY = """
<div id="builderView">
  <section class="hero">
    <div class="wrap">
      <p class="eyebrow">Requirement list</p>
      <h1>Build your heater list</h1>
      <p class="lede">Pick a heater, set the sizes, choose the options, add it to the list. The
        drawing stays beside you and redraws on every change, so you can see the part you are asking
        for before you send it. When you are done, generate a document you can print, email or send
        on WhatsApp. Nothing is stored anywhere and no account is needed.</p>
    </div>
  </section>

  <section class="band">
    <div class="wrap builder">
      <div class="steps">

        <div class="step">
          <div class="step-head"><span class="n" aria-hidden="true">01</span><h2>Which heater?</h2></div>
          <p class="hint">Pick a family. The sizes and options below change to suit it, and so does
            the drawing.</p>
          <ul class="tiles tiles-fam" id="famTiles" aria-label="Product family"></ul>
        </div>

        <div class="step" id="specStep" hidden>
          <div class="step-head"><span class="n" aria-hidden="true">02</span><h2>Sizes</h2></div>
          <p class="hint">Fill in what you know. Leave anything you are unsure of and our engineers
            will suggest it. Each numbered box is the dimension with the same number on the drawing.</p>
          <div class="dimfields" id="dimFields"></div>
          <div class="elecfields" id="elecFields"></div>
        </div>

        <div class="step" id="optStep" hidden>
          <div class="step-head"><span class="n" aria-hidden="true">03</span><h2>Options</h2></div>
          <p class="hint">Tap to choose. Every option changes the drawing and carries the code that
            appears on the final document.</p>
          <div id="optGroups"></div>
        </div>

        <div class="step" id="addStep" hidden>
          <div class="step-head"><span class="n" aria-hidden="true">04</span><h2>Add it to the list</h2></div>
          <div class="partcode">
            <span class="lab">Part code</span>
            <span class="val" id="partCode">&mdash;</span>
          </div>
          <div class="addrow">
            <div class="spec">
              <label for="qty">Quantity <span class="u">nos</span></label>
              <input id="qty" type="number" min="1" max="9999" value="1" inputmode="numeric">
            </div>
            <div class="spec" style="max-width:260px">
              <label for="lineNote">Note for this line <span class="u">optional</span></label>
              <input id="lineNote" type="text" placeholder="e.g. for machine 3, urgent">
            </div>
            <button class="btn" type="button" id="addBtn">Add to list</button>
          </div>
        </div>

      </div>

      <div class="rail">

        <section class="viz-panel" id="vizPanel" hidden aria-labelledby="vizTitle">
          <div class="viz-head">
            <h2 id="vizTitle">Live drawing</h2>
            <div class="viewtoggle" id="viewToggle" role="group" aria-label="Drawing style">
              <button type="button" data-mode="flat" aria-pressed="true">Flat</button>
              <button type="button" data-mode="iso" aria-pressed="false">Isometric</button>
            </div>
          </div>
          <div id="vizArt"></div>
          <p class="cap" id="vizCap">The numbers match the boxes on the left. Every size and every
            option redraws this at once. Not to scale.</p>
        </section>

        <aside class="cart" aria-label="Your list">
          <div class="cart-head">
            <h2>Your list</h2>
            <span class="badge" id="cartCount">0</span>
          </div>
          <div class="cart-body" id="cartBody">
            <div class="cart-empty" id="cartEmpty">
              <svg width="52" height="40" viewBox="0 0 52 40" aria-hidden="true">
                <g fill="none" stroke="currentColor" stroke-width="1.6">
                  <rect x="8" y="14" width="30" height="12" rx="3"/>
                  <path d="M38 18h8M38 22h8"/>
                  <path d="M4 33h44" stroke-dasharray="3 3"/>
                </g>
              </svg>
              <p>Nothing added yet.<br>Pick a heater to start.</p>
            </div>
          </div>
          <div class="cart-foot" id="cartFoot" hidden>
            <div class="tot"><span>Line items</span><b id="totLines">0</b></div>
            <div class="tot"><span>Total pieces</span><b id="totQty">0</b></div>
            <button class="btn" type="button" id="reviewBtn">Review and generate</button>
          </div>
        </aside>

      </div>
    </div>
  </section>

  <section class="band alt" id="whoStep" hidden>
    <div class="wrap">
      <h2>Who is this for?</h2>
      <p>Used on the document and so we know who to reply to. Swiftheat staff building a list for a
        customer can put the customer's details here.</p>
      <div class="who">
        <div class="spec"><label for="cName">Name</label><input id="cName" type="text" autocomplete="name"></div>
        <div class="spec"><label for="cComp">Company</label><input id="cComp" type="text" autocomplete="organization"></div>
        <div class="spec"><label for="cMail">Email</label><input id="cMail" type="email" autocomplete="email"></div>
        <div class="spec"><label for="cPhone">Phone or WhatsApp</label><input id="cPhone" type="tel" autocomplete="tel"></div>
        <div class="spec"><label for="cRef">Your reference <span class="u">optional</span></label><input id="cRef" type="text" placeholder="PO or enquiry number"></div>
        <div class="spec"><label for="cNeed">Required by <span class="u">optional</span></label><input id="cNeed" type="text" placeholder="e.g. 2 weeks"></div>
      </div>
    </div>
  </section>
</div>

<div id="docView" hidden>
  <div class="docwrap">
    <div class="docbar">
      <button class="back" type="button" id="backBtn">&larr; Back to the list</button>
      <span class="spacer"></span>
      <button class="btn" type="button" id="printBtn">Save as PDF or print</button>
      <button class="btn btn-ghost" type="button" id="mailBtn">Send by email</button>
      <button class="btn wa" type="button" id="waBtn">Send on WhatsApp</button>
    </div>
    <article class="doc" id="doc">
      <h2 class="dochead">Heater requirement list</h2>
      <div class="docmeta" id="docMeta"></div>
      <div class="tablewrap" style="border:0;margin:0">
        <table id="docTable">
          <thead>
            <tr>
              <th scope="col">#</th><th scope="col">Part code</th><th scope="col">Heater</th>
              <th scope="col">Specification</th><th scope="col" class="n">Qty</th>
            </tr>
          </thead>
          <tbody id="docBody"></tbody>
        </table>
      </div>
      <div class="foot">
        <p><strong>%(name)s</strong><br>
          %(street)s, %(area)s, %(city)s %(pin)s<br>
          <a href="mailto:%(email)s">%(email)s</a>
          <span class="tbd">Phone number to be confirmed before publication.</span></p>
        <p>This is a requirement list, not a quotation. Prices and lead times follow from Swiftheat
          once the specification is confirmed. Where a value was left blank, our engineers will
          propose one.</p>
      </div>
    </article>
  </div>
</div>
"""


def build_a_list():
    body = BUILDER_BODY % {
        "name": esc(COMPANY["name"]), "street": esc(COMPANY["street"]), "area": esc(COMPANY["area"]),
        "city": esc(COMPANY["city"]), "pin": esc(COMPANY["pin"]), "email": COMPANY["email"],
    }
    return page("build-a-list/index.html", "Build a heater requirement list | %s" % COMPANY["name"],
                "Specify several heaters in one pass, see each one drawn as you specify it, and "
                "generate a printable requirement document. Nothing is stored and no account needed.",
                body, active="build-a-list/", depth=1,
                extra_css=["css/bom.css"], extra_js=["js/bom.js"],
                crumb=[("", "Home"), (None, "Build a list")])


# ---------------------------------------------------------------- 404

def not_found():
    body = """
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">404</p>
    <h1>That page is not here</h1>
    <p class="lede">The link may be old, or the address may have a typo in it. These three cover
      almost everything on the site.</p>
    <div class="actions">
      <a class="btn" href="/products/">All products</a>
      <a class="btn btn-ghost" href="/applications/">All industries</a>
      <a class="btn btn-ghost" href="/contact/">Contact</a>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>Product families</h2>
    %(prods)s
  </div>
</section>
""" % {"prods": cards(0, [("products/%s/" % f["slug"], f["name"], f["summary"]) for f in FAMILIES])}
    # A 404 is served from any depth, so its links have to be absolute.
    html_out = page("404.html", "Page not found | %s" % COMPANY["name"],
                    "That page is not here. Links to the product families, the industries and the "
                    "contact page.",
                    body, active="", depth=0)
    return _absolutise(html_out)


def _absolutise(doc):
    """The 404 document is served in place of any URL at any depth, so every
    relative link in it would resolve against the wrong base. Root them."""
    import re
    doc = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|/)([^"]+)"', r'\1="/\2"', doc)
    return doc
