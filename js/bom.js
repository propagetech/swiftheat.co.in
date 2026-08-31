/* Heater list builder.
   Everything runs in the page. No backend, no storage, no account.
   The finished list leaves as a printed PDF, an email composed in the
   visitor's own mail app, or a WhatsApp message. */
(function () {
  'use strict';

  var SVGNS = 'http://www.w3.org/2000/svg';
  var ink = 'hsl(214 32% 11%)', heat = 'hsl(20 75% 50%)', soft = 'hsl(214 16% 80%)';

  function icon(paths) {
    return '<svg viewBox="0 0 72 44" aria-hidden="true"><g fill="none" stroke="' + ink +
      '" stroke-width="1.7" stroke-linecap="round">' + paths + '</g></svg>';
  }

  /* ---------- product families ---------- */
  var FAMILIES = [
    { key: 'cartridge', view: 'cylinder', dims: ['dia','len','hlen'], code: 'CH', name: 'Cartridge',
      blurb: 'Bore mounted in moulds and platens',
      icon: icon('<rect x="8" y="16" width="42" height="13" rx="3"/><path d="M50 19h14M50 26h14"/>'),
      specs: [
        { k: 'dia',  label: 'Diameter Ø D', unit: 'mm', type: 'select',
          opts: ['6.5','8','10','12.5','16','19','25'] },
        { k: 'len',  label: 'Overall length L', unit: 'mm', type: 'number', min: 35, max: 1500 },
        { k: 'hlen', label: 'Heated length HL', unit: 'mm', type: 'number', min: 20, max: 1500, optional: true },
        { k: 'watt', label: 'Wattage', unit: 'W', type: 'number', min: 20, max: 6000 },
        { k: 'volt', label: 'Voltage', unit: 'V', type: 'select', opts: ['110','230','240','415'] }
      ],
      groups: [
        { title: 'Termination', k: 'term', opts: [
          { c: 'T1', t: 'Straight', d: 'Axial exit from one end' },
          { c: 'T2', t: 'Right angle', d: 'For tight clearance' },
          { c: 'T3', t: 'Double ended', d: 'One lead each end' } ] },
        { title: 'Lead protection', k: 'lead', opts: [
          { c: 'L1', t: 'Fibreglass', d: 'General purpose' },
          { c: 'L3', t: 'Metal braid', d: 'Abrasion resistance' },
          { c: 'L4', t: 'Armour', d: 'Full mechanical protection' },
          { c: 'L5', t: 'Ceramic bead', d: 'Highest exit temperature' } ] },
        { title: 'Inbuilt thermocouple', k: 'tc', opts: [
          { c: 'TC0', t: 'None', d: 'Control from a separate sensor' },
          { c: 'TCJ', t: 'Type J', d: 'Iron constantan' },
          { c: 'TCK', t: 'Type K', d: 'Higher range' },
          { c: 'TCG', t: 'Grounded', d: 'Faster response' } ] },
        { title: 'Mounting', k: 'mount', opts: [
          { c: 'M0', t: 'None', d: 'Plain sheath' },
          { c: 'M1', t: 'Round flange', d: 'Surface mounting' },
          { c: 'M2', t: 'Threaded', d: 'NPT or BSP' },
          { c: 'M3', t: 'Strain clamp', d: 'Where the lead is pulled' } ] }
      ] },

    { key: 'coil', view: 'coil', dims: ['id','hlen'], code: 'CO', name: 'Coil',
      blurb: 'Hot runner nozzles and manifolds',
      icon: icon('<path d="M10 22c0-6 5-6 5 0s5 6 5 0 5-6 5 0 5 6 5 0 5-6 5 0 5 6 5 0 5-6 5 0"/><path d="M56 22h8"/>'),
      specs: [
        { k: 'id',   label: 'Inside diameter', unit: 'mm', type: 'number', min: 8, max: 120 },
        { k: 'hlen', label: 'Heated length', unit: 'mm', type: 'number', min: 20, max: 600 },
        { k: 'watt', label: 'Wattage', unit: 'W', type: 'number', min: 100, max: 3000 },
        { k: 'volt', label: 'Voltage', unit: 'V', type: 'select', opts: ['110','230','240'] }
      ],
      groups: [
        { title: 'Profile', k: 'prof', opts: [
          { c: 'PR', t: 'Round', d: 'Round section wire' },
          { c: 'PS', t: 'Square', d: 'Square section' },
          { c: 'PT', t: 'Rectangular', d: 'Flat section, more contact' } ] },
        { title: 'Lead exit', k: 'exit', opts: [
          { c: 'EA', t: 'Axial', d: 'Along the axis' },
          { c: 'ER', t: 'Radial', d: 'Out of the side' },
          { c: 'ET', t: 'Tangential', d: 'Off the tangent' } ] },
        { title: 'Inbuilt thermocouple', k: 'tc', opts: [
          { c: 'TC0', t: 'None', d: '' },
          { c: 'TCJ', t: 'Type J', d: '' },
          { c: 'TCK', t: 'Type K', d: '' } ] }
      ] },

    { key: 'band', view: 'ring', dims: ['id','width'], code: 'BH', name: 'Band',
      blurb: 'Barrels and cylinders',
      icon: icon('<circle cx="26" cy="22" r="13"/><circle cx="26" cy="22" r="8"/><path d="M39 22h20"/>'),
      specs: [
        { k: 'id',    label: 'Inside diameter', unit: 'mm', type: 'number', min: 20, max: 800 },
        { k: 'width', label: 'Width', unit: 'mm', type: 'number', min: 20, max: 400 },
        { k: 'watt',  label: 'Wattage', unit: 'W', type: 'number', min: 100, max: 9000 },
        { k: 'volt',  label: 'Voltage', unit: 'V', type: 'select', opts: ['230','240','415'] }
      ],
      groups: [
        { title: 'Material', k: 'mat', opts: [
          { c: 'CE', t: 'Ceramic', d: 'Higher temperature, insulated' },
          { c: 'MI', t: 'Mica', d: 'Standard duty, thinner' } ] },
        { title: 'Construction', k: 'con', opts: [
          { c: 'C1', t: 'One piece', d: 'Full circle' },
          { c: 'C2', t: 'Two piece', d: 'Split, for fitted barrels' },
          { c: 'CE1', t: 'Expandable', d: 'Slides over the barrel' },
          { c: 'CP', t: 'Partial', d: 'Part coverage, state the angle' } ] },
        { title: 'Clamping', k: 'clamp', opts: [
          { c: 'K1', t: 'Built in strap', d: 'Integral barrel strap' },
          { c: 'K2', t: 'Separate strap', d: 'Removable' },
          { c: 'K3', t: 'Wedge lock', d: 'For frequent removal' },
          { c: 'K4', t: 'Spring loaded', d: 'Constant pressure' } ] },
        { title: 'Termination', k: 'term', opts: [
          { c: 'S1', t: 'Screw terminals', d: '' },
          { c: 'S2', t: 'Post terminals', d: '' },
          { c: 'S3', t: 'Leads', d: 'Flying leads' },
          { c: 'S4', t: 'Terminal box', d: '' } ] }
      ] },

    { key: 'nozzle', view: 'ring', dims: ['id','len'], code: 'NZ', name: 'Nozzle',
      blurb: 'Injection nozzles',
      icon: icon('<path d="M12 14h26l10 8-10 8H12z"/><path d="M48 22h12"/>'),
      specs: [
        { k: 'id',   label: 'Nozzle outside diameter', unit: 'mm', type: 'number', min: 10, max: 150 },
        { k: 'len',  label: 'Heated length', unit: 'mm', type: 'number', min: 20, max: 400 },
        { k: 'watt', label: 'Wattage', unit: 'W', type: 'number', min: 100, max: 3000 },
        { k: 'volt', label: 'Voltage', unit: 'V', type: 'select', opts: ['110','230','240'] }
      ],
      groups: [
        { title: 'Material', k: 'mat', opts: [
          { c: 'CE', t: 'Ceramic', d: '' }, { c: 'MI', t: 'Mica', d: '' } ] },
        { title: 'Inbuilt thermocouple', k: 'tc', opts: [
          { c: 'TC0', t: 'None', d: '' }, { c: 'TCJ', t: 'Type J', d: '' }, { c: 'TCK', t: 'Type K', d: '' } ] }
      ] },

    { key: 'strip', view: 'strip', dims: ['len','width'], code: 'SH', name: 'Strip',
      blurb: 'Flat and curved surfaces',
      icon: icon('<rect x="8" y="18" width="48" height="9" rx="2"/><path d="M16 18v9M28 18v9M40 18v9"/>'),
      specs: [
        { k: 'len',   label: 'Length', unit: 'mm', type: 'number', min: 60, max: 2000 },
        { k: 'width', label: 'Width', unit: 'mm', type: 'number', min: 20, max: 150 },
        { k: 'watt',  label: 'Wattage', unit: 'W', type: 'number', min: 100, max: 6000 },
        { k: 'volt',  label: 'Voltage', unit: 'V', type: 'select', opts: ['230','240','415'] }
      ],
      groups: [
        { title: 'Profile', k: 'prof', opts: [
          { c: 'F0', t: 'Plain', d: 'Flat strip' },
          { c: 'F1', t: 'Finned', d: 'For heating air' } ] },
        { title: 'Termination', k: 'term', opts: [
          { c: 'S1', t: 'Screw terminals', d: '' }, { c: 'S3', t: 'Leads', d: '' } ] }
      ] },

    { key: 'tubular', view: 'tube', dims: ['dia','len'], code: 'TH', name: 'Tubular',
      blurb: 'Air, liquids and surfaces',
      icon: icon('<path d="M10 30c0-12 12-16 20-16s20 4 20 16"/><path d="M10 30v4M50 30v4"/>'),
      specs: [
        { k: 'dia',  label: 'Sheath diameter', unit: 'mm', type: 'select', opts: ['6.5','8','8.5','11','12.5','16'] },
        { k: 'len',  label: 'Overall length', unit: 'mm', type: 'number', min: 100, max: 4000 },
        { k: 'watt', label: 'Wattage', unit: 'W', type: 'number', min: 100, max: 9000 },
        { k: 'volt', label: 'Voltage', unit: 'V', type: 'select', opts: ['230','240','415'] }
      ],
      groups: [
        { title: 'Bend form', k: 'bend', opts: [
          { c: 'B0', t: 'Straight', d: '' }, { c: 'BU', t: 'U form', d: '' },
          { c: 'BW', t: 'W form', d: '' }, { c: 'BC', t: 'Coiled', d: 'Send a drawing' } ] },
        { title: 'Sheath', k: 'sheath', opts: [
          { c: 'SS', t: 'Stainless', d: '' }, { c: 'IN', t: 'Incoloy', d: 'Higher temperature' },
          { c: 'MS', t: 'Mild steel', d: '' }, { c: 'CU', t: 'Copper', d: 'Water only' } ] },
        { title: 'Terminal', k: 'term', opts: [
          { c: 'S0', t: 'Studs', d: '' }, { c: 'S1', t: 'Screw terminals', d: '' }, { c: 'S3', t: 'Leads', d: '' } ] }
      ] },

    { key: 'sensor', view: 'probe', dims: ['dia','len','clen'], code: 'TS', name: 'Thermocouple',
      blurb: 'Sensors and RTDs',
      icon: icon('<path d="M12 22h28"/><circle cx="46" cy="22" r="6"/><path d="M12 16v12"/>'),
      specs: [
        { k: 'dia',  label: 'Sheath diameter', unit: 'mm', type: 'select', opts: ['1.5','3','4.5','6','8'] },
        { k: 'len',  label: 'Immersion length', unit: 'mm', type: 'number', min: 20, max: 2000 },
        { k: 'clen', label: 'Cable length', unit: 'mm', type: 'number', min: 100, max: 10000, optional: true }
      ],
      groups: [
        { title: 'Type', k: 'type', opts: [
          { c: 'J', t: 'Type J', d: '' }, { c: 'K', t: 'Type K', d: '' },
          { c: 'PT1', t: 'PT100', d: 'RTD' }, { c: 'PT5', t: 'PT500', d: 'RTD' } ] },
        { title: 'Junction', k: 'junc', opts: [
          { c: 'G', t: 'Grounded', d: 'Faster' }, { c: 'U', t: 'Ungrounded', d: 'Isolated' },
          { c: 'E', t: 'Exposed', d: 'Fastest, unprotected' } ] },
        { title: 'Connection', k: 'conn', opts: [
          { c: 'P', t: 'Plug', d: '' }, { c: 'B', t: 'Bare tails', d: '' }, { c: 'H', t: 'Terminal head', d: '' } ] }
      ] },

    { key: 'ir', view: 'panel', dims: ['dist'], code: 'IR', name: 'Ceramic infrared',
      blurb: 'Radiant heating',
      icon: icon('<path d="M14 28h26l-4-12H18z"/><path d="M46 14v16M52 17v10M58 20v4"/>'),
      specs: [
        { k: 'watt', label: 'Wattage', unit: 'W', type: 'number', min: 100, max: 2000 },
        { k: 'volt', label: 'Voltage', unit: 'V', type: 'select', opts: ['230','240'] },
        { k: 'dist', label: 'Distance to the work', unit: 'mm', type: 'number', min: 20, max: 1000, optional: true }
      ],
      groups: [
        { title: 'Element form', k: 'form', opts: [
          { c: 'FT', t: 'Trough', d: 'Focused' }, { c: 'FF', t: 'Flat panel', d: 'Even spread' },
          { c: 'FH', t: 'Hollow', d: '' } ] },
        { title: 'Inbuilt thermocouple', k: 'tc', opts: [
          { c: 'TC0', t: 'None', d: '' }, { c: 'TCK', t: 'Type K', d: '' } ] },
        { title: 'Reflector', k: 'refl', opts: [
          { c: 'R0', t: 'None', d: '' }, { c: 'R1', t: 'Fitted', d: 'Directs the radiation' } ] }
      ] }
  ];

  /* ---------- state ---------- */
  var current = null, spec = {}, chosen = {}, items = [], emptyNode = null;

  var $ = function (id) { return document.getElementById(id); };

  /* ---------- family tiles ---------- */
  function renderFamilies() {
    var ul = $('famTiles');
    ul.innerHTML = FAMILIES.map(function (f) {
      return '<li><button class="tile tile-fam" type="button" aria-pressed="false" data-fam="' + f.key + '">' +
        f.icon + '<span class="t">' + f.name + '</span><span class="d">' + f.blurb + '</span></button></li>';
    }).join('');
    ul.addEventListener('click', function (e) {
      var b = e.target.closest('[data-fam]');
      if (!b) return;
      selectFamily(b.getAttribute('data-fam'));
    });
  }

  function selectFamily(key) {
    current = FAMILIES.filter(function (f) { return f.key === key; })[0];
    spec = {}; chosen = {};
    [].forEach.call($('famTiles').querySelectorAll('[data-fam]'), function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-fam') === key));
    });
    $('viewToggle').hidden = !hasIso(current);
    if (!hasIso(current) && viewMode === 'iso') { /* keep the preference, render flat */ }
    // preselect the first option in every group before the first draw, so the
    // opening drawing already shows the configuration the part code describes
    current.groups.forEach(function (g) { chosen[g.k] = g.opts[0].c; });
    renderSpecs(); renderOptions();
    current.groups.forEach(function (g) { pick(g.k, chosen[g.k]); });
    reveal(function () {
      $('vizPanel').hidden = false;
      $('specStep').hidden = false; $('optStep').hidden = false; $('addStep').hidden = false;
    });
    update();
  }

  /* On a phone the drawing sits above the steps, so revealing it for the first
     time pushes everything down by its own height and the tile you just tapped
     jumps out from under your finger. Measure the shift and take it back. On a
     desktop the panel is in the rail and the shift is zero, so this is a no-op. */
  function reveal(show) {
    var anchor = $('famTiles');
    var before = anchor.getBoundingClientRect().top;
    show();
    /* everything is on the page before the correction, or the scroll is
       clamped by a document that has not grown yet */
    var after = anchor.getBoundingClientRect().top;
    /* instant, not the page's smooth scrolling: this is a correction that
       should never be seen, not a journey */
    if (Math.abs(after - before) > 1) {
      window.scrollBy({ top: after - before, left: 0, behavior: 'instant' });
    }
  }

  /* ---------- the drawing ---------- *
     One frame, 460 by 340, in the rail beside the form. It redraws on every
     keystroke and every option, so it has to be cheap: strings, no DOM walking.
     Rules that keep it honest:
       - geometry carries the shape, the note strip carries the words. No
         floating labels colliding with the artwork.
       - the drawn length is fixed; real sizes are read off the dimension
         numbers. Only proportions move, so a 6.5mm bore never looks like 25mm.
       - every callout number is the position of that dimension in fam.dims,
         so a family without a heated length never shows a heated length
         callout, and callout 3 always means the third box in the form.
  */
  var W = 460, H = 352;
  var mid = 'hsl(214 14% 38%)';        /* annotation grey */
  var wash = 'hsl(30 90% 94%)';        /* heated area */
  var washEdge = 'hsl(24 60% 74%)';
  var shell = 'hsl(214 16% 95%)';
  var ART_BOTTOM = 296;                /* the note strip owns everything below */

  function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function n1(v) { return Math.round(v * 100) / 100; }
  /* A field left blank must read as "no value", not as zero: zero would
     collapse the drawing instead of leaving the default proportions. */
  function num2(v) {
    if (v == null || v === '') return null;
    var n = parseFloat(v);
    return (isNaN(n) || !isFinite(n) || n <= 0) ? null : n;
  }

  function P(d, o) {
    o = o || {};
    var stroke = o.stroke === undefined ? ink : o.stroke;
    var s = '<path' + (o.cls ? ' class="' + o.cls + '"' : '') + ' d="' + d +
      '" fill="' + (o.fill || 'none') + '"';
    if (stroke && stroke !== 'none') {
      s += ' stroke="' + stroke + '" stroke-width="' + (o.w == null ? 1.9 : o.w) + '"';
      if (o.dash) s += ' stroke-dasharray="' + o.dash + '"';
      if (o.cap) s += ' stroke-linecap="' + o.cap + '"';
      if (o.join) s += ' stroke-linejoin="' + o.join + '"';
    }
    return s + '/>';
  }
  function CIR(cx, cy, r, o) {
    o = o || {};
    var stroke = o.stroke === undefined ? ink : o.stroke;
    return '<circle' + (o.cls ? ' class="' + o.cls + '"' : '') + ' cx="' + n1(cx) + '" cy="' +
      n1(cy) + '" r="' + n1(r) + '" fill="' + (o.fill || 'none') + '"' +
      (stroke && stroke !== 'none'
        ? ' stroke="' + stroke + '" stroke-width="' + (o.w == null ? 1.9 : o.w) + '"' : '') + '/>';
  }
  function RECT(x, y, w, h, o) {
    o = o || {};
    var stroke = o.stroke === undefined ? ink : o.stroke;
    return '<rect' + (o.cls ? ' class="' + o.cls + '"' : '') + ' x="' + n1(x) + '" y="' + n1(y) +
      '" width="' + n1(Math.max(0, w)) + '" height="' + n1(Math.max(0, h)) + '"' +
      (o.rx ? ' rx="' + n1(o.rx) + '"' : '') + ' fill="' + (o.fill || 'none') + '"' +
      (stroke && stroke !== 'none'
        ? ' stroke="' + stroke + '" stroke-width="' + (o.w == null ? 1.9 : o.w) + '"' : '') + '/>';
  }
  function TXT(s, x, y, o) {
    o = o || {};
    return '<text' + (o.cls ? ' class="' + o.cls + '"' : '') + ' x="' + n1(x) + '" y="' + n1(y) +
      '" text-anchor="' + (o.anchor || 'start') + '" font-family="Inter,sans-serif" font-size="' +
      (o.size || 15) + '"' + (o.weight ? ' font-weight="' + o.weight + '"' : '') +
      ' fill="' + (o.fill || mid) + '">' + esc(s) + '</text>';
  }

  /* callout numbers come from the family's dimension order, never hardcoded */
  function callouts(fam) {
    var dims = (fam && fam.dims) || [];
    return {
      has: function (k) { return dims.indexOf(k) !== -1; },
      n: function (k) { return dims.indexOf(k) + 1; }
    };
  }
  function badge(n, x, y) {
    if (!n) return '';
    return '<g class="callout-n">' + CIR(x, y, 12, { fill: heat, stroke: 'none' }) +
      TXT(String(n), x, y + 5.5, { anchor: 'middle', size: 15, weight: '700', fill: '#fff' }) + '</g>';
  }
  /* A dimension line with its callout sitting on it. Short spans push the
     callout clear of the line so it never covers its own arrows. */
  function dimH(x1, x2, y, n, off) {
    var d = P('M' + n1(x1) + ' ' + n1(y) + 'H' + n1(x2) + 'M' + n1(x1) + ' ' + n1(y - 5) +
      'v10M' + n1(x2) + ' ' + n1(y - 5) + 'v10', { stroke: heat, w: 1.3 });
    if (off) return d + badge(n, off[0], off[1]);
    return d + (x2 - x1 < 36 ? badge(n, (x1 + x2) / 2, y - 18) : badge(n, (x1 + x2) / 2, y));
  }
  function dimV(y1, y2, x, n, off) {
    var d = P('M' + n1(x) + ' ' + n1(y1) + 'V' + n1(y2) + 'M' + n1(x - 5) + ' ' + n1(y1) +
      'h10M' + n1(x - 5) + ' ' + n1(y2) + 'h10', { stroke: heat, w: 1.3 });
    if (off) return d + badge(n, off[0], off[1]);
    return d + (y2 - y1 < 36 ? badge(n, x, y1 - 18) : badge(n, x, (y1 + y2) / 2));
  }

  /* Centre a composition of known width, so a short heater does not sit in the
     left half of the frame with dead space beside it. The left margin never
     drops below the room a vertical dimension line and its callout need. */
  function centre(width, rightPad) {
    return Math.max(56, (W - width - (rightPad || 0)) / 2);
  }

  /* the chosen option object in a group, so the drawing can use its own words */
  function optOf(fam, k, opt) {
    var g = ((fam && fam.groups) || []).filter(function (x) { return x.k === k; })[0];
    if (!g) return null;
    var code = (opt || {})[k];
    return g.opts.filter(function (o) { return o.c === code; })[0] || null;
  }
  function noteOf(fam, k, opt, suffix) {
    var o = optOf(fam, k, opt);
    if (!o) return null;
    return o.t + (suffix ? ' ' + suffix : '');
  }

  /* The words go here, under the drawing, wrapped and clipped to two lines. */
  function noteStrip(notes) {
    notes = (notes || []).filter(Boolean);
    if (!notes.length) return '';
    var lines = [], line = '';
    notes.forEach(function (t) {
      var next = line ? line + '  ·  ' + t : t;
      if (next.length > 46 && line) { lines.push(line); line = t; } else { line = next; }
    });
    if (line) lines.push(line);
    var out = P('M22 ' + (ART_BOTTOM + 6) + 'H' + (W - 22), { stroke: 'hsl(214 16% 88%)', w: 1 });
    for (var i = 0; i < lines.length && i < 2; i++) {
      out += TXT(lines[i], 22, ART_BOTTOM + 24 + i * 19, { size: 15 });
    }
    /* H leaves room for two lines and their descenders; anything more is the
       part code's job, not the drawing's */
    return '<g class="notes">' + out + '</g>';
  }

  /* Drawn size is mapped onto the range the family actually offers, so every
     catalogue size looks different. Deriving it from d/L instead made long
     heaters clamp to one thickness and a 25mm bore looked like a 12.5mm one. */
  function dimRange(fam, key) {
    var def = ((fam && fam.specs) || []).filter(function (s2) { return s2.k === key; })[0];
    if (!def) return null;
    if (def.type === 'select' && def.opts && def.opts.length) {
      var nums = def.opts.map(parseFloat).filter(function (n) { return !isNaN(n); });
      if (!nums.length) return null;
      return { min: Math.min.apply(null, nums), max: Math.max.apply(null, nums) };
    }
    if (def.min != null && def.max != null) return { min: def.min, max: def.max };
    return null;
  }
  function drawnThickness(fam, key, value, lo, hi) {
    var range = dimRange(fam, key);
    var v = num2(value);
    if (!range || v == null || range.max === range.min) return (lo + hi) / 2;
    return lo + clamp((v - range.min) / (range.max - range.min), 0, 1) * (hi - lo);
  }

  /* ---------- cartridge option layer ----------
     Flat and isometric share this, so a chosen option can never be honoured in
     one view and silently ignored in the other. g carries the body geometry:
     x1, x2, cy, bh and rx (cap foreshortening, zero in the flat view). */
  function cartridgeOpts(g, fam, opt) {
    opt = opt || {};
    var art = '', notes = [];
    var bh = g.bh, cy = g.cy, x1 = g.x1, x2 = g.x2, rx = g.rx || 0;
    var y1 = cy - bh / 2, y2 = cy + bh / 2;
    var yT = cy - Math.max(4.5, bh * 0.18), yB = cy + Math.max(4.5, bh * 0.18);
    var ex = x2 + rx;                       /* where the leads leave the body */
    var tip = Math.min(ex + 106, W - 26);
    var sl0 = ex + 24, sl1 = Math.min(ex + 78, tip - 26);
    var bendX = Math.min(ex + 84, tip - 8);

    /* --- termination --- */
    if (opt.term === 'T2') {
      art += P('M' + ex + ' ' + yT + 'H' + bendX + 'V' + (yT - 46) + 'h16' +
        'M' + ex + ' ' + yB + 'H' + (bendX - 13) + 'V' + (yT - 30) + 'h29',
        { cls: 'opt-term', w: 1.7 });
      notes.push(noteOf(fam, 'term', opt, 'exit'));
    } else {
      art += P('M' + ex + ' ' + yT + 'H' + tip + 'M' + ex + ' ' + yB + 'H' + tip, { w: 1.7 });
      if (opt.term === 'T3') {
        art += P('M' + x1 + ' ' + yT + 'H' + (x1 - 44) + 'M' + x1 + ' ' + yB + 'H' + (x1 - 44),
          { cls: 'opt-term', w: 1.7 });
        notes.push(noteOf(fam, 'term', opt));
      }
    }

    /* --- lead protection: every heater has some, so it is always drawn --- */
    var sh = Math.max(15, (yB - yT) + 11), sy = cy - sh / 2, sw = sl1 - sl0, q;
    if (opt.lead === 'L5') {                /* ceramic beads */
      var beads = '';
      for (q = 0; q < 6; q++) beads += CIR(sl0 + 5 + q * (sw / 6), cy, Math.max(4, Math.min(7.5, sh / 1.9)), { w: 1.3 });
      art += '<g class="opt-lead">' + beads + '</g>';
    } else {
      var sleeve = RECT(sl0, sy, sw, sh, { rx: sh / 2, fill: 'none', w: 1.4 });
      var fill = '';
      if (opt.lead === 'L1') {              /* woven glass: light weave */
        for (q = 0; q < 4; q++) fill += P('M' + (sl0 + 8 + q * 13) + ' ' + (sy + sh) + 'l9 -' + sh,
          { stroke: mid, w: 1 });
      } else if (opt.lead === 'L3') {       /* braid: cross hatch */
        for (q = 0; q < 5; q++) {
          fill += P('M' + (sl0 + 4 + q * 11) + ' ' + (sy + sh) + 'l11 -' + sh +
            'M' + (sl0 + 4 + q * 11) + ' ' + sy + 'l11 ' + sh, { stroke: ink, w: 1 });
        }
      } else if (opt.lead === 'L4') {       /* armour: interlocked rings */
        for (q = 0; q < 7; q++) fill += P('M' + (sl0 + 4 + q * 8) + ' ' + sy + 'v' + sh, { w: 1.2 });
      }
      art += '<g class="opt-lead">' + sleeve + fill + '</g>';
    }
    notes.push(noteOf(fam, 'lead', opt, 'leads'));

    /* --- inbuilt thermocouple --- */
    if (opt.tc && opt.tc !== 'TC0') {
      /* grounded means the junction is welded to the sheath wall, so it sits on
         the wall and its lead comes back to the axis before it leaves */
      var grounded = opt.tc === 'TCG';
      var jx = x1 + 26, jy = grounded ? n1(y1 + 2) : cy;
      var run = 'M' + jx + ' ' + jy + (grounded ? 'L' + (jx + 20) + ' ' + cy : '') +
        'H' + Math.min(ex + 40, W - 24);
      art += '<g class="opt-tc">' + CIR(jx, jy, 5, { fill: heat, stroke: 'none' }) +
        P(run, { stroke: heat, w: 1.3, dash: '4 3' }) +
        (grounded ? P('M' + (jx - 9) + ' ' + jy + 'h18', { stroke: heat, w: 2.4 }) : '') +
        '</g>';
      notes.push(noteOf(fam, 'tc', opt, 'thermocouple'));
    }

    /* --- mounting --- */
    if (opt.mount === 'M1') {                       /* round flange */
      var fx = x1 + 58;
      art += '<g class="opt-mount">' +
        P('M' + fx + ' ' + (y1 - 18) + 'h10v' + (bh + 36) + 'h-10Z', { fill: shell, w: 1.7 }) +
        CIR(fx + 5, y1 - 11, 2.9, { fill: ink, stroke: 'none' }) +
        CIR(fx + 5, y2 + 11, 2.9, { fill: ink, stroke: 'none' }) + '</g>';
    } else if (opt.mount === 'M2') {                /* threaded section */
      var t0 = x1 + 44, thread = '';
      for (q = 0; q < 8; q++) thread += 'M' + (t0 + q * 8) + ' ' + y2 + 'l7 -' + bh + ' ';
      art += '<g class="opt-mount">' + P('M' + t0 + ' ' + y1 + 'V' + y2 + 'M' + (t0 + 64) + ' ' + y1 + 'V' + y2, { w: 1.2 }) +
        P(thread, { w: 1 }) + '</g>';
    } else if (opt.mount === 'M3') {                /* strain relief clamp */
      art += '<g class="opt-mount">' +
        P('M' + ex + ' ' + (yT - 11) + 'H' + (ex + 20) + 'V' + (yB + 11) + 'H' + ex + 'Z',
          { fill: shell, w: 1.7 }) +
        CIR(ex + 10, yT - 11, 3, { fill: ink, stroke: 'none' }) + '</g>';
    }
    if (opt.mount && opt.mount !== 'M0') notes.push(noteOf(fam, 'mount', opt, 'mounting'));

    return { art: art, notes: notes };
  }

  /* Each view returns the artwork and the words for the note strip. */
  var VIEWS = {
    cylinder: function (spec, opt, fam) {
      var C = callouts(fam);
      var L = num2(spec.len) || 200;
      var bh = drawnThickness(fam, 'dia', spec.dia, 22, 88);
      var bw = 196, x1 = centre(bw + 106), x2 = x1 + bw, cy = 152;
      var y1 = cy - bh / 2, y2 = cy + bh / 2;
      var hl = num2(spec.hlen), hlw = (hl && L) ? clamp(hl / L, 0.12, 1) : 0.82;
      var hx1 = x1 + bw * (1 - hlw) / 2, hx2 = x2 - bw * (1 - hlw) / 2;

      var o = cartridgeOpts({ x1: x1, x2: x2, cy: cy, bh: bh, rx: 0 }, fam, opt);
      var art =
        RECT(hx1, y1, hx2 - hx1, bh, { cls: 'heated', fill: wash, stroke: 'none' }) +
        RECT(x1, y1, bw, bh, { cls: 'body', rx: Math.min(7, bh / 3), w: 1.9 }) +
        o.art +
        (C.has('dia') ? dimV(y1, y2, x1 - 22, C.n('dia'), [x1 - 22, y1 - 20]) : '') +
        (C.has('len') ? dimH(x1, x2, 252, C.n('len')) : '') +
        (C.has('hlen') ? dimH(hx1, hx2, 84, C.n('hlen')) : '');
      return { art: art, notes: o.notes };
    },

    /* band and nozzle: the bore end on, plus a side view for the width */
    ring: function (spec, opt, fam) {
      var C = callouts(fam);
      opt = opt || {};
      var id = num2(spec.id) || 90;
      var wd = num2(spec.width) || num2(spec.len) || 60;
      var r = clamp(id / 2.6, 28, 62);
      var wall = opt.mat === 'MI' ? 9 : 14;      /* mica is the thinner wall */
      var cx = 134, cy = 146, ro = r + wall;
      var sw = clamp(wd / 1.6, 18, 92), sx = 276, sy = cy - ro, sh = 2 * ro;
      var notes = [];

      var art = CIR(cx, cy, ro, { cls: 'wall', w: 1.9 }) + CIR(cx, cy, r, { cls: 'bore', w: 1.9 });

      if (opt.mat === 'CE') {                    /* ceramic tiles round the wall */
        var tiles = '', a;
        for (a = 0; a < 360; a += 30) {
          var p0 = polar(cx, cy, r, a), p1 = polar(cx, cy, ro, a);
          tiles += 'M' + p0[0] + ' ' + p0[1] + 'L' + p1[0] + ' ' + p1[1] + ' ';
        }
        art += P(tiles, { stroke: 'hsl(214 16% 72%)', w: 1 });
      }
      if (opt.mat) notes.push(noteOf(fam, 'mat', opt));

      /* --- construction --- */
      if (opt.con === 'C2') {                    /* split into two halves */
        /* The joint runs across the wall on the diagonal: the top of the ring
           belongs to the clamping option and the horizontal belongs to the
           bore dimension, so neither can hide it. */
        var jd = '', ja;
        for (ja = 0; ja < 2; ja++) {
          var g0 = polar(cx, cy, r - 4, 45 + ja * 180), g1 = polar(cx, cy, ro + 4, 45 + ja * 180);
          jd += 'M' + g0[0] + ' ' + g0[1] + 'L' + g1[0] + ' ' + g1[1] + ' ';
        }
        art += '<g class="opt-split">' + P(jd, { stroke: '#fff', w: 6 }) +
          P(jd, { stroke: heat, w: 1.9 }) + '</g>';
      } else if (opt.con === 'CE1') {            /* one gap, tabs turned out */
        art += '<g class="opt-expand">' +
          P('M' + (cx - ro - 3) + ' ' + (cy - 7) + 'h' + (wall + 6) + 'v14h-' + (wall + 6) + 'Z',
            { fill: '#fff', stroke: '#fff', w: 1 }) +
          P('M' + (cx - r) + ' ' + (cy - 7) + 'H' + (cx - ro) + 'l-13 -9M' + (cx - r) + ' ' +
            (cy + 7) + 'H' + (cx - ro) + 'l-13 9', { stroke: heat, w: 1.9 }) + '</g>';
      } else if (opt.con === 'CP') {             /* part coverage only */
        art += '<g class="opt-partial">' + arc(cx, cy, (r + ro) / 2, 200, 340,
          { stroke: heat, w: wall - 2 }) + '</g>';
      }
      if (opt.con) notes.push(noteOf(fam, 'con', opt));

      /* --- clamping --- */
      var st = ro + 7;                           /* the strap sits clear of the wall */
      if (opt.clamp === 'K1') {                  /* strap built into the heater */
        art += '<g class="opt-clamp">' + arc(cx, cy, st, 202, 158, { w: 1.4 }) +
          P('M' + (cx - 9) + ' ' + (cy - st) + 'h18v-10h-18Z', { fill: shell, w: 1.5 }) + '</g>';
      } else if (opt.clamp === 'K2') {           /* strap that comes off */
        art += '<g class="opt-clamp">' + arc(cx, cy, st + 7, 198, 162, { w: 1.7 }) +
          P('M' + (cx - 12) + ' ' + (cy - st - 7) + 'h24v-13h-24Z', { fill: shell, w: 1.5 }) +
          CIR(cx, cy - st - 14, 3.4, { fill: ink, stroke: 'none' }) + '</g>';
      } else if (opt.clamp === 'K3') {           /* wedge, for frequent removal */
        art += '<g class="opt-clamp">' + arc(cx, cy, st, 206, 154, { w: 1.4 }) +
          P('M' + (cx - 15) + ' ' + (cy - st) + 'h30l-8 -19h-14Z', { fill: shell, w: 1.7 }) + '</g>';
      } else if (opt.clamp === 'K4') {           /* spring, constant pressure */
        art += '<g class="opt-clamp">' + arc(cx, cy, st, 208, 152, { w: 1.4 }) +
          P('M' + (cx - 15) + ' ' + (cy - st) + 'v-8l7 -4l-14 -7l14 -7l-7 -4v-6' +
            'M' + (cx + 15) + ' ' + (cy - st) + 'v-8l-7 -4l14 -7l-14 -7l7 -4v-6',
            { stroke: heat, w: 1.6 }) +
          P('M' + (cx - 19) + ' ' + (cy - st - 36) + 'h38', { w: 1.7 }) + '</g>';
      }
      if (opt.clamp) notes.push(noteOf(fam, 'clamp', opt, 'clamp'));

      /* --- side view, and the terminals live on it --- */
      art += P('M' + sx + ' ' + sy + 'h' + sw + 'v' + sh + 'h-' + sw + 'Z', { fill: 'none', w: 1.9 }) +
        TXT('side view', sx, sy - 14, { size: 14 });

      /* terminals live on the side view. Everything but the screws stands off
         the outer face, which is where it stands off the real heater. */
      if (opt.term === 'S1') {                   /* screw terminals */
        art += '<g class="opt-term">' +
          CIR(sx + sw / 2, sy + sh * 0.3, 6.5, { fill: shell, w: 1.5 }) +
          CIR(sx + sw / 2, sy + sh * 0.7, 6.5, { fill: shell, w: 1.5 }) +
          P('M' + (sx + sw / 2 - 4) + ' ' + (sy + sh * 0.3) + 'h8M' + (sx + sw / 2 - 4) + ' ' +
            (sy + sh * 0.7) + 'h8', { w: 1.3 }) + '</g>';
      } else if (opt.term === 'S2') {            /* posts */
        art += '<g class="opt-term">' +
          P('M' + (sx + sw) + ' ' + (cy - 16) + 'h26M' + (sx + sw) + ' ' + (cy + 16) + 'h26',
            { w: 2.8 }) +
          P('M' + (sx + sw + 26) + ' ' + (cy - 22) + 'v12M' + (sx + sw + 26) + ' ' + (cy + 10) + 'v12',
            { w: 1.6 }) + '</g>';
      } else if (opt.term === 'S3') {            /* flying leads */
        art += '<g class="opt-term">' +
          P('M' + (sx + sw) + ' ' + (cy - 10) + 'q20 0 27 -13q7 -13 25 -13' +
            'M' + (sx + sw) + ' ' + (cy + 10) + 'q20 0 27 13q7 13 25 13', { w: 1.7 }) + '</g>';
      } else if (opt.term === 'S4') {            /* terminal box */
        art += '<g class="opt-term">' +
          P('M' + (sx + sw) + ' ' + (cy - 22) + 'h34v44h-34Z', { fill: shell, w: 1.7 }) +
          P('M' + (sx + sw + 10) + ' ' + (cy - 22) + 'v44', { w: 1.2 }) + '</g>';
      }
      if (opt.term) notes.push(noteOf(fam, 'term', opt));

      /* --- inbuilt thermocouple (nozzle) --- */
      if (opt.tc && opt.tc !== 'TC0') {
        var j = polar(cx, cy, (r + ro) / 2, 300);
        art += '<g class="opt-tc">' + CIR(j[0], j[1], 5, { fill: heat, stroke: 'none' }) +
          P('M' + j[0] + ' ' + j[1] + 'L' + (cx + ro + 34) + ' ' + (cy - ro - 16),
            { stroke: heat, w: 1.3, dash: '4 3' }) + '</g>';
        notes.push(noteOf(fam, 'tc', opt, 'thermocouple'));
      }

      art += (C.has('id') ? dimH(cx - r, cx + r, cy, C.n('id'), [cx - ro - 22, cy]) : '') +
        (C.has('width') ? dimH(sx, sx + sw, 252, C.n('width')) : '') +
        (C.has('len') ? dimH(sx, sx + sw, 252, C.n('len')) : '');
      return { art: art, notes: notes };
    },

    /* nozzle and manifold coils */
    coil: function (spec, opt, fam) {
      var C = callouts(fam);
      opt = opt || {};
      var r = clamp(drawnThickness(fam, 'id', spec.id, 21, 54), 21, 54);
      var cw = drawnThickness(fam, 'hlen', spec.hlen, 124, 236);
      var cy = 150, x1 = centre(cw + 58), x2 = x1 + cw;
      var turns = Math.max(4, Math.round(cw / 26));
      var step = cw / turns, near = '', far = '', i;
      for (i = 0; i < turns; i++) {
        var x = x1 + i * step;
        /* the near half of each turn is the heavy line, the far half a hairline:
           drawn with one weight the coil reads as a comb with a bar on top */
        near += 'M' + n1(x) + ' ' + n1(cy - r) + 'q' + n1(step * 0.62) + ' ' + n1(r * 1.15) +
          ' 0 ' + n1(2 * r) + ' ';
        far += 'M' + n1(x) + ' ' + n1(cy - r) + 'q' + n1(step * 0.5) + ' -' + n1(r * 0.55) + ' ' +
          n1(step) + ' 0 ';
      }
      var w = opt.prof === 'PT' ? 5.4 : opt.prof === 'PS' ? 3.6 : 2.2;
      var cap = (!opt.prof || opt.prof === 'PR') ? 'round' : 'butt';
      var notes = [noteOf(fam, 'prof', opt, 'section')];

      var art = P(far, { stroke: 'hsl(24 62% 70%)', w: 1.6 }) +
        P(near, { cls: 'opt-prof', stroke: heat, w: w, cap: cap }) +
        P('M' + n1(x1) + ' ' + n1(cy - r) + 'H' + n1(x2) + 'M' + n1(x1) + ' ' + n1(cy + r) +
          'H' + n1(x2), { w: 1, dash: '3 3' });

      /* lead exit */
      var lead = '';
      if (opt.exit === 'ER') {
        lead = 'M' + n1(x2 - 8) + ' ' + n1(cy - r + 8) + 'V' + n1(cy - r - 52) +
          'M' + n1(x2 - 24) + ' ' + n1(cy - r + 8) + 'V' + n1(cy - r - 38);
      } else if (opt.exit === 'ET') {
        lead = 'M' + n1(x2) + ' ' + (cy - r) + 'l44 -44M' + n1(x2) + ' ' + (cy - r + 12) + 'l44 -44';
      } else {
        lead = 'M' + n1(x2) + ' ' + (cy - r * 0.4) + 'h56M' + n1(x2) + ' ' + (cy + r * 0.4) + 'h56';
      }
      art += P(lead, { cls: 'opt-exit', w: 1.7 });
      notes.push(noteOf(fam, 'exit', opt, 'exit'));

      if (opt.tc && opt.tc !== 'TC0') {
        art += '<g class="opt-tc">' + CIR(x1 + 16, cy, 5, { fill: heat, stroke: 'none' }) +
          P('M' + (x1 + 16) + ' ' + cy + 'H' + n1(x2 + 40), { stroke: heat, w: 1.3, dash: '4 3' }) + '</g>';
        notes.push(noteOf(fam, 'tc', opt, 'thermocouple'));
      }

      art += (C.has('id') ? dimV(cy - r, cy + r, x1 - 26, C.n('id'), [x1 - 26, cy - r - 20]) : '') +
        (C.has('hlen') ? dimH(x1, x2, 252, C.n('hlen')) : '');
      return { art: art, notes: notes };
    },

    /* flat and curved surface strips */
    strip: function (spec, opt, fam) {
      var C = callouts(fam);
      opt = opt || {};
      var bw = drawnThickness(fam, 'len', spec.len, 150, 248);
      var bh = drawnThickness(fam, 'width', spec.width, 22, 78);
      var x1 = centre(bw + 60), x2 = x1 + bw, cy = 150, y1 = cy - bh / 2, y2 = cy + bh / 2;
      var notes = [noteOf(fam, 'prof', opt)];
      var art = RECT(x1, y1, bw, bh, { cls: 'body', rx: 2, w: 1.9 });

      if (opt.prof === 'F1') {                   /* fins for heating air */
        var fins = '', q;
        for (q = 1; q < 11; q++) {
          var fx = x1 + (bw / 11) * q;
          fins += 'M' + n1(fx) + ' ' + n1(y1 - 13) + 'v' + n1(bh + 26) + ' ';
        }
        art += '<g class="opt-fins">' + P(fins, { stroke: heat, w: 1.5 }) + '</g>';
      }
      if (opt.term === 'S1') {                   /* screw terminals on studs */
        art += '<g class="opt-term">' +
          P('M' + n1(x2) + ' ' + n1(cy - bh * 0.26) + 'h22M' + n1(x2) + ' ' + n1(cy + bh * 0.26) + 'h22',
            { w: 2.4 }) +
          P('M' + n1(x2 + 22) + ' ' + n1(cy - bh * 0.26 - 7) + 'h11v14h-11Z' +
            'M' + n1(x2 + 22) + ' ' + n1(cy + bh * 0.26 - 7) + 'h11v14h-11Z', { fill: shell, w: 1.5 }) +
          '</g>';
      } else if (opt.term === 'S3') {             /* flying leads */
        art += '<g class="opt-term">' +
          P('M' + n1(x2) + ' ' + n1(cy - bh * 0.26) + 'q30 0 40 -16q10 -16 34 -16' +
            'M' + n1(x2) + ' ' + n1(cy + bh * 0.26) + 'q30 0 40 16q10 16 34 16', { w: 1.7 }) + '</g>';
      }
      if (opt.term) notes.push(noteOf(fam, 'term', opt));

      art += (C.has('len') ? dimH(x1, x2, 252, C.n('len')) : '') +
        (C.has('width') ? dimV(y1, y2, x1 - 24, C.n('width'), [x1 - 24, y1 - 20]) : '');
      return { art: art, notes: notes };
    },

    /* ceramic infrared: the emitter, the gap, the work */
    panel: function (spec, opt, fam) {
      var C = callouts(fam);
      opt = opt || {};
      var gap = drawnThickness(fam, 'dist', spec.dist, 66, 186);
      var ew = 62, ex = centre(ew + gap + 52), fx = ex + ew, wx = fx + gap;
      var top = 100, bot = 204, cy = (top + bot) / 2;
      var notes = [];

      /* one body, three faces: the difference between the forms is what the
         face pointing at the work looks like */
      var face;
      if (opt.form === 'FT') {                   /* trough, focused */
        face = 'M' + ex + ' ' + top + 'H' + fx + 'L' + (fx - 20) + ' ' + cy +
          'L' + fx + ' ' + bot + 'H' + ex + 'Z';
      } else if (opt.form === 'FH') {            /* hollow face */
        face = 'M' + ex + ' ' + top + 'H' + fx + 'A20 ' + ((bot - top) / 2) + ' 0 0 0 ' + fx + ' ' +
          bot + 'H' + ex + 'Z';
      } else {                                   /* flat panel */
        face = 'M' + ex + ' ' + top + 'H' + fx + 'V' + bot + 'H' + ex + 'Z';
      }
      var art = P(face, { cls: 'opt-form', fill: wash, w: 1.9 });
      /* the element itself: a ceramic emitter is a coil cast into the face, and
         without it the body reads as an empty outline whatever the form */
      var ribs = '', rq;
      for (rq = 1; rq < 5; rq++) {
        var ry = top + ((bot - top) / 5) * rq;
        ribs += 'M' + (ex + 9) + ' ' + n1(ry) + 'h' + (ew - 26) + ' ';
      }
      art += P(ribs, { stroke: washEdge, w: 2.2, cap: 'round' });
      notes.push(noteOf(fam, 'form', opt));

      if (opt.refl === 'R1') {                   /* reflector behind */
        art += '<g class="opt-refl">' +
          P('M' + (ex - 8) + ' ' + (top - 22) + 'H' + (ex - 28) + 'V' + (bot + 22) + 'H' + (ex - 8),
            { fill: shell, w: 1.7 }) +
          P('M' + (ex - 28) + ' ' + (top - 12) + 'h20M' + (ex - 28) + ' ' + cy + 'h20M' +
            (ex - 28) + ' ' + (bot + 12) + 'h20', { w: 1.1 }) + '</g>';
        notes.push(noteOf(fam, 'refl', opt, 'reflector'));
      }

      art += P('M' + wx + ' ' + (top - 26) + 'V' + (bot + 26), { w: 4 }) +
        TXT('work', wx + 10, cy + 5, { size: 14 }) +
        P('M' + (fx + 6) + ' ' + (top + 12) + 'h' + (gap - 12) + 'M' + (fx + 6) + ' ' + cy +
          'h' + (gap - 12) + 'M' + (fx + 6) + ' ' + (bot - 12) + 'h' + (gap - 12),
          { stroke: heat, w: 1.4, dash: '6 4' });

      if (opt.tc && opt.tc !== 'TC0') {
        art += '<g class="opt-tc">' + CIR(fx - 12, top + 18, 5, { fill: heat, stroke: 'none' }) +
          P('M' + (fx - 12) + ' ' + (top + 18) + 'V' + (top - 34) + 'H' + (ex - 40),
            { stroke: heat, w: 1.3, dash: '4 3' }) + '</g>';
        notes.push(noteOf(fam, 'tc', opt, 'thermocouple'));
      }

      art += (C.has('dist') ? dimH(fx, wx, 252, C.n('dist')) : '');
      return { art: art, notes: notes };
    },

    /* tubular: the bend form is the shape of the part, so it is drawn */
    tube: function (spec, opt, fam) {
      var C = callouts(fam);
      opt = opt || {};
      var t = drawnThickness(fam, 'dia', spec.dia, 9, 22);
      var fillCol = { SS: 'hsl(214 12% 80%)', IN: 'hsl(40 26% 72%)',
        MS: 'hsl(214 10% 60%)', CU: 'hsl(20 55% 64%)' }[opt.sheath] || shell;
      var cy = 150, notes = [];
      var g;
      if (opt.bend === 'BU') {
        g = { d: 'M118 112H340A38 38 0 0 1 340 188H118',
          ends: [[118, 112, -1], [118, 188, -1]], box: [118, 378] };
      } else if (opt.bend === 'BW') {
        g = { d: 'M118 100H336A25 25 0 0 1 336 150H150A25 25 0 0 0 150 200H366',
          ends: [[118, 100, -1], [366, 200, 1]], box: [118, 366] };
      } else if (opt.bend === 'BC') {
        var near = '', far = '', i, turns = 6, x0 = 150, step = 34;
        for (i = 0; i < turns; i++) {
          near += 'M' + (x0 + i * step) + ' 112q' + (step * 0.6) + ' 38 0 76 ';
          far += 'M' + (x0 + i * step) + ' 112h' + step + ' ';
        }
        g = { d: near, far: far + 'M' + (x0 + turns * step) + ' 188h14',
          ends: [[150, 112, -1], [368, 188, 1]], box: [136, 382] };
      } else {
        g = { d: 'M118 ' + cy + 'H382', ends: [[118, cy, -1], [382, cy, 1]], box: [118, 382] };
      }

      /* two passes make a stroked line read as a tube: the dark one is the
         wall, the pale one inside it is the sheath. The far half of a coil is
         drawn first and thinner, so it sits behind the near half. */
      var art = '';
      if (g.far) {
        art += P(g.far, { stroke: ink, w: t * 0.72 + 2.6, cap: 'round' }) +
          P(g.far, { stroke: fillCol, w: t * 0.72, cap: 'round' });
      }
      art += P(g.d, { stroke: ink, w: t + 2.6, cap: 'round' }) +
        P(g.d, { stroke: fillCol, w: t, cap: 'round' });
      notes.push(noteOf(fam, 'bend', opt, opt.bend === 'B0' ? null : 'bend'));
      notes.push(noteOf(fam, 'sheath', opt, 'sheath'));

      /* terminals, one treatment repeated at every cold end */
      var term = '';
      g.ends.forEach(function (e) {
        var x = e[0], y = e[1], dir = e[2];
        if (opt.term === 'S0') {                 /* studs and nuts */
          term += P('M' + x + ' ' + y + 'h' + (dir * 22), { w: 2.6 }) +
            P('M' + (x + dir * 22) + ' ' + (y - 8) + 'h' + (dir * 13) + 'v16h' + (-dir * 13) + 'Z',
              { fill: shell, w: 1.5 });
        } else if (opt.term === 'S1') {           /* screw terminal block */
          term += P('M' + (x + dir * 2) + ' ' + (y - 13) + 'h' + (dir * 30) + 'v26h' + (-dir * 30) + 'Z',
            { fill: shell, w: 1.6 }) +
            CIR(x + dir * 17, y, 4.5, { w: 1.3 });
        } else {                                  /* flying leads */
          term += P('M' + x + ' ' + y + 'q' + (dir * 22) + ' 0 ' + (dir * 30) + ' -16q' +
            (dir * 8) + ' -16 ' + (dir * 30) + ' -16', { w: 1.7 });
        }
      });
      art += '<g class="opt-term">' + term + '</g>';
      notes.push(noteOf(fam, 'term', opt));
      if (opt.bend && opt.bend !== 'B0') notes.push('length is the developed length');

      var e0 = g.ends[0];
      /* the terminals reach back past the tube ends, so the diameter is
         dimensioned on an extension line clear of all of them */
      art += (C.has('dia') ? dimV(e0[1] - t / 2, e0[1] + t / 2, 62, C.n('dia'), [62, e0[1] - t / 2 - 20]) : '') +
        (C.has('len') ? dimH(g.box[0], g.box[1], 252, C.n('len')) : '');
      return { art: art, notes: notes };
    },

    /* thermocouples and RTDs: sheath, tip, cable, connection */
    probe: function (spec, opt, fam) {
      var C = callouts(fam);
      opt = opt || {};
      var t = drawnThickness(fam, 'dia', spec.dia, 9, 26);
      var cy = 150, notes = [];
      var cb0 = 100, cb1 = 196, sx0 = 196, sx1 = 396;
      var y1 = cy - t / 2, y2 = cy + t / 2;

      /* sheath with a closed tip */
      var art = P('M' + sx0 + ' ' + y1 + 'H' + (sx1 - t / 2) + 'a' + (t / 2) + ' ' + (t / 2) +
        ' 0 0 1 0 ' + t + 'H' + sx0 + 'Z', { fill: shell, w: 1.9 });

      /* cable */
      art += P('M' + cb0 + ' ' + cy + 'q24 -9 48 0t48 0', { w: 6, stroke: 'hsl(214 16% 66%)', cap: 'round' }) +
        P('M' + cb0 + ' ' + cy + 'q24 -9 48 0t48 0', { w: 1.4, stroke: ink });

      /* connection */
      if (opt.conn === 'H') {                     /* terminal head */
        art += '<g class="opt-conn">' +
          P('M' + (cb0 - 54) + ' ' + (cy - 33) + 'h54v66h-54Z', { fill: shell, w: 1.8 }) +
          P('M' + (cb0 - 54) + ' ' + (cy - 21) + 'h54', { w: 1.2 }) +
          CIR(cb0 - 27, cy + 8, 7, { w: 1.3 }) + '</g>';
      } else if (opt.conn === 'B') {              /* bare tails */
        art += '<g class="opt-conn">' +
          P('M' + cb0 + ' ' + cy + 'q-22 0 -32 -15q-10 -15 -28 -15' +
            'M' + cb0 + ' ' + cy + 'q-22 0 -32 15q-10 15 -28 15', { w: 1.7 }) + '</g>';
      } else {                                    /* plug */
        art += '<g class="opt-conn">' +
          P('M' + (cb0 - 48) + ' ' + (cy - 21) + 'h48v42h-48Z', { fill: shell, w: 1.8 }) +
          P('M' + (cb0 - 48) + ' ' + (cy - 10) + 'h-20M' + (cb0 - 48) + ' ' + (cy + 10) + 'h-20',
            { w: 2.6 }) + '</g>';
      }
      notes.push(noteOf(fam, 'conn', opt));

      /* junction at the tip */
      var jx = sx1 - 16;
      if (opt.junc === 'E') {                     /* exposed, wires out of the tip */
        art += '<g class="opt-junc">' +
          P('M' + (sx1 - 2) + ' ' + n1(cy - t * 0.22) + 'q12 0 18 -8' +
            'M' + (sx1 - 2) + ' ' + n1(cy + t * 0.22) + 'q12 0 18 8', { stroke: heat, w: 1.5 }) +
          CIR(sx1 + 18, cy, 3.4, { fill: heat, stroke: 'none' }) + '</g>';
      } else if (opt.junc === 'U') {              /* ungrounded, insulated */
        art += '<g class="opt-junc">' + CIR(jx, cy, Math.max(4, t * 0.26), { fill: heat, stroke: 'none' }) +
          CIR(jx, cy, Math.max(8, t * 0.42), { stroke: heat, w: 1.2 }) + '</g>';
      } else {                                    /* grounded, welded to the wall */
        art += '<g class="opt-junc">' + CIR(jx, y1 + 2, Math.max(4, t * 0.26), { fill: heat, stroke: 'none' }) +
          P('M' + (jx - 9) + ' ' + (y1 + 2) + 'h18', { stroke: heat, w: 2.4 }) + '</g>';
      }
      notes.push(noteOf(fam, 'junc', opt, 'junction'));
      notes.push(noteOf(fam, 'type', opt));

      /* two lengths on one row would read as a single line with two callouts,
         so the cable length drops to its own row */
      art += (C.has('dia') ? dimV(y1, y2, sx1 + 36, C.n('dia'), [sx1 + 36, y1 - 20]) : '') +
        (C.has('len') ? dimH(sx0, sx1, 244, C.n('len')) : '') +
        (C.has('clen') ? dimH(cb0, cb1, 276, C.n('clen')) : '');
      return { art: art, notes: notes };
    }
  };

  /* Isometric cartridge. Same body geometry, same dimension lines and the same
     option layer as the flat view, so nothing can be honoured in one view and
     ignored in the other. A tube is two cap ellipses and the silhouette
     between them; the heated band is a section of the same tube. */
  var VIEWS_ISO = {
    cylinder: function (spec, opt, fam) {
      var C = callouts(fam);
      var L = num2(spec.len) || 200;
      var bh = drawnThickness(fam, 'dia', spec.dia, 22, 88);
      var bw = 196, x1 = centre(bw + 106), x2 = x1 + bw, cy = 152, r = bh / 2;
      var rx = Math.max(3, r * 0.34);
      var y1 = cy - r, y2 = cy + r;
      var hl = num2(spec.hlen), hlw = (hl && L) ? clamp(hl / L, 0.12, 1) : 0.82;
      var hx1 = x1 + bw * (1 - hlw) / 2, hx2 = x2 - bw * (1 - hlw) / 2;

      var body = 'M' + x1 + ' ' + n1(y1) + 'L' + x2 + ' ' + n1(y1) +
        'A' + n1(rx) + ' ' + n1(r) + ' 0 0 1 ' + x2 + ' ' + n1(y2) +
        'L' + x1 + ' ' + n1(y2) + 'A' + n1(rx) + ' ' + n1(r) + ' 0 0 1 ' + x1 + ' ' + n1(y1) + 'Z';
      var band = 'M' + n1(hx1) + ' ' + n1(y1) + 'A' + n1(rx) + ' ' + n1(r) + ' 0 0 1 ' + n1(hx1) +
        ' ' + n1(y2) + 'L' + n1(hx2) + ' ' + n1(y2) + 'A' + n1(rx) + ' ' + n1(r) + ' 0 0 0 ' +
        n1(hx2) + ' ' + n1(y1) + 'Z';

      var o = cartridgeOpts({ x1: x1, x2: x2, cy: cy, bh: bh, rx: rx }, fam, opt);
      var art =
        P(body, { cls: 'iso-body', fill: shell, w: 1.9 }) +
        P(band, { cls: 'iso-band', fill: wash, stroke: 'none' }) +
        P(band, { stroke: washEdge, w: 1 }) +
        '<ellipse class="iso-cap" cx="' + x2 + '" cy="' + cy + '" rx="' + n1(rx) + '" ry="' + n1(r) +
          '" fill="hsl(214 16% 90%)" stroke="' + ink + '" stroke-width="1.9"/>' +
        '<ellipse cx="' + x2 + '" cy="' + cy + '" rx="' + n1(rx * 0.45) + '" ry="' + n1(r * 0.45) +
          '" fill="none" stroke="hsl(214 16% 74%)" stroke-width="1"/>' +
        P('M' + (x1 + 6) + ' ' + n1(y1 + Math.max(2, r * 0.18)) + 'H' + (x2 - 4),
          { stroke: '#fff', w: Math.max(1, r * 0.16) }) +
        o.art +
        (C.has('dia') ? dimV(y1, y2, x1 - 22, C.n('dia'), [x1 - 22, y1 - 20]) : '') +
        (C.has('len') ? dimH(x1, x2, 252, C.n('len')) : '') +
        (C.has('hlen') ? dimH(hx1, hx2, 84, C.n('hlen')) : '');
      return { art: art, notes: o.notes };
    }
  };

  function polar(cx, cy, r, deg) {
    var t = deg * Math.PI / 180;
    return [n1(cx + r * Math.cos(t)), n1(cy + r * Math.sin(t))];
  }
  function arc(cx, cy, r, a0, a1, o) {
    var p0 = polar(cx, cy, r, a0), p1 = polar(cx, cy, r, a1);
    var sweep = ((a1 - a0) + 360) % 360;
    return P('M' + p0[0] + ' ' + p0[1] + 'A' + n1(r) + ' ' + n1(r) + ' 0 ' +
      (sweep > 180 ? 1 : 0) + ' 1 ' + p1[0] + ' ' + p1[1], o);
  }

  var viewMode = 'flat';

  /** Which renderer to use: isometric where we have one, flat otherwise. */
  function viewFor(fam) {
    if (viewMode === 'iso' && VIEWS_ISO[fam.view]) return VIEWS_ISO[fam.view];
    return VIEWS[fam.view] || VIEWS.cylinder;
  }
  function hasIso(fam) { return !!VIEWS_ISO[fam.view]; }

  function renderSpecs() {
    var dims = current.dims || [];
    var dimCells = [], elecHtml = '';

    current.specs.forEach(function (sp) {
      var at = dims.indexOf(sp.k);
      var id = 'sp_' + sp.k;
      var field;
      if (sp.type === 'select') {
        field = '<select id="' + id + '" data-k="' + sp.k + '"><option value="">Choose</option>' +
          sp.opts.map(function (o) { return '<option>' + o + '</option>'; }).join('') + '</select>';
      } else {
        field = '<input id="' + id + '" data-k="' + sp.k + '" type="number" inputmode="decimal"' +
          (sp.min != null ? ' min="' + sp.min + '"' : '') +
          (sp.max != null ? ' max="' + sp.max + '"' : '') + '>';
      }
      var range = (sp.min != null && sp.max != null)
        ? '<span class="range">' + sp.min + ' to ' + sp.max + ' ' + (sp.unit || '') + '</span>'
        : (sp.optional ? '<span class="range">Optional</span>' : '');

      var html = '<div class="dimfield" id="wrap_' + sp.k + '">' +
        '<label for="' + id + '">' +
        (at !== -1 ? '<span class="num" aria-hidden="true">' + (at + 1) + '</span>' : '') +
        '<span>' + sp.label + (sp.unit ? ' <span class="sym">' + sp.unit + '</span>' : '') +
        '</span></label>' + field + range + '<span class="err" hidden></span></div>';

      /* dimension boxes follow the order of fam.dims, so the numbers in the
         form always ascend and always mean the same callout on the drawing */
      if (at !== -1) dimCells[at] = html; else elecHtml += html;
    });

    $('dimFields').innerHTML = dimCells.join('');
    $('elecFields').innerHTML = elecHtml;
    draw();

    // Re-rendering replaces the field elements, so put the entered values back.
    // On a family change spec is empty and this is a no-op; on a redraw (for
    // example switching flat to isometric) it is what stops the numbers vanishing.
    current.specs.forEach(function (sp) {
      if (spec[sp.k] == null || spec[sp.k] === '') return;
      var el = document.getElementById('sp_' + sp.k);
      if (el) el.value = spec[sp.k];
    });
  }

  /* A description of what is drawn, for anyone who cannot see it. */
  function altText() {
    var out = ['Dimensioned drawing of the ' + current.name.toLowerCase() +
      ' heater you are configuring.'];
    current.specs.forEach(function (sp) {
      if (spec[sp.k]) out.push(sp.label.replace(/ Ø.*| L$| HL$/, '') + ' ' + spec[sp.k] + ' ' + (sp.unit || '') + '.');
    });
    current.groups.forEach(function (g) {
      var o = g.opts.filter(function (x) { return x.c === chosen[g.k]; })[0];
      if (o) out.push(g.title + ': ' + o.t + '.');
    });
    out.push('Each numbered callout matches the box with the same number in the form.');
    return esc(out.join(' '));
  }

  function svgWrap(out) {
    return '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + altText() + '">' +
      out.art + noteStrip(out.notes) + '</svg>';
  }

  function onSpec(e) {
    var k = e.target.getAttribute('data-k');
    if (!k) return;
    spec[k] = e.target.value.trim();
    validate(k, e.target);
    update();
  }

  function validate(k, el) {
    var def = current.specs.filter(function (s2) { return s2.k === k; })[0];
    if (!def) return;
    var wrap = $('wrap_' + k);
    if (!wrap) return;
    var err = wrap.querySelector('.err');
    var v = parseFloat(el.value);
    var bad = el.value !== '' && def.min != null && (v < def.min || v > def.max);
    wrap.classList.toggle('bad', bad);
    err.hidden = !bad;
    if (bad) err.textContent = 'Outside the usual range. We will check it is makeable.';
  }

  function draw() {
    $('vizArt').innerHTML = svgWrap(viewFor(current)(spec, chosen, current));
  }

  function update() {
    if (!current) return;
    $('partCode').textContent = partCode();
    draw();
  }

  /* ---------- options ---------- */
  function renderOptions() {
    $('optGroups').innerHTML = current.groups.map(function (g) {
      return '<div class="optgroup"><h3>' + g.title + '</h3><ul class="tiles">' +
        g.opts.map(function (o) {
          return '<li><button class="tile" type="button" aria-pressed="false" data-g="' + g.k +
            '" data-c="' + o.c + '"><span class="code">' + o.c + '</span><span class="t">' + o.t +
            '</span>' + (o.d ? '<span class="d">' + o.d + '</span>' : '') + '</button></li>';
        }).join('') + '</ul></div>';
    }).join('');
  }

  function pick(gk, code) {
    chosen[gk] = code;
    [].forEach.call($('optGroups').querySelectorAll('[data-g="' + gk + '"]'), function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-c') === code));
    });
  }

  /* ---------- part code and summary ---------- */
  function partCode() {
    if (!current) return '';
    var bits = [current.code];
    var dims = [];
    ['dia', 'id', 'len', 'width', 'hlen', 'clen'].forEach(function (k) { if (spec[k]) dims.push(spec[k]); });
    if (dims.length) bits.push(dims.join('x'));
    if (spec.watt) bits.push(spec.watt + 'W');
    if (spec.volt) bits.push(spec.volt + 'V');
    current.groups.forEach(function (g) { if (chosen[g.k]) bits.push(chosen[g.k]); });
    return bits.join('-');
  }

  function specText() {
    var out = [];
    current.specs.forEach(function (s) {
      if (spec[s.k]) out.push(s.label.replace(/ Ø.*| L$| HL$/, '') + ' ' + spec[s.k] + (s.unit || ''));
    });
    current.groups.forEach(function (g) {
      var c = chosen[g.k];
      if (!c) return;
      var o = g.opts.filter(function (x) { return x.c === c; })[0];
      out.push(g.title + ' ' + o.t + ' (' + c + ')');
    });
    return out.join(', ');
  }

  /* ---------- the list ---------- */
  function addItem() {
    if (!current) return;
    var qty = Math.round(clamp(parseInt($('qty').value, 10) || 1, 1, 9999));
    $('qty').value = qty;
    items.push({
      fam: current.name, code: current.code, part: partCode(),
      text: specText(), qty: qty, note: $('lineNote').value.trim()
    });
    $('lineNote').value = ''; $('qty').value = 1;
    renderCart();
    var b = $('addBtn'); b.textContent = 'Added'; setTimeout(function () { b.textContent = 'Add to list'; }, 900);
  }

  function renderCart() {
    var body = $('cartBody'), n = items.length;
    $('cartCount').textContent = n;
    $('cartFoot').hidden = n === 0;
    if (!n) {
      body.innerHTML = '';
      body.appendChild(emptyNode);
      $('whoStep').hidden = true;
      return;
    }
    if (emptyNode && emptyNode.parentNode) emptyNode.parentNode.removeChild(emptyNode);
    body.innerHTML = items.map(function (it, i) {
      return '<div class="line"><span class="nm">' + it.fam + '</span>' +
        '<span class="q">' + it.qty + ' nos</span>' +
        '<span class="pc">' + it.part + '</span>' +
        '<button class="rm" type="button" data-i="' + i + '">Remove</button>' +
        '<span class="sp">' + it.text + (it.note ? '<br><em>' + it.note + '</em>' : '') + '</span></div>';
    }).join('');
    $('totLines').textContent = items.length;
    $('totQty').textContent = items.reduce(function (a, b) { return a + b.qty; }, 0);
    $('whoStep').hidden = false;
  }

  /* ---------- document ---------- */
  function buildDoc() {
    var now = new Date();
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var date = now.getDate() + ' ' + months[now.getMonth()] + ' ' + now.getFullYear();
    var meta = [
      ['Prepared for', ($('cComp').value || '') + ($('cName').value ? '<br>' + $('cName').value : '') || 'Not stated'],
      ['Contact', ($('cMail').value || '') + ($('cPhone').value ? '<br>' + $('cPhone').value : '') || 'Not stated'],
      ['Reference', $('cRef').value || 'Not stated'],
      ['Required by', $('cNeed').value || 'Not stated'],
      ['Date', date]
    ];
    $('docMeta').innerHTML = meta.map(function (m) {
      return '<div><span>' + m[0] + '</span><b>' + m[1] + '</b></div>';
    }).join('');
    $('docBody').innerHTML = items.map(function (it, i) {
      return '<tr><td>' + (i + 1) + '</td><td><code>' + it.part + '</code></td><td>' + it.fam +
        '</td><td>' + it.text + (it.note ? '<br><em>' + it.note + '</em>' : '') +
        '</td><td class="n">' + it.qty + '</td></tr>';
    }).join('');
  }

  function plainText() {
    var lines = ['HEATER REQUIREMENT LIST', ''];
    if ($('cComp').value) lines.push('Company: ' + $('cComp').value);
    if ($('cName').value) lines.push('Contact: ' + $('cName').value);
    if ($('cRef').value) lines.push('Reference: ' + $('cRef').value);
    if ($('cNeed').value) lines.push('Required by: ' + $('cNeed').value);
    lines.push('');
    items.forEach(function (it, i) {
      lines.push((i + 1) + '. ' + it.fam + '  x' + it.qty + ' nos');
      lines.push('   ' + it.part);
      lines.push('   ' + it.text);
      if (it.note) lines.push('   Note: ' + it.note);
      lines.push('');
    });
    lines.push('Total ' + items.length + ' line items, ' +
      items.reduce(function (a, b) { return a + b.qty; }, 0) + ' pieces.');
    lines.push('Built on swiftheat.co.in');
    return lines.join('\n');
  }

  function showDoc() {
    if (!items.length) return;
    buildDoc();
    $('builderView').hidden = true;
    $('docView').hidden = false;
    window.scrollTo(0, 0);
  }

  /* ---------- wire up ---------- */
  $('viewToggle').hidden = true;
  $('vizPanel').hidden = true;
  emptyNode = $('cartEmpty');
  emptyNode.hidden = false;

  $('viewToggle').addEventListener('click', function (e) {
    var b = e.target.closest('[data-mode]');
    if (!b) return;
    viewMode = b.getAttribute('data-mode');
    [].forEach.call($('viewToggle').querySelectorAll('[data-mode]'), function (x) {
      x.setAttribute('aria-pressed', String(x.getAttribute('data-mode') === viewMode));
    });
    if (current) renderSpecs();
  });

  $('dimFields').addEventListener('input', onSpec);
  $('dimFields').addEventListener('change', onSpec);
  $('elecFields').addEventListener('input', onSpec);
  $('elecFields').addEventListener('change', onSpec);
  $('optGroups').addEventListener('click', function (e) {
    var b = e.target.closest('[data-g]');
    if (!b) return;
    pick(b.getAttribute('data-g'), b.getAttribute('data-c'));
    update();
  });

  renderFamilies();
  renderCart();

  $('addBtn').addEventListener('click', addItem);
  $('reviewBtn').addEventListener('click', showDoc);
  $('backBtn').addEventListener('click', function () {
    $('docView').hidden = true; $('builderView').hidden = false; window.scrollTo(0, 0);
  });
  $('printBtn').addEventListener('click', function () { window.print(); });
  $('mailBtn').addEventListener('click', function () {
    var subj = 'Heater requirement list' + ($('cComp').value ? ' from ' + $('cComp').value : '');
    window.location.href = 'mailto:enquiry@swiftheat.co.in?subject=' +
      encodeURIComponent(subj) + '&body=' + encodeURIComponent(plainText());
  });
  $('waBtn').addEventListener('click', function () {
    window.open('https://wa.me/?text=' + encodeURIComponent(plainText()), '_blank', 'noopener');
  });

  $('cartBody').addEventListener('click', function (e) {
    var b = e.target.closest('[data-i]');
    if (!b) return;
    items.splice(parseInt(b.getAttribute('data-i'), 10), 1);
    renderCart();
  });
})();
