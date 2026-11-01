"""Matrix entries of the Weil form Q_L in the conjugated trigonometric basis (SPEC §1-§2.2, PROOFS P5-P7), as Arb balls.

Method credit: the response/displacement architecture is bramble_trace's (rh_60 v1, "Full-source Schur certificates for Weil
positivity at support radius two", rStation 2026-10-26); the Green-response identity and the bases are lihongmin's (rh_45 v1,
rStation 2026-10-23). Both are unrefereed AI-agent preprints; every formula here is from our SPEC.md/PROOFS.md (general L),
written clean-room (no rStation code was opened, copied or adapted).

u_q = γ_q (2L/π²) Φ_ε(κ_q), v_q = γ_q, λ_q = k_q², A_qr = (u_q v_r − v_q u_r)/(λ_q − λ_r) (q ≠ r),
A_qq = H(κ) − 2C(κ) + [κ>0] S(κ)/(Lκ) + (2/L) γ_q² R_ε(κ).
Mutations (G4 harness only): mut="pole0" sets α_− = 0 (odd pole dropped); mut="gamma1" sets γ_0 = 1.
Shared-input mutations (AUDIT F1 demonstration; set SHARED_MUT, which reaches every Form, including the eq. (P) side of G0):
"pp_drop" drops the largest prime power, "lam_n" uses log n in place of Λ(n) = log p."""
import math
from flint import arb, acb, ctx


def prime_powers(Lb, X):
    """[(n, log p)] for prime powers n with log n < 2L, decided in Arb away from the boundary (SPEC §1)."""
    out = []
    for n in range(2, X + 1):
        p = next(d for d in range(2, n + 1) if n % d == 0)
        m = n
        while m % p == 0: m //= p
        if m != 1: continue
        ln = arb(n).log()
        assert abs(ln - 2 * Lb) > arb(2) ** -40, n
        if ln < 2 * Lb: out.append((n, p))
    return out


SHARED_MUT = None


class Form:
    def __init__(self, Ldec, eps, prec, J=None, mut=None):
        self.Ldec, self.eps, self.prec, self.mut = Ldec, eps, prec, mut
        self.omega2 = 0 if eps == 1 else 1           # 2ω
        with ctx.workprec(prec):
            L = self.L = arb(Ldec)
            self.pi = arb.pi(); self.logpi = self.pi.log()
            X = int(math.exp(2 * float(Ldec))) + 2
            self.pp = prime_powers(L, X)
            if SHARED_MUT == "pp_drop": self.pp = self.pp[:-1]
            self.w = [arb(n if SHARED_MUT == "lam_n" else p).log() / arb(n).sqrt() for n, p in self.pp]
            self.y = [arb(n).log() for n, _ in self.pp]
            self.wc = [w * (1 - y / (2 * L)) for w, y in zip(self.w, self.y)]  # weights of C(x)
            self.theta = [self.pi * y / L for y in self.y]                      # φ_n = π y_n / L
            self.alpha = (L / 2).sinh() ** 2 if eps == 1 else -((L / 2).cosh() ** 2)
            if mut == "pole0" and eps == -1: self.alpha = arb(0)
            self.J = J or math.ceil(prec * math.log(2) / (4 * float(Ldec))) + 2
            self.c = [arb(2 * j) + arb(1) / 2 for j in range(self.J)]
            self.c2 = [c * c for c in self.c]
            self.eta = [(-2 * c * L).exp() for c in self.c]
            cJ = arb(2 * self.J) + arb(1) / 2
            self.dJ = ((-2 * cJ * L).exp() / (1 - (-4 * L).exp())).upper()        # δ_J (P7)
            self.dJc = (self.dJ / (cJ * cJ)).upper()
            self.psi1q = acb(arb(1) / 4).polygamma(1).real                        # ψ'(1/4)

    def k(self, q):   # k_q = q + ω, exact
        return arb(2 * q + self.omega2) / 2

    def lam4(self, q):  # 4 λ_q, an exact integer
        return (2 * q + self.omega2) ** 2

    def gam(self, q):
        if q == 0 and self.eps == 1 and self.mut != "gamma1": return arb(2).sqrt() / 2
        return arb(1)

    def trig(self, q0, q1):
        """S(κ_q), C(κ_q) for q in [q0, q1): rotation recurrence e^{i k_q φ_n}, re-anchored every 32 steps (complex ball
        rotation has the wrapping effect: radii can grow by up to √2 per step, so at most 2^16 over a block)."""
        S, C = [], []
        st = [acb.exp_pi_i(acb(th / self.pi)) for th in self.theta]
        for b0 in range(q0, q1, 32):
            b1 = min(q1, b0 + 32)
            z = [acb.exp_pi_i(acb(self.k(b0) * th / self.pi)) for th in self.theta]
            for q in range(b0, b1):
                S.append(sum((w * zz.imag for w, zz in zip(self.w, z)), arb(0)))
                C.append(sum((w * zz.real for w, zz in zip(self.wc, z)), arb(0)))
                z = [zz * s for zz, s in zip(z, st)]
        return S, C

    def rows(self, q0, q1, diag=True):
        """For q in [q0, q1): dict of lists u, A (if diag), H, S (balls at self.prec)."""
        out = dict(u=[], A=[], H=[], S=[])
        with ctx.workprec(self.prec):
            L, eps, al = self.L, self.eps, self.alpha
            S, C = self.trig(q0, q1)
            pref = 2 * L / self.pi ** 2
            for i, q in enumerate(range(q0, q1)):
                kap = self.pi * self.k(q) / L
                g = self.gam(q)
                if kap == 0:  # even q = 0
                    H = acb(arb(1) / 4).digamma().real - self.logpi
                    out["u"].append(g * pref * (-al / (arb(1) / 4)))  # Φ(0) = F(0) = −α/(1/4)
                    if diag:
                        R0 = self.psi1q / 4 - sum((e / c2 for e, c2 in zip(self.eta, self.c2)), arb(0)) + arb(0, self.dJc) + 16 * al
                        out["A"].append(H - 2 * C[i] + R0 / L)
                    out["H"].append(H); out["S"].append(S[i])
                    continue
                z = acb(arb(1) / 4, kap / 2)
                ps = z.digamma(); H = ps.real - self.logpi
                x2 = kap * kap; q4 = arb(1) / 4 + x2
                d = [c2 + x2 for c2 in self.c2]
                resp1 = x2 * sum((e / dd for e, dd in zip(self.eta, d)), arb(0)) + arb(0, self.dJ)
                F = kap / 2 * ps.imag - eps * resp1 - al / q4
                out["u"].append(g * pref * (kap * S[i] + F))
                if diag:
                    R = ps.imag / (4 * kap) + z.polygamma(1).real / 8 \
                        - eps * (sum((c2 * e / (dd * dd) for c2, e, dd in zip(self.c2, self.eta, d)), arb(0)) + arb(0, self.dJc)) \
                        + al / (q4 * q4)
                    out["A"].append(H - 2 * C[i] + S[i] / (L * kap) + 2 / L * g * g * R)
                out["H"].append(H); out["S"].append(S[i])
        return out

    def Hk(self, q):  # H(κ_q) alone
        with ctx.workprec(self.prec):
            kap = self.pi * self.k(q) / self.L
            return acb(arb(1) / 4, kap / 2).digamma().real - self.logpi


if __name__ == "__main__":  # self-check: SPEC §2.2 references at L = 2 (also part of G0)
    ctx.prec = 256
    for eps, ref in ((1, "0.0175704652725981700130"), (-1, "0.0574304055992914590")):
        F = Form("2", eps, 256)
        a = F.rows(0, 1)["A"][0]
        assert abs(a - arb(ref)) < arb(10) ** -(len(ref) - 3), (eps, a)
        assert len(F.pp) == 24 and F.pp[-1][0] == 53
        print(eps, a.str(25))
    print("entries self-check OK")
