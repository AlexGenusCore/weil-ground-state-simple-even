# Data

All bounds are Arb balls written as strings `"[midpoint +/- radius]"`. Each window row is
`[lambda0_lower, lambda0_upper, lambda1even_lower, lambda0odd_lower]` for the window `[-L, L]`
(the code certifies the dyadic number `arb(L).upper() >= L`, see paper §4.2).

| File | What it is | Provenance |
|---|---|---|
| `theorem_bounds.json` | **Certificate of record**, 31 windows `0.05 ... 1.19` | Rows `L <= 1.0` copied verbatim from the clean end-to-end rerun (2026-10-24, log `logs/run_rerun.log`). Rows `1.03`, `1.06`, `1.09` copied verbatim from the extension run (2026-10-24/25, log `logs/run_extend.log`; snapshot taken 2026-10-25 after window 1.09 finished). Rows `1.12`, `1.15`, `1.18`, `1.19` copied verbatim from the continued extension run (2026-10-25/26, same log), certified with the upper-triangle panel code. |
| `validate_1.0.json` | Window `L = 1.0` recertified with the sharp-cutoff path (`code/validate10.py`) | Extension run, first step (`logs/run_extend.log`, top). Not part of the gluing. |
| `history/theorem_bounds_original.json` | Bounds from the original window runs (several code revisions, Gauss-Legendre off-by-one) | Superseded; kept for the erratum. |
| `history/theorem_bounds_corrected.json` | The original bounds after the Weyl-shift correction and new upper bounds (`code/gl_correction.py`) | Superseded by the rerun; Table 1 of the paper. |
| `logs/run_rerun.log` | Clean rerun: three stages, the failure at `L = 1.0` with the default margins, the resume with `CERT_MARGIN=1.2 CERT_DDIV=8`, and the gluing | |
| `logs/run_extend.log` | Validation at `L = 1.0`, window `1.03`, the out-of-memory abort at `1.06`, the resume, windows `1.06` and `1.09`, the restart with the upper-triangle code and window `1.12`, then windows `1.15`, `1.18`, `1.19` (cluster assembly by `code/prefetch.py` pipelined with local certification) | Complete run log; the earlier release's log is a prefix of it. Redacted copy since 2.0.0 (home paths, account name and private IPs in one traceback replaced; `logs/REDACTION.sha256` maps original to redacted sha256). |
| `logs/run_gl_correction.log` | Output of `gl_correction.py` (history) | |
| `logs/check.log` | Output of `python code/theorem.py --check` on `theorem_bounds.json` | Ends with `THEOREM CERTIFIED for all L in (0, 1.19]`. |
| `piece3/g_<L>_l2.json`, `piece3/g_<L>_odd.json` | **Piece III certificates** (release 1.1.0): lower bounds for the second even eigenvalue (`l2`, run with `--deflate`) and the lowest odd eigenvalue, field `certified_lower_bound` (an Arb ball; the lower end is used). 16 files for `L = 1.2205 ... 1.4035`, plus both sectors at `1.4255`, `1.447`, `1.468`, `1.4885` (release 2.0.0 adds `1.4255` l2 and `1.468`, `1.4885`; past `1.4035` they are redundant with Piece IV) | Elston's certifier `code/gap/elston/grid_certificate_rigorous.py`, run 2026-10-30/31 on three 64-vCPU VMs; options in the field `args`, wall-clock time in `seconds`. The field `args.json` is the path on the compute host. |
| `piece3/upper640.jsonl` | Upper bounds `U(L)` for the lowest even eigenvalue, `K = 640`, 3000 bits, field `lam0_upper` (outward rounded), at the 13 grid points `1.19 ... 1.4885` | `code/upper/fr_sweep.py`, run 2026-10-30. |
| `piece3/rerun_U1.19.jsonl` | Re-run of `U(1.19)` with the shipped `code/upper/` on 2026-10-31 | Reproduces the stored line exactly. The revision of `fast_recurrence.py` used on 2026-10-30 was not recorded; the file was edited afterwards (per the project log, a fix of the `primes=False` path, which the upper bounds do not use). |
| `piece3/check.log` | Output of `python code/gap/check_steps.py` on `data/piece3/` | Ends with `CERTIFIED: ... simple-even for all L in (0, 1.4885]` (12 steps, minimum ratio 1.129); the theorem uses it only up to `1.4035`. |
| `piece3/SHA256SUMS` | SHA-256 of every file in `piece3/` | `cd data/piece3 && sha256sum -c SHA256SUMS`. |

## Piece IV (`piece4/`, release 2.0.0): rh_60-route grid G on `[1.4035, 2]`

Certifier `code/rh60route/certify.py`, run 2026-10-31/11-01 on one 64-vCPU VM (grid G under `PREREG_GRID.md`, the gap under
`PREREG_GAP.md`). Every record is JSON. The step test reads `certified_lower_bound`, an Arb ball whose lower end is used, and
it requires `result` PASS, `Ldec`, `mut` null, the sector, and `stamp_sha256`.

| File | What it is |
|---|---|
| `piece4/glue/` | **The glued set, 208 files.** `g_<L>_odd.json` and `g_<L>_l2.json` (106 records, 53 windows `1.41473388671875 ... 2`; each is the first PASS rung of its ladder) and the upper bounds `upper_<L>_<par>.jsonl` (`code/upper/fr_sweep.py`, `K = 384 ... 1024`, every row `rigorous_quadrature: true`; the smallest `lam0_upper` per `L` is used). `upper640.jsonl` is the Piece III file; it supplies `U(1.4035)`. |
| `piece4/windows.txt`, `windows_partial.txt` | The 54 windows of the full glue (refinement window `31443/2^14 = 1.91912841796875` included), and the 44 windows of the registered partial outcome |
| `piece4/rule_e/` | The three registered λ_2 rungs at `1.92364501953125` (all FAIL at V4: the grid fails, K3g), the rule-E run `l2_1.92364501953125_1o4_e1.json` (PASS, `N = 38912`; `glue/g_1.92364501953125_l2.json` is a byte-identical copy), and the `REFINED_` markers |
| `piece4/controls/` | Negative controls at μ above the true value; all must FAIL. Six grid G controls fail at V4; the rule-E control `nc_1.92364501953125_l2e` fails at V2, which is weaker than planned |
| `piece4/mutations/G4_1.5.json` | G4: 15 code mutations at `L = 1.5`, all caught |
| `piece4/logs/` | Glue output: `GLUE.log`, `GLUE_r1.log` (grid G, refinement pending), `GLUE_P.log` (partial, 43 steps), `GLUE_r2.log` (**full, 53 steps, minimum ratio 2.099**) |
| `piece4/inputs/` | s(L) and Ritz inputs for `L = 1.5` and `2`, for re-running a window (sha256 equal the records' `s_sha256`) |
| `piece4/PREREG_GRID.md`, `GRID.stamp` | The pre-registration of grid G and its run-time stamp (hashes of every registered document and executed file) |
| `piece4/PREREG_GAP.md`, `GAP.stamp` | The post-hoc pre-registration of rule E (written after the grid failure, stamped before the run) |
| `piece4/AMENDMENTS.log` | The append-only amendment log (21 entries, hash chain) |
| `piece4/RESULTS_GRID.md`, `RESULTS_GAP.md`, `AUDIT_GRID.md` | Scored results of both pre-registrations, and the fresh-agent audit |
| `piece4/REDACTION.sha256` | Original sha256 → redacted sha256 for every redacted file (see below) |
| `piece4/SHA256SUMS` | SHA-256 of every file in `piece4/`; `cd data/piece4 && sha256sum -c SHA256SUMS` |

**Redaction.** The run records, stamps, amendment log and documents named host paths, a user name and the compute hosts.
In the shipped copies these are replaced: the run account's home directory by `~`, the account name by `user`, and the hosts by
`vm1` … `vm4`. Nothing else changed. In particular, no number or field of any record was edited, and the step test gives
byte-identical output on the redacted records. Hashes that were recorded during the runs refer to the **originals**. These
are the record pins (`amendments.sha256`), `stamp_sha256`, the stamp lines, the amendment hash chain, and `code_sha256` for
`pilot.py`. `REDACTION.sha256` maps every original hash to its redacted hash. The originals are available on request.

On the originals, `amend.py --verify` gives `chain OK, 21 entries, sha256 c9029e85…`. All 117 shipped rh_60-route record files pin a prefix of
that chain: 112 at 14 entries, 2 at 15, and 3 at 20. The last 3 are the rule-E run, its glued copy and its control. Every record carries
`stamp_sha256 = 7a3c6b28…` = sha256(original `GRID.stamp`). The redacted `AMENDMENTS.log` does **not** verify, because its
bytes differ.

The documents use development paths (`grid_run/`, `grid_run_gap/`, `gap/out_all/`, `highprec/…`). Their shipped
counterparts are `piece4/` and `piece3/` as listed above. Files that the documents name but this release does not ship are
GAP_DIAG, VERIFY_GRID, SPEC, PROOFS, the per-window G0 records and the run logs. They are available on request.

Notes.

- The extension run kept its own bounds file, which also contains the rows `L <= 1.0`. Those are the same values
  re-serialized, with radii rounded outward by about 1% (for example `3.43e-21` became `3.45e-21`). We release the
  rerun's original strings. Either set passes the gluing.
- The row `L = 1.0` is the rerun's (crude cutoff `T# = 3610`). The released code would recompute `1.0` with the sharp
  path; that result is `validate_1.0.json`.
- Logs were scrubbed for publication: absolute paths are replaced by `<code>/` and `<python>/`, host names by
  `user@host1` ... `user@host3`, and the time-zone abbreviation was removed from timestamps. No number was changed.
