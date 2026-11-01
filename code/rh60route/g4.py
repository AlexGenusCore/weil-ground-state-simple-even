"""Gate G4 (SPEC §13, PREREG §3): the 9 registered mutations at L = 1.5, each run at the passing μ of that sector's L = 1.5
control, plus (AUDIT fixes) the G6 auditor's 3 mutations and the F1/F2 demonstrations. Caught = the run does not PASS and
names the failing gate(s) (or fails as a run). Entry mutations also go through the full Arb G0 (eqp.py) with the mutated
closed forms; for the shared-input mutations (pp_drop, lam_n) that G0 is expected to be blind (AUDIT F1), G0i is not.
Usage: python g4.py Ldec Uev  -> <run dir>/out/G4_<Ldec>.json
Method credit: rh_60 v1 / rh_45 v1 (unrefereed AI-agent preprints); harness is ours."""
import glob, json, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import pilot, eqp, entries

L, Uev = sys.argv[1], sys.argv[2]; O = pilot.O
def passing(prefix):
    for f in sorted(glob.glob(f"{O}/out/{prefix}_{L}_*.json")):
        r = json.load(open(f))
        if r.get("result") == "PASS" and not r.get("mut"): return r
odd, l2 = passing("odd"), passing("l2")
assert odd and l2, "G4 needs passing L-controls in both kinds"
expect = dict(pole0="G0", gamma1="G0", Qq0="G5", s_half="G-S", rM0="C-rM", defl_sign="G5", tau0="C-tau", M0="G2/G5", gen="G5p",
              aud_sr_q0="G5 (F3)", aud_tau_half="C-ind (F7)", aud_rM_half="C-ind (F7)",
              pp_drop="G0i (F1)", lam_n="G0i (F1)", gen2K="G5p (F2)")
extra = dict(gen2K=["--Rmax", "128"])  # Rmax below Rq(2K): the regime where the pilot's capped G5′ path was vacuous
out = dict(Ldec=L, odd_mu_rel=odd["mu_rel"], l2_mu_rel=l2["mu_rel"], mutations={})
def job(m):
    base = l2 if m in ("gamma1", "defl_sign", "gen2K") else odd
    args = pilot.common(L, Uev) + ["--eps", str(base["eps"]), "--mu-rel", base["mu_rel"], "--mu-ref", base["mu_ref"],
                                    "--tmin", str(base["tmin"]), "--sr", "--mut", m] + (["--deflate"] if base["deflate"] else []) + extra.get(m, [])
    return pilot.run(f"g4_{L}_{m}", args)
with ThreadPoolExecutor(int(os.environ.get("G4_PAR", "1"))) as ex: runs = dict(zip(expect, ex.map(job, expect)))
for m, exp in expect.items():
    r = runs[m]
    caught = r.get("result") != "PASS"
    rec = dict(expected=exp, result=r.get("result"), failed_gates=r.get("failed_gates"), reason=r.get("reason"), caught=caught)
    if m in ("pole0", "gamma1", "pp_drop", "lam_n"):
        entries.SHARED_MUT = m if m in ("pp_drop", "lam_n") else None
        g0 = eqp.run(L, 160, mut=m); rec["full_G0_passed"] = g0["passed"]; entries.SHARED_MUT = None
        if m in ("pole0", "gamma1"): rec["caught"] = caught or not g0["passed"]
    out["mutations"][m] = rec
out["all_caught"] = all(v["caught"] for v in out["mutations"].values())
json.dump(out, open(f"{O}/out/G4_{L}.json", "w"), indent=1); print(json.dumps(out, indent=1))
