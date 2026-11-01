"""Input-independent checks (AUDIT F1 and F7), in mpmath point arithmetic: gates, never certificates.

G0i (F1): matrix entries by paper eq. (P) with the G6 auditor's own prime list, weights, γ_q, k_q and modes (mp_entries.py, a
  verbatim copy of audit/mp_entries.py, written from eq. (P) without reading entries.py), compared with the closed forms the
  certifier uses. A shared input error (prime list, Λ(n), γ_0, ...) that the Arb G0 cannot see (it reads its inputs from
  entries.Form) fails here.
C-ind (F7): τ_core(N), τ_pole(N), t_N and r_M recomputed from SPEC §6 / PROOFS P14-P18, P22 with code that shares nothing with
  certify.py's stage F: own prime list, V_h, E_h, r̄, J_2, J_4, u_q (auditor's closed form), moments, F0/F1, L_ab, τ and r_M
  formulas, 𝒯 rows taken from the SPEC T1 table. Inputs from the run: the certified core solves (cross-checked by G5 against an
  independent Arb core solve), the generators 𝒢_i on [K, N) for S_a (cross-checked by G5′), the balancing powers, N, M, μ, s.
  The run's values are Arb upper ends of the same formulas, so they must lie in [mp, mp(1 + slack)]: a factor-2 error either way
  fails. The moment/τ code follows the auditor's audit/mp_tau.py (generalised here to deflation and r_M).
Method credit: rh_60 v1 (bramble_trace) and rh_45 v1 (lihongmin), unrefereed AI-agent preprints; this file is ours.
Usage: python indep.py g0i Ldec [dps]   -> JSON for both sectors; exit 0 iff all pass."""
import json, math, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import mpmath as mp
import mp_entries as mpe

PAIRS = [(0, 0), (1, 1), (2, 2), (7, 7), (40, 40), (0, 1), (3, 7), (2, 40)]  # the auditor's set (AUDIT §1a)


def amp(x):  # exact mpf of an arb midpoint (rounded to the working precision)
    m, e = x.mid().man_exp()
    return mp.ldexp(mp.mpf(int(m)), int(e))


def g0i(Ldec, eps, closed, dps=30, tol="1e-20"):
    """closed(q, r) -> arb (the certifier's closed form). Passes iff |eq.(P) − closed| ≤ tol at every pair."""
    with mp.workdps(dps):
        L = mp.mpf(Ldec); rows = []; ok = True
        for q, r in PAIRS:
            v = mpe.entry(L, eps, q, r); c = closed(q, r)
            d = abs(v - amp(c)); good = bool(d <= mp.mpf(tol) and float(c.rad()) < 1e-30)
            ok &= good; rows.append(dict(q=q, r=r, eqP=mp.nstr(v, 25), diff=mp.nstr(d, 3), ok=good))
        return dict(ok=ok, n_pp=len(mpe.prime_powers(L)), dps=dps, tol=tol, entries=rows)


def far(Ldec, eps, K, N, M, deflate, sol, scal, mu, s, G, run, dps, slack=1e-3):
    """sol: {'a','b'(,'eh','e')}: lists of K arb; scal: balancing Fractions per 𝒯 row; mu, s: Fractions; G: list of generator
    rows (arb) for q = K, K+1, ... (only [K, N) is used); run: dict of the run's tc, tp, rM (arb), tpN, tpM (Fractions)."""
    with mp.workdps(dps):
        L = mp.mpf(Ldec); w = mp.mpf(0) if eps == 1 else mp.mpf(1) / 2; pi = mp.pi
        pp = mpe.prime_powers(L)
        wn = [mp.log(p) / mp.sqrt(n) for n, p in pp]; yn = [mp.log(n) for n, _ in pp]
        alpha = mp.sinh(L / 2) ** 2 if eps == 1 else -mp.cosh(L / 2) ** 2
        J = 1
        while mp.exp(-2 * (2 * J + mp.mpf(1) / 2) * L) > mp.mpf(10) ** (-dps - 5): J += 1
        cj = [2 * j + mp.mpf(1) / 2 for j in range(J)]; eta = [mp.exp(-2 * c * L) for c in cj]
        k = lambda q: q + w
        gam = lambda q: 1 / mp.sqrt(2) if (eps == 1 and q == 0) else mp.mpf(1)

        def u_of(q):  # SPEC §2.2: u_q = γ_q (2L/π²) Φ_ε(κ_q)
            kap = pi * k(q) / L
            if kap == 0: return gam(q) * 2 * L / pi ** 2 * (-alpha * 4)
            S = mp.fsum(a * mp.sin(kap * y) for a, y in zip(wn, yn)); ps = mp.digamma(mp.mpf(1) / 4 + 1j * kap / 2); x2 = kap ** 2
            F = kap / 2 * mp.im(ps) - eps * x2 * mp.fsum(e / (c * c + x2) for e, c in zip(eta, cj)) - alpha / (mp.mpf(1) / 4 + x2)
            return gam(q) * 2 * L / pi ** 2 * (kap * S + F)

        X = dict(u=[u_of(q) for q in range(K)], v=[gam(q) for q in range(K)])
        Y = {y: [amp(x) for x in vec] for y, vec in sol.items()}
        lam = [k(q) ** 2 for q in range(K)]; ls = k(K - 1) ** 2; th = [l / ls for l in lam]
        # SPEC T1 rows (δ_1, δ_2), entry 1 = ±R_{x,y} on u_q, entry 2 = ±R_{x,y} on v_q; order U, V, Y(=ê), X(=e)
        rows = [((1, 0), ("v", "a"), ("u", "a")), ((0, 1), ("v", "b"), ("u", "b"))]
        if deflate: rows += [((0, 0), ("v", "eh"), ("u", "eh")), ((0, 0), ("v", "e"), ("u", "e"))]
        sc = [abs(mp.mpf(f.numerator) / f.denominator) for f in scal]
        keys = {xy for r in rows for xy in r[1:]}
        c = {(x, y): [a * b for a, b in zip(X[x], Y[y])] for x, y in keys}
        Af = {kk: mp.fsum(abs(t) for t in cv) for kk, cv in c.items()}
        mom = {kk: [] for kk in c}; pw = {kk: list(cv) for kk, cv in c.items()}

        def m_r(kk, r):  # moments m_r = Σ c_i θ_i^r, extended on demand
            while len(mom[kk]) <= r:
                mom[kk].append(mp.fsum(pw[kk])); pw[kk] = [p * t for p, t in zip(pw[kk], th)]
            return mom[kk][r]

        def F01(kk, z0):  # PROOFS P14, R rule of SPEC 6.2 (start 96, step 8)
            t = ls / z0; A = Af[kk]; R = 96
            while True:
                F0 = mp.fsum(abs(m_r(kk, r)) * t ** r for r in range(R)) + A * t ** R / (1 - t)
                if A * t ** R <= mp.mpf(2) ** -64 * F0: break
                R += 8
            F1 = mp.fsum((r + 1) * abs(m_r(kk, r)) * t ** r for r in range(R)) + A * t ** R * (R + 1 - R * t) / (1 - t) ** 2
            return F0, F1

        def bounds(z0):  # per balanced row ρ and column a: |𝒯_ρa| ≤ T0 = 2^τρ(|δ_ρa| + F0/z0), |z² 𝒯′_ρa| ≤ T1 = 2^τρ F1
            F = {kk: F01(kk, z0) for kk in keys}
            T0 = [[sc[i] * (r[0][a] + F[r[1 + a]][0] / z0) for a in range(2)] for i, r in enumerate(rows)]
            T1 = [[sc[i] * F[r[1 + a]][1] for a in range(2)] for i, r in enumerate(rows)]
            return T0, T1

        pairs = [(2 * p, 2 * p + 1) for p in range(len(rows) // 2)]; pairs += [(b, a) for a, b in pairs]  # |J_b| = 1 on these
        V = mp.fsum(x * x for x in wn) / 2; Vh = mp.mpf(1) / 4 + 4 / pi ** 2 * V
        phis = [pi * y / L for y in yn]
        E1 = mp.fsum(x / abs(mp.sin(t / 2)) for x, t in zip(wn, phis))
        E = mp.fsum(wn[i] * wn[j] / (2 * abs(mp.sin((phis[i] - phis[j]) / 2))) for i in range(len(wn)) for j in range(len(wn)) if i != j) \
            + mp.fsum(wn[i] * wn[j] / (2 * abs(mp.sin((phis[i] + phis[j]) / 2))) for i in range(len(wn)) for j in range(len(wn)))
        Eh = 2 / pi * E1 + 4 / pi ** 2 * E
        J2 = lambda n: Vh / (k(n) - 1) + Eh / k(n) ** 2
        J4 = lambda n: 1 / (3 * (k(n) - 1) ** 3)
        rbar = 2 * L / pi ** 2 * (1 + mp.exp(-L) / (1 - mp.exp(-4 * L)) + abs(alpha) / (mp.mpf(1) / 4 + (pi * k(K) / L) ** 2))
        Hk = lambda q: mp.re(mp.digamma(mp.mpf(1) / 4 + 1j * pi * k(q) / (2 * L))) - mp.log(pi)
        # τ_core (P15, P18)
        z0 = k(N) ** 2; Tb, T1 = bounds(z0)
        Lab = [[mp.fsum(Tb[r][a] * T1[s_][b] for r, s_ in pairs) for b in range(2)] for a in range(2)]
        j2, j4 = J2(N), J4(N)
        tau = Lab[0][0] * j2 + (2 * rbar * Lab[0][0] + Lab[0][1] + Lab[1][0]) * mp.sqrt(j2 * j4) \
            + (rbar ** 2 * Lab[0][0] + rbar * (Lab[0][1] + Lab[1][0]) + Lab[1][1]) * j4
        taup = 2 * L ** 3 / pi ** 4 * mp.cosh(L / 2) ** 2 * j4 if eps == -1 else mp.mpf(0)
        fr = lambda f: mp.mpf(f.numerator) / f.denominator
        tN = Hk(N) - fr(mu) - fr(s) - tau - taup; tM = Hk(M) - fr(mu) - fr(s) - tau - taup
        # r_M (P22)
        with mp.workdps(30):
            Sa = [mp.fsum(amp(G[i][r]) ** 2 for i in range(N - K)) for r in range(len(rows))]
        A0, _ = bounds(k(M) ** 2)
        beta = [A0[r][0] * mp.sqrt(J2(M)) + (A0[r][0] * rbar + A0[r][1]) * mp.sqrt(J4(M)) for r in range(len(rows))]
        varrho = k(N - 1) / k(M)
        rM = mp.fsum(mp.sqrt(Sa[a]) * beta[b] for a, b in pairs) ** 2 / (tM * (1 - varrho ** 2) ** 2)

        def near(run_v, mp_v):  # run is an Arb upper end of the same formula: mp ≤ run ≤ mp (1 + slack)
            r_ = amp(run_v.upper()) if hasattr(run_v, "upper") else mp.mpf(run_v)
            if mp_v == 0: return bool(r_ == 0), 0.0
            q = r_ / mp_v; return bool(1 - mp.mpf(10) ** -9 <= q <= 1 + slack), float(q - 1)
        res = {}
        for name, rv, mv in (("tau_core", run["tc"], tau), ("tau_pole", run["tp"], taup), ("r_M", run["rM"], rM)):
            ok, d = near(rv, mv); res[name] = dict(mp=mp.nstr(mv, 12), rel_excess=d, ok=ok)
        tpN = fr(run["tpN"]); okt = bool(tN - mp.mpf(2) ** -39 - mp.mpf(10) ** -9 <= tpN <= tN + mp.mpf(10) ** -9)
        res["t_N"] = dict(mp=mp.nstr(tN, 12), tprime_N=mp.nstr(tpN, 12), ok=okt)
        res["L_ab"] = [mp.nstr(x, 8) for r in Lab for x in r]; res["n_pp"] = len(pp); res["dps"] = dps
        res["ok"] = all(v["ok"] for v in res.values() if isinstance(v, dict))
        return res


if __name__ == "__main__":
    from flint import ctx
    from entries import Form
    import eqp
    assert sys.argv[1] == "g0i", __doc__
    Ldec = sys.argv[2]; dps = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    ctx.prec = 160; t0 = time.time(); out = dict(gate="G0i", Ldec=Ldec)
    for eps in (1, -1):
        F = Form(Ldec, eps, 160)
        out["ev" if eps == 1 else "od"] = g0i(Ldec, eps, lambda q, r: eqp.closed(F, q, r), dps)
    out["passed"] = out["ev"]["ok"] and out["od"]["ok"]; out["seconds"] = round(time.time() - t0)
    import hashlib; out["sha256"] = {f: hashlib.sha256(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), f), "rb").read()).hexdigest()
                                     for f in ("indep.py", "mp_entries.py", "entries.py", "eqp.py")}
    print(json.dumps(out, indent=1)); sys.exit(0 if out["passed"] else 1)
