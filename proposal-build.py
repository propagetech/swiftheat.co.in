#!/usr/bin/env python3
"""Generates the Swiftheat proposal pages. One shell, seven bodies."""
import html, pathlib

PAGES = [
    ("index.html",              "Proposal",              "Swiftheat website proposal"),
    ("01-where-you-stand.html", "Where you stand today", "What your website does right now"),
    ("02-being-found.html",     "How buyers find you",   "Search visibility and where enquiries go"),
    ("03-competitors.html",     "The two sites you sent","Nexthermal, Electron Systems, the wider field"),
    ("04-what-we-build.html",   "What we will build",    "Structure, product pages, industry pages"),
    ("05-plan.html",            "How the work runs",     "Phases, timeline and what we need"),
    ("06-investment.html",      "The investment",        "Rs 65,000, and why that is the number"),
]

DESCR = {
 "index.html":"Website redesign proposal for Swiftheat Thermal Technologies, Peenya, Bangalore. Prepared by ProPage.",
 "01-where-you-stand.html":"An audit of swiftheat.co.in as it stands in August 2026, and what it is costing in enquiries.",
 "02-being-found.html":"How Swiftheat is found in search today, why IndiaMART outranks the website, and the unclaimed Peenya searches.",
 "03-competitors.html":"A close read of Nexthermal and Electron Systems, the two competitor sites Swiftheat asked us to review.",
 "04-what-we-build.html":"The proposed structure: seven product family pages, nine industry pages, and an enquiry form that asks for a specification.",
 "05-plan.html":"The five phases of the build, the timeline, and the content and photography we need from Swiftheat.",
 "06-investment.html":"Rs 65,000 for the complete build, set against published Indian market pricing for a custom manufacturer website.",
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
      <p class="lede">Before writing this proposal we read your current website in full,
        then more than twenty five competitor websites: heater manufacturers in Bangalore,
        the strongest names across India, and the international leaders in Germany, the
        United States and Ireland. Everything in this document is a verified observation,
        not an opinion about design.</p>
      <hr class="rule">
      <p>Four findings shaped the entire proposal.</p>
    </div>

    <div class="kpis">
      <div class="kpi"><b>0</b><span>Indian heater manufacturers, local or national, whose enquiry form asks for a single specification</span></div>
      <div class="kpi"><b>0</b><span>Bangalore manufacturers whose own website appears for Peenya heater searches</span></div>
      <div class="kpi"><b>1 in 17</b><span>Indian heater sites that name the electrical tests they perform</span></div>
      <div class="kpi"><b>0</b><span>Indian heater sites that publish a lead time or a minimum order quantity</span></div>
    </div>

    <div class="wrap">
      <p>That is the shape of the opportunity. This is not a market where you have to be
        cleverer than everyone else. It is a market where almost nobody has done the
        straightforward work of telling an engineer what they need to know.</p>

      <h2>How this proposal is ordered</h2>
      <p>Each section earns the next one. We start with what exists, then what it is costing
        you, then what your competitors do and fail to do, then what we would build, how it
        runs, and only at the end, what it costs.</p>
    </div>

    <ol class="steps">
      <li>
        <h3><a href="01-where-you-stand.html">Where you stand today</a></h3>
        <p>An audit of swiftheat.co.in as it is right now, including three faults that are
          turning away enquiries this week.</p>
      </li>
      <li>
        <h3><a href="02-being-found.html">How buyers find you</a></h3>
        <p>Why IndiaMART is currently acting as your homepage, what happens when someone
          searches for heater manufacturers in Peenya, and one domain name issue you should
          know about.</p>
      </li>
      <li>
        <h3><a href="03-competitors.html">The two sites you sent us</a></h3>
        <p>A close read of Nexthermal and Electron Systems, what each does better than the
          other, and where both leave the door open.</p>
      </li>
      <li>
        <h3><a href="04-what-we-build.html">What we will build</a></h3>
        <p>Seven product family pages, nine industry pages, and an enquiry form that asks
          your customer for a diameter instead of a paragraph. Includes a
          <a href="mockup/cartridge-heaters.html">working mockup of a product page</a>.</p>
      </li>
      <li>
        <h3><a href="05-plan.html">How the work runs</a></h3>
        <p>Five phases, six to eight weeks, and an honest list of what we need from your side
          before we can start and before we can launch.</p>
      </li>
      <li>
        <h3><a href="06-investment.html">The investment</a></h3>
        <p>Rs 65,000 for the complete build, set against what the Indian market actually
          charges for a manufacturer website of this size.</p>
      </li>
    </ol>

    <div class="quiet">
      <p><strong>One promise about content.</strong> We publish only what you send us and can
        verify. No invented certifications, no borrowed photographs, no claims about years or
        clients or export markets that we cannot stand behind. If a useful claim cannot be
        supported, it does not go on the site.</p>
    </div>
"""

BODIES["01-where-you-stand.html"] = """
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
        <a href="05-plan.html">how the work runs</a>.</p>

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

BODIES["02-being-found.html"] = """
    <div class="chapter"><span class="num" aria-hidden="true">02</span>
      <div><p class="eyebrow">Section two</p><h1>How buyers find you</h1></div></div>
    <div class="wrap">
      <p class="lede">A website that cannot be found is a brochure in a drawer. Three things
        are happening in search right now, and two of them are working against you.</p>
      <hr class="rule">
    </div>

    <div class="finding">
      <span class="tag">Finding 1</span>
      <p><strong>Your own website does not appear when someone searches for Swiftheat.</strong>
        The results are your IndiaMART listing, Zauba Corp, IndiaMART product pages,
        peenya.info and Justdial. In practice, IndiaMART is acting as your homepage.</p>
      <p>That matters commercially. On IndiaMART your listing sits next to competitors, the
        enquiry is shared, and you have no control over how your company is presented. You are
        paying for that placement in one form or another. Your own domain is free and it is
        yours.</p>
    </div>

    <div class="finding">
      <span class="tag">Finding 2, not a website matter</span>
      <p><strong>swiftheat.com belongs to a different company.</strong> It is Swift Heat and
        Control, and their product range is close to identical to yours: cartridge heaters,
        mica and ceramic band heaters, nozzle heaters, coil heaters, thermocouples and RTDs.
        Anyone who types the obvious .com address lands on a competitor.</p>
      <p>We raise it because you should know, not because it is part of this project. It may
        be worth checking whether that domain can be acquired, separately from the website.</p>
    </div>

    <div class="wrap">
      <h2>Peenya is unclaimed</h2>
      <p>This is the finding we would build the site around. We ran the searches a buyer in
        Bangalore would actually run and recorded what came back.</p>
    </div>

    <div class="tablewrap">
      <table>
        <caption>What currently ranks for heater searches with a Bangalore or Peenya qualifier</caption>
        <thead><tr><th scope="col">Search</th><th scope="col">What appears</th><th scope="col">Read</th></tr></thead>
        <tbody>
          <tr class="is-us"><td>band heater manufacturers Peenya Bangalore</td>
            <td>IndiaMART, then two pages from a <strong>Pune</strong> company, then five Justdial listings</td>
            <td>Not one Bangalore manufacturer's own website appears at all</td></tr>
          <tr><td>ceramic band heater manufacturers Bangalore</td>
            <td>A <strong>Pune</strong> company first, then an IndiaMART built site, then Electron Systems</td>
            <td>A Pune firm outranks every Bangalore manufacturer</td></tr>
          <tr><td>cartridge heater manufacturers in Bangalore</td>
            <td>SRI Electronics, Heatcon, Electron Systems</td>
            <td>Own sites do win here. An exact page title is enough.</td></tr>
          <tr><td>industrial heater manufacturers in Bangalore</td>
            <td>Sulekha directory first, then Heatcon and Electron Systems</td>
            <td>A directory takes the top position</td></tr>
        </tbody>
      </table>
    </div>

    <div class="wrap">
      <p>Read the first row again. You manufacture heaters in Peenya Industrial Area Phase 1.
        When a buyer searches for exactly that, they are shown directories and a company in
        Pune. There is no Bangalore manufacturer's website in the way, because none of them
        has built the page.</p>
      <p>The second row is the same story with a different query. A company several hundred
        kilometres away is winning a Bangalore search because they wrote a Bangalore page and
        your neighbours did not.</p>

      <h2>What we would target</h2>
      <p>These are the searches the new site would be built to answer. Each one maps to a
        single page with a single job, which is how search engines prefer it.</p>
    </div>

    <div class="tablewrap">
      <table>
        <caption>Target searches and the page that would answer each</caption>
        <thead><tr><th scope="col">Search</th><th scope="col">Page that answers it</th><th scope="col">Currently held by</th></tr></thead>
        <tbody>
          <tr><td>heater manufacturers in Peenya industrial area</td><td>Home and Contact</td><td>Nobody. Directories only.</td></tr>
          <tr><td>cartridge heater manufacturers in Bangalore</td><td>Cartridge Heaters</td><td>Three local firms, all beatable</td></tr>
          <tr><td>ceramic band heater manufacturers Bangalore</td><td>Ceramic Band Heaters</td><td>A Pune company</td></tr>
          <tr><td>mica band heater manufacturers in Bangalore</td><td>Mica Band Heaters</td><td>A Pune company and Justdial</td></tr>
          <tr><td>hot runner nozzle heater manufacturers Bangalore</td><td>Nozzle Heaters</td><td>Thin coverage locally</td></tr>
          <tr><td>strip heater manufacturers in Bangalore</td><td>Strip Heaters</td><td>Directories only</td></tr>
          <tr><td>tubular heater manufacturers in Bangalore</td><td>Tubular Heaters</td><td>Fragmented, no clear owner</td></tr>
          <tr><td>ceramic infrared heater manufacturers Bangalore</td><td>Ceramic IR Heaters</td><td>Low local depth</td></tr>
          <tr class="is-us"><td>extruder barrel heater Bangalore, injection moulding machine heater supplier Bangalore</td>
            <td>The industry pages</td><td><strong>Nobody.</strong> No competitor has application led pages.</td></tr>
          <tr class="is-us"><td>custom cartridge heater as per drawing Bangalore</td>
            <td>Custom Solutions and the enquiry form</td><td><strong>Nobody targets this.</strong></td></tr>
        </tbody>
      </table>
    </div>

    <div class="quiet">
      <p><strong>A note on honesty in search.</strong> We do not buy links, spin articles or
        publish machine written city pages. Two of the firms currently ranking against you do
        exactly that, and one of them still has placeholder testimonials from a fictional
        company on its homepage. Our approach is slower and it holds: one page, one subject,
        written properly, marked up so Google can read the specifications.</p>
    </div>
"""

BODIES["03-competitors.html"] = """
    <div class="chapter"><span class="num" aria-hidden="true">03</span>
      <div><p class="eyebrow">Section three</p><h1>The two sites you sent us</h1></div></div>
    <div class="wrap">
      <p class="lede">You pointed us to Nexthermal and Electron Systems, and said Electron
        is the more appropriate of the two. We had already audited both. There is something
        important in that judgement, and it is worth separating it from the thing it is
        easily mistaken for.</p>
      <hr class="rule">
      <p><strong>What is right about Electron Systems is what it says, not how it is built.</strong>
        Somebody who understands heaters wrote those words. The diameter and length matrix,
        the fit calculation, the instruction telling a buyer exactly which four things to
        state when ordering: that is a manufacturer talking to an engineer, and almost nobody
        else in this market does it. That instinct is correct and we would build on it.</p>
      <p><strong>What is wrong with it is the structure and the presentation, and we would not
        repeat either.</strong> The navigation is a flat list of thirteen products with
        "ISO Certificate" sitting in the menu beside them. There is no way in for a buyer who
        thinks in terms of their machine rather than a product name, because there are no
        application pages. The catalogue mixes heaters with hopper dryers, sealing machines
        and welding mirrors, so the company reads as a general supplier rather than a heater
        manufacturer. The specifications are strewn through bullet prose: the cartridge page
        contains two tables in total. There is nothing to download, no enquiry form on the
        product pages, a gmail address for contact, a copyright line reading 2018, and a
        setting that stops a visitor pinch zooming on a phone.</p>
      <p>So the honest summary is this. Electron shows the right respect for the buyer's
        question and then buries the answer in a layout that cannot carry it. Swiftheat should
        take the respect and discard the layout.</p>
    </div>

    <div class="finding">
      <span class="tag">Rather than describe it</span>
      <p>Section four sets out the page we would build instead. Because that is difficult to
        picture from a description, we have built one.
        <a href="mockup/cartridge-heaters.html"><strong>Open the cartridge heater page
        mockup</strong></a>. It is a real page, not a picture of one: the tables, the drawings,
        the coded option catalogue and a working enquiry form that shows you the email
        Swiftheat would receive.</p>
    </div>

    <h2>Electron Systems</h2>
    <div class="grid grid-2">
      <div class="card">
        <h3>What they get right</h3>
        <ul>
          <li>A <strong>page for each product</strong>, with a page title written for the
            search a buyer actually types: "Cartridge heater manufacturers in Bangalore".</li>
          <li>A real <strong>diameter and length matrix</strong>: 6.5, 8, 10, 12.5, 16, 19
            and 25 mm against imperial equivalents, with minimum lengths from 35 to 75 mm
            and maximums from 250 to 1500 mm.</li>
          <li>A worked <strong>fit calculation</strong>, with a numeric example arriving at
            0.18 mm maximum permissible clearance, plus mounting bore guidance of 0.15 to
            0.30 mm.</li>
          <li>An explicit instruction to the buyer: <em>when ordering please specify
            diameter and length, wattage and voltage, type of terminal, and a drawing for
            special configurations.</em></li>
        </ul>
      </div>
      <div class="card">
        <h3>What they throw away</h3>
        <ul>
          <li>Having told the buyer exactly which four things to state, <strong>they give
            them a blank message box.</strong> The specification never reaches the sales desk
            in a usable form.</li>
          <li><strong>Nothing to download.</strong> No catalogue, no datasheet, no drawing,
            anywhere on the site.</li>
          <li>The product pages carry <strong>no enquiry form at all</strong>. The buyer has
            to go and find the contact page.</li>
          <li>The contact address is a <strong>gmail.com address</strong>, not a company one.</li>
          <li>The footer reads <strong>Copyright 2018</strong>.</li>
          <li>The cartridge page sets <code>user-scalable=0</code>, which
            <strong>stops a visitor pinch zooming on a phone</strong>. For an engineer
            trying to read a dimension table on a shop floor, that is a real problem, and it
            is an accessibility failure.</li>
        </ul>
      </div>
    </div>

    <h2>Nexthermal</h2>
    <div class="grid grid-2">
      <div class="card">
        <h3>What they get right</h3>
        <ul>
          <li><strong>Five downloadable PDFs</strong>, including a full cartridge catalogue,
            an abbreviated catalogue, an installation and operation guide, a configuration
            chart and their ISO certificate. They are the only manufacturer in Bangalore who
            offers a buyer anything to take away.</li>
          <li>Genuine <strong>engineering options written out</strong>: distributed wattage,
            moisture resistance, removal aids, right angle exits and blocks, flanges and NPT
            fittings, anti seize, and a centreless grind tolerance of plus or minus
            0.0008 inches.</li>
          <li>Real <strong>part numbered product photography</strong>, shot properly.</li>
          <li>A frequently asked questions block on the product page itself.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Where they leave the door open</h3>
        <ul>
          <li>It is the Indian arm of a company in Battle Creek, Michigan, and it reads that
            way. There is <strong>almost no Bangalore or Karnataka signal</strong> anywhere on
            the site. They do not compete for local searches.</li>
          <li>Their enquiry form asks name, email, phone, company, subject and message.
            <strong>No specification, no drawing upload</strong>, despite all that catalogue
            depth sitting one click away.</li>
          <li>Their live cartridge heater page still contains <strong>unedited placeholder
            marketing text</strong>, sitting between two real technical sections. It reads:
            "Credibly innovate granular internal sources whereas high standards
            Energistically scale future-proof core competencies vis-a-vis impactful
            experiences."</li>
        </ul>
      </div>
    </div>

    <div class="wrap">
      <p>We mention that last point without any pleasure, because your own site has the same
        problem. It is worth knowing that the most technically credible heater website in
        Bangalore has been shipping nonsense text on a live product page for some time and
        nobody has caught it. The bar here is lower than it looks.</p>

      <h2>Side by side</h2>
    </div>

    <div class="tablewrap">
      <table>
        <caption>The two sites you sent, your current site, and what we propose</caption>
        <thead><tr><th scope="col">Capability</th><th scope="col">Electron Systems</th>
          <th scope="col">Nexthermal</th><th scope="col">Swiftheat today</th>
          <th scope="col">Swiftheat proposed</th></tr></thead>
        <tbody>
          <tr><td>Page per product family</td><td>Yes</td><td>Yes</td><td>No, one combined page</td><td class="is-us">Yes, seven</td></tr>
          <tr><td>Specification tables</td><td>Partly, two tables</td><td>In PDFs only</td><td>No</td><td class="is-us">Yes, on every family page</td></tr>
          <tr><td>Dimension drawings</td><td>No</td><td>In PDFs only</td><td>No</td><td class="is-us">Yes</td></tr>
          <tr><td>Coded option catalogue</td><td>No</td><td>Written as prose</td><td>No</td><td class="is-us">Yes, coded and diagrammed</td></tr>
          <tr><td>Downloadable datasheets</td><td>None</td><td>Five PDFs</td><td>None</td><td class="is-us">One per family</td></tr>
          <tr><td>Enquiry form asks for specifications</td><td>No</td><td>No</td><td>No</td><td class="is-us">Yes, per product family</td></tr>
          <tr><td>Industry or application pages</td><td>No</td><td>Four, US written</td><td>No</td><td class="is-us">Nine, written for your industries</td></tr>
          <tr><td>Quality and testing content</td><td>ISO page</td><td>ISO certificate PDF</td><td>None</td><td class="is-us">Named tests, rig photos, sample certificate</td></tr>
          <tr><td>Targets Bangalore and Peenya searches</td><td>Bangalore yes, Peenya no</td><td>No</td><td>No</td><td class="is-us">Both</td></tr>
          <tr><td>Works properly on a phone</td><td>Zoom blocked</td><td>Yes</td><td>Partly</td><td class="is-us">Yes, and audited to WCAG 2.1 AA</td></tr>
        </tbody>
      </table>
    </div>

    <div class="wrap">
      <h2>The wider field, in case it is useful</h2>
      <p>We did not stop at these two. We read the strongest heater manufacturer websites
        across India, then the international leaders: Watlow and Tempco in the United States,
        Hotset, Elstein and Turk plus Hillinger in Germany, and Ceramicx in Ireland.</p>
      <p>Two things stood out.</p>
      <p><strong>In India, looking modern and being useful are almost unrelated.</strong>
        The most useful Indian heater site to a buying engineer, after Tempsens in Udaipur,
        is Excel Heaters in Mumbai, and it looks like it was built in 2004. Its order forms
        are built around a dimensioned drawing and capture diameter, length, voltage, wattage,
        hole positions, slot radius, lead length and quantity. Meanwhile the sites that look
        current tell an engineer nothing. Almost nobody has done both.</p>
      <p><strong>The international leaders are beatable on industry pages.</strong> We
        expected their application pages to be excellent. They are not. Chromalox's plastics
        page is a banner image, one paragraph and a single case study. Elstein's thermoforming
        page has no diagram, no numbers and no product links. This is genuinely open ground,
        not just in Bangalore but anywhere.</p>
    </div>

    <div class="quiet">
      <p><strong>What we would take from each.</strong> From Electron Systems, the instinct
        that a product page exists to answer an engineer's question, and their habit of telling
        the buyer exactly what to specify. From Nexthermal, downloadable collateral and real
        product photography. From Excel Heaters in Mumbai, the dimensioned order form. From
        Tempco in the United States, the coded and diagrammed option catalogue. Then we add the
        two things none of them have: an enquiry form that captures the specification, and
        industry pages that show the heating zones on the machine.</p>
    </div>
"""

BODIES["04-what-we-build.html"] = """
    <div class="chapter"><span class="num" aria-hidden="true">04</span>
      <div><p class="eyebrow">Section four</p><h1>What we will build</h1></div></div>
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
      <p>This is the piece that does the most work. The structure below is drawn from the
        best pages we found anywhere in the world, chiefly Elstein in Germany, Watlow and
        Tempco in the United States. No Indian heater manufacturer publishes a page like
        this today.</p>
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
        and a line on when to use it. <strong>This is the single strongest thing on the
        page and nobody in India has one.</strong></p></li>
      <li><h3>Selection guidance</h3><p>How to choose a watt density for the application,
        and how to size the heater. Electron Systems publishes a fit calculation and it is
        one of the best things on their site. We would do the same, better.</p></li>
      <li><h3>Installation and failure modes</h3><p>Common causes of premature failure and
        how to avoid them. In this category, telling a buyer how your product fails is the
        most credible thing you can do.</p></li>
      <li><h3>Applications, downloads, related products, enquiry</h3><p>Cards linking to the
        relevant industry pages, the datasheet PDF, adjacent families, and an enquiry form
        already scoped to this product.</p></li>
    </ol>

    <div class="wrap">
      <h2>The industry page</h2>
      <p>Nine of these, one per industry in your brief. As noted earlier, the international
        leaders do this badly, which makes it open ground. The centre of each page is a table
        that maps the machine to your products.</p>
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
      <p>The most valuable thing in this proposal, and the cheapest to explain. Today, every
        heater manufacturer in India asks a customer for a name, a phone number and a message.
        Your form will ask for a heater.</p>
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
        Cloudflare's global network with HTTPS. Two of the international leaders we tested
        failed to load fully. Speed is a competitive advantage in this category.</p></div>
      <div class="card"><h3>Readable by machines</h3><p>Schema.org structured data marks up
        your company, your products and your specifications, so Google and the newer AI
        search tools can read them properly rather than guessing.</p></div>
      <div class="card"><h3>Accessible, and audited</h3><p>WCAG 2.1 AA, checked with a real
        contrast audit rather than claimed. Every tap target at least 44 pixels. Pinch zoom
        works, unlike on two of the sites currently outranking you.</p></div>
      <div class="card"><h3>Nothing borrowed from elsewhere</h3><p>Fonts served from your own
        site, no tracking scripts, no cookie banner needed because there are no cookies to
        consent to.</p></div>
      <div class="card"><h3>Look and feel</h3><p>Two registers held together: your factory
        and your products photographed honestly, and a dry, precise datasheet treatment for
        the technical pages. Industrial, not decorative.</p></div>
    </div>
"""

BODIES["05-plan.html"] = """
    <div class="chapter"><span class="num" aria-hidden="true">05</span>
      <div><p class="eyebrow">Section five</p><h1>How the work runs</h1></div></div>
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
      <p>Two workable routes, and the choice is yours.</p>
      <p><strong>You shoot it.</strong> A recent phone, a plain background, daylight from a
        window rather than overhead tube lights, and we give you a shot list and a short guide
        with examples. This works better than people expect and it costs nothing.</p>
      <p><strong>We arrange a photographer.</strong> Half a day at Peenya covering all seven
        families plus the plant, priced separately at cost, in the range of Rs 25,000 to
        45,000 depending on who is available.</p>
      <p>What will not work is stock photography of somebody else's heaters. Your advantage
        over the trading companies in this market is that you actually manufacture, and the
        only way a website shows that is with real pictures of your real factory.</p>

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

BODIES["06-investment.html"] = """
    <div class="chapter"><span class="num" aria-hidden="true">06</span>
      <div><p class="eyebrow">Section six</p><h1>The investment</h1></div></div>
    <div class="wrap">
      <p class="lede">One price for the whole thing. No phases, no modules, no upgrade path
        you have to buy later to make the site work.</p>
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
      <h2>Why Rs 65,000, and not less</h2>
      <p>We did not pick this number from a price list. We checked what Indian agencies
        publish for a manufacturer website of this size, and set our price below the market
        floor for it. Here is the whole picture, including the parts that make us look
        expensive.</p>
    </div>

    <div class="tablewrap">
      <table>
        <caption>Published Indian and international pricing for business and manufacturer
          websites, 2026. Sources are agency price pages and published project figures.</caption>
        <thead><tr><th scope="col">What you are buying</th><th scope="col" class="num-cell">Published price</th>
          <th scope="col">What it actually is</th></tr></thead>
        <tbody>
          <tr><td>Bangalore budget package</td><td class="num-cell">Rs 12,999 to 16,999</td>
            <td>Five to seven pages on a bought template, text swapped in</td></tr>
          <tr><td>India, basic informational site</td><td class="num-cell">Rs 15,000 to 40,000</td>
            <td>Template based. Published definitions exclude a product catalogue.</td></tr>
          <tr><td>Manufacturing site, template</td><td class="num-cell">Rs 25,000 to 75,000</td>
            <td>Five to ten pages, basic customisation, minimal search work</td></tr>
          <tr class="is-us"><td><strong>This proposal</strong></td><td class="num-cell"><strong>Rs 65,000</strong></td>
            <td><strong>Twenty three pages, custom designed, hand built, accessibility audited</strong></td></tr>
          <tr><td>Manufacturing site, custom, published floor</td><td class="num-cell">Rs 85,000 to 1,80,000</td>
            <td>Eight to twelve pages, product galleries, contact forms</td></tr>
          <tr><td>Manufacturing site, semi custom</td><td class="num-cell">Rs 1,00,000 to 2,50,000</td>
            <td>Fifteen to thirty pages, product catalogue, technical content, quote forms.
              <strong>This is the tier our page count falls into.</strong></td></tr>
          <tr><td>Real Indian project, automotive component supplier</td><td class="num-cell">Rs 2,07,000</td>
            <td>Published 2025 project figure, development plus content</td></tr>
          <tr><td>Real Indian project, industrial valve manufacturer</td><td class="num-cell">Rs 5,50,000</td>
            <td>Published 2025 project figure</td></tr>
          <tr><td>Same site built in the United Kingdom</td><td class="num-cell">Rs 8.9 to 27.8 lakh</td>
            <td>Custom design, twelve to twenty five pages</td></tr>
          <tr><td>Same site built in the United States</td><td class="num-cell">Rs 6.2 to 15.8 lakh</td>
            <td>Small to mid size manufacturer, custom</td></tr>
        </tbody>
      </table>
    </div>

    <div class="finding">
      <span class="tag">The comparison that matters most</span>
      <p>ExportersIndia sells manufacturers and exporters a <strong>template</strong> website
        at <strong>Rs 60,000 every year, recurring</strong>. This proposal is Rs 65,000 once,
        for a site designed only for you, that you own outright, and that nobody can switch
        off. The difference in year two is Rs 60,000 against Rs 12,000.</p>
    </div>

    <div class="wrap">
      <h2>If someone quotes you Rs 20,000</h2>
      <p>Someone will, and they will be quoting honestly for a different product. In the
        Indian market's own published definitions, the ten to twenty five thousand band means
        a purchased template with your text dropped into it, and those definitions
        specifically exclude a product catalogue. That is a real service and for some
        businesses it is the right one. It is not what your brief describes.</p>
      <p>Three things worth weighing before comparing the two numbers.</p>
      <ul>
        <li><strong>The cheap quote is rarely the cheap cost.</strong> Add the domain,
          hosting at three to fifteen thousand a year, premium theme and plugin licences, and
          a WordPress maintenance contract at ten to thirty thousand a year. The Indian
          guidance on this is blunt: a twelve thousand rupee website that has to be rebuilt in
          eighteen months costs more than a forty five thousand rupee one that runs for five
          years.</li>
        <li><strong>You have already run this experiment.</strong> Your current WordPress site
          has had a placeholder phone number and Latin filler text live on it for around two
          years. The problem was never that the platform could not be edited. It is that
          nobody edits it. A site with no plugins to patch and six updates a year included
          fails differently.</li>
        <li><strong>Your buyers are procurement engineers.</strong> Some of them are comparing
          you against German and American suppliers whose websites cost between six and
          twenty eight lakh rupees. A template reads as a template to that reader.</li>
      </ul>

      <h2>Optional, only if you want them</h2>
      <p>None of these are needed for the site described in this proposal to work. They are
        priced here so there are no surprises later.</p>
    </div>

    <div class="tablewrap">
      <table>
        <caption>Optional additions</caption>
        <thead><tr><th scope="col">Item</th><th scope="col" class="num-cell">Price</th></tr></thead>
        <tbody>
          <tr><td>Product and factory photography, half day at Peenya, all seven families</td>
            <td class="num-cell">Rs 25,000 to 45,000, photographer billed at cost</td></tr>
          <tr><td>Technical copywriting of specification content, working with your engineers</td><td class="num-cell">Rs 18,000</td></tr>
          <tr><td>Drawn set: construction cutaways and dimension drawings, per family</td><td class="num-cell">Rs 4,500 each</td></tr>
          <tr><td>Heater sizing and watt density calculator on the site</td><td class="num-cell">Rs 15,000</td></tr>
          <tr><td>Technical knowledge base, six written articles</td><td class="num-cell">Rs 24,000</td></tr>
          <tr><td>Additional product family page beyond seven</td><td class="num-cell">Rs 6,000 each</td></tr>
          <tr><td>Additional industry page beyond nine</td><td class="num-cell">Rs 4,000 each</td></tr>
          <tr><td>Changes beyond the care plan allowance</td><td class="num-cell">Rs 1,500 per hour</td></tr>
          <tr><td>Third and further rounds of changes at preview</td><td class="num-cell">Rs 5,000 per round</td></tr>
        </tbody>
      </table>
    </div>

    <div class="wrap">
      <h2>The annual care plan</h2>
      <p>Included for the first year, Rs 12,000 a year after that. We should be straight
        about what it is, because the hosting itself is nearly free and you would be right to
        ask. You are not paying us for server space. You are paying for these seven things.</p>
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
      <p>For comparison, Indian agencies publish annual maintenance for a site of this kind at
        Rs 18,000 to 30,000, and specifically for manufacturing sites at Rs 10,000 to 25,000.</p>

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
          <tr><td>Scope</td><td>Seven product families, nine industries, as listed in section four</td></tr>
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
      <p>And whether or not we work together: please change the phone number on your contact
        page this week. It costs nothing and it is currently sending every caller nowhere.</p>
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
