#!/usr/bin/env python3
"""Generates the Swiftheat proposal pages. One shell, seven bodies."""
import html, pathlib

PAGES = [
    ("index.html",             "Proposal",             "Swiftheat website proposal"),
    ("01-what-we-found.html",  "What we found",        "The inputs the build starts from"),
    ("02-what-we-build.html",  "What we will build",   "Structure, product pages, industry pages"),
    ("03-plan.html",           "How the work runs",    "Phases, timeline and what we need"),
    ("04-investment.html",     "The investment",       "Rs 65,000, and what it covers"),
]

DESCR = {
 "index.html":"Website redesign proposal for Swiftheat Thermal Technologies, Peenya, Bangalore. Prepared by ProPage.",
 "01-what-we-found.html":"What the current swiftheat.co.in contains, and what the new build needs from it.",
 "02-what-we-build.html":"The proposed structure: seven product family pages, nine industry pages, and an enquiry form that asks for a specification.",
 "03-plan.html":"The five phases of the build, the timeline, and the content and photography we need from Swiftheat.",
 "04-investment.html":"Rs 65,000 for the complete build, and exactly what that covers.",
}

def nav(current):
    items = []
    for i, (href, short, _sub) in enumerate(PAGES):
        n = "%02d" % i
        cur = ' aria-current="page"' if href == current else ""
        items.append(
            '        <li><a href="%s"%s><span class="n" aria-hidden="true">%s</span>'
            '<span>%s</span></a></li>' % (href, cur, n, html.escape(short))
        )
    return "\n".join(items)

def pager(current):
    idx = [p[0] for p in PAGES].index(current)
    out = ['    <nav class="pager" aria-label="Proposal pages">']
    if idx > 0:
        h, s, _ = PAGES[idx - 1]
        out.append('      <a class="prev" href="%s"><span class="dir">Previous</span>'
                   '<span class="to">%s</span></a>' % (h, html.escape(s)))
    if idx < len(PAGES) - 1:
        h, s, _ = PAGES[idx + 1]
        out.append('      <a class="next" href="%s"><span class="dir">Next</span>'
                   '<span class="to">%s</span></a>' % (h, html.escape(s)))
    out.append("    </nav>")
    return "\n".join(out)

SHELL = """<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{descr}">
<meta name="robots" content="noindex, nofollow">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{descr}">
<meta property="og:type" content="website">
<link rel="preload" href="fonts/archivo-narrow-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/proposal.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="shell">
  <aside class="rail">
    <a class="brandmark" href="index.html">Pro<span>Page</span></a>
    <p class="rail-meta">Website proposal<br>Swiftheat Thermal Technologies<br>25 August 2026</p>
    <button class="railtoggle" type="button" aria-expanded="true" aria-controls="contents">Contents</button>
    <nav id="contents" aria-label="Proposal contents">
      <p class="rail-title">In this proposal</p>
      <ol>
{navitems}
      </ol>
    </nav>
    <p class="rail-foot">ProPage<br><a href="tel:+919945621717">+91 9945 62 1717</a></p>
  </aside>
  <main class="main" id="main">
{body}
{pagerhtml}
  </main>
</div>
<script src="js/proposal.js"></script>
</body>
</html>
"""

BODIES = {}

BODIES["index.html"] = """
    <header class="cover">
      <p class="eyebrow">Website design and development proposal</p>
      <h1>The heater is made to a drawing. The website should be too.</h1>
      <p>A redesign of swiftheat.co.in built around the one thing your buyer is actually
        trying to do: describe a heater precisely enough to get a price.</p>
      <dl class="meta">
        <div><dt>Prepared for</dt><dd>Rekha Prabhu, Swiftheat Thermal Technologies Pvt Ltd</dd></div>
        <div><dt>Prepared by</dt><dd>ProPage</dd></div>
        <div><dt>Date</dt><dd>25 August 2026</dd></div>
        <div><dt>Investment</dt><dd>Rs 65,000 complete, first year of care included</dd></div>
      </dl>
    </header>

    <div class="wrap">
      <p class="lede">Rather than describe the site we would build for you, we have built a
        page of it. Everything else in this proposal follows from that page.</p>
      <hr class="rule">
    </div>

    <div class="finding">
      <span class="tag">Start here</span>
      <p><a href="mockup/bom-builder.html"><strong>Open the heater list builder</strong></a>.
        Pick a heater, set the sizes, tap the options, add it to the list. Build up as many
        lines as you need, then generate a document you can save as a PDF, email or send on
        WhatsApp. Your sales team can use the same tool to build a list on a customer's
        behalf.</p>
      <p><a href="mockup/cartridge-heaters.html"><strong>Open the cartridge heater page</strong></a>.
        It is a working page, not a picture of one: specification tables, a construction
        cutaway, a dimensioned drawing, your ordering options set out with codes, and an
        enquiry form that shows you the email your works would receive. Every specification
        value in it is deliberately marked "to confirm", because those numbers come from your
        engineers, not from us.</p>
    </div>

    <div class="wrap">
      <p>Twenty three pages, built to the same standard as that one. Seven product families,
        nine industries, your custom work and capabilities, your quality and testing, your
        downloads, and an enquiry form that asks a customer for a diameter rather than a
        paragraph.</p>

      <h2>What is in this proposal</h2>
    </div>

    <ol class="steps">
      <li>
        <h3><a href="01-what-we-found.html">What we found</a></h3>
        <p>What your current site contains, what can be reused, and the handful of things
          that need a decision from you before the build can start.</p>
      </li>
      <li>
        <h3><a href="02-what-we-build.html">What we will build</a></h3>
        <p>The full structure, how a product page is put together, how an industry page
          works, and the enquiry form in detail.</p>
      </li>
      <li>
        <h3><a href="03-plan.html">How the work runs</a></h3>
        <p>Five phases, six to eight weeks, and a straight list of what we need from your
          side before we can start and before we can launch.</p>
      </li>
      <li>
        <h3><a href="04-investment.html">The investment</a></h3>
        <p>Rs 65,000 for the complete build, what that covers, and the terms.</p>
      </li>
    </ol>

    <div class="quiet">
      <p><strong>One promise about content.</strong> We publish only what you send us and can
        verify. No invented certifications, no borrowed photographs, no claims about years or
        clients that we cannot stand behind. Anything still unconfirmed appears on the preview
        marked as outstanding, in a colour you cannot miss, until you confirm it.</p>
    </div>
"""

BODIES["01-what-we-found.html"] = """
    <div class="chapter"><span class="num" aria-hidden="true">01</span>
      <div><p class="eyebrow">Section one</p><h1>Where you stand today</h1></div></div>
    <div class="wrap">
      <p class="lede">swiftheat.co.in runs on WordPress with the Elementor page builder,
        hosted at Hostinger. Every image on it was uploaded in June or July 2024. There are
        four pages: Home, About Us, Products and Contact Us.</p>
      <hr class="rule">
      <h2>Three faults that are costing you enquiries now</h2>
    </div>

    <div class="finding">
      <span class="tag">Fault 1</span>
      <p><strong>Your phone number is a placeholder.</strong> The Contact page publishes
        <code>+91 12345 67890</code>. It has been there since the site was built. Anyone who
        tries to call the number on your website reaches nobody.</p>
    </div>
    <div class="finding">
      <span class="tag">Fault 2</span>
      <p><strong>Placeholder Latin text is still live on the Home page.</strong> Under the
        heading "06. Immersion Heaters" the page reads "Click edit button to change this
        text. Lorem ipsum dolor sit amet, elit. Ut elit tellus, nec ullamcorper."</p>
    </div>
    <div class="finding">
      <span class="tag">Fault 3</span>
      <p><strong>The address on the site is not the address on your letterhead.</strong> The
        website says Plot No. B-132, 3rd Cross, E Main, near Peenya Police Station. Your email
        signature says Plot No. C-262, 6th Cross, near SVC Co-operative Bank. Google is
        currently working from the first one. We need you to confirm which is correct before
        anything is published.</p>
    </div>

    <div class="wrap">
      <h2>What else the audit found</h2>
      <ul>
        <li><strong>Nothing on the site is tappable.</strong> There is not one
          <code>tel:</code> or <code>mailto:</code> link anywhere. On a phone your number and
          your email address are plain text. A visitor has to memorise them and switch apps.
          Most will not.</li>
        <li><strong>The social icons link nowhere.</strong> Facebook, X and LinkedIn all
          render on the Contact page with no destination attached.</li>
        <li><strong>There is nothing to download.</strong> No catalogue, no datasheet, no
          brochure, no test certificate. A buyer who wants to send your details to their
          purchase department has nothing to send.</li>
        <li><strong>There is no quality or testing content at all</strong>, which in this
          category is one of the two or three things a buyer is actually checking.</li>
        <li><strong>There are no applications or industries pages</strong>, so a search like
          "cartridge heater for injection moulding" has nowhere on your site to land.</li>
        <li><strong>The enquiry form asks four things:</strong> name, phone, email, message.
          For a heater manufacturer that is four things that are not a specification.</li>
      </ul>

      <h2>The photography problem</h2>
      <p>This is the largest single gap, and it will decide how good the new site can look.
        There are twenty images on the entire website. These are the original sizes of the
        product photographs, as stored on your server.</p>
    </div>

    <div class="tablewrap">
      <table>
        <caption>Original image dimensions on swiftheat.co.in, measured 25 August 2026</caption>
        <thead><tr><th scope="col">Image</th><th scope="col" class="num-cell">Width</th>
          <th scope="col" class="num-cell">Height</th><th scope="col">Usable for a modern page?</th></tr></thead>
        <tbody>
          <tr><td>Coil heaters</td><td class="num-cell">835 px</td><td class="num-cell">835 px</td><td>Largest on the site. Small card only.</td></tr>
          <tr><td>Band heaters</td><td class="num-cell">733 px</td><td class="num-cell">547 px</td><td>Small card only.</td></tr>
          <tr><td>Strip heaters</td><td class="num-cell">602 px</td><td class="num-cell">602 px</td><td>Small card only.</td></tr>
          <tr><td>Tubular heaters</td><td class="num-cell">352 px</td><td class="num-cell">352 px</td><td>No.</td></tr>
          <tr><td>Cartridge heaters</td><td class="num-cell">314 px</td><td class="num-cell">314 px</td><td>No.</td></tr>
          <tr><td>Temperature sensors</td><td class="num-cell">256 px</td><td class="num-cell">256 px</td><td>No.</td></tr>
          <tr><td>Company logo</td><td class="num-cell">625 px</td><td class="num-cell">208 px</td><td>Raster only. No vector file exists online.</td></tr>
        </tbody>
      </table>
    </div>

    <div class="wrap">
      <p>A full width photograph on a modern site needs roughly 2000 pixels across. Nothing
        here reaches half of that. New photography is not a nice addition to this project, it
        is a requirement, and we have set out the options in
        <a href="03-plan.html">how the work runs</a>.</p>

      <h2>Your product list has changed</h2>
      <p>The list in your brief does not match what the website shows. We need this settled
        before we start.</p>
    </div>

    <div class="tablewrap">
      <table>
        <caption>Current website compared with the product list in your brief</caption>
        <thead><tr><th scope="col">On the website today</th><th scope="col">In your brief</th><th scope="col">Status</th></tr></thead>
        <tbody>
          <tr><td>Cartridge Heaters</td><td>Cartridge Heaters, with or without inbuilt thermocouple</td><td>Expanded</td></tr>
          <tr><td>Coil Heaters</td><td>Coil Heaters, with or without inbuilt thermocouple</td><td>Expanded</td></tr>
          <tr><td>Band Heaters</td><td>Ceramic and Mica Band Heaters, plus Ceramic and Mica Nozzle Heaters</td><td>Split into two families</td></tr>
          <tr><td>Strip Heaters</td><td>Strip Heaters</td><td>Unchanged</td></tr>
          <tr><td>Tubular Heaters</td><td>Tubular Heaters</td><td>Unchanged</td></tr>
          <tr><td>Temperature Sensors</td><td>Thermocouples and Temperature Sensors</td><td>Expanded</td></tr>
          <tr class="is-us"><td>Immersion Heaters</td><td>Not listed</td><td>Please confirm: dropped or omitted?</td></tr>
          <tr class="is-us"><td>Control Systems</td><td>Not listed</td><td>Please confirm: dropped or omitted?</td></tr>
          <tr class="is-us"><td>Not listed</td><td>Ceramic Infrared Heaters</td><td>New. No copy or photographs exist.</td></tr>
        </tbody>
      </table>
    </div>

    <div class="wrap">
      <h2>What is worth keeping</h2>
      <p>One part of the current site is genuinely good and we would not throw it away. The
        Products page carries technical writing that an engineer clearly produced: the
        cartridge heater accessories (right angle exits, right angle blocks, T strain clamps,
        round and oval flanges, special mountable threads), the lead protection types
        (silicone coated fibreglass sleeve, braided metal sleeve, armour), the coil heater
        spiral construction, and the RTD types PT100, PT500 and PT1000.</p>
      <p>That material is a real head start. We would edit it up and build on it rather than
        start from a blank page.</p>
    </div>
"""

BODIES["02-what-we-build.html"] = """
    <div class="chapter"><span class="num" aria-hidden="true">02</span>
      <div><p class="eyebrow">Section two</p><h1>What we will build</h1></div></div>
    <div class="wrap">
      <p class="lede">Every section in your brief, plus the three things the audit says are
        unclaimed: a specification driven enquiry, product pages built like datasheets, and
        an industry page for each of the nine industries you named.</p>
      <hr class="rule">
      <h2>The structure</h2>
      <p>Eight sections, containing twenty three pages.</p>
    </div>

    <div class="finding">
      <span class="tag">See it rather than read it</span>
      <p>Everything described in this section has been built as a working page so you can
        judge it directly.
        <a href="mockup/cartridge-heaters.html"><strong>Open the cartridge heater page
        mockup</strong></a>. The specification values in it are deliberately marked "to
        confirm", because those numbers come from your engineers. The structure, the drawings
        and the enquiry form are real and working.</p>
    </div>

    <div class="grid grid-3">
      <div class="card"><h3>Home</h3><p>Who you are, what you make, for which industries,
        and the two ways to act: request a quote, or call. Product highlights, capability
        summary, quality summary, Peenya location.</p></div>
      <div class="card"><h3>About Us</h3><p>Company profile, capabilities, vision and
        mission, why Swiftheat, infrastructure and team. Written from facts you supply.</p></div>
      <div class="card"><h3>Products</h3><p>An overview page plus <strong>seven family
        pages</strong>: cartridge, coil, ceramic and mica band, ceramic and mica nozzle,
        strip, tubular, thermocouples and sensors, ceramic infrared.</p></div>
      <div class="card"><h3>Applications</h3><p>An overview plus <strong>nine industry
        pages</strong>: injection moulding, packaging machinery, extrusion, blow moulding,
        die and mould, food processing, pharmaceutical machinery, rubber, and other
        industrial heating.</p></div>
      <div class="card"><h3>Custom Solutions and Capabilities</h3><p>Custom design, reverse
        engineering, prototype development, small batch manufacturing, your process,
        machinery and infrastructure, engineering and design capability.</p></div>
      <div class="card"><h3>Quality and Testing</h3><p>Testing procedures, resistance
        testing, high voltage testing, dimensional inspection, material traceability, and
        what the customer receives with a delivery.</p></div>
      <div class="card"><h3>Resources and Gallery</h3><p>Catalogues, technical datasheets,
        brochures, factory and infrastructure photographs, product photographs.</p></div>
      <div class="card"><h3>Contact and Get a Quote</h3><p>Address, phone, email, Google
        map, WhatsApp, and the enquiry form described below.</p></div>
    </div>

    <div class="wrap">
      <h2>The product family page</h2>
      <p>This is the piece that does the most work. Ten parts, in this order, each one
        answering a question an engineer will ask before they enquire.</p>
    </div>

    <ol class="steps">
      <li><h3>Headline and specification chips</h3><p>The family name, one line on what it
        is for, a real product photograph, and the headline numbers immediately visible:
        maximum temperature, maximum watt density, voltage range, size range.</p></li>
      <li><h3>Request a quote, above the fold</h3><p>Two buttons directly under the title:
        request a quote for this product, and download the datasheet. The buyer never has to
        hunt for either.</p></li>
      <li><h3>What it is and why the construction matters</h3><p>Two or three short
        paragraphs on construction and its thermal consequence. Mechanism, not adjectives.</p></li>
      <li><h3>Construction cutaway</h3><p>A labelled cross section: sheath, insulation,
        resistance wire, termination.</p></li>
      <li><h3>Specification table</h3><p>Maximum sheath temperature, maximum watt density,
        standard voltages, resistance tolerance, diameter range, length range, lead
        temperature rating. Split by sheath material where that changes the answer.</p></li>
      <li><h3>Dimensions</h3><p>A dimension drawing in millimetres with labelled datums,
        and a table of standard sizes.</p></li>
      <li><h3>The option catalogue</h3><p>Every option you offer, numbered, coded and
        drawn: termination location, electrical termination type, lead protection, sheath
        material, sensor options, mounting. Each one with its temperature or current rating
        and a line on when to use it. <strong>This is what turns a quotation phone call into
        a part number.</strong></p></li>
      <li><h3>Selection guidance</h3><p>How to choose a watt density for the application,
        and how to size the heater, including the bore fit that decides whether a cartridge
        heater lasts or burns out.</p></li>
      <li><h3>Installation and failure modes</h3><p>Common causes of premature failure and
        how to avoid them. In this category, telling a buyer how your product fails is the
        most credible thing you can do.</p></li>
      <li><h3>Applications, downloads, related products, enquiry</h3><p>Cards linking to the
        relevant industry pages, the datasheet PDF, adjacent families, and an enquiry form
        already scoped to this product.</p></li>
    </ol>

    <div class="wrap">
      <h2>The industry page</h2>
      <p>Nine of these, one per industry in your brief. The centre of each page is a table
        that maps the machine to your products, zone by zone.</p>
    </div>

    <div class="tablewrap">
      <table>
        <caption>Illustrative structure of the heating zone table, using injection moulding.
          Actual temperatures and product matches will come from your engineers.</caption>
        <thead><tr><th scope="col">Zone on the machine</th><th scope="col">Typical duty</th>
          <th scope="col">Swiftheat product</th><th scope="col">Why this element</th></tr></thead>
        <tbody>
          <tr><td>Barrel zones</td><td>Continuous, banded surface</td><td>Ceramic or mica band heaters</td><td>Even heat around a cylinder, clamped to suit barrel wear</td></tr>
          <tr><td>Nozzle</td><td>Tight space, fast response</td><td>Coil or nozzle heaters</td><td>High watt density in a small area, thermocouple built in</td></tr>
          <tr><td>Hot runner manifold</td><td>Precise, zoned</td><td>Coil heaters with inbuilt thermocouple</td><td>Profiled heat along the flow path</td></tr>
          <tr><td>Mould and platen</td><td>Embedded in metal</td><td>Cartridge heaters</td><td>Bore mounted, sized to the fit tolerance in your part</td></tr>
          <tr><td>Hopper and drying</td><td>Air heating</td><td>Tubular or finned heaters</td><td>Large surface area into moving air</td></tr>
        </tbody>
      </table>
    </div>

    <div class="wrap">
      <p>Around that table sits a process diagram with the zones marked, a short set of
        application notes specific to that industry, a curated shortlist of products rather
        than the whole catalogue, and an enquiry form already set to that industry.</p>

      <h2>The enquiry form</h2>
      <p>The most valuable thing in this proposal, and the cheapest to explain. A general
        contact form asks for a name, a phone number and a message. Your form will ask for a
        heater.</p>
      <p>It changes according to what the visitor selects. Two examples.</p>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h3>If they choose cartridge heaters</h3>
        <p>Sheath diameter, overall length, heated length, sheath material, watts, volts,
          watt density or "calculate it for me", termination location, lead type, lead
          length, inbuilt thermocouple and type, thermocouple junction position, mounting
          flange, threaded fitting, and the hole diameter and fit tolerance in their own
          part.</p>
      </div>
      <div class="card">
        <h3>If they choose ceramic band heaters</h3>
        <p>Inside diameter, width, construction style, angle of coverage if partial, watts,
          volts, clamping style, termination type, termination position on the circumference,
          cutouts and holes, thermocouple hole, and whether an insulation blanket is needed.</p>
      </div>
    </div>

    <div class="wrap">
      <p>The same logic covers coil, nozzle, strip, tubular, thermocouples and ceramic
        infrared. Numeric fields carry sensible minimum and maximum hints, so an impossible
        enquiry never reaches your desk. Application context comes first, contact details
        come last, and the whole thing stays on one page.</p>
      <p><strong>The list builder.</strong> The same specification logic also drives a list
        builder, so a customer ordering six different heaters does it in one pass and sends
        one document rather than six emails. Your own sales team can use it on a customer's
        behalf while on the phone. <a href="mockup/bom-builder.html">Open the list
        builder</a>.</p>
      <p><strong>How it reaches you.</strong> The form assembles everything the visitor
        entered into a clean, readable email and opens it in their own mail application,
        ready to send to your enquiry address. They attach their drawing to that message in
        the normal way. Nothing is stored on a third party server, there is no database to
        secure, and the enquiry arrives in your inbox in a form your engineer can quote from
        directly.</p>

      <h2>The engineering underneath</h2>
    </div>

    <div class="grid grid-2">
      <div class="card"><h3>Built by hand, not assembled</h3><p>Semantic HTML with one
        stylesheet and one small script. No WordPress, no Elementor, no plugins to patch and
        nothing that breaks on an update. Your current site loads 155 KB of HTML on the home
        page before a single image.</p></div>
      <div class="card"><h3>Fast, and on your own domain</h3><p>Served as static files from
        Cloudflare's global network with HTTPS. Nothing to boot up, nothing to time out, the
        same speed from Peenya as from Stuttgart.</p></div>
      <div class="card"><h3>Readable by machines</h3><p>Schema.org structured data marks up
        your company, your products and your specifications, so Google and the newer AI
        search tools can read them properly rather than guessing.</p></div>
      <div class="card"><h3>Accessible, and audited</h3><p>WCAG 2.1 AA, checked with a real
        contrast audit rather than claimed. Every tap target at least 44 pixels, and pinch
        zoom works, which matters when someone is reading a dimension table on a shop floor.</p></div>
      <div class="card"><h3>Nothing borrowed from elsewhere</h3><p>Fonts served from your own
        site, no tracking scripts, no cookie banner needed because there are no cookies to
        consent to.</p></div>
      <div class="card"><h3>Look and feel</h3><p>Two registers held together: your factory
        and your products photographed honestly, and a dry, precise datasheet treatment for
        the technical pages. Industrial, not decorative.</p></div>
    </div>
"""

BODIES["03-plan.html"] = """
    <div class="chapter"><span class="num" aria-hidden="true">03</span>
      <div><p class="eyebrow">Section three</p><h1>How the work runs</h1></div></div>
    <div class="wrap">
      <p class="lede">Six to eight weeks from the day your content reaches us. Nothing
        touches swiftheat.co.in until you have seen every page and approved it.</p>
      <hr class="rule">
    </div>

    <ol class="steps">
      <li><h3>Week 1. Content and confirmation</h3><p>We confirm your address, phone numbers,
        enquiry email and final product list. You send the logo in a vector file, your
        specification ranges per family, your testing detail, certificates, and any existing
        catalogues in whatever state they are in. We agree the photography route.</p></li>
      <li><h3>Weeks 2 to 3. Structure and design</h3><p>We build the page structure and design
        the look on the two hardest pages first: the home page and one product family page.
        You review those two before we build the other twenty one. Changing a direction here
        costs an hour. Changing it in week six costs a week.</p></li>
      <li><h3>Weeks 3 to 5. Build</h3><p>All twenty three pages, the enquiry form with its
        conditional specification fields, the datasheet templates, structured data, the map,
        WhatsApp and calling. Photography is shot or supplied during this window.</p></li>
      <li><h3>Week 6. Review on a private link</h3><p>You get a private preview address that
        only you have. Read every page on your phone and on a computer, with your engineers.
        Two rounds of changes are included.</p></li>
      <li><h3>Weeks 7 to 8. Accessibility audit and go live</h3><p>Contrast and accessibility
        audit, link check, speed check, then we point swiftheat.co.in at the new site, enable
        HTTPS, submit the sitemap, and map the old pages so no existing link breaks.</p></li>
    </ol>

    <div class="wrap">
      <h2>What we need from you</h2>
      <p>We want to be direct about this, because content is what slows these projects down,
        not building. The list is not long but it is real.</p>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h3>Before we start</h3>
        <ul>
          <li>Your correct registered address, confirmed against the two we found</li>
          <li>Real phone numbers, and a WhatsApp number if you want that option</li>
          <li>The email address enquiries should reach</li>
          <li>Your logo as a vector file: AI, EPS, PDF or SVG. Only a small image exists
            online today.</li>
          <li>The final product list, including whether immersion heaters and control
            systems are in or out</li>
          <li>The year Swiftheat was founded</li>
        </ul>
      </div>
      <div class="card">
        <h3>Before we can launch</h3>
        <ul>
          <li><strong>Photographs.</strong> Two to four clean shots per product family, at
            least one of each installed on a machine, plus your plant, machinery, assembly
            and test bench.</li>
          <li><strong>Specification ranges per family:</strong> diameters, lengths, wattage
            and voltage ranges, sheath materials, watt density, maximum temperatures,
            tolerances, thermocouple types, termination and lead options, clamping styles.</li>
          <li><strong>Testing detail:</strong> which tests, on what equipment, at what stage,
            what is recorded, and what the customer receives.</li>
          <li><strong>Certificates and numbers:</strong> ISO, MSME or Udyam, GST, CIN.</li>
          <li>Any existing catalogues, datasheets or brochures, including old files and
            printed scans.</li>
          <li>The industries and customers you actually supply, and any export markets.</li>
        </ul>
      </div>
    </div>

    <div class="wrap">
      <h2>On photography</h2>
      <p>You shoot these yourselves, and there is no photographer to hire. We send a shot
        list and a one page guide before you start.</p>
      <p>A recent phone is enough. What actually matters is not the camera, it is the
        light and the background. Daylight from a shutter or a doorway beats the overhead
        tube lights on a shop floor, a plain sheet of paper or cloth behind the part removes
        the clutter, and shiny metal needs light bounced off a white surface rather than
        pointed straight at it, or it glares. The guide covers all of that, plus the angles
        we need per family, how to include something for scale, and the minimum size to
        shoot at.</p>
      <p>Set aside an afternoon and one person who knows the products. That is genuinely the
        whole requirement.</p>
      <p>What will not work is stock photography of somebody else's heaters. You actually
        manufacture, and the only way a website shows that is with real pictures of your real
        products and your real factory. A slightly imperfect photograph of your own coil
        heater on your own bench is worth more here than a perfect photograph of a heater that
        is not yours.</p>

      <h2>How we handle content that has not arrived</h2>
      <p>Where a specification or a certificate is outstanding, we mark it clearly as
        outstanding on the preview and we do not invent a value to fill the gap. If content is
        still outstanding past an agreed date, the build clock pauses rather than the scope
        quietly shrinking. We would rather have that conversation early than hand you a site
        with placeholder text on it, which is the position you are in today.</p>
    </div>

    <div class="quiet">
      <p><strong>After go live.</strong> The site is yours. The code, the content and the
        domain stay in your name, and you can take it to anyone. There is no licence, no
        lock in and no monthly platform fee. The annual care plan described in the next
        section is optional, and it is a service, not a hostage.</p>
    </div>
"""

BODIES["04-investment.html"] = """
    <div class="chapter"><span class="num" aria-hidden="true">04</span>
      <div><p class="eyebrow">Section four</p><h1>The investment</h1></div></div>
    <div class="wrap">
      <p class="lede">One price for the whole thing. No phases, no modules, no upgrade path
        you have to buy later to make the site work, and nothing else to procure.</p>
    </div>

    <div class="price">
      <p class="figure">Rs 65,000<small>One time, for the complete website described in this
        proposal. Includes the first year of the annual care plan, so there is nothing further
        to pay in year one. GST not applicable.</small></p>
      <hr>
      <h3>What that covers</h3>
      <ul class="linelist">
        <li><b>All eight sections, twenty three pages</b><span>Included</span></li>
        <li><b>Seven product family pages, built as datasheets</b><span>Included</span></li>
        <li><b>Nine industry pages with heating zone tables</b><span>Included</span></li>
        <li><b>Specification driven enquiry form, per product family</b><span>Included</span></li>
        <li><b>Downloadable datasheet, one per product family</b><span>Included</span></li>
        <li><b>Construction cutaways and dimension drawings, drawn by us</b><span>Included</span></li>
        <li><b>Photography shot list and guide, so you can shoot it yourselves</b><span>Included</span></li>
        <li><b>Quality and testing section built as evidence</b><span>Included</span></li>
        <li><b>Bangalore and Peenya search coverage</b><span>Included</span></li>
        <li><b>Structured data, sitemap, per page titles and descriptions</b><span>Included</span></li>
        <li><b>WCAG 2.1 AA accessibility audit</b><span>Included</span></li>
        <li><b>Hosting, HTTPS, domain cutover and go live</b><span>Included</span></li>
        <li><b>Old site archived, existing links mapped</b><span>Included</span></li>
        <li><b>Two rounds of changes at preview</b><span>Included</span></li>
        <li><b>Annual care plan, first year</b><span>Included</span></li>
      </ul>
      <hr>
      <p style="margin-bottom:0">From year two, the care plan renews at <strong
        style="color:#fff">Rs 12,000 per year</strong>. It is optional and you can stop it at
        any time without losing the site.</p>
    </div>

    <div class="wrap">
      <h2>There is nothing else to buy</h2>
      <p>Most website quotes are followed by three more: a photographer, a copywriter and
        somebody to draw the diagrams. We have deliberately not built this proposal that way.
        You would end up briefing four suppliers, holding four schedules and paying four
        invoices, for a website.</p>
      <p>Everything this site needs, you already have inside the company or we produce
        ourselves. Here is the honest division of labour.</p>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h3>What comes from you</h3>
        <ul>
          <li><strong>The technical substance.</strong> Diameters, lengths, wattage and
            voltage ranges, sheath materials, watt density, temperatures, tolerances,
            thermocouple types, termination and clamping options. Your engineers already know
            all of this. Rough notes, a marked up old catalogue or a phone call is enough. It
            does not need to be written well, it needs to be correct.</li>
          <li><strong>The photographs.</strong> Taken by you, on a recent phone. We send a
            shot list and a one page guide covering angles, how to light metal so it does not
            glare, what to stand the parts on and what size to shoot at. What makes these
            photographs work is that they are your real products and your real factory, not
            that a studio took them.</li>
          <li><strong>The proof.</strong> Certificates, test records, a sample test report,
            the industries and customers you actually supply.</li>
          <li><strong>One engineer's sign off.</strong> Somebody who knows heaters reads every
            specification and every drawing before it is published.</li>
        </ul>
      </div>
      <div class="card">
        <h3>What we do with it</h3>
        <ul>
          <li><strong>Write and structure every page</strong> from your notes and your
            existing catalogue text. You will not be asked to produce finished copy.</li>
          <li><strong>Draw the construction cutaways, the dimension drawings and the option
            diagrams</strong> for each product family, then send them to your engineer to
            check.</li>
          <li><strong>Build, design, and make it findable:</strong> the structure, the
            enquiry form, the search work, the accessibility audit, the speed, the hosting.</li>
          <li><strong>Never invent a number.</strong> Anything not yet confirmed appears on
            the preview marked clearly as outstanding, in a colour you cannot miss, until you
            confirm it. Nothing unverified is published.</li>
        </ul>
      </div>
    </div>

    <div class="wrap">
    </div>

    <div class="finding">
      <span class="tag">Why this is worth having</span>
      <p>One supplier, one price, one schedule. Nothing on your website will be waiting on a
        photographer's calendar, and nothing will be published that your own people have not
        read and confirmed.</p>
    </div>

    <div class="wrap">
      <h2>The annual care plan</h2>
      <p>Included for the first year, Rs 12,000 a year after that. Seven things, itemised so
        you know exactly what it is.</p>
      <ul>
        <li>Hosting, the HTTPS certificate and DNS management</li>
        <li>Uptime monitoring, so we know before you do</li>
        <li>Off site backups with a one click rollback</li>
        <li>Security patching of the build toolchain</li>
        <li><strong>Six content updates a year:</strong> a new product, revised
          specifications, new photographs, a new download</li>
        <li>A defined response time when something breaks</li>
        <li>An annual report on site health and search visibility</li>
      </ul>


      <h2>Terms</h2>
    </div>

    <div class="tablewrap">
      <table>
        <caption>Commercial terms</caption>
        <thead><tr><th scope="col">Item</th><th scope="col">Terms</th></tr></thead>
        <tbody>
          <tr><td>Payment</td><td>40 percent to begin, 40 percent on preview approval, 20 percent at go live</td></tr>
          <tr><td>Timeline</td><td>Six to eight weeks from receipt of your content</td></tr>
          <tr><td>Changes</td><td>Two rounds included at preview. Further rounds Rs 5,000 each.</td></tr>
          <tr><td>Scope</td><td>Seven product families, nine industries, as listed in section two</td></tr>
          <tr><td>Beyond that scope</td><td>Additional product family page Rs 6,000. Additional industry page Rs 4,000. Both at your option, never assumed.</td></tr>
          <tr><td>Later changes</td><td>Rs 1,500 per hour, once the care plan allowance for the year is used</td></tr>
          <tr><td>Ownership</td><td>The site, the code and the domain are yours. No licence, no lock in.</td></tr>
          <tr><td>GST</td><td>Not applicable</td></tr>
        </tbody>
      </table>
    </div>

    <div class="wrap">
      <h2>The next step</h2>
      <p>If this reads right to you, reply and say so, and we will send a one page scope note
        confirming everything above for your records. We will also send the content checklist
        from section five as a simple list you can forward to whoever holds the specifications
        and the certificates.</p>
      <p>If you would rather talk it through first, we are happy to come to Peenya. Seeing the
        plant would improve the site anyway, and it is the fastest way to work out what the
        photography should show.</p>
      <p>One thing regardless of what you decide: the phone number on your current contact
        page is a placeholder. That one is worth fixing this week.</p>
      <p style="margin-top:32px">
        <a class="btn" href="mailto:propagetech@gmail.com?subject=Swiftheat%20website%20proposal">Reply to this proposal</a>
      </p>
      <p style="color:var(--ink-600);font-size:.9rem">ProPage, +91 9945 62 1717</p>
    </div>
"""

out = pathlib.Path("proposal")
for href, short, sub in PAGES:
    title = ("Swiftheat website proposal" if href == "index.html"
             else "%s | Swiftheat website proposal" % short)
    page = SHELL.format(
        title=html.escape(title),
        descr=html.escape(DESCR[href]),
        navitems=nav(href),
        body=BODIES[href].rstrip(),
        pagerhtml=pager(href),
    )
    (out / href).write_text(page, encoding="utf-8")
    print("wrote %-26s %6d bytes" % (href, len(page)))
