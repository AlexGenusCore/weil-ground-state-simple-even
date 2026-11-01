# PREREG_GRID (registered; pre-commitment stamp on vm4): rh_60-route grid G, simple-even ground state on [1.4035, 2] by the step test

**Status.** Written 2026-10-31 after FIXES.md and before any grid computation. Reviewed by a fresh reviewer (`grid_review.md`,
small corrections applied there) and then **pre-committed**: `~/rh60route/PREREG_GRID.stamp` on vm4 holds the md5 and sha256 of
this file, the sha256 of every document, script and executed code file (each code file also as a blob in `archive/`), the
seed-input sha256s and the UTC time. The run-time GRID.stamp below re-verifies every sha256 line of it.
- What exists: float forecasts only (`grid/forecast.jsonl`, `grid/forecast_check.jsonl`, label *float*), the window list
  (`grid/windows.txt`), the job file (`grid/jobs.txt`) and the runner (`grid/run_grid.sh`). GRID_PLAN.md has the derivation and
  the cost model.
- What does not exist: no U(L_i) for a new window, no certifier run, no GRID.stamp. The author approves the big run and the VM;
  until then nothing in §4 runs. No push, publish or contact.
- **This file is frozen from the pre-commitment stamp on.** Changes go into AMENDMENTS.log (`amend.py`) as below.
- **Stamp (when approved).** On the grid VM, after the setup of GRID_PLAN §6 and before job P0, `grid/run_grid.sh stamp`
  first checks every sha256 line of `~/rh60route/PREREG_GRID.stamp` (copied from vm4) and refuses on any difference, unless
  that difference is a logged amendment and `ALLOW_DIFF=1` is set (recorded in the stamp). It then fills `archive/` with every
  executed code file (so no two first runs race to copy a new blob) and writes `~/rh60route/GRID.stamp` once (read-only). It
  holds, then `date -u`:
  - the md5 of this file, GRID_PLAN.md, SPEC.md, PROOFS.md, review.md, spec_changes.md, PREREG.md, AUDIT.md and FIXES.md;
  - the md5 of jobs.txt, windows.txt, the grid scripts, the two forecast files, and every code file a job executes:
    certify.py, entries.py, eqp.py, indep.py, mp_entries.py, sr.py, sr.c, sr_kernel, g3.py, g4.py, ritz.py, pilot.py,
    amend.py, stage_s.py, liu.py, Elston's three files, check_steps.py, fr_sweep.py, fast_recurrence.py and hp.py;
  - the md5 of the seeded inputs (certified U files, s(1.5), s(2), Ritz files);
  - the AMENDMENTS.log chain check.

  A copy goes to `highprec/lb/rh60route/GRID.stamp`. Every run record carries the stamp's sha256 (`stamp_sha256`), its
  archived code blobs (F4) and the amendment-log pin (F5). Gluing uses `check_steps.py … --stamp <sha256>` (F6).
- **After stamping.** This file is never edited (that holds from PREREG_GRID.stamp on). Amendments are entries in the append-only AMENDMENTS.log (`amend.py`, hash
  chain), each written before any result it could affect, and quoted in RESULTS_GRID.md.

**Credit.** The method is bramble_trace's (rh_60 v1, "Full-source Schur certificates for Weil positivity at support radius
two", rStation 2026-10-26) and lihongmin's (rh_45 v1, "Cutoff-free positivity of localized Weil forms through the (log 11)/2
threshold", rStation 2026-10-23). Both are unrefereed AI-agent preprints reviewed only by AI agents. Ours: general L, μ-shift,
rank-one deflation, Lemma SR, the form core, the gluing and this grid. Reused: Elston's MIT code, our stage S, fr_sweep U(L),
and the G6 auditor's `mp_entries.py`.

**Clean room.** Written from SPEC.md, PROOFS.md, review.md, spec_changes.md, PREREG.md, AUDIT.md, FIXES.md and our own code
only. Nothing under `scratch_archive/rstation/` and no rStation URL was opened.

**Labels** (as PREREG.md): *certified* = a Theorem V PASS with every hard gate passed, decided in Arb or exact arithmetic;
*float* = forecasts, Galerkin values, proposals; *diagnostic* = reported, never scored.

## 1. Questions

1. **Q1 (coverage).** Does every step of the registered window list pass the step test U^ev(L_i) < min(ℓ_od, ℓ_2)(L_{i+1}) in
   Arb, with every counted run passing every hard gate? With paper Cor. `cor:step` and Lemma `lem:mono` this gives a simple,
   even ground state of A_L for every L ∈ [1.4035, 2].
2. **Q2 (losses).** What are ℓ_odd = U^od/μ_od and ℓ_2 = λ̂_2/μ_2 per window? How many windows need a fallback rung or a
   refinement?
3. **Q3 (cross-check).** On the overlap with the Elston grid, how do our certified bounds compare with Elston's at the same L
   (§7)?
4. **Q4 (cost).** What are the core-hours, wall time and peak RSS per job type, against GRID_PLAN §3?

## 2. Fixed setup (not tuned on results)

### 2.1 Windows

The windows are `grid/windows.txt`: 53 windows, L_0 = 1.4035 < … < L_52 = 2, so 52 steps.
- **L_0 = 1.4035.** This is the end of the released (0, 1.4035] theorem. Its U^ev comes from `upper640.jsonl`, and no lower
  bound is needed there.
- **Overlap anchors 1.4255, 1.447, 1.468, 1.4885 and 1.5.** These are Elston's windows, kept as exact decimals so §7 can
  compare both methods at the same L. U^ev is already certified at each of them.
- **L = 2.** This is the pilot window.
- **Every other window** is an exact dyadic m/2^14 (float-exact, so Lwin(L) = L in stage S). `grid/plan.py` chose them as the
  fewest windows on each segment between anchors with forecast ρ_i = ⅔·U^od(L_{i+1})/U^ev(L_i) ≥ 2, equalised. Above 1.5 the
  forecast ρ is 2.15–2.32 at selection and 2.08–2.33 when the forecast is rerun at the exact windows. It is 95–102 on the
  overlap and 50.6 on [1.4885, 1.5] (GRID_PLAN §2).
- **Margin 2.** It is chosen so that the ½ rung still glues (ratio 1.5) if the ⅔ rung fails.
- **Exact strings.** Ldec is the exact string in windows.txt, and every certified path uses arb(Ldec). Every window has
  |2L − log n| > 2^−20 for every prime power n (plan.py asserts this).

### 2.2 Upper bounds

**Which U are needed.**
- U^ev(L_i) (par 0) at every window i < 52.
- U^od(L_i) (par 1) at every window i ≥ 1. It is the μ reference and the N2 guard.

**Reused certified files** (no rerun; their md5 goes into the stamp):
- U^ev at 1.4035, 1.4255, 1.447, 1.468 and 1.4885: `gap/out_all/upper640.jsonl` (K = 640);
- U^ev(1.5): `gap/out_all/upper.jsonl` (K = 384);
- U^ev(2) and U^od(2): the pilot rerun `upper_rerun_L2.jsonl` (K = 1024);
- U^od(1.5): `data/odd.jsonl` (K = 512), as in the pilot controls.

**New runs.** 96 runs of `PAR=p THREADS=1 fr_sweep.py upper_<L>_<p>.jsonl K L prec`:
- K = 128·max(5, ⌈e^{2L}/7.8⌉): 640 up to L ≈ 1.83, 768 up to L ≈ 1.92, and 896 above. This is at least 1.22× the
  convergence knee (about 10·e^{2L} at L = 1.5 and 13.4·e^{2L} at 2).
- prec = 3000 for L ≤ 1.5, 4000 for L ≤ 1.75, 6000 above. These are the precisions already used at those L.

**Radius rule (mechanical).** If (lam0_upper − lam0_mid)/lam0_mid > 1e−10, that U is rerun at prec + 2000. This is logged in
AMENDMENTS.log before the rerun.

**Gluing directory.** It holds exactly the files above. check_steps takes the minimum lam0_upper per L over them (R10). Every
row is a rigorous upper bound.

### 2.3 Certifier

The certifier is the code that FIXES.md verified, unchanged: certify.py sha256 0cbb7e7f…, called only through `pilot.py` by
`grid/grid.py`. The only pilot.py change is that the ladders take an optional rung list; its default behaviour is unchanged.
- **Core and precision.**
  - K = 512.
  - prec_core = 64⌈(3b + 512)/64⌉ and prec_T = 64⌈(1.5b + 128)/64⌉, with b = ⌈log2(1/U^ev(L))⌉.
  - prec_src = 192, P_core = 1536, P = 96. J and R follow the SPEC rules.
- **Blocks and margin.**
  - N follows rule R4: t_min = 1 when ϑ = 0, and ½ for λ_2.
  - M = 4N, or 8N when r_M > ¼.
  - δ_0 follows the pilot rule.
- **μ, φ and ϑ.**
  - μ is a 64-bit dyadic, rounded down. For the negative controls it is rounded up.
  - φ and ϑ follow SPEC C4 with the A3 fix.
- **s(L) and the Ritz guard.**
  - s(L) comes from `stage_s.py Ldec 16000 1500`, with LIU_DATA = ~/rh60route/data.
  - The Ritz guard is `ritz.py Ldec 1600`.
  - s(1.5), s(2) and their Ritz files are the pilot's, reused.
- **Hard gates in every run** (certify.py): G-S, G0-mini, G0i, V2–V5, R6, G5 (including the F3 S_input rebuild), G5′
  (uncapped), C-τ, C-r̄, C-J_2, C-r_M and C-ind.

### 2.4 Ladders per window L = L_{i+1} (`grid.py ladder`, using the pilot's ladder logic)

- **Odd.** The rungs are r ∈ {⅔, ½, ⅓} of U^od(L), keeping only the rungs with r·U^od(L) ≥ (1 + 2^−20)·U^ev(L_i). A lower
  rung could not glue.
  - The float proposal picks the start: the first rung with p̂_min ≥ 2^−6.
  - At most 3 rigorous runs; stop at the first PASS.
- **λ_2 (ε = +1, deflated).** The rungs are ¼·λ̂_2(M_0), then 2^−10·λ̂_2(M_0), then 2·U^ev(L_i). At most 3 runs; stop at the
  first PASS.
- **Even λ_1 shift.** Not run (R11).

### 2.5 Refinement (mechanical; it needs no amendment)

A step [L_i, L_{i+1}] is refined in two cases:
- no odd rung qualifies, which is decided from the U values before any certifier run of that window (`REFINE_*` marker, exit 3);
- a ladder ends without a PASS.

The refinement inserts one window L′: the dyadic m/2^14 nearest to ½·log((e^{2L_i} + e^{2L_{i+1}})/2).
- L′ gets the full window job set under the same rules (`plan.py`-style lines appended to jobs.txt).
- L′ is inserted into windows.txt and logged in AMENDMENTS.log, with the md5 of the new windows.txt, before its jobs start.
- At most one refinement level per step, and at most 6 refinements in total (K9g).
- **Execution.** The operator (1) appends an AMENDMENTS.log entry naming the step, L′ and the md5 of the new windows.txt;
  (2) inserts L′ into windows.txt; (3) appends to jobs.txt, every new ID with the suffix `_r<k>`: U0/U1, S, R and G0 at L′, the
  two ladders `grid.py ladder odd|l2 L′ L_i`, the two ladders `grid.py ladder odd|l2 L_{i+1} L′`, and `GLUE_r<k>` depending on
  all of them; (4) renames the `REFINE_*` marker to `REFINED_*`. A rerun ladder reuses every existing run record of the same
  name (pilot.run never reruns a record; the same name means the same μ, except the λ_2 rung 3, whose record keeps the μ of its
  first run), and those records count toward its 3-run cap.
- **Gluing.** `grid.py glue` refuses (exit 3) while any `REFINE_*` marker exists. The scored glue is the last `GLUE_r<k>`, or
  GLUE if there was no refinement.

## 3. Gates and controls

A false hard gate, or a run that crashes, makes the run VOID. `grid.py` then writes `out/STOP_GATE`, and the runner launches
nothing new (K2g). Any other job that exits with a status other than 0, 3 or 4 (3/4: REFINE marker or refinement pending)
makes the runner write `out/STOP_EXIT_<id>`, with the same consequence.

| gate | content | when |
|---|---|---|
| P0 | G3 on the grid VM: exact T2/T3/P13/P20/Lemma SR identities, and sr_kernel equal to the Python reference | first job; every certifier job depends on it |
| T15 | toolchain reproduction: the grid's `odd_1.5_2o3` and `l2_1.5_1o4` must equal the FIXES records `final_odd_1.5_2o3` and `final_l2_1.5_1o4` in μ, N, M, τ_N, r_M, δ_0, ε_E, min pivot, V5 margin, the Lemma SR checksums and the certified ball | after the L = 1.5 ladders; every other certifier job depends on it |
| per-run hard gates | §2.3 | every run |
| G0 | full Arb eq. (P) against the closed forms (`eqp.py Ldec`, both sectors) | every window |
| G2 | negative controls at 3 windows: 1.447, the window nearest 1.75 (1.74713134765625) and L_51 = 1.99200439453125. Even ϑ = 0 at μ = 1.01·U^ev(L) and odd at μ = 1.01·U^od(L). All 6 must FAIL at V2–V5 with no hard gate false | after T15 |
| G4 | at L = 1.5, on the stamped code: the 15 mutations of `g4.py` (the 9 registered, the 3 auditor mutations, pp_drop, lam_n and gen2K). Each must be caught | after T15 |
| N2 | a PASS with μ > U^od(L) (odd) or μ > λ̂_2(M_0) (λ_2) writes `STOP_N2` (pilot.py) | every ladder |
| F6 | at gluing, each file must have result PASS, Ldec equal to the L in its file name, mut null, the right sector and stamp_sha256 equal to the grid stamp | GLUE |

## 4. Order (one VM, `grid/run_grid.sh run`, jobs.txt order = priority)

1. Setup (GRID_PLAN §6), then `run_grid.sh stamp`.
2. P0.
3. The U jobs (longest first), stage S, Ritz and G0, in parallel as memory allows.
4. The L = 1.5 ladders, then T15, then G4.
5. The window ladders (high L first) as their inputs complete; the G2 controls.
6. GLUE: `check_steps.py <glue> windows.txt --stamp <sha256>`.
7. Cross-check (§7), run locally after mirroring.
8. RESULTS_GRID.md, NOTES.md, IDEAS.md.
9. A fresh-agent audit of the grid outputs (G6 pattern) before any claim.

## 5. Success (grid PASS needs all of these)

- **S1g.** `check_steps.py` prints "ALL STEPS PASS" with 52 comparisons (plus one per refinement).
- **S2g.** Every glued record passes F6 and has every hard gate true. T15 holds.
- **S3g.** All 6 G2 controls FAIL at V2–V5, with no hard gate false.
- **S4g.** G4 at 1.5: all 15 mutations are caught.
- **S5g.** P0 passes, and G0 passes at every window.
- **S6g.** N2 is clean, and no `STOP_*` file exists.

**Partial outcome (registered now, so nothing is chosen afterwards).** If S1g fails but S2g–S6g hold, the only claim is the
longest run of consecutive passing steps that starts at L_0 = 1.4035, i.e. [1.4035, L_j], reported as partial coverage.
Passing steps after the first failing step are reported, not claimed.

**Verdict.** A simple, even ground state for every L ∈ [1.4035, 2]. It is *certified* in the PREREG sense, pending the
audit in step 9 of §4.

## 6. Kill criteria

| id | criterion | consequence |
|---|---|---|
| K1g | any G2 PASS or any N2 violation | VOID every result and stop |
| K2g | any hard gate false, or a crash, in any run (STOP_GATE), or any job exiting with a status other than 0, 3 or 4 (STOP_EXIT_<id>) | stop for diagnosis; only an amendment continues |
| K3g | a refined step still has no PASS | stop the route: grid G is not viable as registered |
| K4g | a job's peak RSS exceeds its jobs.txt budget by more than 25 % (live session-RSS sample, STOP_RSS_<id>; or its `logs/<id>.rss` record), or the watchdog fires (STOP_MEM) | stop and re-plan the memory model (amendment) |
| K5g | more than 150 core-h or more than 24 h wall on the VM | stop and report (a budget overrun, not a kill of the method) |
| K6g | P0 fails, or T15 differs (STOP_TOOLCHAIN) | stop before any further certifier run |
| K7g | a G4 mutation is not caught | certified status is void until the gate is fixed by amendment (not a kill) |
| K8g | G0 fails at a window | that window's runs are void; fix the derivation |
| K9g | more than 6 refinements | stop: the forecast model is wrong; re-plan by amendment |

## 7. Cross-check with the Elston grid on [1.4035, 1.5] (a consistency check, not a pass criterion)

`grid.py xcheck windows.txt gap/out_all` compares the windows where both methods have a certified record.
- Now: Elston odd at 1.4255, 1.447, 1.468 and 1.4885, and Elston λ_2 at 1.447 and 1.468.
- Later: the rest as the Elston grid finishes on its own VMs.

The checks:
- **X1 (consistency).** Elston's λ_1^od lower bound must be ≤ our rigorous U^od(L). Both λ_2^ev lower bounds must be ≤ the
  Galerkin λ̂_2 (lam1 of the U^ev row, float, with a 1e−6 tolerance). Ours ≤ U^od is already enforced by N2.
- **X2 (reported).** The ratio ours/Elston per window and kind. Expected: odd ≈ ⅔·U^od/λ_od ∈ [0.62, 0.70]; λ_2 ∈ [0.15, 0.5].
- **X3 (reported).** The step test on the overlap with each method alone. Elston's run on `gap/out_all` is the existing one;
  ours is the glue directory restricted to [1.4035, 1.5].

**Consequence.** An X1 violation blocks every claim on [1.4035, 1.5], from both methods, until it is diagnosed in an
amendment. It does not change the S/K scoring above.

## 8. Registered predictions (float; scored HIT or MISS, never used to tune)

| id | prediction | HIT if |
|---|---|---|
| R-1g | no refinement is needed | 0 refinements |
| R-2g | every odd ladder passes on ⅔; every λ_2 ladder on ¼ | all first rungs |
| R-3g | the minimum check_steps ratio is ≥ 1.5 (forecast 2.1) | yes |
| R-4g | N per run within ±10 % of the GRID_PLAN model | all runs |
| R-5g | per-run wall within ×1.5 of the model; total within ±30 % of 74.5 core-h (vm4-equivalent) | both |
| R-6g | every job's peak RSS ≤ its jobs.txt budget | all jobs |
| R-7g | every new U passes the radius rule at the registered prec | all 96 |
| R-8g | X2 odd ratio ∈ [0.62, 0.70] at every compared window | all |
| R-9g | T15 is bit-identical | yes |

## 9. Resources

- **Machine.** One 64-vCPU VM, with the author's approval: vm2 (144 GB; about 2–3 h wall) or vm3 (60 GB; about 4–7 h).
  vm1 and vm4 are not used for the grid.
- **Runner** (`run_grid.sh`):
  - slots = nproc − 4;
  - memory budget = 0.85·MemTotal − (memory in use at start), plus a live check that MemAvailable − job ≥ 0.15·MemTotal;
  - nice 5, and setsid for each job;
  - a watchdog at MemAvailable < 5 %, which kills that job's process group by explicit PGID and writes STOP_MEM;
  - oom_score_adj 1000 for every job, so a kernel OOM takes a grid job and nothing else;
  - per job, GNU time writes the peak RSS to `logs/<id>.rss` (R-6g, K4g), and each 20 s loop samples the job's session RSS
    (STOP_RSS_<id> above 1.25 × budget, K4g).
- **Coexistence.** If Elston grid jobs still run on the chosen VM, the live check makes ours wait. The runner kills nothing
  that is not its own.
- **Budget.** 150 core-h and 24 h wall (K5g). No push, publish or contact.

## 10. To settle before the GRID.stamp (the pre-commitment stamp is written)

- The author's approval of the run, and the VM choice.
- Copy `~/rh60route/PREREG_GRID.stamp` from vm4 to the VM (`run_grid.sh stamp` checks it).
- Setup on that VM (GRID_PLAN §6), including the Python/flint versions, the sr_kernel binary (P0 checks it) and the two FIXES
  reference records in `grid_run/ref/`.
- **AMENDMENTS.log.** The canonical log moves to the grid VM: it is copied from vm4, and vm4's copy is frozen. The
  stamp records the chain sha256.
- Fresh review: done (`grid_review.md`); its corrections are in this file, run_grid.sh, grid.py and selftest_jobs.txt.
- GNU time (`/usr/bin/time`) on the VM (the runner refuses to start without it), and free disk checked with `df`.
- **FIXES' pre-PREREG list.** Stamp indep.py, mp_entries.py, amend.py and check_steps.py; glue with `--stamp`; export
  RH60_AMEND. All three are covered by the stamp list, `grid.py glue` and `run_grid.sh`.

## 11. Waivers before the stamp (dated; empty unless used)
