"""Grid G driver helpers (PREREG_GRID.md §2-§4). Runs certify.py only through code/pilot.py, so every run record carries the
stamp, the archive map (F4) and the amendment-log pin (F5) exactly as in the pilot.
  python grid.py ladder odd|l2 L Lprev       one window's ladder with the registered step-aware rungs (§2.4)
  python grid.py nc ev|od L                  G2 negative control at μ = 1.01·U^σ(L) (must FAIL; §3)
  python grid.py t15 REFDIR                  toolchain check: the grid's L = 1.5 first rungs equal the FIXES records (§3)
  python grid.py glue WINDOWS STAMP [ARGS]   PASS records -> $RH60_RUN/glue, then check_steps.py --stamp [ARGS] (§5)
  python grid.py nc l2e L                    PREREG_GAP negative control: rule-E parameters at μ = 1.01·λ̂_2(M_0) (must FAIL)
Rule E (PREREG_GAP §2): an l2 ladder whose 3 rungs all FAIL with failed_gates == [V4] runs one more rung l2_<L>_1o4_e1 at
μ = ¼·λ̂_2(M_0) with --tmin = t_N(l2_<L>_1o4) + 2^-10 (R4 then takes the next N); a PASS renames REFINE_<Lp>_<L> to REFINED_.
  python grid.py xcheck WINDOWS ELSTON_DIR   overlap cross-check against Elston's certified bounds (§6; consistency only)
U values are the minimum lam0_upper over the rows of $RH60_RUN/upper/*.jsonl with that L and parity (every row is a rigorous
upper bound). A hard-gate failure or a crash writes out/STOP_GATE, a G2 PASS writes out/STOP_G2 (pilot.py writes STOP_N2);
run_grid.sh launches nothing new once any STOP_* exists.
Method credit: rh_60 v1 (bramble_trace) / rh_45 v1 (lihongmin), unrefereed AI-agent preprints; this driver is ours."""
import glob, hashlib, json, os, shutil, subprocess, sys
from fractions import Fraction
CODE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "code")
sys.path.insert(0, CODE)
import pilot

O = pilot.O
HARD = {"G-S", "G0-mini", "G0i", "G5", "G5p", "C-tau", "C-rbar", "C-J2", "C-rM", "C-ind", "R6"}  # V2-V5: an ordinary FAIL at that μ
FLOOR = 1 + Fraction(1, 2 ** 20)  # a rung must exceed U^ev(L_prev) by this factor to be of use to the step test


def U(L, par, field="lam0_upper"):
    rows = [r for f in glob.glob(f"{O}/upper/*.jsonl") for r in map(json.loads, open(f)) if r["L"] == L and r.get("par", 0) == par]
    assert rows, f"no U row for L = {L}, par = {par}"
    return min(rows, key=lambda r: Fraction(r["lam0_upper"]))[field]


def stop(kind, **kw):
    with open(f"{O}/out/STOP_{kind}", "a") as f: f.write(json.dumps(kw) + "\n")
    sys.exit(f"STOP_{kind}: {kw}")


_run = pilot.run
def checked(name, args):  # every grid run goes through here: a hard-gate failure or a crash stops the grid (PREREG_GRID K2g)
    r = _run(name, args)
    bad = sorted(g for g, ok in (r.get("gates") or {}).items() if g in HARD and ok is False)
    if bad or r.get("result") == "CRASH": stop("GATE", run=name, result=r.get("result"), gates=bad)
    return r
pilot.run = checked  # the pilot ladders call the module-level run()


def tmin_e1(L):  # rule E: t_N of the failed 1/4 rung + 2^-10
    return repr(float(Fraction(json.load(open(f"{O}/out/l2_{L}_1o4.json"))["t_N"]) + Fraction(1, 1024)))


def ladder(kind, L, Lp):
    Uev, floor = U(L, 0), Fraction(U(Lp, 0)) * FLOOR
    if kind == "odd":
        Uod = U(L, 1)
        rungs = [r for r in ("2/3", "1/2", "1/3") if Fraction(r) * Fraction(Uod) >= floor]
        if not rungs:  # registered refinement (PREREG_GRID §2.5), decided from U values alone, before any certifier run
            open(f"{O}/out/REFINE_{Lp}_{L}", "w").write(json.dumps(dict(Uod=Uod, Uev_prev=U(Lp, 0))))
            sys.exit(3)
        hist = pilot.ladder_odd(L, Uod, Uev, L, rungs)
    else:
        rungs = [("1/4", "lam2hat"), ("1/1024", "lam2hat"), ("2", U(Lp, 0))]
        hist = pilot.ladder_l2(L, Uev, L, rungs)
        recs = [json.load(open(f"{O}/out/l2_{L}_{r.replace('/', 'o')}.json")) for r, _ in rungs] if not any("PASS" in h for h in hist) else []
        if recs and all(r.get("result") == "FAIL" and r.get("failed_gates") == ["V4"] for r in recs):  # rule E (PREREG_GAP §2)
            r = checked(f"l2_{L}_1o4_e1", pilot.common(L, Uev) + ["--eps", "1", "--deflate", "--tmin", tmin_e1(L), "--mu-rel", "1/4",
                                                                  "--mu-ref", "lam2hat", "--sr"])
            hist.append(("1/4", "lam2hat", "e1", r.get("result")))
            if r.get("result") == "PASS":
                pilot.n2(r, Fraction(r["lam2hat_M0"]))
                if os.path.exists(f"{O}/out/REFINE_{Lp}_{L}"): os.rename(f"{O}/out/REFINE_{Lp}_{L}", f"{O}/out/REFINED_{Lp}_{L}")
    print(json.dumps(hist))
    if not any("PASS" in h for h in hist):
        open(f"{O}/out/REFINE_{Lp}_{L}", "a").write(json.dumps(dict(kind=kind, hist=hist)) + "\n")
        sys.exit(4)


def nc(sec, L):
    Uev = U(L, 0); ref = Uev if sec == "ev" else U(L, 1)
    args = ["--eps", "1" if sec == "ev" else "-1", "--mu-rel", "101/100", "--mu-ref", ref, "--mu-up", "--tmin", "1", "--sr"]
    if sec == "l2e":  # PREREG_GAP: above the Galerkin value λ̂_2(M_0) ≥ λ_2^ev(L), so a PASS is impossible for a sound certifier
        args = ["--eps", "1", "--deflate", "--mu-rel", "101/100", "--mu-ref", "lam2hat", "--mu-up", "--tmin", tmin_e1(L), "--sr"]
    r = checked(f"nc_{L}_{sec}", pilot.common(L, Uev) + args)
    if r.get("result") == "PASS": stop("G2", run=f"nc_{L}_{sec}")  # K1g: VOID everything
    print(r.get("result"), r.get("failed_gates"))


def t15(ref):
    keys = ("mu", "N", "M", "tau_N", "r_M", "delta0", "eps_E", "min_pivot", "SR_checksum", "certified_lower_bound", "V5_margin")
    for new, old in (("odd_1.5_2o3", "final_odd_1.5_2o3"), ("l2_1.5_1o4", "final_l2_1.5_1o4")):
        p = f"{O}/out/{new}.json"
        if not os.path.exists(p): stop("TOOLCHAIN", run=new, missing=True)
        a, b = json.load(open(p)), json.load(open(f"{ref}/{old}.json"))
        diff = [k for k in keys if a.get(k) != b.get(k)]
        if diff: stop("TOOLCHAIN", run=new, fields=diff)
    print("T-1.5: identical to the FIXES records")


def glue(wfile, stamp, *extra):
    W, G = open(wfile).read().split(), f"{O}/glue"
    # an unresolved REFINE marker on a step of W: glue only after the refinement (PREREG_GRID §2.5; PREREG_GAP: steps outside W
    # do not block a glue of W)
    pend = [p for p in glob.glob(f"{O}/out/REFINE_*") if set(os.path.basename(p).split("_")[1:]) <= set(W)]
    if pend: print("refinement pending, not glued:", *map(os.path.basename, pend)); sys.exit(3)
    os.makedirs(G, exist_ok=True)
    for L in W[1:]:
        for kind in ("odd", "l2"):
            ok = [f for f in sorted(glob.glob(f"{O}/out/{kind}_{L}_*.json")) if json.load(open(f)).get("result") == "PASS"]
            if ok: shutil.copyfile(ok[0], f"{G}/g_{L}_{kind}.json")
    for f in glob.glob(f"{O}/upper/*.jsonl"): shutil.copyfile(f, f"{G}/{os.path.basename(f)}")
    sha = hashlib.sha256(open(stamp, "rb").read()).hexdigest()
    sys.exit(subprocess.run([sys.executable, "-I", os.path.join(CODE, "..", "..", "..", "gap", "check_steps.py"), G, wfile,
                             "--stamp", sha, *extra]).returncode)


def xcheck(wfile, edir):
    from flint import arb
    out = []
    for L in open(wfile).read().split():
        for kind in ("odd", "l2"):
            e, o = f"{edir}/g_{L}_{kind}.json", f"{O}/glue/g_{L}_{kind}.json"
            if not (os.path.exists(e) and os.path.exists(o)): continue
            le = arb(json.load(open(e))["certified_lower_bound"]).lower()
            lo = arb(json.load(open(o))["certified_lower_bound"]).lower()
            # X1: a lower bound may never exceed an upper bound. odd: our rigorous U^od(L); l2: the Galerkin λ̂_2 (lam1, float, 1e-6)
            ub = arb(U(L, 1)) if kind == "odd" else arb(U(L, 0, "lam1")) * (1 + arb("1e-6"))
            out.append(dict(L=L, kind=kind, ours=lo.str(6, radius=False), elston=le.str(6, radius=False),
                            ratio_ours_over_elston=(lo / le).str(4, radius=False), X1=bool(not le > ub and not lo > ub)))
    json.dump(out, open(f"{O}/out/xcheck.json", "w"), indent=1); print(json.dumps(out, indent=1))


if __name__ == "__main__":
    c, a = sys.argv[1], sys.argv[2:]
    dict(ladder=ladder, nc=nc, t15=t15, glue=glue, xcheck=xcheck)[c](*a)
