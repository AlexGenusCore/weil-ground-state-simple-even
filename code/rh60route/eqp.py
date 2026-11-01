"""Gate G0 ("one form, two codes"): matrix entries of Q_L from the position-side formula, paper eq. (P), in Arb, compared with
the closed forms of entries.py (SPEC §2.2 / PROOFS P5-P6).

Method credit for the closed forms: rh_60 v1 (bramble_trace) and rh_45 v1 (lihongmin), unrefereed AI-agent preprints; this
file is ours and independent of them: g = f * f~ is derived here by product-to-sum on [-L, L] (it does not use the PROOFS P4
translation formulas), and every integral is a rigorous acb.integral.

eq. (P): Q(f) = 4∫_0^{2L} g cosh(x/2) − g(0)(log π + γ + log(1 − e^{−4L})) + ∫_0^{2L} 2[e^{−2x}g(0) − e^{−x/2}g(x)]/(1 − e^{−2x})
         − 2 Σ_{log n<2L} Λ(n)/√n g(log n).
The middle integral has a removable singularity at 0: it is integrated on [δ, 2L], δ = 2^-120, and |∫_0^δ| ≤ 2δ(1.5 g(0) + G1),
G1 = ‖f‖∞² + ‖f‖₂‖f′‖₂ ≥ sup|g′| (spec_changes.md item 1).
Usage: python eqp.py Ldec [prec]  -> prints a JSON record with every comparison; exit status 0 iff all pass."""
import json, sys, time
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flint import arb, acb, ctx
from entries import Form


def modes(F, q):
    """f = 𝒰_ε ẽ_q = Σ a cos(κ x + φ): list of (a, κ, φ)."""
    kap = F.pi * F.k(q) / F.L
    a = (-1) ** q * F.gam(q) / F.L.sqrt()
    return [(a, kap, arb(0) if F.eps == 1 else -F.pi / 2)]


def make_g(F, md):
    L = F.L

    def g(x):  # x: acb (or arb); valid for real x in [0, 2L], analytic continuation elsewhere
        tot = acb(0)
        for i, (ak, kk, pk) in enumerate(md):
            for j, (al, kl, pl) in enumerate(md):
                for s, c, same in ((kk + kl, kl * x + pk + pl, kk.is_zero() and kl.is_zero()), (kk - kl, -kl * x + pk - pl, i == j)):
                    if same: I = (2 * L - x) * acb(c).cos()  # s = 0 exactly (same mode, or the even q = 0 mode twice)
                    else: I = ((s * (L - x) + c).sin() - (-s * L + c).sin()) / s
                    tot += ak * al / 2 * I
        return tot
    return g


def Q_eqP(F, md, prec):
    with ctx.workprec(prec):
        L = F.L; g = make_g(F, md)
        g0 = g(acb(0)).real
        tol = arb(2) ** (-prec + 30)
        I1 = acb.integral(lambda x, an: g(x) * (x / 2).cosh(), 0, 2 * L, rel_tol=tol, abs_tol=tol)
        delta = arb(2) ** -120
        e = lambda z: z.exp()
        I2 = acb.integral(lambda x, an: 2 * (e(-2 * x) * g0 - e(-x / 2) * g(x)) / (1 - e(-2 * x)), delta, 2 * L, rel_tol=tol, abs_tol=tol)
        A1 = sum((abs(a) for a, _, _ in md), arb(0)); Ak = sum((abs(a) * k for a, k, _ in md), arb(0))
        G1 = A1 * A1 + g0.sqrt() * (2 * L).sqrt() * Ak
        I2 = I2.real + arb(0, (2 * delta * (arb(3) / 2 * g0 + G1)).upper())
        pr = sum((w * g(acb(y)).real for w, y in zip(F.w, F.y)), arb(0))
        c = F.logpi + arb.const_euler() + (1 - (-4 * L).exp()).log()
        return 4 * I1.real - g0 * c + I2 - 2 * pr


def closed(F, q, r):
    """A_qr from entries.py (same balls the certifier uses)."""
    lo, hi = min(q, r), max(q, r)
    if q == r: return F.rows(q, q + 1)["A"][0]
    uq, ur = F.rows(lo, lo + 1, diag=False)["u"][0], F.rows(hi, hi + 1, diag=False)["u"][0]
    lq, lr = F.k(lo) ** 2, F.k(hi) ** 2
    return (uq * F.gam(hi) - F.gam(lo) * ur) / (lq - lr)


def run(Ldec, prec=160, K=512, mut=None, tol="1e-30"):
    ctx.prec = prec
    rec = dict(gate="G0", Ldec=Ldec, prec=prec, K=K, mut=mut, entries=[])
    ok = True; t0 = time.time()
    for eps in (1, -1):
        F = Form(Ldec, eps, prec, mut=mut); Fp = Form(Ldec, eps, prec)  # eq. (P) side never sees a mutation
        diag = {}
        qs = sorted({0, 1, 2, K - 1, K, 2 * K, 3, 7})
        for q in qs:
            diag[q] = Q_eqP(Fp, modes(Fp, q), prec)
        pairs = [(q, q) for q in (0, 1, 2, K - 1, K, 2 * K)] + [(0, 1), (1, 2), (3, 7), (K - 1, K)]
        for q, r in pairs:
            if q == r: P = diag[q]
            else: P = (Q_eqP(Fp, modes(Fp, q) + modes(Fp, r), prec) - diag[q] - diag[r]) / 2
            Cf = closed(F, q, r)
            good = bool(P.overlaps(Cf)) and P.rad() < arb(tol) and Cf.rad() < arb(tol)
            ok &= good
            rec["entries"].append(dict(eps=eps, q=q, r=r, eqP=P.str(35), closed=Cf.str(35),
                                       diff=abs(P - Cf).upper().str(3, radius=False), ok=good))
    if Ldec == "2" and mut is None:
        for eps, ref in ((1, "0.0175704652725981700130"), (-1, "0.0574304055992914590")):
            a = Form("2", eps, prec).rows(0, 1)["A"][0]
            good = bool(abs(a - arb(ref)) < arb(10) ** -(len(ref) - 3)); ok &= good
            rec["entries"].append(dict(eps=eps, q=0, r=0, reference=ref, closed=a.str(30), ok=good))
    rec.update(passed=bool(ok), seconds=round(time.time() - t0))
    return rec


if __name__ == "__main__":
    r = run(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 160, mut=(sys.argv[3] if len(sys.argv) > 3 else None))
    print(json.dumps(r, indent=1)); sys.exit(0 if r["passed"] else 1)
