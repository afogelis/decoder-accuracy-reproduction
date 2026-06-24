"""Exact logical error rates for the optimal and MWPM decoders.

When the number of independent error mechanisms ``M`` is small we can enumerate
all ``2**M`` error patterns, weight each by its probability, and compute the
*exact* logical error rate of any decoder -- no Monte Carlo noise. This is the
key idea of arXiv:2311.12503: the optimal (maximum-likelihood) decoder gives a
hard lower bound on the achievable logical error rate, and any practical decoder
is judged by how close it gets to that bound.

* **Optimal decoder.** For each syndrome it predicts the logical class with the
  highest total probability (summed over all consistent errors). Its logical
  error rate is ``1 - sum_s max_l P(s, l)``.
* **MWPM decoder.** For each syndrome it predicts a fixed logical class; its
  error rate is ``1 - sum_s P(s, prediction(s))``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .codes import CodeCapacityProblem

MAX_ENUMERABLE_MECHANISMS = 22


@dataclass(frozen=True)
class AccuracyResult:
    """Exact logical error rates at one physical error rate."""

    distance: int
    physical_error_rate: float
    optimal_ler: float
    mwpm_ler: float
    num_mechanisms: int

    @property
    def suboptimality(self) -> float:
        """Additive gap: how much worse MWPM is than optimal (>= 0)."""
        return self.mwpm_ler - self.optimal_ler

    @property
    def suboptimality_ratio(self) -> float:
        """Multiplicative gap MWPM / optimal (>= 1)."""
        if self.optimal_ler <= 0.0:
            return float("nan")
        return self.mwpm_ler / self.optimal_ler


def _enumerate_patterns(num_mechanisms: int) -> np.ndarray:
    """Return a ``(2**M, M)`` boolean array of all error patterns."""
    count = 1 << num_mechanisms
    indices = np.arange(count, dtype=np.uint64)
    bits = ((indices[:, None] >> np.arange(num_mechanisms, dtype=np.uint64)) & 1).astype(np.uint8)
    return bits


def _pattern_probabilities(patterns: np.ndarray, priors: np.ndarray) -> np.ndarray:
    """Probability of each enumerated independent-error pattern."""
    per_bit = patterns * priors + (1 - patterns) * (1.0 - priors)
    return np.prod(per_bit, axis=1)


def exact_accuracy(problem: CodeCapacityProblem) -> AccuracyResult:
    """Compute exact optimal and MWPM logical error rates by full enumeration."""
    matrices = problem.matrices
    num_mechanisms = matrices.num_mechanisms
    if num_mechanisms > MAX_ENUMERABLE_MECHANISMS:
        raise ValueError(
            f"{num_mechanisms} mechanisms exceeds the exact-enumeration limit "
            f"({MAX_ENUMERABLE_MECHANISMS}); use a smaller distance"
        )

    check = matrices.check_matrix.astype(np.uint8)  # (D, M)
    observable = matrices.observable_matrix.astype(np.uint8)  # (O, M)
    priors = matrices.priors

    patterns = _enumerate_patterns(num_mechanisms)  # (N, M)
    probabilities = _pattern_probabilities(patterns, priors)  # (N,)
    syndromes = (patterns @ check.T) % 2  # (N, D)
    logicals = (patterns @ observable.T) % 2  # (N, O)

    num_detectors = check.shape[0]
    powers = 1 << np.arange(num_detectors, dtype=np.uint64)
    syndrome_keys = syndromes.astype(np.uint64) @ powers  # (N,) unique int per syndrome
    logical_keys = (
        logicals[:, 0].astype(np.uint8)
        if observable.shape[0]
        else np.zeros(len(patterns), np.uint8)
    )

    optimal_correct = 0.0
    mwpm_correct = 0.0
    for key in np.unique(syndrome_keys):
        mask = syndrome_keys == key
        prob_class0 = probabilities[mask & (logical_keys == 0)].sum()
        prob_class1 = probabilities[mask & (logical_keys == 1)].sum()
        optimal_correct += max(prob_class0, prob_class1)

        # MWPM prediction for this syndrome.
        detector_bits = syndromes[np.argmax(mask)].astype(np.uint8)
        prediction = int(np.asarray(problem.matching.decode(detector_bits)).ravel()[0])
        mwpm_correct += prob_class1 if prediction == 1 else prob_class0

    return AccuracyResult(
        distance=problem.distance,
        physical_error_rate=problem.physical_error_rate,
        optimal_ler=float(1.0 - optimal_correct),
        mwpm_ler=float(1.0 - mwpm_correct),
        num_mechanisms=num_mechanisms,
    )
