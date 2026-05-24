import math
import subprocess
import sys
import unittest
from pathlib import Path

from frustum import flat_pattern

SCRIPT = Path(__file__).parent / "frustum.py"


class TestFlatPattern(unittest.TestCase):
    def test_known_frustum_6_10_3(self):
        """Hand-verified: top=6, bottom=10, height=3 -> slant=sqrt(13)."""
        result = flat_pattern(top_diameter=6, bottom_diameter=10, height=3)
        sqrt13 = math.sqrt(13)
        self.assertAlmostEqual(result.straight_slant, sqrt13, places=10)
        self.assertAlmostEqual(result.outer_radius, 5 * sqrt13 / 2, places=10)
        self.assertAlmostEqual(result.inner_radius, 3 * sqrt13 / 2, places=10)
        self.assertAlmostEqual(result.sweep_degrees, 360 * 2 / sqrt13, places=10)

    def test_inverted_frustum_matches_upright(self):
        """Swapping top and bottom yields the same flat pattern."""
        upright = flat_pattern(top_diameter=6, bottom_diameter=10, height=3)
        inverted = flat_pattern(top_diameter=10, bottom_diameter=6, height=3)
        self.assertAlmostEqual(upright.inner_radius, inverted.inner_radius, places=10)
        self.assertAlmostEqual(upright.outer_radius, inverted.outer_radius, places=10)
        self.assertAlmostEqual(upright.sweep_degrees, inverted.sweep_degrees, places=10)
        self.assertAlmostEqual(upright.straight_slant, inverted.straight_slant, places=10)

    def test_arc_lengths_match_circle_circumferences(self):
        """Rolling the pattern back into a frustum: arcs must equal circumferences."""
        top_d, bot_d, h = 7.5, 13.25, 9
        result = flat_pattern(top_diameter=top_d, bottom_diameter=bot_d, height=h)
        theta_rad = math.radians(result.sweep_degrees)
        outer_arc = result.outer_radius * theta_rad
        inner_arc = result.inner_radius * theta_rad
        self.assertAlmostEqual(outer_arc, math.pi * bot_d, places=10)
        self.assertAlmostEqual(inner_arc, math.pi * top_d, places=10)


class TestCLI(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            capture_output=True,
            text=True,
            check=True,
        )

    def test_cli_prints_all_four_labeled_values(self):
        result = self.run_cli(6, 10, 3)
        out = result.stdout
        self.assertIn("Inner arc radius:", out)
        self.assertIn("Outer arc radius:", out)
        self.assertIn("Sweep angle:", out)
        self.assertIn("Straight slant:", out)

    def test_cli_values_match_math(self):
        result = self.run_cli(6, 10, 3)
        sqrt13 = math.sqrt(13)
        self.assertIn(f"{3 * sqrt13 / 2:.3f}", result.stdout)
        self.assertIn(f"{5 * sqrt13 / 2:.3f}", result.stdout)
        self.assertIn(f"{360 * 2 / sqrt13:.3f}", result.stdout)
        self.assertIn(f"{sqrt13:.3f}", result.stdout)


if __name__ == "__main__":
    unittest.main()
