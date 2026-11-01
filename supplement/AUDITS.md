# Protocol and review history (release 2.0.0)

This file holds the protocol and audit history that the paper (`paper/main.tex`) used to state in full. The second Codex
review (`reviews/codex_review_v2_round2.md`, point 9) asked for it to move out of the paper so that the proof dependencies are
easier to see. Nothing here is a premise of the theorem; the "Dependency summary" after the main theorem lists the premises.
Labels in backticks are the LaTeX labels of `paper/main.tex`. All reviews
below were carried out by AI agents directed by the author. No independent human referee has checked the proofs or the code.

## 1. Clean-room protocol of Piece IV (paper, `sec:piece4credit`)

The method of Piece IV is that of bramble_trace (rStation paper 60) and lihongmin (rStation paper 45); see the paper, `sec:piece4credit`.

1. A specification and a proof document were written from the manuscript text of rStation papers 45 and 60 only. No
   supplement code of either paper was opened. The code licence of paper 60 allows execution and inspection for
   verification only, and paper 45 reserves all rights.
2. The implementer worked from these two documents and our own code only, and opened no rStation file.
3. No rStation code was copied, adapted or vendored. An independent audit searched our code for the manuscripts' code
   identifiers and characteristic constants and found none.
4. Every step was re-derived from first principles in the proof document, including steps that paper 60 spot-checks only.

The proof document and the specification are shipped in this folder (`PROOFS.md`, byte-identical to the stamped file;
`SPEC.md`, a redacted copy). They contain no rStation code. The shipped code of Piece IV is ours, apart from Elston's
MIT-licensed integer Cholesky and weighted Schur-test routines, which Piece III already uses.

The pre-registration of the Piece IV grid (stamps, amendment log, scored results, the registered failure and rule E) is in
`data/piece4/` (`PREREG_GRID.md`, `GRID.stamp`, `AMENDMENTS.log`, `RESULTS_GRID.md`, `PREREG_GAP.md`, `GAP.stamp`,
`RESULTS_GAP.md`, `AUDIT_GRID.md`). The paper keeps the disclosure of the failure (`sec:piece4fail`, Remark `rem:noE`).

## 2. Review and audit history

- **Pieces I–II.** Three independent AI review rounds of the earlier note produced, among others:
  - the Gauss–Legendre exponent correction (paper, Remark `rem:erratum`);
  - reconciliation of the Piece I constants across precisions;
  - outward rounding of all quoted bounds;
  - a downward-induction proof of the Bessel ratio enclosure;
  - the definition of the continuation of Re ψ off the real axis;
  - documentation of Python `min` on balls;
  - a mollification argument for the position-side formula;
  - a self-contained discreteness proof;
  - a SHA-256 check of remote code;
  - corrected credit to Zhu for the reduction.

  Every finding was checked against code, logs and data before it was applied. A clean end-to-end rerun with a single code
  revision (empty cache, tools rebuilt, remote code hashed) then reproduced all lower bounds for L ≤ 1 to about three
  significant digits. The sharp-cutoff path and the windows 1.03–1.19 have not been through a review round.
- **Upper-bound code.** An external review of the high-precision notes (six findings, all accepted) led to per-code-path
  rigour labels, outward rounding of exported upper endpoints, and withdrawal of an unsupported tail claim. An earlier
  review found and fixed an inaccurate ball inverse, a missing residual check and a missing quadrature bound.
- **Piece III.** Elston's certifier was audited independently at L = 1.19 (two issues fixed; documented in Elston's
  repository). The post-audit code at larger L and our `--deflate` addition have not been audited. The step test
  (`code/gap/check_steps.py`, about 50 lines) compares explicit Arb endpoints. The reproduction of Elston's L = 1.19 bounds
  to 12 and 17 digits is a consistency check of the installation, not an audit.
- **Piece IV.**
  - The specification and the proof document were reviewed by a fresh AI agent before the pilot was pre-registered.
  - A pilot at L = 2 was audited by another fresh AI agent with its own code: matrix entries from the position-side
    formula, far-block constants, an independent core solve, mutation tests, rounding directions and the clean room. It
    found no rigour defect and required six fixes: independent per-window entries, an uncapped second path, explicit
    labels for Lemma SR, archiving of executed code, an append-only amendment log, and checks at gluing. They were made and
    verified before the grid was pre-registered.
  - The grid was then checked by a fresh AI agent with its own code: step test, gates, controls, mutations, provenance,
    entries from the position-side formula, and the cross-check.
  - The gap closure and the combined statement on (0, 2] were checked by another fresh AI agent. Its verdict was
    "certified, conditional on the imported trust of `sec:piece4trust`; grid G alone gives [1.4035, 1.91912841796875]".

  None of these agents wrote the code it checked, but all are instances of the same AI system that wrote it.
- **Second AI system, round 1.** OpenAI's Codex reviewed the first release candidate of 2.0.0 on 1 November 2026,
  read-only and with web search (`reviews/review_codex_20261101_0407.md`, responses in `reviews/responses_codex_v2.md`).
  - It re-derived the parity, monotonicity, deflation and Schur-complement arguments, recomputed the Piece I constants, ran
    the gluing script and rebuilt `paper/generated.tex`.
  - It compared 40 Legendre–Galerkin and 18 trigonometric matrix entries with independent high-precision code (agreement
    to 6.5e−62 and 1.4e−55).
  - It found no fatal error and no counterexample to the theorem. It recommended against release as a completed
    computer-assisted proof until three major points were fixed: the Piece IV derivations were not public; two printed
    upper bounds lacked a demonstrated outward rounding; and the hypothesis of Connes–van Suijlekom, Thm. 6.1, was
    misstated.
  - It also raised nine minor points, among them that rule E is not needed. Earlier drafts had said that without rule E
    the theorem covers only (0, 1.91912841796875]; that was too strong (paper, Remark `rem:noE`).
- **Second AI system, round 2.** Codex reviewed the revised candidate on 1 November 2026 (`reviews/codex_review_v2_round2.md`,
  responses in `reviews/responses_codex_v2_round2.md`).
  - It advised public release as a preprint after minor corrections. It called this "a positive preprint recommendation,
    **not an independent certification of every large computation**".
  - It raised nine minor points: an ambiguous eigenvalue label, the dyadic anchors of Pieces I–II, notation in §7.2–7.3,
    Fourier phases, the Kramarenko-Byrd title and form-core claim, record validation in the checker, wording on rank-one
    interlacing, two rounding errors in the kink table, and presentation. This version addresses all nine.
  - It reproduced the Piece I constants and 24 trigonometric and 40 Legendre entries (to 2.1e−55 and 1.6e−56), and it
    found that all 106 Piece IV lower-bound balls enclose their exact μ.

Neither Codex round regenerated the window matrices, stage S, the C factorisations or the multi-hour certificates, and
neither certified the proof.
