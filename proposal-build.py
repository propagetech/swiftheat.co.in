#!/usr/bin/env python3
"""Generates the Swiftheat proposal pages. One shell, seven bodies."""
import html, pathlib

# The preview address. Everything in the proposal that points at the built site
# reads from here, so moving the preview is a one line change.
#
# Note what this is: GitHub Pages on a public repository. It is unlisted, not
# private. There is no password, because GitHub Pages cannot do one. What keeps
# it out of Google is the noindex on every page, set by PREVIEW_NOINDEX in
# build/data.py. Do not describe it to the client as private.
PREVIEW = "https://propagetech.github.io/swiftheat.co.in"

PAGES = [
    ("index.html",             "Proposal",             "Swiftheat website proposal"),
    ("01-what-we-found.html",  "What we found",        "The inputs the build starts from"),
    ("02-what-we-build.html",  "What we built",        "Structure, product pages, industry pages"),
    ("03-plan.html",           "Where it stands",      "What is done, what is left before launch"),
    ("04-investment.html",     "The investment",       "Rs 65,000, and what it covers"),
]

DESCR = {
 "index.html":"Website redesign proposal for Swiftheat Thermal Technologies, Peenya, Bangalore. Prepared by ProPage.",
 "01-what-we-found.html":"What the current swiftheat.co.in contains, where Swiftheat stands in search, and what the Bangalore competitor field does and does not do.",
 "02-what-we-build.html":"The delivered structure: eight product family pages, nine industry pages, and an enquiry form that asks for a specification.",
 "03-plan.html":"What is built, and the short list still outstanding before swiftheat.co.in can be switched over.",
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
    <p class="rail-meta">Website build<br>Swiftheat Thermal Technologies<br>Built 26 August 2026</p>
    <button class="railtoggle" type="button" aria-expanded="true" aria-controls="contents">Contents</button>
    <nav id="contents" aria-label="Proposal contents">
      <p class="rail-title">In this document</p>
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
      <p class="eyebrow">Website build, ready for your review</p>
      <h1>The heater is made to a drawing. The website should be too.</h1>
      <p>A redesign of swiftheat.co.in built around the one thing your buyer is actually
        trying to do: describe a heater precisely enough to get a price. It is built. This
        document is now the record of what was delivered, and of the short list still
        standing between it and go live.</p>
      <dl class="meta">
        <div><dt>Prepared for</dt><dd>Rekha Prabhu, Swiftheat Thermal Technologies Pvt Ltd</dd></div>
        <div><dt>Prepared by</dt><dd>ProPage</dd></div>
        <div><dt>Proposed</dt><dd>25 August 2026</dd></div>
        <div><dt>Built</dt><dd>26 August 2026, awaiting your approval</dd></div>
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
      <p><a href="{preview}/"><strong>Open the site</strong></a>. All twenty six pages, on a
        working address that is not linked from anywhere and is kept out of Google. Read it on
        your phone and on a computer, and get an engineer to read the product pages.</p>
      <p><a href="{preview}/build-a-list/"><strong>Open the heater list builder</strong></a>.
        Pick a heater, set the sizes, tap the options, add it to the list. Build up as many
        lines as you need, then generate a document you can save as a PDF, email or send on
        WhatsApp. Your sales team can use the same tool to build a list on a customer's
        behalf.</p>
      <p><a href="{preview}/products/cartridge-heaters/"><strong>Open the cartridge heater
        page</strong></a>. Specification tables, a construction cutaway, a dimensioned
        drawing, your ordering options set out with codes, and an enquiry form that shows you
        the email your works would receive. The dimensions and lead ratings on it came off
        your own brochure. The values still marked "to confirm" are the ones we are waiting on
        from your engineers, and they are the reason this is a preview and not a launch.</p>
    </div>

    <div class="wrap">
      <p>Twenty six pages, all to the same standard. Eight product families, nine
        industries, your custom work and capabilities, your quality and testing, your
        downloads, and an enquiry form that asks a customer for a diameter rather than a
        paragraph.</p>

      <h2>What is in this document</h2>
    </div>

    <ol class="steps">
      <li>
        <h3><a href="01-what-we-found.html">What we found</a></h3>
        <p>What your current site contains and what was worth keeping. Then the research:
          where you stand in search today, what the eight Bangalore competitors with their own
          site do and do not do, and the thirteen gaps none of them fill.</p>
      </li>
      <li>
        <h3><a href="02-what-we-build.html">What we built</a></h3>
        <p>The full structure, how a product page is put together, how an industry page
          works, and the enquiry form in detail.</p>
      </li>
      <li>
        <h3><a href="03-plan.html">Where it stands</a></h3>
        <p>What is finished, what arrived from you on 26 August, and the straight list of
          what is still outstanding before swiftheat.co.in can be switched over.</p>
      </li>
      <li>
        <h3><a href="04-investment.html">The investment</a></h3>
        <p>Rs 65,000 for the complete build, what that covers, and the terms.</p>
      </li>
    </ol>

    <div class="quiet">
      <p><strong>One promise about content, and we kept it.</strong> We publish only what you
        send us and can verify. No invented certifications, no borrowed photographs, no claims
        about years or clients we cannot stand behind. Everything still unconfirmed is on the
        preview marked as outstanding, in a colour you cannot miss. That is why the preview has
        visible gaps in it: they are honest gaps, and section three lists every one.</p>
    </div>
"""

BODIES["01-what-we-found.html"] = """
    <div class="chapter"><span class="num" aria-hidden="true">01</span>
      <div><p class="eyebrow">Section one</p><h1>Where you stand today</h1></div></div>
    <div class="wrap">
      <p class="lede">swiftheat.co.in runs on WordPress with the Elementor page builder,
        hosted at Hostinger. Every image on it was uploaded in June or July 2024. There are
        four pages: Home, About Us, Products and Contact Us. The second half of this section
        is the competitor and search research, which is where most of the build decisions
        came from.</p>
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
        currently working from the first one.</p>
      <p><em>Updated 26 August.</em> Your printed brochure gives a third: No. C-205, 2nd Floor,
        4th Cross, Peenya 1st Stage. So there are now three plots on record rather than two,
        and this is still the first thing we need confirmed.</p>
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
      <p>That material is a real head start. We edited it up and built on it rather than
        starting from a blank page.</p>
    </div>

    <div class="wrap">
      <hr class="rule">
      <h2>Where you stand in search</h2>
      <p>We read every Bangalore competitor site live, plus seventeen national manufacturers
        and a shortlist of the best in the world, in August 2026. Two findings came out of it
        that matter more than anything on your current site.</p>
    </div>

    <div class="finding">
      <span class="tag">Finding 1</span>
      <p><strong>Swiftheat does not rank for its own name.</strong> Searching the brand
        returns Zauba Corp, your IndiaMART profile, IndiaMART product pages, peenya.info and
        Justdial. <code>swiftheat.co.in</code> did not surface at all.</p>
      <p><strong>Your IndiaMART listing is currently your homepage in search.</strong> Every
        enquiry that starts with your name is being handed to a lead broker who also sells
        your competitors the same enquiry.</p>
    </div>

    <div class="finding">
      <span class="tag">Finding 2, and it is not a website problem</span>
      <p><strong><code>swiftheat.com</code> belongs to a different company.</strong> Swift
        Heat &amp; Control, with a near identical product line: cartridge, mica and ceramic
        band, nozzle, coil heaters, thermocouples and RTDs. Anyone who guesses the .com lands
        on a competitor.</p>
      <p>We cannot fix that with a website and we are not suggesting you buy the domain. We
        are telling you because it is worth a commercial decision at your end, and because
        nobody had told you.</p>
    </div>

    <div class="wrap">
      <h2>The local field, as it actually is</h2>
      <p>Eight Bangalore manufacturers with their own site. The last two columns are the ones
        that matter.</p>
    </div>

    <div class="tablewrap">
      <table>
        <caption>Bangalore industrial heater manufacturers, read live August 2026</caption>
        <thead><tr><th scope="col">Company</th><th scope="col">Area</th>
          <th scope="col">Downloads</th><th scope="col">Form asks for a specification?</th></tr></thead>
        <tbody>
          <tr><td>Nexthermal India</td><td>Gerupalaya</td><td>4 PDFs, cartridge only</td><td>No</td></tr>
          <tr><td>Technobel Heating Solutions</td><td>Attibele</td><td>None</td><td>No</td></tr>
          <tr><td>Heatcon Sensors</td><td>Hessarghatta</td><td>None</td><td>No</td></tr>
          <tr><td>Electron Systems</td><td>Sunkadakatte</td><td>None</td><td>No</td></tr>
          <tr><td>SRI Electronics</td><td>Nandini Layout</td><td>None</td><td>No form at all</td></tr>
          <tr><td>Sushma Heaters</td><td>Yeshwantpur</td><td>None</td><td>IndiaMART widget</td></tr>
          <tr><td>TMH Heating Technologies</td><td>Kamakshipalya</td><td>None</td><td>IndiaMART widget</td></tr>
          <tr><td>India Heaters</td><td>Banashankari</td><td>None</td><td>IndiaMART widget</td></tr>
        </tbody>
      </table>
    </div>

    <div class="wrap">
      <p>Three of the eight are IndiaMART built microsites. One ships downloadable
        collateral, and only for one product family. <strong>Not one form in the entire
        local field asks a buyer for a diameter.</strong></p>
      <p>Two more things worth knowing. On the query <em>ceramic band heater manufacturers
        Bangalore</em>, a Pune company outranks every Bangalore manufacturer. On <em>band
        heater manufacturers Peenya Bangalore</em>, no Bangalore manufacturer's own site
        appears at all: only directories and out of town firms farming your city's
        enquiries.</p>
    </div>

    <div class="finding">
      <span class="tag">The single highest value gap</span>
      <p><strong>Nobody claims Peenya.</strong> Searches for heater manufacturers in Peenya
        return Justdial and companies in Pune and Delhi. Not one manufacturer's own site
        targets Peenya, Rajajinagar, Bommasandra, Jigani or Hosur Road.</p>
      <p>You are physically in Peenya 1st Stage. That is the cheapest ground on this list to
        take, and it is the reason Peenya appears in the page titles, the descriptions and the
        structured data on the new site rather than only in the footer.</p>
    </div>

    <div class="wrap">
      <h2>Thirteen things nobody in the local field does</h2>
      <p>We checked each of these across every competitor. The right hand column is what the
        new site does about it, which is where most of the build decisions came from.</p>
    </div>

    <div class="tablewrap">
      <table>
        <caption>Gaps in the local field, and the answer built into your site</caption>
        <thead><tr><th scope="col">Nobody does this</th><th scope="col">Your site</th></tr></thead>
        <tbody>
          <tr><td>No form anywhere asks for diameter, length, wattage, voltage, sheath or
            terminal type</td><td>Specification driven enquiry, per product family, plus the
            requirement list builder</td></tr>
          <tr><td>No drawing or sample upload, in an industry whose sales motion is "send us
            a drawing"</td><td>Enquiry form accepts a drawing</td></tr>
          <tr><td>Almost no downloadable collateral a buyer could forward to
            purchasing</td><td>A datasheet per product family</td></tr>
          <tr><td>Specs written as prose, not tables. One competitor's cartridge page has no
            table at all</td><td>Specification tables with units on every family page</td></tr>
          <tr><td>No dimensional drawings on any competitor product page</td><td>Dimensioned
            drawings and construction cutaways, drawn for each family</td></tr>
          <tr><td>Peenya and the Bangalore industrial corridor unclaimed</td><td>Peenya in
            titles, descriptions and structured data</td></tr>
          <tr><td>Certifications asserted, never shown</td><td>Nothing claimed until the
            certificate is supplied. Currently marked outstanding.</td></tr>
          <tr><td>No proof of manufacture. A buyer cannot tell a maker from a
            trader</td><td>Factory and process photography, which is the outstanding item in
            section three</td></tr>
          <tr><td>No application led entry point. Everything organised by product
            type</td><td>Nine industry pages, each mapping the machine to the element</td></tr>
          <tr><td>Two of the top ranking local sites block pinch zoom</td><td>WCAG 2.1 AA
            audited, no horizontal overflow from 360 pixels up</td></tr>
          <tr><td>Visible content rot at the top of the market: filler copy, lorem ipsum
            testimonials, a 2020 copyright</td><td>Nothing published that is not
            verified</td></tr>
          <tr><td>No lead time, minimum order or delivery commitment stated
            anywhere</td><td>Ready to state once you confirm the numbers</td></tr>
          <tr><td>No sizing or watt density guidance</td><td>Selection guidance and failure
            modes on every family page</td></tr>
        </tbody>
      </table>
    </div>

    <div class="wrap">
      <h2>What we measured your site against</h2>
      <p>Not against the local field, because the local field is a low bar. Two other
        reference points went into this.</p>
      <p><strong>Seventeen Indian manufacturers, to find the median.</strong> A typical
        Indian heater manufacturer site in 2026 runs a rotating hero, product pages of 150 to
        400 words with specs as prose, an ISO badge that is a photograph of a certificate, and
        one contact form asking name, email, phone and message. Above that median means a
        downloadable catalogue, a named industry list, and specs as numbers with units. Your
        site clears the median on every count. At the bottom of that set, one manufacturer
        with a genuine TUV Austria certification ships live lorem ipsum and has no enquiry
        form at all.</p>
      <p><strong>Nine of the best in the world, to set the ceiling.</strong> Tempco in the
        United States for the deepest coded option taxonomy in the category, which is where
        your seventy six option codes come from. Watlow for engineering calculators and
        industry led structure. Hotset in Germany for completely ungated downloads, which is
        why your datasheets ask for nothing. Thermocoax in France for how quality and
        traceability should be presented. Ceramicx in Ireland for real factory photography.
        Backer in Sweden for a product finder that searches by article number.</p>
      <p>We are not pretending a Rs 65,000 site matches Watlow. The point of reading them was
        to take the specific mechanics that work at that level and that a small manufacturer
        can actually maintain: coded options, specs as tables, ungated downloads, and industry
        pages that start from the machine rather than the product.</p>
    </div>

    <div class="quiet">
      <p><strong>On the research itself.</strong> Sites were read live in August 2026 from
        their published markup. Search positions came from a non Bangalore index, so exact
        rankings should be rechecked from a local connection before anyone treats them as a
        target. The pattern held across five separate queries, which is what we are relying
        on rather than any single position.</p>
    </div>
"""

BODIES["02-what-we-build.html"] = """
    <div class="chapter"><span class="num" aria-hidden="true">02</span>
      <div><p class="eyebrow">Section two</p><h1>What we built</h1></div></div>
    <div class="wrap">
      <p class="lede">Every section in your brief, plus the three things the audit says are
        unclaimed: a specification driven enquiry, product pages built like datasheets, and
        an industry page for each of the nine industries you named.</p>
      <hr class="rule">
      <h2>The structure</h2>
      <p>Eight sections, containing twenty six pages.</p>
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
      <div class="card"><h3>Products</h3><p>An overview page plus <strong>eight family
        pages</strong>: cartridge, coil, ceramic and mica band, ceramic and mica nozzle,
        strip, tubular, thermocouples and sensors, ceramic infrared. Four of those eight are
        awaiting your confirmation, see section three.</p></div>
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
        contact form asks for a name, a phone number and a message. Your form asks for a
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
      <div><p class="eyebrow">Section three</p><h1>Where it stands</h1></div></div>
    <div class="wrap">
      <p class="lede">The build is finished and published to a working address that is not
        linked from anywhere and is kept out of search. Nothing has touched swiftheat.co.in,
        and nothing will until you approve it. What is left is content that only you can
        supply, and it is a short list.</p>
      <hr class="rule">
    </div>

    <div class="kpis">
      <div class="kpi"><b>26</b><span>Pages built</span></div>
      <div class="kpi"><b>8</b><span>Product families</span></div>
      <div class="kpi"><b>9</b><span>Industry pages</span></div>
      <div class="kpi"><b>76</b><span>Coded options published</span></div>
    </div>

    <div class="wrap">
      <h2>What is done</h2>
    </div>

    <ol class="steps">
      <li><h3>Structure and design</h3><p>Twenty six pages, one stylesheet, self hosted
        fonts, no third party trackers. The look was set on the home page and the cartridge
        heater page first, then applied across the rest.</p></li>
      <li><h3>Product and industry pages</h3><p>Eight family pages built as datasheets, with
        specification tables, construction cutaways, dimensioned drawings and coded ordering
        options. Nine industry pages, each with a heating zone table that maps the machine to
        the element type.</p></li>
      <li><h3>The requirement list builder</h3><p>Built and tested. A customer picks a
        heater, sets sizes, chooses coded options and generates a document to print, email or
        send on WhatsApp. Nothing is stored and no account is needed. It carries a live
        drawing that redraws on every change.</p></li>
      <li><h3>Your brochure, mined and applied</h3><p>The write up and the two brochure
        photographs you sent on 26 August went straight in. Cartridge diameters 6.35 to
        25.4 mm and both watt density classes. Nine thermocouple types where the old site
        claimed two. The washer, lug, bolt, spring loaded, mineral insulated and manifold
        ranges. Lead temperature limits by insulation. One hundred percent calibration,
        Class 1 and Class A. Your mission and vision, in your words.</p></li>
      <li><h3>Your logo, in vector for the first time</h3><p>No vector file exists, so the
        625 pixel image was traced into one and the masthead carries it. The site palette was
        then retuned to your logo red, since it had been built before we had the logo.</p></li>
      <li><h3>Accessibility and quality checks</h3><p>WCAG 2.1 AA contrast audit passing on
        2,172 text elements across thirteen pages. No horizontal overflow from 360 to 1440
        pixels wide. One hundred automated tests on the list builder, all passing.</p></li>
    </ol>

    <div class="wrap">
      <h2>What is outstanding</h2>
      <p>Split honestly into the items that stop us launching and the items that can follow
        after. Every one is content, not building.</p>
    </div>

    <div class="tablewrap">
      <table>
        <caption>Outstanding items, in the order they block the launch</caption>
        <thead><tr><th scope="col">Item</th><th scope="col">What we need</th>
          <th scope="col">Why it blocks</th></tr></thead>
        <tbody>
          <tr><td><strong>Photographs</strong></td>
            <td>Two to four clean shots per family, at least one installed on a machine, plus
              plant, machinery, assembly and test bench</td>
            <td>Forty nine places on the site carry a marked placeholder instead of a
              photograph. This is the largest single gap by a wide margin.</td></tr>
          <tr><td><strong>Your address</strong></td>
            <td>Which plot a courier reaches you at today</td>
            <td>Three different plots are on record and your brochure introduced a third.
              It goes on every page, in your map pin and in your search listing.</td></tr>
          <tr><td><strong>Enquiry email</strong></td>
            <td>Confirm the address enquiries should reach</td>
            <td>Your brochure gives rekha@ and sales@ and never mentions info@, which is what
              the site uses. If info@ is not a live mailbox, web enquiries are being lost
              right now.</td></tr>
          <tr><td><strong>Phone numbers</strong></td>
            <td>Which of the two brochure numbers is the sales line, and which takes
              WhatsApp</td>
            <td>We have 9108803706 and 8553002014 from your brochure but publish neither
              until it has been dialled and answered.</td></tr>
          <tr><td><strong>Final product list</strong></td>
            <td>A yes or no on Ceramic Infrared, Nozzle, Strip and Tubular heaters</td>
            <td>Those four have pages, but they appear in neither your write up nor your
              brochure. We will not sell a family you do not make.</td></tr>
          <tr><td><strong>Domain access</strong></td>
            <td>Registrar login for swiftheat.co.in, or the ability to change nameservers</td>
            <td>Required to point the domain at the new site. The domain currently sits at
              Hostinger.</td></tr>
        </tbody>
      </table>
    </div>

    <div class="tablewrap">
      <table>
        <caption>Wanted, but the site can launch without them</caption>
        <thead><tr><th scope="col">Item</th><th scope="col">What we need</th></tr></thead>
        <tbody>
          <tr><td>Performance figures</td><td>Maximum sheath temperature, maximum watt density
            and tolerances per family. Nine places still read "to confirm".</td></tr>
          <tr><td>Heater testing detail</td><td>Which tests, on what equipment, at what stage,
            recorded against what. Your sensor calibration is already published because the
            brochure states it; the heater equivalent is not.</td></tr>
          <tr><td>Certificates</td><td>ISO if you hold one, Udyam or MSME, GST. Numbers and
            certificates, not claims. Nothing appears until the document does.</td></tr>
          <tr><td>Logo artwork</td><td>AI, EPS, PDF or SVG. Our trace works, but a trace of a
            625 pixel image is a copy of a copy.</td></tr>
          <tr><td>Print ready brochure</td><td>The PDF or source file your printer was given.
            It goes in Downloads, and it very likely contains the logo artwork above.</td></tr>
          <tr><td>Specification sign off</td><td>One engineer to read every specification
            table and every drawing before it is published.</td></tr>
        </tbody>
      </table>
    </div>

    <div class="finding">
      <span class="tag">Two decisions, not deliveries</span>
      <p><strong>The four unevidenced families.</strong> Confirm them and they stay as built.
        Tell us they are out and we remove them, redirect the addresses and tidy the
        navigation, at no cost. Tell us they are bought in rather than made, and we say so on
        the page, the way the coil heater page now says the element is German made.</p>
      <p><strong>Your applications list.</strong> Your write up names nine. Two of them,
        hot runner systems and laboratories, have no page. Two pages we built, blow moulding
        and die and mould, are not on your list. Confirm which nine you want.</p>
    </div>

    <div class="wrap">
      <h2>What the photographs need to be</h2>
      <p><strong>Coverage.</strong> Two to four shots of each product family, and at least
        one of each family fitted on a machine or in the application. Separately, the plant
        itself: machinery, winding, assembly, and the test bench.</p>
      <p><strong>Technical.</strong> Minimum 2000 pixels on the long edge. In focus, evenly
        lit, and on a plain uncluttered background for the product shots.</p>
      <p><strong>Two things we cannot use.</strong> Stock photography of somebody else's
        heaters: your old site carried a cartridge heater image with a Chinese manufacturer's
        watermark still on it, and reverse image search makes that trivial to spot. And your
        own brochure photographs, which are yours but sit at roughly 200 to 400 pixels once
        cropped out of a printed page. They show us what to expect, but they are not usable
        at the size the site needs.</p>

      <h2>If you would rather launch sooner</h2>
      <p>There is a middle path, and it is your call rather than ours. We can launch on the
        four items that are pure fact, which is the address, the email, the phone and the
        product list, and hold back the pages that lean hardest on photography until the
        photographs exist. You would go live with fewer pages that are all complete, instead
        of waiting for every page to be complete at once.</p>
      <p>It costs nothing either way and it changes no part of the price. Say which you
        prefer.</p>
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
      <p class="lede">One price for the whole thing, unchanged from the proposal. No phases,
        no modules, no upgrade path you have to buy later to make the site work, and nothing
        else to procure.</p>
    </div>

    <div class="price">
      <p class="figure">Rs 65,000<small>One time, for the complete website as built.
        Includes the first year of the annual care plan, so there is nothing further to pay in
        year one. GST not applicable. The proposal miscounted the product families as seven
        while listing eight; eight were always the scope and eight were built, at no
        change to this figure.</small></p>
      <hr>
      <h3>What that covers</h3>
      <ul class="linelist">
        <li><b>All eight sections, twenty six pages</b><span>Included</span></li>
        <li><b>Eight product family pages, built as datasheets</b><span>Included</span></li>
        <li><b>Nine industry pages with heating zone tables</b><span>Included</span></li>
        <li><b>Specification driven enquiry form, per product family</b><span>Included</span></li>
        <li><b>Downloadable datasheet, one per product family</b><span>Included</span></li>
        <li><b>Construction cutaways and dimension drawings, drawn by us</b><span>Included</span></li>
        <li><b>Quality and testing section built as evidence</b><span>Included</span></li>
        <li><b>Bangalore and Peenya search coverage</b><span>Included</span></li>
        <li><b>Structured data, sitemap, per page titles and descriptions</b><span>Included</span></li>
        <li><b>WCAG 2.1 AA accessibility audit</b><span>Included</span></li>
        <li><b>Hosting, HTTPS, domain cutover and go live</b><span>Included</span></li>
        <li><b>Old site archived, existing links mapped</b><span>Included</span></li>
        <li><b>Changes at preview</b><span>Included</span></li>
        <li><b>Annual care plan, first year</b><span>Included</span></li>
      </ul>
      <hr>
      <p><strong style="color:#fff">You pay nothing until the site is live.</strong> No
        deposit, no stage payments, nothing on approval. The full amount falls due when
        swiftheat.co.in is switched over and you have confirmed it is working. If it never goes
        live, you never pay, and the work already done costs you nothing.</p>
      <p style="margin-bottom:0">From year two, the care plan renews at <strong
        style="color:#fff">Rs 12,000 per year</strong>. It is optional and you can stop it at
        any time without losing the site.</p>
    </div>

    <div class="wrap">
      <h2>What is in the price</h2>
      <p>Most website quotes are followed by two more: a copywriter and somebody to draw the
        diagrams. We deliberately did not run this project that way. Every page was written
        here, and every cutaway, dimension drawing and option diagram was drawn here. Neither
        is a separate invoice and neither is a separate schedule.</p>
      <p>Photography is the one input that is yours rather than ours. The specification is in
        section three.</p>
      <p>All twenty six pages are built and the whole of the right hand column below is
        finished. Here is the honest division of labour, and where it now stands.</p>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h3>What still comes from you</h3>
        <ul>
          <li><strong>The photographs.</strong> The one item that has not moved, and the one
            that sets the launch date. Two to four per family, one of each in application,
            plus the plant. Minimum 2000 pixels, in focus, plain background.</li>
          <li><strong>The rest of the technical substance.</strong> Your brochure covered more
            than we expected: cartridge diameters, the thermocouple ranges, the lead
            temperature limits, your calibration classes. All of that is published. What is
            still missing is the performance side, which is maximum sheath temperature,
            maximum watt density and tolerances per family. Nine cells still read "to
            confirm". Rough notes or a phone call is enough; it does not need to be written
            well, it needs to be correct.</li>
          <li><strong>The proof.</strong> Certificates, test records, a sample test report,
            the industries and customers you actually supply.</li>
          <li><strong>One engineer's sign off.</strong> Somebody who knows heaters reads every
            specification and every drawing before it is published. The drawings are drawn and
            waiting for exactly this.</li>
        </ul>
      </div>
      <div class="card">
        <h3>What we did with it</h3>
        <ul>
          <li><strong>Wrote and structured all twenty six pages</strong> from your brochure,
            your write up and your old catalogue text. You were not asked to produce a line of
            finished copy, and you will not be.</li>
          <li><strong>Drew the construction cutaways, the dimension drawings and the option
            diagrams</strong> for all eight product families. They are on the pages now,
            waiting for your engineer to check rather than waiting to be drawn.</li>
          <li><strong>Built, designed and made it findable:</strong> the structure, the
            enquiry form, the requirement list builder, the search work, the structured data,
            the hosting. The accessibility audit passes WCAG 2.1 AA on 2,172 text elements,
            and one hundred automated tests pass on the list builder.</li>
          <li><strong>Traced your logo into vector,</strong> which had never existed, and
            retuned the site palette to your own red rather than the placeholder we started
            with.</li>
          <li><strong>Never invented a number.</strong> Every value we could not verify is on
            the preview marked as outstanding, in a colour you cannot miss. That is why the
            gaps are visible: they are honest gaps, and section three lists every one.</li>
        </ul>
      </div>
    </div>

    <div class="wrap">
    </div>

    <div class="finding">
      <span class="tag">Why this is worth having</span>
      <p>One supplier, one price, one schedule. Nothing has been published that your own
        people have not read and confirmed, which is the whole reason the remaining gaps are
        visible rather than filled with something plausible.</p>
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
          <tr><td>Payment</td><td>Nothing until go live. The full Rs 65,000 falls due when swiftheat.co.in is switched over to the new site and you have confirmed it is working.</td></tr>
          <tr><td>Timeline</td><td>The build is complete. Go live follows 5 to 10 working days after the outstanding items in section three reach us.</td></tr>
          <tr><td>Scope</td><td>Eight product families, nine industries, as listed in section two and as delivered</td></tr>
          <tr><td>Later changes</td><td>Rs 1,500 per hour, once the care plan allowance for the year is used</td></tr>
          <tr><td>GST</td><td>Not applicable</td></tr>
        </tbody>
      </table>
    </div>

    <div class="wrap">
      <h2>The next step</h2>
      <p>Read the preview, with an engineer alongside you for the product pages. Then reply
        with three things and we can move.</p>
      <ol>
        <li><strong>Your approval of the build</strong>, or the changes you want.</li>
        <li><strong>The six items in the first table of section three.</strong> Address,
          enquiry email, which phone is the sales line, a yes or no on the four unconfirmed
          product families, the photographs, and registrar access for the domain.</li>
        <li><strong>Whether you want to launch complete or launch sooner</strong>, as set out
          at the end of section three.</li>
      </ol>
      <p>Approval and the first four of those six can come back in one reply. The photographs
        are the item with a real lead time, so if only one thing happens this week, let it be
        an afternoon with a phone camera.</p>
      <p>Nothing about this reply commits you to a payment. The invoice follows go live, not
        approval, so you are free to take as long over the review as it needs.</p>
      <p>If you would rather talk it through first, a call is easiest. Phone or WhatsApp,
        whichever suits you, and we can settle the photography list on the same call.</p>
      <p>One thing worth doing regardless: send a test email to info@swiftheat.co.in from an
        outside address and see whether it arrives. Your brochure does not list it, the old
        site did, and if it is dead then enquiries have been going nowhere.</p>
      <p style="margin-top:32px">
        <a class="btn" href="mailto:propagetech@gmail.com?subject=Swiftheat%20website%20approval%20for%20go%20live">Approve the build</a>
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
        body=BODIES[href].rstrip().replace("{preview}", PREVIEW),
        pagerhtml=pager(href),
    )
    (out / href).write_text(page, encoding="utf-8")
    print("wrote %-26s %6d bytes" % (href, len(page)))

if "github.io" in PREVIEW:
    print("\nNote: PREVIEW points at GitHub Pages, which is unlisted but public and has\n"
          "      no password. The only thing keeping it out of search is PREVIEW_NOINDEX\n"
          "      in build/data.py. Confirm that is True and pushed before sending links.")
