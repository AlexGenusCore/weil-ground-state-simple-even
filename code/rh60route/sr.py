"""Lemma SR (PROOFS P23; SPEC §8 with review fixes R5, R6, R15): exact structured LDL^T of S_input − δ_0 I.

ref(): Python-int reference (identical arithmetic to sr.c); kernel(): the C/GMP production kernel (sr_kernel); eps_E(): exact
ε_E from the kernel totals; float_ldl(): the float64 proposal (chooses μ only, no rigour).
Labels (AUDIT F3): every row j carries its exact integer label lab_j = 4λ_j, passed explicitly; λ_j − λ_i = (lab_j − lab_i)/4.
Method credit: the structured Schur recursion is rh_60 v1's (bramble_trace, unrefereed AI-agent preprint), replaced here by our
exact-integer Lemma SR with explicit residual (PROOFS P23). Clean room: no rStation code was used."""
import os, subprocess, tempfile, time
from fractions import Fraction
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def cdiv2(x, s):  # ceil(x / 2^s) for Python ints
    return -((-x) >> s)


def check_lab(lab):
    assert all(b > a and (b - a) % 4 == 0 for a, b in zip(lab, lab[1:])), "labels must increase in steps = 0 mod 4"


def ref(H, Dv, Jm, P, lab):
    """Python reference. H: list of n lists of D ints (2^P h), Dv: n ints (2^P d), lab: n ints (4λ). Same record as sr.c."""
    check_lab(lab)
    H = [list(r) for r in H]; Dv = list(Dv); n, D = len(H), len(Jm)
    J1 = sum(abs(c) for row in Jm for c in row)
    T = 0; fail = -1; minp = Dv[0] if n else 0; sump = 0; sumL = 0
    for i in range(n):
        if Dv[i] <= 0: fail = i; break
        minp = min(minp, Dv[i]); sump += Dv[i]
        g = [sum(Jm[a][b] * H[i][b] for b in range(D)) for a in range(D)]
        E = Lm = Gm = 0
        for j in range(i + 1, n):
            nu = sum(H[j][a] * g[a] for a in range(D))
            den = (lab[j] - lab[i]) // 4 * Dv[i]
            L_, rem = divmod(nu, den)
            E = max(E, rem); Lm = max(Lm, abs(L_)); sumL += L_
            for a in range(D):
                H[j][a] -= cdiv2(L_ * H[i][a], P); Gm = max(Gm, abs(H[j][a]))
            Dv[j] -= cdiv2(L_ * L_ * Dv[i], 2 * P)
        Gm += 1
        T += (E << P) + 2 * Lm * E + J1 * (2 * Gm + 1) * (1 << P)
    r = dict(fail=fail, n=n, D=D, P=P, J1=J1, T=T, minp=minp, sump=sump, sumL=sumL)
    if fail >= 0: r["failpivot"] = Dv[fail]
    return r


def kernel(H, Dv, Jm, P, lab, workdir=None, log=None):
    """Run sr_kernel; returns the parsed record (ints) plus seconds."""
    n, D = len(H), len(Jm); check_lab(lab)
    fd, path = tempfile.mkstemp(suffix=".sr", dir=workdir); os.close(fd)
    with open(path, "w") as f:
        f.write(f"{n} {D} {P}\n" + " ".join(str(c) for row in Jm for c in row) + "\n")
        for r, d, l in zip(H, Dv, lab): f.write(" ".join(format(x, "x") for x in r) + " " + format(d, "x") + f" {l}\n")
    t = time.time()
    out = subprocess.run([os.path.join(HERE, "sr_kernel"), path], capture_output=True, text=True, check=True)
    os.remove(path)
    rec = {}
    for kv in out.stdout.split():
        k, v = kv.split("=")
        rec[k] = int(v, 16) if k in ("T", "minp", "sump", "sumL", "failpivot") else int(v)
    rec["seconds"] = round(time.time() - t, 1)
    return rec


def eps_E(rec, HS):
    """ε_E = n 2^-P + H_S T / 2^{3P} (exact Fraction; HS a Fraction ≥ sup_i Σ_{j≠i} 1/|λ_i − λ_j|)."""
    P = rec["P"]
    return Fraction(rec["n"], 1 << P) + HS * Fraction(rec["T"], 1 << (3 * P))


def float_ldl(H, d, Jm, lab):
    """Float64 proposal of the same recursion (no flooring); returns min pivot. Rows H (n x D float), d (n), labels lab = 4λ."""
    H = np.array(H, dtype=float); d = np.array(d, dtype=float); J = np.array(Jm, dtype=float); n = len(d)
    lam = np.array(lab, dtype=float) / 4
    pmin = np.inf
    for i in range(n):
        p = d[i]; pmin = min(pmin, p)
        if p <= 0: return p, i
        g = J @ H[i]
        nu = H[i + 1:] @ g
        l = nu / ((lam[i + 1:] - lam[i]) * p)
        H[i + 1:] -= np.outer(l, H[i]); d[i + 1:] -= p * l * l
    return pmin, -1


if __name__ == "__main__":  # self-check: kernel == reference on random instances (also part of G3)
    import random
    rnd = random.Random(7)
    for D, m in ((4, 2), (8, 4)):
        Jb = [[0] * m for _ in range(m)]
        for a in range(0, m, 2): Jb[a][a + 1], Jb[a + 1][a] = 1, -1
        Jm = [[0] * D for _ in range(D)]
        for a in range(m):
            for b in range(m): Jm[a][b] = Jb[a][b]
            Jm[a][m + a] = -1; Jm[m + a][a] = 1
        for w2 in (0, 1):
            n, P, q0 = 40, 30, 7
            H = [[rnd.randrange(-2 ** 34, 2 ** 34) for _ in range(D)] for _ in range(n)]
            Dv = [rnd.randrange(2 ** 33, 2 ** 35) for _ in range(n)]
            lab = [(2 * (q0 + j) + w2) ** 2 for j in range(n)]
            a, b = ref(H, Dv, Jm, P, lab), kernel(H, Dv, Jm, P, lab)
            b.pop("seconds"); assert a == b, (a, b)
    print("sr kernel == reference OK")
