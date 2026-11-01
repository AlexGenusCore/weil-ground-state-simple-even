# PREREG_GAP (registered; stamp `GAP.stamp` on vm3): closing the λ_2 gap of grid G at 1.92364501953125

**Status.** Written 2026-11-01, after GAP_DIAG.md and before any scored run under it. It is stamped on vm3
(`~/rh60route/GAP.stamp`, read-only; copy in `highprec/lb/rh60route/GAP.stamp`). The stamp holds the md5 and sha256 of this file,
the sha256 of every executed code and job file (each also as a blob `hp/lb/rh60route/archive/<sha256>.<name>`), the sha256 of
the reused records, the AMENDMENTS.log chain check and the UTC time. AMENDMENTS.log entry 20 holds the md5 of this file and of
GAP.stamp. **This file is frozen from the stamp on.** Changes go into AMENDMENTS.log (`amend.py`), written before any result
they could affect.
- **Approval.** As stated in the workflow task: the author approved running the rh_60-route grid on vm3, and this step
  closes its one gap. vm3 only. vm1 is idle but unused, vm2 is off limits, and vm4 (Liu job) gets no compute.
- **Post hoc.** This registration was written *after* grid G failed (K3g) and after the diagnostic D2 run (GAP_DIAG) had
  passed at the new N. It is a protocol fix chosen after seeing a FAIL, and it is reported as one (§7). It changes nothing in
  grid G's registered scoring.
- **No push, publish or contact.**

**Credit.** The method is bramble_trace's (rh_60 v1, "Full-source Schur certificates for Weil positivity at support radius
two", rStation 2026-10-26) and lihongmin's (rh_45 v1, "Cutoff-free positivity of localized Weil forms through the (log 11)/2
threshold", rStation 2026-10-23). Both are unrefereed AI-agent preprints reviewed only by AI agents. Ours: general L, μ-shift,
rank-one deflation, Lemma SR, the form core, the gluing, grid G and this fix.

**Clean room.** Written from GAP_DIAG.md, RESULTS_GRID.md, VERIFY_GRID.md, PREREG_GRID.md, GRID_PLAN.md, SPEC.md, PROOFS.md,
the paper (Lemma `lem:mono`, Cor. `cor:step`), the run records and our own code. Nothing under `scratch_archive/rstation/` and
no rStation URL was opened.

**Labels** (PREREG.md): *certified* = a Theorem V PASS with every hard gate passed, decided in Arb or exact arithmetic;
*float* = forecasts, Galerkin values, proposals; *diagnostic* = reported, never scored.

## 0. What changes, and what does not

| file | change | sha256 (new) |
|---|---|---|
| `code/certify.py` | **none** | 0cbb7e7f82c4bc935e2c14be1e0381ff4932e97012d4313a54147e2b98acaa3c |
| `code/pilot.py`, sr.py, sr.c, sr_kernel, entries.py, … | **none** (as in GRID.stamp) | pilot.py e289962a… |
| `grid/run_grid.sh` | **none** | 8c0f07bd… |
| `grid/grid.py` | rule E (§2); `nc l2e` (§5); `glue` takes extra check_steps args, and a REFINE marker blocks a glue only if both of its windows are in that glue's window list | 49eefc2cd6f13807e6cc009d3b5641855c969fbe85c00bf8dbe3bad7bdd1df0a (was 94399de9…) |
| `gap/check_steps.py` | optional `--l2-from L=L*` (§4); without it the behaviour is unchanged | cc7764e933213e47c9652f8b99881abd66c5c502404c9de9449c57753c0847d0 (was 083dece7…) |
| `grid/jobs_gap.txt` | new: the 4 scored jobs of §3 | b64e3620276745913adb34fcb9f124e2f4922a437294d9ea4c4d711b8c1d79ea |
| `grid/jobs_gap_mono.txt` | new: the fallback glue of §4 (run only if §4 triggers) | 6d5c041781f3009ea382548bd20facdaaef3294918515256d9bb1fb34b361345 |
| `grid/windows_partial.txt` | new: vm3 windows.txt (md5 74e62f6d…) truncated at 1.91912841796875, 44 windows | dce63890c702fb06bc4ddc70a0a880586e9c47587bc52e61cf4061defd12a87e |

- **Gates unchanged.** Every hard gate (G-S, G0-mini, G0i, V2–V5, R6, G5, G5′, C-τ, C-r̄, C-J_2, C-r_M, C-ind), N2, F6 and the
  STOP_* logic are those of PREREG_GRID §2.3/§3, in the same code.
- **Stamp of the records.** The new runs keep `RH60_STAMP = GRID.stamp`, so they carry `stamp_sha256` = 7a3c6b28… like every
  grid record, and one `check_steps --stamp` covers the whole chain. They are bound to *this* registration through the
  amendment pin (`amendments` field): the AMENDMENTS.log state at their start has ≥ 20 entries, and entry 20 is this stamp's.
- **Self-tests before the stamp** (scratch copy of the laptop mirror, `RH60_RUN` = scratch; no certify.py run; not scored).
  - The rule-E branch with a mocked certifier: name `l2_1.92364501953125_1o4_e1`, one `--tmin` = 0.5920743125, μ-rel 1/4,
    deflated, `--sr`. On a mocked PASS the marker is renamed REFINED_ and the exit is 0; on a mocked FAIL it is kept and the
    exit is 4. `nc l2e` gets μ-rel 101/100, `--mu-up`, the same tmin, and a mocked PASS writes STOP_G2.
  - The glue paths: the partial glue proceeds despite the marker; the full glue exits 3 while it exists; the full glue after a
    rename reports `missing: l2` (52 comparisons); `--l2-from` with L* < L is refused.
  - On the mirror, the partial glue and the fallback glue print the numbers that RESULTS_GRID §7 and VERIFY_GRID had already
    published (43 steps / 2.099; 448.6 on the gap step). So no new information was seen before this registration.

## 1. Questions

1. **QG1.** Does rule E (§2) give a certified λ_2^ev lower bound at 1.92364501953125 under the unchanged gates?
2. **QG2.** Does the scored partial glue confirm grid G's registered partial outcome [1.4035, 1.91912841796875]? This closes
   deviation D1 of RESULTS_GRID.
3. **QG3.** Does the scored full chain [1.4035, 2] glue, through rule E or else through the registered fallback (§4)?

## 2. Rule E (the registered parameter fix)

**Trigger.** A window's λ_2 ladder ends without a PASS, **and** all three rung records (`l2_<L>_1o4`, `_1o1024`, `_2`) have
result FAIL with `failed_gates == ["V4"]`.

**Action.** Run exactly one extra rung, `l2_<L>_1o4_e1`, through `grid.py ladder` (so through `checked`, with K2g and N2):
- μ = ¼·λ̂_2(M_0) (`--mu-rel 1/4 --mu-ref lam2hat`), ε = +1, `--deflate`, `--sr`, all other arguments from `pilot.common`;
- `--tmin` = t_N(`l2_<L>_1o4`) + 2^−10, from that record's `t_N` field (one `--tmin` in argv).
- R4 then picks the next multiple of 1024. At 1.92364501953125: lb t_N(37888) = 0.59110 < 0.59207 ≤ lb t_N(38912) = 0.70570, and
  every N < 37888 has lb t_N < ½, so **N = 38912**. tmin enters certify.py only in the N rule and the record.
- **PASS** → N2 check, then `REFINE_<Lp>_<L>` is renamed `REFINED_<Lp>_<L>` and the ladder exits 0. **No PASS** → the marker
  stays and the exit is 4, as before.

**Why it is sound.** N is a free parameter of Theorem V (PROOFS §8): any N with t′_N > 0 is admissible, and every gate is
recomputed at the new N. The edge loss S²/t′_N only lowers S_M (T ⪯ S_FF, P19), so it causes false FAILs, never false PASSes
(GAP_DIAG §4). Choosing N after a FAIL cannot weaken a deductive certificate; it is a protocol matter, hence this file.

**Where it fires.** Only at **1.92364501953125** in grid G.
- 1.91912841796875 (L′) needs no rerun: `l2_1.91912841796875_1o4` passed on ¼ (p̂_min 0.727; sha256 838766cf…).
- 1.8958740234375 needs no rerun either: its ladder passed on 2^−10, so the trigger does not hold. That it shares the
  cause is inferred only and is not claimed.

## 3. Scored runs (vm3, in this order, after the stamp and entry 20)

**Launch.**

    cd ~/rh60route && setsid nohup bash hp/lb/rh60route/grid/run_grid.sh run $HOME/rh60route/hp/lb/rh60route/grid/jobs_gap.txt \
        > grid_run/logs/runner_gap.out 2>&1 < /dev/null &

The runner is the unchanged run_grid.sh: RH60_STAMP = GRID.stamp, RH60_AMEND = AMENDMENTS.log, memory and RSS checks, and no
launch once any STOP_* exists. The scored outputs are written to `grid_run/out/`, `grid_run/glue/` and `grid_run/logs/`.

| job | deps | command | role |
|---|---|---|---|
| GLUE_P | – | `grid.py glue $G/windows_partial.txt $RH60_STAMP` | (3b) registered partial glue [1.4035, 1.91912841796875] |
| l2_1.92364501953125_e1 | GLUE_P | `grid.py ladder l2 1.92364501953125 1.91912841796875` | (1) reuses the 3 FAIL records (cap rule of §2.5), then rule E |
| nc_1.92364501953125_l2e | GLUE_P | `grid.py nc l2e 1.92364501953125` | negative control (§5) |
| GLUE_r2 | both above | `grid.py glue $G/windows.txt $RH60_STAMP` | (3a) full chain [1.4035, 2], 54 windows (md5 74e62f6d…) |

`grid.py glue` builds `grid_run/glue/` by its registered selection rule (the first sorted PASS record per (L, kind), plus every
upper file). It then runs `check_steps.py grid_run/glue <windows> --stamp 7a3c6b28…` (F6 on every input).

**Budget.** 2 single-core certifier runs (≈ 20 min each, ≤ 2.3 GB measured, 3.0 GB job budget) and two glues of seconds each.
Stop and report if the total is over 2 h wall or 2 core-h, or if any K4g RSS stop fires.

## 4. Registered fallback (Lemma `lem:mono`), only if rule E does not PASS

**Trigger.** `l2_1.92364501953125_1o4_e1` has result FAIL (some of V2–V5 false, every hard gate true), the control met §5,
no STOP_* file exists, and GLUE_r2 exited 3 (marker still present). A STOP_*, a crash or a false hard gate is **not** a
trigger: then §5 K-G2 applies.

**Execution** (no step may be skipped or reordered):
1. Append an AMENDMENTS.log entry declaring the fallback, before any file change.
2. `mv grid_run/out/REFINE_1.91912841796875_1.92364501953125 grid_run/out/MONO_1.91912841796875_1.92364501953125`.
3. `run_grid.sh run $G/jobs_gap_mono.txt` → job GLUE_m: `grid.py glue $G/windows.txt $RH60_STAMP --l2-from
   1.92364501953125=1.9326171875`.

**Records used** (already certified under GRID.stamp sha256 7a3c6b28…, amendment pin 14 entries, every hard gate true;
re-checked by F6 with `--stamp`):

| role | record | sha256 | value (lower end) |
|---|---|---|---|
| ℓ_2 for the window 1.92364501953125 | `l2_1.9326171875_1o4.json` (next window, L_45) | 8817657b1eb1ba6451e387577150df1c3bfaf1eeb196828074dc7aad6dc1640b | 1.3019e−236 |
| ℓ_od at 1.92364501953125 | `odd_1.92364501953125_2o3.json` | 3edb63b444e4f738e9cc4ac461f3eba89b35aaa30d6e45e409ca39bfd1d0c80d | 1.232e−236 |
| U^ev(L′) | `upper_1.91912841796875_0.jsonl` | (as glued) | 2.7471e−239 |

Only this one substitution is allowed: the next window, 1.9326171875, and no other.

**The step it closes.** For x ∈ [L′, 1.92364501953125]:

λ_1^ev(x) ≤ λ_1^ev(L′) ≤ U^ev(L′) < min(ℓ_od(1.92364501953125), ℓ_2(1.9326171875)) ≤ min(λ_1^od(x), λ_2^ev(x)).

The last inequality uses λ_1^od(x) ≥ λ_1^od(1.92364501953125) (since x ≤ 1.92364501953125) and λ_2^ev(x) ≥
λ_2^ev(1.9326171875) (since x ≤ 1.9326171875), both by Lemma `lem:mono`. Then paper Cor. `cor:criterion` applies. check_steps
implements it by reading the l2 bound at 1.92364501953125 from `g_1.9326171875_l2.json` (F6 against L* = 1.9326171875,
with L* > L asserted).

**Proof sketch of `lem:mono` in the even sector** (paper Lemma `lem:mono`; this is the min-max argument the step test already
uses). Let 0 < L < L′.
1. Extension by zero, ι: L²(−L, L) → L²(−L′, L′), is an isometry, and it maps even functions to even functions.
2. It maps C_c^∞(−L, L) into C_c^∞(−L′, L′), and Q_{L′}(ιf) = Q_L(f):
   - the pole and archimedean terms depend only on F = f̂, which ι does not change;
   - a prime power with 2L ≤ log n < 2L′ contributes g(log n) = 0, since g = f∗f̃ is continuous, supported in [−2L, 2L]
     and vanishes at ±2L.
   So ι is form-isometric on the core, and it extends to the form domains: ι𝒟_L^ev ⊂ 𝒟_{L′}^ev.
3. For any k-dimensional V ⊂ 𝒟_L^ev, ιV is a k-dimensional subspace of 𝒟_{L′}^ev with the same Rayleigh quotients. The
   min-max infimum for λ_k^ev(L′) runs over a family that contains every ιV, so λ_k^ev(L′) ≤ λ_k^ev(L) (k = 2 here).
4. With Theorem V for ϑ > 0 (PROOFS §8, deflation): λ_2^ev(L*) ≥ μ ≥ ℓ_2(L*). Hence λ_2^ev(L) ≥ ℓ_2(L*) for every L ≤ L*.

## 5. Pass/fail criteria and the negative control

**Negative control** (`nc_1.92364501953125_l2e`). Same window and the rule-E parameters (deflated, ε = +1, the same tmin, so
N = 38912 expected), with μ = 1.01·λ̂_2(M_0) rounded **up** (`--mu-up`). This μ is above the Galerkin value λ̂_2(M_0), which is ≥
λ_2^ev(L) by min-max (float; its error is far below the 1 % margin). So a sound certifier must FAIL. It runs whatever the rule-E outcome is.

| id | criterion |
|---|---|
| C-P | GLUE_P prints `ALL STEPS PASS (43 comparisons): simple-even on [1.4035, 1.91912841796875]`, with no rejected record |
| C-E | `l2_1.92364501953125_1o4_e1`: result PASS, `failed_gates` [], all 15 gates true; stamp_sha256 = 7a3c6b28…; amendment pin ≥ 20 entries, and its log prefix contains entry 20 (this stamp); certify.py 0cbb7e7f… in `code_sha256`; N2 clean (μ ≤ λ̂_2(M_0)) |
| C-N | the control: result FAIL with `failed_gates` ⊆ {V2, V3, V4, V5}, no hard gate false, no certified lower bound, no STOP_G2 |
| C-F | GLUE_r2 (rule-E route) or GLUE_m (fallback route) prints `ALL STEPS PASS (53 comparisons): simple-even on [1.4035, 2]`, with no rejected record |

**Outcomes.**
- **Gap closed by rule E:** C-E, C-N and C-F (GLUE_r2).
- **Gap closed by the fallback:** e1 FAIL (the §4 trigger), C-N and C-F (GLUE_m).
- **Partial outcome scored:** C-P. It is scored independently of the other three.

**Kill criteria.**

| id | criterion | consequence |
|---|---|---|
| K-G1 | the control PASSes (STOP_G2), or any N2 violation | VOID every result of this registration, *including* C-P, and of grid G (as K1g); no claim |
| K-G2 | any hard gate false, a crash, or any other STOP_* in the e1 run or the control | stop; no gap closure and no fallback until a diagnosis is logged as an amendment; C-P stands only if it held before |
| K-G3 | rule E FAILs and GLUE_m does not print ALL STEPS PASS (53) | gap not closed; the claim is C-P only |
| K-G4 | over 2 h wall or 2 core-h on vm3 | stop and report (budget) |

## 6. Registered predictions (from D2 and the diagnostic glue; scored HIT/MISS, never used to tune)

| id | prediction | HIT if |
|---|---|---|
| RG-1 | e1 equals D2 bit for bit: N 38912, M 155648, t_N 0.70569743, τ_N 1.22067, r_M 0.140106, δ_0 37/256, ε_E 9.911494025049308e−17, min pivot 0.8663379010872191, V5 margin 0.00442510, SR_fail −1, SR_checksum T 13c7013111f097ad767aa29143793131 / sump 4adb89d2a90bba8fdf86a47ea2f85 / sumL −45de0e820bcd28357b6585d28ba4, certified ℓ_2 = [4.5716755664090265288e−232 ± 1.93e−252] | every field equal |
| RG-2 | the control FAILs at V4 only, at N 38912 | yes |
| RG-3 | GLUE_P: 43 comparisons, minimum step ratio 2.099 | yes |
| RG-4 | GLUE_r2: 53 comparisons, minimum 2.099 on [1.5, 1.5174560546875]; the step [1.91912841796875, 1.92364501953125] has ratio 4.49e+2 (448.6), odd-limited | all |
| RG-5 | the fallback is not needed | e1 PASS |

## 7. Reporting rule

1. **Both results are reported.**
   - (a) **Grid G as registered:** it FAILS (K3g). That verdict and the PREREG_GRID R-scores do not change. The
     partial outcome [1.4035, 1.91912841796875] (43 steps) is now scored by GLUE_P (C-P).
   - (b) **The gap closure under PREREG_GAP:** stated as a post-hoc registered fix, written after the grid failure and after
     the D2 diagnostic. The report names the route (rule E or the `lem:mono` fallback).
2. **No claim beyond what the scored glue prints.** "Simple, even ground state of A_L for every L in [1.4035, 2]" is claimed
   only on C-F (with C-N, and C-E on the rule-E route). Otherwise only the span C-P prints is claimed. In particular:
   - nothing is claimed about the cause at 1.8958740234375;
   - D1, D2, edge.py and the self-tests are diagnostic;
   - the RG predictions are float.
3. **Audit before any claim.** A fresh-agent audit of the PREREG_GAP records (the PREREG_GRID §4 step 9 pattern) comes before
   any claim. The imported trust is the same as RESULTS_GRID §9.
4. **Outcome entry.** An AMENDMENTS.log entry with the md5 of every new record and log, written after the jobs finish.

## 8. Limits and choices not made

- **No new G4 mutation.** GAP_DIAG suggested one that drops the last-pivot check. It would need a certify.py/sr.c hook, and
  certify.py stays unchanged. The liveness of that check is shown instead by the 4 grid FAIL records and D1, which all fail at
  label n − 1.
- **Rule E is tested at one window only** (D2). t_min = 1 for all λ_2 runs and a generic N-retry inside certify.py were not
  chosen (GAP_DIAG §5).
- **D2 is not a record.** It ran on patched code with no stamp, so the e1 run must produce the certificate on its own.
