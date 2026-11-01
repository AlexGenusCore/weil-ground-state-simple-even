"""Stage S: certified s >= ||C_p|| = sup spec C_p on L^2(-L, L) (spec Q1), by Elston's Collatz-Wielandt Schur test
(gap/elston/grid_norm.py, MIT; the body of grid_certificate_rigorous.mu_upper with a = b = L, keeping the float Galerkin top).
The window L is the exact dyadic of liu.Lwin, which is float-exact, so Elston's float arguments see the exact window (M2).
Usage: python stage_s.py Ldec [K_cells iters]  ->  $LIU_DATA/s/s_<Ldec>.json"""
import json, math, os, sys, time
import liu
from fractions import Fraction
from flint import arb, ctx
import grid_norm as gn

Ldec = sys.argv[1]; Kc = int(sys.argv[2]) if len(sys.argv) > 2 else 8000; iters = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
Lid, Lq, La = liu.Lwin(Ldec); b = float(Lq); assert Fraction(b) == Lq  # float-exact window
ctx.prec = 200
for n in range(2, int(math.exp(2 * b)) + 3):  # prime set decided away from the boundary (float tests in Elston agree)
    assert abs(arb(n).log() - 2 * La) > arb(2) ** -40, n
t = time.time()
w = gn.weights("zeta", b, comb_a=b)
mu_top, A, it, vec = gn.top_eigenvalue(w, b, Kc)
n_list = [n for n in range(2, int(math.exp(2 * b)) + 1) if any(abs(math.log(n) - l) < 1e-12 for l, _ in w)]
assert all(arb(n).log() < 2 * La for n in n_list) and len(n_list) == len(w)
phi = gn.schur_weight(n_list, b, Kc, vec, iters=iters)
s = gn.schur_upper(n_list, b, Kc, phi)  # exact dyadic upper bound
m, e = s.mid().man_exp(); sq = Fraction(int(m)) * Fraction(2) ** int(e)
assert arb(sq.numerator) / sq.denominator == s
rec = dict(Ldec=Ldec, L=Lid, s=f"{sq.numerator}/{sq.denominator}", s_float=float(sq), mu_top_float=mu_top, slack=float(sq) - mu_top,
           K_cells=Kc, iters=iters, n_list=n_list, seconds=round(time.time() - t), peak_gb=round(liu.peak_gb(), 2))
os.makedirs(os.path.join(liu.DATA, "s"), exist_ok=True)
out = os.path.join(liu.DATA, "s", f"s_{Ldec}.json"); assert not os.path.exists(out)
json.dump(rec, open(out, "w"), indent=1); print(json.dumps(rec))
