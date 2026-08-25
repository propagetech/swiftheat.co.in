import { test, before, after, describe } from 'node:test';
import assert from 'node:assert/strict';
import { start, stop, builder } from './harness.mjs';
import { matchSnapshot } from './snapshot.mjs';

before(async () => { await start(); });
after(async () => { await stop(); });

/* ------------------------------------------------------------------ *
 * Regression tests. Each one is a bug that actually shipped into the
 * working tree during the build. They are named so that if one fails
 * again, the failure explains itself.
 * ------------------------------------------------------------------ */
describe('regressions', () => {
  test('adding an item actually adds it (renderCart threw and killed every button listener)', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '120', watt: '315', volt: '230' });
    await b.field('qty', 4);
    await b.add();
    assert.equal(await b.cartCount(), '1',
      'A valid part code is not proof the button works. This is the assertion that catches it.');
    assert.deepEqual(b.errors, []);
    await b.close();
  });

  test('no horizontal overflow at 375px (grid 1fr sized to content, not viewport)', async () => {
    const b = await builder({ width: 375, height: 812 });
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '120' });
    assert.equal(await b.overflows(), false);
    await b.close();
  });

  test('every control is at least 44px tall on mobile (select was styled, input was not)', async () => {
    const b = await builder({ width: 375, height: 812 });
    await b.family('cartridge');
    const small = await b.smallTapTargets();
    assert.deepEqual(small, [], `Controls under 44px: ${small.join(', ')}`);
    await b.close();
  });

  test('the drawing really sticks on a phone (a sticky grid item cannot)', async () => {
    // The mobile layout put the drawing in its own grid row. A sticky item can
    // only stick inside its own grid area, which for a single-row item is its
    // own height, so it scrolled away exactly as if nothing had been set. The
    // fix is a flex column, where the containing block is the whole column.
    const b = await builder({ width: 390, height: 844 });
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '120' });
    await b.page.evaluate(() => window.scrollBy(0, 1200));
    const top = await b.page.evaluate(() =>
      document.getElementById('vizPanel').getBoundingClientRect().top);
    assert.ok(top >= -1 && top < 120,
      `the drawing left the screen at scroll 1200: top=${Math.round(top)}`);
    await b.close();
  });

  test('the drawing panel does not push the page sideways on a phone', async () => {
    // Bleeding the panel to the screen edges with a negative margin made it
    // wider than its flex parent, and the whole page scrolled sideways.
    const b = await builder({ width: 390, height: 844 });
    await b.family('band');
    await b.spec({ id: '200', width: '80' });
    assert.equal(await b.overflows(), false);
    const wide = await b.page.evaluate(() => {
      const vw = document.documentElement.clientWidth;
      return [...document.querySelectorAll('body *')]
        .filter((e) => e.getBoundingClientRect().width > vw + 1)
        .map((e) => e.className || e.tagName);
    });
    assert.deepEqual(wide, [], `wider than the screen: ${wide.join(', ')}`);
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * The drawing must answer to the numbers.
 * ------------------------------------------------------------------ */
describe('drawing responds to the numbers', () => {
  test('a fatter, shorter heater is drawn fatter', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '6.5', len: '400' });
    const thin = (await b.bodyShapes()).outline.h;
    await b.spec({ dia: '25', len: '100' });
    const fat = (await b.bodyShapes()).outline.h;
    assert.ok(fat > thin, `expected fat (${fat}) > thin (${thin})`);
    await b.close();
  });

  test('the body keeps a constant drawn length; only the aspect ratio moves', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '120' });
    const a = (await b.bodyShapes()).outline.w;
    await b.spec({ len: '900' });
    const c = (await b.bodyShapes()).outline.w;
    assert.equal(a, c, 'drawn body width is deliberately fixed; length is shown by the dimension line');
    await b.close();
  });

  test('heated length shades a proportional part of the body', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '200', hlen: '50' });
    let s = await b.bodyShapes();
    const quarter = s.heated.w / s.outline.w;
    assert.ok(Math.abs(quarter - 0.25) < 0.02, `expected about a quarter shaded, got ${quarter.toFixed(3)}`);

    await b.spec({ hlen: '200' });
    s = await b.bodyShapes();
    assert.equal(s.heated.w, s.outline.w, 'heated length equal to overall length should shade the whole body');
    await b.close();
  });

  test('the shaded region is centred on the body', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '200', hlen: '100' });
    const { outline, heated } = await b.bodyShapes();
    const lead = heated.x - outline.x;
    const tail = (outline.x + outline.w) - (heated.x + heated.w);
    assert.ok(Math.abs(lead - tail) < 0.5, `cold zones should match: ${lead} vs ${tail}`);
    await b.close();
  });

  test('a band heater with a bigger bore is drawn with a bigger bore', async () => {
    const b = await builder();
    await b.family('band');
    await b.spec({ id: '40', width: '50' });
    // The bore and the wall are named in the drawing, so this cannot pick up a
    // callout badge or a terminal screw by accident.
    const bore = async () => (await b.ringRadii()).bore;
    const small = await bore();
    await b.spec({ id: '200' });
    const big = await bore();
    assert.ok(big > small, `expected bore ${big} > ${small}`);
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * The drawing must answer to the options too.
 * ------------------------------------------------------------------ */
describe('drawing responds to the options', () => {
  test('the defaults draw a plain heater: no bend, no sensor, no mounting', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '120' });
    assert.equal(await b.has('.opt-term'), false, 'a straight exit is just the leads');
    assert.equal(await b.has('.opt-tc'), false, 'no thermocouple was asked for');
    assert.equal(await b.has('.opt-mount'), false, 'no mounting was asked for');
    // Lead protection is the exception: every heater has some, so the default
    // fibreglass sleeve is drawn rather than left off.
    assert.equal(await b.has('.opt-lead'), true);
    await b.close();
  });

  test('double ended termination draws leads at both ends', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '120' });
    await b.option('term', 'T3');
    assert.equal(await b.has('.opt-term'), true);
    await b.close();
  });

  test('choosing a thermocouple draws the thermocouple', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '120' });
    await b.option('tc', 'TCK');
    assert.equal(await b.has('.opt-tc'), true);
    await b.option('tc', 'TC0');
    assert.equal(await b.has('.opt-tc'), false, 'switching back to none must clear it');
    await b.close();
  });

  test('all five lead protections draw a different sleeve', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '120' });
    const seen = new Map();
    for (const code of ['L1', 'L2', 'L3', 'L4', 'L5']) {
      await b.option('lead', code);
      const sleeve = await b.page.$eval('.opt-lead', (g) => g.innerHTML);
      assert.ok(sleeve.length > 0, `${code} drew nothing on the lead`);
      assert.ok(!seen.has(sleeve), `${code} draws the same sleeve as ${seen.get(sleeve)}`);
      seen.set(sleeve, code);
    }
    await b.close();
  });

  test('every mounting draws its own feature, and none draws nothing', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '16', len: '200' });
    const seen = new Map();
    for (const code of ['M1', 'M2', 'M3']) {
      await b.option('mount', code);
      const art = await b.page.$eval('.opt-mount', (g) => g.innerHTML);
      assert.ok(!seen.has(art), `${code} draws the same as ${seen.get(art)}`);
      seen.set(art, code);
    }
    await b.option('mount', 'M0');
    assert.equal(await b.has('.opt-mount'), false, 'no mounting must clear the feature');
    await b.close();
  });

  test('a finned strip heater is drawn with fins', async () => {
    const b = await builder();
    await b.family('strip');
    await b.spec({ len: '400', width: '50' });
    assert.equal(await b.has('.opt-fins'), false);
    await b.option('prof', 'F1');
    assert.equal(await b.has('.opt-fins'), true);
    await b.close();
  });

  test('a two piece band heater is drawn split', async () => {
    const b = await builder();
    await b.family('band');
    await b.spec({ id: '90', width: '60' });
    assert.equal(await b.has('.opt-split'), false);
    await b.option('con', 'C2');
    assert.equal(await b.has('.opt-split'), true);
    await b.close();
  });

  test('coil section changes the drawn coil weight', async () => {
    const b = await builder();
    await b.family('coil');
    await b.spec({ id: '30', hlen: '120' });
    const round = await b.page.getAttribute('.opt-prof', 'stroke-width');
    await b.option('prof', 'PT');
    const rect = await b.page.getAttribute('.opt-prof', 'stroke-width');
    assert.ok(parseFloat(rect) > parseFloat(round), `rectangular (${rect}) should read heavier than round (${round})`);
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * Flat and isometric.
 * ------------------------------------------------------------------ */
describe('isometric view', () => {
  test('the toggle is offered only where an isometric drawing exists', async () => {
    const b = await builder();
    await b.family('cartridge');
    assert.equal(await b.toggleHidden(), false, 'cartridge has an isometric view');
    await b.family('band');
    assert.equal(await b.toggleHidden(), true, 'band does not, so do not offer it');
    await b.close();
  });

  test('switching to isometric draws a tube, switching back removes it', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '16', len: '160', hlen: '120' });
    assert.equal(await b.has('.iso-body'), false);
    await b.mode('iso');
    assert.equal(await b.has('.iso-body'), true, 'tube silhouette');
    assert.equal(await b.has('.iso-cap'), true, 'near end face');
    assert.equal(await b.has('.iso-band'), true, 'heated section');
    await b.mode('flat');
    assert.equal(await b.has('.iso-body'), false);
    await b.close();
  });

  test('switching view keeps the numbers in the boxes', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '16', len: '160', hlen: '120', watt: '400', volt: '230' });
    const before = await b.partCode();
    await b.mode('iso');
    assert.equal(await b.specValues(['dia', 'len', 'hlen', 'watt', 'volt']), '16/160/120/400/230',
      'redrawing replaces the field elements; the entered values must be put back');
    assert.equal(await b.partCode(), before, 'the part code must not change with the drawing style');
    await b.close();
  });

  test('changing family still clears the boxes', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '16', len: '160' });
    await b.family('strip');
    assert.equal(await b.specValues(['len', 'width']), '/', 'a new family starts empty');
    await b.close();
  });

  test('option markers survive a view switch', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '16', len: '160' });
    await b.option('tc', 'TCK');
    await b.mode('iso');
    assert.equal(await b.has('.opt-tc'), true, 'isometric must honour the chosen options too');
    await b.mode('flat');
    assert.equal(await b.has('.opt-tc'), true);
    await b.close();
  });

  test('the first render after picking a family already honours the options', async () => {
    // renderSpecs used to call the view without the chosen options, so markers
    // only appeared on a later redraw. Selecting a family last is what catches it.
    const b = await builder();
    await b.family('cartridge');
    await b.option('tc', 'TCK');
    await b.option('term', 'T3');
    await b.family('tubular');
    await b.family('cartridge');
    assert.equal(await b.has('.opt-tc'), false, 'a fresh family resets its options');
    await b.option('tc', 'TCJ');
    await b.mode('iso');
    assert.equal(await b.has('.opt-tc'), true);
    await b.close();
  });

  test('the isometric view dimensions the same things, the same way round', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '16', len: '160', hlen: '120' });
    const callouts = () => b.page.evaluate(() =>
      [...document.querySelectorAll('#vizArt svg .callout-n')].map((g) => ({
        n: g.querySelector('text').textContent,
        x: Math.round(+g.querySelector('circle').getAttribute('cx')),
        y: Math.round(+g.querySelector('circle').getAttribute('cy')),
      })));
    const flat = await callouts();
    await b.mode('iso');
    const iso = await callouts();
    assert.equal(flat.length, 3, 'diameter, overall length, heated length');
    assert.deepEqual(iso, flat,
      'a callout that moves between views makes the reader hunt for it again');
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * Geometry snapshots: catches any unintended change to a drawing.
 * ------------------------------------------------------------------ */
describe('drawing snapshots', () => {
  const cases = [
    ['cartridge-12.5x120-hl95-T2-TCK-L4', 'cartridge',
      { dia: '12.5', len: '120', hlen: '95' }, { term: 'T2', tc: 'TCK', lead: 'L4' }],
    ['cartridge-default', 'cartridge', { dia: '8', len: '200' }, {}],
    ['band-90x60-twopiece', 'band', { id: '90', width: '60' }, { con: 'C2' }],
    ['coil-30x120-rect', 'coil', { id: '30', hlen: '120' }, { prof: 'PT' }],
    ['strip-400x50-finned', 'strip', { len: '400', width: '50' }, { prof: 'F1' }],
    ['tubular-12.5x600', 'tubular', { dia: '12.5', len: '600' }, {}],
    ['sensor-6x300', 'sensor', { dia: '6', len: '300' }, {}],
    ['ir-panel-150', 'ir', { watt: '650', volt: '230', dist: '150' }, {}],
    // one per view that the option layer can reshape, so a change to a bend
    // form or a junction cannot slip through unnoticed
    ['tubular-16x1200-uform-incoloy', 'tubular',
      { dia: '16', len: '1200' }, { bend: 'BU', sheath: 'IN', term: 'S1' }],
    ['tubular-8x2000-coiled-leads', 'tubular',
      { dia: '8', len: '2000' }, { bend: 'BC', sheath: 'CU', term: 'S3' }],
    ['band-200x80-expandable-wedge-box', 'band',
      { id: '200', width: '80' }, { mat: 'MI', con: 'CE1', clamp: 'K3', term: 'S4' }],
    ['band-90x60-partial-spring-posts', 'band',
      { id: '90', width: '60' }, { con: 'CP', clamp: 'K4', term: 'S2' }],
    ['coil-60x300-square-tangential', 'coil',
      { id: '60', hlen: '300' }, { prof: 'PS', exit: 'ET', tc: 'TCK' }],
    ['nozzle-40x60-mica-typeK', 'nozzle', { id: '40', len: '60' }, { mat: 'MI', tc: 'TCK' }],
    ['strip-1200x120-plain-leads', 'strip',
      { len: '1200', width: '120' }, { prof: 'F0', term: 'S3' }],
    ['sensor-3x120-exposed-tails', 'sensor',
      { dia: '3', len: '120', clen: '500' }, { type: 'K', junc: 'E', conn: 'B' }],
    ['sensor-8x2000-pt100-head', 'sensor',
      { dia: '8', len: '2000', clen: '10000' }, { type: 'PT1', junc: 'U', conn: 'H' }],
    ['ir-hollow-900-reflector', 'ir',
      { watt: '1200', volt: '230', dist: '900' }, { form: 'FH', tc: 'TCK', refl: 'R1' }],
    ['cartridge-25x1500-double-ended-beads', 'cartridge',
      { dia: '25', len: '1500', hlen: '1400' }, { term: 'T3', lead: 'L5', tc: 'TCG', mount: 'M2' }],
  ];

  for (const [name, fam, spec, opts] of cases) {
    test(`${name} is drawn as recorded`, async () => {
      const b = await builder();
      await b.family(fam);
      await b.spec(spec);
      for (const [g, c] of Object.entries(opts)) await b.option(g, c);
      matchSnapshot(name, await b.geometry());
      await b.close();
    });
  }

  test('iso-cartridge-16x160-hl120-TCK is drawn as recorded', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '16', len: '160', hlen: '120' });
    await b.option('tc', 'TCK');
    await b.mode('iso');
    matchSnapshot('iso-cartridge-16x160-hl120-TCK', await b.geometry());
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * Part codes.
 * ------------------------------------------------------------------ */
describe('part codes', () => {
  test('a fully configured cartridge produces the documented code', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '120', hlen: '95', watt: '315', volt: '230' });
    await b.option('term', 'T2'); await b.option('lead', 'L4');
    await b.option('tc', 'TCK'); await b.option('mount', 'M1');
    assert.equal(await b.partCode(), 'CH-12.5x120x95-315W-230V-T2-L4-TCK-M1');
    await b.close();
  });

  test('every family produces a code with its own prefix', async () => {
    const expect = { cartridge: 'CH', coil: 'CO', band: 'BH', nozzle: 'NZ',
      strip: 'SH', tubular: 'TH', sensor: 'TS', ir: 'IR' };
    const b = await builder();
    for (const [fam, prefix] of Object.entries(expect)) {
      await b.family(fam);
      const code = await b.partCode();
      assert.ok(code.startsWith(prefix + '-'), `${fam} gave "${code}", expected ${prefix}-`);
    }
    await b.close();
  });

  test('the code updates as options change', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '10', len: '150' });
    const before = await b.partCode();
    await b.option('term', 'T3');
    const after = await b.partCode();
    assert.notEqual(before, after);
    assert.ok(after.includes('T3'));
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * The list.
 * ------------------------------------------------------------------ */
describe('the list', () => {
  test('totals count lines and pieces separately', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '120', watt: '315', volt: '230' });
    await b.field('qty', 24); await b.add();
    await b.family('band');
    await b.spec({ id: '90', width: '60', watt: '1200', volt: '240' });
    await b.field('qty', 6); await b.add();
    assert.deepEqual(await b.totals(), { lines: '2', qty: '30' });
    await b.close();
  });

  test('lines keep their own family and code', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '120' }); await b.add();
    await b.family('strip');
    await b.spec({ len: '400', width: '50' }); await b.add();
    const codes = await b.lineCodes();
    assert.equal(codes.length, 2);
    assert.ok(codes[0].startsWith('CH-'));
    assert.ok(codes[1].startsWith('SH-'));
    await b.close();
  });

  test('removing every line restores the empty state and the list still works after', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '120' });
    await b.add(); await b.add();
    await b.page.click('.line .rm');
    assert.equal(await b.cartCount(), '1');
    await b.page.click('.line .rm');
    assert.equal(await b.cartCount(), '0');
    assert.equal(await b.has('#cartBody .cart-empty'), true, 'empty state must come back');
    await b.add();
    assert.equal(await b.cartCount(), '1', 'the list must still work after emptying it');
    assert.deepEqual(b.errors, []);
    await b.close();
  });

  test('the customer details step appears only once something is on the list', async () => {
    const b = await builder();
    await b.family('cartridge');
    assert.equal(await b.page.isVisible('#whoStep'), false);
    await b.spec({ dia: '12.5', len: '120' });
    await b.add();
    assert.equal(await b.page.isVisible('#whoStep'), true);
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * Validation.
 * ------------------------------------------------------------------ */
describe('validation', () => {
  test('an out of range value is flagged but never blocks the enquiry', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '99999' });
    assert.equal(await b.page.isVisible('#wrap_len .err'), true, 'should warn');
    await b.add();
    assert.equal(await b.cartCount(), '1', 'a warning must not stop a real enquiry reaching the works');
    await b.close();
  });

  test('an in range value clears the warning', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ len: '99999' });
    assert.equal(await b.page.isVisible('#wrap_len .err'), true);
    await b.spec({ len: '120' });
    assert.equal(await b.page.isVisible('#wrap_len .err'), false);
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * The document.
 * ------------------------------------------------------------------ */
describe('the generated document', () => {
  test('one row per line, in order, with quantities', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '120', watt: '315', volt: '230' });
    await b.field('qty', 24); await b.add();
    await b.family('band');
    await b.spec({ id: '90', width: '60', watt: '1200', volt: '240' });
    await b.field('qty', 6); await b.add();
    await b.field('cComp', 'Acme Moulders');
    await b.review();
    const rows = await b.docRows();
    assert.equal(rows.length, 2);
    assert.deepEqual(rows.map((r) => r.n), ['1', '2']);
    assert.deepEqual(rows.map((r) => r.qty), ['24', '6']);
    assert.ok(rows[0].part.startsWith('CH-'));
    assert.ok(rows[1].part.startsWith('BH-'));
    await b.close();
  });

  test('going back to the list and adding more updates the document', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '120' }); await b.add();
    await b.review();
    assert.equal((await b.docRows()).length, 1);
    await b.back();
    await b.family('strip');
    await b.spec({ len: '400', width: '50' }); await b.add();
    await b.review();
    assert.equal((await b.docRows()).length, 2);
    await b.close();
  });

  test('unstated customer details read as "Not stated" rather than blank', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.spec({ dia: '12.5', len: '120' }); await b.add();
    await b.review();
    const meta = await b.page.$$eval('#docMeta div', (d) => d.map((e) => e.textContent));
    assert.ok(meta.some((m) => m.includes('Not stated')));
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * Responsive.
 * ------------------------------------------------------------------ */
describe('responsive', () => {
  for (const [label, width] of [['phone', 375], ['tablet', 768], ['laptop', 1280]]) {
    test(`no overflow on ${label} through a full build`, async () => {
      const b = await builder({ width, height: 900 });
      await b.family('cartridge');
      await b.spec({ dia: '12.5', len: '120', watt: '315', volt: '230' });
      await b.add();
      assert.equal(await b.overflows(), false, 'builder view');
      await b.review();
      assert.equal(await b.overflows(), false, 'document view');
      await b.close();
    });
  }

  test('the size boxes are one numbered grid at every width', async () => {
    // The boxes used to be positioned on top of the drawing at desktop widths
    // and stacked on a phone, which meant two layouts to keep working and a
    // drawing that could not leave the form. Now the drawing lives in the rail
    // and the boxes are always a plain numbered grid.
    for (const width of [375, 768, 1280, 1440]) {
      const b = await builder({ width });
      await b.family('cartridge');
      const seen = await b.page.evaluate(() => ({
        position: getComputedStyle(document.querySelector('#dimFields .dimfield')).position,
        numbered: [...document.querySelectorAll('#dimFields .num')].length,
        callouts: [...document.querySelectorAll('#vizArt .callout-n')]
          .every((g) => getComputedStyle(g).display !== 'none'),
      }));
      assert.equal(seen.position, 'static', `boxes are positioned at ${width}`);
      assert.equal(seen.numbered, 3, `numbers missing from the boxes at ${width}`);
      assert.equal(seen.callouts, true, `callouts hidden on the drawing at ${width}`);
      await b.close();
    }
  });
});

/* ------------------------------------------------------------------ *
 * Accessibility in the states a cold page load never reaches.
 * ------------------------------------------------------------------ */
describe('accessibility', () => {
  test('selected option tiles keep AA contrast', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.option('term', 'T2');
    const bad = await b.page.evaluate(() => {
      const lum = (c) => { const v = c.map((x) => x / 255)
        .map((x) => (x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4)));
        return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; };
      const parse = (s) => s.match(/\d+(\.\d+)?/g).slice(0, 3).map(Number);
      const ratio = (f, g) => { const a = lum(f), b2 = lum(g);
        return (Math.max(a, b2) + 0.05) / (Math.min(a, b2) + 0.05); };
      const tile = document.querySelector('.tile[aria-pressed="true"]');
      const bg = parse(getComputedStyle(tile).backgroundColor);
      return [...tile.querySelectorAll('span')].map((s) => ({
        text: s.textContent.slice(0, 20),
        ratio: +ratio(parse(getComputedStyle(s).color), bg).toFixed(2),
      })).filter((r) => r.ratio < 4.5);
    });
    assert.deepEqual(bad, [], `Low contrast on a selected tile: ${JSON.stringify(bad)}`);
    await b.close();
  });

  test('the selected state is exposed to assistive tech, not just coloured', async () => {
    const b = await builder();
    await b.family('cartridge');
    await b.option('term', 'T3');
    const pressed = await b.page.getAttribute('[data-g="term"][data-c="T3"]', 'aria-pressed');
    assert.equal(pressed, 'true');
    await b.close();
  });

  test('the drawing carries a text alternative', async () => {
    const b = await builder();
    await b.family('cartridge');
    const label = await b.page.getAttribute('#vizArt svg', 'aria-label');
    assert.ok(label && label.length > 20, 'the SVG needs a meaningful aria-label');
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * No page errors anywhere in the main flow.
 * ------------------------------------------------------------------ */
test('a full pass through every family raises no page errors', async () => {
  const b = await builder();
  for (const fam of ['cartridge', 'coil', 'band', 'nozzle', 'strip', 'tubular', 'sensor', 'ir']) {
    await b.family(fam);
    await b.add();
  }
  await b.review();
  assert.equal(await b.cartCount(), '8');
  assert.deepEqual(b.errors, [], `Page errors: ${b.errors.join(' | ')}`);
  await b.close();
});
