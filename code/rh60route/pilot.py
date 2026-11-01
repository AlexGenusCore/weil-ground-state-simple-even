"""Pilot driver (PREREG.md §2, §4): runs certify.py per the registered rules on vm4 (nice, one process per run).
  python pilot.py run NAME [certify args...]            one run -> out/NAME.json, logs/NAME.log
  python pilot.py ladder odd Ldec Uod Uev [tag]          odd ladder {2/3,1/2,1/3,1/4,1/8,1/10}·U^od, float proposal picks the
                                                         start (first rung with p̂_min >= 2^-6), <= 3 rigorous runs, the 3rd
                                                         at 1/10 if the first two fail; stop at the first PASS
  python pilot.py ladder l2 Ldec Uev [tag]               λ_2 ladder {2^-2, 2^-10}·λ̂_2(M_0), then 2^4·U^ev; <= 3 runs
N2: a PASS with μ above U^σ (or above λ̂_2) writes out/STOP_N2 and stops everything.
Method credit: rh_60 v1 (bramble_trace) and rh_45 v1 (lihongmin), unrefereed AI-agent preprints; driver is ours."""
import json, os, subprocess, sys
from fractions import Fraction

R = os.path.expanduser("~/rh60route"); HERE = os.path.dirname(os.path.realpath(__file__))
O = os.environ.get("RH60_RUN", R)  # run directory for out/ and logs/ (default: the pilot's)
PY = sys.executable


def common(L, Uev):
    a = ["--L", L, "--Uev", Uev, "--s-file", f"{R}/data/s/s_{L}.json", "--ritz", f"{R}/data/ritz_{L}.json", "--workdir", f"{R}/work"]
    b = f"{R}/out/P0_bench.json"
    if os.path.exists(b): a += ["--cD", str(json.load(open(b))["c_8_us_per_pair"] * 1e-6)]
    return a


def run(name, args):
    out = f"{O}/out/{name}.json"
    if os.path.exists(f"{O}/out/STOP_N2"): sys.exit("STOP_N2 present")
    if not os.path.exists(out):
        env = dict(os.environ); env.setdefault("RH60_STAMP", f"{R}/PREREG.stamp")
        with open(f"{O}/logs/{name}.log", "a") as lg:
            subprocess.run(["nice", "-n", "5", PY, "-I", os.path.join(HERE, "certify.py"), *args, "--out", out, "--label", name],
                           stdout=lg, stderr=subprocess.STDOUT, env=env)
    return json.load(open(out)) if os.path.exists(out) else dict(result="CRASH")


def n2(rec, Ubound):
    if rec.get("result") == "PASS" and Fraction(rec["mu"]) > Fraction(Ubound):
        open(f"{O}/out/STOP_N2", "w").write(json.dumps(dict(run=rec.get("label"), mu=rec["mu"], U=str(Ubound))))
        sys.exit("N2 violation: STOP")


def ladder_odd(L, Uod, Uev, tag, rungs=("2/3", "1/2", "1/3", "1/4", "1/8", "1/10")):  # grid: step-aware rungs (grid/grid.py)
    rungs = list(rungs)
    base = common(L, Uev) + ["--eps", "-1", "--mu-ref", Uod, "--tmin", "1"]
    nrig, i, hist = 0, 0, []
    while i < len(rungs) and nrig == 0:  # proposal phase: SR only if p̂_min >= 2^-6
        last = i == len(rungs) - 1  # no rung proposed: the 1/10 rung is run rigorously anyway (it decides kill K2)
        r = run(f"odd_{tag}_{rungs[i].replace('/', 'o')}", base + ["--mu-rel", rungs[i]] + (["--sr"] if last else ["--sr-if-pmin", str(2 ** -6)]))
        hist.append((rungs[i], r.get("result"), r.get("float_pmin")))
        if r.get("result") in ("PASS", "FAIL"): nrig += 1
        if r.get("result") == "PASS": n2(r, Uod); return hist
        i += 1
    while nrig < 3 and i + 1 < len(rungs):
        i = len(rungs) - 1 if nrig == 2 else i + 1  # the 3rd rigorous run is the 1/10 rung
        r = run(f"odd_{tag}_{rungs[i].replace('/', 'o')}", base + ["--mu-rel", rungs[i], "--sr"])
        hist.append((rungs[i], r.get("result"), r.get("float_pmin"))); nrig += 1
        if r.get("result") == "PASS": n2(r, Uod); return hist
    return hist


def ladder_l2(L, Uev, tag, rungs=None):  # grid: third rung 2·U^ev(L_prev) (grid/grid.py)
    rungs = rungs or [("1/4", "lam2hat"), ("1/1024", "lam2hat"), ("16", Uev)]
    base = common(L, Uev) + ["--eps", "1", "--deflate", "--tmin", "0.5"]
    hist = []
    for rel, ref in rungs:
        r = run(f"l2_{tag}_{rel.replace('/', 'o')}", base + ["--mu-rel", rel, "--mu-ref", ref, "--sr"])
        hist.append((rel, ref, r.get("result")))
        if r.get("result") == "PASS":
            n2(r, Fraction(r["lam2hat_M0"])); return hist
    return hist


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "run": print(json.dumps(run(sys.argv[2], sys.argv[3:]).get("result")))
    elif cmd == "ladder" and sys.argv[2] == "odd": print(ladder_odd(*sys.argv[3:6], sys.argv[6] if len(sys.argv) > 6 else sys.argv[3]))
    elif cmd == "ladder" and sys.argv[2] == "l2": print(ladder_l2(sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else sys.argv[3]))
