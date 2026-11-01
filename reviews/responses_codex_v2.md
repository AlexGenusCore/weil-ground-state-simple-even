# Responses to the Codex review of release candidate 2.0.0 (review of 2026-11-01, 04:07)

Review: `reviews/review_codex_20261101_0407.md` (OpenAI Codex, read-only, with web search). Its verdict was not to release
the candidate as a completed computer-assisted proof until three major points were fixed. It found no fatal error and no
counterexample to the main theorem. We accept all twelve points. None of them changes a certified number that enters the
proof. Section, remark and table numbers below are those of the revised `paper/main.pdf`; the item headings keep your numbering. The responses were drafted with an AI
assistant (Anthropic's Claude), like the rest of this work. The fixes have not yet been reviewed by Codex or by a human.

## Major

**1. The Piece IV derivations were not public (§7.3, Theorem 7.3).** Accepted.
- The proof document and the specification are now shipped as a versioned supplement, `supplement/`:
  - `PROOFS.md`, items P1–P23 including P14–P22 and Theorem V (§8). It is **byte-identical** to the file whose sha256
    (`7e18f2d0…`) the run-time stamp `data/piece4/GAP.stamp` records. `check_theorem.sh` now verifies this.
  - `SPEC.md`, a redacted copy: one host name and one `user@IP` line replaced. `supplement/REDACTION.sha256` maps the
    original hash (also in `GAP.stamp`) to the shipped one.
  - `MAP.md`, the requested map from each formula to the code (`code/rh60route/certify.py` and the helper files) and to
    the record fields and gates that hold or check its value.
- The paper now states the formulas themselves.
  - §7.2 gives the diagonal entry A_qq (P6), with R_ε and the q = 0 case.
  - §7.3 has a new paragraph, "The explicit constants". It gives the generators and transfer rows (P11), the diagonal
    correction (P12), the moment bounds F0, F1 and L_ab (P14–P15), r̄, V_h, E_h, J_2, J_4 (P16–P17), τ_N and t′_q
    (P18–P19), S_M and the assembly debit ε_asm (P20–P21), and r_M (P22). Each is cited to the supplement, and the
    outline proof of Theorem 7.3 points to the full proof (P3, P19–P23, §8).
- §7.1 (iv), the provenance table and imported-trust item 4 are updated. Both documents remain AI-written and AI-reviewed;
  the paper says so.

**2. Two upper bounds in Table 8 lacked outward rounding (§8, Remark 8.2).** Accepted.
- We confirmed the problem. `str(15, radius=False)` rounds to nearest. On 20 000 random inputs it was below its input
  about half the time, with relative error at most 4.9e−15.
- Of all shipped upper-bound records, only the two original even runs (L = 2 and L = 2.25) lack the relative 1e−13 raise
  that `fr_sweep.py` applies before printing.
- L = 2: Table 8 now uses 1.84681871820109e−283 from `data/piece4/glue/upper_rerun_L2.jsonl`. This is the rerun with the
  shipped code and the corrected exponent; it is also U^ev(2) of Table 6.
- L = 2.25: there is no rerun (it would take about 18 h). We bound the serialisation error explicitly: the true upper end
  is within one unit of the 15th digit. We print the value rounded up to 12 digits, 9.03204367910e−476, a relative 6e−12
  above the record. The record's radius is a relative 1e−1546. The record is now shipped as `data/upper/rig_L225.jsonl`,
  together with `rig_L2.jsonl` and `odd.jsonl`.
- Remark 8.2 is rewritten. Part (a) covers the decimal export and part (b) the quadrature exponent. As you note, neither
  value enters a step of the proof.

**3. The Connes–van Suijlekom hypothesis was omitted (abstract, §1.2, §11).** Accepted. We remove the consequence; we do not
prove the hypothesis.
- The abstract and §1.2 now state Thm 6.1 with its hypothesis: Q, defined on trigonometric polynomials, gives a
  lower-bounded essentially self-adjoint operator. They note that the introduction of the cited paper states the result
  without that hypothesis.
- Both now say that we have not shown that trigonometric polynomials are an operator core for our A_L, nor any form-core
  substitute, and that we therefore claim nothing about the zeros of the Fourier transform of our ground state.
- Limitation 8 and the README say the same. Proving the core property, or a form-core version of Thm 6.1, is left open.

## Minor

**4. Rule E is not needed (Remark 4.2, §§7.4–7.5, §11(2)).** Accepted, with thanks; this is a real simplification.
- We reproduced your check. With `--l2-from 1.92364501953125=1.9326171875` all 53 comparisons pass with minimum ratio
  2.099. The substituted record (rung ¼λ̂_2, N = 39936) belongs to the registered grid, and its bound 1.30191e−236 exceeds
  the odd bound 1.23237e−236. The step [L′, 1.92364501953125] keeps ratio 448.6 and stays odd-limited.
- New Remark 7.5 ("Rule E is not needed") gives the argument. Remark 4.2, Remark 7.1, §7.6 and Limitation 2 no longer say
  that rejecting rule E shortens the range. They say that the registered grid failed as an experiment, and that the open
  step has two proofs.
- `check_theorem.sh` now runs both routes and requires both to pass.
- We keep the full history of the failure. We also note that the substitution was written down after the failure: it is
  the fallback of the rule-E registration, `PREREG_GAP.md` §4. It uses no new computation.
- README, REVIEWING.md, CITATION.cff and `code/rh60route/README.md` are updated to match.

**5. Sign error in the proof of Proposition 5.13(a).** Accepted: (P + μ̄) is now (P − μ̄). We added |P − μ̄| ≤ A + μ̄, the
estimate that (H3) uses.

**6. The initial domain was overstated (§§1.1, 2.3).** Accepted.
- §1.1 now defines Q_L on real f ∈ C_c^∞(−L, L) and says that §2.3 extends it by closure.
- §2.3 has a new paragraph, "Closability". It writes Q_L = q_H + b_L. Here q_H is the restriction of the closed form of
  the lower-bounded Fourier multiplier H(t) ≥ H(0) (Lemma 5.6) to the closed subspace L²(−L, L). The remainder b_L is
  bounded: the pole term by 4 sinh(L)‖f‖² and the prime term by 2Σ Λ(n)n^{−1/2}‖f‖². A closable lower-bounded form plus a
  bounded form is closable with the same domain.
- The form domain is then named explicitly. The existing discreteness argument follows.

**7. The Galerkin weight is singular (§8, Proposition 8.1).** Accepted.
- §8 now writes the archimedean term of eq. (P) as ∫ k_L(r)(g(0) − g(Lr)) dr + d_L g(0). It notes that k_L ~ 1/r, that
  the regularised integrand is analytic, and that d_L's integrand tends to −3L/2. The diagonal correction (d_L + c_L)I is
  stated, and the moments m_j are written out, including ∫ k_L(r)(P_j(−1) − P_j(r − 1)) dr.
- Proposition 8.1 now explains the quadrature bound for that integrand: h_L(r)·(P_j(−1) − P_j(r − 1))/r, bounded on the
  ellipse boundary through the maximum principle by max|h_L|·(1 + ρ^j)/min|r|.
- It also states the Chebyshev rounding bound that the code uses: per-step δ = 2^(8−p) asserted, accumulated error at most
  Σ|c_n| j²(δ/2 + r_x) via |U_m| ≤ m + 1 and Markov's inequality, and a nonnegative Chebyshev-to-Legendre map with row
  sums 1.

**8. rStation paper 83 was missing (§§1.3, 1.4, 8).** Accepted.
- Paper 83 (bramble_trace with span_of_dilates, v1, 2026-10-31 19:33 UTC) is cited in the prior-work list, in
  Contribution 4 and in "Not claimed as new". It is described as unconditional, at the 4πe^{2L} scale, for every fixed
  index in each parity sector, with non-explicit constants and no lower bound or simplicity statement.
- The wording that attributed this scale's rigorous upper bounds only to the conditional paper 81 is gone.
- §8 now says that paper 83 gives no explicit value at L = 2.25.

**9. Siche's repository was missing (§1.3).** Accepted.
- New item in §1.3: Siche, `Architect-Resonance/Riemann-Hypothesis`. Its first commit is 2026-04-03 and its last change
  2026-04-07 (GitHub API); it is unrefereed. It claims simplicity for all windows via Krein–Rutman.
- We state the two steps we could not reconcile: a finite sum of compressed translations is in general not compact, and
  the even pole term has norm 2(L + sinh L) ~ λ, not O(log λ). We do not treat the claim as an established proof, and we
  add that if it is correct, it contains our theorem.
- The abstract, Contribution 1 and the README novelty bullet now say "no certified proof known", with this pointer.

**10. Overclaim about the continuum eigenfunction (§9).** Accepted.
- §9 now says "consistent with" and "appear to tend to 0". It adds that four resolutions establish neither statement, nor
  anything about the limit.
- It defines the effective mesh size h = 2L/N_tot. It gives the fitting procedure: least squares of 1/mean against
  ln(1/h), on means computed from the unrounded jumps, with result c ≈ 0.740, b ≈ 0.586 and residuals < 0.0022.
- It reports that a power law c′h^0.153 fits equally well.
- The raw measurements are now shipped: `data/kinks/kink_119_<N>.json`.

**11. Stale run counts (§10.1).** Accepted. We recomputed from the records: 24 Piece III records, 2006.37 worker-process
hours; the 16-record subset gives 814.00 h. The paper now says 24 and about 2006. We also updated the L = 2 even run time,
which is now the rerun's 4276 s.

**12. Local corrections.** All accepted.
- Lemma 5.10: the claim is now stated for 1 ≤ k ≤ N, with N the head size.
- §5.2: the text notes that Lemma 5.4 needs T♯ ≥ 3/2 and that every cutoff used is at least 200.
- §2.2: the leading term is now (g(0) − g(x))/x.
- §5.2: f_L(y) := f(Ly) is defined before g(Ls) = L∫ f_L(y) f_L(y + s) dy.
- §7.6 (your §7.5): "every other hard gate being true".
- Lemma 5.4 is now labelled "improved form of [Zhu, Lemma 3.1]", with a note that Zhu states the envelope for t ≥ 15/4
  and that the proof here gives t ≥ 3/2.

## Also changed

- §1.2 and Limitation 7 record your term-by-term match of eq. (weil) against CCM (3.7)–(3.11) under u = e^x, as an AI check.
- The audit section (§10.3) and the AI-assistance statement now describe this review: what it checked, what it did not,
  and that it does not certify the proof.

## Points we did not act on

- *What the review could not check.* This covers the window matrices, stage S, the C factorisations, the multi-hour
  certificates, the historical code revisions, and the Zenodo and rStation priority timestamps. These remain imported
  trust, listed in §7.9 and §11. We did not rerun them for this release.
- *The review session log.* The log (`review_codex_20261101_0407.md.log`, 614 KB) is not shipped. It contains many
  listings of the author's private working tree. Its sha256 is in `reviews/REDACTION.sha256`, and it is available on
  request.

## Status after these changes

- `check_theorem.sh` passes. This covers file hashes including the supplement, Pieces I–II, Piece III, Piece IV with
  rule E and Piece IV without rule E.
- The paper compiles.
- The result is still unrefereed, AI-assisted and audited only by AI systems. It concerns simple-even on (0, 2] only, and
  says nothing about RH.
