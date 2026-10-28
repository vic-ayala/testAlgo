"""Regression tests for Cartesian-to-polar conversion and CSV output."""

import csv
import math
import tempfile
import unittest
from pathlib import Path

from algorithm import cartesian_to_polar, generate_random_pairs, write_pairs_to_csv


class PolarConversionTests(unittest.TestCase):
    def test_quadrants_axes_and_origin(self):
        examples = [
            (3.0, 4.0, 5.0, math.atan2(4.0, 3.0)),
            (-3.0, 4.0, 5.0, math.pi - math.atan(4.0 / 3.0)),
            (-3.0, -4.0, 5.0, -math.pi + math.atan(4.0 / 3.0)),
            (3.0, -4.0, 5.0, -math.atan(4.0 / 3.0)),
            (2.0, 0.0, 2.0, 0.0),
            (0.0, 2.0, 2.0, math.pi / 2),
            (-2.0, 0.0, 2.0, math.pi),
            (0.0, -2.0, 2.0, -math.pi / 2),
            (0.0, 0.0, 0.0, 0.0),
        ]
        for x, y, expected_radius, expected_angle in examples:
            with self.subTest(x=x, y=y):
                radius, angle = cartesian_to_polar(x, y)
                self.assertAlmostEqual(radius, expected_radius, places=12)
                self.assertAlmostEqual(angle, expected_angle, places=12)

    def test_radius_and_angle_reconstruct_point(self):
        for x, y in [(1.0, 8.0), (-7.0, 2.0), (-5.0, -9.0), (6.0, -3.0)]:
            with self.subTest(x=x, y=y):
                radius, angle = cartesian_to_polar(x, y)
                self.assertAlmostEqual(radius * math.cos(angle), x, places=12)
                self.assertAlmostEqual(radius * math.sin(angle), y, places=12)


class DatasetTests(unittest.TestCase):
    def test_seed_and_default_row_count(self):
        one = generate_random_pairs()
        two = generate_random_pairs()
        self.assertEqual(one, two)
        self.assertEqual(len(one), 1000)
        self.assertEqual([row[0] for row in one], list(range(1, 1001)))
        self.assertGreater(len({round(row[4], 8) for row in one}), 1)
        self.assertAlmostEqual(one[0][1], 5.9196533315, places=9)
        self.assertAlmostEqual(one[0][2], 11.6608847700, places=9)
        for _, x, y, radius, angle in one:
            self.assertAlmostEqual(radius, math.sqrt(x*x+y*y), places=11)
            self.assertAlmostEqual(radius*math.cos(angle), x, places=11)
            self.assertAlmostEqual(radius*math.sin(angle), y, places=11)

    def test_csv_writer_and_committed_dataset(self):
        generated = generate_random_pairs()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "nested" / "derived_pairs.csv"
            write_pairs_to_csv(generated, output)
            self.assertTrue(output.is_file())
            self.assertEqual(output.read_bytes(), (Path(__file__).resolve().parents[1] / "derived_pairs.csv").read_bytes())
            with output.open(newline="") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 1000)
            self.assertEqual(list(rows[0]), ["iteration", "cartesian_x", "cartesian_y", "polar_radius", "polar_angle"])
            self.assertNotEqual(rows[0]["polar_angle"], rows[1]["polar_angle"])


if __name__ == "__main__":
    unittest.main()
