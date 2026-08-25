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
  browser = await chromium.launch({ channel: 'chrome' });
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

  /** The body outline and the shaded heated region, the two shapes that carry meaning. */
  bodyShapes() {
    return this.page.evaluate(() => {
      const rects = [...document.querySelectorAll('#vizArt svg rect')]
        .map((r) => ({
          w: +r.getAttribute('width'), h: +r.getAttribute('height'),
          x: +r.getAttribute('x'), filled: (r.getAttribute('fill') || 'none') !== 'none',
        }));
      return { outline: rects.find((r) => !r.filled) || null, heated: rects.find((r) => r.filled) || null };
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
