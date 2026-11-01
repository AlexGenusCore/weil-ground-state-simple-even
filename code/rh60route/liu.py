"""Shared helpers for the Liu value certificate (DESIGN.md, design_changes.md): paths, exact windows, exact ball-matrix I/O.
Matrix files: gzip text, line 1 = JSON metadata, then one entry per line "man exp rman rexp" (hex): the arb midpoint and radius
exactly, so storage adds no rounding. sha256 of every file goes into the run records (checker pins)."""
import gzip, hashlib, json, os, resource, sys, time
from math import ceil
from fractions import Fraction
from flint import arb, arf, arb_mat, ctx

HERE = os.path.dirname(os.path.abspath(__file__))
HP = os.path.dirname(os.path.dirname(HERE))          # highprec/
for p in (HP, os.path.join(HP, "lb"), os.path.join(HP, "gap", "elston"), os.path.join(os.path.dirname(HP), "extend"),
          os.path.join(HERE, "mori")):
    if p not in sys.path: sys.path.insert(0, p)
DATA = os.environ.get("LIU_DATA", os.path.join(HERE, "data"))


def Lwin(Ldec):
    """Exact window: ceil(Ldec * 2^24) / 2^24 >= Ldec (M2). Returns (string id, Fraction, exact arb)."""
    q = Fraction(ceil(Fraction(Ldec) * 2 ** 24), 2 ** 24)
    return f"{q.numerator}/{q.denominator}", q, arb(q.numerator) / q.denominator


def frac_arb(q):
    return arb(q.numerator) / q.denominator  # exact for dyadic q at prec >= bits of q


def dyadic_le(x, bits=20):  # largest k/2^bits <= lower end of the ball x
    return Fraction(int((x.lower() * 2 ** bits).floor().unique_fmpz()), 2 ** bits)


def lg2(x):  # ~log2 of a nonnegative exact arb (e.g. a radius); -inf for 0. Diagnostics only.
    m, e = x.man_exp(); m = int(m)
    return float("-inf") if m == 0 else int(e) + m.bit_length()


def peak_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6  # Linux: KB -> GB


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def _hx(m, e):
    return f"{int(m):x} {int(e):x}"


def arb_hex(x):  # post-audit F2: exact text form "man exp" (hex) of an exact arb (radius 0), e.g. a trusted upper bound
    assert x.rad() == 0 and x.is_finite(), x
    return _hx(*x.mid().man_exp())


def hex_arb(t):  # inverse of arb_hex, exact
    m, e = (int(v, 16) for v in t.split())
    return arb(arf((m, e)))


def save_mat(path, M, **meta):
    """Exact (lossless) storage of an arb_mat. Refuses to overwrite earlier evidence."""
    assert not os.path.exists(path), path
    meta.update(rows=M.nrows(), cols=M.ncols())
    with gzip.open(path + ".tmp", "wt", compresslevel=3) as f:
        f.write(json.dumps(meta) + "\n")
        for x in M.entries():
            assert x.is_finite()
            f.write(_hx(*x.mid().man_exp()) + " " + _hx(*x.rad().man_exp()) + "\n")
    os.replace(path + ".tmp", path)
    return sha(path)


def load_mat(path, K=None):
    """Load the leading K x K block (all if K is None). Exact: arb(arf, arf) does not round."""
    with gzip.open(path, "rt") as f:
        meta = json.loads(f.readline()); n = meta["cols"]; K = K or n; assert K <= n
        rows = []
        for i in range(K):
            row = []
            for j in range(n):
                m, e, r, re = (int(v, 16) for v in f.readline().split())
                if j < K: row.append(arb(arf((m, e)), arf((r, re))))
            rows.append(row)
    return arb_mat(rows), meta


def sym(M):  # (M + M^T)/2 encloses the symmetric truth when M encloses it entrywise
    return (M + M.transpose()) / 2


def ident(n):
    I = arb_mat(n, n)
    for i in range(n): I[i, i] = 1
    return I


def rowsum_rad(M):  # max_i sum_j rad(M_ij): an operator-norm bound for a symmetric radius pattern
    # post-audit F1: max over exact upper ends (max over overlapping balls keeps the first ball and can under-state)
    n, m = M.nrows(), M.ncols(); E = M.entries()
    return max(sum((E[i * m + j].rad() for j in range(m)), arb(0)).upper() for i in range(n))


def norm_bound(M):
    """sqrt(||M||_1 ||M||_inf) >= ||M||_2, from upper ends of |entries| (Mori, check_certificate.norm_bound)."""
    n, m = M.nrows(), M.ncols(); E = [abs(x).upper() for x in M.entries()]
    r = max(sum(E[i * m:(i + 1) * m], arb(0)).upper() for i in range(n))  # F1: max of exact upper ends
    c = max(sum((E[i * m + j] for i in range(n)), arb(0)).upper() for j in range(m))
    return (r * c).sqrt().upper()


class Log:
    def __init__(self, path):
        self.path, self.t0 = path, time.time()

    def __call__(self, **rec):
        rec.update(t_wall=round(time.time() - self.t0, 1), peak_gb=round(peak_gb(), 2), utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        with open(self.path, "a") as f: f.write(json.dumps(rec, default=str) + "\n")
        print(json.dumps(rec, default=str)[:400], flush=True)
