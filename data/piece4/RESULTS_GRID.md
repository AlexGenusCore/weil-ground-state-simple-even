# RESULTS_GRID: rh_60-route grid G on [1.4035, 2] (simple-even ground state by the step test)

**Credit.** The method is bramble_trace's (rh_60 v1, "Full-source Schur certificates for Weil positivity at support radius
two", rStation 2026-10-26) and lihongmin's (rh_45 v1, "Cutoff-free positivity of localized Weil forms through the (log 11)/2
threshold", rStation 2026-10-23). Both are unrefereed AI-agent preprints reviewed only by AI agents. Ours: general L, μ-shift,
rank-one deflation, Lemma SR, the form core, the gluing and this grid. Reused: Elston's MIT code, our stage S, fr_sweep U(L)
and the G6 auditor's `mp_entries.py`.

**Stamps.** Pre-commitment `PREREG_GRID.stamp` (vm4, 2026-10-31T16:23:27Z, sha256 3982e0bf…; PREREG_GRID.md md5
64a84a7f…). Run-time `GRID.stamp` (vm3, 2026-10-31 16:28:47 UTC, sha256 **7a3c6b287f840aba50fc11d49e6f919eb0cb758a6a0ce03e6248298feda4b9e8**),
which every run record carries as `stamp_sha256`. Canonical AMENDMENTS.log: vm3 `~/rh60route/AMENDMENTS.log`, 17 entries,
chain OK (`amend.py --verify`), sha256 166e7821…; entries 14–17 are quoted in §4.

**Status (2026-11-01, written on the laptop from the mirror).** Every registered job has run: 372 jobs (362 registered + 10
refinement jobs `_r1`), exit codes 368 × 0, 2 × 3 (GLUE, GLUE_r1), 2 × 4 (the two λ_2 ladders at 1.92364501953125); no
`STOP_*` file on vm3 or in the mirror. **Grid G does not pass.** The partial outcome below is *certified* in the PREREG sense
only **pending the fresh-agent audit (PREREG_GRID §4 step 9)** and the formal-glue question in deviation D1. No claim before
that. No push, publish or contact.

**Clean room.** Written from PREREG_GRID.md, GRID_PLAN.md, the run records, the grid scripts and our own code. Nothing under
`scratch_archive/rstation/` and no rStation URL was opened.

**Labels** (PREREG.md): *certified* = a Theorem V PASS with every hard gate passed, decided in Arb or exact arithmetic;
*float* = forecasts, Galerkin values, proposals; *diagnostic* = reported, never scored.

## 1. Headline

- **Verdict: grid G FAILS as registered (K3g).** Step 43, [1.91455078125, 1.92364501953125], had no certified λ_2 lower bound
  at 1.92364501953125. The one registered refinement (L′ = 1.91912841796875 = 31443/2^14) split it; the new left sub-step passes
  (ratio 470), but the right sub-step [1.91912841796875, 1.92364501953125] still has no λ_2 bound. PREREG_GRID §2.5 allows one
  refinement level per step, so K3g applies: *grid G is not viable as registered.*
- **It was never a ratio failure.** All three λ_2 rungs at 1.92364501953125 (¼·λ̂_2(M_0), 2^−10·λ̂_2(M_0), and
  2·U^ev(1.91455078125) = 1.0316e−236) FAIL at V4 only: every hard gate true, V5 margin > 0, float p̂_min −0.643 / −0.133 /
  −0.132, Lemma SR failing at label 37375 of 37376 (the last one) each time (N 37888, M 151552). p̂_min levels off near −0.13
  as μ → 0, so no μ passes there with these certifier parameters. The odd ladder at that window passed on ⅔.
- **Registered partial outcome (§5): coverage [1.4035, 1.91912841796875].** S1g fails and S2g–S6g hold (§2), so the only
  claim is the longest run of consecutive passing steps from L_0: **43 steps, [1.4035, 1.91912841796875]**, a simple, even
  ground state of A_L for every L in it (paper Cor. `cor:step` with Lemma `lem:mono`). It is *certified* only pending the
  §4 step 9 audit, and it rests on a diagnostic glue (D1).
- **Reported, not claimed:** the 9 steps [1.92364501953125, 2] all pass (ratios 2.22–2.41).
- **Post hoc (diagnostic, section 7 below):** the unregistered monotone-λ_2 lever would close the gap with records already certified
  (ratio 448.6 on the refined sub-step). This needs an amendment and does not change K3g.
- **Minimum step ratio 2.099** at [1.5, 1.5174560546875] (odd-bound limited), over 52 passing comparisons. This is from the
  diagnostic check_steps (D1), since the scored glue never ran check_steps.
- **Cross-check (PREREG_GRID §7; section 5 below):** X1 holds at all 8 compared (L, kind) pairs. Ours/Elston is 0.764–0.775 (odd) and 0.314–0.322 (λ_2). The
  1.5 Elston records are pending (the vm2 rerun is in progress).

## 2. Mechanical scoring

### Success criteria (§5)

| id | criterion | outcome | evidence |
|---|---|---|---|
| S1g | check_steps "ALL STEPS PASS" with 52 (+1 per refinement) comparisons | **FAIL** | Scored glue GLUE_r1 exit 3, verbatim: `refinement pending, not glued: REFINE_1.91912841796875_1.92364501953125` (GLUE before it: `… REFINE_1.91455078125_1.92364501953125`). Diagnostic check_steps (D1): 52 comparisons pass, 1 missing (`[1.91912841796875, 1.92364501953125]  missing: l2`), `NOT (yet) certified on [1.4035, 2]` |
| S2g | every glued record passes F6, every hard gate true; T15 holds | **holds** (on the diagnostic glue set) | No glued set exists formally (D1). Diagnostic glue, 105 PASS records (53 odd, 52 λ_2): check_steps `--stamp 7a3c6b28…` rejected none. All 115 non-mutation certifier records (53 odd, 56 λ_2, 6 G2): every hard gate of grid.py's HARD set true, no CRASH. T15 log `T-1.5: identical to the FIXES records` |
| S3g | all 6 G2 controls FAIL at V2–V5, no hard gate false | **holds** | 6/6 FAIL with failed_gates = [V4] only; SR first failure at labels 923, 1001 (1.447), 601, 611 (1.747…), 716, 740 (1.992…) |
| S4g | G4 at 1.5: all 15 mutations caught | **holds** | `out/G4_1.5.json`: 15/15 caught (9 registered, 3 auditor, pp_drop, lam_n, gen2K) |
| S5g | P0 passes; G0 passes at every window | **holds** | `P0_G3.json` passed (T2/T3/P13/P20/SR_D4/SR_D8). G0: 53/53 windows (1–53, incl. L′), every entry ok, mut null |
| S6g | N2 clean; no STOP_* file | **holds** | Rechecked here: μ ≤ U^od(L) on all 53 odd PASS, μ ≤ λ̂_2(M_0) on all 52 λ_2 PASS. No STOP_* on vm3 (checked 2026-11-01) or in the mirror |

**Grid verdict: no PASS.** **Partial outcome applies:** [1.4035, 1.91912841796875].

### Kill criteria (§6)

| id | triggered? | evidence |
|---|---|---|
| K1g | no | no G2 PASS, no N2 violation, no STOP_G2 / STOP_N2 |
| K2g | no | no hard gate false, no crash, exit codes only 0/3/4, no STOP_GATE / STOP_EXIT_* |
| **K3g** | **yes** | refined step [1.91912841796875, 1.92364501953125] has no PASS (λ_2 ladder at 1.92364501953125 exit 4 after reusing its 3 FAIL records); AMENDMENTS.log entry 16 |
| K4g | no | max peak RSS / budget = 0.88 (`l2_1.5`, 1.23 of 1.4 GB); no job over budget; no STOP_RSS / STOP_MEM |
| K5g | no | 87.4 core-h (vm3, GNU time wall × CPU) < 150; 7 h 27 min runner wall (6 h 35 min + 52 min), 7 h 35 min elapsed < 24 h |
| K6g | no | P0 passed; T15 identical |
| K7g | no | 15/15 G4 mutations caught |
| K8g | no | G0 passed at 53/53 windows |
| K9g | no | 1 refinement of 6 |

### Registered predictions (§8; float, never used to tune)

| id | prediction | score | detail |
|---|---|---|---|
| R-1g | no refinement | **MISS** | 1 refinement (step 43) |
| R-2g | every odd ladder on ⅔, every λ_2 ladder on ¼ | **MISS** | odd 53/53 on ⅔; λ_2 51/53 on ¼: 1.8958740234375 passed on 2^−10 (¼ FAIL at V4), 1.92364501953125 no PASS |
| R-3g | minimum check_steps ratio ≥ 1.5 (forecast 2.1) | **not scorable** | no scored check_steps run (D1); the diagnostic minimum 2.099 would be a HIT |
| R-4g | N per run within ±10 % of the GRID_PLAN model | **MISS** | 35 of 115 runs outside (N/model 0.88–1.33); 33 above (mostly one 1024 step above the model at small N), 2 below (G2 at 1.992…, 67584 vs 76800) |
| R-5g | per-run wall within ×1.5 of the model; total ±30 % of 74.5 core-h | **MISS** | certifier runs: 9/115 outside (×1.50–1.70, all at L ≤ 1.535, where fixed cost dominates); U jobs: 12/98 outside (×1.64–1.70 for 8 K = 896 jobs above 1.96; ×0.63–0.66 for 4); stage S 24/51 outside (×0.83–2.12). Total 87.4 vm3 core-h is +17 %, inside the ±30 % band, but it is not converted to vm4-equivalent |
| R-6g | every job's peak RSS ≤ its budget | **HIT** | 372/372 (max ratio 0.88) |
| R-7g | every new U passes the radius rule at the registered prec | **HIT** | 98/98 new rows (96 + 2 at L′), max (upper − mid)/mid = 1.05e−13 ≤ 1e−10; no rerun |
| R-8g | X2 odd ratio ∈ [0.62, 0.70] | **MISS** | 0.764–0.775 at all 4 windows. Cause: U^od(K = 640) is 14.6–16.3 % above Elston's λ_1^od mid, where plan.py assumed 1–2 % (§5) |
| R-9g | T15 bit-identical | **HIT** | every registered T15 field equal, and every other field equal except run-specific ones (label, seconds, peak_gb, argv, utc, log, code map, archive, amendment pin, stamp, SR_seconds, proj_SR_hours) |

Score: 3 HIT (R-6g, R-7g, R-9g), 5 MISS, 1 not scorable.

**Q2 (losses).** ℓ_odd = U^od/μ_od = 1.5 at all 53 windows (⅔ rung). ℓ_2 = λ̂_2(M_0)/μ_2 = 4 at 51 windows, 1024 at
1.8958740234375, and none at 1.92364501953125. One fallback rung (λ_2 at 1.8958740234375) and one refinement were needed.
On the overlap the true odd loss is about 1.30, since U^od there is about 15 % above λ_1^od (§5).

## 3. Windows (current windows.txt on vm3: 54 windows, 53 steps, md5 74e62f6dc210e167d8147026ce53df5d)

- **Bounds.** Lower bounds are the lower ends of the certified Arb balls, to 4 digits; the exact balls are in
  `grid_run/out/{odd,l2}_<L>_<rung>.json`.
- **U.** U^ev and U^od are the minimum lam0_upper over `grid_run/upper/*.jsonl`. "c" means a seeded certified file (upper640
  K 640; upper_k384; upper_rerun_L2 K 1024; upper_1.5_1 K 512). New U: K 640/768/896 and prec 3000/4000/6000 per §2.2; L′ uses
  K 768, prec 6000.
- **Step ratio.** The step ratio into L is min(ℓ_od, ℓ_2)(L)/U^ev(L_prev), from the diagnostic check_steps (D1).
- **Rungs.** "2U" is the λ_2 rung 3, μ = 2·U^ev(L_prev).
- **Run times.** run s and peak GB are the certifier record's `seconds` and `peak_gb` (ru_maxrss of the certifier process),
  per rung in ladder order. U jobs gives GNU time wall s and peak GiB per job, ev/od.

| i | L | U^ev(L) | U^od(L) | odd rungs | **ℓ_od lower bound** | λ_2 rungs | **ℓ_2 lower bound** | step ratio into L | N odd | N λ_2 | run s odd | run s λ_2 | peak GB odd | peak GB λ_2 | U jobs wall s (ev/od) | U jobs peak GiB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.4035 | 2.4927e-78 c | — | — | — | — | — | — | — | — | — | — | — | — | seed | — |
| 1 | 1.41473388671875 | 2.4325e-80 | 4.0903e-76 | ⅔ PASS | 2.727e-76 | ¼ PASS | 9.581e-73 | 1.09e+2 | 3072 | 3072 | 193 | 210 | 1.18 | 1.22 | 815/823 | 1.23/1.23 |
| 2 | 1.4255 | 2.3703e-82 c | 4.1442e-78 | ⅔ PASS | 2.763e-78 | ¼ PASS | 1.069e-74 | 1.14e+2 | 4096 | 3072 | 202 | 230 | 1.18 | 1.22 | seed/984 | 1.23 |
| 3 | 1.4366455078125 | 2.1453e-84 | 3.9469e-80 | ⅔ PASS | 2.631e-80 | ¼ PASS | 9.514e-77 | 1.11e+2 | 4096 | 3072 | 207 | 226 | 1.21 | 1.25 | 1014/1003 | 1.23/1.22 |
| 4 | 1.447 | 2.1066e-86 c | 3.7685e-82 | ⅔ PASS | 2.512e-82 | ¼ PASS | 1.102e-78 | 1.17e+2 | 4096 | 4096 | 224 | 244 | 1.21 | 1.26 | seed/1013 | 1.23 |
| 5 | 1.4576416015625 | 1.8351e-88 | 3.5850e-84 | ⅔ PASS | 2.390e-84 | ¼ PASS | 9.629e-81 | 1.13e+2 | 4096 | 4096 | 206 | 247 | 1.21 | 1.26 | 1022/1034 | 1.22/1.23 |
| 6 | 1.468 | 1.7399e-90 c | 3.2485e-86 | ⅔ PASS | 2.166e-86 | ¼ PASS | 9.056e-83 | 1.18e+2 | 4096 | 4096 | 215 | 265 | 1.22 | 1.27 | seed/1013 | 1.23 |
| 7 | 1.478271484375 | 1.2498e-92 | 2.8368e-88 | ⅔ PASS | 1.891e-88 | ¼ PASS | 9.330e-85 | 1.09e+2 | 5120 | 4096 | 228 | 252 | 1.23 | 1.26 | 907/1002 | 1.23/1.23 |
| 8 | 1.4885 | 1.0835e-94 c | 2.2749e-90 | ⅔ PASS | 1.517e-90 | ¼ PASS | 6.791e-87 | 1.21e+2 | 5120 | 4096 | 172 | 213 | 1.23 | 1.27 | seed/785 | 1.23 |
| 9 | 1.5 | 3.8511e-97 c | 8.2178e-93 c | ⅔ PASS | 5.479e-93 | ¼ PASS | 2.736e-89 | 50.6 | 5120 | 4096 | 175 | 197 | 1.26 | 1.29 | seed | — |
| 10 | 1.5174560546875 | 5.1710e-101 | 1.2123e-96 | ⅔ PASS | 8.082e-97 | ¼ PASS | 4.814e-93 | 2.10 | 6144 | 5120 | 221 | 282 | 1.26 | 1.31 | 1213/1177 | 1.58/1.58 |
| 11 | 1.53466796875 | 6.9895e-105 | 1.7903e-100 | ⅔ PASS | 1.194e-100 | ¼ PASS | 7.206e-97 | 2.31 | 6144 | 5120 | 244 | 279 | 1.27 | 1.31 | 1284/1278 | 1.58/1.58 |
| 12 | 1.5511474609375 | 9.6804e-109 | 2.4628e-104 | ⅔ PASS | 1.642e-104 | ¼ PASS | 1.023e-100 | 2.35 | 6144 | 6144 | 235 | 299 | 1.27 | 1.33 | 1265/1279 | 1.58/1.58 |
| 13 | 1.5672607421875 | 1.0835e-112 | 3.3374e-108 | ⅔ PASS | 2.225e-108 | ¼ PASS | 1.462e-104 | 2.30 | 7168 | 6144 | 244 | 289 | 1.3 | 1.35 | 1289/1304 | 1.58/1.58 |
| 14 | 1.58306884765625 | 1.1771e-116 | 3.9222e-112 | ⅔ PASS | 2.615e-112 | ¼ PASS | 1.839e-108 | 2.41 | 7168 | 7168 | 201 | 320 | 1.31 | 1.37 | 1258/1290 | 1.58/1.58 |
| 15 | 1.5986328125 | 1.1183e-120 | 4.0625e-116 | ⅔ PASS | 2.708e-116 | ¼ PASS | 2.152e-112 | 2.30 | 8192 | 7168 | 214 | 311 | 1.32 | 1.37 | 1089/1261 | 1.58/1.58 |
| 16 | 1.61376953125 | 1.0511e-124 | 3.9681e-120 | ⅔ PASS | 2.645e-120 | ¼ PASS | 2.316e-116 | 2.37 | 9216 | 8192 | 254 | 319 | 1.36 | 1.42 | 1199/1189 | 1.58/1.58 |
| 17 | 1.62847900390625 | 8.6526e-129 | 3.6198e-124 | ⅔ PASS | 2.413e-124 | ¼ PASS | 2.356e-120 | 2.30 | 9216 | 8192 | 256 | 335 | 1.36 | 1.42 | 1220/1194 | 1.59/1.59 |
| 18 | 1.642822265625 | 7.4414e-133 | 3.0509e-128 | ⅔ PASS | 2.034e-128 | ¼ PASS | 2.084e-124 | 2.35 | 10240 | 9216 | 275 | 355 | 1.37 | 1.43 | 1196/1224 | 1.59/1.58 |
| 19 | 1.65692138671875 | 6.3062e-137 | 2.7080e-132 | ⅔ PASS | 1.805e-132 | ¼ PASS | 1.847e-128 | 2.43 | 10240 | 9216 | 251 | 337 | 1.39 | 1.46 | 1213/1064 | 1.58/1.59 |
| 20 | 1.6705322265625 | 5.0100e-141 | 2.1850e-136 | ⅔ PASS | 1.457e-136 | ¼ PASS | 1.618e-132 | 2.31 | 11264 | 10240 | 256 | 354 | 1.41 | 1.47 | 1211/1210 | 1.58/1.59 |
| 21 | 1.6839599609375 | 3.7428e-145 | 1.8222e-140 | ⅔ PASS | 1.215e-140 | ¼ PASS | 1.393e-136 | 2.42 | 12288 | 11264 | 281 | 400 | 1.42 | 1.49 | 1208/1208 | 1.58/1.58 |
| 22 | 1.69708251953125 | 2.4560e-149 | 1.2961e-144 | ⅔ PASS | 8.640e-145 | ¼ PASS | 1.053e-140 | 2.31 | 13312 | 11264 | 316 | 376 | 1.47 | 1.52 | 1196/1208 | 1.58/1.58 |
| 23 | 1.71002197265625 | 1.5541e-153 | 8.4723e-149 | ⅔ PASS | 5.648e-149 | ¼ PASS | 7.392e-145 | 2.30 | 14336 | 12288 | 298 | 387 | 1.49 | 1.54 | 1057/1125 | 1.58/1.58 |
| 24 | 1.7225341796875 | 9.9942e-158 | 5.5374e-153 | ⅔ PASS | 3.692e-153 | ¼ PASS | 5.610e-149 | 2.38 | 15360 | 13312 | 317 | 434 | 1.51 | 1.56 | 864/892 | 1.58/1.58 |
| 25 | 1.73504638671875 | 5.6174e-162 | 3.4747e-157 | ⅔ PASS | 2.316e-157 | ¼ PASS | 3.363e-153 | 2.32 | 15360 | 14336 | 336 | 460 | 1.53 | 1.59 | 951/958 | 1.58/1.59 |
| 26 | 1.74713134765625 | 3.3011e-166 | 1.9796e-161 | ⅔ PASS | 1.320e-161 | ¼ PASS | 1.883e-157 | 2.35 | 16384 | 15360 | 344 | 460 | 1.55 | 1.61 | 1046/866 | 1.58/1.58 |
| 27 | 1.759033203125 | 1.6634e-170 | 1.1561e-165 | ⅔ PASS | 7.707e-166 | ¼ PASS | 1.164e-161 | 2.33 | 17408 | 15360 | 351 | 478 | 1.57 | 1.62 | 1747/1729 | 2.39/2.39 |
| 28 | 1.770751953125 | 7.9149e-175 | 5.9152e-170 | ⅔ PASS | 3.943e-170 | ¼ PASS | 6.767e-166 | 2.37 | 19456 | 16384 | 389 | 502 | 1.62 | 1.67 | 1523/1664 | 2.39/2.39 |
| 29 | 1.78216552734375 | 3.9774e-179 | 2.8723e-174 | ⅔ PASS | 1.915e-174 | ¼ PASS | 3.517e-170 | 2.42 | 20480 | 17408 | 464 | 525 | 1.63 | 1.69 | 1568/1568 | 2.39/2.38 |
| 30 | 1.7933349609375 | 1.9662e-183 | 1.4319e-178 | ⅔ PASS | 9.546e-179 | ¼ PASS | 1.943e-174 | 2.40 | 21504 | 18432 | 427 | 564 | 1.64 | 1.71 | 1539/1457 | 2.39/2.39 |
| 31 | 1.80438232421875 | 8.7062e-188 | 6.8169e-183 | ⅔ PASS | 4.545e-183 | ¼ PASS | 8.955e-179 | 2.31 | 22528 | 19456 | 458 | 604 | 1.7 | 1.75 | 1441/1475 | 2.39/2.38 |
| 32 | 1.81524658203125 | 3.8232e-192 | 3.1457e-187 | ⅔ PASS | 2.097e-187 | ¼ PASS | 4.231e-183 | 2.41 | 23552 | 21504 | 519 | 644 | 1.7 | 1.8 | 2244/1426 | 2.38/2.38 |
| 33 | 1.825927734375 | 1.4064e-196 | 1.3216e-191 | ⅔ PASS | 8.811e-192 | ¼ PASS | 2.025e-187 | 2.30 | 25600 | 22528 | 583 | 697 | 1.75 | 1.82 | 2264/2169 | 2.38/2.38 |
| 34 | 1.83642578125 | 5.0279e-201 | 4.8240e-196 | ⅔ PASS | 3.216e-196 | ¼ PASS | 8.126e-192 | 2.29 | 26624 | 23552 | 533 | 738 | 1.79 | 1.86 | 2924/2965 | 3.42/3.39 |
| 35 | 1.8468017578125 | 1.9136e-205 | 1.7340e-200 | ⅔ PASS | 1.156e-200 | ¼ PASS | 2.811e-196 | 2.30 | 27648 | 24576 | 551 | 772 | 1.8 | 1.91 | 2518/2500 | 3.42/3.42 |
| 36 | 1.85687255859375 | 6.9741e-210 | 6.8787e-205 | ⅔ PASS | 4.586e-205 | ¼ PASS | 1.219e-200 | 2.40 | 30720 | 26624 | 635 | 832 | 1.81 | 1.91 | 2652/2648 | 3.42/3.41 |
| 37 | 1.86688232421875 | 2.2779e-214 | 2.4176e-209 | ⅔ PASS | 1.612e-209 | ¼ PASS | 4.568e-205 | 2.31 | 31744 | 27648 | 671 | 895 | 1.85 | 1.95 | 2653/2641 | 3.41/3.39 |
| 38 | 1.87664794921875 | 6.8020e-219 | 7.5219e-214 | ⅔ PASS | 5.015e-214 | ¼ PASS | 1.580e-209 | 2.20 | 32768 | 28672 | 745 | 905 | 1.84 | 1.96 | 2653/2647 | 3.42/3.39 |
| 39 | 1.8863525390625 | 2.2027e-223 | 2.4867e-218 | ⅔ PASS | 1.658e-218 | ¼ PASS | 5.265e-214 | 2.44 | 34816 | 30720 | 767 | 1115 | 1.85 | 1.97 | 2577/2619 | 3.42/3.39 |
| 40 | 1.8958740234375 | 6.7489e-228 | 8.2188e-223 | ⅔ PASS | 5.479e-223 | ¼ FAIL → 2⁻¹⁰ PASS | 6.678e-221 | 2.49 | 36864 | 32768/31744 | 799 | 1192/870 | 1.91 | 2.06/2.02 | 2584/2578 | 3.39/3.39 |
| 41 | 1.9052734375 | 1.9104e-232 | 2.3180e-227 | ⅔ PASS | 1.545e-227 | ¼ PASS | 5.446e-223 | 2.29 | 38912 | 33792 | 979 | 1244 | 1.97 | 2.12 | 2618/2618 | 3.42/3.42 |
| 42 | 1.91455078125 | 5.1581e-237 | 6.6336e-232 | ⅔ PASS | 4.422e-232 | ¼ PASS | 1.662e-227 | 2.31 | 40960 | 35840 | 934 | 1307 | 2.05 | 2.2 | 2614/2628 | 3.40/3.37 |
| 43 | 1.91912841796875 | 2.7471e-239 | 3.6361e-234 | ⅔ PASS | 2.424e-234 | ¼ PASS | 8.622e-230 | 4.70e+2 | 41984 | 36864 | 766 | 1037 | 2.09 | 2.27 | 2064/2058 | 3.40/3.38 |
| 44 | 1.92364501953125 | 1.4208e-241 | 1.8486e-236 | ⅔ PASS | 1.232e-236 | ¼ FAIL → 2⁻¹⁰ FAIL → 2U FAIL | **none** | missing l2 | 43008 | 37888/37888/37888 | 1003 | 1386/1266/1082 | 2.12 | 2.3/2.3/2.3 | 3559/3573 | 4.64/4.64 |
| 45 | 1.9326171875 | 3.6543e-246 | 5.0868e-241 | ⅔ PASS | 3.391e-241 | ¼ PASS | 1.302e-236 | 2.39 | 46080 | 39936 | 1095 | 1525 | 2.31 | 2.45 | 3825/3831 | 4.63/4.63 |
| 46 | 1.94146728515625 | 8.7242e-251 | 1.2167e-245 | ⅔ PASS | 8.112e-246 | ¼ PASS | 3.477e-241 | 2.22 | 48128 | 41984 | 1168 | 1630 | 2.37 | 2.55 | 3897/3884 | 4.63/4.63 |
| 47 | 1.95013427734375 | 1.9466e-255 | 2.9375e-250 | ⅔ PASS | 1.958e-250 | ¼ PASS | 9.753e-246 | 2.24 | 51200 | 44032 | 1314 | 1799 | 2.46 | 2.64 | 3926/3895 | 4.63/4.63 |
| 48 | 1.958740234375 | 4.5868e-260 | 6.7472e-255 | ⅔ PASS | 4.498e-255 | ¼ PASS | 2.122e-250 | 2.31 | 54272 | 46080 | 1413 | 1799 | 2.61 | 2.76 | 3897/3976 | 4.62/4.61 |
| 49 | 1.96722412109375 | 1.0466e-264 | 1.6588e-259 | ⅔ PASS | 1.106e-259 | ¼ PASS | 5.273e-255 | 2.41 | 56320 | 48128 | 1463 | 1939 | 2.66 | 2.85 | 5389/5357 | 4.62/4.61 |
| 50 | 1.9755859375 | 2.2692e-269 | 3.5978e-264 | ⅔ PASS | 2.399e-264 | ¼ PASS | 1.323e-259 | 2.29 | 59392 | 51200 | 1594 | 2056 | 2.82 | 2.98 | 5433/5579 | 4.61/4.62 |
| 51 | 1.98382568359375 | 4.6644e-274 | 7.6874e-269 | ⅔ PASS | 5.125e-269 | ¼ PASS | 3.010e-264 | 2.26 | 62464 | 53248 | 1742 | 2259 | 3.07 | 3.16 | 5536/5553 | 4.62/4.61 |
| 52 | 1.99200439453125 | 9.2322e-279 | 1.6120e-273 | ⅔ PASS | 1.075e-273 | ¼ PASS | 6.330e-269 | 2.30 | 66560 | 56320 | 1929 | 2444 | 3.26 | 3.31 | 5436/5450 | 4.62/4.62 |
| 53 | 2 | 1.8468e-283 c | 3.2382e-278 c | ⅔ PASS | 2.159e-278 | ¼ PASS | 1.365e-273 | 2.34 | 69632 | 58368 | 2134 | 2630 | 3.4 | 3.43 | seed | — |

Window 44 had two ladder jobs per kind: the r1 ladders at 1.92364501953125 (L_prev = L′) reused the existing records
(wall 0.05 s each), so there are no new runs there. Its step ratio is missing because there is no λ_2 bound; the step into
window 45 uses U^ev(1.92364501953125) and passes.

## 4. Refinement record

| step | trigger | L′ | outcome |
|---|---|---|---|
| 43: [1.91455078125, 1.92364501953125] | job `l2_1.92364501953125` exit 4 (ladder ended without PASS), marker `REFINE_1.91455078125_1.92364501953125` (kind l2) | 1.91912841796875 = 31443/2^14 (nearest dyadic to ½·log((e^{2L_i}+e^{2L_{i+1}})/2) = 1.91911857640); min \|2L′ − log n\| = 0.0119 | [1.91455078125, L′]: PASS, ratio 470 (odd ⅔ PASS, λ_2 ¼ PASS at L′, p̂_min 0.616 / 0.727). [L′, 1.92364501953125]: no λ_2 PASS. `l2_1.92364501953125_r1` reused its 3 FAIL records (cap reached), exit 4, marker `REFINE_1.91912841796875_1.92364501953125`, left in place. K3g |

**Execution as §2.5 requires.**
1. Entry 15 was logged before any file change.
2. L′ was inserted into windows.txt (md5 1beaea14… → 74e62f6d…).
3. 10 `_r1` lines were appended to jobs.txt (md5 12bd6f01… → f77b5459…).
4. The marker was renamed `REFINED_1.91455078125_1.92364501953125`.
5. The runner was restarted under setsid nohup at 23:11:30Z and finished at 00:03:43Z with no STOP file.

At L′: U0/U1 exit 0 (wall 2064/2058 s, peak 3.40/3.38 GiB, radius 9.8e−14/9.9e−14). S, R and G0 exit 0. Refinements used:
1 of 6.

**Amendments since the pre-commitment stamp (verbatim, canonical vm3 log).** Entries 1–13 are pre-stamp (planning and
review; see the laptop copy, which is vm4's frozen log at 13 entries).

> **Entry 14** (2026-10-31T16:28:31Z, prev_sha256 1efb780aea61…, md5 of 11 file(s)): Hand-over to vm3 (GRID_PLAN 6 steps 1-4; grid G VM). From this entry the canonical log is vm3 ~/rh60route/AMENDMENTS.log; the vm4 copy is frozen at entry 13 (md5 370d4a9039aee6d7e6693fe8c8486750, chain sha256 1efb780a...). Approval as stated in the workflow task text: the author approved running grid G on [1.4035, 2] on vm3 (2026-10-31 ~16:50, time zone not stated); vm1/vm2 not touched (Elston grid still running); vm4 read/copy only. Setup: hp/ and upper/ rsynced from vm4 via the laptop (49 files, md5 equal to vm4; the 27 code/ and grid/ files equal to the laptop copies and to the PREREG_GRID.stamp sha256 lines; 49 archive blobs match their sha256 names); code -> hp/lb/rh60route/code. Seeds, sha256 equal to the PREREG_GRID.stamp comments: data/s/s_{1.5,2}.json, data/ritz_{1.5,2}.json, out/P0_bench.json, grid_run/ref/final_{odd_1.5_2o3,l2_1.5_1o4}.json (from vm4); grid_run/upper/upper640.jsonl, upper_k384.jsonl (= laptop gap/out_all/upper.jsonl), upper_rerun_L2.jsonl (laptop pilot/glue); upper_1.5_1.jsonl = line 1 (L 1.5, par 1, K 512) of laptop data/odd.jsonl (sha256 b87cde45... as in the stamp). Environment: ~/weil/.venv Python 3.12.15 (vm4: 3.12.16), python-flint 0.9.0, mpmath 1.4.1, numpy 2.5.4 (no scipy; no grid file imports it); GNU time at /usr/bin/time; glibc 2.43 as on vm4 (sr_kernel copied, not rebuilt; P0 checks it); 64 vCPU, MemTotal 60340 MB, root disk 85 GB free. run_grid.sh unchanged: memory budget 0.85*MemTotal - in use at start (about 49 GB, 15 % headroom), 60 slots. No code change; no grid job has run.
>
> **Entry 15** (2026-10-31T23:10:28Z, prev_sha256 8fe0ff9b1b35…, md5 of 3 file(s)): Refinement r1 (PREREG_GRID 2.5, mechanical; this entry is execution step (1), written before windows.txt/jobs.txt change and before any r1 job). Step 43 of 52, [1.91455078125, 1.92364501953125]: job l2_1.92364501953125 exited 4, marker grid_run/out/REFINE_1.91455078125_1.92364501953125 (kind l2): the lambda_2 ladder at 1.92364501953125 ended without a PASS. All 3 rungs (1/4*lam2hat(M0), 2^-10*lam2hat(M0), 2*U^ev(1.91455078125) = 5.15805902827798e-237) FAIL at V4 only (every hard gate true, V5 margin > 0; float p_min -0.643 / -0.133 / -0.132, SR_fail 37375 of 37376 labels at all three; N 37888, M 151552, t_N 0.59-0.62). The odd ladder there passed on 2/3. No STOP_* file; GLUE exited 3 (refinement pending). L prime = 1.91912841796875 = 31443/2^14, the dyadic nearest to 1/2 log((e^{2L_i} + e^{2L_i+1})/2) = 1.91911857640 (= 31442.839/2^14); min |2L prime - log n| over prime powers n = 0.0119 > 2^-20. New windows.txt: L prime inserted after 1.91455078125 (54 windows, 53 steps), md5 74e62f6dc210e167d8147026ce53df5d. jobs.txt gets 10 lines with suffix _r1 (plan.py rules at L prime: K 768, prec 6000, 4.2 GB): U0/U1, S, R, G0 at L prime; grid.py ladder odd|l2 1.91912841796875 1.91455078125; grid.py ladder odd|l2 1.92364501953125 1.91912841796875; GLUE_r1 after all of them. Then REFINE_1.91455078125_1.92364501953125 is renamed REFINED_. Refinements: 1 of 6 (K9g). Operator note before any r1 result: under the reuse rule of 2.5 the rerun lambda_2 ladder at 1.92364501953125 already holds its 3 FAIL records (l2_1.92364501953125_{1o4,1o1024,2}; the V4 failure does not depend on mu), so the refined sub-step [1.91912841796875, 1.92364501953125] is expected to end without a PASS; if so, K3g applies (one refinement level per step).
>
> **Entry 16** (2026-11-01T00:03:59Z, prev_sha256 7fa66c0067fb…, md5 of 4 file(s)): Refinement r1 outcome (operator record, no change to any file or rule). Runner restarted 2026-10-31T23:11:30Z on the appended jobs, finished 2026-11-01T00:03:43Z, no STOP_* file. At L prime = 1.91912841796875: U0/U1 exit 0 (K 768, prec 6000; U^ev 2.74710710889347e-239, U^od 3.63609239109277e-234, radius rule rel 9.8e-14 / 9.9e-14, holds; peak 3.57/3.54 GB, wall 2064/2058 s), S, R, G0 exit 0; odd ladder PASS on 2/3 (p_min 0.616), lambda_2 ladder PASS on 1/4 (p_min 0.727). At 1.92364501953125 with L_prev = L prime: odd ladder reused odd_1.92364501953125_2o3 (PASS); lambda_2 ladder reused its 3 FAIL records (cap reached, no new run), exit 4, marker out/REFINE_1.91912841796875_1.92364501953125. GLUE_r1 exit 3: refinement pending, not glued: REFINE_1.91912841796875_1.92364501953125. The refined sub-step [1.91912841796875, 1.92364501953125] has no PASS and PREREG_GRID 2.5 allows one refinement level per step, so no further refinement is made (1 of 6 used); K3g applies: grid G is not viable as registered. The REFINE_ marker is left in place.
>
> **Entry 17** (2026-11-01T00:04:26Z, prev_sha256 fb6713c00e53…, md5 of 0 file(s)): Erratum to entries 15-16 (wording only): 5.15805902827798e-237 is U^ev(1.91455078125) itself; the lambda_2 rung-3 record l2_1.92364501953125_2 ran at mu = 2*U^ev(1.91455078125) = 1.0316e-236 and was reused unchanged by l2_1.92364501953125_r1 (its printed hist shows the new reference 2.74710710889347e-239 = U^ev(1.91912841796875), but no run was made at 2*that value).

## 5. Cross-check with the Elston grid (§7)

**Registered command.** It was run as GRID_PLAN §6 step 8 says:
`RH60_RUN=<run dir> grid.py xcheck <windows.txt> highprec/gap/out_all`, with the vm3 windows.txt (md5 74e62f6d…).
- **On the real run directory it returns `[]`.** xcheck reads `$RH60_RUN/glue/g_<L>_<kind>.json`, and the scored glue never
  filled `glue/`, which is empty on vm3 and in the mirror.
- **The table below is the same command on the diagnostic glue directory (D1).** That directory was built by grid.py glue's
  own selection rule: the first sorted PASS record per (L, kind), plus every upper file.

| L | kind | ours (lower end) | Elston (lower end) | **ours / Elston** | X1 | ours run s | Elston run s | U^od / Elston λ_1^od mid |
|---|---|---|---|---|---|---|---|---|
| 1.4255 | odd | 2.76281e−78 | 3.56423e−78 | **0.7751** | ok | 202 | 13217 | 1.163 |
| 1.4255 | λ_2 | 1.06874e−74 | 3.36669e−74 | **0.3174** | ok | 230 | 18715 | |
| 1.447 | odd | 2.51231e−82 | 3.26977e−82 | **0.7683** | ok | 224 | 20970 | 1.153 |
| 1.447 | λ_2 | 1.10206e−78 | 3.42061e−78 | **0.3222** | ok | 244 | 24322 | |
| 1.468 | odd | 2.16568e−86 | 2.83496e−86 | **0.7639** | ok | 215 | 25765 | 1.146 |
| 1.468 | λ_2 | 9.05596e−83 | 2.88636e−82 | **0.3138** | ok | 265 | 31456 | |
| 1.4885 | odd | 1.51658e−90 | 1.96436e−90 | **0.7720** | ok | 172 | 44638 | 1.158 |
| 1.4885 | λ_2 | 6.79091e−87 | 2.14180e−86 | **0.3171** | ok | 213 | 40211 | |
| 1.5 | odd, λ_2 | 5.479e−93, 2.736e−89 | **pending** (vm2 rerun in progress; no record yet) | — | — | 175, 197 | — | |

- **X1 (consistency): holds at all 8 pairs.**
  - Elston's ℓ_od ≤ our rigorous U^od(L).
  - Both λ_2 lower bounds ≤ the Galerkin λ̂_2 (lam1 of the U^ev row) × (1 + 1e−6). For example, at 1.4255 λ̂_2 = 3.898e−74 ≥ 3.367e−74.
  - No claim on [1.4035, 1.5] is blocked.
- **X2 (reported).**
  - Odd 0.764–0.775, above the expected [0.62, 0.70] (R-8g MISS).
  - Elston's odd lower bound is 0.999999 of its own λ_1^od mid, so our U^od(K = 640, prec 3000) sits 14.6–16.3 % above λ_1^od. plan.py's
    calibration comment assumed 1–2 %.
  - This is not a soundness issue: U^od is only the μ reference, and N2 holds. It does mean the odd upper bound at K = 640 is
    looser than modelled. ⅔·U^od was still a certifiable rung everywhere.
  - λ_2 0.314–0.322, inside the expected [0.15, 0.5].
- **X3 (reported).**
  - Ours alone on [1.4035, 1.5] (diagnostic glue): 9/9 steps pass, minimum ratio 50.6 at [1.4885, 1.5]; the others are 109–121.
  - Elston alone (`check_steps.py gap/out_all 1.4035,…,1.5`): 4/4 steps pass on [1.4035, 1.4885], minimum ratio 1.129 at [1.468, 1.4885].
  - [1.4885, 1.5] is `missing: l2 odd` (pending).
- **Cost on the overlap.** Ours costs 172–265 s per run on one core; Elston's costs 3.7–12.4 h per run. Elston's bounds are
  essentially tight; ours sit at ⅔·U^od and ¼·λ̂_2.

## 6. Cost and memory (Q4; vm3, 64 vCPU, 60 GB; GNU time per job)

| job type | jobs | core-h measured | core-h model (GRID_PLAN §3, vm4-equiv.) | wall per job | peak RSS max (GiB) | budget max (GB) |
|---|---|---|---|---|---|---|
| U (fr_sweep) | 98 | 57.9 | 51.7 | K640/p3000 785–1034 s; K640/p4000 864–1304 s; K640/p6000 1426–2264 s; K768/p6000 2058–2965 s; K896/p6000 3559–5579 s | 4.64 | 5.6 |
| λ_2 ladders | 54 | 12.5 | 9.1 (+ fallbacks) | up to 3735 s (3 runs at 1.92364501953125) | 3.27 | 4.1 |
| odd ladders | 54 | 8.8 | 7.0 | up to 2135 s (L = 2) | 3.24 | 4.1 |
| stage S | 51 | 5.8 | 4.1 | up to 631 s | 0.03 | 0.2 |
| Ritz | 51 | 0.83 | 0.8 | 44–68 s | 0.10 | 0.5 |
| G2 controls | 6 | 0.65 | 0.6 | 194–676 s | 3.15 | 4.3 |
| G4 (4 cores) | 1 | 0.71 | 0.7 | 638 s | 1.23 | 6.0 |
| G0 | 53 | 0.14 | 0.4 | 7–33 s | 0.03 | 0.5 |
| P0, T15, GLUE ×2 | 4 | < 0.01 | — | ≤ 3 s | 0.05 | 1.0 |
| **total** | **372** | **87.4** | **74.5** | runner wall 7 h 27 min (forecast for vm3: 5.2 h, range 3.6–6.7 h) | | |

The U jobs dominate, as planned (66 % of core-h). K = 896 jobs ran 59–93 min against the 55-min model, and K = 640 jobs at
prec 3000–4000 ran faster than modelled. The memory model held: K = 896 U peaked at 4.64 of 5.6 GB, and certifier runs at
L = 2 at 3.40 / 3.43 GB.

## 7. The failing window (diagnostic; unverified reading)

- **Pattern.** Every failing λ_2 run in the grid fails V4 at the *last* Lemma SR label (n − 1 of n labels):
  - the three runs at 1.92364501953125 (label 37375 of 37376, N 37888, δ_0 39/256 or 19/128, p̂_min −0.643 / −0.133 / −0.132);
  - the ¼ run at 1.8958740234375 (label 32255 of 32256, N 32768, δ_0 19/128, p̂_min −0.018).
- **The passing runs.** The 52 passing λ_2 runs have p̂_min 0.45–2.57 with no failing label. The 2^−10 rerun at 1.8958740234375
  passed with N 31744 and δ_0 5/32.
- **What it is not.** The failure does not follow t_N: failing t_N are 0.59–0.62, while passing runs reach t_N 2.17. It is not
  a step-size effect, because μ = 2·U^ev(L_prev) fails like μ = ¼·λ̂_2.
- **My reading (unverified).** This looks like a certifier-parameter or boundary effect at the last block row for particular
  (L, N, δ_0) in the deflated λ_2 sector, not a property of λ_2(L). Changing anything there needs an amendment.
- **Design gap in §2.5.** Under the registered reuse rule, a μ-independent failure at L_{i+1} cannot be fixed by refinement:
  the ladder at L_{i+1} keeps its 3 FAIL records. Entry 15 predicted this before any r1 result.
- **Post-hoc observation (diagnostic; not registered, not claimed, does not change K3g).**
  - The monotone-λ_2 lever (GRID_PLAN §8 "unused lever", AUDIT §9 item 4) rests on the same min-max monotonicity that the step
    test already uses (Lemma `lem:mono`). Under it, the certified ℓ_2(1.9326171875) = 1.302e−236 bounds λ_2^ev(L) for every
    L ≤ 1.9326171875.
  - In Arb, min(ℓ_od(1.92364501953125), ℓ_2(1.9326171875)) is odd-limited and exceeds U^ev(L′) by **448.6**, and
    U^ev(1.91455078125) by **2.389**. So the existing records would close the gap, even without the refinement.
  - Using this needs an amendment (a check_steps change) logged before any claim, plus the audit. It is a post-hoc choice and
    must be reported as one.

## 8. Deviations

- **D1. No scored check_steps run.**
  - What happened: `grid.py glue` refuses while a `REFINE_*` marker exists (§2.5), and under K3g that marker stays. So
    GLUE_r1, the scored glue, exited 3 before check_steps, and `grid_run/glue/` is empty.
  - What this report uses instead: S1g's detail, the step ratios, the X tables and the partial-outcome coverage all come from a
    *diagnostic* run on the laptop. That run used `check_steps.py <scratch glue> windows.txt --stamp 7a3c6b28…`, with the scratch
    glue built by grid.py glue's own selection rule. Nothing was written into `grid_run/`.
  - What a formal partial claim needs: an amendment that registers a scored partial glue, for example check_steps on windows.txt
    truncated at 1.91912841796875 with `--stamp`, run on vm3 before the audit.
- **D2. xcheck as registered returns `[]`** (empty glue/). The comparison in §5 is the same command on the diagnostic glue.
- **D3. Stale laptop copies.** The laptop copies of grid/windows.txt, grid/jobs.txt and AMENDMENTS.log are stale (the laptop
  log is vm4's frozen 13-entry copy). This scoring read the current vm3 files read-only:
  - windows.txt md5 74e62f6d…
  - jobs.txt md5 f77b5459…
  - AMENDMENTS.log md5 5fdfe43c…
- **D4. Entry 17** corrects a wording slip in entries 15–16. 5.158e−237 is U^ev(1.91455078125); rung 3 ran at μ = 2× that.
- **D5. Runner restart.** The first runner had finished (pending 0) before the refinement jobs were appended, so it was
  restarted, not left to re-read jobs.txt. §2.5 permits this; it is recorded in entry 16.
- **D6. R-5g speed.** R-5g's "vm4-equivalent" was not converted, so the vm3 wall times are scored raw.

## 9. What remains imported trust

- **Stage S, s(L)** (Elston's `schur_upper`, Liu data, `stage_s.py Ldec 16000 1500`) at the 51 new windows. G-S detects only
  errors larger than s − Ritz guard, which is 0.0041–0.0055 over all 115 runs here. An s that is too small is invisible to
  every other gate.
- **Elston's integer Cholesky and residual code** (the proposal path and `cholesky_blocked`).
- **fr_sweep U(L)**, paper §upper: 96 + 2 new rows, plus the seeded upper640, K 384, the K 1024 rerun and K 512 odd.
- **Arb/FLINT** (python-flint 0.9.0), including the acb digamma and polygamma functions.
- **Paper §2.3** (closability, compact resolvent, min-max), **Lemma `lem:M`**, Cor. `cor:step` and Lemma `lem:mono`.
- **The Green identity (P1–P2)**, checked indirectly through G0 (eq. (P) against the closed forms at every window).
- **Elston's own certified records** on the overlap, used only in the §7 consistency check.

## 10. Files

- **Mirror.** `grid_run/` on the laptop, an exact copy of vm3 `~/rh60route/grid_run`, 1533 files.
  - `out/`: run records, G0, G4, P0, the controls, and the `REFINED_` / `REFINE_` markers.
  - `logs/`: per-job .log and .rss, and runner.log.
  - `done/`: exit codes. `upper/`: the 102 U files. `ref/`: the FIXES T15 references.
- **Diagnostic outputs** (not in grid_run/): scratch only, reproducible as above. They are the check_steps listing (its rows are
  the step-ratio column of §3) and xcheck.json (§5).
- **Scoring.** Every number in §2 was re-derived mechanically on the laptop from the mirror, plus the current vm3
  windows.txt, jobs.txt and AMENDMENTS.log (read-only):
  - the records' gates and results;
  - Fraction comparisons for N2;
  - md5 / field comparison for T15;
  - Fraction radius for R-7g;
  - GNU time records for RSS and wall;
  - plan.py's `N_of`, `cert_cost` and `fr_cost` for the models.
