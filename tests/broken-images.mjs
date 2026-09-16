/* Load every live page and report broken images.
   Uses playwright-core against installed Chrome, same as the builder suite. */
import { chromium } from 'playwright-core';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { readFileSync } from 'node:fs';
import net from 'node:net';

const HERE = dirname(fileURLToPath(import.meta.url));
const SITE = join(HERE, '..');

function sitemapPaths() {
  const xml = readFileSync(join(SITE, 'sitemap.xml'), 'utf8');
  const locs = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => {
    const u = new URL(m[1]);
    return u.pathname.endsWith('/') ? u.pathname : u.pathname + '/';
  });
  if (!locs.includes('/404.html')) locs.push('/404.html');
  return locs;
}

async function freePort() {
  return new Promise((res) => {
    const srv = net.createServer();
    srv.listen(0, () => { const { port } = srv.address(); srv.close(() => res(port)); });
  });
}

function isAsset(url) {
  return /\.(png|jpe?g|webp|gif|svg|ico|avif|woff2?)(\?|$)/i.test(url);
}

const port = await freePort();
const baseURL = `http://127.0.0.1:${port}`;
const server = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1'],
  { cwd: SITE, stdio: 'ignore' });

for (let i = 0; i < 100; i++) {
  try { const r = await fetch(baseURL + '/index.html'); if (r.ok) break; } catch {}
  await new Promise((r) => setTimeout(r, 50));
}

const browser = await chromium.launch({ channel: 'chrome', headless: true });
const paths = sitemapPaths();
const report = [];

try {
  for (const path of paths) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();
    const failed = [];
    page.on('response', (res) => {
      const url = res.url();
      if (!url.startsWith(baseURL)) return;
      if (!isAsset(url) && res.request().resourceType() !== 'image') return;
      if (res.status() >= 400) {
        failed.push({ url: url.slice(baseURL.length), status: res.status(), type: res.request().resourceType() });
      }
    });
    page.on('requestfailed', (req) => {
      const url = req.url();
      if (!url.startsWith(baseURL)) return;
      if (!isAsset(url) && req.resourceType() !== 'image') return;
      failed.push({ url: url.slice(baseURL.length), status: 0, failure: req.failure()?.errorText, type: req.resourceType() });
    });

    const url = path === '/404.html' ? baseURL + '/404.html' : baseURL + path;
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.evaluate(() => {
      document.querySelectorAll('img[loading="lazy"]').forEach((img) => { img.loading = 'eager'; });
    });
    await page.waitForTimeout(200);

    const brokenImgs = await page.evaluate(() => {
      return Array.from(document.images).map((img) => ({
        src: img.currentSrc || img.getAttribute('src') || '',
        alt: img.getAttribute('alt') || '',
        complete: img.complete,
        naturalWidth: img.naturalWidth,
        naturalHeight: img.naturalHeight,
      })).filter((img) => !img.src || !img.complete || img.naturalWidth === 0);
    });

    const bgBroken = await page.evaluate(async () => {
      const urls = new Set();
      for (const el of document.querySelectorAll('*')) {
        const bg = getComputedStyle(el).backgroundImage;
        const m = [...bg.matchAll(/url\(["']?([^"')]+)["']?\)/g)];
        m.forEach((x) => urls.add(x[1]));
      }
      const out = [];
      for (const u of urls) {
        if (u.startsWith('data:')) continue;
        try {
          const r = await fetch(u, { method: 'HEAD' });
          if (!r.ok) out.push({ url: u, status: r.status });
        } catch (e) {
          out.push({ url: u, status: 0, failure: String(e) });
        }
      }
      return out;
    });

    report.push({ path, failed, brokenImgs, bgBroken });
    await ctx.close();
  }
} finally {
  await browser.close();
  server.kill();
}

let nFailed = 0;
let nBroken = 0;
for (const row of report) {
  nFailed += row.failed.length;
  nBroken += row.brokenImgs.length + row.bgBroken.length;
}

console.log(`Pages checked: ${report.length}`);
console.log(`Failed asset responses: ${nFailed}`);
console.log(`Broken <img> / background URLs: ${nBroken}`);

for (const row of report) {
  if (!row.failed.length && !row.brokenImgs.length && !row.bgBroken.length) continue;
  console.log('\n' + row.path);
  for (const f of row.failed) {
    console.log(`  HTTP ${f.status || 'FAIL'} ${f.type} ${f.url}${f.failure ? ' (' + f.failure + ')' : ''}`);
  }
  for (const img of row.brokenImgs) {
    console.log(`  IMG naturalWidth=0 complete=${img.complete} src=${img.src} alt="${img.alt}"`);
  }
  for (const bg of row.bgBroken) {
    console.log(`  BG HTTP ${bg.status} ${bg.url}`);
  }
}

if (nFailed || nBroken) process.exit(1);
console.log('\nNo broken images.');
