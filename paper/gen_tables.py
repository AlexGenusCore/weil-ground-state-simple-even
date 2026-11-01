"""Generate paper/generated.tex (Piece IV table, Piece III rows past 1.4035, cross-check, text macros) from the run records.

Usage: python paper/gen_tables.py GLUE WINDOWS PIECE3 [OUT ...] > paper/generated.tex
  GLUE     glued Piece IV set: g_<L>_{odd,l2}.json and upper*.jsonl (shipped: data/piece4/glue)
  WINDOWS  the 54-window list (shipped: data/piece4/windows.txt)
  PIECE3   Piece III (Elston-route) records g_<L>_{odd,l2}.json and upper*.jsonl (shipped: data/piece3)
  OUT      optional run-record directories (all runs, passing or not); if given, every glued record must equal, byte for
           byte, the first passing record in sorted order over them (the registered selection rule)
Every number in generated.tex comes from these files; nothing is typed by hand. Checks: each glued record has result PASS, no
failed gate, all 15 gates true, mut null, the grid stamp, Ldec equal to its window and the right sector; every step
min(l_odd, l_2)(L_{i+1}) > U_ev(L_i) holds in exact arithmetic on the Arb endpoints. Lower bounds are rounded down, upper
bounds up, ratios down, to 4 significant digits."""
import json, os, sys
from fractions import Fraction
from flint import arb, ctx

ctx.prec = 512
STAMP = "7a3c6b287f840aba50fc11d49e6f919eb0cb758a6a0ce03e6248298feda4b9e8"  # sha256 of the run-time stamp of grid G
glue, wfile, p3, outdirs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]


def frac(x):  # exact value of an exact Arb endpoint
    m, e = x.mid().man_exp()
    return Fraction(int(m)) * Fraction(2) ** int(e)


def r4(q, up=False):  # 4 significant digits, directed; returns (mantissa 1000..9999, exponent)
    e = len(str(q.numerator)) - len(str(q.denominator))
    while q < Fraction(10) ** e: e -= 1
    while q >= Fraction(10) ** (e + 1): e += 1
    s = q / Fraction(10) ** (e - 3)
    m = -(-s.numerator // s.denominator) if up else s.numerator // s.denominator
    return (1000, e + 1) if m == 10000 else (m, e)


def sci(q, up=False):
    m, e = r4(q, up)
    return f"{m // 1000}.{m % 1000:03d}e{e}"


def tex(q, up=False):  # same value as sci(), typeset for math mode in the text (\\e from main.tex)
    m, e = r4(q, up)
    return f"{m // 1000}.{m % 1000:03d}\\e{{{e}}}"


def fix(q):  # floored, 4 significant digits, fixed point (ratios)
    m, e = r4(q)
    s = str(m)
    if e < 0: return "0." + "0" * (-e - 1) + s
    return s[:e + 1] + ("." + s[e + 1:] if e < 3 else "") if e <= 3 else str(m * 10 ** (e - 3))


def lo(rec): return frac(arb(rec["certified_lower_bound"]).lower())


def uppers(d):  # smallest rigorous upper end per (L, par) over every upper*.jsonl in d
    U = {}
    for fn in sorted(f for f in os.listdir(d) if f.startswith("upper") and f.endswith(".jsonl")):
        for line in open(os.path.join(d, fn)):
            r = json.loads(line)
            assert r["rigorous_quadrature"] is True, fn
            k, v = (r["L"], r.get("par", 0)), frac(arb(r["lam0_upper"]).upper())
            U[k] = min(U.get(k, v), v)
    return U


# ---------------------------------------------------------------- Piece IV
W = [l.strip() for l in open(wfile) if l.strip()]
assert len(W) == 54 and all(arb(a) < arb(b) for a, b in zip(W, W[1:])), "windows"
outs = {f: os.path.join(d, f) for d in outdirs for f in os.listdir(d) if f.endswith(".json")}
rec = {}
for L in W[1:]:
    for kind in ("odd", "l2"):
        g = os.path.join(glue, f"g_{L}_{kind}.json")
        r = json.load(open(g))
        assert (r["Ldec"], r["mut"], r["result"], r["failed_gates"], r["stamp_sha256"]) == (L, None, "PASS", [], STAMP), g
        assert all(r["gates"].values()) and len(r["gates"]) == 15, g
        assert (r["eps"], bool(r["deflate"])) == ((-1, False) if kind == "odd" else (1, True)), g
        if outs:
            ok = [f for f in sorted(outs) if f.startswith(f"{kind}_{L}_") and json.load(open(outs[f]))["result"] == "PASS"]
            assert ok and open(outs[ok[0]], "rb").read() == open(g, "rb").read(), (g, ok[:1])
        rec[L, kind] = r
U = uppers(glue)

rows, steps = [], []
for i, L in enumerate(W):
    u = sci(U[L, 0], up=True) if i < len(W) - 1 or (L, 0) in U else "---"
    if i == 0:
        rows.append(f"0 & {L} & {u} & --- & --- & --- & --- & ---\\\\")
        continue
    o, t = rec[L, "odd"], rec[L, "l2"]
    m = min(lo(o), lo(t))
    q = m / U[W[i - 1], 0]
    assert m > U[W[i - 1], 0], ("step fails", L)
    steps.append((q, W[i - 1], L, "odd" if lo(o) <= lo(t) else "l2"))
    rung = t["label"].split(f"l2_{L}_")[1]
    mark = {"1o4": "", "1o1024": "$^{\\dagger}$", "1o4_e1": "$^{\\ddagger}$"}[rung]
    assert o["label"] == f"odd_{L}_2o3"
    rows.append(f"{i} & {L} & {u} & {sci(lo(o))} & {sci(lo(t))}{mark} & {fix(q)} & {o['N']} & {t['N']}\\\\")
assert len(steps) == 53 and all(s[3] == "odd" for s in steps)
qmin = min(steps)
part = [s for s in steps if arb(s[2]) <= arb("1.91912841796875")]
assert len(part) == 43
Lp, Lg = "1.91912841796875", "1.92364501953125"
gstep = [s for s in steps if s[1:3] == (Lp, Lg)][0]
e1 = rec[Lg, "l2"]
assert e1["label"] == f"l2_{Lg}_1o4_e1" and e1["N"] == 38912

# ---------------------------------------------------------------- Piece III past 1.4035 and the cross-check
P = ["1.4035", "1.4255", "1.447", "1.468", "1.4885"]
U3 = uppers(p3)
g3 = {(L, k): json.load(open(os.path.join(p3, f"g_{L}_{k}.json"))) for L in P for k in ("odd", "l2")}
for (L, k), r in g3.items():
    assert r["args"]["a"] == L and r["sector"] == ("odd" if k == "odd" else "even") and bool(r["deflate"]) == (k == "l2")
rows3, grid3, ratios3, xrows, xo, x2 = [], [], [], [], [], []
for a, b in zip(P, P[1:]):
    o, t = g3[b, "odd"], g3[b, "l2"]
    m = min(lo(o), lo(t))
    assert m > U3[a, 0], ("Piece III step fails", b)
    ratios3.append(m / U3[a, 0])
    rows3.append(f"{b} & {sci(U3[b, 0], up=True)} & {sci(lo(o))} & {sci(lo(t))} & {fix(m / U3[a, 0])}\\\\")
    keys = ("delta", "beta_k", "tsharp", "nmodes", "gl", "prec")
    newn = ", ".join(str(n) for n in o["comb"] if n not in g3[a, "odd"]["comb"])
    if all(o["args"][k] == t["args"][k] for k in keys):
        A = o["args"]
        grid3.append(f"{b} & {A['delta']} & {A['beta_k']} & {A['tsharp']} & {A['nmodes']} & {A['gl']} & {A['prec']} & "
                     f"{t['seconds']} / {o['seconds']} & {newn}\\\\")
    else:
        for k, r in (("even", t), ("odd", o)):
            A = r["args"]
            grid3.append(f"{b}, {k} & {A['delta']} & {A['beta_k']} & {A['tsharp']} & {A['nmodes']} & {A['gl']} & {A['prec']} & "
                         + (f"{r['seconds']} / ---" if k == "even" else f"--- / {r['seconds']}") + f" & {newn if k == 'even' else ''}\\\\")
    qo, q2 = lo(rec[b, "odd"]) / lo(o), lo(rec[b, "l2"]) / lo(t)
    xo.append(qo); x2.append(q2)
    xrows.append(f"{b} & {sci(lo(rec[b, 'odd']))} & {sci(lo(o))} & {fix(qo)} & {sci(lo(rec[b, 'l2']))} & {sci(lo(t))} & {fix(q2)} & "
                 f"{rec[b, 'odd']['seconds']}, {rec[b, 'l2']['seconds']} & {o['seconds']}, {t['seconds']}\\\\")
    assert lo(o) <= U[b, 1], ("X1", b)  # Elston's odd lower bound below our rigorous U_od

# ---------------------------------------------------------------- output
mac = {
    "PIVrows": "\n".join(rows), "PIVminratio": fix(qmin[0]), "PIVminstep": f"[{qmin[1]},{qmin[2]}]",
    "PIVpartmin": fix(min(part)[0]), "PIVgapratio": fix(gstep[0]), "PIVgapltwo": tex(lo(e1)), "PIVgapU": tex(U[Lp, 0], up=True),
    "PIVoddTwo": tex(lo(rec["2", "odd"])), "PIVltwoTwo": tex(lo(rec["2", "l2"])), "PIVUTwo": tex(U["2", 0], up=True),
    "PIVsecmin": str(min(r["seconds"] for r in rec.values())), "PIVsecmax": str(max(r["seconds"] for r in rec.values())),
    "PIVtwoRatio": tex(min(lo(rec["2", "odd"]), lo(rec["2", "l2"])) / U["2", 0]),
    "PIIIrows": "\n".join(rows3), "PIIIgridrows": "\n".join(grid3), "PIIIextmin": fix(min(ratios3)),
    "PIVxrows": "\n".join(xrows), "PIVxodd": f"{fix(min(xo))}--{fix(max(xo))}", "PIVxltwo": f"{fix(min(x2))}--{fix(max(x2))}",
}
print("% Generated by gen_tables.py from the run records; do not edit.")
for k, v in mac.items(): print(f"\\newcommand{{\\{k}}}{{{v}}}")
print(f"53 steps pass; min {fix(qmin[0])} on [{qmin[1]}, {qmin[2]}]; gap step {fix(gstep[0])}; partial 43 steps min "
      f"{fix(min(part)[0])}; Piece III past 1.4035 min {fix(min(ratios3))}", file=sys.stderr)
