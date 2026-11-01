"""Gate G-S input (review R9): float Rayleigh-Ritz value of the prime comb C_L in the trigonometric basis, both parities.
Ritz values are lower bounds on sup spec C_L, so a valid s(L) must exceed them; this catches gross errors in s only.
Entries: −(B_p)_qr = −(2γ_qγ_r/L)[κ_q S(κ_q) − κ_r S(κ_r)]/(κ_q² − κ_r²), −(B_p)_qq = 2γ²C(κ) − γ²S(κ)/(Lκ) (PROOFS P5/P6).
Method credit: trig basis and translation integrals as in rh_45/rh_60 (unrefereed AI-agent preprints), re-derived in PROOFS P4.
Usage: python ritz.py Ldec [K] -> ritz_<Ldec>.json"""
import json, sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from flint import ctx
from entries import Form

Ldec = sys.argv[1]; K = int(sys.argv[2]) if len(sys.argv) > 2 else 1600
rec = dict(Ldec=Ldec, K=K)
for eps, name in ((1, "ritz_ev"), (-1, "ritz_od")):
    ctx.prec = 64
    F = Form(Ldec, eps, 64)
    S, C = F.trig(0, K)
    L = float(F.L); kap = np.array([float(F.pi * F.k(q) / F.L) for q in range(K)])
    g = np.array([float(F.gam(q)) for q in range(K)]); S = np.array([float(x) for x in S]); C = np.array([float(x) for x in C])
    kS = kap * S
    with np.errstate(divide="ignore", invalid="ignore"):
        B = (2 / L) * np.outer(g, g) * (kS[:, None] - kS[None, :]) / (kap[:, None] ** 2 - kap[None, :] ** 2)
        d = -2 * g ** 2 * C + np.where(kap > 0, g ** 2 * S / (L * np.where(kap > 0, kap, 1)), 0.0)
    if eps == 1: d[0] = -2 * C[0]  # even q = 0: I_00 is doubled, the prime term is −2C(0), no γ_0² (SPEC §2.2; amendment A1)
    np.fill_diagonal(B, d)
    rec[name] = float(np.linalg.eigvalsh(-B)[-1])
json.dump(rec, open(f"ritz_{Ldec}.json", "w")); print(json.dumps(rec))
