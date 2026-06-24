"""Sweep exact decoder accuracy across physical error rates and distances."""

from __future__ import annotations

from collections.abc import Sequence

from .codes import build_problem
from .optimal import MAX_ENUMERABLE_MECHANISMS, AccuracyResult, exact_accuracy


def sweep_accuracy(
    *,
    distances: Sequence[int] = (3,),
    error_rates: Sequence[float] = (0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.15),
    basis: str = "Z",
    rotated: bool = True,
) -> list[AccuracyResult]:
    """Compute exact optimal vs MWPM logical error rates over a grid.

    Distances whose code-capacity model exceeds the exact-enumeration limit are
    skipped with a note, keeping the reproduction fully exact rather than mixing
    in Monte Carlo estimates.
    """
    results: list[AccuracyResult] = []
    for distance in distances:
        probe = build_problem(distance=distance, physical_error_rate=error_rates[0],
                              basis=basis, rotated=rotated)
        if probe.num_mechanisms > MAX_ENUMERABLE_MECHANISMS:
            print(f"skipping d={distance}: {probe.num_mechanisms} mechanisms exceed exact limit")
            continue
        for p in error_rates:
            problem = build_problem(distance=distance, physical_error_rate=p,
                                   basis=basis, rotated=rotated)
            results.append(exact_accuracy(problem))
    return results
