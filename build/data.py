# -*- coding: utf-8 -*-
"""Every fact the site publishes, in one place.

Two rules govern what is in here.

1. Nothing is asserted about Swiftheat that has not been supplied by Swiftheat.
   Size ranges come from the list builder specification agreed in the proposal.
   Performance figures (temperature, watt density, tolerances) are marked TBD
   until the client's engineers confirm them, and render as "To confirm".
2. Option codes match the list builder exactly, so a code seen on a product page
   is the same code that appears on a generated requirement document.
"""

TBD = "To confirm"

# Option tuples are (code, name, why, rating) with an optional fifth element:
# the filename of a photograph in imgs/. Those photographs are the accessory
# shots off the old site's Products page, background knocked out by
# build/prep-imgs.py. Provenance is unconfirmed, see archive-old-site/PROVENANCE.md.

COMPANY = {
    "name": "Swiftheat Thermal Technologies Pvt Ltd",
    "short": "Swiftheat",
    "street": "Plot No. C-262, 6th Cross, near SVC Co-operative Bank",
    # Both client sources, the MCA filing and the 2026 brochure, say "1st Stage".
    # "1st Phase" came off the old site and is the odd one out.
    "area": "Peenya Industrial Area 1st Stage",
    "city": "Bengaluru",
    "state": "Karnataka",
    "pin": "560058",
    "country": "IN",
    # Held back pending the client, see the address and contact note below.
    # The 2026 brochure gives rekha@ and sales@ and does not mention info@ at all,
    # so info@ may not even be a live mailbox. Nothing changes until that is answered.
    "email": "info@swiftheat.co.in",
    "phone_display": TBD,
    # From the brochure, both ordinary mobiles rather than an IndiaMART 8047x
    # call tracking number. Not published: the house rule is that a number is
    # dialled and answered directly before it goes on the site.
    "phone_unverified": ("9108803706", "8553002014"),
    "email_unverified": ("rekha@swiftheat.co.in", "sales@swiftheat.co.in"),
    # Confirmed from Swiftheat's own IndiaMART company profile and the MCA
    # registry, August 2026. Both are the company's own filings, not a third
    # party's description, so they are publishable.
    #   indiamart.com/swiftheat-thermal-technologies/profile.html
    #   CIN U29100KA2021PTC150780
    "founded": "2021",
    "founded_long": "August 2021",
    "staff": "11 to 25",
    "cin": "U29100KA2021PTC150780",
    # Three sources, three different plots, and the brochure made it worse rather
    # than better. Nothing goes live until the client says which plot a courier
    # reaches them at today.
    #   B-132, 3rd Cross  MCA filing at incorporation, and the old site
    #   C-262, 6th Cross  email signature, and what this file still publishes
    #   C-205, 4th Cross  the 2026 printed brochure, 2nd Floor, Peenya 1st Stage
    "address_registry": "B-132, 3rd Cross, 1st Stage, Peenya Industrial Estate, Bangalore 560058",
    "address_brochure": "No. C-205, 2nd Floor, 4th Cross, Peenya 1st Stage, Peenya Industrial Area, Bangalore 560058",
    "domain": "swiftheat.co.in",
    "origin": "https://swiftheat.co.in",
}

# ---------------------------------------------------------------- product families

FAMILIES = [
{
 "slug": "cartridge-heaters",
 "name": "Cartridge Heaters",
 "nav": "Cartridge",
 "code": "CH",
 "art": "cartridge",
 "lede": "Swaged, high watt density heaters for bore mounting in moulds, platens and dies. "
         "Built to your drawing, with or without an inbuilt thermocouple.",
 "summary": "Bore mounted in moulds, platens and dies. Round, swaged, made to your length.",
 "meta": "Cartridge heaters made in Peenya, Bangalore. Diameters 6.35 to 25.4 mm, swaged "
         "construction, single or double ended, inbuilt thermocouple optional. Built to your drawing.",
 "facets": {"heats": "metal|liquid", "industry": "injection-moulding|die-and-mould|packaging-machinery|blow-moulding|rubber|food-processing",
            "form": "insert"},
 "chips": [("6.35 to 25.4 mm", "Diameter range", False),
           ("35 to 1500 mm", "Length range", False),
           (TBD, "Max sheath temp", True),
           (TBD, "Max watt density", True)],
 "temps": (200, 750),
 "construction": [
   "A resistance coil is wound over a ceramic core and centred inside a metal sheath. The void is "
   "packed with magnesium oxide, then the whole assembly is compacted by swaging, which crushes the "
   "MgO into a dense, void free mass.",
   "That compaction is the entire point. Dense MgO conducts heat outward to the sheath far better "
   "than loose powder, so the coil runs cooler for the same output. A heater that transfers its heat "
   "quickly into your tool is a heater that does not cook itself. Poorly compacted elements fail "
   "early and always fail the same way.",
   "The heated section stops short of each end, leaving unheated cold zones so the terminations stay "
   "below the temperature that would damage the leads or the seal.",
 ],
 "spec_cols": ["Property", "Stainless steel", "Incoloy 800"],
 "spec_rows": [
   ("Maximum sheath temperature", TBD, TBD),
   ("Maximum watt density", TBD, TBD),
   ("Watt density classes made", "High and medium", "High and medium"),
   ("Standard voltages", "110, 230, 240, 415 V", "110, 230, 240, 415 V"),
   ("Diameter range", "6.35 to 25.4 mm", "6.35 to 25.4 mm"),
   ("Length range", "35 to 1500 mm", "35 to 1500 mm"),
   ("Wattage range", "20 to 6000 W", "20 to 6000 W"),
   ("Diameter tolerance", TBD, TBD),
   ("Wattage tolerance", TBD, TBD),
   ("Resistance tolerance", TBD, TBD),
   ("Lead temperature rating", "By lead type, see options", "By lead type, see options"),
 ],
 "dim_caption": "Standard diameters and available lengths",
 "dim_cols": ["Diameter D", "Inch", "Min L", "Max L"],
 "dim_rows": [("6.35 mm", "1/4", TBD, TBD), ("7.94 mm", "5/16", TBD, TBD), ("9.53 mm", "3/8", TBD, TBD),
              ("12.7 mm", "1/2", TBD, TBD), ("15.88 mm", "5/8", TBD, TBD), ("19.05 mm", "3/4", TBD, TBD),
              ("25.4 mm", "1", TBD, TBD)],
 "dim_keys": "L overall length, HL heated length, CZ cold zone, D diameter, LL lead length",
 "options": [
   ("Termination", [
     ("T1", "Single end, straight", "Leads exit axially from one end. The default.", ""),
     ("T2", "Single end, right angle", "For tight clearance above the tool face.", "", "Right-angle-exit.png"),
     ("T3", "Double ended", "One lead from each end, for through holes.", ""),
   ]),
   ("Lead protection", [
     ("L1", "Silicone coated fibreglass", "General purpose, dry and clean environments.", TBD, "Silicon-coated-Fibreglass-sleeve.png"),
     ("L2", "PTFE insulated", "Where oil or plasticiser contact is likely.", TBD),
     ("L3", "Braided metal sleeve", "Abrasion resistance where leads move or rub.", TBD, "Braided-Metal-sleeve.png"),
     ("L4", "Armour cable", "Full mechanical protection on a moving platen.", TBD, "Armour.png"),
     ("L5", "Ceramic beading", "Highest lead exit temperature, no organic insulation.", TBD),
   ]),
   ("Inbuilt thermocouple", [
     ("TC0", "None", "Control from a separate sensor.", ""),
     ("TCJ", "Type J, ungrounded", "Iron constantan, isolated from the sheath.", ""),
     ("TCK", "Type K, ungrounded", "Higher range than Type J.", ""),
     ("TCG", "Grounded junction", "Faster response, junction bonded to the sheath.", ""),
   ]),
   ("Mounting and fittings", [
     ("M0", "None", "Plain sheath, no fitting.", ""),
     ("M1", "Round flange", "Welded, for surface mounting to a plate.", "", "Flange.png"),
     ("M2", "Threaded fitting", "NPT or BSP, size to be specified.", "", "Heater-with-Spl-mountable-threads.png"),
     ("M3", "T strain clamp", "Strain relief where the lead is pulled in service.", ""),
   ]),
 ],
 "options_note": "Thermocouple junction position is specified separately: disc end, mid length or lead end. "
                 "Continuous lead temperature limits, as published by Swiftheat: Teflon 270 C, "
                 "fibreglass 450 C, ceramic 900 to 1000 C.",
 "selection": [
   ("Watt density",
    "Watt density is the load on the sheath surface. Too high and the element burns out early, too "
    "low and the tool will not reach temperature. It is chosen from the working temperature and how "
    "well the heat leaves the heater, which in practice means how tightly it fits the bore."),
   ("Fit is what actually kills cartridge heaters",
    "An air gap between the heater and the bore is an insulator. The heater keeps making heat that "
    "cannot escape, so the coil temperature climbs until the element fails, while the tool never gets "
    "hot enough. Nine failures in ten start here."),
   ("Work the clearance out before ordering",
    "Fit equals the largest hole diameter minus the smallest heater diameter. Tell us the bore "
    "diameter and tolerance in your own part on the enquiry form and we will size the heater to suit "
    "it, rather than sending a standard part and hoping."),
 ],
 "failures": [
   ("Loose fit", "The commonest cause by a wide margin. Heat cannot leave the sheath, so the coil cooks."),
   ("Watt density too high", "Specified for speed rather than for the duty the tool actually runs."),
   ("Moisture in the MgO", "Insulation resistance falls after a shutdown. Often recoverable by baking out."),
   ("Lead damage at the exit", "Movement and abrasion at the tool face. Solved with the right lead protection."),
   ("Contamination", "Plastic or oil ingress into the bore, changing the heat path."),
   ("Cycling stress", "Rapid on and off duty on a heater specified for continuous running."),
 ],
 "industries": ["injection-moulding", "die-and-mould", "packaging-machinery", "blow-moulding", "rubber", "food-processing"],
 "related": ["coil-heaters", "tubular-heaters", "thermocouples-and-sensors"],
},
{
 "slug": "coil-heaters",
 "name": "Coil Heaters",
 "nav": "Coil",
 "code": "CO",
 "art": "coil",
 "lede": "Spiral wound elements that wrap a nozzle or a manifold and put a high watt density into a "
         "very small area, with the thermocouple built into the coil.",
 "summary": "Hot runner nozzles and manifolds. Wound to the diameter, profiled along the length.",
 "meta": "Coil heaters for hot runner nozzles and manifolds, supplied from Peenya, Bangalore. German "
         "made element, standard profile 2.2 by 4.2 mm, inbuilt Type J thermocouple, Teflon leads.",
 "facets": {"heats": "metal", "industry": "injection-moulding|blow-moulding|packaging-machinery|extrusion", "form": "wrap"},
 "chips": [("8 to 120 mm", "Inside diameter", False),
           ("20 to 600 mm", "Heated length", False),
           ("100 to 3000 W", "Wattage range", False),
           (TBD, "Max sheath temp", True)],
 "temps": (200, 750),
 "construction": [
   "A resistance conductor and its mineral insulation are drawn down inside a metal sheath, then the "
   "whole cable is wound into a close pitched spiral. The result is a heater that is mostly surface: "
   "almost all of it touches the part it is heating.",
   "Profile is the decision that matters. A square or rectangular section sits flat against the "
   "nozzle and transfers heat through a face rather than a line, which is why hot runner work almost "
   "always specifies it. Round section is easier to wind to a tight radius.",
   "Pitch can be varied along the length, so more turns can be placed where the heat is needed and "
   "fewer where it is not. That is how a manifold gets an even melt without hot spots at the ends.",
   "These are the one family Swiftheat supplies rather than winds. The element is German made, and "
   "the standard item is a 2.2 by 4.2 mm section with Teflon leads, an inbuilt Type J thermocouple, "
   "a 900 mm black fibreglass sleeve and a ground wire. We say so because where a part is made is a "
   "fair question, and the answer here is not Peenya.",
 ],
 "spec_cols": ["Property", "Value"],
 "spec_rows": [
   ("Maximum sheath temperature", TBD),
   ("Maximum watt density", TBD),
   ("Standard voltages", "110, 230, 240 V"),
   ("Inside diameter range", "8 to 120 mm"),
   ("Heated length range", "20 to 600 mm"),
   ("Wattage range", "100 to 3000 W"),
   ("Profile sections offered", "Round, square, rectangular"),
   ("Standard stock section", "2.2 mm thick by 4.2 mm wide"),
   ("Standard lead", "Teflon insulated, with ground wire"),
   ("Standard sleeve", "900 mm black fibreglass"),
   ("Resistance tolerance", TBD),
   ("Thermocouple types", "J and K, inbuilt. Type J on the standard item"),
   ("Manufacture", "German made element, supplied by Swiftheat"),
 ],
 "dim_caption": "What we need in order to wind a coil",
 "dim_cols": ["Dimension", "Symbol", "Range"],
 "dim_rows": [("Inside diameter", "ID", "8 to 120 mm"), ("Heated length", "HL", "20 to 600 mm"),
              ("Total length including cold ends", "L", TBD), ("Coil pitch", "P", "State if profiled"),
              ("Lead length", "LL", "State per end")],
 "dim_keys": "ID inside diameter, HL heated length, P pitch, LL lead length",
 "options": [
   ("Profile", [
     ("PR", "Round section", "Round section wire. Easiest to wind to a tight radius.", ""),
     ("PS", "Square section", "Flat contact face, better transfer than round.", ""),
     ("PT", "Rectangular section", "Widest contact face. The usual hot runner choice.", ""),
   ]),
   ("Lead exit", [
     ("EA", "Axial", "Leads leave along the axis of the coil.", ""),
     ("ER", "Radial", "Leads leave out of the side.", ""),
     ("ET", "Tangential", "Leads leave off the tangent, for tight manifold pockets.", ""),
   ]),
   ("Inbuilt thermocouple", [
     ("TC0", "None", "Control from a separate sensor.", ""),
     ("TCJ", "Type J", "Iron constantan.", ""),
     ("TCK", "Type K", "Higher range than Type J.", ""),
   ]),
 ],
 "options_note": "State which end the leads leave from, and whether a reflection tube or sleeve is required. "
                 "The standard stock item is a 2.2 by 4.2 mm section with Teflon leads, an inbuilt "
                 "Type J thermocouple, a 900 mm black fibreglass sleeve and a ground wire.",
 "selection": [
   ("Match the bore, not the nominal size",
    "A coil heater works by contact. Give us the actual measured diameter of the nozzle or the pocket, "
    "not the drawing's nominal, and say whether it is worn."),
   ("Profile the pitch where the heat is lost",
    "Ends lose heat into the surrounding steel. Closing the pitch at the ends and opening it in the "
    "middle gives a flatter melt profile than a single evenly wound coil at the same wattage."),
   ("Put the thermocouple where the control needs it",
    "An inbuilt thermocouple reads the heater, not the melt. Tell us where the junction must sit "
    "along the coil, and we will place it there."),
 ],
 "failures": [
   ("Loose wrap", "Any air gap between coil and nozzle traps heat in the element."),
   ("Wrong profile", "Round section on a face that needed rectangular contact runs hotter for the same output."),
   ("Lead exit fouling", "The exit direction was not stated, so the leads foul the manifold plate on assembly."),
   ("Overtightened on fitting", "Forcing a coil down a nozzle deforms the section and cracks the insulation."),
   ("Thermocouple in the wrong place", "The controller holds a temperature the melt never sees."),
 ],
 "industries": ["injection-moulding", "blow-moulding", "packaging-machinery", "extrusion"],
 "related": ["nozzle-heaters", "cartridge-heaters", "thermocouples-and-sensors"],
},
{
 "slug": "band-heaters",
 "name": "Ceramic and Mica Band Heaters",
 "nav": "Band",
 "code": "BH",
 "art": "band",
 "lede": "Clamped around barrels and cylinders to heat them evenly. Ceramic for the higher "
         "temperatures and insulated running, mica where the section has to stay thin.",
 "summary": "Barrels, cylinders and pipes. One piece, split, expandable or partial coverage.",
 "meta": "Ceramic and mica band heaters made in Peenya, Bangalore. Inside diameters 20 to 800 mm, "
         "one piece, two piece, expandable and partial coverage, built to your cutout drawing.",
 "facets": {"heats": "metal", "industry": "injection-moulding|extrusion|blow-moulding|packaging-machinery|rubber|food-processing", "form": "wrap"},
 "chips": [("20 to 800 mm", "Inside diameter", False),
           ("20 to 400 mm", "Width", False),
           ("100 to 9000 W", "Wattage range", False),
           (TBD, "Max working temp", True)],
 "temps": (150, 700),
 "construction": [
   "A ceramic band carries the resistance wire threaded through interlocking ceramic tiles, held in a "
   "stainless steel outer with a ceramic fibre insulation blanket behind it. The wire never touches "
   "the barrel, so it can run hotter, and the insulation sends the heat inward instead of into the "
   "workshop.",
   "A mica band carries flat resistance ribbon wound over a mica sheet, sandwiched between more mica "
   "and a thin steel outer. It is thinner, cheaper and faster to make, and it suits lower "
   "temperatures and tighter clearances.",
   "Whichever it is, the heater only works if it clamps down onto the barrel. A band that has been "
   "opened and refitted a dozen times, or fitted to a barrel that has worn oval, is heating an air "
   "gap.",
 ],
 "spec_cols": ["Property", "Ceramic", "Mica"],
 "spec_rows": [
   ("Maximum working temperature", TBD, TBD),
   ("Maximum watt density", TBD, TBD),
   ("Standard voltages", "230, 240, 415 V", "230, 240, 415 V"),
   ("Inside diameter range", "20 to 800 mm", "20 to 800 mm"),
   ("Width range", "20 to 400 mm", "20 to 400 mm"),
   ("Wattage range", "100 to 9000 W", "100 to 9000 W"),
   ("Section thickness", TBD, TBD),
   ("Cutouts and holes", "Yes, to your drawing", "Yes, to your drawing"),
   ("Insulation blanket", "Optional", "Not applicable"),
 ],
 "dim_caption": "What we need in order to make a band",
 "dim_cols": ["Dimension", "Symbol", "Note"],
 "dim_rows": [("Inside diameter", "ID", "Measured on the barrel, not the drawing nominal"),
              ("Width", "W", "Across the band"),
              ("Gap at the joint", "G", "State if a specific gap is required"),
              ("Angle of coverage", "A", "Partial coverage only"),
              ("Cutout positions", "-", "Position and size, from a stated datum"),
              ("Termination position", "-", "Clock position on the circumference")],
 "dim_keys": "ID inside diameter, W width, G joint gap, A angle of coverage",
 "options": [
   ("Material", [
     ("CE", "Ceramic", "Higher temperature, insulated, heat directed inward.", TBD),
     ("MI", "Mica", "Thinner section, lower temperature, lower cost.", TBD),
   ]),
   ("Construction", [
     ("C1", "One piece", "Full circle, slides on from the end of the barrel.", ""),
     ("C2", "Two piece", "Split into halves, fits a barrel that cannot be cleared.", ""),
     ("CE1", "Expandable", "Opens to slide over the barrel, then closes down onto it.", ""),
     ("CP", "Partial coverage", "Part of the circumference. State the angle.", ""),
   ]),
   ("Clamping", [
     ("K1", "Built in strap", "Integral barrel strap, the usual choice.", ""),
     ("K2", "Separate strap", "Removable clamping band.", ""),
     ("K3", "Wedge lock", "For heaters that come off frequently.", ""),
     ("K4", "Spring loaded", "Holds pressure as the barrel expands and contracts.", ""),
   ]),
   ("Termination", [
     ("S1", "Screw terminals", "Exposed screw posts.", ""),
     ("S2", "Post terminals", "Ceramic insulated posts.", ""),
     ("S3", "Flying leads", "Leads with the protection of your choice.", ""),
     ("S4", "Terminal box", "Enclosed box, for washdown or dusty plant.", ""),
   ]),
 ],
 "options_note": "Cutouts, thermocouple holes and slots are made to your drawing. Send the drawing "
                 "with the enquiry and state the datum you are measuring from.",
 "selection": [
   ("Measure the barrel, not the drawing",
    "Barrels wear. An inside diameter taken from the machine's original drawing can be a millimetre "
    "or more away from the surface the band actually has to grip."),
   ("Watt density follows the process temperature",
    "The higher the barrel runs, the lower the watt density the element can carry without the wire "
    "reaching its own limit. Tell us the zone temperature and we will work back to a safe loading."),
   ("Insulate the ones that pay for it",
    "An insulation blanket on a barrel band cuts the heat lost into the shop and shortens heat up "
    "time. It is worth it on continuous running machines and rarely worth it on short duty ones."),
 ],
 "failures": [
   ("Not clamped down", "The commonest failure. Air between band and barrel traps heat in the element."),
   ("Refitted too many times", "Repeated opening and closing work hardens the outer and it stops closing tight."),
   ("Contamination at the joint", "Purged plastic finds the gap, carbonises and insulates."),
   ("Terminal damage", "Screw terminals loosened by vibration arc and burn the connection."),
   ("Wrong construction for the fit", "A one piece band fitted where the barrel could not be cleared, forced open on assembly."),
 ],
 "industries": ["injection-moulding", "extrusion", "blow-moulding", "packaging-machinery", "rubber", "food-processing"],
 "related": ["nozzle-heaters", "coil-heaters", "strip-heaters"],
},
{
 "slug": "nozzle-heaters",
 "name": "Ceramic and Mica Nozzle Heaters",
 "nav": "Nozzle",
 "code": "NZ",
 "art": "nozzle",
 "lede": "Short bands sized for the nozzle itself, where there is very little room, the temperature "
         "has to hold steady and the thermocouple usually has to come built in.",
 "summary": "Injection nozzles and short cylindrical sections with no room for a full band.",
 "meta": "Ceramic and mica nozzle heaters made in Peenya, Bangalore. Outside diameters 10 to 150 mm, "
         "heated lengths 20 to 400 mm, inbuilt thermocouple optional.",
 "facets": {"heats": "metal", "industry": "injection-moulding|blow-moulding|packaging-machinery", "form": "wrap"},
 "chips": [("10 to 150 mm", "Nozzle diameter", False),
           ("20 to 400 mm", "Heated length", False),
           ("100 to 3000 W", "Wattage range", False),
           (TBD, "Max working temp", True)],
 "temps": (150, 700),
 "construction": [
   "A nozzle heater is a band heater built to nozzle proportions: short, small in diameter and "
   "usually clamped rather than strapped. The construction choices are the same, ceramic tile or mica "
   "sheet, but the tolerances are tighter because there is no slack anywhere on a nozzle.",
   "Wall thickness constrains everything. A nozzle that has to pass through a fixed platen bore has a "
   "hard limit on how thick the heater can be, and that limit decides whether the element can be "
   "ceramic at all.",
   "Most nozzle heaters carry the thermocouple. The controller is holding the melt at the gate, and "
   "the only practical place to read it is on the nozzle itself.",
 ],
 "spec_cols": ["Property", "Ceramic", "Mica"],
 "spec_rows": [
   ("Maximum working temperature", TBD, TBD),
   ("Maximum watt density", TBD, TBD),
   ("Standard voltages", "110, 230, 240 V", "110, 230, 240 V"),
   ("Nozzle outside diameter", "10 to 150 mm", "10 to 150 mm"),
   ("Heated length range", "20 to 400 mm", "20 to 400 mm"),
   ("Wattage range", "100 to 3000 W", "100 to 3000 W"),
   ("Minimum wall thickness", TBD, TBD),
   ("Inbuilt thermocouple", "J or K", "J or K"),
 ],
 "dim_caption": "What we need in order to make a nozzle heater",
 "dim_cols": ["Dimension", "Symbol", "Note"],
 "dim_rows": [("Nozzle outside diameter", "OD", "Measured, at the seat of the heater"),
              ("Heated length", "HL", "Along the nozzle"),
              ("Maximum wall thickness available", "T", "The bore the nozzle passes through"),
              ("Groove or step configuration", "-", "Send a sketch if the nozzle is stepped"),
              ("Thermocouple position", "-", "Distance from the gate end")],
 "dim_keys": "OD nozzle outside diameter, HL heated length, T available wall thickness",
 "options": [
   ("Material", [
     ("CE", "Ceramic", "Higher temperature, thicker section.", TBD),
     ("MI", "Mica", "Thin section where clearance is the constraint.", TBD),
   ]),
   ("Inbuilt thermocouple", [
     ("TC0", "None", "Control from a separate sensor.", ""),
     ("TCJ", "Type J", "Iron constantan.", ""),
     ("TCK", "Type K", "Higher range than Type J.", ""),
   ]),
 ],
 "options_note": "Clamping, termination type and termination position follow the band heater option "
                 "list. State the clock position of the terminal so it clears the platen.",
 "selection": [
   ("Clearance decides the material",
    "Measure the bore the nozzle passes through before choosing ceramic. If the available wall is "
    "thin, mica is not a compromise, it is the only option that fits."),
   ("Say where the terminal must point",
    "A nozzle heater that is electrically perfect and mechanically fouling the platen is a scrapped "
    "part. The clock position costs nothing to state and everything to get wrong."),
   ("Put the junction near the gate",
    "The melt temperature that matters is at the gate, not at the back of the nozzle. Tell us the "
    "distance from the gate end and we will set the junction there."),
 ],
 "failures": [
   ("Clamped onto a worn nozzle", "The heater no longer grips and heats an air gap."),
   ("Purge contamination", "Melt escaping at the gate runs back under the heater and carbonises."),
   ("Terminal fouling", "The terminal position was never stated, so it hits the platen on assembly."),
   ("Lead flexing", "The nozzle moves with the carriage and the leads work harden at the exit."),
 ],
 "industries": ["injection-moulding", "blow-moulding", "packaging-machinery"],
 "related": ["band-heaters", "coil-heaters", "thermocouples-and-sensors"],
},
{
 "slug": "strip-heaters",
 "name": "Strip Heaters",
 "nav": "Strip",
 "code": "SH",
 "art": "strip",
 "lede": "Flat elements bolted to a plate, a platen or a sealing bar, in plain form for conduction "
         "and finned form for moving air.",
 "summary": "Flat and gently curved surfaces, sealing bars, platens and duct air.",
 "meta": "Strip heaters made in Peenya, Bangalore. Lengths 60 to 2000 mm, widths 20 to 150 mm, "
         "plain or finned, mounting holes to your drawing.",
 "facets": {"heats": "metal|air", "industry": "packaging-machinery|food-processing|die-and-mould|industrial-heating|rubber", "form": "surface"},
 "chips": [("60 to 2000 mm", "Length range", False),
           ("20 to 150 mm", "Width range", False),
           ("100 to 6000 W", "Wattage range", False),
           (TBD, "Max sheath temp", True)],
 "temps": (150, 650),
 "construction": [
   "Resistance ribbon is wound over a mica or ceramic former, insulated, and pressed into a flat "
   "metal case. The case is the working surface, so how flat it is and how hard it is clamped decide "
   "how much of the heat actually reaches the job.",
   "Finned versions carry pressed steel fins on the back of the case. Fins are for air: they multiply "
   "the surface the element can shed heat from, which is what keeps the sheath temperature down when "
   "there is no metal to conduct into.",
   "Mounting holes, slots and the position of the terminals are all made to your drawing, because a "
   "strip heater that does not line up with the existing holes in a sealing bar is scrap.",
 ],
 "spec_cols": ["Property", "Plain", "Finned"],
 "spec_rows": [
   ("Maximum sheath temperature", TBD, TBD),
   ("Maximum watt density", TBD, TBD),
   ("Standard voltages", "230, 240, 415 V", "230, 240, 415 V"),
   ("Length range", "60 to 2000 mm", "60 to 2000 mm"),
   ("Width range", "20 to 150 mm", "20 to 150 mm"),
   ("Wattage range", "100 to 6000 W", "100 to 6000 W"),
   ("Typical duty", "Clamped to metal", "Free air and ducts"),
   ("Mounting holes", "To your drawing", "To your drawing"),
 ],
 "dim_caption": "What we need in order to make a strip heater",
 "dim_cols": ["Dimension", "Symbol", "Note"],
 "dim_rows": [("Length", "L", "Overall, including any cold ends"),
              ("Width", "W", "Across the case"),
              ("Thickness", "T", TBD),
              ("Mounting hole diameter", "d", "And quantity"),
              ("Hole positions", "-", "From a stated datum end"),
              ("Terminal position", "-", "Which end, or centre")],
 "dim_keys": "L length, W width, T thickness, d hole diameter",
 "options": [
   ("Profile", [
     ("F0", "Plain", "Flat case, for clamping to metal.", ""),
     ("F1", "Finned", "Fins on the back, for heating air.", ""),
   ]),
   ("Termination", [
     ("S1", "Screw terminals", "Exposed screw posts at one end.", ""),
     ("S3", "Flying leads", "Leads with the protection of your choice.", ""),
   ]),
 ],
 "options_note": "Sheath material, hole pattern and any bend or curve are quoted from your drawing.",
 "selection": [
   ("Clamped or free air changes everything",
    "The same element run bolted to a platen and run hanging in air will not survive the same watt "
    "density. Tell us which it is."),
   ("Flatness is a specification",
    "A strip heater bolted at the ends onto a surface that is not flat touches at two points. Say if "
    "the mounting face is machined or as cast."),
   ("Give us the hole pattern, not the old part number",
    "Old part numbers do not travel between suppliers. A dimensioned sketch of the hole positions "
    "does, and it is faster to quote from."),
 ],
 "failures": [
   ("Bolted to an uneven face", "Contact at two points only, so the middle of the element overheats."),
   ("Fins choked with dust", "A finned heater in a dusty plant loses the surface it depends on."),
   ("Over tightened bolts", "The case deforms and the internal insulation cracks."),
   ("Terminals in the hot zone", "Terminals positioned where the process heat reaches them."),
 ],
 "industries": ["packaging-machinery", "food-processing", "die-and-mould", "rubber", "industrial-heating"],
 "related": ["tubular-heaters", "band-heaters", "cartridge-heaters"],
},
{
 "slug": "tubular-heaters",
 "name": "Tubular Heaters",
 "nav": "Tubular",
 "code": "TH",
 "art": "tubular",
 "lede": "The general purpose element. A mineral insulated tube that can be bent to almost any form "
         "and put into air, into liquid or clamped against a surface.",
 "summary": "Air, liquids and surfaces. Straight, U form, W form or coiled to your drawing.",
 "meta": "Tubular heaters made in Peenya, Bangalore. Sheath diameters 6.5 to 16 mm, lengths 100 to "
         "4000 mm, straight, U form, W form and coiled, stainless steel and Incoloy sheaths.",
 "facets": {"heats": "air|liquid|metal", "industry": "food-processing|pharmaceutical-machinery|industrial-heating|packaging-machinery|extrusion", "form": "immersion"},
 "chips": [("6.5 to 16 mm", "Sheath diameter", False),
           ("100 to 4000 mm", "Length range", False),
           ("100 to 9000 W", "Wattage range", False),
           (TBD, "Max sheath temp", True)],
 "temps": (150, 750),
 "construction": [
   "A resistance coil runs down the centre of a metal tube, packed in magnesium oxide and compacted "
   "so the powder becomes a solid, electrically insulating, thermally conducting core. Cold ends at "
   "each terminal keep the seals out of the heat.",
   "Because the finished tube is a solid rod of insulation, it can be bent. That is what makes the "
   "family so general: the same element becomes a duct heater, an immersion heater or a platen "
   "heater depending on the form it is bent to.",
   "Sheath material is chosen for what the element sits in, not for what it costs. Copper for clean "
   "water, stainless for most process work, Incoloy where the temperature or the chemistry would eat "
   "stainless.",
 ],
 "spec_cols": ["Property", "Stainless steel", "Incoloy"],
 "spec_rows": [
   ("Maximum sheath temperature", TBD, TBD),
   ("Maximum watt density in air", TBD, TBD),
   ("Maximum watt density in liquid", TBD, TBD),
   ("Standard voltages", "230, 240, 415 V", "230, 240, 415 V"),
   ("Sheath diameters", "6.5, 8, 8.5, 11, 12.5, 16 mm", "6.5, 8, 8.5, 11, 12.5, 16 mm"),
   ("Length range", "100 to 4000 mm", "100 to 4000 mm"),
   ("Wattage range", "100 to 9000 W", "100 to 9000 W"),
   ("Bend forms", "Straight, U, W, coiled", "Straight, U, W, coiled"),
   ("Cold end length", TBD, TBD),
 ],
 "dim_caption": "What we need in order to make a tubular heater",
 "dim_cols": ["Dimension", "Symbol", "Note"],
 "dim_rows": [("Sheath diameter", "D", "From the standard list"),
              ("Overall length", "L", "Developed length if bent"),
              ("Heated length", "HL", "Excluding cold ends"),
              ("Cold end length", "CZ", "Each end"),
              ("Bend form", "-", "Straight, U, W or coiled"),
              ("Bend radius and centres", "-", "Send a drawing for anything other than a plain U")],
 "dim_keys": "D sheath diameter, L overall length, HL heated length, CZ cold end",
 "options": [
   ("Bend form", [
     ("B0", "Straight", "The plain rod.", ""),
     ("BU", "U form", "Folded once, both terminals at the same end.", ""),
     ("BW", "W form", "Folded twice, more heated length in the same envelope.", ""),
     ("BC", "Coiled", "Wound to a helix. Send a drawing.", "", "Flexible-Tubular-heaters.png"),
   ]),
   ("Sheath material", [
     ("SS", "Stainless steel", "General process work.", TBD),
     ("IN", "Incoloy", "Higher temperature and more aggressive media.", TBD),
     ("MS", "Mild steel", "Dry air and oil, where cost matters.", TBD),
     ("CU", "Copper", "Clean water only.", TBD),
   ]),
   ("Terminal", [
     ("S0", "Studs", "Threaded studs with nuts, the default.", ""),
     ("S1", "Screw terminals", "Screw posts.", ""),
     ("S3", "Flying leads", "Leads with the protection of your choice.", ""),
   ]),
 ],
 "options_note": "Mounting flanges, threaded bosses and terminal enclosures are quoted from your drawing.",
 "selection": [
   ("What the element sits in sets the watt density",
    "Still air will carry a fraction of the loading that flowing water will. State the medium and "
    "whether it moves."),
   ("Never let an immersion element run dry",
    "An element specified for liquid and switched on in air will reach its own limit in seconds. "
    "Low level protection is not optional on a tank."),
   ("Send a drawing for anything bent",
    "A developed length and a bend form describe a U. Anything else, including coils and multi plane "
    "bends, needs a drawing to be quoted correctly the first time."),
 ],
 "failures": [
   ("Dry running", "The single most destructive failure mode for an immersion element."),
   ("Scale on the sheath", "Hard water deposits insulate the element and drive the sheath temperature up."),
   ("Wrong sheath for the medium", "Stainless pitting in chloride, mild steel in water."),
   ("Terminal ingress", "Moisture entering an unsealed terminal end after a washdown."),
   ("Vibration at the bend", "An unsupported long element fatigues at the first bend."),
 ],
 "industries": ["food-processing", "pharmaceutical-machinery", "industrial-heating", "packaging-machinery", "extrusion"],
 "related": ["strip-heaters", "cartridge-heaters", "ceramic-infrared-heaters"],
},
{
 "slug": "thermocouples-and-sensors",
 "name": "Thermocouples and Temperature Sensors",
 "nav": "Sensors",
 "code": "TS",
 "art": "sensor",
 "lede": "The measuring half of the job. Nine thermocouple types and PT100 class RTDs, made to the "
         "immersion length, junction and connection your controller expects.",
 "summary": "Types J, K, N, T, E, R, S, B and C, plus PT100, PT500 and PT1000 RTDs, made to length.",
 "meta": "Thermocouples and temperature sensors made in Peenya, Bangalore. Types J, K, N, T, E, R, S, "
         "B and C, PT100, PT500 and PT1000 RTDs, washer, lug, bolt, spring loaded and manifold styles.",
 "facets": {"heats": "sensor", "industry": "injection-moulding|extrusion|food-processing|pharmaceutical-machinery|industrial-heating|packaging-machinery|blow-moulding|die-and-mould|rubber", "form": "sensor"},
 "chips": [("1.5 to 8 mm", "Sheath diameter", False),
           ("20 to 2000 mm", "Immersion length", False),
           ("9 types, PT100", "Types offered", False),
           ("Class 1 and Class A", "Tolerance class", False)],
 "temps": (0, 1100),
 "construction": [
   "A thermocouple is two dissimilar wires joined at one end. The junction produces a small voltage "
   "that varies with temperature, and the controller reads that voltage. Everything else, the sheath, "
   "the insulation, the cable, exists to get that junction to the right place and keep it there.",
   "An RTD works differently. A platinum element changes resistance with temperature in a way that is "
   "very repeatable, which is why PT100 is the usual choice where accuracy and stability matter more "
   "than range or speed.",
   "The junction arrangement is the decision that changes the behaviour. Grounded to the sheath is "
   "fastest but electrically connected to the process. Ungrounded is isolated and slower. Exposed is "
   "fastest of all and has no protection at all.",
 ],
 "spec_cols": ["Property", "Thermocouple", "RTD"],
 "spec_rows": [
   ("Types offered", "J, K, N, T, E, R, S, B, C", "PT100, PT500, PT1000"),
   ("Useful range", TBD, TBD),
   ("Tolerance class", "Class 1", "Class A"),
   ("Calibration", "100 percent, certificate on request", "100 percent, certificate on request"),
   ("Sheath diameters", "1.5, 3, 4.5, 6, 8 mm", "3, 4.5, 6, 8 mm"),
   ("Immersion length range", "20 to 2000 mm", "20 to 2000 mm"),
   ("Cable length range", "100 to 10000 mm", "100 to 10000 mm"),
   ("Junction arrangements", "Grounded, ungrounded, exposed", "Not applicable"),
   ("Connections", "Plug, bare tails, terminal head", "Plug, bare tails, terminal head"),
   ("Terminals", "PVC pin, round lug, fork", "PVC pin, round lug, fork"),
   ("Washer style", "OD 8 to 16 mm, bolt M3 to M10, 3 to 6 mm thick", TBD),
   ("Lug style", "OD 8 to 20 mm, bolt M3 to M12, 0.5 to 3 mm thick", TBD),
   ("Bolt style, fixed or rotational", "Standard thread sizes", "Standard thread sizes"),
   ("Spring loaded style", "Bayonet ID 11 to 18 mm, spring 100 to 1000 mm", "Bayonet ID 11 to 18 mm, spring 100 to 1000 mm"),
   ("Mineral insulated sheath", "2 to 8 mm", TBD),
   ("Manifold style", "TEF-68, 4 mm diameter, 11 and 12 mm tip", "Not applicable"),
 ],
 "dim_caption": "What we need in order to make a sensor",
 "dim_cols": ["Dimension", "Symbol", "Note"],
 "dim_rows": [("Sheath diameter", "D", "From the standard list"),
              ("Immersion length", "L", "Tip to the underside of the fitting"),
              ("Cable length", "CL", "Tail or lead"),
              ("Process thread", "-", "If a fitting or compression gland is required"),
              ("Spring loading", "-", "For bayonet and spring loaded styles")],
 "dim_keys": "D sheath diameter, L immersion length, CL cable length",
 "options": [
   ("Type", [
     ("J", "Type J thermocouple", "Iron constantan. The plastics industry default.", ""),
     ("K", "Type K thermocouple", "Nickel chromium. Wider range than Type J.", ""),
     ("PT1", "PT100 RTD", "Platinum, 100 ohm at 0 degrees C. Highest stability.", ""),
     ("PT5", "PT500 RTD", "Platinum, 500 ohm at 0 degrees C.", ""),
   ]),
   ("Junction", [
     ("G", "Grounded", "Bonded to the sheath. Fastest of the protected types.", ""),
     ("U", "Ungrounded", "Electrically isolated from the sheath.", ""),
     ("E", "Exposed", "No sheath at the tip. Fastest, and unprotected.", ""),
   ]),
   ("Connection", [
     ("P", "Plug", "Standard miniature or flat pin plug.", ""),
     ("B", "Bare tails", "Stripped and tinned tails.", ""),
     ("H", "Terminal head", "Cast head with a terminal block.", ""),
   ]),
 ],
 "options_note": "The coded list above is the part the requirement builder covers. Types N, T, E, R, "
                 "S, B and C are made to order alongside them, as are washer, lug, bolt, spring "
                 "loaded, mineral insulated and manifold styles, compression fittings, bulkheads, "
                 "NPT and BSP bushes, connectors and extension cable. Continuous limits by lead "
                 "insulation: Teflon 270 C, fibreglass 450 C, ceramic 900 to 1000 C, and mineral "
                 "insulated sensors run to 1200 to 1400 C. State the controller make and model if "
                 "you want us to match an existing sensor.",
 "selection": [
   ("Match the type to the controller",
    "A Type K sensor read by a controller set to Type J is wrong at every temperature, and it is a "
    "surprisingly common fault on a production line. State what the controller is set to."),
   ("Isolate where there is electrical noise",
    "An ungrounded junction breaks the electrical path between the process and the controller input, "
    "which is worth having on a machine with drives and solid state relays."),
   ("Immersion length is measured, not guessed",
    "A sensor that stops short of the melt reads the steel around it. Measure from the seating face "
    "to where the tip has to sit."),
 ],
 "failures": [
   ("Wrong type for the controller", "The reading is plausible and wrong, so nobody questions it."),
   ("Insufficient immersion", "The sensor reads the fitting, not the process."),
   ("Cable run beside power cables", "Induced noise on a millivolt signal."),
   ("Extension cable of the wrong type", "Copper extension on a thermocouple circuit adds its own junction."),
   ("Bent or crushed sheath", "The junction moves, or the insulation resistance falls."),
 ],
 "industries": ["injection-moulding", "extrusion", "blow-moulding", "packaging-machinery", "die-and-mould",
                "food-processing", "pharmaceutical-machinery", "rubber", "industrial-heating"],
 "related": ["cartridge-heaters", "coil-heaters", "band-heaters"],
},
{
 "slug": "ceramic-infrared-heaters",
 "name": "Ceramic Infrared Heaters",
 "nav": "Ceramic IR",
 "code": "IR",
 "art": "ir",
 "lede": "Radiant elements that heat the surface of the work directly, without heating the air in "
         "between. Trough, flat panel and hollow forms, with or without a reflector.",
 "summary": "Radiant surface heating, thermoforming, drying and preheating.",
 "meta": "Ceramic infrared heaters made in Peenya, Bangalore. Trough, flat panel and hollow element "
         "forms, 100 to 2000 W, reflector and inbuilt thermocouple optional.",
 "facets": {"heats": "radiant|air", "industry": "packaging-machinery|blow-moulding|food-processing|industrial-heating|pharmaceutical-machinery", "form": "radiant"},
 "chips": [("100 to 2000 W", "Wattage range", False),
           ("230, 240 V", "Voltages", False),
           ("Trough, panel, hollow", "Element forms", False),
           (TBD, "Peak wavelength", True)],
 "temps": (300, 750),
 "construction": [
   "A resistance coil is embedded in a moulded ceramic body. When the ceramic is hot it radiates in "
   "the medium wave infrared band, and that radiation crosses the gap and is absorbed at the surface "
   "of the work. The air in between is barely heated at all.",
   "That is the whole argument for the technology. Where a convection oven has to bring the air, the "
   "enclosure and the fixtures up to temperature before the job gets hot, a radiant panel puts its "
   "energy where the job is.",
   "Element form controls the pattern. A trough concentrates the radiation into a band, a flat panel "
   "spreads it evenly over an area, and a reflector behind either of them sends back the half that "
   "would otherwise be lost.",
 ],
 "spec_cols": ["Property", "Value"],
 "spec_rows": [
   ("Element forms", "Trough, flat panel, hollow"),
   ("Wattage range", "100 to 2000 W"),
   ("Standard voltages", "230, 240 V"),
   ("Element face temperature", TBD),
   ("Peak wavelength", TBD),
   ("Inbuilt thermocouple", "Type K, optional"),
   ("Reflector", "Optional, fitted"),
   ("Typical working distance", "20 to 1000 mm, application dependent"),
 ],
 "dim_caption": "What we need in order to specify a radiant installation",
 "dim_cols": ["Input", "Symbol", "Note"],
 "dim_rows": [("Element form", "-", "Trough, flat panel or hollow"),
              ("Wattage per element", "W", "And how many elements"),
              ("Distance to the work", "d", "Face of the element to the surface"),
              ("Target surface temperature", "-", "What the work has to reach"),
              ("Material being heated", "-", "Absorption depends on the material"),
              ("Line speed or dwell time", "-", "For continuous processes")],
 "dim_keys": "d distance to the work",
 "options": [
   ("Element form", [
     ("FT", "Trough", "Concentrates the radiation into a band.", ""),
     ("FF", "Flat panel", "Even spread over an area.", ""),
     ("FH", "Hollow", "Deeper body, for higher output per element.", ""),
   ]),
   ("Inbuilt thermocouple", [
     ("TC0", "None", "Control by power percentage or from a separate sensor.", ""),
     ("TCK", "Type K", "Closed loop control on the element face.", ""),
   ]),
   ("Reflector", [
     ("R0", "None", "Element only.", ""),
     ("R1", "Fitted reflector", "Directs the back radiation forward.", ""),
   ]),
 ],
 "options_head": "Frames, cassettes and multi element panels are made to order. Tell us the area to "
                 "be covered and the target temperature and we will lay the elements out.",
 "options_note": "Frames, cassettes and multi element panels are made to order. Tell us the area to "
                 "be covered and the target temperature and we will lay the elements out.",
 "selection": [
   ("Distance sets the intensity",
    "Radiant intensity falls off sharply with distance. Halving the gap does far more than adding "
    "elements, and it is usually cheaper."),
   ("The material decides how much is absorbed",
    "Two materials at the same distance under the same element will reach very different "
    "temperatures. Tell us what is being heated."),
   ("Control the element, or control the work",
    "An inbuilt thermocouple holds the element face steady. Holding the work steady needs a sensor "
    "looking at the work. Say which one the process needs."),
 ],
 "failures": [
   ("Too far from the work", "The commonest specification error. Output is fine, intensity at the surface is not."),
   ("No reflector", "Half the radiation goes backwards into the frame."),
   ("Thermal shock", "Cold draught or splash onto a hot ceramic body cracks it."),
   ("Wired without power control", "Full on and full off cycling stresses the ceramic and overshoots the work."),
 ],
 "industries": ["packaging-machinery", "blow-moulding", "food-processing", "pharmaceutical-machinery", "industrial-heating"],
 "related": ["tubular-heaters", "strip-heaters", "thermocouples-and-sensors"],
},
]

FAMILY_BY_SLUG = {f["slug"]: f for f in FAMILIES}

# ---------------------------------------------------------------- industries

# Zone temperatures are typical for the process, not Swiftheat ratings. Every
# industry page says so under the table. `band` is 0 to 3 and only drives the
# colour of the zone on the process diagram.

INDUSTRIES = [
{
 "slug": "injection-moulding",
 "name": "Injection Moulding",
 "nav": "Injection moulding",
 "lede": "Every zone on the machine, from the dryer to the mould, with the element type that suits it.",
 "problem": "One machine, six heating problems, and each one wants a different element.",
 "meta": "Heaters for injection moulding machines: barrel band heaters, nozzle and coil heaters, hot "
         "runner manifold heaters, mould and platen cartridge heaters. Made in Peenya, Bangalore.",
 "zones": [
   ("Hopper and material dryer", "Air heating, continuous", "60 to 120 °C", 0, "tubular-heaters",
    "Large surface area into moving air, so the sheath stays cool"),
   ("Barrel zones 1 to 4", "Banded surface, continuous", "160 to 300 °C", 2, "band-heaters",
    "Even heat around a cylinder, clamped to suit a worn barrel"),
   ("Nozzle", "Tight space, fast response", "180 to 300 °C", 2, "nozzle-heaters",
    "High watt density in very little room, thermocouple built in"),
   ("Hot runner manifold and nozzles", "Precise, zoned", "180 to 320 °C", 3, "coil-heaters",
    "Profiled pitch along the flow path, so the melt does not stall at the ends"),
   ("Mould and platen", "Embedded in metal", "40 to 200 °C", 1, "cartridge-heaters",
    "Bore mounted, sized to the fit tolerance in your own tool"),
   ("Control loop", "Measurement", "-", 0, "thermocouples-and-sensors",
    "Type J or K to match the controller, immersion length measured to the melt"),
 ],
 "notes": [
   ("Thermocouple placement in a manifold",
    "A manifold thermocouple that sits in the steel rather than close to the flow channel reports a "
    "temperature the melt never sees. When the controller then holds that number, the material "
    "either degrades or freezes off at the gate. Tell us the distance from the seating face to where "
    "the junction has to sit, and which end the cable has to leave from."),
   ("Band clamping on a worn barrel",
    "Barrels wear oval and they wear undersize. A band sized to the machine's original drawing "
    "grips at two points and heats air at the rest. Measure the barrel where the heater sits, and "
    "if the machine is old, say so: a spring loaded or wedge lock clamping style will hold pressure "
    "where a plain strap will not."),
   ("Bore fit in mould and platen work",
    "Cartridge heater life in a mould is decided almost entirely by the clearance between the heater "
    "and the hole. Send the bore diameter and its tolerance from your own drawing. We will size the "
    "heater to that fit rather than shipping a standard part and hoping it is close enough."),
 ],
 "checklist": [
   "Machine make, model and clamping force",
   "Barrel diameter measured at each zone, and how worn it is",
   "Zone temperatures the process actually runs at",
   "Nozzle outside diameter and the bore it passes through",
   "Number of hot runner zones and the manifold drawing if you have it",
   "Bore diameter and tolerance for any mould or platen cartridges",
   "What the controller is set to read, Type J or Type K",
 ],
 "products": ["band-heaters", "nozzle-heaters", "coil-heaters", "cartridge-heaters", "tubular-heaters", "thermocouples-and-sensors"],
},
{
 "slug": "extrusion",
 "name": "Extrusion",
 "nav": "Extrusion",
 "lede": "Barrel, adapter and die head heating for pipe, profile, sheet and film lines.",
 "problem": "A long barrel, a lot of zones, and a die head that has to hold temperature across its face.",
 "meta": "Heaters for extrusion lines: barrel band heaters, adapter and die head heaters, hopper air "
         "heating and zone thermocouples. Made in Peenya, Bangalore.",
 "zones": [
   ("Hopper and drying", "Air heating", "60 to 120 °C", 0, "tubular-heaters",
    "Finned or tubular elements into moving air"),
   ("Feed zone", "Banded, controlled cooling too", "140 to 200 °C", 1, "band-heaters",
    "Even band coverage with room for the cooling fans"),
   ("Barrel zones", "Banded surface, continuous", "180 to 300 °C", 2, "band-heaters",
    "Ceramic where the zone runs hot, mica where the clearance is tight"),
   ("Adapter and screen changer", "Awkward shapes", "200 to 300 °C", 2, "band-heaters",
    "Partial coverage bands and strip heaters made to the casting"),
   ("Die head", "Zoned, must be even across the face", "200 to 320 °C", 3, "coil-heaters",
    "Coil heaters wound to the tool, pitch profiled to even out the face"),
   ("Control loop", "Measurement", "-", 0, "thermocouples-and-sensors",
    "Immersion length measured to the melt channel, not to the casting"),
 ],
 "notes": [
   ("Partial coverage where the casting is not round",
    "Adapters, screen changers and die bodies are rarely a clean cylinder. A partial coverage band "
    "made to a stated angle, or a strip heater made to the flat, puts heat where the metal actually "
    "is instead of bridging the gaps."),
   ("Zone counts and spares",
    "An extrusion line stops for one failed band. Standardising the barrel zones onto as few "
    "different sizes as the machine allows means one spare covers several zones. Send us the zone "
    "list and we will tell you where the sizes can be consolidated."),
   ("Cooling fans and band construction",
    "On a feed zone that is cooled as well as heated, the band has to leave the fan path clear. Say "
    "where the fans sit and we will position the terminals and the coverage around them."),
 ],
 "checklist": [
   "Line type: pipe, profile, sheet, film or compounding",
   "Barrel diameter and the number of zones",
   "Measured inside diameter and width for each band position",
   "Cutouts needed for fans, sensors or bolts, with positions",
   "Die head drawing, or the diameter and length of each coil position",
   "Zone temperatures and the material being run",
 ],
 "products": ["band-heaters", "coil-heaters", "strip-heaters", "tubular-heaters", "thermocouples-and-sensors"],
},
{
 "slug": "blow-moulding",
 "name": "Blow Moulding",
 "nav": "Blow moulding",
 "lede": "Preform reheat, extrusion head and neck tooling heating for PET and extrusion blow lines.",
 "problem": "The reheat oven is a radiant problem, and everything after it is a contact problem.",
 "meta": "Heaters for blow moulding: ceramic infrared preform reheat elements, extrusion head band "
         "and coil heaters, neck tooling cartridge heaters. Made in Peenya, Bangalore.",
 "zones": [
   ("Preform reheat oven", "Radiant, line speed dependent", "90 to 120 °C at the wall", 1, "ceramic-infrared-heaters",
    "Radiation reaches the preform wall without heating the tunnel air"),
   ("Extruder barrel", "Banded surface, continuous", "160 to 260 °C", 2, "band-heaters",
    "Standard barrel banding for extrusion blow machines"),
   ("Head and die", "Zoned, even across the face", "180 to 280 °C", 3, "coil-heaters",
    "Wound to the head, pitch profiled so the parison wall is even"),
   ("Neck and mould tooling", "Embedded in metal", "40 to 150 °C", 1, "cartridge-heaters",
    "Bore mounted in the neck tooling, sized to your fit"),
   ("Control loop", "Measurement", "-", 0, "thermocouples-and-sensors",
    "Fast junctions where the oven is controlled on line speed"),
 ],
 "notes": [
   ("Reheat is about intensity, not wattage",
    "A preform passing an oven at speed absorbs what reaches its surface in the time it is in front "
    "of the element. Distance from the element to the preform matters more than the total wattage "
    "installed. Tell us the gap, the line speed and the preform material."),
   ("Parison wall thickness follows head temperature",
    "An uneven head gives an uneven parison and a bottle with a thin spot. Coil pitch is the tool for "
    "that: more turns where the tooling steals heat, fewer where it does not."),
   ("Neck tooling runs cool and still fails",
    "Neck tooling cartridges are low temperature and often ignored, but the bores are small and the "
    "fit is usually loose after a few changes. Send the bore diameter and tolerance."),
 ],
 "checklist": [
   "Process type: injection stretch blow, extrusion blow or reheat stretch blow",
   "Oven length, number of element positions and the distance to the preform",
   "Preform material and target wall temperature",
   "Head and die dimensions, or a drawing",
   "Barrel diameter and zone widths",
   "Neck tooling bore diameters and tolerances",
 ],
 "products": ["ceramic-infrared-heaters", "band-heaters", "coil-heaters", "nozzle-heaters", "cartridge-heaters", "thermocouples-and-sensors"],
},
{
 "slug": "packaging-machinery",
 "name": "Packaging Machinery",
 "nav": "Packaging",
 "lede": "Sealing bars, cutting and creasing tools, shrink tunnels and hot melt tanks.",
 "problem": "Short cycles, tight tolerances on the seal, and a machine that cannot stop.",
 "meta": "Heaters for packaging machinery: sealing bar strip and cartridge heaters, shrink tunnel air "
         "heating, hot melt tank heating and sealing jaw sensors. Made in Peenya, Bangalore.",
 "zones": [
   ("Film unwind and preheat", "Gentle, radiant or air", "40 to 90 °C", 0, "ceramic-infrared-heaters",
    "Radiant preheat without dragging the film through hot air"),
   ("Sealing bars and jaws", "Cyclic, fast response", "120 to 250 °C", 2, "cartridge-heaters",
    "Bore mounted along the bar, so the seal face is even end to end"),
   ("Long seal bars and platens", "Flat surface", "120 to 220 °C", 2, "strip-heaters",
    "Clamped to the flat, hole pattern made to your drawing"),
   ("Cutting and creasing tools", "Cyclic, embedded", "100 to 200 °C", 1, "cartridge-heaters",
    "Small diameter cartridges in the tool body"),
   ("Shrink tunnel", "Air heating, high flow", "120 to 220 °C", 2, "tubular-heaters",
    "Finned tubular elements into the air stream"),
   ("Hot melt tank", "Liquid or block", "140 to 180 °C", 1, "strip-heaters",
    "Clamped to the tank wall, or cartridges into the block"),
 ],
 "notes": [
   ("An even seal face is a heater layout problem",
    "A sealing bar heated by one cartridge in the middle is hotter in the middle. Multiple cartridges "
    "at the right pitch, or a distributed wattage element, is what gives a seal that passes at both "
    "ends of the bar. Send us the bar drawing and the seal temperature."),
   ("Cyclic duty is harder than continuous",
    "Packaging tools switch on and off constantly. That is thermal cycling, and a heater specified "
    "for continuous running at the same wattage will not last as long. Say how many cycles an hour "
    "the machine runs."),
   ("Leads move, so protect them",
    "On a reciprocating jaw the lead flexes every cycle. Armour or braided metal sleeve at the exit "
    "is the difference between a heater that lasts a year and one that lasts a month."),
 ],
 "checklist": [
   "Machine type: form fill seal, flow wrap, cartoning, shrink or labelling",
   "Sealing bar length, section and the existing hole pattern",
   "Seal temperature and cycles per hour",
   "Whether the heated part moves in service",
   "Tunnel dimensions and air flow for shrink applications",
   "Existing part numbers or old elements you are replacing",
 ],
 "products": ["cartridge-heaters", "strip-heaters", "tubular-heaters", "ceramic-infrared-heaters", "band-heaters", "thermocouples-and-sensors"],
},
{
 "slug": "die-and-mould",
 "name": "Die and Mould",
 "nav": "Die and mould",
 "lede": "Hot stamping dies, press platens and mould preheat, where the heater lives inside the tool.",
 "problem": "The tool is expensive, the bores are already machined, and the heater has to fit them exactly.",
 "meta": "Heaters for dies and moulds: cartridge heaters for hot stamping tools and press platens, "
         "mould preheat and tool sensors. Made in Peenya, Bangalore.",
 "zones": [
   ("Press platens", "Embedded, continuous", "100 to 300 °C", 2, "cartridge-heaters",
    "Bore mounted across the platen, wattage distributed to keep the face even"),
   ("Hot stamping and forming dies", "Embedded, cyclic", "120 to 300 °C", 2, "cartridge-heaters",
    "Small diameter cartridges close to the working face"),
   ("Mould preheat", "Embedded or clamped", "40 to 200 °C", 1, "cartridge-heaters",
    "Cartridges in the bolster, or strip heaters on the flat"),
   ("Tool face plates", "Flat surface", "100 to 250 °C", 2, "strip-heaters",
    "Clamped to a machined face, hole pattern to your drawing"),
   ("Control loop", "Measurement", "-", 0, "thermocouples-and-sensors",
    "Sensor bores are usually already in the tool, so the diameter is fixed"),
 ],
 "notes": [
   ("The bore is already there, so the heater is made to it",
    "In tool work the hole exists before the heater does. Send the bore diameter with its tolerance "
    "and the depth. We size the heater to that fit, which is the single biggest lever on how long it "
    "will last."),
   ("Distributed wattage across a platen",
    "A platen heated by identical cartridges is hotter in the middle, because the edges lose heat. "
    "Uneven wattage along the heater, or a different wattage in the edge bores, evens the face out. "
    "Tell us the platen size and how flat the face has to be."),
   ("Removal matters as much as installation",
    "A cartridge that has run for a year in a mould can seize in the bore. A removal aid, or a "
    "sacrificial anti seize on assembly, turns a two hour job into a five minute one. Ask for it "
    "when the tool is expected to be serviced in place."),
 ],
 "checklist": [
   "Tool type and the process it runs",
   "Bore diameter, tolerance and depth for every heated position",
   "Number of bores and their layout across the tool",
   "Working temperature and how flat the face has to be",
   "Whether the tool is serviced in place",
   "Sensor bore diameter and depth",
 ],
 "products": ["cartridge-heaters", "strip-heaters", "tubular-heaters", "thermocouples-and-sensors"],
},
{
 "slug": "food-processing",
 "name": "Food Processing",
 "nav": "Food processing",
 "lede": "Tanks, sealing tools, dryers and jacketed lines, in plant that gets washed down.",
 "problem": "Everything here is either immersed, sealed against water, or both.",
 "meta": "Heaters for food processing plant: immersion tubular heaters, sealing bar heaters, hot air "
         "drying and washdown rated terminations. Made in Peenya, Bangalore.",
 "zones": [
   ("Process tanks and vats", "Immersed, continuous", "60 to 120 °C", 0, "tubular-heaters",
    "Immersion elements with the sheath chosen for the medium"),
   ("Hot air drying and baking", "Air heating, high flow", "80 to 250 °C", 2, "tubular-heaters",
    "Finned elements into moving air"),
   ("Sealing and forming tools", "Cyclic, fast response", "120 to 220 °C", 2, "cartridge-heaters",
    "Bore mounted in the tool, washdown rated lead protection"),
   ("Long sealing bars", "Flat surface", "120 to 200 °C", 2, "strip-heaters",
    "Clamped to the bar, sealed terminal box"),
   ("Surface and radiant heating", "Radiant", "100 to 250 °C", 1, "ceramic-infrared-heaters",
    "Heats the product surface without heating the whole enclosure"),
   ("Control loop", "Measurement", "-", 0, "thermocouples-and-sensors",
    "Stainless sheaths and sealed heads"),
 ],
 "notes": [
   ("Washdown decides the termination, not the element",
    "Most heater failures in a food plant are water finding a terminal, not the element wearing out. "
    "A sealed terminal box, a proper gland and a lead protection rated for the wash cycle are worth "
    "more than a higher grade sheath."),
   ("Sheath material follows the medium",
    "Water, brine, syrup, oil and cleaning chemicals all attack differently. Chloride in particular "
    "pits stainless. Tell us what the element sits in, including what is used to clean it."),
   ("Dry running protection on every tank",
    "An immersion element switched on in an empty tank fails within seconds. Low level protection is "
    "part of the installation, not an optional extra."),
 ],
 "checklist": [
   "What is being heated, and what the vessel is made of",
   "Whether the plant is washed down, and with what",
   "Operating temperature and whether the duty is continuous",
   "Tank dimensions and the mounting available: flange, boss or over the side",
   "Any food contact requirement that affects material choice",
   "Existing element dimensions if this is a replacement",
 ],
 "products": ["tubular-heaters", "cartridge-heaters", "strip-heaters", "ceramic-infrared-heaters", "thermocouples-and-sensors"],
},
{
 "slug": "pharmaceutical-machinery",
 "name": "Pharmaceutical Machinery",
 "nav": "Pharma machinery",
 "lede": "Blister and tube sealing, granulation drying, jacketed vessels and validated temperature "
         "measurement.",
 "problem": "Repeatability is the specification. A process that drifts is a batch that fails.",
 "meta": "Heaters for pharmaceutical machinery: blister forming and sealing heaters, granulation "
         "dryer air heating, jacketed vessel elements and PT100 sensors. Made in Peenya, Bangalore.",
 "zones": [
   ("Fluid bed and granulation dryers", "Air heating, continuous", "40 to 120 °C", 0, "tubular-heaters",
    "Finned elements into a clean, high flow air stream"),
   ("Blister forming station", "Cyclic, flat tool", "110 to 160 °C", 1, "cartridge-heaters",
    "Bore mounted in the forming plate, even across the web"),
   ("Blister sealing station", "Cyclic, flat tool", "150 to 220 °C", 2, "cartridge-heaters",
    "Distributed wattage so every cavity seals the same"),
   ("Tube and sachet sealing", "Cyclic, small tools", "140 to 220 °C", 2, "cartridge-heaters",
    "Small diameter cartridges, protected leads on a moving jaw"),
   ("Jacketed vessels", "Immersed or clamped", "40 to 150 °C", 1, "tubular-heaters",
    "Sheath chosen for the jacket medium"),
   ("Control loop", "Measurement", "-", 0, "thermocouples-and-sensors",
    "PT100 where stability and repeatability matter more than speed"),
 ],
 "notes": [
   ("PT100 where the record matters",
    "A platinum RTD drifts less than a thermocouple and repeats better between sensors. On a process "
    "that has to produce the same record batch after batch, that stability is the reason to choose "
    "it, even though it is slower."),
   ("Even sealing across every cavity",
    "A sealing plate that is two degrees cooler at one corner produces a blister that fails leak "
    "testing in exactly that corner. Distributed wattage and a measured hole pattern are how that is "
    "fixed at the heater rather than at the controller."),
   ("Clean air means clean elements",
    "In a granulation dryer the element sits in the air path that reaches the product. Finish, "
    "sheath material and the absence of anything that can shed matter as much as the wattage."),
 ],
 "checklist": [
   "Machine type: blister, tube filling, granulation, coating or filling",
   "Tool or plate dimensions and the existing bore pattern",
   "Operating temperature and the tolerance the process is validated to",
   "Cycles per hour",
   "Sensor type the controller expects, and whether PT100 is required",
   "Any material or documentation requirement that affects sheath choice",
 ],
 "products": ["cartridge-heaters", "tubular-heaters", "thermocouples-and-sensors", "strip-heaters", "ceramic-infrared-heaters"],
},
{
 "slug": "rubber",
 "name": "Rubber and Elastomers",
 "nav": "Rubber",
 "lede": "Curing and vulcanising platens, extruder barrels and mould heating.",
 "problem": "Long soaks at temperature, big platens, and cure that depends on the whole face being even.",
 "meta": "Heaters for rubber processing: curing and vulcanising platen cartridge heaters, extruder "
         "band heaters, mould heating and platen sensors. Made in Peenya, Bangalore.",
 "zones": [
   ("Curing and vulcanising platens", "Embedded, continuous", "140 to 220 °C", 2, "cartridge-heaters",
    "Bore mounted across the platen, wattage distributed for an even face"),
   ("Moulds and bolsters", "Embedded", "140 to 200 °C", 2, "cartridge-heaters",
    "Sized to the bores already in the tool"),
   ("Extruder barrel", "Banded surface, continuous", "60 to 120 °C", 1, "band-heaters",
    "Rubber barrels run cooler than plastics, so watt density is lower"),
   ("Preheat and warm up", "Radiant or air", "40 to 120 °C", 0, "ceramic-infrared-heaters",
    "Brings stock and tooling up before the run starts"),
   ("Control loop", "Measurement", "-", 0, "thermocouples-and-sensors",
    "Platen sensors sized to the bores already drilled"),
 ],
 "notes": [
   ("Cure is decided by the coldest point on the platen",
    "The whole face has to be within the cure window, so the specification is the spread across the "
    "platen, not the average. Tell us the platen size, the bore layout and the spread you have to "
    "hold."),
   ("Rubber barrels are not plastics barrels",
    "An extruder running rubber works at a much lower temperature than one running plastics, and it "
    "wants a lower watt density to match. Reusing a plastics band specification here shortens element "
    "life for no benefit."),
   ("Long soaks favour a conservative loading",
    "Rubber tooling sits at temperature for hours at a time. A heater specified conservatively is "
    "cheaper over a year than one specified for the fastest possible heat up."),
 ],
 "checklist": [
   "Process: compression, transfer, injection or extrusion",
   "Platen or tool dimensions and the bore layout",
   "Bore diameter, tolerance and depth",
   "Cure temperature and the spread the process allows",
   "Hours at temperature per day",
   "Barrel diameter and zone widths for extrusion",
 ],
 "products": ["cartridge-heaters", "band-heaters", "strip-heaters", "ceramic-infrared-heaters", "thermocouples-and-sensors"],
},
{
 "slug": "industrial-heating",
 "name": "Other Industrial Heating",
 "nav": "Other industrial",
 "lede": "Ovens, tanks, ducts, pipes and surfaces, in plant that does not fit any of the categories "
         "above.",
 "problem": "The application is one of a kind, so the element has to be made rather than picked.",
 "meta": "Industrial heating elements made to order in Peenya, Bangalore: duct and oven air heating, "
         "tank immersion elements, pipe and surface heating, drying and preheating.",
 "zones": [
   ("Ducts and air handling", "Air heating, high flow", "40 to 300 °C", 1, "tubular-heaters",
    "Finned elements sized to the duct and the air velocity"),
   ("Ovens and drying cabinets", "Air heating, enclosed", "60 to 300 °C", 2, "tubular-heaters",
    "Element banks laid out to the cabinet, with even circulation"),
   ("Tanks and vats", "Immersed", "40 to 150 °C", 0, "tubular-heaters",
    "Sheath material chosen for the medium, flange or boss mounted"),
   ("Surfaces, plates and pipes", "Clamped", "60 to 250 °C", 1, "strip-heaters",
    "Clamped to the flat, or a bent element to the pipe"),
   ("Radiant and surface drying", "Radiant", "80 to 300 °C", 2, "ceramic-infrared-heaters",
    "Puts the energy on the surface instead of into the room"),
   ("Control loop", "Measurement", "-", 0, "thermocouples-and-sensors",
    "Sized to whatever fitting the plant already has"),
 ],
 "notes": [
   ("Tell us the problem, not the part",
    "For one off applications the most useful enquiry describes what has to get hot, from what "
    "temperature to what temperature, how quickly, and what the element can be mounted to. The part "
    "follows from that."),
   ("Air, liquid and metal are three different specifications",
    "The same element cannot be loaded the same way in all three. Still air is the hardest duty, "
    "flowing liquid the easiest. State the medium and whether it moves."),
   ("Replacing something that already exists",
    "If there is an old element, its dimensions and its rating are the fastest route to a correct "
    "replacement. A photograph of the label, or the element beside a tape measure, is usually enough "
    "to start."),
 ],
 "checklist": [
   "What has to be heated, and what it is made of",
   "Start temperature, target temperature and how quickly",
   "The medium: still air, moving air, liquid, or metal contact",
   "Space available and how the element can be mounted",
   "Supply voltage and whether it is single or three phase",
   "Photograph or dimensions of any element being replaced",
 ],
 "products": ["tubular-heaters", "strip-heaters", "ceramic-infrared-heaters", "cartridge-heaters", "thermocouples-and-sensors"],
},
]

INDUSTRY_BY_SLUG = {i["slug"]: i for i in INDUSTRIES}

# ---------------------------------------------------------------- enquiry fields
# The specification block on each product page. Same names, ranges and option
# codes as the list builder, so an enquiry and a generated document describe the
# same part in the same words.
# (id, label, kind, extra)  kind: select | text | number
#   select -> extra is the option list
#   number -> extra is (min, max, unit)
#   text   -> extra is the placeholder

FORMS = {
 "cartridge-heaters": [
   ("dia", "Sheath diameter D", "select", ["6.5 mm","8 mm","10 mm","12.5 mm","16 mm","19 mm","25 mm","Other, see notes"]),
   ("len", "Overall length L", "number", (35, 1500, "mm")),
   ("hlen", "Heated length HL", "number", (20, 1500, "mm")),
   ("watt", "Wattage", "number", (20, 6000, "W")),
   ("volt", "Voltage", "select", ["110 V","230 V","240 V","415 V"]),
   ("sheath", "Sheath material", "select", ["Stainless steel","Incoloy 800","Recommend one"]),
   ("term", "Termination", "select", ["T1 single end, straight","T2 single end, right angle","T3 double ended"]),
   ("lead", "Lead protection", "select", ["L1 silicone coated fibreglass","L2 PTFE","L3 braided metal sleeve","L4 armour cable","L5 ceramic beading"]),
   ("leadlen", "Lead length LL", "number", (50, 5000, "mm")),
   ("tc", "Inbuilt thermocouple", "select", ["TC0 none","TCJ type J","TCK type K","TCG grounded junction"]),
   ("bore", "Bore diameter in your part", "text", "mm, with tolerance"),
   ("mount", "Mounting", "select", ["M0 none","M1 round flange","M2 threaded fitting","M3 T strain clamp"]),
 ],
 "coil-heaters": [
   ("id", "Inside diameter", "number", (8, 120, "mm")),
   ("hlen", "Heated length", "number", (20, 600, "mm")),
   ("tlen", "Total length including cold ends", "number", (20, 800, "mm")),
   ("watt", "Wattage", "number", (100, 3000, "W")),
   ("volt", "Voltage", "select", ["110 V","230 V","240 V"]),
   ("prof", "Profile", "select", ["PR round","PS square","PT rectangular"]),
   ("exit", "Lead exit", "select", ["EA axial","ER radial","ET tangential"]),
   ("tc", "Inbuilt thermocouple", "select", ["TC0 none","TCJ type J","TCK type K"]),
   ("tcpos", "Thermocouple position", "text", "distance from which end"),
   ("leadlen", "Lead length", "number", (50, 5000, "mm")),
 ],
 "band-heaters": [
   ("id", "Inside diameter", "number", (20, 800, "mm")),
   ("width", "Width", "number", (20, 400, "mm")),
   ("watt", "Wattage", "number", (100, 9000, "W")),
   ("volt", "Voltage", "select", ["230 V","240 V","415 V"]),
   ("mat", "Material", "select", ["CE ceramic","MI mica","Recommend one"]),
   ("con", "Construction", "select", ["C1 one piece","C2 two piece","CE1 expandable","CP partial coverage"]),
   ("angle", "Angle of coverage", "text", "partial coverage only"),
   ("clamp", "Clamping", "select", ["K1 built in strap","K2 separate strap","K3 wedge lock","K4 spring loaded"]),
   ("term", "Termination", "select", ["S1 screw terminals","S2 post terminals","S3 flying leads","S4 terminal box"]),
   ("termpos", "Termination position", "text", "clock position on the circumference"),
   ("cutouts", "Cutouts and holes", "text", "size and position, or send a drawing"),
   ("blanket", "Insulation blanket", "select", ["No","Yes"]),
 ],
 "nozzle-heaters": [
   ("od", "Nozzle outside diameter", "number", (10, 150, "mm")),
   ("hlen", "Heated length", "number", (20, 400, "mm")),
   ("watt", "Wattage", "number", (100, 3000, "W")),
   ("volt", "Voltage", "select", ["110 V","230 V","240 V"]),
   ("mat", "Material", "select", ["CE ceramic","MI mica","Recommend one"]),
   ("wall", "Wall thickness available", "text", "the bore the nozzle passes through"),
   ("tc", "Inbuilt thermocouple", "select", ["TC0 none","TCJ type J","TCK type K"]),
   ("tcpos", "Thermocouple position", "text", "distance from the gate end"),
   ("termpos", "Termination position", "text", "clock position"),
 ],
 "strip-heaters": [
   ("len", "Length", "number", (60, 2000, "mm")),
   ("width", "Width", "number", (20, 150, "mm")),
   ("watt", "Wattage", "number", (100, 6000, "W")),
   ("volt", "Voltage", "select", ["230 V","240 V","415 V"]),
   ("prof", "Profile", "select", ["F0 plain","F1 finned"]),
   ("holes", "Mounting holes", "text", "quantity, diameter and positions"),
   ("term", "Termination", "select", ["S1 screw terminals","S3 flying leads"]),
   ("mounting", "What it mounts to", "text", "clamped to metal, or free air"),
 ],
 "tubular-heaters": [
   ("dia", "Sheath diameter", "select", ["6.5 mm","8 mm","8.5 mm","11 mm","12.5 mm","16 mm"]),
   ("len", "Overall length", "number", (100, 4000, "mm")),
   ("hlen", "Heated length", "number", (50, 4000, "mm")),
   ("watt", "Wattage", "number", (100, 9000, "W")),
   ("volt", "Voltage", "select", ["230 V","240 V","415 V"]),
   ("bend", "Bend form", "select", ["B0 straight","BU U form","BW W form","BC coiled, drawing attached"]),
   ("sheath", "Sheath material", "select", ["SS stainless steel","IN Incoloy","MS mild steel","CU copper","Recommend one"]),
   ("term", "Terminal", "select", ["S0 studs","S1 screw terminals","S3 flying leads"]),
   ("medium", "What it heats", "select", ["Still air","Moving air","Water","Oil","Other liquid","Metal contact"]),
   ("mounting", "Mounting", "text", "flange, boss, thread or bracket"),
 ],
 "thermocouples-and-sensors": [
   ("type", "Type", "select", ["J thermocouple","K thermocouple","PT100 RTD","PT500 RTD","PT1000 RTD"]),
   ("dia", "Sheath diameter", "select", ["1.5 mm","3 mm","4.5 mm","6 mm","8 mm"]),
   ("len", "Immersion length", "number", (20, 2000, "mm")),
   ("clen", "Cable length", "number", (100, 10000, "mm")),
   ("junc", "Junction", "select", ["G grounded","U ungrounded","E exposed"]),
   ("conn", "Connection", "select", ["P plug","B bare tails","H terminal head"]),
   ("style", "Style", "select", ["Insertion","Bayonet","Washer","Surface","Spring loaded"]),
   ("thread", "Process thread or fitting", "text", "if one is required"),
   ("ctrl", "Controller make and model", "text", "so the type matches"),
 ],
 "ceramic-infrared-heaters": [
   ("form", "Element form", "select", ["FT trough","FF flat panel","FH hollow","Recommend one"]),
   ("watt", "Wattage per element", "number", (100, 2000, "W")),
   ("volt", "Voltage", "select", ["230 V","240 V"]),
   ("count", "How many elements", "number", (1, 999, "nos")),
   ("dist", "Distance to the work", "number", (20, 1000, "mm")),
   ("target", "Target surface temperature", "text", "degrees C"),
   ("material", "Material being heated", "text", "PET, board, coating, food"),
   ("tc", "Inbuilt thermocouple", "select", ["TC0 none","TCK type K"]),
   ("refl", "Reflector", "select", ["R0 none","R1 fitted"]),
   ("speed", "Line speed or dwell time", "text", "for continuous processes"),
 ],
}


def _industries_for(slug):
    """Every industry that names this family, either in its product shortlist or
    in one of its heating zones."""
    out = []
    for ind in INDUSTRIES:
        if slug in ind["products"] or any(z[4] == slug for z in ind["zones"]):
            out.append(ind["slug"])
    return out


# One source of truth, in one direction. An industry page claims a product by
# putting it in a zone or on its shortlist; the product page's "where these are
# used" cards and the finder facet are both read back from that. Neither can
# claim an application the other does not.
for _f in FAMILIES:
    _f["industries"] = _industries_for(_f["slug"])
    _f["facets"]["industry"] = "|".join(_f["industries"])
    assert _f["industries"], _f["slug"]
