/* Test harness: serves the proposal folder, drives the builder in real Chrome.
   Uses node:test and playwright-core, no extra dependencies and no browser
   download, the same approach as the house contrast-audit script. */
import { chromium } from 'playwright-core';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import net from 'node:net';

const HERE = dirname(fileURLToPath(import.meta.url));
export const SITE = join(HERE, '..', 'proposal');

async function freePort() {
  return new Promise((res) => {
    const srv = net.createServer();
    srv.listen(0, () => { const { port } = srv.address(); srv.close(() => res(port)); });
  });
}

let server, browser, baseURL;

export async function start() {
  const port = await freePort();
  baseURL = `http://127.0.0.1:${port}`;
  server = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1'],
    { cwd: SITE, stdio: 'ignore' });
  // wait for it to answer rather than sleeping a fixed amount
  for (let i = 0; i < 100; i++) {
    try { const r = await fetch(baseURL + '/index.html'); if (r.ok) break; } catch {}
    await new Promise((r) => setTimeout(r, 100));
  }
  browser = await chromium.launch({
    channel: 'chrome',
    headless: process.env.HEADED !== '1',
    slowMo: Number(process.env.SLOWMO || 0),
  });
  return baseURL;
}

export async function stop() {
  if (browser) await browser.close();
  if (server) server.kill();
}

/** Open the builder at a given viewport and hand back a driver. */
export async function builder({ width = 1280, height = 900 } = {}) {
  const ctx = await browser.newContext({ viewport: { width, height } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  await page.goto(`${baseURL}/mockup/bom-builder.html`, { waitUntil: 'load' });
  return new Driver(page, ctx, errors);
}

class Driver {
  constructor(page, ctx, errors) { this.page = page; this.ctx = ctx; this.errors = errors; }
  async close() { await this.ctx.close(); }

  family(key) { return this.page.click(`[data-fam="${key}"]`); }

  async spec(values) {
    await this.page.evaluate((vals) => {
      for (const [k, v] of Object.entries(vals)) {
        const el = document.getElementById('sp_' + k);
        if (!el) throw new Error('no spec field: ' + k);
        el.value = String(v);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }, values);
  }

  async option(group, code) { await this.page.click(`[data-g="${group}"][data-c="${code}"]`); }

  async field(id, value) {
    await this.page.evaluate(({ id, value }) => {
      const el = document.getElementById(id);
      el.value = String(value);
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
    }, { id, value });
  }

  mode(m) { return this.page.click(`[data-mode="${m}"]`); }
  toggleHidden() { return this.page.evaluate(() => document.getElementById('viewToggle').hidden); }
  specValues(keys) {
    return this.page.evaluate((ks) => ks.map((k) => document.getElementById('sp_' + k).value).join('/'), keys);
  }

  add() { return this.page.click('#addBtn'); }
  review() { return this.page.click('#reviewBtn'); }
  back() { return this.page.click('#backBtn'); }

  partCode() { return this.page.textContent('#partCode'); }
  cartCount() { return this.page.textContent('#cartCount'); }
  totals() {
    return this.page.evaluate(() => ({
      lines: document.getElementById('totLines').textContent,
      qty: document.getElementById('totQty').textContent,
    }));
  }
  lineCodes() {
    return this.page.$$eval('.line .pc', (els) => els.map((e) => e.textContent.trim()));
  }

  /** A normalised description of the drawing: shapes and rounded numbers only,
      so it is stable across machines and readable in a git diff. */
  geometry() {
    return this.page.evaluate(() => {
      const svg = document.querySelector('#vizArt svg');
      if (!svg) return null;
      const r = (v) => (v === null || v === '' ? null : Math.round(parseFloat(v) * 10) / 10);
      const out = [];
      for (const el of svg.querySelectorAll('rect, circle, path, text')) {
        const t = el.tagName.toLowerCase();
        const cls = el.getAttribute('class') || el.parentElement?.getAttribute('class') || '';
        if (t === 'rect') out.push({ t, cls, x: r(el.getAttribute('x')), y: r(el.getAttribute('y')), w: r(el.getAttribute('width')), h: r(el.getAttribute('height')) });
        else if (t === 'circle') out.push({ t, cls, cx: r(el.getAttribute('cx')), cy: r(el.getAttribute('cy')), rad: r(el.getAttribute('r')) });
        else if (t === 'text') out.push({ t, cls, s: el.textContent.trim() });
        else out.push({ t, cls, w: r(el.getAttribute('stroke-width')), len: (el.getAttribute('d') || '').length });
      }
      return out;
    });
  }

  /** The body outline and the shaded heated region, the two shapes that carry
      meaning. Both are named in the drawing, so this cannot pick up a sleeve or
      a terminal block by accident. */
  bodyShapes() {
    return this.page.evaluate(() => {
      const read = (sel) => {
        const r = document.querySelector('#vizArt svg ' + sel);
        return r ? { x: +r.getAttribute('x'), y: +r.getAttribute('y'),
          w: +r.getAttribute('width'), h: +r.getAttribute('height') } : null;
      };
      return { outline: read('rect.body'), heated: read('rect.heated') };
    });
  }

  /** The bore and outer wall of a ring drawing. */
  ringRadii() {
    return this.page.evaluate(() => {
      const r = (sel) => {
        const el = document.querySelector('#vizArt svg ' + sel);
        return el ? +el.getAttribute('r') : null;
      };
      return { bore: r('circle.bore'), wall: r('circle.wall') };
    });
  }

  has(selector) { return this.page.evaluate((s) => !!document.querySelector(s), selector); }

  overflows() {
    return this.page.evaluate(() => {
      const d = document.documentElement;
      return d.scrollWidth > d.clientWidth;
    });
  }

  smallTapTargets() {
    return this.page.evaluate(() => [...document.querySelectorAll('a,button,input,select,textarea')]
      .filter((e) => { const r = e.getBoundingClientRect(); return r.height > 0 && r.height < 44; })
      .filter((e) => !e.classList.contains('skip'))
      .map((e) => (e.textContent || e.id || e.tagName).trim().slice(0, 30) + ' h=' + Math.round(e.getBoundingClientRect().height)));
  }

  docRows() {
    return this.page.$$eval('#docBody tr', (rows) => rows.map((r) => ({
      n: r.cells[0].textContent.trim(), part: r.cells[1].textContent.trim(),
      fam: r.cells[2].textContent.trim(), qty: r.cells[4].textContent.trim(),
    })));
  }
}

/* ------------------------------------------------------------------ *
 * Exhaustive sweeps.
 *
 * A permutation sweep runs entirely inside the page: clicking an option
 * is synchronous, so a whole cartesian product costs one round trip
 * instead of one per combination. What comes back is the evidence, not
 * the raw drawings: every violation found, plus a signature per option
 * so a group that draws the same thing for two different codes can be
 * caught.
 * ------------------------------------------------------------------ */
Object.assign(Driver.prototype, {
  /** The family, spec and option model as the page itself sees it. */
  model() {
    return this.page.evaluate(() => {
      const out = [];
      for (const btn of document.querySelectorAll('[data-fam]')) {
        btn.click();
        out.push({
          fam: btn.getAttribute('data-fam'),
          iso: !document.getElementById('viewToggle').hidden,
          dims: [...document.querySelectorAll('#dimFields [data-k]')].map((e) => e.getAttribute('data-k')),
          elec: [...document.querySelectorAll('#elecFields [data-k]')].map((e) => e.getAttribute('data-k')),
          specs: [...document.querySelectorAll('[data-k]')].map((e) => ({
            k: e.getAttribute('data-k'),
            tag: e.tagName.toLowerCase(),
            min: e.getAttribute('min'), max: e.getAttribute('max'),
            opts: [...e.querySelectorAll('option')].map((o) => o.value).filter(Boolean),
          })),
          groups: [...document.querySelectorAll('.optgroup')].map((g) => ({
            k: g.querySelector('[data-g]').getAttribute('data-g'),
            title: g.querySelector('h3').textContent,
            opts: [...g.querySelectorAll('[data-c]')].map((b) => b.getAttribute('data-c')),
          })),
        });
      }
      return out;
    });
  },

  /** Run every combination of every option group for one family. */
  sweep(fam, spec = {}) {
    return this.page.evaluate(({ fam, spec }) => {
      const $ = (id) => document.getElementById(id);
      document.querySelector(`[data-fam="${fam}"]`).click();
      for (const [k, v] of Object.entries(spec)) {
        const el = $('sp_' + k);
        if (!el) continue;
        el.value = String(v);
        el.dispatchEvent(new Event('input', { bubbles: true }));
      }

      const groups = [...document.querySelectorAll('.optgroup')].map((g) => ({
        k: g.querySelector('[data-g]').getAttribute('data-g'),
        opts: [...g.querySelectorAll('[data-c]')].map((b) => b.getAttribute('data-c')),
      }));

      /* the drawing, judged: bad numbers, anything drawn outside the frame,
         an empty drawing, or a part code missing a code that was chosen */
      const inspect = (combo) => {
        const bad = [];
        const svg = document.querySelector('#vizArt svg');
        if (!svg) return ['no drawing at all'];
        const box = svg.getAttribute('viewBox').split(' ').map(Number);
        const markup = svg.innerHTML;
        const junk = markup.match(/NaN|Infinity|undefined|null|=""/);
        if (junk) bad.push('bad number or empty attribute in the drawing: ' + junk[0]);

        const shapes = svg.querySelectorAll('rect, circle, ellipse, path');
        if (shapes.length < 4) bad.push('only ' + shapes.length + ' shapes drawn');
        for (const el of shapes) {
          const b = el.getBBox();
          if (b.width === 0 && b.height === 0) continue;
          if (b.x < -1 || b.y < -1 || b.x + b.width > box[2] + 1 || b.y + b.height > box[3] + 1) {
            bad.push(el.tagName + '.' + (el.getAttribute('class') || el.parentElement.getAttribute('class') || '') +
              ' is drawn outside the frame: ' +
              [b.x, b.y, b.width, b.height].map((n) => Math.round(n)).join(','));
          }
        }
        for (const t of svg.querySelectorAll('text')) {
          const b = t.getBBox();
          if (b.x < -1 || b.x + b.width > box[2] + 1 || b.y + b.height > box[3] + 8) {
            bad.push('text "' + t.textContent.slice(0, 18) + '" outside the frame');
          }
        }

        const code = $('partCode').textContent;
        for (const c of Object.values(combo)) {
          if (!code.split('-').includes(c)) bad.push('part code ' + code + ' is missing ' + c);
        }
        /* the callouts on the drawing and the numbered boxes in the form must
           be the same set of numbers, or a number means two different things */
        const drawn = [...svg.querySelectorAll('.callout-n text')].map((t) => +t.textContent).sort();
        const boxed = [...document.querySelectorAll('#dimFields .num')].map((n) => +n.textContent).sort();
        if (drawn.join() !== boxed.join()) {
          bad.push('callouts ' + drawn.join() + ' do not match the boxes ' + boxed.join());
        }
        return bad.map((b) => b + '  [' + Object.values(combo).join(' ') + ']');
      };

      const violations = [];
      const sigs = {};       /* group -> code -> drawing signature */
      let combos = 0;

      const walk = (i, combo) => {
        if (i === groups.length) {
          combos++;
          violations.push(...inspect(combo));
          const markup = document.querySelector('#vizArt svg').innerHTML;
          for (const g of groups) {
            sigs[g.k] = sigs[g.k] || {};
            /* record one signature per code, all other groups held equal */
            const key = groups.map((x) => (x.k === g.k ? '*' : combo[x.k])).join('|');
            sigs[g.k][combo[g.k]] = sigs[g.k][combo[g.k]] || {};
            sigs[g.k][combo[g.k]][key] = markup.length + ':' + hash(markup);
          }
          return;
        }
        for (const c of groups[i].opts) {
          document.querySelector(`[data-g="${groups[i].k}"][data-c="${c}"]`).click();
          walk(i + 1, { ...combo, [groups[i].k]: c });
        }
      };
      function hash(s) {
        let h = 5381;
        for (let i = 0; i < s.length; i++) h = ((h * 33) ^ s.charCodeAt(i)) >>> 0;
        return h.toString(36);
      }
      if (groups.length) walk(0, {}); else { combos = 1; violations.push(...inspect({})); }

      /* for every group, is every code drawn differently from its siblings,
         with the rest of the configuration held constant? */
      const sameDrawing = [];
      for (const g of groups) {
        const codes = Object.keys(sigs[g.k]);
        const keys = Object.keys(sigs[g.k][codes[0]]);
        for (const key of keys) {
          const seen = new Map();
          for (const c of codes) {
            const sig = sigs[g.k][c][key];
            if (seen.has(sig)) sameDrawing.push(g.k + ': ' + seen.get(sig) + ' and ' + c + ' draw the same thing');
            else seen.set(sig, c);
          }
        }
      }
      return { combos, violations, sameDrawing: [...new Set(sameDrawing)] };
    }, { fam, spec });
  },

  /** Push one value into one spec field and report what the page did with it. */
  probe(k, value) {
    return this.page.evaluate(({ k, value }) => {
      const el = document.getElementById('sp_' + k);
      if (!el) throw new Error('no spec field: ' + k);
      el.value = String(value);
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
      const svg = document.querySelector('#vizArt svg');
      const box = svg.getAttribute('viewBox').split(' ').map(Number);
      const out = { junk: null, outside: [], warned: false, code: document.getElementById('partCode').textContent };
      const m = svg.innerHTML.match(/NaN|Infinity|undefined/);
      out.junk = m ? m[0] : null;
      for (const el2 of svg.querySelectorAll('rect, circle, ellipse, path')) {
        const b = el2.getBBox();
        if (b.width === 0 && b.height === 0) continue;
        if (b.x < -1 || b.y < -1 || b.x + b.width > box[2] + 1 || b.y + b.height > box[3] + 1) {
          out.outside.push(el2.tagName + ' ' + [b.x, b.y, b.width, b.height].map((n) => Math.round(n)).join(','));
        }
      }
      const wrap = document.getElementById('wrap_' + k);
      const err = wrap && wrap.querySelector('.err');
      out.warned = !!(err && !err.hidden);
      return out;
    }, { k, value });
  },
});
