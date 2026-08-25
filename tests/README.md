# Tests for the heater list builder

44 cases, about 23 seconds, real Chrome. No build step and no browser download:
this uses `playwright-core` against the Chrome already installed on the machine,
the same approach as the house `contrast-audit.mjs`.

```bash
cd tests
npm install     # once
npm test
```

The test server starts and stops itself on a free port. Nothing to launch first.

## What is covered

| Group | What it protects |
| --- | --- |
| `regressions` | Four bugs that actually shipped into the working tree during the build. Named so a repeat failure explains itself. |
| `drawing responds to the numbers` | The outline, the shaded heated region and the bore change correctly as dimensions change. |
| `drawing responds to the options` | Termination, thermocouple, lead protection, fins, split bands and coil section all change the drawing, and clear again when switched back. |
| `drawing snapshots` | Eight recorded drawings across all five views. Any unintended change to the artwork fails. |
| `part codes` | Prefix per family, full code assembly, live update on option change. |
| `the list` | Totals, per line identity, remove down to zero and back, the customer step appearing at the right time. |
| `validation` | Out of range warns but never blocks an enquiry. |
| `the generated document` | Row order, quantities, round tripping back to the list, unstated fields reading as "Not stated". |
| `responsive` | No overflow at 375, 768 and 1280 through a full build, in both views. Fields on the drawing at desktop, stacked with numbered callouts on a phone. |
| `accessibility` | Contrast on selected tiles and `aria-pressed`, which a cold page load never reaches so the contrast audit script cannot see them. |

## Visual regression, without pixels

`drawing snapshots` records the drawing as **geometry, not a screenshot**:
shapes with rounded coordinates, written to `__snapshots__/*.json`.

That is deliberate. Image baselines flake on font rendering, GPU and OS, and a
failure gives you two pictures to squint at. A JSON baseline diffs readably in
git, so a failure tells you exactly which rectangle moved and by how much.

Verified to work: narrowing the drawn body from 260 to 258 units, a change far
too small to notice by eye, fails four snapshot tests.

When a drawing change is intentional:

```bash
npm run test:update
```

Then read the diff before committing it. The point of the baseline is that
somebody looks at what changed.

## The four regression tests

1. **Adding an item actually adds it.** `renderCart` destroyed its own empty
   state node and threw, which stopped every button listener below it from
   binding. Part codes still rendered perfectly, so the page looked fine while
   nothing could be added. Asserting on the part code would have passed.
2. **No horizontal overflow at 375px.** A CSS grid `1fr` column sized itself to
   its content, 636px wide inside a 375px viewport.
3. **Every control at least 44px on mobile.** The CSS styled `input` but not
   `select`, so the one family whose diameter is a dropdown had a 19px target.
4. **Fields do not overlap the drawn body.** The diameter callout sat on top of
   the heater at desktop width.
