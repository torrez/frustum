import argparse
import math
from typing import NamedTuple


class FlatPattern(NamedTuple):
    inner_radius: float
    outer_radius: float
    sweep_degrees: float
    straight_slant: float


def flat_pattern(top_diameter, bottom_diameter, height):
    r_top = top_diameter / 2
    r_bot = bottom_diameter / 2
    diff = abs(r_bot - r_top)
    slant = math.sqrt(diff ** 2 + height ** 2)
    r_outer = max(r_top, r_bot) * slant / diff
    r_inner = min(r_top, r_bot) * slant / diff
    sweep_degrees = 360 * diff / slant
    return FlatPattern(
        inner_radius=r_inner,
        outer_radius=r_outer,
        sweep_degrees=sweep_degrees,
        straight_slant=slant,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Compute the flat pattern (annular sector) for a frustum.",
    )
    parser.add_argument("top_diameter", type=float)
    parser.add_argument("bottom_diameter", type=float)
    parser.add_argument("height", type=float)
    args = parser.parse_args()

    pattern = flat_pattern(args.top_diameter, args.bottom_diameter, args.height)
    print(f"Inner arc radius: {pattern.inner_radius:.3f}")
    print(f"Outer arc radius: {pattern.outer_radius:.3f}")
    print(f"Sweep angle:      {pattern.sweep_degrees:.3f}°")
    print(f"Straight slant:   {pattern.straight_slant:.3f}")


if __name__ == "__main__":
    main()
