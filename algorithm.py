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
5. All derived pairs are written to a CSV file.

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
class DerivedPair:
    """Represent a derived pair of values stored in the CSV output."""

    iteration: int
    pair_type: str
    first_value: float
    second_value: float


def generate_random_pairs(
    *,
    iterations: int = 1000,
    samples_per_iteration: int = 3,
    value_range: Tuple[float, float] = (0.0, 5.0),
    seed: int = 2024,
) -> List[DerivedPair]:
    """Generate derived pairs based on the requested algorithm."""

    rng = random.Random(seed)
    lower, upper = value_range

    derived_pairs: List[DerivedPair] = []

    for iteration in range(1, iterations + 1):
        final_x = 0.0
        final_y = 0.0

        for _ in range(samples_per_iteration):
            x = rng.uniform(lower, upper)
            y = rng.uniform(lower, upper)
            final_x += x
            final_y += y

        derived_pairs.append(
            DerivedPair(iteration, "cartesian", final_x, final_y)
        )

        radius = math.hypot(final_x, final_y)
        angle = math.atan2(final_y, final_y)
        derived_pairs.append(
            DerivedPair(iteration, "polar", radius, angle)
        )

    return derived_pairs


def write_pairs_to_csv(pairs: Iterable[DerivedPair], output_path: Path) -> None:
    """Write the derived pairs to a CSV file."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["iteration", "pair_type", "first_value", "second_value"])

        for pair in pairs:
            writer.writerow([
                pair.iteration,
                pair.pair_type,
                f"{pair.first_value:.10f}",
                f"{pair.second_value:.10f}",
            ])


def main() -> None:
    derived_pairs = generate_random_pairs()
    write_pairs_to_csv(derived_pairs, Path("derived_pairs.csv"))


if __name__ == "__main__":
    main()
