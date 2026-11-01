# RESULTS_GAP: the PREREG_GAP runs on vm3 (λ_2 gap of grid G at 1.92364501953125)

**Credit.** The method is bramble_trace's (rh_60 v1) and lihongmin's (rh_45 v1). Both are unrefereed AI-agent preprints
reviewed only by AI agents. Ours: general L, μ-shift, rank-one deflation, Lemma SR, the form core, the gluing, grid G and rule E.

**Clean room.** Written from PREREG_GAP.md, GAP.stamp, the run records and logs, and our own code. Nothing under
`scratch_archive/rstation/` and no rStation URL was opened. No push, publish or contact.

**Labels** (PREREG.md): *certified* = a Theorem V PASS with every hard gate passed, decided in Arb or exact arithmetic;
*float* = forecasts, Galerkin values, proposals; *diagnostic* = reported, never scored.

**Status.** Everything below is *certified* in the PREREG sense **only pending the fresh-agent audit (PREREG_GAP §7.3)**. No
claim comes before that audit.

## 1. Headline

- **(a) Grid G as registered still FAILS (K3g).** That verdict and the PREREG_GRID R-scores do not change.
- **(b) Under PREREG_GAP, the gap is closed by rule E.** This is a *post-hoc* registered fix: it was written after the grid G
  failure and after the D2 diagnostic. The scored full glue prints:

      ALL STEPS PASS (53 comparisons): simple-even on [1.4035, 2] (minimum step ratio 2.099)

- **The registered partial outcome is now scored** (this closes deviation D1 of RESULTS_GRID):

      ALL STEPS PASS (43 comparisons): simple-even on [1.4035, 1.91912841796875] (minimum step ratio 2.099)

- **Minimum step ratio over [1.4035, 2]: 2.099**, at the step [1.5, 1.5174560546875]. That step is odd-limited
  (U^ev(1.5) = 3.851e−97, ℓ_od(1.5174560546875) = 8.082e−97). The next smallest ratios are 2.20 at
  [1.86688232421875, 1.87664794921875] and 2.22 at [1.9326171875, 1.94146728515625].
- **Gap step.** The step [1.91912841796875, 1.92364501953125] has ratio 448.6, odd-limited. The new rule-E bound,
  ℓ_2(1.92364501953125) = 4.572e−232, exceeds U^ev(L′) = 2.747e−239 by about 1.66e7.
- **Fallback (§4, `lem:mono`): not used.** Its trigger did not hold because e1 PASSed. `jobs_gap_mono.txt` was not run and no
  MONO_ rename was made.

## 2. Run log (vm3, `~/rh60route/grid_run`)

- **Launch.** The §3 command, verbatim, at 2026-11-01T01:13:06Z. The stamp was at 01:12:01Z and entry 20 at 01:12:15Z. Before
  the launch I checked: `GAP.stamp` sha256 lines verify, the chain is OK at 20 entries, there is no STOP_*, `glue/` is empty,
  and none of the four job IDs is in `done/`.
- **Runner.** `runner_gap.out` reads: `finished: pending 0, stop none` at 01:32:28Z. There is no STOP_* file.

| job | exit | wall s | peak RSS (KB) |
|---|---|---|---|
| GLUE_P | 0 | 0.18 | 28128 |
| l2_1.92364501953125_e1 | 0 | 1106.42 | 2342168 |
| nc_1.92364501953125_l2e | 0 | 121.55 | 631964 |
| GLUE_r2 | 0 | 0.50 | 28560 |

- **Budget (K-G4 not hit).** Wall time was 19 min 22 s against a 2 h limit. Compute was about 0.34 core-h against a 2 core-h
  limit. Peak RSS was 2.34 GB against a 3.0 GB job budget, and no K4g stop fired.
- **Order.** The e1 run and the control both depend only on GLUE_P, so they ran concurrently, as jobs_gap.txt allows.
- **Ladder history** (`logs/l2_1.92364501953125_e1.log`): the 3 registered FAIL records were reused, then rule E ran:

      [["1/4", "lam2hat", "FAIL"], ["1/1024", "lam2hat", "FAIL"], ["2", "2.74710710889347e-239", "FAIL"], ["1/4", "lam2hat", "e1", "PASS"]]

  grid.py renamed `REFINE_1.91912841796875_1.92364501953125` to `REFINED_…`.

## 3. Scoring per PREREG_GAP item

| item | outcome | evidence |
|---|---|---|
| **C-P** (QG2) | **holds** | GLUE_P printed the 43-step line above. No record was rejected (0 `rejected` lines). |
| **C-E** (QG1) | **holds** | `l2_1.92364501953125_1o4_e1.json`: result PASS, `failed_gates` [], all 15/15 gates true (G-S, G0-mini, G0i, V2, V3, C-τ, C-r̄, C-J_2, C-ind, G5′, C-r_M, G5, V4, R6, V5). `stamp_sha256` 7a3c6b28…. Amendment pin: 20 entries, sha256 558287d9…, which is the log including entry 20. `code_sha256` includes certify.py 0cbb7e7f…, and all 21 code hashes are identical to the grid G records and to GAP.stamp. N2 is clean: μ = 4.5717e−232 ≤ λ̂_2(M_0) = 1.8287e−231 (Fraction). The glued `g_1.92364501953125_l2.json` is byte-identical to the e1 record. |
| **C-N** (control) | **holds** | `nc_1.92364501953125_l2e.json`: result FAIL, `failed_gates` [V2] ⊆ {V2..V5}, reason `core Cholesky proposal failed`. The evaluated hard gates (G-S, G0-mini, G0i) are true and none is false. No certified bound, no STOP_G2. μ = 1.01·λ̂_2(M_0) rounded up, so μ > λ̂_2(M_0) holds exactly. |
| **C-F** (QG3) | **holds, rule-E route** | GLUE_r2 printed the 53-step line above. No record was rejected and there is no `lem:mono` line. |
| K-G1 | not triggered | The control FAILed, and there was no N2 violation. |
| K-G2 | not triggered | No hard gate was false, there was no crash, and there was no STOP_*. |
| K-G3 | not applicable | Rule E PASSed. |
| K-G4 | not triggered | See §2. |

**Outcome: the gap was closed by rule E** (C-E, C-N and C-F with GLUE_r2). The partial outcome C-P is scored on its own and holds.

**Predictions** (float; scored, never used to tune):

| id | score | detail |
|---|---|---|
| RG-1 | **HIT** | Every listed field equals D2: N 38912, M 155648, t_N 0.70569743, τ_N 1.22067, r_M 0.140106, δ_0 37/256, ε_E 9.911494025049308e−17, min pivot 0.8663379010872191, V5 margin 0.00442510, SR_fail −1, SR_checksum (T/sump/sumL), and certified ℓ_2 [4.5716755664090265288e−232 ± 1.93e−252]. μ and θ are also identical. Only run metadata differs, plus `tmin` (0.5920743125 vs D2's 0.5; both give N 38912). |
| RG-2 | **MISS** | The control FAILed at **V2** (float core Cholesky proposal) before N was set, not at V4 at N 38912. |
| RG-3 | **HIT** | 43 comparisons, minimum 2.099. |
| RG-4 | **HIT** | 53 comparisons; minimum 2.099 on [1.5, 1.5174560546875]; the gap step ratio is 448.6066 (odd-limited). |
| RG-5 | **HIT** | Fallback not needed. |

**My reading of RG-2 (unverified).** λ̂_2(M_0) is the core's own Galerkin value. So at μ > λ̂_2(M_0), the deflated, shifted core
matrix is already indefinite, and the float proposal must fail before the SR stage. The control therefore exercises the V2
path, not the SR/V4 path. It satisfies C-N as registered, but it is a weaker test of SR soundness than predicted. The SR
path's liveness rests on the grid G controls (6/6 FAIL at V4) and the 4 grid FAIL records.

## 4. Reporting rule (§7)

- **Both results stand side by side.** Grid G FAILS as registered (K3g). Under the post-hoc PREREG_GAP (rule E), the scored
  glue certifies a simple, even ground state of A_L for every L in [1.4035, 2].
- **Pending audit.** That claim waits for the fresh-agent audit of the PREREG_GAP records.
- **No further claim.** Nothing is claimed about the cause at 1.8958740234375, and nothing beyond what the glue prints. D1, D2,
  edge.py and the self-tests stay diagnostic.
- **Outcome entry (§7.4).** It is AMENDMENTS.log **entry 21** (vm3, written after all jobs finished). It holds the md5 of the
  2 new records, the REFINED_ marker, the glued e1 copy, and every new log and .rss file. The chain is OK at 21 entries,
  sha256 c9029e85…, and the log md5 is 9c0dcdb8….

## 5. Files

- **`grid_run_gap/`** is the laptop mirror of the new vm3 outputs, 230 files plus `MD5SUMS`:
  - `out/`: e1, the control, and the two REFINED_ markers.
  - `logs/`: GLUE_P, e1 (ladder + certify), nc, GLUE_r2, `.rss`, `runner_gap.out`, `runner.log`.
  - `done/`: the 4 exit codes.
  - `glue/`: the final glued set, 208 files.
  - Copies of AMENDMENTS.log, windows.txt and jobs.txt.
- **Refreshed from vm3:**
  - laptop `AMENDMENTS.log`: 21 entries, md5 9c0dcdb8…;
  - `grid/windows.txt`: md5 74e62f6d…, sha256 312401ea… (matches GAP.stamp);
  - `grid/jobs.txt`: md5 f77b5459….
- **The old `grid_run/` mirror is unchanged.** It still shows the pre-gap `REFINE_` marker.
- **Log note.** `logs/nc_1.92364501953125_l2e.log` holds the job stdout and the certify log in one file, because pilot.run and
  the runner write to the same name. A few bytes of the first line are overwritten ("tart"). The record JSON is unaffected.
