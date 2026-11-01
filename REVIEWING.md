# Reviewing and auditing this work

This is a computer-assisted proof that has **not been peer-reviewed**. All checking so far was done by the
author with AI assistance: independent recomputation, two separate code paths, and AI-run review rounds
(see the paper, §"Verification and audits"). Piece IV was also pre-registered and audited by a fresh AI agent
(`data/piece4/`), and a release candidate of 2.0.0 was reviewed by a second AI system, OpenAI's Codex (`reviews/`).
No independent human expert has checked the proofs or the code.

**Independent review is welcome from anyone.** You do not need to check everything: one verified step,
one reproduced window, or one well-founded objection is a real contribution and will be credited
(by name or anonymously, as you prefer) in the paper and in this file.

## How to report

- Open a GitHub issue, with the label `review` if you can. Please say which section, file or table it
  concerns, what you checked, and what you found, including "checked, no problem found".
- Or write to info@genuscore.com.
- Errors are the most valuable kind of feedback. Confirmed errors are fixed in public, with credit,
  and listed in the paper's erratum.

## Where to look first: the weakest links

These are the parts we consider least checked, roughly in order of how much the result depends on them:

1. **Piece IV (L in [1.4035, 2], new in release 2.0.0).** This is our clean-room rh_60-route certifier
   (`code/rh60route/`).
   - **Rule E.** The pre-registered grid failed at L = 1.92364501953125. The gap is closed by rule E, which raises the
     truncation N by 1024 at that window. Rule E is post hoc: it was written after the failure and after a diagnostic that
     showed it passes, and stamped before its scored run. Is rule E sound? `data/piece4/PREREG_GAP.md` §2 and
     `AUDIT_GRID.md` §3 argue that it is. Rule E is not needed for the theorem: by Lemma `lem:mono` the registered
     grid record at 1.9326171875 bounds λ_2^even at 1.92364501953125 from below (paper Remark 7.5), and
     `check_theorem.sh` also runs that route (`--l2-from 1.92364501953125=1.9326171875`, 53 steps pass).
   - **Weak negative control.** The negative control of rule E failed at V2, not at V4. So no control exercises Lemma SR at
     the new N.
   - **Audit.** The only audit was by an AI agent, which used the same Arb library.
   - **Imported trust, not re-verified:**
     - Stage S s(L): Elston's `schur_upper`.
     - Elston's integer Cholesky, which decides V2.
     - `fr_sweep` U(L).
     - `certify.py`, `sr.c`, `sr_kernel`, and their proofs: Theorem V, Lemma SR, P1–P23. The proofs are in
       `supplement/PROOFS.md` (byte-identical to the stamped file), with `supplement/SPEC.md` and the map
       `supplement/MAP.md`; they were reviewed only by AI agents.
     - Arb/FLINT.
     - Lemmas `lem:M`, `lem:deflation`, `cor:step` and `lem:mono`.
   - **Step ratios.** They are at least 2.0986, so breaking a step would need one bound to be wrong by a factor of about 2.
     But the code is new, and it follows unrefereed AI-agent preprints (rStation rh_60 v1, rh_45 v1).
2. **Piece III (L in (1.19, 1.4035], new in release 1.1.0).** It uses Elston's certifier
   (`code/gap/elston/`, MIT), which was independently audited only at L = 1.19, and our `--deflate` addition
   (about 15 lines, option `--deflate` in `grid_certificate_rigorous.py`). Neither the larger-L runs, nor the
   per-window parameter changes (beta_K, T#, N, Gauss points), nor the deflation have been audited. The step
   ratios are small (1.131 to 1.552), so a 13% error in one bound could break a step.
3. **One form, several codes.** The step test compares lower bounds (Elston's code in Piece III, our rh_60-route code in
   Piece IV) with our upper bounds. Both must
   evaluate exactly the same quadratic form with the same norm (paper, §5.4, "One form, two codes").
4. **The sharp-cutoff path and the windows 1.03–1.19** of Piece II (paper §5.2 and the README), which have
   not been through any review round.
5. **The rigorous Gauss–Legendre bound** in `code/upper/fast_recurrence.py`, `quad_bounds` (Bernstein
   ellipse, n-point rule exponent ρ^(−2n+2)), which all upper bounds U(L) rely on. The revision of that file
   used for the U runs was not recorded (paper, Remark 8.2).

## Checks by effort

### Minutes (no heavy computation)

- **Run `./check_theorem.sh`.** It checks the SHA-256 sums (including `supplement/` against `GAP.stamp`) and runs the
  gluing checks (Pieces I–II, III, and IV with and without rule E). It should end with the combined statement for (0, 2].
- **Check the Piece IV provenance.**
  - Every glued record in `data/piece4/glue/` should be a PASS with all 15 gates true.
  - Each record should carry `stamp_sha256` 7a3c6b28…, and an amendment pin that is a prefix of the chain.
  - Compare the rule-E record with the three FAIL rungs in `data/piece4/rule_e/`. Its argv should differ from the
    `1o4` rung only in `--tmin`, `--out` and `--label`.
  - Read `PREREG_GAP.md` against `RESULTS_GAP.md` and `AUDIT_GRID.md`.
- **Check the redaction.** `data/piece4/REDACTION.sha256` lists every redacted file. If you obtain the originals, they
  should hash to the left column and verify with `python code/rh60route/amend.py AMENDMENTS.log --verify`.
- **Re-check the gluing piece by piece.** `python code/theorem.py --check` (Pieces I–II, `data/theorem_bounds.json`),
  `python code/gap/check_steps.py` (Piece III, `data/piece3/`) and the Piece IV command in the README; confirm every step ratio
  min(λ₂^even, λ₁^odd)(L_{i+1}) / U(L_i) exceeds 1, and compare with `data/logs/check.log` and
  `data/piece3/check.log`. `sha256sum -c data/piece3/SHA256SUMS` (run in `data/piece3/`) checks the files.
- **Read the deflation lemma and its corollary** (paper, Lemma 5.14 and Corollary 5.15, half a page).
- **Read the monotonicity lemma and the step criterion** (paper §3).
- **Spot-check certificate files** against the tables in the paper (every number in a table is traceable to a
  file listed in the reproducibility table).

### Hours (one machine)

- **Re-run one Piece IV window.** `code/rh60route/README.md` re-runs L = 1.5, odd sector (about 3 minutes, 1.3 GB), and
  L = 2 (about 45 minutes per sector, 3.5 GB). Compare `mu`, `N`, `M`, `SR_checksum` and `certified_lower_bound` with
  the shipped record. Building the Lemma SR kernel with GCC 15.2 reproduces the binary the runs used bit for bit.
- **Re-run one Piece III window**, e.g. L = 1.2205 (a few core-hours), with and without `--deflate`, and
  compare with the shipped JSON.
- **Re-run one upper bound U(L)** with `code/upper/fr_sweep.py` (K = 640, 3000 bits, about 12 minutes) and
  compare `lam0_upper` with `data/piece3/upper640.jsonl`.
- **Re-run one Piece II window** with `code/certify.py`.

- **Check the Piece IV far-block and tail constants against the code.** Read `supplement/PROOFS.md` P14–P22 (moment
  bounds, L_ab, r̄, V_h/E_h/J_2/J_4, τ_N, t′_q, S_M, ε_asm, r_M) and follow `supplement/MAP.md` to the lines of
  `code/rh60route/certify.py` and the record fields that hold each value. The paper (§7.3, "The explicit constants")
  states the same formulas.

### Days (cluster or patience)

- Full re-run of Piece IV: 87.4 core-hours on one 64-vCPU VM, driven by `code/rh60route/run_grid.sh`.
- An independent implementation of Lemma SR, or of the Piece IV far-block bounds (C-τ, C-r̄, C-J_2, C-r_M).
- Full re-run of Piece III up to 1.4035 (about 800 worker-process hours; parameters in each JSON's `args`).
- A line-by-line audit of Elston's certifier at larger L, or of our upper-bound code.
- An independent implementation of any one component (the best check of all).

## What a review is not expected to do

You do not need to assess the Riemann hypothesis, the Connes–van Suijlekom programme, or the novelty
claims; those are stated with sources in the paper's introduction. The question is only:
**are the stated bounds correct and does the argument prove the theorem as stated?**
