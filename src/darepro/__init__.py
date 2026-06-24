"""Reproduction of arXiv:2311.12503 -- exact MWPM vs optimal decoder accuracy."""

from .accuracy import sweep_accuracy
from .codes import CodeCapacityProblem, build_problem
from .optimal import AccuracyResult, exact_accuracy

__version__ = "0.1.0"

__all__ = [
    "AccuracyResult",
    "CodeCapacityProblem",
    "build_problem",
    "exact_accuracy",
    "sweep_accuracy",
]
