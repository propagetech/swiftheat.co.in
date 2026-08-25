/* Exhaustive permutation tests for the heater list builder.
 *
 * builder.test.mjs checks the behaviour a person walks through. This file
 * checks the space: every option of every group of every family, crossed with
 * every other group, and then crossed again with the extremes of every
 * dimension. Roughly five thousand configurations, in about ten seconds,
 * because the sweep runs inside the page instead of driving it from here.
 *
 * What a configuration has to satisfy:
 *   1. it draws something, with no NaN and no empty attributes
 *   2. nothing is drawn outside the frame
 *   3. the callout numbers on the drawing are exactly the numbered boxes
 *      in the form
 *   4. the part code carries every code that was chosen
 *   5. no two options in the same group draw the same picture, which is what
 *      catches an option the drawing quietly ignores
 *   6. no page errors, ever
 */
import { test, before, after, describe } from 'node:test';
import assert from 'node:assert/strict';
import { start, stop, builder } from './harness.mjs';

before(async () => { await start(); });
after(async () => { await stop(); });

/* A realistic size for each family, so the sweep runs against a drawing
   somebody might actually ask for rather than only against the defaults. */
const REAL = {
  cartridge: { dia: '12.5', len: '120', hlen: '95', watt: '315', volt: '230' },
  coil: { id: '30', hlen: '120', watt: '400', volt: '230' },
  band: { id: '120', width: '70', watt: '1200', volt: '240' },
  nozzle: { id: '40', len: '60', watt: '300', volt: '230' },
  strip: { len: '600', width: '60', watt: '1000', volt: '240' },
  tubular: { dia: '12.5', len: '900', watt: '2000', volt: '240' },
  sensor: { dia: '6', len: '300', clen: '2000' },
  ir: { watt: '650', volt: '230', dist: '150' },
};
const FAMILIES = Object.keys(REAL);

/** Every dimension pushed to a value that has broken a drawing before. */
function edgeSets(model) {
  const numeric = model.specs.filter((s) => s.tag === 'input');
  const selects = model.specs.filter((s) => s.tag === 'select');
  const sets = { blank: {}, smallest: {}, largest: {}, zero: {}, negative: {},
    huge: {}, tiny: {}, 'not a number': {} };
  for (const s of numeric) {
    sets.smallest[s.k] = s.min;
    sets.largest[s.k] = s.max;
    sets.zero[s.k] = 0;
    sets.negative[s.k] = -50;
    sets.huge[s.k] = 999999;
    sets.tiny[s.k] = 0.001;
    sets['not a number'][s.k] = 'abc';
  }
  for (const s of selects) {
    sets.smallest[s.k] = s.opts[0];
    sets.largest[s.k] = s.opts[s.opts.length - 1];
  }
  return sets;
}

function report(fam, label, r) {
  const lines = [...r.violations, ...r.sameDrawing];
  return `${fam} / ${label}: ${r.combos} combinations, ${lines.length} problems\n  ` +
    lines.slice(0, 12).join('\n  ');
}

/* ------------------------------------------------------------------ *
 * The whole option space, one family at a time.
 * ------------------------------------------------------------------ */
describe('every combination of every option', () => {
  for (const fam of FAMILIES) {
    test(`${fam}: every combination draws, and no two options draw alike`, async () => {
      const b = await builder({ width: 1440, height: 1000 });
      const r = await b.sweep(fam, REAL[fam]);
      assert.ok(r.combos > 0, 'nothing was swept');
      assert.deepEqual(r.violations, [], report(fam, 'real sizes', r));
      assert.deepEqual(r.sameDrawing, [],
        `An option that draws the same picture as its neighbour is an option the drawing ignores.\n` +
        report(fam, 'real sizes', r));
      assert.deepEqual(b.errors, []);
      await b.close();
    });
  }
});

/* ------------------------------------------------------------------ *
 * The same option space again, against dimensions that fight back.
 * ------------------------------------------------------------------ */
describe('every combination against every extreme dimension', () => {
  for (const fam of FAMILIES) {
    test(`${fam}: blank, smallest, largest, zero, negative, huge, tiny and junk`, async () => {
      const b = await builder({ width: 1440, height: 1000 });
      const model = (await b.model()).find((m) => m.fam === fam);
      let combos = 0;
      for (const [label, spec] of Object.entries(edgeSets(model))) {
        const r = await b.sweep(fam, spec);
        combos += r.combos;
        assert.deepEqual(r.violations, [], report(fam, label, r));
        assert.deepEqual(r.sameDrawing, [], report(fam, label, r));
      }
      assert.ok(combos >= 8, `only ${combos} combinations swept`);
      assert.deepEqual(b.errors, []);
      await b.close();
    });
  }
});

/* ------------------------------------------------------------------ *
 * Isometric is a second renderer, so it gets the same treatment.
 * ------------------------------------------------------------------ */
describe('the isometric view honours everything the flat view honours', () => {
  test('every cartridge combination draws in isometric too', async () => {
    const b = await builder({ width: 1440, height: 1000 });
    await b.family('cartridge');
    await b.mode('iso');
    const r = await b.sweep('cartridge', REAL.cartridge);
    assert.deepEqual(r.violations, [], report('cartridge', 'isometric', r));
    assert.deepEqual(r.sameDrawing, [], report('cartridge', 'isometric', r));
    assert.deepEqual(b.errors, []);
    await b.close();
  });

  test('the same options produce the same markers in both views', async () => {
    const b = await builder({ width: 1440, height: 1000 });
    const markers = () => b.page.evaluate(() =>
      [...document.querySelectorAll('#vizArt svg [class]')]
        .map((e) => e.getAttribute('class'))
        .filter((c) => c.startsWith('opt-'))
        .sort().join(','));

    const combos = [
      { term: 'T1', lead: 'L1', tc: 'TC0', mount: 'M0' },
      { term: 'T2', lead: 'L3', tc: 'TCK', mount: 'M1' },
      { term: 'T3', lead: 'L5', tc: 'TCG', mount: 'M2' },
      { term: 'T2', lead: 'L4', tc: 'TCJ', mount: 'M3' },
    ];
    for (const combo of combos) {
      await b.family('cartridge');
      await b.spec(REAL.cartridge);
      for (const [g, c] of Object.entries(combo)) await b.option(g, c);
      await b.mode('flat');
      const flat = await markers();
      await b.mode('iso');
      const iso = await markers();
      assert.equal(iso, flat,
        `${JSON.stringify(combo)} draws ${flat || 'nothing'} flat but ${iso || 'nothing'} isometric`);
    }
    await b.close();
  });

  test('the toggle is offered only where an isometric drawing exists', async () => {
    const b = await builder();
    const model = await b.model();
    const iso = model.filter((m) => m.iso).map((m) => m.fam);
    assert.deepEqual(iso, ['cartridge'],
      'families claiming an isometric view must have one: ' + iso.join(', '));
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * Dropdowns: every catalogue value has to draw.
 * ------------------------------------------------------------------ */
describe('every value in every dropdown', () => {
  test('each catalogue size draws and reaches the part code', async () => {
    const b = await builder({ width: 1440, height: 1000 });
    let checked = 0;
    for (const m of await b.model()) {
      for (const s of m.specs.filter((x) => x.tag === 'select')) {
        await b.family(m.fam);
        for (const v of s.opts) {
          const r = await b.probe(s.k, v);
          assert.equal(r.junk, null, `${m.fam} ${s.k}=${v} drew ${r.junk}`);
          assert.deepEqual(r.outside, [], `${m.fam} ${s.k}=${v} drew outside the frame`);
          assert.ok(r.code.includes(v), `${m.fam} ${s.k}=${v} is missing from ${r.code}`);
          checked++;
        }
      }
    }
    assert.ok(checked > 30, `only ${checked} dropdown values checked`);
    assert.deepEqual(b.errors, []);
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * Numbered boxes and numbered callouts are one system.
 * ------------------------------------------------------------------ */
describe('the numbers in the form and on the drawing are the same numbers', () => {
  test('every family numbers its dimensions 1..n with no strays', async () => {
    const b = await builder({ width: 1440, height: 1000 });
    for (const m of await b.model()) {
      await b.family(m.fam);
      const seen = await b.page.evaluate(() => ({
        boxes: [...document.querySelectorAll('#dimFields .dimfield')].map((d) => ({
          n: d.querySelector('.num') ? +d.querySelector('.num').textContent : null,
          k: d.querySelector('[data-k]').getAttribute('data-k'),
        })),
        callouts: [...document.querySelectorAll('#vizArt svg .callout-n text')].map((t) => +t.textContent),
      }));
      const want = m.dims.map((_, i) => i + 1);
      assert.deepEqual(seen.boxes.map((x) => x.n), want,
        `${m.fam} numbers its boxes ${seen.boxes.map((x) => x.n).join()}`);
      assert.deepEqual(seen.boxes.map((x) => x.k), m.dims,
        `${m.fam} boxes are out of order against fam.dims`);
      assert.deepEqual([...seen.callouts].sort((a, c) => a - c), want,
        `${m.fam} draws callouts ${seen.callouts.join()} for dimensions ${m.dims.join()}`);
    }
    await b.close();
  });

  test('electrical values are not given callout numbers', async () => {
    const b = await builder({ width: 1440, height: 1000 });
    for (const m of await b.model()) {
      await b.family(m.fam);
      const numbered = await b.page.evaluate(() =>
        [...document.querySelectorAll('#elecFields .num')].length);
      assert.equal(numbered, 0, `${m.fam} numbered a wattage or a voltage as if it were a size`);
    }
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * Values outside the catalogue warn, and still draw, and still sell.
 * ------------------------------------------------------------------ */
describe('values outside the usual range', () => {
  test('below and above the range warn, in range does not, and all three draw', async () => {
    const b = await builder({ width: 1440, height: 1000 });
    for (const m of await b.model()) {
      await b.family(m.fam);
      for (const s of m.specs.filter((x) => x.tag === 'input' && x.min != null)) {
        const min = Number(s.min), max = Number(s.max);
        for (const [label, v, warn] of [
          ['below', min - 1, true], ['at the bottom', min, false],
          ['at the top', max, false], ['above', max + 1, true],
        ]) {
          const r = await b.probe(s.k, v);
          assert.equal(r.junk, null, `${m.fam} ${s.k} ${label} drew ${r.junk}`);
          assert.deepEqual(r.outside, [], `${m.fam} ${s.k} ${label} drew outside the frame`);
          assert.equal(r.warned, warn, `${m.fam} ${s.k}=${v} (${label}) warned=${r.warned}`);
        }
      }
    }
    assert.deepEqual(b.errors, []);
    await b.close();
  });

  test('a warning never blocks the enquiry', async () => {
    const b = await builder({ width: 1440, height: 1000 });
    for (const fam of FAMILIES) {
      await b.family(fam);
      await b.probe(Object.keys(REAL[fam])[0], 999999);
      await b.add();
    }
    assert.equal(await b.cartCount(), String(FAMILIES.length),
      'an out of range size must still be allowed to reach the works');
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * The list and the document, across every family at once.
 * ------------------------------------------------------------------ */
describe('the list and the document take every family', () => {
  test('one line per family, fully optioned, all the way to the document', async () => {
    const b = await builder({ width: 1440, height: 1000 });
    const model = await b.model();
    const expected = [];

    for (const m of model) {
      await b.family(m.fam);
      await b.spec(REAL[m.fam]);
      /* the last option in every group, so no line is left on defaults */
      for (const g of m.groups) await b.option(g.k, g.opts[g.opts.length - 1]);
      await b.field('qty', 7);
      expected.push({ code: await b.partCode(), fam: m.fam });
      await b.add();
    }

    assert.equal(await b.cartCount(), String(model.length));
    assert.deepEqual(await b.totals(), { lines: String(model.length), qty: String(model.length * 7) });
    assert.deepEqual(await b.lineCodes(), expected.map((e) => e.code));

    await b.review();
    const rows = await b.docRows();
    assert.equal(rows.length, model.length);
    assert.deepEqual(rows.map((r) => r.part), expected.map((e) => e.code));
    assert.deepEqual(rows.map((r) => r.qty), model.map(() => '7'));
    assert.deepEqual(rows.map((r) => r.n), model.map((_, i) => String(i + 1)));

    /* every chosen option has to be readable on the document, not just encoded */
    const spec = await b.page.$$eval('#docBody tr', (rs) => rs.map((r) => r.cells[3].textContent));
    for (let i = 0; i < model.length; i++) {
      for (const g of model[i].groups) {
        const last = g.opts[g.opts.length - 1];
        assert.ok(spec[i].includes(last),
          `${model[i].fam} row does not mention ${g.title} ${last}: ${spec[i]}`);
      }
    }
    assert.deepEqual(b.errors, []);
    await b.close();
  });

  test('a quantity that makes no sense is corrected, not shipped', async () => {
    const b = await builder({ width: 1440, height: 1000 });
    await b.family('cartridge');
    await b.spec(REAL.cartridge);
    for (const [typed, want] of [[-5, '1'], [0, '1'], ['', '1'], [100000, '9999'], [2.7, '2']]) {
      await b.field('qty', typed);
      await b.add();
      const lines = await b.page.$$eval('.line .q', (els) => els.map((e) => e.textContent.trim()));
      assert.equal(lines[lines.length - 1], want + ' nos', `typing ${JSON.stringify(typed)}`);
    }
    await b.close();
  });

  test('the message that leaves the page carries every line', async () => {
    const b = await builder({ width: 1440, height: 1000 });
    for (const fam of ['cartridge', 'band', 'sensor']) {
      await b.family(fam);
      await b.spec(REAL[fam]);
      await b.add();
    }
    await b.field('cComp', 'Acme Moulders');
    const text = await b.page.evaluate(() => {
      /* the WhatsApp and email bodies are built from the same text */
      const link = document.getElementById('waBtn');
      let captured = '';
      const open = window.open;
      window.open = (url) => { captured = decodeURIComponent(url.split('text=')[1]); };
      link.click();
      window.open = open;
      return captured;
    });
    assert.ok(text.includes('Acme Moulders'), 'the company must be on the message');
    for (const prefix of ['CH-', 'BH-', 'TS-']) {
      assert.ok(text.includes(prefix), `the message is missing a ${prefix} line`);
    }
    assert.ok(/3 line items/.test(text), 'the message must total the lines: ' + text.slice(-120));
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * Switching around, which is where state leaks.
 * ------------------------------------------------------------------ */
describe('switching family, view and back', () => {
  test('every family follows every other family without residue', async () => {
    const b = await builder({ width: 1440, height: 1000 });
    for (const from of FAMILIES) {
      for (const to of FAMILIES) {
        await b.family(from);
        await b.spec(REAL[from]);
        await b.family(to);
        const state = await b.page.evaluate(() => ({
          fields: [...document.querySelectorAll('[data-k]')].map((e) => e.value).join('|'),
          pressed: [...document.querySelectorAll('#optGroups [aria-pressed="true"]')].length,
          groups: document.querySelectorAll('.optgroup').length,
          code: document.getElementById('partCode').textContent,
        }));
        assert.match(state.fields, /^\|*$/,
          `${from} to ${to} left values behind: ${state.fields}`);
        assert.equal(state.pressed, state.groups,
          `${from} to ${to}: ${state.pressed} of ${state.groups} groups have a choice`);
        assert.ok(!/undefined|NaN/.test(state.code), `${from} to ${to} gave code ${state.code}`);
      }
    }
    assert.deepEqual(b.errors, []);
    await b.close();
  });

  test('a family with no isometric drawing keeps the preference for one that has', async () => {
    const b = await builder({ width: 1440, height: 1000 });
    await b.family('cartridge');
    await b.mode('iso');
    await b.family('band');
    assert.equal(await b.toggleHidden(), true, 'no isometric band drawing, so no toggle');
    assert.equal(await b.has('.iso-body'), false, 'and no isometric artwork either');
    await b.family('cartridge');
    assert.equal(await b.has('.iso-body'), true, 'the preference comes back with the family');
    await b.close();
  });

  test('the drawing panel appears with the first family and never empties', async () => {
    const b = await builder({ width: 1440, height: 1000 });
    assert.equal(await b.page.isVisible('#vizPanel'), false, 'nothing to draw yet');
    for (const fam of FAMILIES) {
      await b.family(fam);
      assert.equal(await b.page.isVisible('#vizPanel'), true, `${fam} should be drawn`);
      const shapes = await b.page.evaluate(() =>
        document.querySelectorAll('#vizArt svg rect, #vizArt svg circle, #vizArt svg path, #vizArt svg ellipse').length);
      assert.ok(shapes > 6, `${fam} drew only ${shapes} shapes`);
    }
    await b.close();
  });
});

/* ------------------------------------------------------------------ *
 * The layout the whole tool depends on: the drawing stays in view.
 * ------------------------------------------------------------------ */
describe('the drawing stays in view while you work', () => {
  test('on a desktop it sits above the list, in a column that sticks', async () => {
    const b = await builder({ width: 1440, height: 900 });
    await b.family('cartridge');
    const geo = await b.page.evaluate(() => {
      const panel = document.getElementById('vizPanel').getBoundingClientRect();
      const cart = document.querySelector('.cart').getBoundingClientRect();
      const steps = document.querySelector('.steps').getBoundingClientRect();
      return {
        stuck: getComputedStyle(document.querySelector('.rail')).position,
        aboveTheList: panel.bottom <= cart.top + 1,
        besideTheForm: panel.left >= steps.right - 1,
      };
    });
    assert.equal(geo.stuck, 'sticky');
    assert.equal(geo.aboveTheList, true, 'the drawing belongs on top of the list');
    assert.equal(geo.besideTheForm, true, 'and beside the form, not under it');
    await b.close();
  });

  test('it really stays put when the page scrolls', async () => {
    const b = await builder({ width: 1440, height: 900 });
    await b.family('cartridge');
    const before = await b.page.evaluate(() =>
      document.getElementById('vizPanel').getBoundingClientRect().top);
    await b.page.evaluate(() => window.scrollBy(0, 900));
    const after = await b.page.evaluate(() =>
      document.getElementById('vizPanel').getBoundingClientRect().top);
    assert.ok(Math.abs(after - before) < 40 || after > 0,
      `the drawing scrolled away: ${Math.round(before)} to ${Math.round(after)}`);
    assert.ok(after > -10, 'the drawing must not leave the top of the screen');
    await b.close();
  });

  test('on a phone it takes the top of the screen instead', async () => {
    const b = await builder({ width: 390, height: 844 });
    await b.family('cartridge');
    const geo = await b.page.evaluate(() => {
      const panel = document.getElementById('vizPanel');
      const steps = document.querySelector('.steps').getBoundingClientRect();
      return {
        position: getComputedStyle(panel).position,
        aboveTheSteps: panel.getBoundingClientRect().top <= steps.top + 1,
        callouts: [...document.querySelectorAll('#vizArt .callout-n')]
          .every((g) => getComputedStyle(g).display !== 'none'),
      };
    });
    assert.equal(geo.position, 'sticky');
    assert.equal(geo.aboveTheSteps, true, 'the drawing has to come before the form on a phone');
    assert.equal(geo.callouts, true, 'the callout numbers are how the boxes are matched up');
    assert.equal(await b.overflows(), false);
    await b.close();
  });

  test('revealing the drawing does not move the form under your finger', async () => {
    // On a phone the drawing goes above the steps, so the first family picked
    // pushes everything down by the height of the panel. The tile you just
    // tapped has to stay where you tapped it.
    for (const width of [390, 768, 1440]) {
      const b = await builder({ width, height: 844 });
      for (const y of [0, 300, 700]) {
        await b.page.reload();
        // instant, or the page's own smooth scrolling is still animating when
        // the measurement is taken and the test measures its own scroll
        await b.page.evaluate((to) => window.scrollTo({ top: to, behavior: 'instant' }), y);
        const moved = await b.page.evaluate(() => {
          const tiles = document.getElementById('famTiles');
          const before = tiles.getBoundingClientRect().top;
          document.querySelector('[data-fam="cartridge"]').click();
          return tiles.getBoundingClientRect().top - before;
        });
        assert.ok(Math.abs(moved) < 3,
          `at ${width}px and scroll ${y} the tiles jumped ${Math.round(moved)}px`);
      }
      await b.close();
    }
  });

  test('no overflow and no tiny controls at any width, in either view', async () => {
    for (const width of [360, 390, 768, 900, 1024, 1041, 1280, 1440]) {
      const b = await builder({ width, height: 900 });
      await b.family('cartridge');
      await b.spec(REAL.cartridge);
      await b.add();
      assert.equal(await b.overflows(), false, `builder overflows at ${width}`);
      await b.mode('iso');
      assert.equal(await b.overflows(), false, `isometric overflows at ${width}`);
      if (width <= 900) {
        const small = await b.smallTapTargets();
        assert.deepEqual(small, [], `controls under 44px at ${width}: ${small.join(', ')}`);
      }
      await b.review();
      assert.equal(await b.overflows(), false, `document overflows at ${width}`);
      await b.close();
    }
  });
});
