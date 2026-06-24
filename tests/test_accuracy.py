import numpy as np

from darepro.codes import build_problem
from darepro.optimal import exact_accuracy


def test_mwpm_is_never_better_than_optimal():
    for p in (0.02, 0.05, 0.10):
        result = exact_accuracy(build_problem(distance=3, physical_error_rate=p))
        # Optimal is a lower bound; allow tiny FP slack.
        assert result.mwpm_ler >= result.optimal_ler - 1e-12
        assert result.suboptimality_ratio >= 1.0 - 1e-9


def test_logical_error_rates_in_unit_interval():
    result = exact_accuracy(build_problem(distance=3, physical_error_rate=0.08))
    assert 0.0 <= result.optimal_ler <= 1.0
    assert 0.0 <= result.mwpm_ler <= 1.0


def test_error_rate_increases_with_physical_rate():
    low = exact_accuracy(build_problem(distance=3, physical_error_rate=0.02)).optimal_ler
    high = exact_accuracy(build_problem(distance=3, physical_error_rate=0.12)).optimal_ler
    assert high > low


def test_distance_three_is_enumerable():
    problem = build_problem(distance=3, physical_error_rate=0.05)
    assert problem.num_mechanisms <= 22
