"""Figures for the decoder-accuracy reproduction."""

from __future__ import annotations

from collections.abc import Sequence

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from .optimal import AccuracyResult


def _by_distance(results: Sequence[AccuracyResult]) -> dict[int, list[AccuracyResult]]:
    grouped: dict[int, list[AccuracyResult]] = {}
    for result in results:
        grouped.setdefault(result.distance, []).append(result)
    for series in grouped.values():
        series.sort(key=lambda r: r.physical_error_rate)
    return grouped


def plot_ler_vs_p(results: Sequence[AccuracyResult], *, ax: Axes | None = None) -> Axes:
    """Optimal vs MWPM logical error rate against physical error rate, per distance."""
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 5))
    for distance, series in sorted(_by_distance(results).items()):
        ps = [r.physical_error_rate for r in series]
        ax.plot(ps, [r.optimal_ler for r in series], marker="o", label=f"optimal (d={distance})")
        ax.plot(
            ps,
            [r.mwpm_ler for r in series],
            marker="s",
            linestyle="--",
            label=f"MWPM (d={distance})",
        )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Physical error rate p")
    ax.set_ylabel("Logical error rate (exact)")
    ax.set_title("Optimal vs MWPM decoder accuracy")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    return ax


def plot_suboptimality(results: Sequence[AccuracyResult], *, ax: Axes | None = None) -> Axes:
    """MWPM / optimal logical-error-rate ratio against physical error rate."""
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 5))
    for distance, series in sorted(_by_distance(results).items()):
        ps = [r.physical_error_rate for r in series]
        ratios = [r.suboptimality_ratio for r in series]
        ax.plot(ps, ratios, marker="o", label=f"d = {distance}")
    ax.axhline(1.0, color="gray", linestyle=":", label="optimal")
    ax.set_xscale("log")
    ax.set_xlabel("Physical error rate p")
    ax.set_ylabel("MWPM / optimal logical error rate")
    ax.set_title("MWPM sub-optimality vs physical error rate")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    return ax
