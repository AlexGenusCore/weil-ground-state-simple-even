"""G6 auditor: independent mpmath evaluation of Weil-form matrix entries by paper eq. (P), and of the far-block constants.
Written from the paper's eq. (P) and the SPEC formulas only; imports nothing from rh60route/code. Usage:
  python mp_entries.py entries  Ldec eps q[,r] ...      -> JSON lines {L, eps, q, r, val}
  python mp_entries.py consts   Ldec eps K N M          -> JSON with V_h, E_h, rbar, J2, J4, tau_pole, H, H(kappa_N), H(kappa_M), pole_sum
"""
import json, sys
import mpmath as mp

mp.mp.dps = 50


def prime_powers(L):
    out, X, n = [], mp.exp(2 * L), 2
    while n < X:
        p = next(d for d in range(2, n + 1) if n % d == 0)
        m = n
        while m % p == 0: m //= p
        if m == 1: out.append((n, p))
        n += 1
    return out


def mode(L, eps, q):  # f = a cos(kappa x + phi) on [-L, L], the conjugated parity basis vector of index q
    w = 0 if eps == 1 else mp.mpf(1) / 2
    gam = 1 / mp.sqrt(2) if (eps == 1 and q == 0) else mp.mpf(1)
    return ((-1) ** q * gam / mp.sqrt(L), mp.pi * (q + w) / L, mp.mpf(0) if eps == 1 else -mp.pi / 2)


def gfun(L, md):
    """g(x) = int_{x-L}^{L} f(y) f(y-x) dy for x in [0, 2L], f = sum a cos(k y + p)."""
    def g(x):
        s = mp.mpf(0)
        for ak, kk, pk in md:
            for al, kl, pl in md:
                for sg, c in ((kk + kl, pk + pl - kl * x), (kk - kl, pk - pl + kl * x)):
                    if abs(sg) < mp.mpf(10) ** (-mp.mp.dps + 5):
                        I = (2 * L - x) * mp.cos(c)
                    else:
                        I = (mp.sin(sg * L + c) - mp.sin(sg * (x - L) + c)) / sg
                    s += ak * al / 2 * I
        return s
    return g


def Q(L, md, pts):
    g = gfun(L, md); g0 = g(mp.mpf(0))
    I1 = 4 * mp.quad(lambda x: g(x) * mp.cosh(x / 2), pts)
    I2 = mp.quad(lambda x: 2 * (mp.exp(-2 * x) * g0 - mp.exp(-x / 2) * g(x)) / (1 - mp.exp(-2 * x)), pts)
    pr = sum(mp.log(p) / mp.sqrt(n) * g(mp.log(n)) for n, p in prime_powers(L))
    return I1 - g0 * (mp.log(mp.pi) + mp.euler + mp.log(1 - mp.exp(-4 * L))) + I2 - 2 * pr


def entry(L, eps, q, r):
    kmax = max(q, r) + 1
    pts = mp.linspace(0, 2 * L, 4 * kmax + 9)
    if q == r: return Q(L, [mode(L, eps, q)], pts)
    a, b = mode(L, eps, q), mode(L, eps, r)
    return (Q(L, [a, b], pts) - Q(L, [a], pts) - Q(L, [b], pts)) / 2


def Hk(L, k):  # archimedean symbol at kappa = pi k / L
    return mp.re(mp.digamma(mp.mpf(1) / 4 + 1j * mp.pi * k / (2 * L))) - mp.log(mp.pi)


def consts(L, eps, K, N, M):
    w = 0 if eps == 1 else mp.mpf(1) / 2
    pp = prime_powers(L)
    wn = [mp.log(p) / mp.sqrt(n) for n, p in pp]; th = [mp.pi * mp.log(n) / L for n, _ in pp]
    V = sum(x * x for x in wn) / 2; Vh = mp.mpf(1) / 4 + 4 / mp.pi ** 2 * V
    E1 = sum(x / abs(mp.sin(t / 2)) for x, t in zip(wn, th))
    E = sum(wn[i] * wn[j] / (2 * abs(mp.sin((th[i] - th[j]) / 2))) for i in range(len(wn)) for j in range(len(wn)) if i != j) \
        + sum(wn[i] * wn[j] / (2 * abs(mp.sin((th[i] + th[j]) / 2))) for i in range(len(wn)) for j in range(len(wn)))
    Eh = 2 / mp.pi * E1 + 4 / mp.pi ** 2 * E
    alpha = mp.sinh(L / 2) ** 2 if eps == 1 else -mp.cosh(L / 2) ** 2
    kK = K + w; kapK = mp.pi * kK / L
    rbar = 2 * L / mp.pi ** 2 * (1 + mp.exp(-L) / (1 - mp.exp(-4 * L)) + abs(alpha) / (mp.mpf(1) / 4 + kapK ** 2))
    kN = N + w; kM = M + w
    J2 = Vh / (kN - 1) + Eh / kN ** 2; J4 = 1 / (3 * (kN - 1) ** 3)
    taup = 2 * L ** 3 / mp.pi ** 4 * mp.cosh(L / 2) ** 2 * J4 if eps == -1 else mp.mpf(0)
    mp.mp.dps = 20
    psum = mp.fsum(2 / L * mp.cosh(L / 2) ** 2 / (mp.mpf(1) / 4 + (mp.pi * (q + w) / L) ** 2) ** 2 for q in range(N, M)) if eps == -1 else 0
    mp.mp.dps = 50
    Hc = (1 + mp.log(N - K)) / K
    return dict(n_pp=len(pp), last_pp=pp[-1][0], V_h=mp.nstr(Vh, 15), E_h=mp.nstr(Eh, 15), rbar=mp.nstr(rbar, 12), J2=mp.nstr(J2, 10),
                J4=mp.nstr(J4, 10), tau_pole=mp.nstr(taup, 10), H=mp.nstr(Hc, 10), H_kN=mp.nstr(Hk(L, kN), 20), H_kM=mp.nstr(Hk(L, kM), 20),
                pole_sum=mp.nstr(psum, 6) if eps == -1 else "0", varrho=mp.nstr((N - 1 + w) / kM, 12))


if __name__ == "__main__":
    cmd, Ldec, eps = sys.argv[1], sys.argv[2], int(sys.argv[3]); L = mp.mpf(Ldec)
    if cmd == "entries":
        for qr in sys.argv[4:]:
            q, r = (list(map(int, qr.split(","))) + [None])[:2]; r = q if r is None else r
            print(json.dumps(dict(L=Ldec, eps=eps, q=q, r=r, val=mp.nstr(entry(L, eps, q, r), 42))), flush=True)
    else:
        K, N, M = map(int, sys.argv[4:7])
        print(json.dumps(consts(L, eps, K, N, M)))
