# Testing the Accuracy of Surface Code Decoders (reproduction)

A reproduction of the methodology of *Testing the Accuracy of Surface Code Decoders*
(arXiv:2311.12503): comparing a practical decoder (minimum-weight perfect matching) against the
**optimal** maximum-likelihood decoder, which sets a hard lower bound on the achievable logical
error rate.

## Approach

We work in the code-capacity model (one round of correction, data-qubit noise, perfect stabilizer
measurements) on small surface codes, where the number of independent error mechanisms
([7, 21]) is small enough to **enumerate every error pattern**. This yields the *exact*
logical error rate of each decoder -- no Monte Carlo sampling error:

- The **optimal decoder** predicts, for every syndrome, the logical class with the highest total
  probability. Its error rate `1 - sum_s max_l P(s, l)` is a lower bound for any decoder.
- **MWPM** predicts a fixed class per syndrome; we evaluate its exact error rate the same way.

## Results

| distance | p | optimal LER | MWPM LER | MWPM / optimal |
|----------|---|-------------|----------|----------------|
| 3 | 0.020 | 3.0372e-03 | 3.0372e-03 | 1.000 |
| 3 | 0.040 | 1.1523e-02 | 1.1523e-02 | 1.000 |
| 3 | 0.060 | 2.4572e-02 | 2.4572e-02 | 1.000 |
| 3 | 0.080 | 4.1376e-02 | 4.1376e-02 | 1.000 |
| 3 | 0.100 | 6.1194e-02 | 6.1194e-02 | 1.000 |
| 3 | 0.120 | 8.3356e-02 | 8.3356e-02 | 1.000 |
| 3 | 0.150 | 1.1969e-01 | 1.1969e-01 | 1.000 |
| 5 | 0.020 | 6.2719e-04 | 6.2719e-04 | 1.000 |
| 5 | 0.040 | 4.5206e-03 | 4.5206e-03 | 1.000 |
| 5 | 0.060 | 1.3675e-02 | 1.3676e-02 | 1.000 |
| 5 | 0.080 | 2.8919e-02 | 2.8926e-02 | 1.000 |
| 5 | 0.100 | 5.0179e-02 | 5.0209e-02 | 1.001 |
| 5 | 0.120 | 7.6734e-02 | 7.6842e-02 | 1.001 |
| 5 | 0.150 | 1.2390e-01 | 1.2442e-01 | 1.004 |

The MWPM logical error rate is always at or above the optimal bound (ratio >= 1), as it must be.
The largest sub-optimality observed here is a factor of **1.004**. MWPM is near-optimal at
low physical error rates and degrades, relative to optimal, as the error rate rises and degenerate
error configurations -- which matching cannot weigh against each other -- become more important.
This reproduces the central message of the paper: matching is an excellent but not optimal decoder,
and the gap is quantifiable.

## Figures

- `figures/ler_vs_p.png` -- optimal vs MWPM logical error rate.
- `figures/suboptimality.png` -- MWPM / optimal ratio vs physical error rate.

## Limitations

- Exact enumeration restricts the analysis to small distances (code-capacity, single round). The
  paper uses tensor-network maximum-likelihood decoding to reach larger instances; the conclusion
  -- a small, growing matching sub-optimality -- is the same.
- The code-capacity model omits measurement errors and multi-round dynamics.

## References

Higgott O, et al. Testing the Accuracy of Surface Code Decoders. arXiv:2311.12503, 2023.

Dennis E, Kitaev A, Landahl A, Preskill J. Topological quantum memory. Journal of Mathematical
Physics 2002; 43:4452-4505.
