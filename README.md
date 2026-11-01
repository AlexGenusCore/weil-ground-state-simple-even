# Simple, even ground state of the localized Weil form for L in (0, 2]

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23832220.svg)](https://doi.org/10.5281/zenodo.23832220)

This is a computer-assisted proof of the following statement. It uses Arb/FLINT ball arithmetic and exact integer
arithmetic. For every window half-width `L` in `(0, 2]`, the lowest eigenvalue of Weil's quadratic form for the Riemann zeta
function on `L^2(-L, L)` is simple, and its eigenfunction is even.

**Please read this first.**

- **Unrefereed.** Nobody outside the project has checked the proofs or the code.
- **AI-assisted, and audited only by AI.** It was produced **largely by an AI assistant** (Anthropic's Claude, used through
  Claude Code). The author directed the work but is not a professional mathematician. Every review and audit so far was run
  by AI agents, including the fresh-agent audit of the new Piece IV (`data/piece4/AUDIT_GRID.md`). No human expert has
  checked any part. See [AI assistance](#ai-assistance).
- **The pre-registered grid of Piece IV, `[1.4035, 2]`, failed as registered.** At `L = 1.92364501953125` the second even
  eigenvalue could not be certified at the planned truncation `N`, because of a boundary effect of the cut. As registered,
  grid G certifies `[1.4035, 1.91912841796875]`. The one open step is closed in two ways:
  - by **rule E** (`N -> N + 1024`), which was written after the failure but stamped before its scored run (its negative
    control failed as required, but at V2 rather than V4, so it does not exercise Lemma SR at the new `N`);
  - **without rule E**, by min-max monotonicity (`lem:mono`) from the registered grid record at the next window
    `1.9326171875`: `lambda_2^even(1.92364501953125) >= lambda_2^even(1.9326171875) >= 1.3019e-236`, above the odd bound
    `1.2323e-236` there. This uses no computation made after the failure. `check_theorem.sh` runs both routes.

  Earlier drafts said the theorem shrinks to `(0, 1.91912841796875]` without rule E. That was too strong; the second AI
  review (Codex) pointed it out. See [Disclosures](#disclosures-for-release-200).
- It is computer-assisted. Its correctness depends on:
  - the code in `code/`: our certifiers, Zac Elston's certifier in `code/gap/elston/`, and our clean-room
    rh_60-route certifier in `code/rh60route/`;
  - Arb/FLINT and GMP;
  - the lemmas in the paper;
  - the imported trust listed under [Weakest links](#weakest-links).
- It is **not** a result about the Riemann hypothesis and brings no proof of RH closer in any quantified sense.
  - In the Connes–van Suijlekom / Connes–Consani–Moscovici programme, "the lowest eigenvalue of `Q_L` is simple with an even
    eigenfunction" is one hypothesis. Connes–van Suijlekom (Thm 6.1) show that it implies real zeros for the Fourier
    transform of that ground state **if** the form also defines an essentially self-adjoint operator on trigonometric
    polynomials. Our operator is the closure of `Q_L` on `C_c^inf(-L, L)`, and we have **not** verified that hypothesis, so
    we claim nothing about those zeros.
  - Reaching RH would also need that hypothesis for every `L`, and control of the limit `L -> inf` (that those zeros converge
    to the zeta zeros). Neither is addressed here.
  - We verify the hypothesis only on the bounded range `(0, 2]`.

**Check it in seconds:** `./check_theorem.sh`. It validates the shipped records (hashes, schema, all 15 Piece IV gates,
provenance) and runs the gluing checks, then prints the combined statement; see [Reproducing](#reproducing). This is record
validation: it shows that the recorded bounds prove the theorem, not that they are correct. Regenerating a certificate means
re-running its window (hours).

The paper is [`paper/main.pdf`](paper/main.pdf), with source in `paper/main.tex` and `paper/refs.bib`. Piece IV is
documented in four more places:
- its specification, its proofs P1–P23 and a formula → code → record-field map in [`supplement/`](supplement/MAP.md);
- its pre-registrations, scored results and audit in `data/piece4/`;
- its code in `code/rh60route/`, with a README;
- [`data/README.md`](data/README.md).

The note of the `(0, 1.19]` release is kept as [`paper/NOTE.md`](paper/NOTE.md).

## Progress

Public releases across the author's three related repositories, as of 1 November 2026. All are **unrefereed** and
**AI-assisted** (Anthropic's Claude, used through Claude Code, directed by the author). Every review so far was run by AI
systems: internal Claude-based referees, and for the later items a second AI system, OpenAI's Codex. **No human expert has
checked any of them.** Independent review is welcome: info@genuscore.com.

| Date | Release | Result | Review status |
|---|---|---|---|
| 2026-10-25 | [weil-ground-state-simple-even](https://github.com/AlexGenusCore/weil-ground-state-simple-even), first release (commit `26fd9e6`; no tag, no DOI) | Certified simple, even ground state of the localized Weil form for `L` in `(0, 1.09]` | Internal AI review rounds only; the windows 1.03–1.09 had no review round |
| 2026-10-26 | weil-ground-state-simple-even, version of 2026-10-26 (commit `8adfbe5`; no tag, no DOI) | Range extended to `(0, 1.19]` | Internal AI review only; the windows 1.03–1.19 had no review round |
| 2026-10-31 | weil-ground-state-simple-even v1.1.0, archived as v1.1.1 (credits corrected): [10.5281/zenodo.23832221](https://doi.org/10.5281/zenodo.23832221) | Range extended to `(0, 1.4035]` (Piece III, with Elston's certifier) | Internal AI review only; Piece III not audited beyond `L = 1.19` |
| 2026-10-31 | [weil-edge-laws](https://github.com/AlexGenusCore/weil-edge-laws) v0.1.2, research notes: [10.5281/zenodo.23832560](https://doi.org/10.5281/zenodo.23832560) | Edge law, Hadamard formula, kink (echo) and tail laws | Internal AI referee rounds only |
| 2026-10-31 | [log-laplacian-interval-trace](https://github.com/AlexGenusCore/log-laplacian-interval-trace) v1.0.0, paper: [10.5281/zenodo.23832744](https://doi.org/10.5281/zenodo.23832744) | Boundary trace identity and simple Dirichlet spectrum for the logarithmic Laplacian on an interval | Internal AI referees; two reviews by GPT-6.1 Sol (the second through Codex): release as a preprint after minor corrections, which were made |
| 2026-10-31 | weil-edge-laws v0.2.0, paper: [10.5281/zenodo.23834265](https://doi.org/10.5281/zenodo.23834265) | The notes consolidated into a paper with complete proofs, pending external review | Internal AI referees; Codex (GPT-6.1 Sol): release as a preprint after minor fixes, which were made; the changes were not reviewed again |
| 2026-11-01 | weil-ground-state-simple-even v2.0.0: [10.5281/zenodo.23852617](https://doi.org/10.5281/zenodo.23852617) | Range extended to `(0, 2]` (Piece IV) | Fresh-agent AI audits of Piece IV; two Codex (GPT-6.1 Sol) rounds, the first "not yet" (three major points), the second "release as a preprint after minor corrections"; all points addressed; the round-two fixes were not reviewed again. Neither round re-ran the large certificates |

Several of these results, or parts of them, were obtained earlier by others; each repository's README and paper give
the credits (among them Zhu, Kramarenko-Byrd, Elston, the rStation authors bramble_trace and lihongmin, and the mathia
notes). None of the results is a result about the Riemann hypothesis. Work on extending the range and on computer-light
proofs continues; nothing beyond the releases above is claimed.

## What is new in 2.0.0

- **The range grows from `(0, 1.4035]` to `(0, 2]`.** The new part is **Piece IV**, `[1.4035, 2]`.
- **Piece IV covers 54 windows (53 steps) from `1.4035` to `2`.** They include the refinement window
  `31443/2^14 = 1.91912841796875`. We certify:
  - at each of the 53 windows past `1.4035`, lower bounds on the odd-sector bottom `lambda_1^odd` and on the second even eigenvalue `lambda_2^even`, from our
    clean-room implementation of the rh_60-route certifier (`code/rh60route/certify.py`);
  - at every window, a rigorous upper bound `U(L)` on `lambda_0` (`code/upper/fr_sweep.py`).
- **All 53 steps pass.** The smallest step ratio is `2.0986`, at `[1.5, 1.5174560546875]`. Every step is limited by the odd
  sector. The step that closes the gap, `[1.91912841796875, 1.92364501953125]`, has ratio `448.6`.
- **At `L = 2` itself:** `lambda_1^odd >= 2.158e-278` and `lambda_2^even >= 1.365e-273`, against `U^ev(2) <= 1.847e-283`.
- **The method is credited to two AI-agent preprints on rStation:** bramble_trace, riemann_hypothesis paper 60 v1
  (2026-10-26), and lihongmin, paper 45 v1 (2026-10-23). Both are unrefereed and were reviewed only by AI agents. Piece IV
  does not use their claims. Our clean-room code re-verifies the odd-sector part of their positivity claims at every grid
  window. In the even sector the grid certifies `lambda_2^even`, which is what simple-even needs, not `lambda_0^even`.
- **Our additions:**
  - the formulas for general `L`;
  - the μ-shift;
  - the rank-one deflation, which raises the core displacement rank from 2 to 4;
  - Lemma SR, an exact-integer structured LDL^T with an explicit residual;
  - the form-core argument;
  - the independent gates G0i and C-ind;
  - rule E;
  - the gluing.
- **Second AI review.** A release candidate was reviewed by a second AI system, OpenAI's Codex (1 November 2026). It found
  no fatal error and raised 3 major and 9 minor points; all are addressed in this version. The review and our point-by-point
  responses are in [`reviews/`](reviews/). Codex did not re-run the large certificates and does not certify the proof.
- **Pre-registration.** Grid G was run under `PREREG_GRID.md` and the gap under `PREREG_GAP.md`. Both have run-time stamps
  (hashes of every registered document and executed file) and an append-only amendment log with a hash chain. All are in
  `data/piece4/`.
- **Piece III data.** The Elston-route certificates at `1.4255` (λ_2), `1.468` and `1.4885` (both sectors) are added. That
  route now passes on `[1.19, 1.4885]`, in 12 steps with minimum ratio `1.129`. The theorem needs it only up to `1.4035`.
- **New files:**
  - `check_theorem.sh`;
  - `code/rh60route/`;
  - `data/piece4/` (106 glued records, the upper bounds, rule-E records, controls, mutation summary, glue logs,
    pre-registrations, stamps, amendment log, results, audit, SHA-256 sums, and the redaction map);
  - 5 new files in `data/piece3/`;
  - `supplement/` (Piece IV specification, proofs P1–P23, formula–code–field map);
  - `data/upper/` (the original records behind the paper's table of upper bounds at `L = 1.5 ... 2.25`) and `data/kinks/`
    (the raw jump measurements of paper §9);
  - `reviews/` (the Codex review and our responses).

## Disclosures for release 2.0.0

1. **Grid G failed as registered** (kill criterion K3g). The registered outcome is the partial range
   `[1.4035, 1.91912841796875]`, 43 steps (`data/piece4/logs/GLUE_P.log`).
   - The three registered λ_2 rungs at `1.92364501953125` all FAIL at V4, that is, in Lemma SR at its last label, with every
     hard gate true. One refinement level was allowed, and it did not help.
   - A ratio was never the problem.
2. **Rule E is post hoc.** We wrote it after the failure, and after a diagnostic run (D2) had shown that `N + 1024` passes.
   We stamped it (`GAP.stamp`, 01:12:01Z) before the scored run (01:13:06Z). The scored run reproduced D2 bit for bit, so the
   outcome was known when the rule was registered.
   - Rule E changes one argument, `--tmin`, and that argument only selects `N`. No tolerance, gate or certified formula
     changes. Theorem V does not constrain `N`, and every gate is recomputed at the new `N`.
   - For a deductive certificate, choosing `N` after the fact carries no false-positive risk, unless the code has an
     `N`-dependent bug (`AUDIT_GRID.md` §3).
   - Rule E is applied at one window only.
3. **The negative control was weaker than planned.** The rule-E control (`μ = 1.01·λ̂_2(M_0)`) FAILED, as it must. It failed
   at V2, the float core proposal, rather than at V4 (prediction RG-2 missed), so it does not exercise Lemma SR at the new `N`.
   The evidence that V4 is live comes from elsewhere: the 6/6 grid G controls that fail at V4, the four grid FAIL records at
   the last label, and diagnostic D1.
4. **The registered fallback also closes the gap.** That fallback is a `lem:mono` substitution (`check_steps.py --l2-from
   1.92364501953125=1.9326171875`). Its trigger (rule E failing) did not hold, so it was not scored. It reads only a
   registered grid record and passes all 53 steps (paper Remark `rem:noE`), so rule E is not needed for the theorem.
5. **The window `1.8958740234375` passed only narrowly.** It passed on its last rung (`2^-10`), at the last SR label of a
   different `N`, which is the same edge effect. Future grids should register an `N` rule up front.
6. **The shipped records are redacted.** Host names, a user name and home paths are replaced. No number or field was
   changed otherwise. Hashes recorded during the runs (stamps, pins, amendment chain) refer to the originals.
   `data/piece4/REDACTION.sha256` maps original to redacted sha256, and the originals are available on request.
7. **What the audit covered.** The fresh-agent audit recomputed the step chain independently, but with the same Arb library.
   It did not re-prove the certifier.
   - The specification and proofs that the code cites are shipped in `supplement/` since the Codex review: `PROOFS.md`
     (P1–P23, Theorem V, Lemma SR) is byte-identical to the file hashed in `GAP.stamp`; `SPEC.md` is a copy with one host
     name redacted. Both were written with AI assistance and reviewed only by AI agents.
8. **The method comes from AI-agent preprints** reviewed only by AI agents (see above). Our code is clean room: no rStation
   code was opened, copied or adapted.

## What was new in 1.1.0

- The certified range grew from `(0, 1.19]` to `(0, 1.4035]` (**Piece III**).
- Lower bounds come from Elston's window-compressed prime-norm certifier (`weil-windows`, MIT, upstream commit
  `3cc4cb7b`). It is run unchanged except for one added option, `--deflate`. That option adds `v v^T`, where `v` is an
  approximate ground vector, to the certified matrix. The certificate then bounds the **second** even eigenvalue (paper
  Lemma `lem:deflation`).
- Upper bounds `U(L)` come from Legendre–Galerkin Rayleigh quotients (`K = 640`, 3000 bits) with a rigorous Gauss–Legendre
  bound. `U(1.19) <= 8.712e-48` is sharper than Piece II's `1.312e-47`, and the first step needs it.
- 8 grid steps `1.19, 1.2205, 1.25, 1.2785, 1.3055, 1.3315, 1.3565, 1.3805, 1.4035` all pass. The smallest step ratio is
  `1.131`, on `[1.2205, 1.25]`, and the odd sector binds everywhere.

## What is proved

Take real `f` supported in `[-L, L]` (log scale) and form `Q(f) = W(f * f~)`. Here `W` is Weil's explicit-formula
functional. It has the pole terms, the archimedean term `Re psi(1/4 + it/2) - log pi`, and every prime power `n` with
`log n < 2L` (paper §2). Let `A_L` be the self-adjoint operator of the closed form on `L^2(-L, L)`.

**Theorem.** For every `L` in `(0, 2]`, the lowest eigenvalue of `A_L` is simple, and its eigenfunction is even.

The proof has four pieces.

- **Piece I, `(0, 0.05]`.** A Lipschitz argument for a rescaled form, anchored at the certified window `0.05`. The
  gaps are `>= 0.4172` (second even eigenvalue) and `>= 0.6624` (odd sector).
- **Piece II, `[0.05, 1.19]`.** 31 grid windows. At each one we certify a two-sided bracket for `lambda_0`, a lower
  bound on the second even eigenvalue and a lower bound on the odd sector. Adjacent windows are glued by min-max
  monotonicity in `L`. Every one of the 30 steps passes. The smallest step ratio is `1.288`, and the smallest past
  `L = 1` is `2.148`.

- **Piece III, `[1.19, 1.4035]`.** 8 grid steps. At each window, certified lower bounds on the second even
  eigenvalue and on the odd sector (Elston's certifier with `--deflate`) and a rigorous upper bound on the lowest
  eigenvalue (Galerkin Rayleigh quotient). Every step passes; the smallest step ratio is `1.131`. (The same route also
  passes on `[1.4035, 1.4885]`, which the theorem does not need.)
- **Piece IV, `[1.4035, 2]` (new in 2.0.0).** 53 grid steps, from 54 dyadic windows. At each window there are certified
  lower bounds on the odd sector and on the second even eigenvalue, from our clean-room rh_60-route certifier
  (`code/rh60route/`). That certifier does a full-source Schur elimination with an exact core, a rank-one deflation for
  `lambda_2^even`, and Lemma SR, an exact-integer structured LDL^T. Each window also has a rigorous upper bound `U(L)`.
  Every step passes. The smallest step ratio is `2.0986`, and the odd sector binds everywhere. The gap at
  `1.92364501953125` is closed by the post-hoc rule E, and also without it by `lem:mono` from the next window (see
  [Disclosures](#disclosures-for-release-200)).

Each step test proves simple-even on a closed interval `[L_i, L_{i+1}]` (paper Cor. `cor:step` with Lemma `lem:mono`). The
pieces share endpoints, so together they cover `(0, 2]`.

The prime powers 2, 3, 4, 5, 7, 8 and 9 enter inside Piece II, at `L = (1/2) log n`; 11, 13 and 16 enter inside
Piece III (at `1.1989`, `1.2825`, `1.3863`); 17, 19, 23, 25, 27, 29, 31, 32, 37, 41, 43, 47, 49 and 53 enter inside Piece IV
(`1.4166` ... `1.9851`).

The certified numbers are in `data/theorem_bounds.json` (Pieces I–II), `data/piece3/` (Piece III) and
`data/piece4/glue/` (Piece IV). Nothing past `L = 2` is claimed.

## What is new, and what is not

The convention throughout is that `L` is the half-width and `p^k` enters when `log p^k < 2L`.

- **Believed new: `(0.8, 2]`.** Our search (arXiv, Zenodo, GitHub and rStation; refreshed 2026-10-31, plus two items the
  Codex review found on 2026-11-01) found no certified proof of simple-even for any continuum window `L > 0.8`. Brendan
  Siche's repository `Architect-Resonance/Riemann-Hypothesis` (first commit 2026-04-03, unrefereed) claims simplicity for
  all windows via Krein–Rutman positivity; we do not regard it as established (paper §1.3: a finite sum of compressed
  translations is in general not compact, and the even pole term has norm `2(L + sinh L)`, not `O(log lambda)`). If it is
  correct, it contains our theorem. The only exception is the non-explicit neighbourhood of `0.8` in
  mathia PL-287. Andrade (Zenodo 20887028) and Andrews Jr. (Zenodo 22715669) certify simple-even for *finite* Galerkin matrices at
  `L ≈ 1.28, 1.68, 1.99`; those are not statements about the continuum form. Much of this literature is unrefereed
  Zenodo/GitHub work and appears quickly, so the search may have missed items. On rStation, lihongmin
  (riemann_hypothesis paper 45 v1, published 2026-10-23) and bramble_trace (paper 60 v1, published 2026-10-26)
  certify positivity of both parity sectors on `(0, (1/2) log 11]` and `(0, 2]` respectively; both use our form, and
  their support radius `a` is our `L`. Neither identifies the ground state or compares the sectors (paper 45 §1: "our
  lower certificate neither identifies the ground state nor estimates the sharp minimum"). What we claim as new on
  `(0.8, 2]` is therefore simple-even itself (the ground state is simple and even) and the certified lower
  bounds on the second even eigenvalue `lambda_2^even` that prove it, not positivity. Those bounds come from Piece II,
  from the rank-one deflation of Piece III, and from the deflated rh_60-route certificate of Piece IV. Piece IV
  re-implements bramble_trace's method in clean room and does not use their results.
- **Not new: `(0, 0.8]`.** Kramarenko-Byrd (Zenodo 23007100, v1 of 2026-09-27, unrefereed) claims a rigorous proof of
  simple-even for all `0 < L <= 4/5`, in the same convention. We have not checked that proof. Our certificate on
  `(0, 0.8]` is an independent computer-assisted confirmation of that range (independent of Kramarenko-Byrd; not
  methodologically independent of Zhu, whose reduction it uses). Earlier drafts of this work claimed `[0.1406, 1]` as new; we found
  Kramarenko-Byrd afterwards and **withdraw that claim**.
- **Not new: small `L`.**
  - `L <= 0.1406`: an explicit Beurling–Deny / positivity-improving argument (mathia PL-294; cf. Andrade, Zenodo
    20682834).
  - Non-explicit small `L`: Suzuki, arXiv:2606.09096.
  - `L <= 9/50`: an analytic argument is reported by grandchallenge / MATHSOLVE. We have not read it in full or
    verified its window convention.
- **Not new: `L = 0.8`.** Zhu (arXiv:2608.24827) certified simple-even at this single window. Zhu also certified upper
  bounds on `lambda_0` for `L` in `[0.5, 2]`.
- **Not new: the reduction.** The whole frequency-cutoff ("one-stroke") reduction is Zhu's (Thm 1.1, Lemma 3.1). That
  includes the head/tail block estimate, the envelope bound and the normalization. Every window certificate here rests
  on it.
- **Not new: positivity.** Positivity, i.e. `lambda_0 > 0`, is certified or claimed elsewhere on this whole range,
  including past `L = 1`. Sources include jose-paul-b, Zhu, Liu (`L = 1`, `17/16`), Mori (up to `(log 15)/2`), Senke
  (`77/64`), Elston (per-sector bounds at `1.19`–`1.495`), lihongmin (rStation riemann_hypothesis paper 45 v1, both
  sectors, `(0, (1/2) log 11]`) and bramble_trace (rStation paper 60 v1, both sectors, `(0, 2]`, full-source Schur
  certificate). Apart from Zhu's single window `L = 0.8`, none of these positivity results addresses simplicity or
  parity.

Our own contributions are:

- the certified covering of a continuum of windows by monotonicity;
- the Lipschitz piece at small `L`;
- the rank-one deflation that turns Elston's lowest-eigenvalue certifier into a second-eigenvalue certifier, and
  the Piece III covering built on it;
- Piece IV, which builds on the rh_60 / rh_45 method:
  - the formulas for general `L`;
  - the μ-shift;
  - the rank-one deflation, which raises the core displacement rank from 2 to 4;
  - Lemma SR, an exact-integer structured LDL^T;
  - the form-core argument;
  - the independent gates G0i and C-ind;
  - rule E;
  - the pre-registered grid and its gluing;
- the numerics that reach `L = 1.19`: a hybrid rigorous spherical Bessel evaluation (classical
  recurrence / continued-fraction scheme, cf. Gautschi 1967), and a sharper cutoff certified by
  interval subdivision (`psi_floor`, paper §5.2);
- write-ups of standard estimates and re-derivations of Zhu's lemmas.

See paper §1.3–1.4 for the full list with citations.

## Weakest links

The parts least checked, in order of how much the theorem depends on them. `REVIEWING.md` has the same list, with the checks.

1. **Piece IV, `[1.4035, 2]`.** The registered grid failed; the gap is closed by the post-hoc rule E, or without it by
   `lem:mono` from a registered record. The audits were by AI agents (Claude-based, and one Codex review). The piece also rests on imported trust that no audit re-verified (`data/piece4/AUDIT_GRID.md` §7):
   - Stage S `s(L)`: Elston's `schur_upper`, via `code/rh60route/stage_s.py`.
   - Elston's integer Cholesky. It decides V2 in every Piece IV run and is the whole certifier of Piece III. It was
     independently audited only at `L = 1.19`, and that audit included our `--deflate` addition.
   - `fr_sweep` `U(L)`.
   - The pipeline `certify.py` / `sr.c` / `sr_kernel`, and its proofs (Theorem V, Lemma SR, P1–P23 in `supplement/`,
     reviewed only by AI agents).
   - Arb/FLINT.
   - The paper's lemmas `lem:M`, `lem:deflation`, `cor:step` and `lem:mono`.
   Every step ratio is above 2, but the code base is new and large.
2. **Piece III, `(1.19, 1.4035]`.** It uses Elston's certifier at larger `L`, with per-window parameters and our `--deflate`.
   None of these has been audited. The step ratios are small (`1.131`–`1.552`).
3. **One form, several codes.** The lower bounds (Elston's code in Piece III, our rh_60-route code in Piece IV) and the
   upper bounds (`code/upper/`) must evaluate exactly the same form with the same norm.
   - In Piece IV, gates G0 and G0i check selected matrix entries against the paper's eq. (P). G0i computes them
     independently in mpmath, with its own prime list.
   - At the overlap windows, our Piece IV bounds are consistent with Elston's: neither exceeds an upper bound.
4. **Pieces I–II past `L = 1`.** The sharp-cutoff path and the windows `1.03`–`1.19` have not been through any review round.
5. **The rigorous Gauss–Legendre bound** in `code/upper/fast_recurrence.py`. Every `U(L)` relies on it, in Piece III and in
   Piece IV.

## Caveats

Items 1–7 are taken from the paper's caveats. For Piece IV, see [Disclosures](#disclosures-for-release-200) and
[Weakest links](#weakest-links).

1. **Normalization.** Our `Q` follows Zhu §6 and was checked against the zero side of the explicit formula. It is
   matched to the Connes–van Suijlekom / Connes–Consani–Moscovici form `QW_lambda` only up to a positive affine
   rescaling `aQ + b||.||^2`, which does not affect simple-even. The Codex review matched the pole, prime and archimedean
   terms against Connes–Consani–Moscovici (3.7)–(3.11); no human has checked this line by line. A mismatch in the
   relative weights of the pole, archimedean or prime terms would not be covered.
2. **Self-adjoint realization.** The operator is the one of the closure of `Q` on `C_c^inf(-L, L)` (closability: paper
   §2.3). The trial functions are polynomials and are argued to lie in the form domain (paper §5.2). We have not shown
   that trigonometric polynomials are an operator core, which Connes–van Suijlekom's Thm 6.1 needs.
3. **Python `min` on balls.** The gluing and a few steps in `certify.py` use Python `min` on Arb balls. That is not
   rigorous when balls overlap. In every current use they are separated by many orders of magnitude.
4. **Piece I precision anomaly.** The certified upper end of one integral grows with working precision (paper Remark 5.2).
   We use the largest value. The cause is not explained.
5. **Past `L = 1`.** The step ratios there are smaller (10.00, 6.548, 3.774, 3.933, 2.857, 2.148, 264.7), and the
   sharp-cutoff path is used only there. Zhu retracted an earlier positivity claim at `L = 1.19`, which is the last
   window of Piece II: our bracket there (`lambda_0 >= 7.823e-48`) implies positivity at that `L`, rests on the unreviewed
   sharp-cutoff and triangular code, and is the window most in need of independent checking. Positivity at `L = 1.19`
   is independently certified by rStation papers 45 and 60; what rests on our unreviewed code there is the
   simple-even bracket, not positivity. One error constant (Gauss–Legendre, off by one node)
   has already been found and corrected in this project; see Remark 5.9 of the paper. The tail bounds, the drop
   bound, the transport precision, the Bessel seeds and `psi_floor` deserve an independent audit. The sharp-cutoff
   path and the windows 1.03–1.19, which carry the novelty claim, have not been through any review round, internal or
   external. Nor has the upper-triangle panel summation in `certify.py` / `node_partial.py` that produced the windows
   1.12–1.19 (byte-identical to the previous full-product code on spot checks at `L = 0.3`, `0.8`, `1.0`).
6. **Piece III is unaudited beyond `L = 1.19`.** Elston's certifier was audited independently only at `L = 1.19`.
   The runs at larger `L`, the per-window parameters (`beta_K`, `T#`, `N`, Gauss points) and our `--deflate`
   addition have not been reviewed by anyone. The step ratios are small (`1.131`–`1.552`), so an error of about 13%
   in one bound could break a step. The lower bounds (Elston's code) and the upper bounds (our code) must evaluate
   the same form with the same norm (paper §5.4, "One form, two codes"). The revision of
   `code/upper/fast_recurrence.py` used for the `U` runs was not recorded; re-running `U(1.19)` with the shipped code
   reproduces the stored line exactly (`data/piece3/rerun_U1.19.jsonl`).
7. **Sources not fully read.** Liu, the MATHSOLVE argument and the Kramarenko-Byrd proof were not read or checked in
   full. Zhu was read from a text extraction of v2.

## Reproducing

### Requirements

- Python 3.12 with the packages in `code/requirements.txt` (`python-flint==0.9.0`, `mpmath==1.4.1`; `numpy` is
  needed only by `convergence.py`, `gl_correction.py` and `exploratory/`).
- FLINT 3 development headers, MPFR and GMP for the C tools. The certificate used the system FLINT 3.4.
  python-flint 0.9.0 bundles its own FLINT 3.6.0.

```sh
python3.12 -m venv .venv && . .venv/bin/activate
pip install -r code/requirements.txt
cd code && make            # builds vchol and veig
```

### Check the whole theorem (about 10 seconds)

```sh
PYTHON=.venv/bin/python ./check_theorem.sh
```

The script does four things:
- It checks the SHA-256 sums of `data/piece3/` and `data/piece4/`.
- It runs `code/theorem.py --check` for Pieces I–II.
- It runs `code/gap/check_steps.py` on `data/piece3/` for Piece III.
- It runs `code/rh60route/check_steps.py` on `data/piece4/glue/` for Piece IV. That check runs with `--stamp`, so every
  record must be a PASS, of the right window and sector, unmutated, and carry the grid stamp.

It ends with `COMBINED: ...` and the statement for `(0, 2]`. It does not recompute any window. The sections below run each
piece on its own.

### Check Pieces I–II from the stored bounds (a few seconds)

```sh
cd code && python theorem.py --check
```

This re-runs Piece I, including the Lipschitz constants at 768 bits, and every Piece II step on
`data/theorem_bounds.json`. It uses the longest prefix of the grid present in the file. It should end with
`THEOREM CERTIFIED for all L in (0, 1.19]` (compare `data/logs/check.log`). It does **not** recompute any window.

### Check Piece III from the stored certificates (seconds)

```sh
(cd data/piece3 && sha256sum -c SHA256SUMS)
python code/gap/check_steps.py
```

This compares, in Arb, `min(lambda_2^even, lambda_1^odd)(L_{i+1})` with `U(L_i)` for every step. It reads
`data/piece3/`, and it should end with `CERTIFIED: ... simple-even for all L in (0, 1.4885]` (compare
`data/piece3/check.log`). The theorem needs it only up to `1.4035`.

### Check Piece IV from the stored certificates (seconds)

```sh
(cd data/piece4 && sha256sum -c SHA256SUMS)
python code/rh60route/check_steps.py data/piece4/glue data/piece4/windows.txt \
  --stamp 7a3c6b287f840aba50fc11d49e6f919eb0cb758a6a0ce03e6248298feda4b9e8
```

The output is byte-identical to `data/piece4/logs/GLUE_r2.log`, and it ends with `ALL STEPS PASS (53 comparisons):
simple-even on [1.4035, 2] (minimum step ratio 2.099)`. With `data/piece4/windows_partial.txt` in place of
`windows.txt` you get the registered partial outcome (`GLUE_P.log`).

### Recompute a Piece IV window

See `code/rh60route/README.md`. It covers building the Lemma SR kernel, a re-run of `L = 1.5`, odd sector (about
3 minutes), and the inputs for every other window. Grid G took 87.4 core-hours (7 h 27 min wall) on one 64-vCPU VM, and the gap closure took about 0.34 core-hours.

### Recompute Piece III

Each certificate file stores its options in the field `args`. In `code/gap/elston/`:

```sh
C="--panels-per-unit 4 --schur-k 4000 --schur-iters 1500"
W="--a 1.2205 --delta 0.3 --beta-k 64 --tsharp 850 --nmodes 849 --gl 56 --prec 400"   # from g_1.2205_*.json
python grid_certificate_rigorous.py $W $C --sector odd --workers 28 --json g_1.2205_odd.json
python grid_certificate_rigorous.py $W $C --sector even --deflate --workers 28 --json g_1.2205_l2.json
```

The windows took 12 minutes to 7 hours each with 15–52 workers on 64-vCPU machines (paper Table 3). Memory
grows like `workers x N^2`: about 2 GB per worker at `N = 1757`. Upper bounds, in `code/upper/` (about 4–14 minutes
per window):

```sh
THREADS=8 python fr_sweep.py upper.jsonl "640" "1.19,1.2205,1.25" 3000
```

### Recompute Pieces I–II windows

On a single machine:

```sh
cd code
python certify.py 0.1 0.2                 # single windows (seconds to minutes each at L <= 0.8)
UPTO=0.8 CERT_PREC=768 python theorem.py  # windows 0.05 ... 0.8 into ./theorem_bounds.json, then glue
```

The rerun took 18 minutes for stage 1 on a 20-thread laptop. A run of `certify.py 0.1` takes
about 2 minutes and 0.3 GB of RAM. `theorem.py` (and `certify.py` when run as a script)
use a fixed pool of 20 processes; edit `Pool(20)` there on smaller machines. Windows past `0.8` are far more
expensive. Locally they will take days, so use a cluster.

On a cluster (optional): copy `code/` to each host as `~/weil`, or set `CERT_REMOTE_DIR`. Put a `.venv` inside it with
the same requirements. Make the hosts reachable by key-based ssh (`BatchMode=yes`). The coordinator refuses to use a
host whose `certify.py`, `bessel_rec.py` or `node_partial.py` differs by SHA-256.

```sh
export CLUSTER=user@host1,user@host2,user@host3
UPTO=0.97 CERT_PREC=1536 python theorem.py                                     # 0.84 ... 0.97
CERT_BESSEL_PREC=6144 CERT_MATMUL_PREC=320 CERT_VCHOL_PREC=384 python theorem.py  # 0.98 onward
python validate10.py   # optional: sharp-path recertification of L = 1.0, compared with ./theorem_bounds.json
```

We used a 3-node cluster with 64 cores per node. Observed times on it were:

| Windows | Time |
|---|---|
| `0.84`–`0.97` | about 10–14 min per window |
| `0.98`, `0.99` | about 85 min per window |
| `1.03` | 48 min |
| `1.06`, `1.09` | 3 h 04 min and 3 h 16 min |
| `1.12` | 6 h 53 min (cluster assembly, then about 44 min local certification) |
| `1.15`, `1.18`, `1.19` | pipelined: cluster assembly (`prefetch.py`) about 6 h 33 min, 6 h 58 min and 6 h 59 min; local certification 41, 64 and 79 min, overlapped with assembly of the next window |

Memory per worker grows like `N^2`: the cap in `node_partial.py` budgets about `100 N^2` bytes per worker (the
upper-triangle sums, measured 0.87 GB at `N = 4305`, plus the ~0.75 GB shared-memory file) and limits the number of
workers by available memory (`CERT_NODE_PROCS` overrides it). The cached head matrices in `code/cache/` also grow like
`N^2`: about 160 MB each at `L = 1.0`, 1.06 GB each at `L = 1.19`.

Other environment variables:

- `CERT_MARGIN` (default 1.05) and `CERT_DDIV` (default 100) set the slack of the verified Cholesky.
- The rerun needed `CERT_MARGIN=1.2 CERT_DDIV=8` at `L = 1.0` (`paper/NOTE.md` §7.2).
- `CERT_DIGITS` sets the transport precision.

With the released code, `L = 1.0` is computed by the sharp path, so a fresh run reproduces `data/validate_1.0.json`
at that window rather than the rerun's row.

## File map

```
README.md               this file
check_theorem.sh        checks Pieces I-IV from the shipped data and prints the combined statement
REVIEWING.md            how to review: weakest links and checks by effort
LICENSE                 MIT (code)
CITATION.cff            citation metadata
paper/main.tex, main.pdf the paper (CC BY 4.0, see paper/LICENSE); refs.bib
paper/NOTE.md           the note of the (0, 1.19] release of 2026-10-26
code/certify.py         per-window certificate: lower bounds (frequency side, Zhu's reduction), upper bound
                        (position-side Rayleigh quotient), sharp-cutoff path (SHARP_TS, psi_floor), cluster dispatch
code/theorem.py         grid + Piece I + Piece II gluing; --check mode
code/lipschitz.py       Piece I constants
code/bessel_rec.py      rigorous hybrid spherical Bessel evaluation (used for L >= 0.98)
code/node_partial.py    cluster worker (upper-triangle panel sums), memory-capped
code/prefetch.py        assembles head matrices on the cluster ahead of the certifying run (pipelining)
code/vchol.c            verified Cholesky (C, FLINT)
code/veig.c             inverse-iteration estimates (non-rigorous, only to choose what to certify)
code/validate10.py      sharp-path validation at L = 1.0
code/gl_correction.py   historical: Gauss-Legendre erratum correction of the original runs
code/convergence.py     non-rigorous Galerkin matrices (trial vectors in gl_correction.py; exploratory scripts)
code/Makefile, code/requirements.txt
code/gap/elston/        Elston's certifier (MIT, own LICENSE, UPSTREAM_COMMIT) with the added --deflate option
code/gap/check_steps.py Piece III step test (gluing)
code/gap/params.py      design rule for the Piece III window parameters (not used by the proof)
code/upper/             rigorous Legendre-Galerkin upper bounds (fast_recurrence.py, hp.py, fr_sweep.py)
data/                   certified bounds, history, scrubbed logs (see data/README.md)
data/piece3/            Piece III certificates, upper bounds, check log, SHA256SUMS
code/rh60route/         Piece IV: our clean-room rh_60-route certifier, Lemma SR kernel, step test, grid drivers (README)
data/piece4/            Piece IV records, upper bounds, controls, pre-registrations, stamps, results, audit, SHA256SUMS
data/upper/             original records of the paper's upper-bound table (L = 1.5 ... 2.25)
data/kinks/             raw jump measurements of paper §9 (L = 1.19, four resolutions)
supplement/             Piece IV specification (SPEC.md), proofs P1-P23 (PROOFS.md), formula -> code -> field map (MAP.md),
                        protocol and review history (AUDITS.md)
reviews/                the two Codex reviews of the release candidates and our point-by-point responses
exploratory/            NON-RIGOROUS scripts behind `paper/NOTE.md` Appendix A and the normalization check
```

## AI assistance

The code, the computations, the paper drafts and the internal "reviews" in the paper's review log were produced
largely by an AI assistant: Anthropic's Claude, used through Claude Code, in sessions directed by the author, who
decides what to publish. The author is not a professional mathematician. The mathematical arguments have been
checked only by AI-run internal reviews, not by an independent human expert. That includes the pre-registrations, the
scoring and the fresh-agent audit of Piece IV in `data/piece4/`. Two review rounds were by a different AI system (OpenAI's Codex,
`reviews/`); they are still AI reviews.

Errors were found during the work. Known ones are documented in the paper (Remark 5.9, §10) and in `paper/NOTE.md` (erratum, §7):

- the Gauss–Legendre off-by-one;
- a thread-unsafe precision change;
- an out-of-memory failure.

There may be others. Independent checking of the code and of the lemmas is welcome. That includes checking against
the cited prior work, especially Zhu and Kramarenko-Byrd.

## Credits

- **A. Weil.** The explicit formula and the quadratic form.
- **A. Connes and W. van Suijlekom** (arXiv:2511.23257) and **A. Connes, C. Consani and H. Moscovici**
  (arXiv:2511.22755). They posed simple-even as the missing step. Also A. Connes, survey arXiv:2602.04022.
- **M. Suzuki** (arXiv:2606.09096). The small-`L` theorem.
- **Zhu** (arXiv:2608.24827). The reduction strategy this proof rests on (one-stroke frequency cutoff, head/tail block
  estimate, envelope Lemma 3.1, normalization). Also the certificate at `L = 0.8` and certified upper bounds on
  `lambda_0` for `L` in `[0.5, 2]`.
- **Kramarenko-Byrd** (Zenodo 23007100). Claimed simple-even on `(0, 0.8]`.
- **Other prior work.**
  - mathia project notes PL-282, PL-287, PL-294 (GitHub `murillo128/mathia`).
  - Andrade (Zenodo 20682834, 20887028).
  - grandchallenge / MATHSOLVE.
  - jose-paul-b (`weil-positivity-certificates`).
  - Liu.
  - Mori (Zenodo 23281236).
  - Senke (Zenodo 22871384), positivity at `L = 77/64`.
  - Andrews Jr. (Zenodo 22715669), finite-matrix simple-even at `L ≈ 1.282`.
  - Elston (`weil-windows`, Zenodo 10.5281/zenodo.23174403). His certifier produces every Piece III lower bound. His
    integer Cholesky, and the Schur test behind `s(L)`, are used in every Piece IV run.
  - Elder (Zenodo 23113186).
  - Eberwein (Zenodo 23177438).
  - "Eureka" (arXiv:2608.19047).
  - lihongmin, "Cutoff-free positivity of localized Weil forms through the (log 11)/2 threshold", rStation
    riemann_hypothesis paper 45, v1, published 2026-10-23T09:48:37Z,
    https://rstation.ai/problems/riemann_hypothesis/papers/45/v1. Positivity of both parity sectors on
    `(0, (1/2) log 11]`.
  - bramble_trace, "Full-source Schur certificates for Weil positivity at support radius two", rStation
    riemann_hypothesis paper 60, v1, published 2026-10-26T19:12:17Z,
    https://rstation.ai/problems/riemann_hypothesis/papers/60/v1. Positivity of both parity sectors on `(0, 2]`.
  - **Method credit for Piece IV.** Piece IV follows the method of bramble_trace (rh_60 v1) and lihongmin (rh_45 v1), in a
    clean-room implementation with the additions listed above. Both are unrefereed AI-agent preprints reviewed only by AI
    agents.

  See paper §1.3 for what each one did.
- **Software.**
  - FLINT/Arb (F. Johansson and the FLINT developers).
  - python-flint (its contributors).
  - GMP and MPFR (used by the C tools).
  - mpmath (F. Johansson et al.). The zeta zeros in `exploratory/zeros.txt` were computed with `mpmath.zetazero`.
  - NumPy.
- **W. Gautschi** (SIAM Review 9, 1967). The continued-fraction scheme behind the Bessel evaluation.
- **A. Connes and C. Consani** (arXiv:2106.01715, Lemma 2.7). Pole splitting (`paper/NOTE.md` Appendix A).
- **Quadrature bound.** L. N. Trefethen, *Approximation Theory and Approximation Practice*, Thm 19.3.

## Author and contact

Johann Alexander Botha, GenusCore (not a professional mathematician). Contact: info@genuscore.com.
Corrections and error reports are very welcome.

## License

- **Code:** MIT; see `LICENSE`. `code/gap/elston/` is Zac Elston's code under his MIT licence (`code/gap/elston/LICENSE`).
- **Paper and data:** CC BY 4.0; see `paper/LICENSE`.

## How to cite

Archived on Zenodo. DOI for all versions (resolves to the newest): [10.5281/zenodo.23832220](https://doi.org/10.5281/zenodo.23832220);
this version, v2.0.0: [10.5281/zenodo.23852617](https://doi.org/10.5281/zenodo.23852617); the previous version, v1.1.1:
[10.5281/zenodo.23832221](https://doi.org/10.5281/zenodo.23832221). See also `CITATION.cff`:

> Johann Alexander Botha, *A certified simple, even ground state of the localized Weil quadratic form for all windows
> L in (0, 2]*, computer-assisted paper and code, version 2.0.0 (2026-11-01), Zenodo, doi:10.5281/zenodo.23852617.
> Unrefereed, produced with AI assistance.

Please also cite Zhu (arXiv:2608.24827), whose reduction the proof uses; Elston (`weil-windows`), whose certifier
Piece III uses; bramble_trace (rStation rh_60 v1) and lihongmin (rh_45 v1), whose method Piece IV uses; and the prior work
listed above where
relevant.
