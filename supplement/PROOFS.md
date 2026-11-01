# PROOFS: first-principles re-derivation of the rh_60-route constants and lemmas (general L, spot values at L = 2)

**Status.** Written 2026-10-31 from `SPEC.md`, our paper `weil-public/paper/main.tex` and our own code. No rStation file (manuscript,
supplement or study note) was opened for this document. Nothing scored or parameter-setting was run. PREREG.md is not yet stamped.
Spot values are mpmath/numpy proposals from `proofs_spot.py` (this directory; laptop, < 1 GB) and carry no rigour.

**Credit.** The architecture is bramble_trace's (rh_60 v1, "Full-source Schur certificates for Weil positivity at support radius
two", rStation 2026-10-26): summed digamma responses, the displacement-rank-2 matrix, exact core elimination, moment/Abel tail, HS
omitted tail. The Green-response identity and the bases are lihongmin's (rh_45 v1, "Cutoff-free positivity of localized Weil forms
through the (log 11)/2 threshold", rStation 2026-10-23). Both are **unrefereed AI-agent preprints reviewed only by AI agents**; every
statement below is proved here from scratch, and "rh60 (x.y)" only says which of their steps a lemma replaces. Ours: the general-L
forms, μ-shift, deflation, the virtual-label proof of rh60 (5.5), the form-core argument, Lemma SR and the general-L tail constants.

**Clean room.** The implementer reads this file and SPEC.md only. No rStation code may be copied, adapted or vendored.

**Conventions.** Notation is SPEC §1. "Arb" means python-flint 0.9 `arb`/`acb` balls; `ub(x)` = `x.upper()`, `lb(x)` = `x.lower()`.
A *bound* is a ball whose upper (or lower) endpoint is used, never its midpoint. A comparison `a > b` is accepted only when Arb
returns True (certain). Decimal L enters as `arb("L")`; dyadic data as exact `arb(p)/2**e`. ω ∈ {0, ½}, k_q = q + ω, λ_q = k_q²,
κ_q = πk_q/L, w_n = Λ(n)/√n, y_n = log n, φ_n = πy_n/L, c_j = 2j + ½, η_j = e^{−2c_jL}. Sector ε = +1 (ev) or −1 (od).

Trusted base (not re-proved here; see §11): Arb/FLINT; our paper §2.3 (Q_L closable and semibounded on C_c^∞(−L, L), compact
resolvent, min-max) and Lemma `lem:M` (Re ψ(s + iy) increasing in |y|); Elston's audited cell evaluation inside stage S (P9).

---

## 1. The form in the trigonometric basis

### P1. Green kernel identity (rh_45 Lemma 3.1; used by rh60 §2)

**Statement.** Let c > 0 and E_c^ε(x, y) = e^{−c|x−y|} + ε e^{−c(x+y)} on (0, L)². Let R_c^ε = (−∂² + c²)⁻¹ on L²(0, L) with
v′(L) = 0 and v′(0) = 0 (ε = +1) or v(0) = 0 (ε = −1). Put r_c(x) = e^{−cL}(e^{cx} + εe^{−cx})/√(1 − εe^{−2cL}). Then, as kernels,

  2c R_c^ε − E_c^ε = r_c ⊗ r_c,

and R_c^ε has the orthonormal eigenbasis ẽ_q with eigenvalues 1/(c² + κ_q²).

**Proof.** For x ≤ y the Green function is G⁺ = cosh(cx)cosh(c(L−y))/(c sinh cL) and G⁻ = sinh(cx)cosh(c(L−y))/(c cosh cL)
(symmetric extension for x ≥ y). Each solves the homogeneous equation off the diagonal and meets the boundary conditions, and the
jump of ∂_xG across x = y is −[cosh(cy)sinh(c(L−y)) + sinh(cy)cosh(c(L−y))]/sinh(cL) = −1 (even) or
−[sinh(cy)sinh(c(L−y)) + cosh(cy)cosh(c(L−y))]/cosh(cL) = −1 (odd). For x ≤ y, E⁺ = 2cosh(cx)e^{−cy} and E⁻ = 2sinh(cx)e^{−cy}. Using
cosh(cL − cy) − e^{−cy}sinh(cL) = e^{−cL}cosh(cy) and cosh(cL − cy) − e^{−cy}cosh(cL) = e^{−cL}sinh(cy):
- 2cG⁺ − E⁺ = 2cosh(cx)cosh(cy)e^{−cL}/sinh(cL) = 4cosh(cx)cosh(cy)e^{−2cL}/(1 − e^{−2cL}) = r_c(x)r_c(y);
- 2cG⁻ − E⁻ = 2sinh(cx)sinh(cy)e^{−cL}/cosh(cL) = 4sinh(cx)sinh(cy)e^{−2cL}/(1 + e^{−2cL}) = r_c(x)r_c(y).
The functions cos(πqx/L) (Neumann–Neumann) and sin(π(q+½)x/L) (Dirichlet–Neumann) are the complete Sturm–Liouville eigenbases. ∎

**Arb.** Gate check only: evaluate both sides at 200 random rational (x, y, c, L); the difference ball must contain 0.

**L = 2 (mp, dps 30).** Max |2cR − E − r(x)r(y)| over 200 random points: 2.5e−29 (ε = +1), 4.9e−31 (ε = −1).

### P2. Green expansion of Q_L on smooth test functions (rh_45 Lemma 3.1 assembled; rh60 (2.1)–(2.4))

**Statement.** Let f = 𝒰_ε v ∈ C_c^∞(−L, L) have parity ε, and x_q = ⟨v, ẽ_q⟩. Then

  Q_L(f) = Σ_q H(κ_q) x_q² + ⟨B_p^ε v, v⟩ + Σ_{j≥0} ⟨r_j, v⟩² + ε⟨p_ε, v⟩²,  r_j := r_{c_j}, p_ε = e^{x/2} + εe^{−x/2},

where B_p^ε := 𝒰_ε*(−C_L)𝒰_ε, C_L = Σ_{𝒩_L} w_n(τ_{y_n} + τ_{−y_n}) compressed to L²(−L, L), (τ_s f)(t) = f(t − s).

**Proof.** *Archimedean part.* With ĝ = |F|² and g(0) = ‖f‖² = (1/2π)∫|F|², the digamma and log π terms of (weil) give
(1/2π)∫_ℝ H(t)|F(t)|² dt. From ψ(w) = −γ + Σ_n (1/(n+1) − 1/(n+w)) at w = ¼ + it/2 = (c_n + it)/2:
Re 1/(n+w) = 2c_n/(c_n² + t²), so H(t) − H(0) = Σ_j [2/c_j − 2c_j/(c_j² + t²)], every term ≥ 0. The Fourier transform of e^{−c|x|}
is 2c/(c² + t²), so (1/2π)∫ 2c/(c² + t²)|F|² = ∬ e^{−c|x−y|} f(x)f(y) = ⟨E_c^ε v, v⟩ (split (−L, L)² into four quadrants; the two
mixed quadrants carry ε). By P1 and Parseval in the basis ẽ_q,
  (1/2π)∫ [2/c − 2c/(c² + t²)] |F|² = (2/c)‖v‖² − 2c⟨R_c v, v⟩ + ⟨r_c, v⟩² = Σ_q [2/c − 2c/(c² + κ_q²)] x_q² + ⟨r_c, v⟩².
Sum over j: the left side converges to (1/2π)∫(H − H(0))|F|² by monotone convergence (finite, since H(t) = O(log t) and F decays
rapidly); the right side is a double series of nonnegative terms, so Tonelli gives Σ_q (H(κ_q) − H(0)) x_q² + Σ_j ⟨r_j, v⟩².
Add H(0)‖v‖² = Σ_q H(0) x_q².
*Primes.* g(y) = ∫ f(t) f(t − y) dt = ⟨f, τ_y f⟩, so the prime term is −⟨C_L f, f⟩ = ⟨B_p^ε v, v⟩. RC_LR = C_L for the reflection
R (Rτ_yR = τ_{−y}), so C_L preserves parity and B_p^ε is well defined.
*Pole.* F(−i/2) = ∫ f e^{x/2} = ⟨p_ε, v⟩/√2 and F(i/2) = ∫ f e^{−x/2} = ε⟨p_ε, v⟩/√2, so 2F(i/2)F(−i/2) = ε⟨p_ε, v⟩². ∎

**Arb.** Nothing to evaluate (identity); its numerical content is checked by P5/P6 against eq. (P).

### P3. Form core and closure (replaces rh60 §2's H^s cutoff and density argument, (2.5)–(2.7))

**Statement.**
(a) For f as in P2, x_q = O(k_q^{−m}) for every m.
(b) Q_L(f) = Σ_{q,r} A_qr x_q x_r with absolute convergence, where
  A_qr = H(κ_q)δ_qr + (B_p)_qr + 𝓡_qr + ε P_qr, 𝓡_qr = Σ_j ⟨r_j, ẽ_q⟩⟨r_j, ẽ_r⟩, P_qr = ⟨p_ε, ẽ_q⟩⟨p_ε, ẽ_r⟩,
and |A_qr − H(κ_q)δ_qr| ≤ 2Σ_{𝒩_L} w_n + (4/(1 − e^{−L}))(L + π/2) + ‖p_ε‖².
(c) Let μ, ϑ ≥ 0 and φ ∈ ℝ^K, Φ = 𝒰_ε Σ_{q<K} φ_q ẽ_q. If Σ_{q,r}(A_qr + ϑφ_qφ_r − μδ_qr) x_q x_r ≥ 0 for every coefficient
sequence of (a), then Q̄_L(f) + ϑ⟨Φ, f⟩² ≥ μ‖f‖² for every f in the form domain 𝒟^ε of the sector, where Q̄_L is the closure.

**Proof.** (a) Even f: v = √2 f|_(0,L) is smooth on [0, L], vanishes near L and has v^{(2i+1)}(0) = 0. Integrating ∫v cos(κ_q x)
by parts 2m times, every boundary term contains sin(0), sin(κ_q L) = 0, an odd derivative at 0, or a derivative at L (all 0), so
x_q = O(κ_q^{−2m}). Odd f: v^{(2i)}(0) = 0 and the same argument applies to sin(κ_q x).
(b) Σ_q |x_q| < ∞, so v = Σ x_q ẽ_q converges absolutely in L². For bounded operators B, ⟨Bv, v⟩ = Σ_{q,r} B_qr x_q x_r absolutely,
with |B_qr| ≤ ‖B‖. Apply this to B_p^ε (‖C_L‖ ≤ 2Σw_n, each translation has norm ≤ 1), to 𝓡 = Σ_j r_j ⊗ r_j (bounded by P8) and to
p_ε ⊗ p_ε. The diagonal H(κ_q) = O(log k_q) (Binet), so Σ(1 + log k_q)|x_q| < ∞ gives absolute convergence of the whole sum.
(c) Parity splits the closed form (paper Lemma `lem:parity`: Q(f_e + f_o) = Q(f_e) + Q(f_o), and ‖·‖² splits), so if f_n → f in
form norm with f_n ∈ C_c^∞, then the parity-ε parts converge to f in form norm, and they lie in C_c^∞. The hypothesis and P2, (b) give
Q_L(f_n^ε) + ϑ⟨Φ, f_n^ε⟩² − μ‖f_n^ε‖² ≥ 0. Q̄_L is continuous in form norm, and ⟨Φ, ·⟩ and ‖·‖ are L²-continuous; pass to the limit. ∎

No identification of the domain of A_L, and no H^s cutoff, is needed. (SPEC §2.4's bound
Σ_j(Σ_q|⟨r_j, ẽ_q⟩||x_q|)² ≤ Σ_j c_j^{−2}(Σ|x_q|)² is missing a factor 4/L; (b) avoids it.)

---

## 2. Matrix entries

### P4. Translation integrals (rh60 (2.6) at general L)

**Statement.** Let φ_q = γ_q cos(κ_q x)/√L (ε = +1) or sin(κ_q x)/√L (ε = −1) on (−L, L), 0 < y < 2L, and
I_qr(y) := (L/(γ_qγ_r))[⟨τ_y φ_q, φ_r⟩ + ⟨τ_{−y} φ_q, φ_r⟩]. Then, in both sectors,
- q ≠ r: I_qr(y) = (−1)^{q+r}·2[κ_r sin(κ_r y) − κ_q sin(κ_q y)]/(κ_q² − κ_r²);
- q = r, κ_q > 0: I_qq(y) = (2L − y)cos(κ_q y) − sin(κ_q y)/κ_q;  I_00(y) = 2(2L − y) (even, q = 0).

**Proof.** ⟨τ_y φ_q, φ_r⟩ = (γγ/L)T(a, b) with a = κ_q, b = κ_r and T(a, b) = ∫_{y−L}^{L} cos(a(t−y))cos(bt) dt (even case).
Write the product as ½[cos(st − ay)] summed over s = a ± b. Since aL = πq and bL = πr (even), sL = π(q ± r) and
sin(πm − θ) = −(−1)^m sin θ give ∫_{y−L}^{L} cos(st − ay) dt = −(−1)^{q+r}(sin ay + sin by)/(a + b) for s = a + b, and
(−1)^{q+r}(sin by − sin ay)/(a − b) for s = a − b. Adding: T(a, b) = (−1)^{q+r}(b sin by − a sin ay)/(a² − b²). T is symmetric, and
⟨τ_{−y}φ_q, φ_r⟩ = ⟨φ_q, τ_y φ_r⟩ = (γγ/L)T(b, a), which doubles it. For a = b, ½[cos(2at − ay) + cos(ay)] integrates to
½[(2L − y)cos(ay) − sin(ay)/a] because 2aL = 2πq. Odd case: sin(a(t−y))sin(bt) = ½[cos((a−b)t − ay) − cos((a+b)t − ay)] with
aL = π(q + ½); since (a ± b)L ∈ πℤ again, the same computation gives the same formulas. ∎

**Arb.** Not evaluated directly; enters through S and C in P5/P6.

### P5. Off-diagonal entries and displacement (rh60 (3.2)–(3.4) at general L)

**Statement.** With Φ_ε(x) = xS(x) + F_ε(x), F_ε(x) = G(x) − εx²Σ_j η_j/(c_j² + x²) − α_ε/(¼ + x²), u_q = γ_q(2L/π²)Φ_ε(κ_q),
v_q = γ_q, α_+ = sinh²(L/2), α_− = −cosh²(L/2):

  A_qr = (u_q v_r − v_q u_r)/(λ_q − λ_r)  (q ≠ r),  i.e.  ΛA − AΛ = u vᵀ − v uᵀ.

Also ⟨r_j, ẽ_q⟩ = √(2/L) γ_q c_j √(1 − εη_j)/(c_j² + κ_q²) and ⟨p_ε, ẽ_q⟩ = √(2/L) γ_q s_ε/(¼ + κ_q²), s_+ = sinh(L/2), s_− = cosh(L/2).

**Proof.** *Coefficients.* ∫_0^L cosh(cx)cos(κx) = c sinh(cL)(−1)^q/(c² + κ²) (κL = πq) and
∫_0^L sinh(cx)sin(κx) = c cosh(cL)(−1)^q/(c² + κ²) (κL = π(q + ½)); with 2e^{−cL}sinh(cL) = 1 − η and 2e^{−cL}cosh(cL) = 1 + η this
gives ⟨r_j, ẽ_q⟩. The pole coefficient is the case c = ½ without the r-normalisation.
*Primes.* By P4, (B_p)_qr = −(γ_qγ_r/L)(−1)^{q+r}Σ w_n I_qr(y_n) = (2γ_qγ_r/L)[κ_q S(κ_q) − κ_r S(κ_r)]/(κ_q² − κ_r²).
*Responses and pole.* c²/((c² + x²)(c² + y²)) = [x²/(c² + x²) − y²/(c² + y²)]/(x² − y²) and
1/((¼ + x²)(¼ + y²)) = [−1/(¼ + x²) + 1/(¼ + y²)]/(x² − y²). Using Σ_j x²/(c_j² + x²) = G(x) (since Im ψ(¼ + ix/2) = Σ 2x/(c_j² + x²))
and εs_ε² = α_ε: 𝓡_qr + εP_qr = (2γ_qγ_r/L)[F_ε(κ_q) − F_ε(κ_r)]/(κ_q² − κ_r²).
*Sum.* A_qr = (2γ_qγ_r/L)[Φ_ε(κ_q) − Φ_ε(κ_r)]/(κ_q² − κ_r²). Since κ_q² − κ_r² = (π/L)²(λ_q − λ_r), this is the claim. ∎

**Arb.** At precision p: y_n = arb(n).log(); w_n = arb(p_n).log()/arb(n).sqrt(); κ = arb.pi()*k/L;
G(x) = x/2 * acb(0.25, x/2).digamma().imag; Σ_j η_j/(c_j² + x²) to j < J plus arb(0, δ_J) (P7); S, C as plain Arb sums.

**L = 2.** 𝒩_2 has 24 prime powers (n ≤ 53), Σw_n = 12.19164592. eq. (P) cross-check of off-diagonals: §10.

### P6. Exact diagonal (rh60 (3.5)–(3.6) at general L)

**Statement.**
  A_qq = H(κ_q) − 2C(κ_q) + [κ_q > 0]·S(κ_q)/(Lκ_q) + (2/L)γ_q² R_ε(κ_q),
  R_ε(x) = Im ψ(¼ + ix/2)/(4x) + Re ψ′(¼ + ix/2)/8 − εΣ_j c_j²η_j/(c_j² + x²)² + α_ε/(¼ + x²)²,
  R_+(0) = ψ′(¼)/4 − Σ_j η_j/c_j² + 16α_+  (even q = 0, where the formula reads A_00 = H(0) − 2C(0) + R_+(0)/L).

**Proof.** *Primes:* by P4, (B_p)_qq = −(γ_q²/L)Σ w_n I_qq(y_n) = −2γ_q²C(κ_q) + γ_q²S(κ_q)/(Lκ_q); γ_q = 1 except at even
q = 0, where I_00 = 2(2L − y) gives −(1/(2L))·2Σ w_n(2L − y_n) = −2C(0). *Responses and pole:* 𝓡_qq + εP_qq =
(2/L)γ_q²[Σ_j c_j²(1 − εη_j)/(c_j² + κ²)² + α_ε/(¼ + κ²)²]. From Im ψ(¼ + ix/2) = Σ 2x/(c_j² + x²) and
Re ψ′(¼ + ix/2) = Σ 4(c_j² − x²)/(c_j² + x²)² (since n + ¼ + ix/2 = (c_n + ix)/2):
Σ_j c_j²/(c_j² + x²)² = ½[Σ 1/(c² + x²) + Σ (c² − x²)/(c² + x²)²] = Im ψ/(4x) + Re ψ′/8. At x = 0, Im ψ(¼ + ix/2)/(4x) → ψ′(¼)/8. ∎

**Arb.** H(x) = acb(0.25, x/2).digamma().real − arb.pi().log(); Re ψ′ = acb(0.25, x/2).polygamma(1).real; ψ′(¼) =
acb(0.25).polygamma(1).real. Truncated sums plus arb(0, δ_J/c_J²) (P7).

**L = 2 (mp, dps 30).** A_00^+ = 0.01757046527259817001305, A_00^− = 0.05743040559929145907946: both agree with the SPEC §2.2
references in every printed digit. Independent eq. (P) quadrature for (q, r) ∈ {(0,0), (1,1), (2,2), (0,1), (1,2), (3,7)}: §10.

### P7. Response truncation (rh60 (3.7))

**Statement.** For J ≥ 0 and x real: |x²Σ_{j≥J} η_j/(c_j² + x²)| ≤ Σ_{j≥J} η_j = δ_J := e^{−2c_J L}/(1 − e^{−4L});
Σ_{j≥J} c_j²η_j/(c_j² + x²)² ≤ Σ_{j≥J} η_j/c_j² ≤ δ_J/c_J².

**Proof.** x²/(c² + x²) ≤ 1, c²/(c² + x²)² ≤ 1/c², c_j ≥ c_J, and η_{j+1}/η_j = e^{−4L}. ∎

**Arb.** δ = (−2c_J L).exp()/(1 − (−4L).exp()); add arb(0, ub(δ)). J = ⌈prec·ln 2/(4L)⌉ + 2 only sets sharpness.

**L = 2.** prec 192 → J = 19, δ_J = 2^−222.2; prec 1600 → J = 141, 2^−1630; prec 3392 → J = 296, 2^−3419.

### P8. Response-sum norm (rh60 (2.7); used only in P3(b))

**Statement.** ‖Σ_j r_j ⊗ r_j‖ ≤ (4/(1 − e^{−L}))(L + π/2) on L²(0, L), both sectors.

**Proof.** |r_j(x)| ≤ 2e^{−c_j(L−x)}/√(1 − η_j) and η_j ≤ η_0 = e^{−L}, so the kernel satisfies
|Σ_j r_j(x)r_j(y)| ≤ (4/(1 − e^{−L}))Σ_j e^{−c_j s}, s = 2L − x − y. The terms decrease in j, so
Σ_j e^{−c_j s} ≤ e^{−s/2} + ∫_0^∞ e^{−(2j+½)s} dj ≤ 1 + 1/(2s). With σ = L − x, τ = L − y ∈ (0, L): the constant kernel has norm L, and
1/(2(σ + τ)) has norm ≤ π/2 (Hilbert's inequality, Carleman kernel on (0, ∞)). A kernel dominated in absolute value by a nonnegative
kernel has norm at most that kernel's norm. ∎

**Arb.** 4/(1 − (−L).exp())*(L + arb.pi()/2), upper endpoint.

**L = 2.** 16.518756 (< 17, agreeing with rh_60's stated bound).

---

## 3. The prime norm

### P9. −B_p^ε ⪯ s(L) for every L, from our stage S (replaces rh60 (6.1) and its float endpoint lookups)

**Statement.** Let b = Lwin(L) = ⌈2^24 L⌉/2^24 ≥ L, and let s be the dyadic returned by `lb/liu/stage_s.py L` (prime list
{n : log n < 2b}). Then ⟨−B_p^ε v, v⟩ ≤ s‖v‖² for every v ∈ L²(0, L) and both ε. Hence for every closed subspace V spanned by
basis vectors (for example the far block q ≥ N), the compression satisfies −P_V B_p^ε P_V ⪯ s.

**Proof.** (i) *Schur test.* C_b = Σ_{log n<2b} w_n(τ_{y_n} + τ_{−y_n}) compressed to L²(−b, b) is a symmetric positivity-preserving
operator. If φ > 0 and C_bφ ≤ sφ pointwise, then ‖C_b‖ ≤ s: write ⟨C_b|f|, |g|⟩ as an integral against the symmetric measure
kernel and apply Cauchy–Schwarz with weights φ(x)/φ(y) and φ(y)/φ(x); each factor is ≤ s‖·‖². Stage S applies this with a cell-wise
weight and Arb maxima on cells (Elston's `schur_upper`, audited in Liu AUDIT §1b). So sup spec C_b ≤ ‖C_b‖ ≤ s.
(ii) *Compression.* For f ∈ L²(−L, L), extended by 0 to (−b, b): a prime power with 2L ≤ log n < 2b shifts the support of f outside
(−L, L), so ⟨C_b f, f⟩ = ⟨C_L f, f⟩ ≤ s‖f‖². With f = 𝒰_ε v (unitary) and B_p^ε = −𝒰_ε*C_L𝒰_ε, the claim follows; restricting
the quadratic form to V cannot raise its supremum. ∎

**Arb.** Read s from `s_<L>.json` as an exact Fraction and use arb(num)/den. Guard (F3, from the Liu audit): s must exceed the
float Ritz value below. If it does not, the run is void. The Liu audit (§2) showed that an unsound s is invisible to the negative
controls, because it only makes certificates stronger.

**L = 2.** s(2) is not yet run (P2 of the pilot). The float Ritz value of the comb on L²(−2, 2) (trig basis, P4 entries) is
7.97429 (K = 800) and 7.97445 (K = 1600) in the even sector, and 4.548 → 5.161 (not converged) in the odd sector. Ritz values are
lower bounds on sup spec C_2, so s(2) ≥ 7.9744. rh_60's ρ = 8.920292 is ≈ 0.95 above it. Earlier pins have exceeded the Ritz
value by ≈ 0.008, so s(2) ≈ 7.98 is plausible (a diagnostic only; it sets no parameter). Trivial bound: 2Σw_n = 24.383.

---

## 4. Core and post-core

### P10. Core positivity by integer Cholesky, and certified solves (C2–C3; rh60 (4.1)–(4.3))

**Statement (Lemma IC).** Let M be a symmetric K×K ball matrix. Let M̂ be its midpoint rounded to the 2^−2P grid, with the rounding
added to the radii ρ_ij. Let μ″ ∈ 2^−2Pℤ and R̂ ∈ ℤ^{K×K} arbitrary (a proposal), and compute exactly
Res = 2^{2P}(M̂ − μ″I) − R̂ᵀR̂ ∈ ℤ^{K×K}. Then every symmetric matrix in the ball M satisfies
λ_min ≥ m_core := μ″ − 2^{−2P}‖Res‖_∞ − max_i Σ_j ρ_ij.

**Proof.** M − μ″I = 2^{−2P}R̂ᵀR̂ + 2^{−2P}Res + Δ with |Δ_ij| ≤ ρ_ij. Here R̂ᵀR̂ ⪰ 0. For a symmetric matrix the spectral norm is at
most the max row sum, so ‖Res‖_2 ≤ ‖Res‖_∞ and ‖Δ‖_2 ≤ max_i Σ_j ρ_ij (≤ K·r_max, SPEC's form). ∎

**Solve enclosure.** If m_core > 0, x_0 is any proposal and r ⊇ Mx_0 − f is computed in Arb, then
‖M⁻¹f − x_0‖_2 ≤ ‖r‖_2/m_core, because x − x_0 = −M⁻¹(Mx_0 − f) and ‖M⁻¹‖ ≤ 1/m_core. Put the bound on every coordinate.

**Arb.** Elston's `cholesky_blocked` + `exact_residual` (MIT, audited) implement exactly Lemma IC. The same lemma is the dense
cross-check in G3 and the test for any dense block ≤ 6000.

**L = 2.** Pilot output (rh_60 reports 3.3055e−283 even, 5.7369e−278 odd at μ = 0, unchecked).

### P11. Post-core displacement, with μ-shift and deflation (rh60 (5.1)–(5.3))

**Statement.** Let C = (A_iq)_{i<K≤q} be the core–tail coupling, M = M_0 − μI + ϑφφᵀ ≻ 0, a = M⁻¹u_c, b = M⁻¹v_c, e = M⁻¹φ,
ê = M⁻¹Λ_cφ. Put U = u_t − Cᵀa, V = v_t − Cᵀb, Y = Cᵀê, X = Cᵀe, S = (A − μI)_tt − CᵀM⁻¹C. Then
  Λ_t S − SΛ_t = UVᵀ − VUᵀ + ϑ(YXᵀ − XYᵀ),
and (Cᵀy)_q = u_q R_{v,y}(λ_q) − v_q R_{u,y}(λ_q), so that 𝒢_q = (U_q, V_q, Y_q, X_q) = 𝒯(λ_q)g_q with SPEC T1's rows.

**Proof.** By P5, Λ_cM − MΛ_c = u_cv_cᵀ − v_cu_cᵀ + ϑ(Λ_cφφᵀ − φφᵀΛ_c) (−μI commutes with Λ), and
Λ_tCᵀ = CᵀΛ_c + u_tv_cᵀ − v_tu_cᵀ. Using Λ_cM⁻¹ − M⁻¹Λ_c = −M⁻¹(Λ_cM − MΛ_c)M⁻¹ and putting α = Cᵀa, β = Cᵀb:
Λ_tCᵀM⁻¹C − CᵀM⁻¹CΛ_t = −αβᵀ + βαᵀ − ϑ(YXᵀ − XYᵀ) + u_tβᵀ − v_tαᵀ + αv_tᵀ − βu_tᵀ.
Subtracting this from Λ_tA_tt − A_ttΛ_t = u_tv_tᵀ − v_tu_tᵀ and expanding (u_t − α)(v_t − β)ᵀ − (v_t − β)(u_t − α)ᵀ gives the claim.
The coupling formula is (Cᵀy)_q = Σ_i y_i(u_iv_q − v_iu_q)/(λ_i − λ_q). ∎

**Arb.** None (exact identity). Machine-check in fmpq (G3). **L = 2 (mp, dps 60, K = 6, 14 tail modes):** max error 3.6e−59
(even, ϑ = 4, random φ, μ = 10⁻³) and 1.9e−58 (odd).

### P12. The diagonal correction by virtual labels (rh60 (5.5), only spot-checked there)

**Statement.** For q ≥ K, S_qq = A_qq − μ − Q_q with Q_q = c_qᵀM⁻¹c_q = g_qᵀ 𝒯(λ_q)ᵀ J_ϑ 𝒯′(λ_q) g_q ≥ 0, where c_q is column q of C,
J_ϑ = diag(J, ϑJ), J = [[0, 1], [−1, 0]], and 𝒯′ is the entrywise derivative (R′_{x,y}(z) = −Σ x_iy_i/(z − λ_i)²).

**Proof.** For z ∉ {λ_i} and a generator g = (u, v), let c_g(z)_i = (u_iv − v_iu)/(λ_i − z). The computation of P11 is entrywise and
uses only this form of the columns, so it holds for a two-row virtual tail with labels z ≠ w and the same g in both rows. Then the
tail term u_tv_tᵀ − v_tu_tᵀ has (z, w) entry gᵀJg = 0, and (z − w)c_g(z)ᵀM⁻¹c_g(w) = −(𝒯(z)g)ᵀJ_ϑ(𝒯(w)g). Since J_ϑ is skew,
(𝒯(z)g)ᵀJ_ϑ(𝒯(z)g) = 0, so c_g(z)ᵀM⁻¹c_g(w) = gᵀ𝒯(z)ᵀJ_ϑ[𝒯(w) − 𝒯(z)]g/(w − z). Both sides are continuous in w ∉ {λ_i}; let w → z,
then put z = λ_q (> max λ_i) and g = g_q. Q_q ≥ 0 because M ≻ 0. ∎

**Arb.** 𝒯 and 𝒯′ at λ_q from the Toeplitz/Hankel sums of P13 at prec_T; Q_q as a ball. G5: a direct Arb solve at 32 indices.

**L = 2 (mp, dps 60, same toy).** max |S_qq − (A_qq − μ − Q_q)| = 9.3e−61 (even, deflated), 2.1e−59 (odd).

### P13. Partial fractions (rh60 (5.6), (7.2))

**Statement.** With λ = k², k_q = q + ω: 1/(λ_q − λ_i) = (1/(2k_q))[1/(q − i) + 1/(q + i + 2ω)] and
1/(λ_q − λ_i)² = (1/(4k_q²))[1/(q − i)² + 1/(q + i + 2ω)² + (1/k_q)(1/(q − i) + 1/(q + i + 2ω))]. Also
1/((λ_i − λ_q)(λ_j − λ_q)) = [1/(λ_i − λ_q) − 1/(λ_j − λ_q)]/(λ_j − λ_i).

**Proof.** λ_q − λ_i = (q − i)(q + i + 2ω) and (q − i) + (q + i + 2ω) = 2k_q; square the first identity. The last is direct. ∎

**Check.** Exact Fractions, ω ∈ {0, ½}, 5 ≤ q < 40, i < 5: 0 failures.

---

## 5. The far block q ≥ N

### P14. Moment bounds (rh60 (6.2)–(6.3))

**Statement.** Let f(z) = Σ_{i<K} x_iy_i/(z − λ_i), ℓ_* ≥ max λ_i (ℓ_* = (K − 1 + ω)²), θ_i = λ_i/ℓ_* ∈ [0, 1] (θ⁰ = 1),
m_r = Σ x_iy_iθ_i^r, A_f = Σ|x_iy_i|, z_0 > ℓ_*, t_0 = ℓ_*/z_0. For every real z ≥ z_0:
  |z f(z)| ≤ F0 := Σ_{r<R}|m_r|t_0^r + A_f t_0^R/(1 − t_0),
  |z² f′(z)| ≤ F1 := Σ_{r<R}(r + 1)|m_r|t_0^r + A_f t_0^R(R + 1 − Rt_0)/(1 − t_0)².

**Proof.** With t = ℓ_*/z ≤ t_0: zf(z) = Σ_i x_iy_i/(1 − θ_it) = Σ_r m_r t^r and z²f′(z) = −Σ_r (r + 1)m_r t^r, both absolutely
convergent. Bound |m_r| ≤ A_f for r ≥ R and use Σ_{r≥R}(r+1)t^r = d/dt[t^{R+1}/(1 − t)] = t^R(R + 1 − Rt)/(1 − t)². Each term is
increasing in t, so t = t_0 is the worst case. ∎

**Arb.** m_r from the balls x_i, y_i at prec_T, summed before any absolute value; |m_r| → ub(abs(m_r)). R is raised until
ub(A_f t_0^R) ≤ 2^−64 ub(F0). **Check:** 20 random rational instances × 3 values of z: max ratio 0.9999 ≤ 1.

### P15. Diagonal-correction constants (rh60 (6.4))

**Statement.** Write the (balanced) rows of 𝒯 as 𝒯_ρa(z) = δ_ρa + (±R_{x,y}(z)), ρ = 1..m, a ∈ {1, 2}, with skew matrix J_b
(J_ϑ, or plain J after the pair scaling of SPEC T5, in which case δ_U1 = 2^τ, δ_V2 = 2^−τ). Let F0_ρa, F1_ρa be the P14 constants of
the R in entry (ρ, a), computed with z_0 ≤ k_N². Define
  L_ab := Σ_{ρ,σ} (|δ_ρa| + F0_ρa/z_0)·|(J_b)_ρσ|·F1_σb  (a, b ∈ {1, 2}).
Then for q ≥ N: Q_q ≤ [L_11 u_q² + (L_12 + L_21)|u_q| + L_22]/k_q⁴. (SPEC's 2·L12 means L_12 + L_21.)

**Proof.** Q_q = Σ_{a,b} g_a X_ab(λ_q) g_b with X = 𝒯ᵀJ_b𝒯′, g = (u_q, 1). By P14, |𝒯_ρa(z)| ≤ |δ_ρa| + F0_ρa/z_0 and
|𝒯′_σb(z)| ≤ F1_σb/z² for z ≥ z_0, so |X_ab(z)| ≤ L_ab/z². Use z = λ_q = k_q². ∎

**Arb.** Sums of upper endpoints. **L = 2:** pilot output (needs the core solves).

### P16. Phase decomposition r̄(L) (rh60 (6.5), "monotone integral comparison" there)

**Statement.** For q ≥ 1 write u_q = k_q h_q + r_q with h_q = ½ + (2/π)S(κ_q). Then for q ≥ K,
  |r_q| ≤ r̄(L) := (2L/π²)[1 + e^{−L}/(1 − e^{−4L}) + |α_ε|/(¼ + κ_K²)].

**Proof.** γ_q = 1, and (2L/π²)κ_qS(κ_q) = (2k_q/π)S(κ_q), so r_q = (2L/π²)F_ε(κ_q) − k_q/2 = (2L/π²)[F_ε(κ) − πκ/4].
f(j) = x²/(c_j² + x²) decreases in j, so ∫_0^∞ f ≤ G(x) ≤ f(0) + ∫_0^∞ f with ∫_0^∞ f = (x/2)(π/2 − arctan(1/(2x))) (substitute
s = 2j + ½). Since 0 ≤ (x/2)arctan(1/(2x)) ≤ ¼ and 0 ≤ f(0) < 1: G(x) − πx/4 ∈ [−¼, 1). Next,
|x²Σ_j η_j/(c_j² + x²)| ≤ Σ_j η_j = e^{−L}/(1 − e^{−4L}) and |α_ε|/(¼ + κ_q²) ≤ |α_ε|/(¼ + κ_K²). ∎

**Arb.** Closed form, upper endpoint. **Control:** the Arb max of |r_q| over K ≤ q < M must not exceed r̄.

**L = 2, K = 512.** r̄ = 0.4601533 (ev), 0.4601540 (od). rh_60 states 0.461. Control (mp, q ∈ [512, 4096) step 7): max |r_q| =
0.0465 (ev) and 0.156 (od). The bound is about 3× loose in the odd sector and about 10× in the even sector, which is harmless.

### P17. Oscillation constants V_h, E_h, J_2, J_4 (rh60 (6.6)–(6.7), Abel bounds unchecked there)

**Statement.** Let V = ½Σw_n², V_h = ¼ + (4/π²)V, E_1 = Σ_n w_n/|sin(φ_n/2)|,
E = Σ_{n≠m} w_nw_m/(2|sin((φ_n − φ_m)/2)|) + Σ_{n,m} w_nw_m/(2|sin((φ_n + φ_m)/2)|), E_h = (2/π)E_1 + (4/π²)E. Every denominator is
nonzero. For N ≥ 2:
  Σ_{q≥N} h_q²/k_q² ≤ J_2(N) := V_h/(k_N − 1) + E_h/k_N²,  Σ_{q≥N} k_q^{−4} ≤ J_4(N) := 1/(3(k_N − 1)³).

**Proof.** κ_qy_n = k_qφ_n. Expand S² with product-to-sum: S² = V + ½Σ_{n≠m}w_nw_m cos(k(φ_n − φ_m)) − ½Σ_{n,m}w_nw_m cos(k(φ_n + φ_m)),
so h_q² − V_h = (2/π)S(κ_q) + (4/π²)(S² − V) is a finite sum of terms c·trig(k_qθ). For θ ∉ 2πℤ,
|Σ_{q=N}^{s} e^{i(q+ω)θ}| = |1 − e^{i(s−N+1)θ}|/|1 − e^{iθ}| ≤ 1/|sin(θ/2)|, which bounds the partial sums of the cos and sin terms
alike. Hence |Σ_{q=N}^{s}(h_q² − V_h)| ≤ E_h for all s. Abel summation with a_q = 1/k_q² decreasing to 0:
|Σ_{q≥N} a_q b_q| ≤ a_N sup_s|Σ_{q=N}^s b_q| ≤ E_h/k_N². Also Σ_{q≥N} 1/k_q² ≤ ∫_{N−1}^∞ dt/(t + ω)² = 1/(k_N − 1), and likewise for
J_4. *Denominators:* 0 < y_n < 2L gives φ_n ∈ (0, 2π); distinct prime powers have distinct logarithms, so 0 < |φ_n − φ_m| < 2π;
and φ_n + φ_m = 2π would mean nm = e^{2L}, which is impossible because e^{2L} is transcendental for rational L ≠ 0
(Lindemann–Weierstrass). ∎

**Arb.** Every sin(·) as an Arb ball; assert lb(abs(sin)) > 0 (the balls must exclude 0); sum the 1/abs upper endpoints.

**L = 2.** V = 3.53655909404, V_h = 1.68331341372 (SPEC 1.6833134137…), E_1 = 51.95296587, E = 492.7069969,
E_h = 232.7609098 (rh_60: < 232.761). Smallest |sin((φ_n + φ_m)/2)| = 0.00576 (n·m = 5·11 = 55, close to e⁴ = 54.6). At
N = 131072: J_2 = 1.28563086e−5 (ev) / 1.28562595e−5 (od), J_4 = 1.4803e−16. Control (float): Σ_{[N,4N)} h²/k² = 9.6332e−6 (ev) and
9.6311e−6 (od), both ≤ J_2. The non-oscillating part over the same range is 9.6321e−6.

### P18. Trace bounds τ_core, τ_pole (rh60 (6.8)–(6.9))

**Statement.** For any z ∈ ℓ²(q ≥ N):
- zᵀ(CᵀM⁻¹C)_FF z ≤ τ_core‖z‖², with τ_core := L_11J_2 + (2r̄L_11 + L_12 + L_21)√(J_2J_4) + (r̄²L_11 + r̄(L_12 + L_21) + L_22)J_4.
- In the odd sector, ⟨p_−, Σ_{q≥N} z_qẽ_q⟩² ≤ τ_pole‖z‖², with τ_pole := (2L³/π⁴)cosh²(L/2)J_4(N).

**Proof.** zᵀ(CᵀM⁻¹C)z = ‖M^{−1/2}Σ_q z_qc_q‖² ≤ (Σ_q‖M^{−1/2}c_q‖|z_q|)² ≤ (Σ_{q≥N}Q_q)‖z‖² (Cauchy–Schwarz). By P15–P17
(|u_q| ≤ k_q|h_q| + r̄, then Minkowski and Cauchy–Schwarz in ℓ²(q ≥ N)): Σ u_q²/k_q⁴ ≤ (√J_2 + r̄√J_4)² and
Σ|u_q|/k_q⁴ ≤ √(J_2J_4) + r̄J_4. Collecting terms gives τ_core. Pole: ⟨p_−, ẽ_q⟩² = (2/L)cosh²(L/2)/(¼ + κ_q²)² ≤ (2/L)cosh²(L/2)(L/π)⁴k_q^{−4}. ∎

**Arb.** Upper endpoints throughout. **L = 2, N = 131072:** τ_pole = 5.79e−17. τ_core is a pilot output (rh_60 reports
τ_N < 0.2260 ev and 0.2227 od, unchecked).

### P19. Far bound S_FF ⪰ T (rh60 (6.10))

**Statement.** Let t_q = H(κ_q) − μ − s − τ_N, τ_N = τ_core + [ε = −1]τ_pole. Choose t′_N ≤ lb(t_N) dyadic with t′_N > 0, and for
q > N any dyadic t′_q with t′_N ≤ t′_q ≤ t_q (rule: t′_q := max(t′_N, ⌊lb(t_q)⌋_40) for N < q < M, and t′_q := t′_M for q ≥ M). Then
zᵀS_FF z ≥ Σ t′_q z_q² for every rapidly decreasing z, and t′_q ≥ t′_N > 0 for all q ≥ N.

**Proof.** S_FF = diag(H(κ_q)) − μ + (B_p)_FF + 𝓡_FF + εP_FF − (CᵀM⁻¹C)_FF as quadratic forms on such z (P3(b)). Here 𝓡_FF ⪰ 0 and
P_FF ⪰ 0 (dropped when ε = +1), (B_p)_FF ⪰ −s (P9), εP_FF ⪰ −τ_pole when ε = −1 (P18), and −(CᵀM⁻¹C)_FF ⪰ −τ_core (P18). H(κ_q) is
increasing in q (paper Lemma `lem:M`), so t_q ≥ t_N ≥ t′_N for q ≥ N, and t′_q ≤ t_q in every case. ∎

**Correction to SPEC §6.7 / (V3).** Positivity is needed for *every* t′_q (T⁻¹ appears in P22 and Theorem V). Taking
⌊lb(t_q)⌋ alone does not guarantee t′_q ≥ t′_N, because balls are not monotone; the max rule above does.

**L = 2, N = 131072.** H(κ_N) = 10.3972077 (ev), 10.3972115 (od). With rh_60's ρ and τ_N, t_N = 10.39721 − 8.920292 − 0.2260 = 1.2509
(rh_60: > 1.2499). If s(2) ≈ 7.98, t_N ≈ 2.19 at this N, so a smaller N would satisfy the SPEC §12 rule.

---

## 6. The intermediate block I_P = [K, N)

### P20. Structure of S_M (rh60 (7.1)–(7.4))

**Statement.** For i ∈ I_P and q ∈ [N, M) let S_iq = 𝒢_iᵀJ_b𝒢_q/(λ_i − λ_q) (P11), Z(i) = Σ_q 𝒢_q𝒢_qᵀ/(t′_q(λ_i − λ_q)),
Z2(i) = Σ_q 𝒢_q𝒢_qᵀ/(t′_q(λ_i − λ_q)²), w_i = J_bZ(i)J_bᵀ𝒢_i, h_i = (𝒢_i, w_i) and 𝒥 = [[J_b, −I_m], [I_m, 0]]. Then
S_M := S_PP − Σ_{q∈[N,M)} c_qc_qᵀ/t′_q has (S_M)_ij = h_iᵀ𝒥h_j/(λ_i − λ_j) for i ≠ j and (S_M)_ii = S_ii − 𝒢_iᵀJ_bZ2(i)J_bᵀ𝒢_i.

**Proof.** (𝒢_iᵀJ_b𝒢_q)(𝒢_jᵀJ_b𝒢_q) = 𝒢_iᵀJ_b𝒢_q𝒢_qᵀJ_bᵀ𝒢_j. Apply the last identity of P13 and sum over q:
Σ_q S_iqS_jq/t′_q = 𝒢_iᵀJ_b[Z(i) − Z(j)]J_bᵀ𝒢_j/(λ_j − λ_i). Since J_bZJ_bᵀ is symmetric, 𝒢_iᵀJ_bZ(i)J_bᵀ𝒢_j = w_iᵀ𝒢_j and
𝒢_iᵀJ_bZ(j)J_bᵀ𝒢_j = 𝒢_iᵀw_j. So (λ_i − λ_j)(S_M)_ij = 𝒢_iᵀJ_b𝒢_j + w_iᵀ𝒢_j − 𝒢_iᵀw_j = h_iᵀ𝒥h_j. The diagonal is the same with
squares. 𝒥 is skew. ∎

**L = 2 (mp toy, 6 + 8 tail modes, random t′).** max error 1.9e−61 off-diagonal and 1.2e−61 diagonal (ev, deflated); 9.0e−60 and
3.1e−61 (od).

### P21. Assembly error ε_asm and the Cauchy constant H (rh60 (7.5))

**Statement.** For i ≠ j in I_P, sup_i Σ_{j≠i} 1/|λ_i − λ_j| ≤ H := (1 + log n)/K, n = N − K. Let ĥ_i, d̂_i be the dyadic roundings of
SPEC §7.2, e_h ≥ max_i‖h_i − ĥ_i‖_∞ (radius plus rounding), e_d ≥ max_i|(S_M)_ii − d̂_i|, and |ĥ|_a = max_i|ĥ_ia|. Then
‖S_M − S_input‖ ≤ ε_asm := e_d + H·Σ_{a,b}|𝒥_ab|(e_h(|ĥ|_a + |ĥ|_b) + e_h²).

**Proof.** |λ_i − λ_j| = |i − j|(k_i + k_j) ≥ 2K|i − j|, and Σ_{j≠i}1/|i − j| ≤ 2(1 + log(n − 1)). The numerator difference is
|h_iᵀ𝒥h_j − ĥ_iᵀ𝒥ĥ_j| ≤ Σ_ab|𝒥_ab|(|h_ia − ĥ_ia||h_jb| + |ĥ_ia||h_jb − ĥ_jb|) with |h_jb| ≤ |ĥ|_b + e_h. A symmetric matrix has spectral
norm at most its max row sum. ∎

**L = 2.** H = 0.024960 at K = 512 and n = 130560 (SPEC: 0.0250).

### P22. Omitted tail r_M (rh60 (7.6)–(7.8), unchecked there)

**Statement.** Let R_M = Σ_{q≥M} c_qc_qᵀ/t′_q on ℝ^{I_P}, ϱ = k_{N−1}/k_M, S_a ≥ Σ_{i∈I_P}𝒢_ia²,
A_ρ = |δ_ρ1| + F0_ρ1/k_M², C_ρ = |δ_ρ2| + F0_ρ2/k_M² (F0 computed with z_0 ≤ k_M²), β_ρ = A_ρ√J_2(M) + (A_ρr̄ + C_ρ)√J_4(M). Then
0 ⪯ R_M and ‖R_M‖ ≤ r_M := [Σ_{a,b}|(J_b)_ab|√S_a β_b]²/(t′_M(1 − ϱ²)²).

**Proof.** ‖R_M‖ ≤ tr R_M ≤ (1/t′_M)Σ_{q≥M}‖c_q‖², because t′_q = t′_M. For q ≥ M and i < N, λ_q − λ_i ≥ k_q²(1 − ϱ²). Hence
|S_iq| ≤ Σ_ab|J_ab||𝒢_ia||𝒢_qb|/(k_q²(1 − ϱ²)), and the matrix (|S_iq|)_{i,q} is entrywise dominated by
(1 − ϱ²)^{−1}Σ_ab|J_ab|α_aβ̃_bᵀ, with α_a = (|𝒢_ia|)_i and β̃_b = (|𝒢_qb|/k_q²)_{q≥M}. The Frobenius norm of a sum of rank-one terms is
at most Σ‖α_a‖‖β̃_b‖, with ‖α_a‖ ≤ √S_a. Finally, |𝒢_qρ| ≤ A_ρ|u_q| + C_ρ ≤ A_ρk_q|h_q| + A_ρr̄ + C_ρ (P14, P16, v_q = 1), and
Minkowski with P17 gives ‖β̃_ρ‖ ≤ β_ρ. ∎

**Arb.** Upper endpoints. **Control:** the finite part over [M, 2M), computed by convolution, must be ≤ r_M. **L = 2:** pilot output
(rh_60 reports < 0.1440 ev and 0.1445 od, unchecked).

---

## 7. Rigorous positivity of S_input − δ_0 I (replaces rh60 (8.1)–(8.5): point LDL, hand lemma (8.4), IEEE assumptions)

### P23. Lemma SR (exact structured LDLᵀ with explicit residual; the spec's version is the special case (∗) below)

**Statement.** Input: distinct rationals λ_1..λ_n; rows h_j ∈ (2^−Pℤ)^D; a skew integer matrix 𝒥 (|𝒥|_1 = Σ|𝒥_ab|); diagonal
d_j ∈ 2^−Pℤ; Ŝ_jk = h_jᵀ𝒥h_k/(λ_j − λ_k) (j ≠ k), Ŝ_jj = d_j. For i = 1..n (the current h, d):
1. p_i := d_i; stop with FAIL unless p_i > 0 (exact).
2. For j > i: ν_j = h_jᵀ𝒥h_i (exact); pick **any** rational multiplier ℓ_j; put ĉ_j = p_iℓ_j, ν̂_j = ĉ_j(λ_j − λ_i);
   h′_j = h_j − ℓ_jh_i; h_j ← ⌊h′_j⌋_P (componentwise floor to 2^−Pℤ); d_j ← ⌊d_j − p_iℓ_j²⌋_P.
3. Record e_i = max_j|ν_j − ν̂_j|, ℓ̄_i = max_j|ℓ_j|, G′_i = max_j‖h′_j‖_∞, all exact.
Let H_S ≥ max_j Σ_{k≠j}1/|λ_j − λ_k| (for I_P, H_S = H of P21), ν̄_i = 2ℓ̄_ie_i + |𝒥|_1 2^−P(2G′_i + 2^−P),
and ε_E = Σ_i [2^−P + (e_i + ν̄_i)H_S]. If no step fails, then Ŝ ⪰ −ε_E I, that is λ_min(Ŝ) ≥ −ε_E.

(∗) SPEC's choice: ℓ_j = ⌊ν_j⌋_P/((λ_j − λ_i)p_i), so e_i < 2^−P. A float multiplier is also admissible: it makes the recursion
division-free (multiply and shift only), at the price of e_i ≈ 2^−53|ν|. Rigour never depends on how ℓ was chosen.

**Proof.** Let S^(i) be the Cauchy-like matrix on indices ≥ i with the current (h, d), ℓ^(i) = 1_i + Σ_{j>i}ℓ_j1_j (1_j the unit
vectors), and E_i := S^(i) − p_iℓ^(i)ℓ^(i)ᵀ − S^(i+1) (zero-extended). Telescoping gives Ŝ = Σ_i p_iℓ^(i)ℓ^(i)ᵀ + Σ_i E_i
exactly, and Σ p_iℓℓᵀ ⪰ 0. Entries of E_i, with c_j = ν_j/(λ_j − λ_i) the true column:
- (E_i)_ii = 0; (E_i)_ji = c_j − ĉ_j = (ν_j − ν̂_j)/(λ_j − λ_i);
- (E_i)_jj = (d_j − p_iℓ_j²) − ⌊d_j − p_iℓ_j²⌋_P ∈ [0, 2^−P);
- (E_i)_jk (j ≠ k > i) = ν^E_jk/(λ_j − λ_k), with ν^E_jk = ℓ_k(ν_j − ν̂_j) − ℓ_j(ν_k − ν̂_k) + (h′_jᵀ𝒥h′_k − ĥ_jᵀ𝒥ĥ_k).
The last entry follows from three facts. First, h_iᵀ𝒥h_i = 0 gives h′_jᵀ𝒥h′_k = h_jᵀ𝒥h_k − ℓ_kν_j + ℓ_jν_k. Second,
p_iℓ_jℓ_k(λ_j − λ_k) = ℓ_kν̂_j − ℓ_jν̂_k, because ν̂_j/ĉ_j − ν̂_k/ĉ_k = λ_j − λ_k. Third, S^(i+1)_jk = ĥ_jᵀ𝒥ĥ_k/(λ_j − λ_k).
*Bound.* ĥ = h′ − δ with δ ∈ [0, 2^−P)^D, so |h′_jᵀ𝒥h′_k − ĥ_jᵀ𝒥ĥ_k| = |δ_jᵀ𝒥h′_k + h′_jᵀ𝒥δ_k − δ_jᵀ𝒥δ_k| ≤ |𝒥|_1 2^−P(2G′_i + 2^−P);
hence |ν^E_jk| ≤ ν̄_i. Row sums of the symmetric E_i: row i ≤ e_iH_S; row j ≤ 2^−P + e_i/|λ_j − λ_i| + ν̄_iH_S ≤ 2^−P + (e_i + ν̄_i)H_S.
So ‖E_i‖ ≤ 2^−P + (e_i + ν̄_i)H_S and Ŝ ⪰ ΣE_i ⪰ −ε_E. ∎

**Use.** Run on Ŝ = S_input − δ_0I (that is, d_j = d̂_j − δ_0, exact). Then λ_min(S_input) ≥ δ_0 − ε_E, and with P21,
λ_min(S_M) ≥ δ_0 − ε_E − ε_asm.

**Implementation recipe.** Integers H_j = 2^P h_j (Python int / numpy object arrays), λ as 4λ ∈ ℤ, p and d scaled by 2^P. Cost
O(n²D) integer operations and O(nD) memory; no float enters any certified quantity. The float LDL of the same recursion is used
only to choose μ (SPEC §8).

**Size of ε_E** (estimate, not a bound). With (∗): ε_E ≈ n2^−P[1 + H(1 + 2ℓ̄ + 2|𝒥|_1G′)]. At P = 96, n = 1.3e5, H = 0.025,
|𝒥|_1 ≤ 12 and G′ ≤ 2^20 this is ≤ 1e−18, negligible against δ_0 ≈ 0.2. SPEC's "~1e−13" is conservative.

**Checks (exact Fractions, `proofs_spot.py sr`).** Random instances with D = 4 (m = 2, P = 12, n = 14) and D = 8 (m = 4, P = 16,
n = 12), 3 trials each, with both multiplier choices: Ŝ − Σp_iℓℓᵀ − ΣE_i = 0 exactly in all 12 runs, and ‖ΣE_i‖ (2e−3 … 8e−5) ≤
ε_E (3.6e−2 … 3.4e−3).

**Ball LDL.** SPEC §8's radius-growth model for a forward Arb recursion is a heuristic. It is neither proved nor needed: Lemma SR
replaces it, and Lemma IC (P10) covers dense blocks.

---

## 8. Theorem V (rh60 (9.1)–(9.2))

**Statement.** Under SPEC §3 (V1)–(V5), with t′_q as in P19: Q̄_L(f) + ϑ⟨Φ, f⟩² ≥ μ‖f‖² on 𝒟^ε. Hence λ_1^ε(L) ≥ μ (ϑ = 0) and
λ_2^ev(L) ≥ μ (ϑ > 0).

**Proof.** By P3(c) it suffices to show xᵀ(A − μ + ϑφφᵀ)x ≥ 0 for rapidly decreasing x = (x_c, y, z) (core, I_P, far). Every series
below converges absolutely: entries of A grow at most like log k, |S_iq| = O(1/k_q) by P22's bound, and t′_q ≥ t′_N > 0.
1. M ≻ 0 (V2), so xᵀ(·)x = ‖M^{1/2}(x_c + M⁻¹C(y, z))‖² + (y, z)ᵀS(y, z) ≥ (y, z)ᵀS(y, z).
2. (y, z)ᵀS(y, z) ≥ yᵀS_PPy + 2yᵀS_PFz + Σ t′_qz_q² (P19)
   = ‖T^{1/2}z + T^{−1/2}S_PFᵀy‖² + yᵀ(S_PP − S_PFT⁻¹S_PFᵀ)y ≥ yᵀ𝒮y, where 𝒮 = S_M − R_M (P20, P22).
3. 𝒮 ⪰ S_input − ε_asm − r_M ⪰ (δ_0 − ε_E − ε_asm − r_M)I ⪰ 0 (P21, P23, P22, V5).
For ϑ > 0: in every 2-dimensional V ⊂ 𝒟^ev there is f ≠ 0 with f ⊥ Φ, and for it Q̄(f)/‖f‖² = (Q̄(f) + ϑ⟨Φ, f⟩²)/‖f‖² ≥ μ. Min-max
gives λ_2^ev ≥ μ (paper Lemma `lem:deflation` lifted to the operator). ∎

---

## 9. Arb recipe summary (one place for the implementer)

| item | formula | rounding |
|---|---|---|
| u_q, A_qq, A_qr | P5, P6 with P7 balls | balls |
| s | P9: exact Fraction from stage S | exact |
| r̄, V_h, E_h, J_2, J_4, τ_pole | P16, P17, P18 | upper endpoints; sin balls must exclude 0 |
| F0, F1, L_ab | P14, P15 | upper |
| τ_core, t_q, t′_q | P18, P19 | t′_q dyadic ≤ lb(t_q), max rule |
| A_ρ, C_ρ, β_ρ, S_a, r_M | P22 | upper |
| H, ε_asm | P21 | upper |
| m_core | P10 (exact integer residual) | exact + upper |
| ε_E, pivots | P23 (exact integers) | exact |
| final | (V5): lb(δ_0 − ε_E − ε_asm − r_M) > 0 | certain comparison |

## 10. Spot values at L = 2 (`proofs_spot.py`, mpmath dps 30 unless stated; proposals, not certificates)

| quantity | value | reference |
|---|---|---|
| #𝒩_2, Σw_n, 2Σw_n | 24 (n ≤ 53), 12.19164592, 24.38329184 | — |
| A_00^+ | 0.01757046527259817001305 | SPEC 0.0175704652725981700130 |
| A_00^− | 0.05743040559929145907946 | SPEC 0.0574304055992914590 |
| eq. (P) vs P5/P6 (dps 15) | 12 entries, max diff 2.6e−14 (block below) | gate G0 |
| Green identity | ≤ 2.5e−29 | P1 |
| response norm | 16.518756 | rh_60 < 17 |
| δ_J | 2^−222 (J = 19), 2^−3419 (J = 296) | P7 |
| r̄ (K = 512) | 0.4601533 ev, 0.4601540 od; control max 0.0465 / 0.156 | rh_60 0.461 |
| V_h, E_1, E, E_h | 1.68331341372, 51.95296587, 492.7069969, 232.7609098 | rh_60 E_h < 232.761 |
| J_2, J_4 (N = 131072) | 1.28563e−5, 1.4803e−16 | control ≤ |
| τ_pole (N = 131072) | 5.79e−17 | — |
| H(κ_N) (N = 131072) | 10.3972077 ev, 10.3972115 od | t_N = 1.2509 with rh_60's ρ, τ |
| Ritz sup spec C_2 | ≥ 7.97445 (ev, K = 1600) | rh_60 ρ = 8.920292; s(2) pending |
| H (K = 512, n = 130560) | 0.024960 | SPEC 0.0250 |
| T2 / T3 / P20 toy (dps 60) | ≤ 1.9e−58 | exact in fmpq (G3) |
| Lemma SR toy | residual exactly 0; ‖ΣE‖ ≤ ε_E | P23 |

eq. (P) cross-check (nested quadrature of the paper's position-side formula versus the closed forms of P5/P6):

```
eps=+1 (0,0): eq.(P) 0.017570465272597  closed 0.017570465272595  diff 1.8e-15
eps=+1 (1,1): eq.(P) 0.035272527725048  closed 0.035272527725046  diff 1.6e-15
eps=+1 (2,2): eq.(P) 0.035678010336325  closed 0.035678010336323  diff 2.1e-15
eps=+1 (0,1): eq.(P) 0.024894814445063  closed 0.024894814445063  diff 5.6e-16
eps=+1 (1,2): eq.(P) 0.035473909331599  closed 0.0354739093316  diff -1.4e-15
eps=+1 (3,7): eq.(P) 0.040059979378947  closed 0.040059979378948  diff -9.2e-16
eps=-1 (0,0): eq.(P) 0.057430405599294  closed 0.057430405599292  diff 1.8e-15
eps=-1 (1,1): eq.(P) 0.058686628941222  closed 0.05868662894122  diff 2.4e-15
eps=-1 (2,2): eq.(P) 0.061467187947921  closed 0.061467187947919  diff 2.5e-15
eps=-1 (0,1): eq.(P) 0.058051668248512  closed 0.058051668248513  diff -1.8e-15
eps=-1 (1,2): eq.(P) 0.060045101728368  closed 0.060045101728369  diff -6.9e-16
eps=-1 (3,7): eq.(P) 0.11911597757036  closed 0.11911597757034  diff 2.6e-14
```
All 12 entries agree to ≤ 2.6e−14 (quadrature accuracy at dps 15). Off-diagonals are in the conjugated basis ẽ_q, so the signs
are checked as well. Run time ≈ 25 min on one laptop core.

## 11. Flags: what is not proved here, and corrections to SPEC

**Imported, not re-proved here** (each is cited, and each is either audited or part of the paper):
1. Stage S's cell-wise evaluation (Elston's `schur_upper`; Liu AUDIT §1b). P9 proves the Schur test and the compression step only.
   An unsound s is not caught by any control (Liu AUDIT §2), so the Ritz guard of P9 is mandatory.
2. Elston's `cholesky_blocked` / `exact_residual` implement Lemma IC (P10). The lemma is proved here; the code is audited.
3. Paper §2.3: closability and semiboundedness of Q_L on C_c^∞, compact resolvent and min-max. Also paper Lemma `lem:M`.
4. Arb/FLINT correctness, including acb digamma and polygamma.

**Not proved because they are heuristics, and not needed:** SPEC §8's ball-LDL growth model, the runtime estimates, ε_E ≈ 1e−13
(P23 gives a smaller estimate), and N ≈ 5e4 versus 1.3e5.

**Nothing in the certificate chain is left unproved** apart from items 1–4. Every SPEC formula checked here holds as stated, except
for these corrections and clarifications:
- (a) SPEC §6.7 / (V3): t′_q > 0 is required for every q ≥ N. Use t′_q := max(t′_N, ⌊lb(t_q)⌋_40) (P19).
- (b) SPEC §6.3: "2·L12" must be read as L_12 + L_21, with the explicit L_ab of P15. The diagonal-correction and r_M constants must
  use the δ entries *after* pair balancing (δ_U1 = 2^τ, δ_V2 = 2^−τ) (P15, P22).
- (c) SPEC §2.4: a factor 4/L is missing in the auxiliary inequality. P3(b) replaces that inequality by the P8 operator bound.
- (d) Lemma SR is correct as SPEC states it. P23 generalises it to arbitrary multipliers (bound via e_i), so a float multiplier is
  admissible and the recursion can be division-free.
- (e) P16's r̄ is loose (control 0.0465 ev / 0.156 od versus 0.460). This is harmless and needs no change.
- (f) E_h depends on the closest pair with nm ≈ e^{2L} (at L = 2: 5·11 = 55, |sin| = 0.00576). At other windows it can be much
  larger, but it enters only as E_h/k_N². The Arb balls must exclude 0 (P17).
- (g) Diagnostic: the Ritz value 7.9744 suggests that s(2) will be ≈ 1 below rh_60's ρ = 8.92. If so, N can be smaller than 131072
  by the SPEC §12 rule. This is a float observation and sets no parameter; N must come from the certified s(2) after the stamp.
