# Frustum Flat-Pattern CLI — Design

## Purpose

A command-line utility that computes the unrolled lateral surface (annular
sector) of a frustum given its top diameter, bottom diameter, and height.
Replaces the Fusion 360 step in a slab-built ceramics workflow.

## Inputs

Three positional floats, in this order:

1. `top_diameter`
2. `bottom_diameter`
3. `height`

All three are unit-agnostic — the script preserves whatever the user provides
(inches, mm, cm). No flags, no interactive prompts.

Example: `python frustum.py 10 6 8`

## Outputs

Four labeled values, each on its own line:

- **Inner arc radius** — distance from the apex of the cone-extension to the
  smaller circle, measured along the slant.
- **Outer arc radius** — distance from the apex to the larger circle.
- **Sweep angle** — angle subtended by the annular sector, in degrees.
- **Straight slant** — length of the two straight edges connecting the inner
  and outer arcs. Equal to the frustum's slant height.

Units match the inputs except sweep angle, which is always degrees.

## Math

Let `r_top = top_diameter / 2`, `r_bot = bottom_diameter / 2`, `h = height`.

```
diff      = abs(r_bot - r_top)
slant     = sqrt(diff² + h²)
r_outer   = max(r_top, r_bot) · slant / diff
r_inner   = min(r_top, r_bot) · slant / diff
sweep_deg = 360 · diff / slant
```

The straight-slant output equals `slant`, which also equals `r_outer - r_inner`.

### Derivation

The frustum's side, extended to a point, forms a full cone whose apex sits
along the central axis. The slant from apex to each circle is, by similar
triangles, proportional to that circle's radius. Unrolling the cone gives an
annular sector whose outer arc must equal the larger circle's circumference
and whose inner arc must equal the smaller circle's circumference; both
constraints are satisfied by `sweep_deg = 360 · diff / slant`.

### Inverted frustums

When `top_diameter > bottom_diameter` (e.g. a flared vase), the flat pattern
is identical to the non-inverted case with top and bottom swapped — the
unrolled lateral surface doesn't care about orientation. Using `abs`, `max`,
and `min` makes the formulas symmetric in `r_top` and `r_bot`, so the script
gives correct results for either orientation without branching.

### Cylinder case (out of scope)

If `top_diameter == bottom_diameter`, `diff == 0` and the formulas
divide by zero. Per design discussion, this is not handled — the user opted
out of a cylinder special case.

## Structure

A single file, `frustum.py`, with no third-party dependencies. Standard
library only (`argparse`, `math`). The math lives in one pure function that
takes three floats and returns the four output values; the CLI wrapper parses
arguments and prints results.

This split keeps the math testable in isolation from the CLI surface.

## Output format

Plain text, one labeled value per line, aligned for readability:

```
Inner arc radius: 12.345
Outer arc radius: 23.456
Sweep angle:      87.654°
Straight slant:   11.111
```

Precision: three decimal places. This is enough for marking out a clay slab
and avoids implying false precision from float arithmetic.

## Out of scope

- Generating SVG / DXF template files
- Input validation (negative numbers, zero, non-numeric)
- Cylinder special case
- Configurable precision or output format
- Unit conversion
