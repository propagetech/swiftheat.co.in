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

    { key: 'tubular', view: 'cylinder', dims: ['dia','len'], code: 'TH', name: 'Tubular',
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

    { key: 'sensor', view: 'cylinder', dims: ['dia','len','clen'], code: 'TS', name: 'Thermocouple',
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
    renderSpecs(); renderOptions();
    $('specStep').hidden = false; $('optStep').hidden = false; $('addStep').hidden = false;
    // preselect the first option in every group so the part code is always valid
    current.groups.forEach(function (g) { if (!chosen[g.k]) pick(g.k, g.opts[0].c); });
    update();
  }

  /* ---------- the drawing is the form ---------- */
  var W = 560, H = 340;

  function dimLineH(x1, x2, y) {
    return '<path d="M' + x1 + ' ' + y + 'h' + (x2 - x1) + 'M' + x1 + ' ' + (y - 5) + 'v10M' +
      x2 + ' ' + (y - 5) + 'v10" stroke="' + heat + '" stroke-width="1.2" fill="none"/>';
  }
  function dimLineV(y1, y2, x) {
    return '<path d="M' + x + ' ' + y1 + 'v' + (y2 - y1) + 'M' + (x - 5) + ' ' + y1 + 'h10M' +
      (x - 5) + ' ' + y2 + 'h10" stroke="' + heat + '" stroke-width="1.2" fill="none"/>';
  }
  function leader(x1, y1, x2, y2) {
    return '<path d="M' + x1 + ' ' + y1 + 'L' + x2 + ' ' + y2 + '" stroke="' + soft +
      '" stroke-width="1.1" fill="none" stroke-dasharray="4 3"/>' +
      '<circle cx="' + x1 + '" cy="' + y1 + '" r="2.6" fill="' + heat + '"/>';
  }
  function num(n, x, y) {
    return '<g class="callout-n"><circle cx="' + x + '" cy="' + y + '" r="11" fill="' + heat +
      '"/><text x="' + x + '" y="' + (y + 4) + '" text-anchor="middle" font-family="Inter,sans-serif" ' +
      'font-size="12" font-weight="700" fill="#fff">' + n + '</text></g>';
  }
  function num2(v) { var n = parseFloat(v); return isNaN(n) ? null : n; }

  /* Each view returns the artwork plus the fixed anchor points the inputs sit on.
     Anchors do not move while you type, so a field never jumps under the cursor. */
  var VIEWS = {
    cylinder: function (spec, opt) {
      var d = num2(spec.dia) || 14, L = num2(spec.len) || 200;
      var ratio = Math.max(0.05, Math.min(0.40, d / Math.max(L, 1)));
      var bw = 260, bh = Math.max(16, Math.min(104, bw * ratio));
      var x1 = 165, x2 = x1 + bw, cy = 186, y1 = cy - bh / 2, y2 = cy + bh / 2;
      var hl = num2(spec.hlen), hlw = hl && L ? Math.max(0.15, Math.min(1, hl / L)) : 0.82;
      var hx1 = x1 + bw * (1 - hlw) / 2, hx2 = x2 - bw * (1 - hlw) / 2;
      var art =
        '<rect x="' + hx1 + '" y="' + y1 + '" width="' + (hx2 - hx1) + '" height="' + bh +
          '" fill="hsl(30 90% 95%)"/>' +
        '<rect x="' + x1 + '" y="' + y1 + '" width="' + bw + '" height="' + bh + '" rx="' +
          Math.min(7, bh / 3) + '" fill="none" stroke="' + ink + '" stroke-width="1.9"/>' +
        '<path d="M' + x2 + ' ' + (cy - bh * 0.22) + 'h42M' + x2 + ' ' + (cy + bh * 0.22) +
          'h42" stroke="' + ink + '" stroke-width="1.7" fill="none"/>' +
        dimLineV(y1, y2, 143) + leader(143, cy, 104, 116) + num(1, 78, 96) +
        dimLineH(x1, x2, 268) + leader(295, 268, 295, 292) + num(2, 295, 318) +
        dimLineH(hx1, hx2, 122) + leader((hx1 + hx2) / 2, 122, 295, 92) + num(3, 295, 66);
      opt = opt || {};
      if (opt.term === 'T2') {
        art += '<path class="opt-term" d="M' + (x2 + 30) + ' ' + (cy - bh * 0.22) + 'v-34h20M' +
          (x2 + 30) + ' ' + (cy + bh * 0.22) + 'v-24h20" stroke="' + ink +
          '" stroke-width="1.7" fill="none"/>';
      } else if (opt.term === 'T3') {
        art += '<path class="opt-term" d="M' + x1 + ' ' + (cy - bh * 0.22) + 'h-42M' + x1 + ' ' +
          (cy + bh * 0.22) + 'h-42" stroke="' + ink + '" stroke-width="1.7" fill="none"/>';
      }
      if (opt.tc && opt.tc !== 'TC0') {
        art += '<g class="opt-tc"><circle cx="' + (x1 + 22) + '" cy="' + cy + '" r="5" fill="' + heat +
          '"/><path d="M' + (x1 + 22) + ' ' + cy + 'H' + (x2 + 42) + '" stroke="' + heat +
          '" stroke-width="1.2" stroke-dasharray="3 3" fill="none"/>' +
          '<text x="' + (x1 + 30) + '" y="' + (cy - bh / 2 - 9) + '" font-family="Inter,sans-serif" ' +
          'font-size="11" fill="' + heat + '">' + opt.tc.replace('TC', 'type ') + '</text></g>';
      }
      if (opt.lead === 'L3' || opt.lead === 'L4') {
        var lx = x2 + 42, hatch = '';
        for (var q = 0; q < 5; q++) {
          hatch += 'M' + (lx + q * 7) + ' ' + (cy - bh * 0.30) + 'l5 ' + (bh * 0.60) + ' ';
        }
        art += '<g class="opt-lead"><path d="' + hatch + '" stroke="' + ink +
          '" stroke-width="1.2" fill="none"/></g>';
      }
      return { art: art, anchors: { dia: [86, 96], len: [295, 300], hlen: [295, 62], clen: [470, 300] } };
    },
    ring: function (spec, opt) {
      var id = num2(spec.id) || 90, wd = num2(spec.width) || num2(spec.len) || 60;
      var r = Math.max(34, Math.min(74, id / 2.6));
      var band = Math.max(9, Math.min(30, wd / 3.2));
      var cx = 205, cy = 168;
      var sx = 350, sw = Math.max(16, Math.min(78, wd / 1.6));
      var art =
        '<circle cx="' + cx + '" cy="' + cy + '" r="' + (r + band) + '" fill="none" stroke="' + ink + '" stroke-width="1.9"/>' +
        '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="none" stroke="' + ink + '" stroke-width="1.9"/>' +
        '<path d="M' + (cx + r + band) + ' ' + cy + 'h30" stroke="' + ink + '" stroke-width="1.7" fill="none"/>' +
        dimLineH(cx - r, cx + r, cy) +
        leader(cx - r * 0.7, cy + r * 0.7, 120, 286) + num(1, 96, 300) +
        '<rect x="' + sx + '" y="' + (cy - r - band) + '" width="' + sw + '" height="' +
          (2 * (r + band)) + '" rx="3" fill="none" stroke="' + ink + '" stroke-width="1.9"/>' +
        dimLineH(sx, sx + sw, cy + r + band + 22) +
        leader(sx + sw / 2, cy + r + band + 22, 452, 286) + num(2, 470, 300) +
        '<text x="' + (sx + sw / 2) + '" y="' + (cy - r - band - 12) + '" text-anchor="middle" ' +
          'font-family="Inter,sans-serif" font-size="11" fill="hsl(214 14% 40%)">side view</text>';
      opt = opt || {};
      if (opt.con === 'C2') {
        art += '<g class="opt-split"><path d="M' + cx + ' ' + (cy - r - band - 4) + 'v' + (band + 8) +
          'M' + cx + ' ' + (cy + r - 4) + 'v' + (band + 8) + '" stroke="#fff" stroke-width="5"/>' +
          '<path d="M' + cx + ' ' + (cy - r - band - 4) + 'v' + (band + 8) + 'M' + cx + ' ' +
          (cy + r - 4) + 'v' + (band + 8) + '" stroke="' + heat + '" stroke-width="1.8"/></g>';
      }
      if (opt.con === 'CP') {
        art += '<path class="opt-partial" d="M' + cx + ' ' + cy + 'm-' + (r + band) + ' 0a' +
          (r + band) + ' ' + (r + band) + ' 0 0 1 ' + (2 * (r + band)) + ' 0" fill="none" stroke="' +
          heat + '" stroke-width="4"/>';
      }
      return { art: art, anchors: { id: [110, 300], width: [455, 300], len: [455, 300] } };
    },
    coil: function (spec, opt) {
      var id = num2(spec.id) || 30, hl = num2(spec.hlen) || 120;
      var r = Math.max(16, Math.min(46, id / 1.8));
      var cy = 170, x1 = 150, x2 = Math.min(430, x1 + Math.max(120, Math.min(280, hl * 1.1)));
      var turns = Math.max(5, Math.round((x2 - x1) / 22));
      var step = (x2 - x1) / turns, p = '';
      for (var i = 0; i < turns; i++) {
        var x = x1 + i * step;
        p += 'M' + x + ' ' + (cy - r) + 'q' + (step * 0.55) + ' ' + (r * 1.15) + ' 0 ' + (2 * r) +
             'M' + x + ' ' + (cy - r) + 'h' + step;
      }
      opt = opt || {};
      var coilW = opt.prof === 'PT' ? 5 : opt.prof === 'PS' ? 3.4 : 2;
      var coilCap = opt.prof === 'PR' || !opt.prof ? 'round' : 'butt';
      var art =
        '<path class="opt-prof" d="' + p + '" stroke="' + heat + '" stroke-width="' + coilW +
          '" stroke-linecap="' + coilCap + '" fill="none"/>' +
        '<path d="M' + x1 + ' ' + (cy - r) + 'h' + (x2 - x1) + 'M' + x1 + ' ' + (cy + r) + 'h' + (x2 - x1) +
          '" stroke="' + ink + '" stroke-width="1" stroke-dasharray="3 3" fill="none"/>' +
        dimLineV(cy - r, cy + r, x1 - 26) + leader(x1 - 26, cy, 118, 290) + num(1, 96, 300) +
        dimLineH(x1, x2, cy + r + 46) + leader((x1 + x2) / 2, cy + r + 46, 300, 290) + num(2, 320, 300);
      return { art: art, anchors: { id: [110, 300], hlen: [310, 300] } };
    },
    strip: function (spec, opt) {
      var L = num2(spec.len) || 400, wd = num2(spec.width) || 40;
      var bw = Math.max(160, Math.min(300, L / 1.6));
      var bh = Math.max(16, Math.min(76, wd / 0.9));
      var x1 = 150, x2 = x1 + bw, cy = 168, y1 = cy - bh / 2, y2 = cy + bh / 2;
      var art =
        '<rect x="' + x1 + '" y="' + y1 + '" width="' + bw + '" height="' + bh +
          '" rx="2" fill="none" stroke="' + ink + '" stroke-width="1.9"/>' +
        dimLineH(x1, x2, y2 + 46) + leader((x1 + x2) / 2, y2 + 46, 300, 290) + num(1, 320, 300) +
        dimLineV(y1, y2, x1 - 26) + leader(x1 - 26, cy, 118, 290) + num(2, 96, 300);
      opt = opt || {};
      if (opt.prof === 'F1') {
        var fins = '';
        for (var q = 1; q < 11; q++) {
          var fx = x1 + (bw / 11) * q;
          fins += 'M' + fx + ' ' + (y1 - 12) + 'v' + (bh + 24) + ' ';
        }
        art += '<g class="opt-fins"><path d="' + fins + '" stroke="' + heat +
          '" stroke-width="1.5" fill="none"/></g>';
      }
      return { art: art, anchors: { len: [310, 300], width: [110, 300] } };
    },
    panel: function (spec, opt) {
      var dist = num2(spec.dist) || 150;
      var gap = Math.max(60, Math.min(210, dist / 1.4));
      var ex = 150, wx = ex + 60 + gap;
      var art =
        '<path d="M' + ex + ' 120h60l-10 96h-40z" fill="none" stroke="' + ink + '" stroke-width="1.9"/>' +
        '<path d="M' + (wx) + ' 96v144" stroke="' + ink + '" stroke-width="4"/>' +
        '<text x="' + (wx + 12) + '" y="172" font-family="Inter,sans-serif" font-size="11" fill="hsl(214 14% 40%)">work</text>' +
        '<path d="M' + (ex + 64) + ' 140h' + (gap - 8) + 'M' + (ex + 64) + ' 168h' + (gap - 8) +
          'M' + (ex + 64) + ' 196h' + (gap - 8) + '" stroke="' + heat + '" stroke-width="1.4" stroke-dasharray="6 4" fill="none"/>' +
        dimLineH(ex + 60, wx, 262) + leader((ex + 60 + wx) / 2, 262, 300, 290) + num(1, 320, 300);
      return { art: art, anchors: { dist: [310, 300] } };
    }
  };

  /* Isometric cylinder. Same anchors as the flat view, so the inputs stay
     attached to their dimensions. A tube is two cap ellipses plus the
     silhouette between them; the heated band is a section of the same tube. */
  var VIEWS_ISO = {
    cylinder: function (spec, opt) {
      var d = num2(spec.dia) || 14, L = num2(spec.len) || 200;
      var ratio = Math.max(0.05, Math.min(0.40, d / Math.max(L, 1)));
      var bw = 260, bh = Math.max(16, Math.min(104, bw * ratio));
      var x1 = 165, x2 = x1 + bw, cy = 186, r = bh / 2;
      var rx = Math.max(3, r * 0.34);              // cap foreshortening
      var y1 = cy - r, y2 = cy + r;
      var hl = num2(spec.hlen), hlw = hl && L ? Math.max(0.15, Math.min(1, hl / L)) : 0.82;
      var hx1 = x1 + bw * (1 - hlw) / 2, hx2 = x2 - bw * (1 - hlw) / 2;

      // tube silhouette: top line, near cap arc, bottom line, far cap arc
      var body = 'M' + x1 + ' ' + y1 + 'L' + x2 + ' ' + y1 +
        'A' + rx + ' ' + r + ' 0 0 1 ' + x2 + ' ' + y2 +
        'L' + x1 + ' ' + y2 +
        'A' + rx + ' ' + r + ' 0 0 1 ' + x1 + ' ' + y1 + 'Z';
      // heated band: both edges curve the same way, like a painted ring
      var band = 'M' + hx1 + ' ' + y1 +
        'A' + rx + ' ' + r + ' 0 0 1 ' + hx1 + ' ' + y2 +
        'L' + hx2 + ' ' + y2 +
        'A' + rx + ' ' + r + ' 0 0 0 ' + hx2 + ' ' + y1 + 'Z';

      var art =
        '<path class="iso-body" d="' + body + '" fill="hsl(214 16% 96%)" stroke="' + ink + '" stroke-width="1.9"/>' +
        '<path class="iso-band" d="' + band + '" fill="hsl(30 90% 92%)" stroke="none"/>' +
        '<path d="' + band + '" fill="none" stroke="hsl(24 60% 72%)" stroke-width="1"/>' +
        // near end face
        '<ellipse class="iso-cap" cx="' + x2 + '" cy="' + cy + '" rx="' + rx + '" ry="' + r +
          '" fill="hsl(214 16% 90%)" stroke="' + ink + '" stroke-width="1.9"/>' +
        '<ellipse cx="' + x2 + '" cy="' + cy + '" rx="' + (rx * 0.45) + '" ry="' + (r * 0.45) +
          '" fill="none" stroke="hsl(214 16% 74%)" stroke-width="1"/>' +
        // top highlight, gives the tube its form
        '<path d="M' + (x1 + 6) + ' ' + (y1 + Math.max(2, r * 0.18)) + 'H' + (x2 - 4) +
          '" stroke="#fff" stroke-width="' + Math.max(1, r * 0.16) + '" opacity=".85" fill="none"/>' +
        // leads off the near face
        '<path d="M' + (x2 + rx) + ' ' + (cy - r * 0.35) + 'h40M' + (x2 + rx) + ' ' + (cy + r * 0.35) +
          'h40" stroke="' + ink + '" stroke-width="1.7" fill="none"/>' +
        dimLineV(y1, y2, 143) + leader(143, cy, 104, 116) + num(1, 78, 96) +
        dimLineH(x1, x2, 268) + leader(295, 268, 295, 292) + num(2, 295, 318) +
        dimLineH(hx1, hx2, 122) + leader((hx1 + hx2) / 2, 122, 295, 92) + num(3, 295, 66);

      opt = opt || {};
      if (opt.term === 'T2') {
        art += '<path class="opt-term" d="M' + (x2 + rx + 28) + ' ' + (cy - r * 0.35) + 'v-34h20M' +
          (x2 + rx + 28) + ' ' + (cy + r * 0.35) + 'v-24h20" stroke="' + ink +
          '" stroke-width="1.7" fill="none"/>';
      } else if (opt.term === 'T3') {
        art += '<path class="opt-term" d="M' + x1 + ' ' + (cy - r * 0.35) + 'h-42M' + x1 + ' ' +
          (cy + r * 0.35) + 'h-42" stroke="' + ink + '" stroke-width="1.7" fill="none"/>';
      }
      if (opt.tc && opt.tc !== 'TC0') {
        art += '<g class="opt-tc"><circle cx="' + (x1 + 26) + '" cy="' + cy + '" r="5" fill="' + heat + '"/>' +
          '<path d="M' + (x1 + 26) + ' ' + cy + 'H' + (x2 + rx + 40) + '" stroke="' + heat +
          '" stroke-width="1.2" stroke-dasharray="3 3" fill="none"/>' +
          '<text x="' + (x1 + 34) + '" y="' + (cy - r - 9) + '" font-family="Inter,sans-serif" font-size="11" fill="' +
          heat + '">' + opt.tc.replace('TC', 'type ') + '</text></g>';
      }
      if (opt.lead === 'L3' || opt.lead === 'L4') {
        var lx = x2 + rx + 40, hatch = '';
        for (var q = 0; q < 5; q++) {
          hatch += 'M' + (lx + q * 7) + ' ' + (cy - r * 0.62) + 'l5 ' + (r * 1.24) + ' ';
        }
        art += '<g class="opt-lead"><path d="' + hatch + '" stroke="' + ink + '" stroke-width="1.2" fill="none"/></g>';
      }
      return { art: art, anchors: { dia: [86, 96], len: [295, 300], hlen: [295, 62], clen: [470, 300] } };
    }
  };

  var viewMode = 'flat';

  /** Which renderer to use: isometric where we have one, flat otherwise. */
  function viewFor(fam) {
    if (viewMode === 'iso' && VIEWS_ISO[fam.view]) return VIEWS_ISO[fam.view];
    return VIEWS[fam.view] || VIEWS.cylinder;
  }
  function hasIso(fam) { return !!VIEWS_ISO[fam.view]; }

  function renderSpecs() {
    var view = viewFor(current);
    var out = view(spec, chosen);
    var dims = current.dims || [];
    var i = 0;
    var dimHtml = '', elecHtml = '';

    current.specs.forEach(function (sp) {
      var isDim = dims.indexOf(sp.k) !== -1;
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

      if (isDim) {
        i++;
        var a = out.anchors[sp.k] || [280, 300];
        dimHtml += '<div class="dimfield" id="wrap_' + sp.k + '" style="--x:' +
          (a[0] / W * 100).toFixed(2) + '%;--y:' + (a[1] / H * 100).toFixed(2) + '%">' +
          '<label for="' + id + '"><span class="num" aria-hidden="true">' + i + '</span>' +
          sp.label + (sp.unit ? ' <span class="sym">' + sp.unit + '</span>' : '') + '</label>' +
          field + range + '<span class="err" hidden></span></div>';
      } else {
        elecHtml += '<div class="spec dimfield" id="wrap_' + sp.k + '" style="position:static;transform:none;width:auto">' +
          '<label for="' + id + '">' + sp.label +
          (sp.unit ? ' <span class="sym">' + sp.unit + '</span>' : '') + '</label>' +
          field + range + '<span class="err" hidden></span></div>';
      }
    });

    $('dimFields').innerHTML = dimHtml;
    $('elecFields').innerHTML = elecHtml;
    $('vizArt').innerHTML = svgWrap(out.art);

    // Re-rendering replaces the field elements, so put the entered values back.
    // On a family change spec is empty and this is a no-op; on a redraw (for
    // example switching flat to isometric) it is what stops the numbers vanishing.
    current.specs.forEach(function (sp) {
      if (spec[sp.k] == null || spec[sp.k] === '') return;
      var el = document.getElementById('sp_' + sp.k);
      if (el) el.value = spec[sp.k];
    });
  }

  function svgWrap(art) {
    return '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" ' +
      'aria-label="Dimensioned outline of the heater you are configuring. Each numbered ' +
      'callout matches a box below.">' + art + '</svg>';
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
    $('vizArt').innerHTML = svgWrap(viewFor(current)(spec, chosen).art);
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
  $('viewToggle').hidden = true;
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
