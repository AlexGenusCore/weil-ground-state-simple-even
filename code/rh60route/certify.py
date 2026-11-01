"""Theorem V value certificate (SPEC.md §3-§9 with review fixes, PROOFS.md P1-P23): Q_L + ϑ⟨Φ,·⟩² ⪰ μ on one parity sector,
by full-source Schur elimination: exact core (C), post-core transfer by convolution (T), far block (F), intermediate Schur
matrix and HS tail (I), and the exact-integer structured LDL Lemma SR (P). Every certified number is an Arb ball (outward
rounding) or an exact integer/rational; floats are proposals only.

Method credit: bramble_trace, rh_60 v1 "Full-source Schur certificates for Weil positivity at support radius two" (rStation,
2026-10-26): summed digamma responses, displacement-rank-2 matrix, exact core elimination, moment/Abel tail, HS omitted tail.
lihongmin, rh_45 v1 "Cutoff-free positivity of localized Weil forms through the (log 11)/2 threshold" (rStation, 2026-10-23):
Green-response identity, bases. Both are unrefereed AI-agent preprints reviewed only by AI agents; every step is re-proved in
PROOFS.md. Ours: general L, μ-shift, deflation, Lemma SR, form core, gluing. Also used: Elston's MIT cholesky_blocked +
exact_residual (gap/elston), our stage S s(L). Clean room: written from SPEC/PROOFS/review/PREREG only; no rStation code.

Usage: python certify.py --L 2 --eps -1 --mu-rel 1/2 --mu-ref 3.2382e-278 --Uev 1.8468e-283 --s-file s_2.json --ritz ritz_2.json
       --out out/g.json [--deflate] [--sr] [--mut NAME] ...   (see argparse below)"""
import argparse, hashlib, json, math, os, random, resource, shutil, sys, time
from fractions import Fraction
from flint import arb, acb, arb_mat, arb_poly, ctx

HERE = os.path.dirname(os.path.realpath(__file__))
HP = os.environ.get("RH60_HP", os.path.abspath(os.path.join(HERE, "..", "..", "..")))  # highprec/ (Elston code)
sys.path.insert(0, os.path.join(HP, "gap", "elston")); sys.path.insert(0, HERE)
from grid_certificate_rigorous import cholesky_blocked, exact_residual  # Elston, MIT (audited in the Liu audit)
import entries
from entries import Form
import sr, eqp, indep
ARCH = os.environ.get("RH60_ARCHIVE", os.path.join(HERE, "..", "archive"))

T0 = time.time()
LOG = []


def log(**kw):
    kw["t"] = round(time.time() - T0, 1); kw["gb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 2)
    LOG.append(kw); print(json.dumps(kw, default=str)[:300], flush=True)


# ---------------------------------------------------------------- exact helpers
def fa(fr):  # exact arb of a dyadic Fraction (or ball at ctx.prec otherwise)
    fr = Fraction(fr)
    with ctx.workprec(max(ctx.prec, abs(fr.numerator).bit_length() + 64)):
        return arb(fr.numerator) / fr.denominator


def floor_dy(x, bits):  # largest k/2^bits <= lower(x), Fraction
    return Fraction(int((x.lower() * arb(2) ** bits).floor().unique_fmpz()), 2 ** bits)


def ceil_dy(x, bits):  # smallest k/2^bits >= upper(x)
    return Fraction(int((x.upper() * arb(2) ** bits).ceil().unique_fmpz()), 2 ** bits)


def mid_floor(x, P):  # floor(mid(x) 2^P) as int
    m, e = x.mid().man_exp(); m, e = int(m), int(e) + P
    return m << e if e >= 0 else m >> (-e)


def dy64(x, up=False):  # 64-bit-mantissa dyadic below lower(x) (or above upper(x)), as Fraction
    y = x.upper() if up else x.lower()
    if y == 0: return Fraction(0)
    e = int(math.floor(float(abs(y).log() / arb(2).log()))) - 63
    return ceil_dy(y, -e) if up else floor_dy(y, -e)


def up(x): return x.upper()


def amax(xs):  # max of upper ends (exact)
    m = None
    for x in xs:
        u = x.upper()
        if m is None or u > m: m = u
    return m


def sha(path):
    h = hashlib.sha256(); h.update(open(path, "rb").read()); return h.hexdigest()


def archive():
    """AUDIT F4: copy every file of code/ and every imported module under highprec/ to ARCH/<sha256>.<name> (read-only,
    content-addressed, never overwritten) before the run starts. Returns {path relative to highprec/: sha256}."""
    files = {os.path.join(HERE, f) for f in os.listdir(HERE) if os.path.isfile(os.path.join(HERE, f))}
    files |= {os.path.realpath(m.__file__) for m in list(sys.modules.values()) if getattr(m, "__file__", None)}
    files = sorted(f for f in files if f.startswith((HERE + os.sep, os.path.realpath(HP) + os.sep)))
    os.makedirs(ARCH, exist_ok=True); out = {}
    for f in files:
        h = sha(f); dst = os.path.join(ARCH, f"{h}.{os.path.basename(f)}")
        if not os.path.exists(dst): shutil.copyfile(f, dst); os.chmod(dst, 0o444)
        assert sha(dst) == h, dst
        out[os.path.relpath(f, os.path.realpath(HP))] = h
    return out


# ---------------------------------------------------------------- convolutions (T4, 7.1)
class Kern:
    """Cached kernel polynomials 1/(base + k)^pw, k = 0..n-1, at the current precision."""
    def __init__(self): self.c = {}

    def get(self, base, n, pw):
        key = (base, n, pw, ctx.prec)
        if key not in self.c:
            assert not (base <= 0 < base + n), "kernel hits zero"
            self.c[key] = arb_poly([arb(1) / (base + k) ** pw for k in range(n)])
        return self.c[key]


KERN = Kern()


def toep(c, a0, i0, nout, pw):
    """out[t] = Σ_s c[s] / ((i0 + t) − (a0 + s))^pw, t < nout (arb_poly product)."""
    nc = len(c); Fp = KERN.get(i0 - a0 - nc + 1, nout + nc - 1, pw)
    pr = (arb_poly(c) * Fp).coeffs()
    return pr[nc - 1: nc - 1 + nout]


def hank(c, a0, i0, nout, pw, w2):
    """out[t] = Σ_s c[s] / ((i0 + t) + (a0 + s) + w2)^pw."""
    nc = len(c); Fp = KERN.get(i0 + a0 + w2, nout + nc - 1, pw)
    pr = (arb_poly(c[::-1]) * Fp).coeffs()
    return pr[nc - 1: nc - 1 + nout]


def pf_sums(c, a0, i0, nout, w2, kfun):
    """For out index i = i0 + t: Σ_s c_s/(λ_i − λ_{a0+s}) and Σ_s c_s/(λ_i − λ_{a0+s})² by the partial fractions of P13
    (k_i = kfun(i)). Returns (R, R2) lists."""
    T1, H1 = toep(c, a0, i0, nout, 1), hank(c, a0, i0, nout, 1, w2)
    T2, H2 = toep(c, a0, i0, nout, 2), hank(c, a0, i0, nout, 2, w2)
    R, R2 = [], []
    for t in range(nout):
        k = kfun(i0 + t); s1 = T1[t] + H1[t]
        R.append(s1 / (2 * k)); R2.append((T2[t] + H2[t] + s1 / k) / (4 * k * k))
    return R, R2


# ---------------------------------------------------------------- core proposals (no rigour)
def tri_solve(Lm, b):
    """Proposal: solve L Lᵀ x = b with the exact dyadic factor (mids only)."""
    n = len(b); y = [None] * n
    for i in range(n):
        Li = Lm[i]; s = b[i]
        for j in range(i): s -= Li[j] * y[j]
        y[i] = (s / Li[i]).mid()
    x = [None] * n
    for i in reversed(range(n)):
        s = y[i]
        for j in range(i + 1, n): s -= Lm[j][i] * x[j]
        x[i] = (s / Lm[i][i]).mid()
    return [arb(v) for v in x]


def matvec(M, x):
    K = len(x); X = arb_mat([[v] for v in x]); Y = M * X
    return [Y[i, 0] for i in range(K)]


def dot(a, b): return sum((x * y for x, y in zip(a, b)), arb(0))


def sq_up(x): return abs(x).upper() ** 2  # upper bound of x² (a ball's own square can dip below 0)


def norm_up(v): return sum((sq_up(x) for x in v), arb(0)).sqrt().upper()


def normalize(x):
    n = dot(x, x).sqrt()
    return [(v / n).mid() for v in x]


def inv_iter(M, Lm, its, ortho=None, seed=1):
    rnd = random.Random(seed); K = M.nrows()
    x = [arb(rnd.random() - 0.5) for _ in range(K)]
    for _ in range(its):
        if ortho is not None:
            c = dot(x, ortho); x = [(a - c * o).mid() for a, o in zip(x, ortho)]
        x = normalize([arb(v) for v in x]); x = [arb(v) for v in x]
        x = tri_solve(Lm, x)
    if ortho is not None:
        c = dot(x, ortho); x = [(a - c * o).mid() for a, o in zip(x, ortho)]
    x = [arb(v) for v in normalize([arb(v) for v in x])]
    lam = dot(x, matvec(M, x))
    return lam.mid(), x


# ---------------------------------------------------------------- the certifier
def run(a):
    mut = a.mut
    entries.SHARED_MUT = mut if mut in ("pp_drop", "lam_n") else None  # F1 demo: a bug inside entries.py reaches every Form
    rec = dict(Ldec=a.L, eps=a.eps, sector="ev" if a.eps == 1 else "od", K=a.K, deflate=a.deflate, mut=mut, tmin=a.tmin)
    gates = rec["gates"] = {}
    K = a.K; eps = a.eps; w2 = 0 if eps == 1 else 1
    b = math.ceil(-math.log2(float(a.Uev)))
    pc = a.prec_core or 64 * math.ceil((3 * b + 512) / 64)
    pT = a.prec_T or 64 * math.ceil((1.5 * b + 128) / 64)
    ps = a.prec_src; Pc = a.P_core; P = a.P
    rec.update(prec_core=pc, prec_T=pT, prec_src=ps, P_core=Pc, P=P, b=b)
    log(stage="start", **{k: rec[k] for k in ("Ldec", "eps", "K", "prec_core", "prec_T", "deflate", "mut")})

    # ---- s(L) and gate G-S (R9)
    sj = json.load(open(a.s_file)); s_fr = Fraction(sj["s"])
    rec.update(s=sj["s"], s_float=float(s_fr), s_sha256=sha(a.s_file))
    rz = json.load(open(a.ritz)); guard = max(rz["ritz_ev"], rz["ritz_od"], sj["mu_top_float"])
    if mut == "s_half": s_fr = s_fr / 2
    gates["G-S"] = bool(float(s_fr) > guard and sj["Ldec"] == a.L and rz["Ldec"] == a.L)
    rec["G-S_guard"] = guard

    # ---- mini-G0 on this run's own entries (catches entry mutations in the run itself)
    with ctx.workprec(160):
        Fm, Fp = Form(a.L, eps, 160, mut=mut), Form(a.L, eps, 160)
        ok0 = True
        for q, r in ((0, 0), (1, 1), (2, 2), (0, 1)):
            Pq = eqp.Q_eqP(Fp, eqp.modes(Fp, q), 160) if q == r else \
                (eqp.Q_eqP(Fp, eqp.modes(Fp, q) + eqp.modes(Fp, r), 160) - eqp.Q_eqP(Fp, eqp.modes(Fp, q), 160) - eqp.Q_eqP(Fp, eqp.modes(Fp, r), 160)) / 2
            ok0 &= bool(Pq.overlaps(eqp.closed(Fm, q, r)))
        gates["G0-mini"] = ok0
        # G0i (AUDIT F1): eq. (P) from an independent implementation (own prime list, weights, γ, k) vs this run's closed forms
        rec["G0i"] = indep.g0i(a.L, eps, lambda q, r: eqp.closed(Fm, q, r))
        gates["G0i"] = rec["G0i"]["ok"]
    log(stage="G-S/G0-mini/G0i", gs=gates["G-S"], g0=gates["G0-mini"], g0i=gates["G0i"])

    # ---- Stage C: core
    Fc = Form(a.L, eps, pc, mut=mut)
    ctx.prec = pc
    rows = Fc.rows(0, K)
    uc, Ac = rows["u"], rows["A"]; vc = [Fc.gam(q) for q in range(K)]
    lamc = [Fc.k(q) ** 2 for q in range(K)]
    M0 = arb_mat([[Ac[q] if q == r else (uc[q] * vc[r] - vc[q] * uc[r]) / (lamc[q] - lamc[r]) for r in range(K)] for q in range(K)])
    log(stage="M0")
    theta, phi = Fraction(0), None
    if a.deflate:
        L0, f0 = cholesky_blocked(M0)
        if f0 is not None:
            rec.update(result="FAIL", reason=f"mid(M0) Cholesky proposal failed at {f0}", failed_gates=["proposal"]); return rec
        l1, phi_b = inv_iter(M0, L0, 6, seed=2)
        phi = [floor_dy(arb(v), 128) for v in phi_b]  # 128-bit dyadics (dyadic floor of the mid)
        phia = [fa(v) for v in phi]
        l2, _ = inv_iter(M0, L0, 12, ortho=[arb(v) for v in phi_b], seed=3)  # A3: unrounded φ (the 128-bit φ leaks ~1e-132 at L = 2)
        lam2hat = arb(l2)
        t = round(math.log(2 * float(lam2hat), 4)); theta = Fraction(4) ** t
        rec.update(lam1hat_M0=arb(l1).str(10, radius=False), lam2hat_M0=lam2hat.str(10, radius=False), theta_log4=t)
        log(stage="deflation proposal", lam1=rec["lam1hat_M0"], lam2=rec["lam2hat_M0"], t=t)
    # μ (64-bit dyadic, rounded down; negative controls rounded up)
    ref = arb(a.mu_ref) if a.mu_ref != "lam2hat" else lam2hat
    mu = Fraction(0) if a.mu_rel == "0" else dy64(ref * fa(Fraction(a.mu_rel)), up=a.mu_up)
    mua = fa(mu)
    rec.update(mu=f"{mu.numerator}/{mu.denominator}", mu_float=float(mu), theta=str(theta), mu_rel=a.mu_rel, mu_ref=a.mu_ref)
    log(stage="mu", mu=float(mu))
    def core_matrix(shift):
        M = arb_mat(M0)
        for q in range(K): M[q, q] = M[q, q] - shift
        if a.deflate:
            th = fa(theta)
            for q in range(K):
                for r in range(K): M[q, r] = M[q, r] + th * phia[q] * phia[r]
        return M
    def certify_core(Mx):
        """C2 (Lemma IC): proposal Cholesky of mid(Mx) (also used for solves), λ̂_min by inverse iteration, μ' = λ̂_min/2,
        Cholesky of Mx − μ'I, exact integer residual -> m_core <= λ_min(every matrix in the ball Mx)."""
        Lm0, f0 = cholesky_blocked(Mx)
        if f0 is not None: return None
        lmin, _ = inv_iter(Mx, Lm0, 4, seed=4)
        mup = dy64(arb(lmin) / 2); Ms = arb_mat(Mx)
        for q in range(K): Ms[q, q] = Ms[q, q] - fa(mup)
        Lm1, f1 = cholesky_blocked(Ms)
        if f1 is not None: return None
        res, mupp = exact_residual(Mx, Lm1, fa(mup), Pc)
        rr = max(sum((Mx[i, j].rad() for j in range(K)), arb(0)).upper() for i in range(K))
        return Lm0, (mupp - res - rr).lower(), lmin
    M = core_matrix(arb(0) if mut == "M0" else mua)
    cc = certify_core(M)
    if cc is None:
        rec.update(result="FAIL", reason="core Cholesky proposal failed", failed_gates=["V2"]); return rec
    Lm0, mcore, lmin = cc
    rec.update(lam_min_core_float=arb(lmin).str(8, radius=False), m_core=mcore.str(8, radius=False))
    gates["V2"] = bool(mcore > 0)
    log(stage="core", lmin=rec["lam_min_core_float"], m_core=rec["m_core"], V2=gates["V2"])
    if not gates["V2"]:
        rec.update(result="FAIL", reason="V2", failed_gates=["V2"]); return rec
    # C3 certified solves
    rhs = {"a": uc, "b": vc}
    if a.deflate: rhs.update(e=phia, eh=[l * p for l, p in zip(lamc, phia)])
    sol = {}
    for k_, f in rhs.items():
        x0 = tri_solve(Lm0, f)
        r_ = [x - y for x, y in zip(matvec(M, x0), f)]
        err = (norm_up(r_) / mcore).upper()
        sol[k_] = [x + arb(0, err) for x in x0]
        rec[f"solve_err_{k_}"] = err.str(3, radius=False)
    log(stage="solves", **{k_: rec[f"solve_err_{k_}"] for k_ in rhs})

    # ---- Stage T: coefficient vectors, moments
    ctx.prec = pT
    ys = ["a", "b"] + (["eh", "e"] if a.deflate else [])
    xy = [(x, y) for y in ys for x in ("u", "v")]
    X = {"u": uc, "v": vc}
    cvec = {(x, y): [p * q for p, q in zip(X[x], sol[y])] for x, y in xy}
    lstar = Fc.k(K - 1) ** 2
    theta_i = [l / lstar for l in lamc]
    Af = {k_: sum((abs(c) for c in cv), arb(0)).upper() for k_, cv in cvec.items()}
    Rmax = a.Rmax
    def Rq_rule(q):  # G5′ moment-path degree (R8): tail A_f t0^R below 2^-(prec_src+32), t0 = ℓ*/k_q²
        with ctx.workprec(64):
            tt_ = lstar / Fc.k(q) ** 2
            return int(math.ceil((max(float(v.log() / arb(2).log()) for v in Af.values()) + ps + 32) / -math.log2(float(tt_.upper())))) + 1
    nmom = max(Rmax, Rq_rule(2 * K))  # AUDIT F2: G5′ needs Rq(2K) moments (≈ 570 on deflated L = 2 runs); F0/F1 still stop at Rmax
    mom = {k_: [] for k_ in xy}
    pw_ = [arb(1)] * K
    for r in range(nmom):
        for k_ in xy: mom[k_].append(dot(cvec[k_], pw_))
        pw_ = [p * t for p, t in zip(pw_, theta_i)]
    rec["A_f_log2max"] = max(float(v.log() / arb(2).log()) for v in Af.values())
    log(stage="moments", Rmax=Rmax, A_f_log2=rec["A_f_log2max"])

    # rows of 𝒯 (unbalanced): entries (δ, [(x, y, sign)]) for a = 1 (coefficient of u_q), a = 2 (of v_q)
    TR = [((1, ("v", "a", -1)), (0, ("u", "a", 1))), ((0, ("v", "b", -1)), (1, ("u", "b", 1)))]
    if a.deflate: TR += [((0, ("v", "eh", 1)), (0, ("u", "eh", -1))), ((0, ("v", "e", 1)), (0, ("u", "e", -1)))]
    m = len(TR)
    jsign = [1] * (m // 2)
    if mut == "defl_sign" and m == 4: jsign[1] = -1

    def gen(Rv, R2v, uq, vq):
        """𝒢 and 𝒢' (with the row scales sc) from R, R' values at one q."""
        G, Gp = [], []
        for rho, ((d1, (x1, y1, s1)), (d2, (x2, y2, s2))) in enumerate(TR):
            G.append(sc[rho] * ((d1 + s1 * Rv[(x1, y1)]) * uq + (d2 + s2 * Rv[(x2, y2)]) * vq))
            Gp.append(sc[rho] * (s1 * R2v[(x1, y1)] * uq + s2 * R2v[(x2, y2)] * vq))
        return G, Gp

    def Qform(G, Gp):  # 𝒢ᵀ J_b 𝒢' with J_b = diag(J, J)
        return sum((jsign[p] * (G[2 * p] * Gp[2 * p + 1] - G[2 * p + 1] * Gp[2 * p]) for p in range(m // 2)), arb(0))

    # direct sums on [K, 2K): G5' second path there, and balancing
    ctx.prec = ps
    Fs = Form(a.L, eps, ps, mut=mut)
    def direct_R(q0, q1):
        with ctx.workprec(pT):
            D1 = arb_mat([[arb(1) / (Fc.k(q) ** 2 - lamc[i]) for i in range(K)] for q in range(q0, q1)])
            D2 = arb_mat([[D1[t, i] * D1[t, i] for i in range(K)] for t in range(q1 - q0)])
            Cm = arb_mat([[cvec[k_][i] for k_ in xy] for i in range(K)])
            P1, P2 = D1 * Cm, D2 * Cm
        with ctx.workprec(ps):
            return [{k_: +P1[t, j] for j, k_ in enumerate(xy)} for t in range(q1 - q0)], \
                   [{k_: -P2[t, j] for j, k_ in enumerate(xy)} for t in range(q1 - q0)]
    dR, dR2 = direct_R(K, 2 * K)
    rowsK = Fs.rows(K, 2 * K, diag=False)
    sc = [arb(1)] * m
    G0l = [gen(dR[t], dR2[t], rowsK["u"][t], Fs.gam(K + t))[0] for t in range(K)]
    mx = [max(float(abs(g[r]).upper()) for g in G0l) for r in range(m)]
    tau = round(0.5 * math.log2(mx[1] / mx[0])); scal = [Fraction(2) ** tau, Fraction(2) ** -tau]
    if m == 4:
        tp = round(0.5 * math.log2(mx[3] / mx[2]))  # on top of 2^t, ϑ = 4^t
        tt = rec["theta_log4"]; scal += [Fraction(2) ** (tt + tp), Fraction(2) ** (tt - tp)]
    sc = [fa(x) for x in scal]
    rec["balance"] = [str(x) for x in scal]
    log(stage="balance", scal=rec["balance"])

    # ---- Stage F constants
    L_ = Fs.L; pi = Fs.pi
    al = abs(Fs.alpha)
    def kap(q): return pi * Fs.k(q) / L_
    rbar = (2 * L_ / pi ** 2 * (1 + (-L_).exp() / (1 - (-4 * L_).exp()) + al / (arb(1) / 4 + kap(K) ** 2))).upper()
    V = sum((w * w for w in Fs.w), arb(0)) / 2; Vh = (arb(1) / 4 + 4 / pi ** 2 * V).upper()
    def isn(x):
        s_ = abs(x.sin()); assert s_.lower() > 0, "zero denominator in E_h"; return (1 / s_).upper()
    th_ = Fs.theta
    E1 = sum((w * isn(t / 2) for w, t in zip(Fs.w, th_)), arb(0))
    E = sum((Fs.w[i] * Fs.w[j] * isn((th_[i] - th_[j]) / 2) / 2 for i in range(len(th_)) for j in range(len(th_)) if i != j), arb(0)) \
        + sum((Fs.w[i] * Fs.w[j] * isn((th_[i] + th_[j]) / 2) / 2 for i in range(len(th_)) for j in range(len(th_))), arb(0))
    Eh = (2 / pi * E1 + 4 / pi ** 2 * E).upper()
    def J2(N): return (Vh / (Fs.k(N) - 1) + Eh / Fs.k(N) ** 2).upper()
    def J4(N): return (1 / (3 * (Fs.k(N) - 1) ** 3)).upper()
    rec.update(rbar=rbar.str(8, radius=False), V_h=Vh.str(10, radius=False), E_h=Eh.str(10, radius=False))

    def F01(k_, z0):
        """P14: F0, F1 for R_{x,y} with z0 (> ℓ*). R by the rule (start 96)."""
        with ctx.workprec(pT):
            t0 = lstar / z0; assert t0 < 1
            A = Af[k_]; ms = [abs(v).upper() for v in mom[k_]]
            R = 96
            while True:
                F0 = sum((ms[r] * t0 ** r for r in range(R)), arb(0)) + A * t0 ** R / (1 - t0)
                if (A * t0 ** R).upper() <= (arb(2) ** -64 * F0).upper() or R >= Rmax: break
                R += 8
            F1 = sum(((r + 1) * ms[r] * t0 ** r for r in range(R)), arb(0)) + A * t0 ** R * (R + 1 - R * t0) / (1 - t0) ** 2
            return F0.upper(), F1.upper(), R

    def Lab(z0):
        F = {k_: F01(k_, z0) for k_ in xy}
        Lm_ = [[arb(0), arb(0)], [arb(0), arb(0)]]
        dl = lambda rho, aa: abs(sc[rho]) * TR[rho][aa][0]
        f0 = lambda rho, aa: abs(sc[rho]) * F[TR[rho][aa][1][:2]][0]
        f1 = lambda rho, aa: abs(sc[rho]) * F[TR[rho][aa][1][:2]][1]
        for aa in range(2):
            for bb in range(2):
                for p in range(m // 2):
                    for rho, sig in ((2 * p, 2 * p + 1), (2 * p + 1, 2 * p)):
                        Lm_[aa][bb] += (dl(rho, aa) + f0(rho, aa) / z0) * f1(sig, bb)
        return [[x.upper() for x in r] for r in Lm_], max(v[2] for v in F.values()), F

    def taus(N):
        z0 = Fs.k(N) ** 2
        (L11, L12), (L21, L22) = Lab(z0)[0]
        j2, j4 = J2(N), J4(N)
        tc = (L11 * j2 + (2 * rbar * L11 + L12 + L21) * (j2 * j4).sqrt() + (rbar ** 2 * L11 + rbar * (L12 + L21) + L22) * j4).upper()
        tp = ((2 * L_ ** 3 / pi ** 4) * (L_ / 2).cosh() ** 2 * j4).upper() if eps == -1 else arb(0)
        if mut == "tau0": tc, tp = arb(0), arb(0)
        if mut == "aud_tau_half": tc = (tc / 2).upper()  # G6 auditor mutation
        return tc, tp
    sa = fa(s_fr)

    def tq(q, tN):  # t_q = H(κ_q) − μ − s − τ_N
        return Fs.Hk(q) - mua - sa - tN

    # N rule (R4)
    N = 4 * K
    while True:
        tc, tp = taus(N); tN = tc + tp
        if tq(N, tN).lower() >= a.tmin: break
        N += a.nstep
        if N > a.Nmax:
            rec.update(result="FAIL", reason=f"no N <= {a.Nmax} with lb(t_N) >= {a.tmin}", failed_gates=["V3"]); return rec
    rec.update(N=N, tau_core=tc.str(6, radius=False), tau_pole=tp.str(6, radius=False), tau_N=tN.str(6, radius=False))
    n = N - K
    log(stage="N", N=N, tau_N=rec["tau_N"], t_N=tq(N, tN).str(6, radius=False))

    Mfac = 4
    while True:
        Mq = Mfac * N; Q2 = 2 * Mq
        # ---- entries on [K, 2M)
        ctx.prec = ps
        rowsA = Fs.rows(K, Mq, diag=True); rowsB = Fs.rows(Mq, Q2, diag=False)
        uq = rowsA["u"] + rowsB["u"]; Hq = rowsA["H"] + rowsB["H"]; Sq = rowsA["S"] + rowsB["S"]
        log(stage="entries", M=Mq)
        # ---- convolution transfer on [K, 2M)
        Rv = {}; R2v = {}
        for k_ in xy:
            with ctx.workprec(pT):
                R1, R2 = pf_sums(cvec[k_], 0, K, Q2 - K, w2, Fc.k)
            with ctx.workprec(ps):
                Rv[k_] = [+v for v in R1]; R2v[k_] = [-v for v in R2]
            del R1, R2
        KERN.c.clear()
        log(stage="transfer conv", Q2=Q2)
        ctx.prec = ps
        G = []; Qd = []
        for t in range(Q2 - K):
            g_, gp = gen({k_: Rv[k_][t] for k_ in xy}, {k_: R2v[k_][t] for k_ in xy}, uq[t], Fs.gam(K + t))
            G.append(g_); Qd.append(Qform(g_, gp))
        del Rv, R2v
        if mut in ("gen", "gen2K", "gen2Kmax"):  # gen2K*, F2 demo: a generator at q = 2K + 7, where the pilot's capped G5′ was
            # vacuous on deflated runs for the rows whose solves have the largest A_f (gen2Kmax perturbs that row, gen2K row U)
            qm = random.Random(20261031).randrange(K, Mq) if mut == "gen" else 2 * K + 7
            rho = max(range(m), key=lambda r: max(float(Af[TR[r][0][1][:2]]), float(Af[TR[r][1][1][:2]]))) if mut == "gen2Kmax" else 0
            G[qm - K][rho] = G[qm - K][rho] * (1 + arb(2) ** -20)
            rec["mut_index"] = qm; rec["mut_row"] = rho
        if mut == "Qq0": Qd = [arb(0)] * len(Qd)
        Sqq = [rowsA["A"][t] - mua - Qd[t] for t in range(Mq - K)]
        log(stage="generators", Gmax=[amax(abs(g_[r]) for g_ in G).str(3, radius=False) for r in range(m)],
            Grad=[amax(g_[r].rad() for g_ in G).str(3, radius=False) for r in range(m)],
            Gradarg=[max(range(len(G)), key=lambda t: float(G[t][r].rad())) + K for r in range(m)],
            uradarg=max(range(len(uq)), key=lambda t: float(uq[t].rad())) + K, urad=amax(x.rad() for x in uq).str(3, radius=False), Qmax=amax(abs(x) for x in Qd).str(3, radius=False))
        # ---- t'_q (R3a)
        tNq = tq(N, tN); tpN = floor_dy(tNq, 40)
        tp_ = [max(tpN, floor_dy(Hq[q - K] - mua - sa - tN, 40)) for q in range(N, Mq)]
        tpM = max(tpN, floor_dy(Fs.Hk(Mq) - mua - sa - tN, 40))
        gates["V3"] = bool(tpN > 0)
        # ---- r_M (P22)
        Sa = [sum((sq_up(G[i - K][r]) for i in range(K, N)), arb(0)).upper() for r in range(m)]
        Labm, _, FM = Lab(Fs.k(Mq) ** 2)
        kM2 = Fs.k(Mq) ** 2
        Ar = [abs(sc[rho]) * TR[rho][0][0] + abs(sc[rho]) * FM[TR[rho][0][1][:2]][0] / kM2 for rho in range(m)]
        Cr = [abs(sc[rho]) * TR[rho][1][0] + abs(sc[rho]) * FM[TR[rho][1][1][:2]][0] / kM2 for rho in range(m)]
        beta = [(Ar[r] * J2(Mq).sqrt() + (Ar[r] * rbar + Cr[r]) * J4(Mq).sqrt()).upper() for r in range(m)]
        varrho = Fs.k(N - 1) / Fs.k(Mq)
        num = sum((Sa[2 * p].sqrt() * beta[2 * p + 1] + Sa[2 * p + 1].sqrt() * beta[2 * p] for p in range(m // 2)), arb(0))
        rM = (num ** 2 / (fa(tpM) * (1 - varrho ** 2) ** 2)).upper()
        if mut == "rM0": rM = arb(0)
        if mut == "aud_rM_half": rM = (rM / 2).upper()  # G6 auditor mutation
        log(stage="r_M", M=Mq, r_M=rM.str(5, radius=False))
        if rM > arb(1) / 4 and Mfac == 4: Mfac = 8; continue
        break
    rec.update(M=Mq, t_N=tNq.str(8, radius=False), tprime_N=str(tpN), tprime_M=str(tpM), r_M=rM.str(6, radius=False))

    # ---- controls C-τ, C-r̄, C-J_2
    sQ = sum((Qd[q - K] for q in range(N, Mq)), arb(0))
    ok_tau = bool(sQ.upper() <= tc.upper())
    if eps == -1:
        cosh2 = (L_ / 2).cosh() ** 2
        sP = sum((2 / L_ * cosh2 / (arb(1) / 4 + kap(q) ** 2) ** 2 for q in range(N, Mq)), arb(0))
        ok_tau &= bool(sP.upper() <= tp.upper()); rec["C-tau_pole_sum"] = sP.str(4, radius=False)
    gates["C-tau"] = ok_tau; rec["C-tau_sumQ"] = sQ.str(4, radius=False)
    hq = [arb(1) / 2 + 2 / pi * Sq[q - K] for q in range(K, Q2)]
    rq = amax(abs(uq[q - K] - Fs.k(q) * hq[q - K]) for q in range(K, Mq))
    gates["C-rbar"] = bool(rq <= rbar); rec["C-rbar_max"] = rq.str(4, radius=False)
    sJ2 = sum((sq_up(hq[q - K]) / Fs.k(q) ** 2 for q in range(N, min(4 * N, Q2))), arb(0))
    gates["C-J2"] = bool(sJ2.upper() <= J2(N)); rec["C-J2_sum"] = sJ2.str(5, radius=False); rec["J2"] = J2(N).str(5, radius=False)
    log(stage="controls", Ctau=gates["C-tau"], Crbar=gates["C-rbar"], CJ2=gates["C-J2"])
    # C-ind (AUDIT F7): τ_core, τ_pole, t_N, r_M recomputed by independent mpmath code (indep.far); the factor-level check the
    # C-controls cannot give (they have 1.3–3× slack). Inputs: the G5-checked solves and the G5′-checked generators.
    ci = indep.far(a.L, eps, K, N, Mq, a.deflate, sol, scal, mu, s_fr, G,
                   dict(tc=tc, tp=tp, rM=rM, tpN=tpN, tpM=tpM), dps=int(rec["A_f_log2max"] * 0.30103) + 40)
    rec["C-ind"] = ci; gates["C-ind"] = ci["ok"]
    log(stage="C-ind", ok=ci["ok"], **{k_: ci[k_]["rel_excess"] for k_ in ("tau_core", "tau_pole", "r_M")})

    # ---- G5' second path on [K, M): direct sums q < 2K, moment series q >= 2K (R8)
    ok5p = True; worst = 0
    def cmp(t, Rd, R2d):
        nonlocal ok5p
        g_, gp = gen(Rd, R2d, uq[t], Fs.gam(K + t))
        S2 = rowsA["A"][t] - mua - Qform(g_, gp)
        good = all(bool(x.overlaps(y)) for x, y in zip(g_, G[t])) and bool(S2.overlaps(Sqq[t]))
        ok5p &= good
    for t in range(K): cmp(t, dR[t], dR2[t])
    with ctx.workprec(pT):
        pe = int(max(max(float(abs(v).upper().log() / arb(2).log()) if v != 0 else 0 for v in mom[k_]) for k_ in xy)) + ps + 64
    groups = {}
    for q in range(2 * K, Mq):
        groups.setdefault(Rq_rule(q), []).append(q)  # F2: no Rmax cap (the pilot capped at 400, vacuous near 2K when deflated)
    assert max(groups) <= nmom
    tail_max = None
    with ctx.workprec(pe):
        for Rq, qs in groups.items():
            polys = {k_: (arb_poly([+v for v in mom[k_][:Rq]]), arb_poly([-(r + 1) * mom[k_][r] for r in range(Rq)])) for k_ in xy}
            for q in qs:
                z = Fc.k(q) ** 2; t0 = lstar / z
                Rd, R2d = {}, {}
                for k_ in xy:
                    A = Af[k_]; tail = (A * t0 ** Rq / (1 - t0)).upper(); tail2 = (A * t0 ** Rq * (Rq + 1 - Rq * t0) / (1 - t0) ** 2).upper()
                    if tail_max is None or tail > tail_max: tail_max = tail
                    Rd[k_] = (polys[k_][0](t0) + arb(0, tail)) / z
                    R2d[k_] = (polys[k_][1](t0) + arb(0, tail2)) / (z * z)
                with ctx.workprec(ps): cmp(q - K, {k: +v for k, v in Rd.items()}, {k: +v for k, v in R2d.items()})
    gates["G5p"] = ok5p
    rec["G5p_Rq_max"] = max(groups); rec["G5p_tail_log2_max"] = float(tail_max.log() / arb(2).log()) if tail_max and tail_max > 0 else None
    log(stage="G5'", ok=ok5p, Rq=[min(groups), max(groups)], tail_log2_max=rec["G5p_tail_log2_max"])

    # ---- Stage I: Z, Z2 on I_P, from q in [N, M) (7.1)
    ctx.prec = ps
    pairs = [(bb, dd) for bb in range(m) for dd in range(bb, m)]
    Z = {}; Z2 = {}
    tpa = [fa(x) for x in tp_]
    for bb, dd in pairs:
        wv = [G[q - K][bb] * G[q - K][dd] / tpa[q - N] for q in range(N, Mq)]
        Z[(bb, dd)], Z2[(bb, dd)] = pf_sums(wv, N, K, n, w2, Fs.k)
    KERN.c.clear()
    Jb = [[0] * m for _ in range(m)]
    for p in range(m // 2): Jb[2 * p][2 * p + 1], Jb[2 * p + 1][2 * p] = jsign[p], -jsign[p]
    def Jv(x): return [sum((Jb[r][c] * x[c] for c in range(m) if Jb[r][c]), arb(0)) for r in range(m)]
    def JTv(x): return [sum((Jb[c][r] * x[c] for c in range(m) if Jb[c][r]), arb(0)) for r in range(m)]
    hrows, dS = [], []
    for t in range(n):
        Zm = [[Z[(min(r, c), max(r, c))][t] for c in range(m)] for r in range(m)]
        Z2m = [[Z2[(min(r, c), max(r, c))][t] for c in range(m)] for r in range(m)]
        gi = G[t]; y = JTv(gi)
        wi = Jv([dot(Zm[r], y) for r in range(m)])
        hrows.append(gi + wi)
        dS.append(Sqq[t] - dot(y, [dot(Z2m[r], y) for r in range(m)]))
    del Z, Z2
    log(stage="stage I", n=n)
    # C-r_M (finite part over [M, 2M))
    tr = arb(0); ytail = [JTv(G[Mq - K + t]) for t in range(Mq)]
    for bb, dd in pairs:
        cv = [G[i - K][bb] * G[i - K][dd] for i in range(K, N)]
        _, W2 = pf_sums(cv, K, Mq, Mq, w2, Fs.k)
        for t in range(Mq):
            y = ytail[t]
            tr += (1 if bb == dd else 2) * y[bb] * y[dd] * W2[t]
    KERN.c.clear()
    fin = (tr / fa(tpM)).upper()
    gates["C-rM"] = bool(fin <= rM); rec["C-rM_finite"] = fin.str(4, radius=False)
    log(stage="C-rM", fin=rec["C-rM_finite"], ok=gates["C-rM"])

    # ---- assembly (7.2)
    D = 2 * m
    Jm = [[0] * D for _ in range(D)]
    for r in range(m):
        for c in range(m): Jm[r][c] = Jb[r][c]
        Jm[r][m + r] = -1; Jm[m + r][r] = 1
    Hint = [[mid_floor(x, P) for x in h] for h in hrows]
    Dhat = [mid_floor(x, P) for x in dS]
    two = arb(2) ** -P
    eh = (amax(x.rad() for h in hrows for x in h) + two).upper()
    ed = (amax(x.rad() for x in dS) + two).upper()
    habs = [fa(Fraction(max(abs(h[c]) for h in Hint), 2 ** P)) for c in range(D)]
    Hc = ((1 + arb(n).log()) / K).upper()
    HS = Fraction(int((Hc * arb(2) ** 64).ceil().unique_fmpz()), 2 ** 64)
    easm = (ed + Hc * sum((abs(Jm[r][c]) * (eh * (habs[r] + habs[c]) + eh * eh) for r in range(D) for c in range(D)), arb(0))).upper()
    delta0 = ceil_dy(rM + easm + arb(2) ** -10, 8)
    rec.update(eps_asm=easm.str(4, radius=False), H=Hc.str(6, radius=False), delta0=str(delta0), e_h=eh.str(3, radius=False))
    log(stage="assembly", eps_asm=rec["eps_asm"], delta0=str(delta0))

    # Lemma SR labels (AUDIT F3): passed to the kernel explicitly as the exact integers 4λ_q, q ∈ I_P; G5 below rebuilds S_input
    # entries from exactly these labels, so a label convention error (e.g. a shift by one) fails G5.
    lab = [Fs.lam4(q + (1 if mut == "aud_sr_q0" else 0)) for q in range(K, N)]
    assert all(b_ - a_ >= 8 * K for a_, b_ in zip(lab, lab[1:])), "H_S needs |λ_i − λ_j| ≥ 2K|i − j|"
    rec["SR_labels"] = dict(first=lab[0], last=lab[-1], n=len(lab))
    # ---- G5: direct checks (independent core assembly and Arb solves at prec_core)
    rnd = random.Random(20261031 + int(hashlib.md5(json.dumps([a.L, eps, a.mu_rel, a.deflate]).encode()).hexdigest()[:6], 16))
    idxP = sorted(rnd.sample(range(K, N), 16)); idxF = sorted(rnd.sample(range(N, Mq), 16))
    with ctx.workprec(pc):
        Md = arb_mat([[Ac[q] if q == r else (uc[q] * vc[r] - vc[q] * uc[r]) / (lamc[q] - lamc[r]) for r in range(K)] for q in range(K)])
        for q in range(K): Md[q, q] = Md[q, q] - mua
        if a.deflate:
            th = fa(theta)
            for q in range(K):
                for r in range(K): Md[q, r] = Md[q, r] + th * phia[q] * phia[r]
        idx = idxP + idxF
        ccd = certify_core(Md)  # G5 certifies its own core: no Cholesky, m_core or solve is shared with the pipeline
        assert ccd is not None and ccd[1] > 0, "G5 direct core not positive"
        Lmd, mcd = ccd[0], ccd[1]
        ext = {q: Fc.rows(q, q + 1, diag=(q in idxP)) for q in idx}
        cols = {q: [(uc[i] * Fc.gam(q) - vc[i] * ext[q]["u"][0]) / (lamc[i] - Fc.k(q) ** 2) for i in range(K)] for q in idx}
        xs = {}
        for q in idx:
            x0 = tri_solve(Lmd, cols[q]); r_ = [x - y for x, y in zip(matvec(Md, x0), cols[q])]
            err = (norm_up(r_) / mcd).upper(); xs[q] = [x + arb(0, err) for x in x0]
        Qdir = {q: dot(cols[q], xs[q]) for q in idx}
        solok = True
        for k_, f in rhs.items():
            x0 = tri_solve(Lmd, f); r_ = [x - y for x, y in zip(matvec(Md, x0), f)]
            err = (norm_up(r_) / mcd).upper()
            solok &= all(bool((x + arb(0, err)).overlaps(y)) for x, y in zip(x0, sol[k_]))
    ok5 = all(bool(Qdir[q].overlaps(Qd[q - K])) for q in idx) and solok
    rec["G5_core_solves"] = solok; g5Q = ok5; g5E = True
    rec["G5_Q_maxreldiff"] = max(float(abs(Qdir[q] - Qd[q - K]).upper() / (abs(Qdir[q]).upper() + 1e-300)) for q in idx)
    ents = [(i, i) for i in idxP[:5]] + list(zip(idxP[5:10], idxP[10:15]))
    for i, j in ents:
        with ctx.workprec(pc):
            Aij = ext[i]["A"][0] if i == j else (ext[i]["u"][0] * Fc.gam(j) - Fc.gam(i) * ext[j]["u"][0]) / (Fc.k(i) ** 2 - Fc.k(j) ** 2)
            Sij = Aij - (mua if i == j else 0) - dot(cols[i], xs[j])
        with ctx.workprec(ps):
            Sij = +Sij
            gi, gj = G[i - K], G[j - K]
            far = arb(0)
            for q in range(N, Mq):
                gq = G[q - K]
                si = sum((jsign[p] * (gi[2 * p] * gq[2 * p + 1] - gi[2 * p + 1] * gq[2 * p]) for p in range(m // 2)), arb(0)) / (Fs.k(i) ** 2 - Fs.k(q) ** 2)
                sj = sum((jsign[p] * (gj[2 * p] * gq[2 * p + 1] - gj[2 * p + 1] * gq[2 * p]) for p in range(m // 2)), arb(0)) / (Fs.k(j) ** 2 - Fs.k(q) ** 2)
                far += si * sj / tpa[q - N]
            direct = Sij - far
            if i == j: inp = fa(Fraction(Dhat[i - K], 2 ** P)); tol = ed
            else:
                hi, hj = Hint[i - K], Hint[j - K]
                nu = sum(Jm[r][c] * hi[r] * hj[c] for r in range(D) for c in range(D))
                dl = Fraction(lab[i - K] - lab[j - K], 4)  # F3: the kernel's own label difference, not Fs.k (the direct side uses Fs.k)
                inp = fa(Fraction(nu, 2 ** (2 * P)) / dl)
                tol = sum((abs(Jm[r][c]) * (eh * (habs[r] + habs[c]) + eh * eh) for r in range(D) for c in range(D)), arb(0)) / fa(abs(dl))
            good = bool(abs(direct - inp).lower() <= (direct.rad() + tol).upper())
            ok5 &= good; g5E &= good
    gates["G5"] = ok5; rec["G5_parts"] = dict(Q_and_core_solves=g5Q, S_input_entries=g5E)
    log(stage="G5", ok=ok5, Qrel=rec["G5_Q_maxreldiff"])

    # ---- float proposal, then Lemma SR
    two_P = 1 << P
    d0int = int(delta0 * two_P); assert Fraction(d0int, two_P) == delta0
    Dv = [d - d0int for d in Dhat]
    pmin, pfail = sr.float_ldl([[x / two_P for x in h] for h in Hint], [d / two_P for d in Dv], Jm, lab)
    rec.update(float_pmin=float(pmin), float_fail=pfail)
    log(stage="float LDL", pmin=float(pmin), fail=pfail)
    rec["proj_SR_hours"] = a.cD * n * n / 2 / 3600 if a.cD else None
    if a.save_input:
        with open(a.save_input, "w") as f:
            json.dump(dict(P=P, lab=lab, Jm=Jm, HS=str(HS), H=[[format(x, "x") for x in h] for h in Hint], D=[format(d, "x") for d in Dv]), f)
    if a.sr_if_pmin is not None and not pmin >= a.sr_if_pmin:
        rec["result"] = "PROPOSAL_REJECTED"; return rec
    if a.sr or a.sr_if_pmin is not None:
        srr = sr.kernel(Hint, Dv, Jm, P, lab, workdir=a.workdir)
        eE = sr.eps_E(srr, HS)
        rec.update(SR_fail=srr["fail"], SR_seconds=srr["seconds"], eps_E=float(eE), min_pivot=float(Fraction(srr["minp"], two_P)),
                   SR_checksum=dict(T=format(srr["T"], "x")[:32], sump=format(srr["sump"], "x")[:32], sumL=format(srr["sumL"], "x")[:32]))
        gates["V4"] = srr["fail"] < 0
        gates["R6"] = eE <= Fraction(1, 4096)
        v5 = fa(delta0) - fa(eE) - easm - rM
        gates["V5"] = bool(v5.lower() > 0)
        rec["V5_margin"] = v5.lower().str(6, radius=False)
        log(stage="SR", fail=srr["fail"], sec=srr["seconds"], eps_E=float(eE), V5=gates["V5"])
        hard = ["G-S", "G0-mini", "G0i", "V2", "V3", "V4", "V5", "R6", "G5", "G5p", "C-tau", "C-rbar", "C-J2", "C-rM", "C-ind"]
        passed = all(gates.get(g_) for g_ in hard)
        rec["result"] = "PASS" if passed else "FAIL"
        rec["failed_gates"] = [g_ for g_ in hard if not gates.get(g_)]
        if passed: rec["certified_lower_bound"] = mua.lower().str(20)
    else:
        rec["result"] = "PROPOSAL"
    return rec


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--L", required=True); p.add_argument("--eps", type=int, required=True)
    p.add_argument("--K", type=int, default=512); p.add_argument("--mu-rel", default="0"); p.add_argument("--mu-ref", default="0")
    p.add_argument("--mu-up", action="store_true", help="round μ up (negative controls)")
    p.add_argument("--Uev", required=True, help="U^ev(L) decimal, sets b for the precision rule")
    p.add_argument("--deflate", action="store_true"); p.add_argument("--tmin", type=float, default=1.0)
    p.add_argument("--s-file", required=True); p.add_argument("--ritz", required=True)
    p.add_argument("--prec-core", type=int, default=0); p.add_argument("--prec-T", type=int, default=0)
    p.add_argument("--prec-src", type=int, default=192); p.add_argument("--P-core", type=int, default=1536); p.add_argument("--P", type=int, default=96)
    p.add_argument("--Rmax", type=int, default=400); p.add_argument("--nstep", type=int, default=1024); p.add_argument("--Nmax", type=int, default=262144)
    p.add_argument("--cD", type=float, default=0.0, help="P0 benchmark, seconds per pair (projection only)")
    p.add_argument("--sr", action="store_true"); p.add_argument("--save-input")
    p.add_argument("--sr-if-pmin", type=float, default=None, help="run Lemma SR only if the float proposal's min pivot >= this"); p.add_argument("--workdir")
    p.add_argument("--mut"); p.add_argument("--out", required=True); p.add_argument("--label", default="")
    a = p.parse_args(argv)
    assert not os.path.exists(a.out), a.out
    code = archive()  # F4: every executed file is archived (content-addressed) before the run starts
    amend = os.environ.get("RH60_AMEND")  # F5: state of the append-only amendment log when this run started
    amend = dict(path=amend, sha256=sha(amend), entries=sum(1 for _ in open(amend))) if amend and os.path.exists(amend) else None
    rec = run(a)
    rec.update(label=a.label, seconds=round(time.time() - T0), peak_gb=round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 2),
               argv=sys.argv[1:], utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), log=LOG,
               code_sha256=code, archive_dir=os.path.realpath(ARCH), amendments=amend)
    stamp = os.environ.get("RH60_STAMP")
    if stamp and os.path.exists(stamp): rec["stamp_sha256"] = sha(stamp)
    json.dump(rec, open(a.out, "w"), indent=1, default=str)
    print(json.dumps({k: v for k, v in rec.items() if k not in ("log", "code_sha256")}, default=str))


if __name__ == "__main__":
    main()
