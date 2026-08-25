/* A watchable run of the same assertions the test suite makes.
   One window, one page, stepping slowly with a caption so you can see the
   drawing answer each change. Not a replacement for `npm test`, which runs
   the real 52 headless in about 26 seconds. */
import { chromium } from 'playwright-core';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import net from 'node:net';

const SITE = join(dirname(fileURLToPath(import.meta.url)), '..', 'proposal');
const PACE = Number(process.env.PACE || 3200);   // caption dwell
const KEY  = Number(process.env.KEY  || 170);    // delay between keystrokes

const freePort = () => new Promise((res) => {
  const s = net.createServer();
  s.listen(0, () => { const { port } = s.address(); s.close(() => res(port)); });
});

const port = await freePort();
const server = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1'],
  { cwd: SITE, stdio: 'ignore' });
for (let i = 0; i < 100; i++) {
  try { if ((await fetch(`http://127.0.0.1:${port}/index.html`)).ok) break; } catch {}
  await new Promise((r) => setTimeout(r, 100));
}

const browser = await chromium.launch({
  channel: 'chrome', headless: false,
  slowMo: Number(process.env.SLOWMO || 220),      // makes each click visible
});
const page = await browser.newPage({ viewport: { width: 1360, height: 940 } });
await page.goto(`http://127.0.0.1:${port}/mockup/bom-builder.html`);

await page.addStyleTag({ content: `
  /* the caption is informational only; it must never swallow a click */
  #demoCap{pointer-events:none;position:fixed;left:0;right:0;bottom:0;z-index:9999;
    background:hsl(214 32% 11%);color:#fff;font:600 17px/1.5 Inter,system-ui,sans-serif;
    padding:14px 22px;display:flex;gap:14px;align-items:baseline;
    box-shadow:0 -6px 24px hsl(214 32% 11% / .25)}
  #demoCap b{color:hsl(21 92% 51%);font-size:13px;letter-spacing:.14em;text-transform:uppercase}
  #demoCap span{flex:1}
  #demoCap i{font-style:normal;color:hsl(214 16% 66%);font-weight:400;font-size:14px}
  body{padding-bottom:96px}
  /* un-stick the header for the demo so it cannot cover a field being clicked */
  .masthead{position:static !important}
  .jump{position:static !important}
  .cart{position:static !important}
  html{scroll-behavior:auto !important}
  input,select{scroll-margin-top:120px;scroll-margin-bottom:120px}
` });
await page.evaluate(() => {
  const d = document.createElement('div');
  d.id = 'demoCap';
  d.innerHTML = '<b id="demoStep">start</b><span id="demoText"></span><i id="demoAssert"></i>';
  document.body.appendChild(d);
});

let n = 0;
const say = async (text, assertion = '') => {
  n++;
  await page.evaluate(({ n, text, assertion }) => {
    document.getElementById('demoStep').textContent = String(n).padStart(2, '0');
    document.getElementById('demoText').textContent = text;
    document.getElementById('demoAssert').textContent = assertion;
  }, { n, text, assertion });
  await page.waitForTimeout(PACE);
};

/* Type the value in rather than assigning it, so the drawing redraws on every
   keystroke and you can watch it answer the number as it is entered. */
const set = async (k, v) => {
  const sel = '#sp_' + k;
  const tag = await page.evaluate((s) => document.querySelector(s).tagName, sel);
  if (tag === 'SELECT') {
    await page.selectOption(sel, String(v));
    return;
  }
  await page.click(sel);
  await page.fill(sel, '');
  await page.locator(sel).pressSequentially(String(v), { delay: KEY });
  await page.waitForTimeout(400);
};

const typeInto = async (id, v) => {
  await page.click('#' + id);
  await page.locator('#' + id).fill('');
  await page.locator('#' + id).pressSequentially(String(v), { delay: Math.max(60, KEY / 2) });
};

const shape = () => page.evaluate(() => {
  const rs = [...document.querySelectorAll('#vizArt svg rect')].map((r) => ({
    w: +r.getAttribute('width'), h: +r.getAttribute('height'),
    filled: (r.getAttribute('fill') || 'none') !== 'none' }));
  const paths = [...document.querySelectorAll('#vizArt svg path')];
  const iso = document.querySelector('.iso-body');
  if (iso) {
    const bb = iso.getBBox();
    return { outline: { w: Math.round(bb.width), h: Math.round(bb.height) }, heated: null };
  }
  return { outline: rs.find((r) => !r.filled) || null, heated: rs.find((r) => r.filled) || null };
});

const code = () => page.textContent('#partCode');

// ---------------------------------------------------------------- run
await say('Pick a product family. Everything below adapts to it.');
await page.click('[data-fam="cartridge"]');

await say('Diameter 8 mm, length 400 mm. A long thin heater.');
await set('dia', '8'); await set('len', '400');
let s = await shape();
await say(`Drawn body height is ${s.outline.h}`, 'thin');

await say('Now diameter 25 mm, length 100 mm. Short and fat.');
await set('dia', '25'); await set('len', '100');
s = await shape();
await say(`Drawn body height is now ${s.outline.h}`, 'the drawing followed the numbers');

await say('Back to a realistic part: 12.5 mm x 200 mm.');
await set('dia', '12.5'); await set('len', '200');

await say('Heated length 50 of 200. Watch the shaded band.');
await set('hlen', '50');
s = await shape();
await say(`Shaded ${Math.round((s.heated.w / s.outline.w) * 100)}% of the body`, 'a quarter, as specified');

await say('Heated length 100 of 200.');
await set('hlen', '100');
s = await shape();
await say(`Shaded ${Math.round((s.heated.w / s.outline.w) * 100)}%`, 'cold zones stay equal at both ends');

await say('Heated length 200 of 200, the whole element.');
await set('hlen', '200');
s = await shape();
await say(s.heated.w === s.outline.w ? 'Shaded region equals the body' : 'mismatch',
  'nothing left cold');

await set('watt', '400'); await set('volt', '230');
await say(`Wattage and voltage are not dimensions, so they sit off the drawing.`, await code());

await say('Now the options. Right angle termination.');
await page.click('[data-g="term"][data-c="T2"]');
await say('The lead exit changed on the drawing.', await code());

await say('Double ended instead.');
await page.click('[data-g="term"][data-c="T3"]');
await say('Leads at both ends now.', await code());

await say('Add a type K thermocouple.');
await page.click('[data-g="tc"][data-c="TCK"]');
await say('The sensor and its run appear.', await code());

await say('Armoured lead protection.');
await page.click('[data-g="lead"][data-c="L4"]');
await say('The sleeve is drawn on the lead.', await code());

await say('Switch to the isometric drawing.');
await page.click('[data-mode="iso"]');
await say('Same numbers, same anchors, drawn as a tube.',
  await page.evaluate(() => ['dia','len','hlen'].map((k) => document.getElementById('sp_' + k).value).join(' / ')));

await say('Back to the flat dimensioned drawing.');
await page.click('[data-mode="flat"]');

await say('Add this heater to the list, 24 off.');
await typeInto('qty', 24);
await page.click('#addBtn');
await say('One line on the list.', await page.textContent('#cartCount'));

await say('A different family: ceramic band heater.');
await page.click('[data-fam="band"]');
await set('id', '90'); await set('width', '60'); await set('watt', '1200'); await set('volt', '240');
await say('Different fields, different drawing, its own options.', await code());

await say('Two piece construction.');
await page.click('[data-g="con"][data-c="C2"]');
await say('The band is drawn split.', await code());

await typeInto('qty', 6);
await page.click('#addBtn');
await say('Added. Two lines, thirty pieces.',
  JSON.stringify(await page.evaluate(() => ({
    lines: document.getElementById('totLines').textContent,
    pieces: document.getElementById('totQty').textContent }))));

await say('A strip heater, and make it finned.');
await page.click('[data-fam="strip"]');
await set('len', '400'); await set('width', '50'); await set('watt', '800'); await set('volt', '230');
await page.click('[data-g="prof"][data-c="F1"]');
await say('Fins drawn on.', await code());
await page.click('#addBtn');

await say('Out of range check: length 99999.');
await set('len', '99999');
await say(await page.isVisible('#wrap_len .err') ? 'Warned, but not blocked.' : 'no warning',
  'a warning must never stop a real enquiry');
await set('len', '400');

await say('Fill in who it is for.');
for (const [id, v] of [['cComp', 'Acme Moulders'], ['cName', 'R Prabhu'],
  ['cRef', 'PO-4471']]) {
  await typeInto(id, v);
}

await say('Generate the document.');
await page.click('#reviewBtn');
await say('Three lines, part codes, specifications and quantities.',
  `${(await page.$$('#docBody tr')).length} rows`);

await say('From here: save as PDF, email from your own address, or WhatsApp.');
await say('Done. Run "npm test" for the real suite: 52 checks in about 26 seconds.');

await page.waitForTimeout(4000);
await browser.close();
server.kill();
