"""Piece III gluing: for consecutive windows L_i < L_{i+1}, check min(l2_even, l1_odd)(L_{i+1}) > U(L_i) (paper, Cor. 3.2).
Inputs (directory argument, default ./out): upper*.jsonl (fr_sweep, field lam0_upper, rigorous outward-rounded upper ends; every
run is a valid upper bound, so the smallest one per L is used),
g_<L>_odd.json and g_<L>_l2.json (Elston certifier; field certified_lower_bound, an Arb ball whose lower end is used).
U(1.19) = 1.312e-47 is Piece II's certified upper bound (theorem_bounds.json of the (0, 1.19] release).
All comparisons are done in Arb: a step passes only if the lower end of the left side exceeds the upper end of U.
A one-point grid applies paper Cor. cor:criterion pointwise at that L: U(L) < min(l2_even, l1_odd)(L) (rh60route review R1).
A PASS needs at least one comparison, and a missing input is a FAIL (R1). U is the minimum over every upper*.jsonl row in dir,
so a gluing directory must hold only the intended upper-bound files (R10). Files are matched by the exact L string (R13).
Provenance (rh60route AUDIT F6): every input that is an rh60route certifier record (it has "gates"), and every input at all when
--stamp SHA256 is given, must have result == "PASS", Ldec == the L of its file name, mut == null, the sector of its kind (odd:
eps = −1; l2: eps = +1, deflated) and stamp_sha256 == SHA256 (so an rh60route record always needs --stamp); otherwise it is
rejected (printed) and counts as missing.
--l2-from L=L* (rh60route PREREG_GAP fallback, paper Lemma lem:mono): the l2 bound at window L is read from g_<L*>_l2.json, with
L* > L and the same F6 checks against L*; valid since lambda_2^ev(L) >= lambda_2^ev(L*) for L <= L*.
Usage: python check_steps.py [dir] [grid] [--stamp SHA256] [--l2-from L=L* ...]   (grid: comma list "2" or "1.19,1.2205,...", or a file with one L per line)"""
import sys, json, os
from fractions import Fraction
from flint import arb

argv = sys.argv[1:]; stamp = None
if "--stamp" in argv: i = argv.index("--stamp"); stamp = argv[i + 1]; del argv[i:i + 2]
mono = {}
while "--l2-from" in argv: i = argv.index("--l2-from"); a_, b_ = argv[i + 1].split("="); mono[a_] = b_; del argv[i:i + 2]
assert all(Fraction(b_) > Fraction(a_) for a_, b_ in mono.items()), "--l2-from needs L* > L (lem:mono)"
sys.argv[1:] = argv
d = sys.argv[1] if len(sys.argv) > 1 else "out"
U = {"1.19": arb("1.312e-47")}
for fn in sorted(f for f in os.listdir(d) if f.startswith("upper") and f.endswith(".jsonl")):
    for line in open(os.path.join(d, fn)):
        r = json.loads(line)
        if r.get("par", 0) == 0 and (r["L"] not in U or arb(r["lam0_upper"]) < U[r["L"]]): U[r["L"]] = arb(r["lam0_upper"])
grid = ["1.19", "1.2205", "1.25", "1.2785", "1.3055", "1.3315", "1.3565", "1.3805", "1.4035", "1.4255", "1.447", "1.468", "1.4885", "1.5"]
if len(sys.argv) > 2:
    g = sys.argv[2]
    grid = [x.strip() for x in (open(g).read().split() if os.path.exists(g) else g.split(",")) if x.strip()]

def lower(L, kind):
    if kind == "l2" and L in mono: print(f"  l2 at {L} from {mono[L]} (lem:mono)"); L = mono[L]
    p = os.path.join(d, f"g_{L}_{kind}.json")
    if not os.path.exists(p): return None
    r = json.load(open(p))
    if "gates" in r or stamp:  # F6
        sector = (r.get("eps"), bool(r.get("deflate"))) == ((-1, False) if kind == "odd" else (1, True))
        bad = [k for k, ok in (("result", r.get("result") == "PASS"), ("Ldec", r.get("Ldec") == L), ("mut", r.get("mut") is None),
                               ("sector", sector), ("stamp", stamp is not None and r.get("stamp_sha256") == stamp)) if not ok]
        if bad: print(f"  {os.path.basename(p)} rejected: {', '.join(bad)}"); return None
    v = r.get("certified_lower_bound")
    return arb(v).lower() if v else None

ok_all, worst, n_cmp = True, None, 0
print(f"{'step':>17}  {'U(L_i)':>12}  {'l2_even(L_i+1)':>15}  {'l1_odd(L_i+1)':>14}  ratio   pass")
for a, b in (zip(grid, grid[1:]) if len(grid) > 1 else [(grid[0], grid[0])]):  # one point: pointwise criterion
    u, l2, lo = U.get(a), lower(b, "l2"), lower(b, "odd")
    if None in (u, l2, lo):
        print(f"[{a}, {b}]  missing: {'U ' if u is None else ''}{'l2 ' if l2 is None else ''}{'odd' if lo is None else ''}"); ok_all = False; continue
    m = l2 if l2 < lo else lo
    passed = m > u.upper()
    ratio = m / u.upper(); worst = ratio if worst is None or ratio < worst else worst
    ok_all &= bool(passed); n_cmp += 1
    print(f"[{a}, {b}]  {u.upper().str(4, radius=False):>12}  {l2.str(4, radius=False):>15}  {lo.str(4, radius=False):>14}  {ratio.str(3, radius=False):>5}  {passed}")
span = f"[{grid[0]}, {grid[-1]}]" if len(grid) > 1 else f"L = {grid[0]} (pointwise)"
ok_all = ok_all and n_cmp > 0
print(f"ALL STEPS PASS ({n_cmp} comparisons): simple-even on {span}" if ok_all else f"NOT (yet) certified on {span} ({n_cmp} comparisons)",
      f"(minimum step ratio {worst.str(4, radius=False)})" if worst is not None else "")
