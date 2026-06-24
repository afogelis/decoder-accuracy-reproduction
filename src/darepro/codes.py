"""Build small code-capacity surface-code decoding problems.

To compare a practical decoder against the *optimal* (maximum-likelihood)
decoder we need a setting small enough to solve exactly. We use the
code-capacity model: a single round of error correction with data-qubit noise
and perfect stabilizer measurements. For a distance-``d`` surface code this has
few enough independent error mechanisms (for small ``d``) that every error
pattern can be enumerated.

We reuse the companion repositories: Stim generates the code-capacity detector
error model, ``decbench.dem_to_matrices`` turns it into parity-check / logical
matrices, and PyMatching provides the MWPM decoder under test.
"""

from __future__ import annotations

from dataclasses import dataclass

import pymatching
import stim
from decbench.dem_matrices import DemMatrices, dem_to_matrices


@dataclass(frozen=True)
class CodeCapacityProblem:
    """A small code-capacity decoding problem ready for exact analysis."""

    distance: int
    physical_error_rate: float
    matrices: DemMatrices
    matching: pymatching.Matching

    @property
    def num_mechanisms(self) -> int:
        return self.matrices.num_mechanisms

    @property
    def num_detectors(self) -> int:
        return self.matrices.num_detectors


def build_problem(
    *, distance: int, physical_error_rate: float, basis: str = "Z", rotated: bool = True
) -> CodeCapacityProblem:
    """Construct a code-capacity surface-code problem at the given error rate."""
    task = f"surface_code:{'rotated' if rotated else 'unrotated'}_memory_{basis.lower()}"
    circuit = stim.Circuit.generated(
        task,
        distance=distance,
        rounds=1,
        before_round_data_depolarization=physical_error_rate,
    )
    matrices = dem_to_matrices(circuit.detector_error_model(decompose_errors=False))
    matching = pymatching.Matching.from_detector_error_model(
        circuit.detector_error_model(decompose_errors=True)
    )
    return CodeCapacityProblem(
        distance=distance,
        physical_error_rate=physical_error_rate,
        matrices=matrices,
        matching=matching,
    )
