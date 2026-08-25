/* Geometry snapshots.
   We snapshot the drawing as numbers, not pixels. A JSON baseline diffs
   readably in git, does not flake on font rendering or GPU, and when it
   changes you can see exactly which shape moved. Refresh with:
     UPDATE_SNAPSHOTS=1 npm test  */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import assert from 'node:assert/strict';

const DIR = join(dirname(fileURLToPath(import.meta.url)), '__snapshots__');

export function matchSnapshot(name, value) {
  if (!existsSync(DIR)) mkdirSync(DIR, { recursive: true });
  const file = join(DIR, `${name}.json`);
  const actual = JSON.stringify(value, null, 2);

  if (process.env.UPDATE_SNAPSHOTS === '1' || !existsSync(file)) {
    writeFileSync(file, actual + '\n');
    if (process.env.UPDATE_SNAPSHOTS !== '1') {
      console.log(`  (wrote new snapshot ${name}.json, commit it)`);
    }
    return;
  }
  const expected = readFileSync(file, 'utf8').trim();
  assert.equal(actual, expected,
    `Drawing geometry changed for "${name}".\n` +
    `If the change is intended, run: UPDATE_SNAPSHOTS=1 npm test  then commit the diff.`);
}
