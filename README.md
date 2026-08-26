# swiftheat.co.in

Website for **Swiftheat Thermal Technologies Pvt Ltd**, industrial heater
manufacturer, Plot C-262, 6th Cross, Peenya Industrial Area 1st Phase,
Bangalore 560058.

Built to the ProPage house standard: hand written semantic HTML, one stylesheet
and one script, self hosted woff2 fonts, WCAG 2.1 AA audited, schema.org
structured data, path portable relative URLs, static hosting on Cloudflare Pages.

## The site

Twenty seven pages, generated into the repository root.

| Path | Pages |
| --- | --- |
| `index.html` | Home |
| `products/` | Overview with a faceted finder, plus **eight family pages** |
| `applications/` | Overview, plus **nine industry pages** |
| `about/`, `capabilities/`, `quality/`, `resources/`, `contact/` | Company pages |
| `build-a-list/` | The heater requirement list builder |
| `404.html`, `robots.txt`, `sitemap.xml`, `favicon.svg` | Supporting files |

Assets: `css/site.css` and `css/bom.css`, `js/site.js` and `js/bom.js`,
`fonts/` (five self hosted woff2 faces), `icons/` (eight Noun Project concept
icons, credited in `icons/CREDITS.md`), `imgs/` (the logo in vector, plus seven
accessory photographs recovered from the old site).

### Structure of a product family page

Breadcrumb, hero with headline specification chips, an action bar above the
fold, construction and why it matters, a temperature scale, the technical data
table, dimensions with a drawing, **the coded option catalogue**, selection
guidance, failure modes, applications, downloads, related products, and an
enquiry form already scoped to the family. Seventy six option codes are
published across the eight families, and every code is the same code the list
builder puts on a requirement document.

### Structure of an industry page

Hero, a process flow diagram with every heated zone called out and coloured by
temperature, the **zone by zone table** mapping the machine to the element type,
a curated product shortlist, application notes, a "what to send us" checklist,
and a scoped enquiry form. The process diagram and the zone table are the two
things no site in the international benchmark set publishes.

## Building it

    python3 site-build.py

Never edit the generated HTML: it is overwritten on every run. Everything the
site says lives in `build/`:

| File | What it holds |
| --- | --- |
| `build/data.py` | Every published fact: families, options, industries, zones, enquiry fields |
| `build/chrome.py` | Page shell, navigation, footer, and the shared components |
| `build/render.py` | The product family page and the industry page |
| `build/pages.py` | Home, the two overviews, and the company pages |
| `build/art/*.svg` | One drawing per family, extracted from the list builder |
| `build/extract-art.mjs` | Regenerates `build/art/` from the builder |
| `build/noun-search.py` | Searches the Noun Project, lists only CC BY and public domain results |
| `build/noun-icons.py` | Fetches the chosen icons, traces, crops and recolours them into `icons/` |
| `build/prep-imgs.py` | Knocks the background out of the old site's accessory photographs into `imgs/` |
| `build/logo-svg.py` | Traces Swiftheat's logo into `imgs/swiftheat-logo.svg`, two colours, one coordinate system |

Two rules govern `build/data.py`:

1. **Nothing is asserted about Swiftheat that Swiftheat has not supplied.**
   Size ranges come from the specification agreed in the proposal. Performance
   figures (temperature, watt density, tolerances) render as "To confirm" until
   the client's engineers confirm them. Every one of those markers has to be
   cleared before go live.
2. **Industry data is the single source of truth for applications.** A product
   page can only claim an industry that names it in a zone or on its shortlist,
   so the two directions cannot disagree.

## Icons and imagery

Concept icons are Noun Project, CC BY 3.0 only, traced from the published PNG
with `potrace`, cropped to the artwork and recoloured to `--heat-700`. Eight of
them, on Home, Capabilities and Quality. Attribution rides on every `title=`
plus a consolidated comment per page, and `icons/CREDITS.md` is the index.
Regenerate with:

    python3 build/noun-icons.py

They are decorative: every one is `alt=""` and each card says the same thing in
words, so a blocked image costs nothing.

### The seven accessory photographs

`imgs/` holds seven small photographs taken from the old site's Products page
and used in the option catalogue: right angle exit (T2), round flange (M1),
threaded fitting (M2), the three lead protections (L1, L3, L4) and the coiled
tubular form (BC). `build/prep-imgs.py` knocks the studio background out to
transparency and trims the margin, so they sit on the card rather than on a
white rectangle.

They earn their place because they are shown at 104 px tall, which is inside
what a 214 to 435 px original can carry, and because those option groups had no
imagery at all. **Provenance is still unconfirmed.** None of the seven carries a
watermark, but a file uploaded in the same batch does, so Swiftheat should
confirm these are theirs before go live. They are the only raster images on the
site; pull them by deleting the fifth element from the option tuples in
`build/data.py`.

### The logo

Swiftheat have no vector logo. Three rasters of the same artwork exist: a
625 x 208 PNG in the old site's media library, a 535 x 180 JPEG the client sent
on 26 Aug 2026, and the impression printed on their brochure. `build/logo-svg.py`
traces the largest into `imgs/swiftheat-logo.svg` and the masthead carries that.

It is a trace of their artwork, not a redesign: the slab serif letterforms, the
flame, the two rules that swap colour across it, and the two colours are all
theirs. The colours are raw `#0000ff` and `#ff0000`, sampled off the source,
which is what a logo drawn in an office application looks like. Published as
found rather than tidied, because it is their mark and not ours to restyle.

The site palette answers the logo rather than the other way round. The accent
ramp in `css/site.css` was rust orange while the logo was still unknown; it is
now that logo red deepened into something usable on screen, and the ink ramp was
already the navy that answers the logo blue. Red at a given lightness is darker
than orange, so `--heat-700`, `--heat-600` and `--heat-400` all gained contrast
in the move. `--heat-500` went the other way: every text use of it sits on a
dark surface, and the palest of those is the photograph placeholder rather than
`--ink-900`, so it is lightened and pushed to full saturation to stay a red
rather than drifting to salmon. The contrast audit is the gate on all of it.

Regenerate with:

    python3 build/logo-svg.py

Ask the client for AI, EPS, PDF or SVG anyway. A trace of a 625 px raster is a
copy of a copy, and the brochure's print ready file is the likeliest place the
real curves survive.

### Photography is still the blocker

Nothing else from the old site can be used. `archive-old-site/PROVENANCE.md` has
the detail: `Cartridge-Heaters-2.png` carries a competitor's **DETAI** watermark,
the family group shots are generic trade catalogue photography, and the largest
original on the whole site is 835 px. Every place a real photograph belongs
carries a dashed placeholder with the shot written into it.

## Checking it

Serve it:

    python3 -m http.server 8123

Contrast, from the working folder root:

    node ../_rebuild-kit/tools/contrast-audit.mjs http://127.0.0.1:8123 / /products/ /products/cartridge-heaters/ /applications/injection-moulding/ /contact/

Links and anchors:

    python3 ../_rebuild-kit/tools/linkcheck.py .

The builder has its own suite of 100 cases in `tests/`, which currently runs
against the frozen copy inside `proposal/`. `site-build.py` prints a note when
the live `js/bom.js` and `css/bom.css` have drifted from that copy.

## Also in this repository

| Path | What it is |
| --- | --- |
| `proposal/` | Seven page client proposal, generated by `proposal-build.py`. A dated sales artefact, not part of the finished site. |
| `proposal/mockup/` | The mockup the proposal was sold on. Frozen. |
| `archive-old-site/` | The previous WordPress site as found on 25 Aug 2026: four pages plus every uploaded image at original resolution. |
| `tests/` | Playwright suite for the list builder. |

Internal research, pricing reasoning and the internal quotation are **not** in
this repository. They live in `docs/` in the working folder and are gitignored.

## Before go live

Confirmed since the first build, from Swiftheat's own IndiaMART profile and the
MCA registry, and now published:

- Founded **August 2021**, so no "decades of experience" claim can be made
- **11 to 25 people**
- CIN **U29100KA2021PTC150780**

Still blocking, and all of them are marked in the pages as "to confirm":

1. **The address, and it got worse.** The letterhead says C-262, 6th Cross,
   which is what the site publishes. Swiftheat's own IndiaMART profile **and**
   the MCA registry both say **B-132, 3rd Cross, 1st Stage**, which is what the
   old site said. Two sources against one. Either the company moved and never
   filed it, or the letterhead is wrong. This has to be settled before Google
   Business Profile or schema.org go anywhere near it.
2. **Phone and WhatsApp numbers.** The old site published `+91 12345 67890`. No
   number goes on the site until it has been dialled and answered. `contact/`
   and the footer both carry the placeholder today.
3. **The enquiry address.** Every form composes to `info@swiftheat.co.in`, the
   only address the company has ever published. Change `COMPANY["email"]` in
   `build/data.py` if enquiries should go elsewhere.
4. **Specification ranges.** Maximum temperature, watt density and tolerances
   per family. These are the "To confirm" cells in every technical data table.
   Swiftheat's IndiaMART product listings are **not** a usable source for these:
   two separate cartridge heaters are both listed at "10W" on a 17 to 18 mm
   sheath, which is a form field somebody had to fill in, not a specification.
5. **Photography.** See the section above. This is the largest single gap. Also
   confirm the seven accessory photographs in `imgs/` are Swiftheat's own.
6. **Logo in vector.** Only a 625 px PNG exists, so the masthead uses a type
   lockup and `favicon.svg` is drawn, not supplied.
7. **Plant area, machinery list, certifications, lead times.** Marked "to
   confirm" on `about/`, `capabilities/` and `quality/`.
8. **Downloads.** Every datasheet and catalogue is listed as "to be produced"
   and renders as plain text, not as a dead link.
9. **Product list.** Confirm Immersion Heaters and Control Systems are out, and
   Ceramic IR and Nozzle Heaters are in. The site is built for the second list.

## Sources for published company facts

| Fact | Source |
| --- | --- |
| Founded 2021, 11 to 25 people, manufacturer, HDFC | Swiftheat's own IndiaMART company profile |
| CIN U29100KA2021PTC150780 | MCA registry, via Zauba Corp |
| Registered address B-132, 3rd Cross | IndiaMART profile and MCA registry |
| Size ranges per family | The specification agreed in the proposal |
| Accessory and lead protection options | The old site's Products page, which a heater engineer wrote |

Competitors' catalogue specifications are deliberately **not** a source. Publishing
another manufacturer's numbers as Swiftheat's would make the technical data
tables wrong in a way nobody could detect until an element failed.
