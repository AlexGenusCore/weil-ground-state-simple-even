# Piece IV code: the rh_60-route certifier on [1.4035, 2]

This directory holds the code that produced the Piece IV certificates in `data/piece4/`. Each file is byte-identical to the
file that ran. Every run record lists the sha256 of the files it executed (field `code_sha256`), and `data/piece4/GAP.stamp`
lists them as well. The two exceptions are `pilot.py` and `run_grid.sh`: in each, one comment named a compute host, and that
name was redacted. `data/piece4/REDACTION.sha256` gives the original and the redacted hash of both files.

**Licence.** MIT (the repository `LICENSE`). The code is ours. Elston's `cholesky_blocked` and `exact_residual` are imported
from `code/gap/elston/` under his MIT licence.

**Method credit.** The method follows two preprints:
- bramble_trace, "Full-source Schur certificates for Weil positivity at support radius two", rStation riemann_hypothesis
  paper 60, v1 (2026-10-26). From it we take the summed digamma responses, the displacement-rank-2 matrix, exact core
  elimination, the moment/Abel tail and the omitted Hilbert–Schmidt tail.
- lihongmin, "Cutoff-free positivity of localized Weil forms through the (log 11)/2 threshold", rStation riemann_hypothesis
  paper 45, v1 (2026-10-23). From it we take the Green-response identity and the bases.

Both are unrefereed AI-agent preprints, and only AI agents have reviewed them. Piece IV does not use their claims. At
every grid window this code re-verifies the odd-sector part of their positivity claims. In the even sector it certifies
λ_2^even, not λ_0^even.

**Our additions:**
- the formulas for general `L`;
- the μ-shift;
- the rank-one deflation, which raises the core displacement rank from 2 to 4;
- Lemma SR, an exact-integer structured LDL^T with an explicit residual (`sr.c`, `sr.py`);
- the form-core argument;
- the independent gates G0i and C-ind (`indep.py`, `mp_entries.py`);
- rule E and the gluing.

**Clean room.** The code was written from our own specification and proofs. No rStation code was opened, copied or
adapted.

## Files

| file | role |
|---|---|
| `certify.py` | Theorem V value certificate for one window and one sector. It writes one JSON record with every gate and the certified lower bound. |
| `entries.py`, `eqp.py` | Closed-form matrix entries of the form, and the Arb check G0 of eq. (P). |
| `sr.c`, `sr.py` | Lemma SR. `sr.c` is the C/GMP kernel `sr_kernel`; `sr.py` holds the Python reference, `eps_E` and the float proposal. |
| `indep.py`, `mp_entries.py` | Independent gates. G0i checks 8 entries by eq. (P) with its own prime list. C-ind recomputes τ_core, τ_pole, t_N and r_M in mpmath. |
| `ritz.py` | Float Rayleigh–Ritz value used by gate G-S, as a sanity guard on s(L). |
| `stage_s.py`, `liu.py` | Stage S: the certified s(L) ≥ ‖C_p‖. It uses Elston's Collatz–Wielandt Schur test (`code/gap/elston/grid_norm.py`). |
| `check_steps.py` | The step test (gluing) exactly as used for Piece IV. It requires the provenance checks (`--stamp`), and it has the unused `--l2-from` fallback. Piece III uses the older `code/gap/check_steps.py`. |
| `amend.py` | The append-only amendment log, a hash chain. `python amend.py LOG --verify` checks it. |
| `pilot.py`, `grid.py`, `run_grid.sh` | Drivers for grid G. `grid.py` implements the rung ladders, the controls, rule E (`ladder`) and the glue. They are shipped as the record of what ran. |
| `g4.py` | Mutation harness for G4 (`data/piece4/mutations/G4_1.5.json`). |

The drivers assume the original run layout: `~/rh60route`, with `hp/` holding `lb/rh60route/{code,grid}`, `lb/liu` and
`gap/`. You need none of them to re-run a window or the glue.

## Environment

- Python 3.12 with `python-flint==0.9.0`, `mpmath==1.4.1` and `numpy` (2.5.4 was used); see `code/requirements.txt`.
- GMP and a C compiler for the Lemma SR kernel.

```sh
cd code/rh60route && gcc -O2 -o sr_kernel sr.c -lgmp
sha256sum sr_kernel   # with GCC 15.2.0 (Ubuntu) this is f46d6646..., the binary in every record's code_sha256
```

## Re-run one window

Every record stores its full command line in the field `argv`; the paths there are redacted. As an example, here is
`L = 1.5`, odd sector, rung 2/3. It takes about 3 minutes and 1.3 GB:

```sh
cd code/rh60route
export RH60_HP=$PWD/.. RH60_ARCHIVE=$(mktemp -d)   # Elston's code is in ../gap/elston; executed files are archived here
I=../../data/piece4/inputs
python certify.py --L 1.5 --Uev 3.85105826960019e-97 --s-file $I/s_1.5.json --ritz $I/ritz_1.5.json --workdir $(mktemp -d) \
  --eps -1 --mu-ref 8.21780562022764e-93 --tmin 1 --mu-rel 2/3 --sr-if-pmin 0.015625 --out odd_1.5_2o3.json --label odd_1.5_2o3
```

Compare `mu`, `N`, `M`, `SR_checksum`, `V5_margin` and `certified_lower_bound` with `data/piece4/glue/g_1.5_odd.json`.

`data/piece4/inputs/` holds the s(L) and Ritz inputs for `L = 1.5` and `L = 2`. Their sha256 equal the `s_sha256` of the
records. The λ_2 run at `L = 2` (`g_2_l2.json`, argv in the record) takes about 45 minutes and 3.5 GB. For any other window:

```sh
PYTHONPATH=../gap/elston LIU_DATA=$(mktemp -d) python stage_s.py L 16000 1500   # -> $LIU_DATA/s/s_L.json (minutes)
python ritz.py L                                                                # -> ritz_L.json
```

The exact s(L) of each run is also in its record, in the field `s`.

**What a clean copy reproduced (2026-11-01, laptop).**
- The `L = 1.5` odd run above gives the same `mu`, `N`, `M`, `SR_checksum`, `V5_margin`, gates and certified ball as the
  shipped record. It took 106 s.
- `stage_s.py 1.5 16000 1500` gives the same exact `s`.
- `ritz.py 1.5` agrees only to float rounding (the last 1–2 digits differ). These values feed only the float guard of gate
  G-S.

## Re-run the glue

```sh
python code/rh60route/check_steps.py data/piece4/glue data/piece4/windows.txt \
  --stamp 7a3c6b287f840aba50fc11d49e6f919eb0cb758a6a0ce03e6248298feda4b9e8
```

Run this from the repository root. The output is byte-identical to `data/piece4/logs/GLUE_r2.log`. The stamp is the sha256 of
the original `GRID.stamp`, which every Piece IV record carries. With `data/piece4/windows_partial.txt` you get the
registered partial outcome, `logs/GLUE_P.log`. `check_theorem.sh` in the repository root runs this together with Pieces
I–III.

## Not included

`SPEC.md` and `PROOFS.md` are the specification and proofs that the code cites (Theorem V, Lemma SR, P1–P23). They are not
part of this release. GAP.stamp records their hashes, and they are available on request (info@genuscore.com).
