"""Generate aggregate random coordinate pairs and save to CSV.

The script follows the specification provided by the user:
1. A deterministic random seed is used (default: 2024).
2. For each of 1,000 iterations, three random (x, y) pairs are drawn with
   coordinates in the half-open interval [0, 5).
3. The x- and y-components of the three pairs are summed separately to produce
   ``final_x`` and ``final_y``.
4. Two additional pairs are derived per iteration: the Cartesian pair
   ``(final_x, final_y)`` and the polar pair
   ``(sqrt(final_x**2 + final_y**2), atan2(final_y, final_y))``.
5. Both derived pairs for each iteration are written on the same CSV line.

The request described ``sqrt(final_x^2, final_y^2)`` and ``atan2(final_y, final_y)``;
the implementation follows these expressions literally, interpreting the square
root as operating on the sum of the squared values.
"""

from __future__ import annotations

import csv
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple


@dataclass
class IterationPairs:
    """Represent the derived Cartesian and polar pairs per iteration."""

    iteration: int
    final_x: float
    final_y: float
    radius: float
    angle: float


def generate_random_pairs(
    *,
    iterations: int = 1000,
    samples_per_iteration: int = 3,
    value_range: Tuple[float, float] = (0.0, 5.0),
    seed: int = 2024,
) -> List[IterationPairs]:
    """Generate derived pairs based on the requested algorithm."""

    rng = random.Random(seed)
    lower, upper = value_range

    derived_pairs: List[IterationPairs] = []

    for iteration in range(1, iterations + 1):
        final_x = 0.0
        final_y = 0.0

        for _ in range(samples_per_iteration):
            x = rng.uniform(lower, upper)
            y = rng.uniform(lower, upper)
            final_x += x
            final_y += y

        radius = math.hypot(final_x, final_y)
        angle = math.atan2(final_y, final_y)

        derived_pairs.append(
            IterationPairs(iteration, final_x, final_y, radius, angle)
        )

    return derived_pairs


def write_pairs_to_csv(pairs: Iterable[IterationPairs], output_path: Path) -> None:
    """Write the derived pairs to a CSV file."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            [
                "iteration",
                "cartesian_x",
                "cartesian_y",
                "polar_radius",
                "polar_angle",
            ]
        )

        for pair in pairs:
            writer.writerow(
                [
                    pair.iteration,
                    f"{pair.final_x:.10f}",
                    f"{pair.final_y:.10f}",
                    f"{pair.radius:.10f}",
                    f"{pair.angle:.10f}",
                ]
            )


def main() -> None:
    derived_pairs = generate_random_pairs()
    write_pairs_to_csv(derived_pairs, Path("derived_pairs.csv"))


if __name__ == "__main__":
    main()
