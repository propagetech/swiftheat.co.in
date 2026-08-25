# Tests for the heater list builder

100 cases, about 32 seconds, real Chrome. No build step and no browser download:
this uses `playwright-core` against the Chrome already installed on the machine,
the same approach as the house `contrast-audit.mjs`.

```bash
cd tests
npm install     # once
npm test
```

The test server starts and stops itself on a free port. Nothing to launch first.

Two files:

| File | What it is for |
| --- | --- |
| `builder.test.mjs` | The walk a person takes. Named behaviours, geometry snapshots, regressions. |
| `permutations.test.mjs` | The space, not the walk. Every option of every group of every family, crossed with every other group, then crossed again with the extremes of every dimension. |

## What is covered

| Group | What it protects |
| --- | --- |
| `regressions` | Bugs that actually shipped into the working tree during the build. Named so a repeat failure explains itself. |
| `drawing responds to the numbers` | The outline, the shaded heated region and the bore change correctly as dimensions change. |
| `drawing responds to the options` | Termination, thermocouple, all five lead protections, all four mountings, fins, split bands and coil section all change the drawing, and clear again when switched back. |
| `drawing snapshots` | Twenty recorded drawings across all seven views, including every bend form, both band constructions with clamps and terminals, and every sensor junction. Any unintended change to the artwork fails. |
| `part codes` | Prefix per family, full code assembly, live update on option change. |
| `the list` | Totals, per line identity, remove down to zero and back, the customer step appearing at the right time. |
| `validation` | Out of range warns but never blocks an enquiry. |
| `the generated document` | Row order, quantities, round tripping back to the list, unstated fields reading as "Not stated". |
| `responsive` | No overflow at 375, 768 and 1280 through a full build, in both views. |
| `accessibility` | Contrast on selected tiles and `aria-pressed`, which a cold page load never reaches so the contrast audit script cannot see them. |

## The permutation sweep

`permutations.test.mjs` renders roughly five thousand configurations in about
ten seconds. It can afford to because the sweep runs **inside the page**:
clicking an option is synchronous, so a whole cartesian product costs one round
trip instead of one per combination. What comes back is the evidence, not the
drawings.

Every configuration has to satisfy all six of these:

1. it draws something, with no `NaN`, no `undefined` and no empty attributes
2. nothing is drawn outside the frame, shapes or text
3. the callout numbers on the drawing are exactly the numbered boxes in the form
4. the part code carries every code that was chosen
5. no two options in the same group draw the same picture
6. no page errors, ever

Point 5 is the one that earns its keep. Before this suite existed, **18 of the
26 option groups changed nothing on the drawing**: a tubular heater bent to a U
form was drawn as a straight bar, a band heater's clamping and terminals were
invisible, and a thermocouple's junction and connection were not drawn at all.
Every one of those passed the old tests, because the old tests only asserted on
the options somebody had remembered to draw. Asserting that siblings differ
turns "did we draw this option" into a question the suite asks by itself, and it
will ask again for every option added later.

Crossed with the dimension sets (`blank`, `smallest`, `largest`, `zero`,
`negative`, `huge`, `tiny`, `not a number`) the same six checks cover the cases
that break drawings in practice: a length of 999999 that pushes a dimension line
off the frame, a zero that collapses a body to nothing, a typed minus sign.

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

## Watching it work

```bash
npm run demo
```

Opens one window and steps through the same ground the suite covers, with a
caption, slowly enough to see the drawing answer each keystroke. `HEADLESS=1`
runs the same script without a window, which is only useful for proving the
script itself still works.

## The regression tests

1. **Adding an item actually adds it.** `renderCart` destroyed its own empty
   state node and threw, which stopped every button listener below it from
   binding. Part codes still rendered perfectly, so the page looked fine while
   nothing could be added. Asserting on the part code would have passed.
2. **No horizontal overflow at 375px.** A CSS grid `1fr` column sized itself to
   its content, 636px wide inside a 375px viewport.
3. **Every control at least 44px on mobile.** The CSS styled `input` but not
   `select`, so the one family whose diameter is a dropdown had a 19px target.
4. **The drawing really sticks on a phone.** The mobile layout put the drawing in
   its own grid row. A sticky item can only stick inside its own grid area,
   which for a single-row item is its own height, so it scrolled away exactly as
   if nothing had been set. A flex column fixes it, because there the containing
   block is the whole column.
5. **The drawing panel does not push the page sideways.** Bleeding the panel to
   the screen edges with a negative margin made it wider than its flex parent,
   and the whole page scrolled horizontally.
