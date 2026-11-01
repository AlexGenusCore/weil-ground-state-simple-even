#!/bin/sh
# Check the theorem "simple, even ground state for every L in (0, 2]" from the shipped data, without recomputing any
# window (about 10 seconds). Needs a Python with python-flint 0.9.0 (code/requirements.txt); set PYTHON to choose one.
# This is RECORD VALIDATION, not certificate regeneration: it checks file hashes, the schema, gates and provenance of every
# record, and every step comparison between recorded bounds. It does not recompute any window matrix, stage S, factorisation
# or upper bound; that is regeneration, per window, with the commands in README.md (hours per window).
#   Pieces I-II  (0, 1.19]      code/theorem.py --check            on data/theorem_bounds.json
#   Piece III    [1.19, ...]    code/gap/check_steps.py             on data/piece3/   (only [1.19, 1.4035] is needed)
#   Piece IV     [1.4035, 2]    code/rh60route/check_steps.py       on data/piece4/glue/
#   Records      paper/gen_tables.py: all 15 hard gates, schema and provenance of every glued Piece IV record (the stamped
#                check_steps.py checks only result, window, sector, mutation flag and stamp), Piece III record fields, and
#                that paper/generated.tex is exactly what the records give
# Each step test proves simple-even on a closed interval [L_i, L_{i+1}] (paper Cor. cor:step with Lemma lem:mono), and the
# pieces share endpoints, so together they cover (0, 2].
set -eu
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
# sha256 of the ORIGINAL GRID.stamp, which every Piece IV record carries (field stamp_sha256). The shipped GRID.stamp is a
# redacted copy; data/piece4/REDACTION.sha256 lists original -> redacted hashes.
STAMP=7a3c6b287f840aba50fc11d49e6f919eb0cb758a6a0ce03e6248298feda4b9e8
grep -q "^$STAMP  .*data/piece4/GRID.stamp$" data/piece4/REDACTION.sha256 || { echo "FAIL: stamp hash not in REDACTION.sha256"; exit 1; }

echo "== file hashes"
(cd data/piece3 && sha256sum -c --quiet SHA256SUMS) && (cd data/piece4 && sha256sum -c --quiet SHA256SUMS) \
  && echo "data/piece3, data/piece4: OK" || { echo "FAIL: data hashes"; exit 1; }  # set -e does not stop inside an && list
# The Piece IV proofs (supplement/PROOFS.md) must be the file stamped in GAP.stamp before the gap run.
(cd supplement && sha256sum -c --quiet SHA256SUMS) && grep -q "^$(sha256sum supplement/PROOFS.md | cut -d' ' -f1)  .*/PROOFS.md$" data/piece4/GAP.stamp \
  && echo "supplement: OK (PROOFS.md matches GAP.stamp)" || { echo "FAIL: supplement hashes"; exit 1; }

echo; echo "== Pieces I-II: code/theorem.py --check"
# CERT_PREC=768: Piece I's constants are enclosed on the 768-bit ball of 0.05, whose upper end is the anchor of the 0.05 window
p12=$(CERT_PREC=768 $PY code/theorem.py --check); echo "$p12"
echo; echo "== Piece III: code/gap/check_steps.py data/piece3"
p3=$($PY code/gap/check_steps.py data/piece3); echo "$p3"
echo; echo "== Piece IV: code/rh60route/check_steps.py data/piece4/glue data/piece4/windows.txt --stamp $STAMP"
p4=$($PY code/rh60route/check_steps.py data/piece4/glue data/piece4/windows.txt --stamp "$STAMP"); echo "$p4"
# The same glue without the rule-E record: the lambda_2 bound at 1.92364501953125 is taken from the registered grid record at
# 1.9326171875 by Lemma lem:mono (paper Remark rem:noE).
echo; echo "== Piece IV without rule E: --l2-from 1.92364501953125=1.9326171875"
p4m=$($PY code/rh60route/check_steps.py data/piece4/glue data/piece4/windows.txt --stamp "$STAMP" --l2-from 1.92364501953125=1.9326171875)
echo "$p4m" | grep "lem:mono\|^\[1.91912841796875\|^ALL\|^NOT"

echo; echo "== Records: paper/gen_tables.py (15 gates, schema, provenance); output must equal paper/generated.tex"
fail() { echo "NOT CERTIFIED: $1"; exit 1; }
gen=$($PY paper/gen_tables.py data/piece4/glue data/piece4/windows.txt data/piece3) || fail "record validation (paper/gen_tables.py)"
[ "$gen" = "$(cat paper/generated.tex)" ] && echo "records: OK (paper/generated.tex reproduced)" || fail "paper/generated.tex differs from the records"

echo
echo "$p12" | tail -n 1 | grep -qx "THEOREM CERTIFIED for all L in (0, 1.19]" || fail "Pieces I-II"
e3=$(echo "$p3" | tail -n 1 | sed -n 's/^CERTIFIED: simple-even for all L in \[1\.19, \([0-9.]*\)\].*/\1/p')
[ -n "$e3" ] && awk "BEGIN { exit !($e3 >= 1.4035) }" || fail "Piece III does not reach 1.4035"
echo "$p4" | tail -n 1 | grep -q "^ALL STEPS PASS (53 comparisons): simple-even on \[1.4035, 2\]" || fail "Piece IV"
echo "$p4m" | tail -n 1 | grep -q "^ALL STEPS PASS (53 comparisons): simple-even on \[1.4035, 2\]" || fail "Piece IV without rule E"
echo "COMBINED: Pieces I-II (0, 1.19], Piece III [1.19, $e3], Piece IV [1.4035, 2] (with rule E, and also without it)."
echo "For every L in (0, 2], the lowest eigenvalue of A_L is simple and its eigenfunction is even."
echo "(Computer-assisted, unrefereed, AI-assisted; conditional on the imported trust listed in REVIEWING.md.)"
