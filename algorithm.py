"""Generate aggregate random coordinate pairs and save to CSV.

1. Use a deterministic random seed (default: 2024).
2. For each of 1,000 iterations, draw three random (x, y) pairs with
   coordinates in the interval [0, 5].
3. Sum the components separately to obtain ``final_x`` and ``final_y``.
4. Convert the aggregate point to polar coordinates using
   ``hypot(final_x, final_y)`` and ``atan2(final_y, final_x)``.
5. Write Cartesian and polar coordinates on the same CSV line.

The polar angle is in radians, measured counterclockwise from the positive
x-axis, in the range [-pi, pi]. At the origin, the angle is conventionally
stored as 0.0 (its mathematical value is undefined).
"""

import csv
import math
import random
from pathlib import Path
from typing import Iterable, List, Tuple

# (iteration, final_x, final_y, radius, angle)
DerivedPair = Tuple[int, float, float, float, float]


def cartesian_to_polar(x: float, y: float) -> Tuple[float, float]:
    """Return (radius, angle in radians) for Cartesian coordinates (x, y)."""
    return math.hypot(x, y), math.atan2(y, x)


def generate_random_pairs(
    *,
    iterations: int = 1000,
    samples_per_iteration: int = 3,
    value_range: Tuple[float, float] = (0.0, 5.0),
    seed: int = 2024,
) -> List[DerivedPair]:
    """Generate reproducible aggregate Cartesian and polar coordinate pairs."""

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

        radius, angle = cartesian_to_polar(final_x, final_y)

        derived_pairs.append((iteration, final_x, final_y, radius, angle))

    return derived_pairs


def write_pairs_to_csv(pairs: Iterable[DerivedPair], output_path: Path) -> None:
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
                    pair[0],
                    f"{pair[1]:.10f}",
                    f"{pair[2]:.10f}",
                    f"{pair[3]:.10f}",
                    f"{pair[4]:.10f}",
                ]
            )


def main() -> None:
    derived_pairs = generate_random_pairs()
    write_pairs_to_csv(derived_pairs, Path("derived_pairs.csv"))


if __name__ == "__main__":
    main()
