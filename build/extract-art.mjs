/* Pull one static drawing per product family out of the list builder, so the
   product pages carry exactly the artwork the configurator draws.

   The builder is the source of truth for the geometry and it is covered by the
   test suite in tests/, so this keeps the product pages from drifting away from
   the tool. Run it after changing the drawing code:

       node build/extract-art.mjs

   Needs the test dependencies:  cd tests && npm install
*/
import { chromium } from '../tests/node_modules/playwright-core/index.mjs';
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import net from 'node:net';

const HERE = dirname(fileURLToPath(import.meta.url));
const SITE = join(HERE, '..');
const OUT = join(HERE, 'art');

// One representative configuration per family. Mid range sizes, and the option
// in each group that shows the most of the drawing.
const CASES = [
  ['cartridge', { dia: '12.5', len: 200, hlen: 180, watt: 400, volt: '230' }, [['term','T1'],['lead','L1'],['tc','TC0'],['mount','M0']]],
  ['coil',      { id: 30, hlen: 120, watt: 500, volt: '230' }, [['prof','PT'],['exit','ER'],['tc','TCK']]],
  ['band',      { id: 90, width: 60, watt: 800, volt: '230' }, [['mat','CE'],['con','C2'],['clamp','K1'],['term','S1']]],
  ['nozzle',    { id: 40, len: 60, watt: 400, volt: '230' }, [['mat','CE'],['tc','TCK']]],
  ['strip',     { len: 400, width: 50, watt: 800, volt: '230' }, [['prof','F1'],['term','S1']]],
  ['tubular',   { dia: '12.5', len: 600, watt: 1500, volt: '230' }, [['bend','BU'],['sheath','IN'],['term','S0']]],
  ['sensor',    { dia: '6', len: 300, clen: 2000 }, [['type','K'],['junc','U'],['conn','H']]],
  ['ir',        { watt: 650, volt: '230', dist: 150 }, [['form','FT'],['tc','TCK'],['refl','R1']]],
];

const port = await new Promise((res) => {
  const s = net.createServer();
  s.listen(0, () => { const { port } = s.address(); s.close(() => res(port)); });
});
const server = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1'],
  { cwd: SITE, stdio: 'ignore' });
const base = `http://127.0.0.1:${port}`;
for (let i = 0; i < 100; i++) {
  try { const r = await fetch(base + '/index.html'); if (r.ok) break; } catch {}
  await new Promise((r) => setTimeout(r, 100));
}

const browser = await chromium.launch({ channel: 'chrome', headless: true });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
page.on('pageerror', (e) => { console.error('PAGE ERROR', e.message); process.exitCode = 1; });

for (const [fam, spec, opts] of CASES) {
  await page.goto(`${base}/build-a-list/`, { waitUntil: 'load' });
  await page.click(`[data-fam="${fam}"]`);
  await page.evaluate((vals) => {
    for (const [k, v] of Object.entries(vals)) {
      const el = document.getElementById('sp_' + k);
      if (!el) throw new Error('no spec field: ' + k);
      el.value = String(v);
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }, spec);
  for (const [g, c] of opts) await page.click(`[data-g="${g}"][data-c="${c}"]`);
  const svg = await page.evaluate(() => {
    const host = document.getElementById('vizArt');
    return host ? host.innerHTML.trim() : '';
  });
  if (!svg.startsWith('<svg')) throw new Error('no drawing for ' + fam);
  writeFileSync(join(OUT, fam + '.svg'), svg + '\n');
  console.log(fam.padEnd(10), svg.length, 'bytes');
}

await browser.close();
server.kill();
