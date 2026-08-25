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
    { key: 'cartridge', code: 'CH', name: 'Cartridge',
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
          { c: 'L2', t: 'PTFE', d: 'Oil and plasticiser' },
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

    { key: 'coil', code: 'CO', name: 'Coil',
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

    { key: 'band', code: 'BH', name: 'Band',
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

    { key: 'nozzle', code: 'NZ', name: 'Nozzle',
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

    { key: 'strip', code: 'SH', name: 'Strip',
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

    { key: 'tubular', code: 'TH', name: 'Tubular',
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

    { key: 'sensor', code: 'TS', name: 'Thermocouple',
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

    { key: 'ir', code: 'IR', name: 'Ceramic infrared',
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
    renderSpecs(); renderOptions();
    $('specStep').hidden = false; $('optStep').hidden = false; $('addStep').hidden = false;
    // preselect the first option in every group so the part code is always valid
    current.groups.forEach(function (g) { if (!chosen[g.k]) pick(g.k, g.opts[0].c); });
    update();
  }

  /* ---------- specs ---------- */
  function renderSpecs() {
    $('specGrid').innerHTML = current.specs.map(function (s) {
      var id = 'sp_' + s.k;
      var field;
      if (s.type === 'select') {
        field = '<select id="' + id + '" data-k="' + s.k + '"><option value="">Choose</option>' +
          s.opts.map(function (o) { return '<option>' + o + '</option>'; }).join('') + '</select>';
      } else {
        field = '<input id="' + id + '" data-k="' + s.k + '" type="number" inputmode="decimal"' +
          (s.min != null ? ' min="' + s.min + '"' : '') + (s.max != null ? ' max="' + s.max + '"' : '') + '>';
      }
      var range = (s.min != null && s.max != null)
        ? '<span class="range">Usual range ' + s.min + ' to ' + s.max + ' ' + (s.unit || '') + '</span>'
        : (s.optional ? '<span class="range">Optional</span>' : '');
      return '<div class="spec" id="wrap_' + s.k + '"><label for="' + id + '">' + s.label +
        (s.unit ? ' <span class="u">' + s.unit + '</span>' : '') + '</label>' + field + range +
        '<span class="err" hidden></span></div>';
    }).join('');
  }

  function onSpec(e) {
    var k = e.target.getAttribute('data-k');
    if (!k) return;
    spec[k] = e.target.value.trim();
    validate(k, e.target);
    update();
  }

  function validate(k, el) {
    var def = current.specs.filter(function (s) { return s.k === k; })[0];
    var wrap = $('wrap_' + k), err = wrap.querySelector('.err');
    var v = parseFloat(el.value);
    var bad = el.value !== '' && def.min != null && (v < def.min || v > def.max);
    wrap.classList.toggle('bad', bad);
    err.hidden = !bad;
    if (bad) err.textContent = 'Outside the usual range. We will check it is makeable.';
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
    ['dia', 'id', 'len', 'width', 'hlen'].forEach(function (k) { if (spec[k]) dims.push(spec[k]); });
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

  /* ---------- live drawing ---------- */
  function draw() {
    var w = 460, h = 150, art = '';
    function el(s) { return s; }
    var d = parseFloat(spec.dia || spec.id || 20) || 20;
    var L = parseFloat(spec.len || spec.hlen || spec.width || 200) || 200;
    if (current.key === 'cartridge' || current.key === 'tubular' || current.key === 'sensor') {
      var ratio = Math.max(0.06, Math.min(0.55, d / Math.max(L, 1)));
      var bw = 300, bh = Math.max(12, Math.min(74, bw * ratio));
      var y = (h - bh) / 2;
      art = '<rect x="70" y="' + y + '" width="' + bw + '" height="' + bh + '" rx="' + Math.min(6, bh / 3) +
        '" fill="none" stroke="' + ink + '" stroke-width="1.8"/>' +
        '<path d="M370 ' + (y + bh * 0.3) + 'h40M370 ' + (y + bh * 0.7) + 'h40" stroke="' + ink + '" stroke-width="1.6" fill="none"/>' +
        '<path d="M70 ' + (h - 14) + 'h300M70 ' + (h - 20) + 'v12M370 ' + (h - 20) + 'v12" stroke="' + heat + '" stroke-width="1.2" fill="none"/>' +
        '<text x="220" y="' + (h - 2) + '" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="' + ink + '">' +
        (spec.len ? spec.len + ' mm' : 'length') + '</text>' +
        '<path d="M56 ' + y + 'v' + bh + 'M50 ' + y + 'h12M50 ' + (y + bh) + 'h12" stroke="' + heat + '" stroke-width="1.2" fill="none"/>' +
        '<text x="44" y="' + (h / 2 + 4) + '" text-anchor="end" font-family="Inter,sans-serif" font-size="11" fill="' + ink + '">' +
        (spec.dia ? spec.dia : 'Ø') + '</text>';
      if (chosen.term === 'T3') {
        art += '<path d="M70 ' + (y + bh * 0.5) + 'h-14" stroke="' + ink + '" stroke-width="1.6"/>';
      }
      if (chosen.tc && chosen.tc !== 'TC0') {
        art += '<circle cx="110" cy="' + (y + bh / 2) + '" r="4" fill="' + heat + '"/>' +
          '<text x="118" y="' + (y + bh / 2 - 8) + '" font-family="Inter,sans-serif" font-size="10" fill="' + heat + '">TC</text>';
      }
    } else if (current.key === 'band' || current.key === 'nozzle' || current.key === 'coil') {
      var R = Math.max(28, Math.min(58, (parseFloat(spec.id) || 60) / 4));
      var band = Math.max(8, Math.min(26, (parseFloat(spec.width) || 40) / 3));
      art = '<circle cx="230" cy="70" r="' + (R + band) + '" fill="none" stroke="' + ink + '" stroke-width="1.8"/>' +
        '<circle cx="230" cy="70" r="' + R + '" fill="none" stroke="' + ink + '" stroke-width="1.8"/>' +
        '<path d="M' + (230 + R + band) + ' 70h34" stroke="' + ink + '" stroke-width="1.6"/>' +
        '<path d="M230 70m-' + R + ' 0a' + R + ' ' + R + ' 0 0 1 ' + (2 * R) + ' 0" fill="none" stroke="' + heat + '" stroke-width="1.2" stroke-dasharray="3 3"/>' +
        '<text x="230" y="' + (70 + R + band + 22) + '" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="' + ink + '">ID ' +
        (spec.id ? spec.id + ' mm' : '?') + (spec.width ? ' · width ' + spec.width + ' mm' : '') + '</text>';
      if (current.key === 'coil') {
        art += '<text x="230" y="24" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="' + heat + '">coil section ' +
          (chosen.prof === 'PS' ? 'square' : chosen.prof === 'PT' ? 'rectangular' : 'round') + '</text>';
      }
    } else if (current.key === 'strip') {
      var sw = 300, sh2 = Math.max(10, Math.min(46, (parseFloat(spec.width) || 40) / 2));
      art = '<rect x="80" y="' + ((h - sh2) / 2) + '" width="' + sw + '" height="' + sh2 + '" rx="2" fill="none" stroke="' + ink + '" stroke-width="1.8"/>';
      if (chosen.prof === 'F1') {
        for (var i = 0; i < 10; i++) {
          art += '<path d="M' + (95 + i * 30) + ' ' + ((h - sh2) / 2 - 8) + 'v' + (sh2 + 16) + '" stroke="' + heat + '" stroke-width="1.4"/>';
        }
      }
      art += '<text x="230" y="' + (h - 6) + '" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="' + ink + '">' +
        (spec.len ? spec.len + ' x ' : '') + (spec.width ? spec.width + ' mm' : '') + '</text>';
    } else {
      art = '<rect x="150" y="46" width="160" height="52" rx="4" fill="none" stroke="' + ink + '" stroke-width="1.8"/>' +
        '<path d="M320 58v30M334 52v42M348 60v26" stroke="' + heat + '" stroke-width="1.8" fill="none"/>' +
        '<text x="230" y="126" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="' + ink + '">' +
        (spec.watt ? spec.watt + ' W' : 'radiant element') + '</text>';
    }
    $('vizArt').innerHTML = '<svg viewBox="0 0 ' + w + ' ' + h + '" role="img" aria-label="Outline of the heater you are configuring">' + art + '</svg>';
  }

  function update() {
    if (!current) return;
    $('partCode').textContent = partCode();
    draw();
  }

  /* ---------- the list ---------- */
  function addItem() {
    if (!current) return;
    var qty = parseInt($('qty').value, 10) || 1;
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
  emptyNode = $('cartEmpty');
  emptyNode.hidden = false;

  $('specGrid').addEventListener('input', onSpec);
  $('specGrid').addEventListener('change', onSpec);
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
