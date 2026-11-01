# AUDIT_GRID: fresh-agent audit of grid G and its gap closure (PREREG_GRID §4 step 9; PREREG_GAP §7.3)

**Verdict: (0, 2] certified**, in the PREREG sense, and conditional on the imported trust in §7. Simple, even ground state of
A_L for every L in (0, 2]. It is made of three pieces:
- **(0, 1.19]:** Pieces I–II, already public.
- **[1.19, 1.4035]:** Piece III, the Elston route, public in v1.1.x. The same route also passes on [1.4035, 1.4885], which is
  redundant here.
- **[1.4035, 2]:** rh_60-route grid G, with the gap closed by rule E under PREREG_GAP.

How it must be reported:
- **Grid G as registered still FAILS (K3g).** The [1.4035, 2] piece rests on a **post-hoc registered fix**. Rule E was written
  after the failure and after the D2 diagnostic. It is sound (§3), but it must always be reported as post hoc, next to K3g.
- **Grid G alone certifies [1.4035, 1.91912841796875]** (C-P, 43 steps). That is the fallback claim if rule E is not accepted.

Date 2026-11-01.
- **Clean room.** Nothing under `scratch_archive/rstation/` and no rStation URL was opened.
- **vm3 was only read.** Over ssh I used sha256sum, md5sum, stat, ls, and `amend.py --verify`, which reads only. Nothing was
  run, written, or killed there, and no other VM was touched.
- No push, publish or contact.

## 0. Inputs and own code

- **Documents.** RESULTS_GRID, VERIFY_GRID, GAP_DIAG, PREREG_GAP, GAP.stamp, RESULTS_GAP.
- **Mirrors.** `grid_run/` (grid G) and `grid_run_gap/` (230 files; `md5sum -c MD5SUMS` OK).
- **Archive and code.** The laptop `archive/`, `grid/`, `code/` and `gap/check_steps.py`.
- **Elston-route records.** `highprec/gap/out_all/`, plus `weil-public/data/theorem_bounds.json`.
- **Own script.** `audit_grid/ag.py`, output in `ag.out`, step table in `ag_steps.tsv`.
  - It uses python-flint 0.9.0 at prec 512 and `fractions`.
  - It imports none of grid.py, check_steps.py, pilot.py, certify.py or amend.py.
  - It ends with `RESULT: ALL CHECKS PASS`.

## 1. Pre-registration and provenance

| check | result |
|---|---|
| GAP.stamp | sha256 ed3dca15… and md5 da5e1137… on both the laptop and vm3. All 28 sha256 lines verify on the laptop. On vm3 all of them verify except `REFINE_1.91912841796875_…`, which is expected because it was renamed. Its content, `REFINED_…`, still has the stamped sha256 8a1f1bce…, so this is a rename only. The 7 stamped grid records (3 FAIL rungs, fallback records, U(L′)) verify on the mirror |
| Code blobs | All 20 executed-file blobs of GAP.stamp are present on vm3, and each content sha256 equals its name. The 8 document lines have no blob, by design |
| Amendment chain | Own hash-chain check: OK at 21 entries, sha256 c9029e85…. The laptop log has md5 9c0dcdb8…, equal to vm3. Prefix hashes: 19 entries 2e5b71cd… (as GAP.stamp states) and 20 entries 558287d9… |
| Entry 20 | md5 of PREREG_GAP.md 9651618d…, GAP.stamp, grid.py 2e327acb…, check_steps.py cbbb461d…, jobs_gap.txt, jobs_gap_mono.txt and windows_partial.txt. All equal the current files |
| Entry 21 | All 14 md5 values equal the mirror files. Those include the e1 record, the control, the REFINED_ marker, the glued e1 copy, and every new log and .rss |
| Order | stamp 01:12:01Z < entry 20 01:12:15Z < runner start 01:13:06Z < control written 01:15:27Z < e1 written 01:31:52Z < GLUE_r2 01:32:08Z < entry 21 01:34:00Z. These are vm3 file mtimes in UTC, and they agree with runner.log and the record `utc` fields |
| Pins | e1 and the control carry `amendments` = {entries 20, sha256 558287d9…}. That is the log *including* entry 20, so both started after the registration. Both have `stamp_sha256` = sha256(GRID.stamp) = 7a3c6b28…, as PREREG_GAP §0 registers |
| Mirror vs vm3 | 222 new files (out, glue, logs, done) have equal sha256. VERIFY_GRID already showed this for grid G's 289 record files |
| Status | No STOP_*, no MONO_ and no REFINE_ (only REFINED_ ×2) in the mirror or on vm3. The 4 done files are all 0. vm3 `grid_run/glue/` has 208 files |
| Code changes | grid.py: rule E, `nc l2e`, glue ARGS pass-through, and a REFINE block only when both windows are in W. check_steps.py: `--l2-from`, unused here. I diffed both against the archive blobs 94399de9… and 083dece7…. certify.py and every `code/` file are unchanged (the e1 code map equals the grid G records and the GAP.stamp lines) |

## 2. Rule-E run and control (records re-read, not taken from RESULTS_GAP)

**`l2_1.92364501953125_1o4_e1`:**
- **Result.** PASS, `failed_gates` [], and all 15 gates true. Ldec, ε = +1, deflated, mut null.
- **Argv.** Equal to the failed `l2_…_1o4` rung except `--tmin` (0.5 → 0.5920743125 = t_N(1o4) + 2^−10; exactly one `--tmin`),
  `--out` and `--label`. μ, θ and s (sha 00f9b8d3…) are identical to the failed rung.
- **N.** 37888 → **38912**.
- **Certified quantities.** The certified ball [4.5716755664090265288e−232 ± 1.93e−252] contains the exact dyadic μ, and its
  lower end is > 0.
- **Gates.**
  - V4 is the exact SR fail flag (−1).
  - R6 is ε_E ≤ 2^−12 as a Fraction.
  - V5 is an Arb lower end > 0 (margin 0.00443).
  - t′_N = 775922533935/2^40 > 0.
- **No float in the certified quantities.** float_pmin, min_pivot and eps_E are reported as floats. The gates use the exact
  values (certify.py lines 669–682).
- **N2.** μ = ¼·λ̂_2(M_0) ≤ λ̂_2(M_0) (Fraction).
- **RG-1.** All registered fields equal D2 (`gap_diag/diag_D2_N38912.json`), so RG-1 is a HIT. Only run metadata differs.

**`nc_1.92364501953125_l2e`:**
- FAIL with `failed_gates` [V2] ("core Cholesky proposal failed").
- G-S, G0-mini and G0i are true, and no gate is false. There is no certified bound and no STOP_G2.
- μ/λ̂_2(M_0) = 1.010000 (rounded up), so μ > λ̂_2(M_0) holds exactly. C-N holds as registered.
- **Weakness (RG-2 MISS).** The control stops at the core proposal, so it does not exercise Lemma SR/V4 at N = 38912. The
  liveness of V4 rests on other evidence: the 6/6 grid G controls that FAIL at V4, the 4 grid records that FAIL at V4 at the
  last label, and D1.

## 3. Can rule E create a false PASS? No

- **N is free in Theorem V.** PROOFS §8 needs only V1–V5 with t′_q ≥ t′_N > 0. N is not otherwise constrained, and every gate
  (V2–V5, G5, G5′, C-τ, C-r̄, C-J_2, C-r_M, C-ind, R6) is recomputed at the new N by the unchanged certify.py.
- **What the fix changes.** It changes one argv float that enters only the R4 N loop (certify.py l. 416–422:
  `tq(N).lower() >= tmin`), so it only selects N. It touches no tolerance, gate or certified formula.
- **The trigger is mechanical.** It reads stamped records. The only freedom left is the choice of N, made after seeing the FAIL.
  For a deductive certificate that freedom carries no false-positive risk, unless the code has an N-dependent bug.
- **N = 38912 has been exercised before.** The grid's odd run at 1.9052734375 used the same N. D2 (with G5 extended to labels
  N−1..N−3) agrees with the direct far sum at this N, and the e1 record reproduces D2 bit for bit.
- **The glue is not weakened.** The REFINE filter decides only whether glue runs at all. check_steps still requires every
  record, and a missing record FAILs. GLUE_r2 used no `--l2-from` (0 `lem:mono` lines).
- **The fallback (`lem:mono` substitution) was not used.** Its §4 trigger did not hold, `jobs_gap_mono.txt` did not run, and
  there is no MONO_ marker.
- **The `lem:mono` direction is correct.** The PREREG_GAP §4 proof sketch has it right: extension by zero gives
  λ_k^ev(L′) ≤ λ_k^ev(L) for L < L′, so a bound at L* holds for every L ≤ L*. The same lemma is already used by Cor. `cor:step`
  in every step.

## 4. Glue provenance

- **Each of the 106 glued `g_<L>_<kind>.json` is byte-equal to the first sorted PASS record** for that (L, kind), taken over the
  union of `grid_run/out` and `grid_run_gap/out`. At 1.92364501953125 that record is `l2_…_1o4_e1`, since the 1o1024, 1o4 and 2
  rungs are FAIL.
- **The 102 glued `upper*.jsonl` files are byte-equal to `grid_run/upper/`.** Every row has `rigorous_quadrature: true`.
- **Every glued record passes the same checks:**
  - result PASS, `failed_gates` [], and all 15 gates true;
  - Ldec equal to the file name, mut null, and the right sector;
  - stamp 7a3c6b28…;
  - an amendment pin (≥ 14 entries) whose sha256 equals that prefix of the chain;
  - certify.py 0cbb7e7f…;
  - N2: odd μ ≤ U^od(L) in Arb, λ_2 μ ≤ λ̂_2(M_0);
  - the ball contains μ, and its lower end is > 0.

## 5. Step chain [1.4035, 2] (own python-flint, prec 512)

**Method.**
- U^ev(L_i) is the minimum of `arb(lam0_upper).upper()` over the par-0 rows at the exact L string.
- ℓ is `arb(certified_lower_bound).lower()`.
- A step passes iff min(ℓ_od, ℓ_2)(L_{i+1}) > U^ev(L_i).
- windows.txt has md5 74e62f6d…, 54 windows, strictly increasing. windows_partial.txt is its first 44 windows.

| span | steps | ratio range | binding |
|---|---|---|---|
| [1.4035, 1.5] | 9 | 50.57–121.3 | odd |
| [1.5, 1.91455078125] | 33 | **2.0986**–2.487 | odd |
| [1.91455078125, L′ = 1.91912841796875] | 1 | 470.0 | odd |
| **[L′, 1.92364501953125] (gap)** | 1 | **448.61** | odd (ℓ_2 = 4.572e−232 exceeds U^ev(L′) = 2.747e−239 by 1.66e7) |
| [1.92364501953125, 2] | 9 | 2.220–2.411 | odd |

**Results.**
- **Partial chain:** 43/43 steps pass, minimum 2.0986. C-P is reproduced.
- **Full chain:** 53/53 steps pass, minimum **2.0986 at [1.5, 1.5174560546875]**. The next smallest are 2.201
  ([1.86688232421875, 1.87664794921875]) and 2.220 ([1.9326171875, 1.94146728515625]).
- **Agreement with GLUE_r2.** All 53 rows agree with the GLUE_r2 log (same steps, ratios within 1 %, 0 mismatches) and with
  RG-3/RG-4.

## 6. Combined statement

**Elston route, own recomputation from `gap/out_all`.**
- U(1.19) is the minimum of the rigorous fr_sweep rows: 8.7117e−48. That is below Piece II's 1.3116e−47, and the public
  release README states it the same way.
- 12/12 steps pass on [1.19, 1.4885]: 1.405, 1.132, 1.321, 1.138, 1.413, 1.293, 1.546, 1.552, 1.430, 1.379, 1.346, and
  1.129 on [1.468, 1.4885].
- The record files equal `weil-public/data/piece3` where both exist (spot sha256).

**Why the pieces combine.** Each step test proves simple-even on the *closed* interval [L_i, L_{i+1}], using Cor. `cor:step` with
`lem:mono`. Pieces I–II give (0, 1.19], Piece III gives [1.19, 1.4035] (or [1.19, 1.4885]), and grid G with rule E gives
[1.4035, 2]. The pieces share endpoints, so together they cover **(0, 2]**. Only (0, 1.4035] is needed from the earlier
routes; the Elston steps beyond it are redundant.

## 7. Imported trust (not verified here)

1. **Stage S s(L)** at every grid window, including 1.92364501953125 (the e1 run reuses s sha 00f9b8d3…). This means Elston's
   `schur_upper` and the Liu data. G-S catches only errors larger than s − Ritz guard.
2. **Elston's integer Cholesky and residual code**, which decides V2 in every rh_60-route run and is the whole certifier of
   Piece III. Per the public README, caveat 6, it was audited independently only at L = 1.19. That includes our `--deflate`
   addition.
3. **fr_sweep U(L)** and its outward rounding of `lam0_upper`, including the seeded U(1.4035) and U(1.19) ≤ 8.712e−48.
4. **The certify.py, sr.c and sr_kernel pipeline** beyond its records, plus PROOFS (Theorem V, Lemma SR, P19–P23). These rest on
   review.md, AUDIT, FIXES, P0 and 15/15 G4 mutations. They are not re-proved here.
5. **Arb/FLINT (python-flint 0.9.0).** My own step check uses the same library, so it is not independent of Arb.
6. **The paper:** §2.3 (closability, compact resolvent, min-max), Lemma `lem:M`, `lem:deflation`, Cor. `cor:step` and Lemma
   `lem:mono`, as well as the Green identity (P1–P2), which is checked only indirectly through G0 and G0i.
7. **Pieces I–II (0, 1.19]** as released, with that release's own caveats: windows 1.03–1.19 have not been through any review
   round, and Zhu retracted a claim at exactly L = 1.19.
8. **The vm3 host** reports file contents and times honestly. Every mirror file matches it by sha256.

## 8. Observations (none changes the verdict)

- **RG-2 MISS.** The control is weaker than planned (§2). A future control should target V4, for example with μ just below
  λ̂_2(M_0) at the old N, or with the last-pivot G4 mutation that GAP_DIAG suggested.
- **1.8958740234375 shares the failure pattern.** It passed only on the 2^−10 rung, at the last label of a different N. Rule E
  is tested at one window. Future grids should register an N rule that avoids this edge effect up front.
- **The `nc` log's first bytes are overwritten** ("tart"), because pilot and the runner share a filename. The record is
  unaffected, and its md5 is in entry 21.
- **Every step in [1.4035, 2] is odd-limited.** So the true λ_2 margin is not binding anywhere, including the gap step.
