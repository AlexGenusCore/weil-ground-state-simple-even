# SPEC: value certificates λ_k(sector) ≥ μ by full-source Schur elimination (rh_60 architecture), general L, pilot L = 2

**Status.** Written 2026-10-31 from the rh_60 and rh_45 *manuscripts only* (no supplement code was opened for this spec), from
our paper `weil-public/paper/main.tex` and from our own code. Nothing has been run for this spec. No push, publish or contact.

**Credit (repeat in every document and code docstring).** The architecture is bramble_trace's: rh_60 v1, "Full-source Schur
certificates for Weil positivity at support radius two" (rStation, 2026-10-26): the summed digamma response family, the
displacement-rank-2 full matrix, exact core elimination through rational functions, the moment/Abel tail and the
Hilbert–Schmidt (HS) omitted-tail bound. The Green-response identity, the bases and the closed-form comparison argument are
lihongmin's: rh_45 v1, "Cutoff-free positivity of localized Weil forms through the (log 11)/2 threshold" (rStation,
2026-10-23). Both papers are **unrefereed AI-agent preprints that only AI agents have reviewed**, so every step here is
re-derived and every constant is checked by us. Also reused: Elston's MIT code (`gap/elston/`: `schur_upper` through our
`lb/liu/stage_s.py`, plus `cholesky_blocked` and `exact_residual`), our upper bounds U(L) (`highprec/fr_sweep.py`) and our step
test (`highprec/gap/check_steps.py`). **What is ours:** the general-L re-derivation, the μ-shift, the rank-one core deflation
(paper Lemma `lem:deflation`), the exact-arithmetic structured LDL (§8, which replaces rh_60's point LDL and its lemma (8.4)),
the form-core argument (§2.4) and the gluing.

**Clean room.** rh_60's code licence allows only execution and inspection for verification; rh_45 is all rights reserved.
The implementer works from this SPEC and our own code only. It must not open anything under
`weil-mechanism/scratch_archive/rstation/` (that includes our own study notes there, since they quote supplement code).
No rStation code may be copied, adapted or vendored. Equation numbers "rh60 (x.y)" below are for the auditor only.

**Rigor rules.**
- Every certified quantity comes from Arb balls (python-flint 0.9) with outward rounding, or from exact integers/rationals
  (fmpz, fmpq, Python int).
- Floats, point factorisations and midpoint eigenvectors are *proposals* only and carry no rigour.
- Nothing scored or parameter-setting runs before `PREREG.md` is stamped on vm4 (md5 + UTC).

---

## 1. Notation (ours; rh_60/rh_45 write a = L)

- **Window and form.**
  - L > 0 is the half-width, a decimal string held in Arb as a ball containing it exactly.
  - Q_L is paper eq. `(weil)`. It equals rh_60/rh_45 (2.1) term by term with a = L, factor 1 and shift 0.
  - A_L is the operator of the closure of Q_L on C_c^∞(−L, L) (paper §2.3), with sectors ε = +1 (ev) and ε = −1 (od).
  - λ_k^ε(L) are the eigenvalues, k ≥ 1.
- **Prime set.** 𝒩_L = {prime powers n : log n < 2L}, with w_n = Λ(n)/√n and y_n = log n.
  - Membership is decided in Arb, asserting |log n − 2L| > 2^−40.
  - For a decimal L, e^{2L} is transcendental, so no n sits on the boundary. At L = 2 the 24 prime powers are n ≤ 53.
- **Labels.** ω = 0 (ev) or ½ (od); k_q = q + ω; κ_q = π k_q / L; λ_q = k_q² (an exact quarter-integer).
  - γ_0 = 2^{−1/2} for even q = 0; γ_q = 1 otherwise.
  - The labels λ_q do not depend on L. L enters only through the source values.
- **Basis on (0, L).** e_q^+ = √(2/L) γ_q cos(κ_q x) and e_q^− = √(2/L) sin(κ_q x).
  - Conjugated basis: ẽ_q = (−1)^q e_q.
  - Parity map, unitary from L²(0, L) to the sector: (𝒰_ε v)(x) = v(|x|)/√2 for x > 0 and ε v(|x|)/√2 for x < 0.
  - All matrices below are in the basis 𝒰_ε ẽ_q.
- **Digamma functions.**
  - H(t) = Re ψ(¼ + it/2) − log π, the archimedean symbol; it is increasing in |t| (paper Lemma `lem:M`).
  - G(x) = (x/2) Im ψ(¼ + ix/2) = Σ_{j≥0} x²/(c_j² + x²), where c_j = 2j + ½.
- **Prime sums.** S(x) = Σ_{𝒩_L} w_n sin(x y_n) and C(x) = Σ_{𝒩_L} w_n (1 − y_n/(2L)) cos(x y_n).
- **Response and pole constants.**
  - Responses: η_j = e^{−2 c_j L}.
  - Pole: α_+ = sinh²(L/2), α_− = −cosh²(L/2); s_+ = sinh(L/2), s_− = cosh(L/2).
- **Closed forms.**
  - F_ε(x) = G(x) − ε x² Σ_j η_j/(c_j² + x²) − α_ε/(¼ + x²).  [rh60 (3.1) at L = 2]
  - Φ_ε(x) = x S(x) + F_ε(x).
  - R_ε(x) = Im ψ(¼ + ix/2)/(4x) + Re ψ′(¼ + ix/2)/8 − ε Σ_j c_j² η_j/(c_j² + x²)² + α_ε/(¼ + x²)².  [rh60 (3.6)]
  - R_+(0) = ψ′(¼)/4 − Σ_j η_j/c_j² + 16 α_+.
- **Skew forms.**
  - J = [[0, 1], [−1, 0]].
  - For deflation weight ϑ ≥ 0: J_ϑ = diag(J, ϑJ) (4×4), or J alone when ϑ = 0.
- **Index blocks.** Core [0, K), intermediate I_P = [K, N), finite far [N, M), far q ≥ N; n = N − K.

## 2. The form in this basis (Theorem B)

### 2.1 Green identity (rh_45 Lemma 3.1, re-proved)

For a smooth parity test f = 𝒰_ε v with f ∈ C_c^∞(−L, L), put x_q = ⟨v, ẽ_q⟩. Then

  Q_L(f) = Σ_q H(κ_q) x_q² + ⟨B_p^ε v, v⟩ + Σ_{j≥0} ⟨r_j, v⟩² + ε ⟨p_ε, v⟩²,

where:
- r_j(x) = e^{−c_j L}(e^{c_j x} + ε e^{−c_j x}) / √(1 − ε η_j)  [rh60 (2.4)];
- p_ε(x) = e^{x/2} + ε e^{−x/2};
- B_p^ε is the comb −Σ_{𝒩_L} w_n (τ_{y_n} + τ_{−y_n}) compressed to L²(−L, L) and restricted to the sector.
  On (0, L) these are rh60 (2.6)'s three terms (shift +y, shift −y, reflection y − x) with 4 replaced by 2L.

Proof, to be written out in DERIVATION.md:
1. **Digamma series.** h(t) − h(0) = Σ_j (2/c_j − 2c_j/(c_j² + t²)), from ψ(w) = −γ + Σ (1/(n+1) − 1/(n+w)) at w = ¼ + it/2.
2. **Fourier step.** (1/2π) ∫ 2c/(c² + t²) |f̂|² = ∬ e^{−c|x−y|} f(x) f(y). The parity reduction turns this into the kernel
   E_c^ε = e^{−c|x−y|} + ε e^{−c(x+y)} on (0, L)².
3. **Green kernel identity.** 2c R_c^ε − E_c^ε = r_c ⊗ r_c, where R_c^ε is the Green operator of −∂² + c² with Neumann/Neumann
   (ε = +) or Dirichlet/Neumann (ε = −) conditions. Its eigenbasis is ẽ_q, with eigenvalues 1/(c² + κ_q²).
   - Even case, x ≤ y: 2c R = 2 cosh(cx) cosh(c(L − y))/sinh(cL).
   - cosh(cL − cy) − e^{−cy} sinh(cL) = e^{−cL} cosh(cy), so 2cR − E = 2 cosh(cx) cosh(cy) e^{−cL}/sinh(cL) = r_c(x) r_c(y).
   - The odd case is the same with sinh(cx) and cosh(cL).
   - Machine-check both parities in Arb at 200 random (x, y, c, L).
4. **Assembly.** Summing over j gives H(κ_q) on the diagonal plus the positive rank-one forms. Use monotone convergence of the
   partial sums. The prime term is −2 Σ w_n Re C_f(y_n) = ⟨B_p^ε v, v⟩, and the pole term is
   2F(i/2)F(−i/2) = ε⟨p_ε, v⟩² (paper §2.1).

### 2.2 Matrix entries (general L)

With the full-window functions φ_q = 𝒰_ε e_q (that is γ_q cos(κ_q x)/√L, or sin(κ_q x)/√L) and the translation
integral I_qr(y) = ⟨τ_y φ_q, φ_r⟩ + ⟨τ_{−y} φ_q, φ_r⟩ multiplied by L/(γ_q γ_r):

- I_qr(y) = (−1)^{q+r} · 2[κ_r sin(κ_r y) − κ_q sin(κ_q y)]/(κ_q² − κ_r²) for q ≠ r, in both sectors.
- I_qq(y) = (2L − y) cos(κ_q y) − sin(κ_q y)/κ_q for κ_q > 0.
- I_00(y) = 2(2L − y).
- Prime entries: ⟨B_p φ_r, φ_q⟩ = −(γ_q γ_r/L) Σ_{𝒩_L} w_n I_qr(y_n). The factor (−1)^{q+r} drops out in the basis ẽ_q.
- ⟨r_j, ẽ_q⟩ = √(2/L) γ_q c_j √(1 − ε η_j)/(c_j² + κ_q²).  [rh60 (3.2)]
- ⟨p_ε, ẽ_q⟩ = √(2/L) γ_q s_ε/(¼ + κ_q²).

**Generators.** Write u_q = γ_q (2L/π²) Φ_ε(κ_q) and v_q = γ_q.  [rh60 (3.3): 2k s_k/π + (4/π²)F at L = 2]

Using divided differences (c²/((c² + x²)(c² + y²)) = DD[x²/(c² + x²)], and ε s_ε² = α_ε) and κ_q² − κ_r² = (π/L)²(λ_q − λ_r):

  A_qr = (u_q v_r − v_q u_r)/(λ_q − λ_r)  for q ≠ r,  that is,  ΛA − AΛ = u vᵀ − v uᵀ.  [rh60 (3.4)]

**Exact diagonal.**

  A_qq = H(κ_q) − 2C(κ_q) + [κ_q > 0] · S(κ_q)/(L κ_q) + (2/L) γ_q² R_ε(κ_q).  [rh60 (3.5) at L = 2]

At even q = 0 this reads H(0) − 2C(0) + R_+(0)/L. The prime term carries no γ_0², because I_00 is doubled.

**Truncation.** Sum Σ_j up to J − 1 and add the error balls:
- δ_J = e^{−2 c_J L}/(1 − e^{−4L}) for F and for Σ η_j/c_j²-type sums;
- δ_J/c_J² for R.  [rh60 (3.7)]
- Take J ≥ ⌈prec · ln 2/(4L)⌉ + 2.

**References (gate G0).** At L = 2, using our eq.-(P) script:
- A_00^+ = 0.0175704652725981700130…
- A_00^− = 0.0574304055992914590…

### 2.3 Bounded parts

- The response sum is bounded: ‖Σ_j r_j ⊗ r_j‖ ≤ (4/(1 − e^{−L}))(L + π/2).  [rh60 (2.7): 16.52 < 17 at L = 2]
  - Kernel: ≤ 4 e^{−c_j(2L − x − y)}/(1 − e^{−L}), and Σ_j e^{−c_j s} ≤ 1 + 1/(2s).
  - Constant kernel on (0, L): norm L.
  - Carleman kernel 1/(s + t): norm ≤ π (Hilbert).
- The prime operator satisfies −B_p^ε ⪯ s(L) (§6.1). The pole term is rank one.

### 2.4 Form core (replaces rh60 §2's H^s cutoff and density argument)

For f ∈ C_c^∞(−L, L) of parity ε, the coefficients x_q decay faster than any power:
- For even f, all odd derivatives vanish at 0, and v ≡ 0 near L.
- For odd f, all even derivatives vanish at 0.

So Q_L(f) = Σ_{q,r} A_qr x_q x_r with absolute convergence. Indeed |A_qr| ≤ C(1 + log k_q) δ_qr + O(1), and the response,
prime and pole parts are bounded operators (PROOFS P3(b), via the P8 norm bound). [R3(c): the earlier auxiliary inequality
Σ_j (Σ_q |⟨r_j, ẽ_q⟩| |x_q|)² ≤ Σ_j c_j^{−2} (Σ|x_q|)² lacked a factor 4/L and is no longer used.]

A_L is *defined* as the closure on this core. A form inequality Q_L + ϑ|⟨Φ, ·⟩|² ≥ μ‖·‖² proved on the core therefore holds on
the closure: the rank-one term is L²-continuous. **No domain identification is needed.** The same closure argument appears in
rh_45 §4 (4.6)–(4.8).

## 3. Theorem V (the value certificate)

**Setting.** Fix L, ε, K, N, M, μ ≥ 0, ϑ ≥ 0 (ϑ > 0 only when ε = +1) and a dyadic φ ∈ ℚ^K. Put Φ = 𝒰_ε Σ_{q<K} φ_q ẽ_q.

**Hypotheses.**
- (V1) s ≥ sup spec C_L, where C_L is the comb on L²(−b, b) with dyadic b ≥ L (§6.1).
- (V2) M := M_0 − μI + ϑφφᵀ ≻ 0, where M_0 is the K×K core block of A (§4).
- (V3) t′_N > 0 (§6).
- (V4) The exact structured LDL of §8 completes with every pivot > 0 on S_input − δ_0 I.
- (V5) δ_0 − ε_E − ε_asm − r_M > 0.

**Conclusion.**
- Q_L(f) + ϑ⟨Φ, f⟩² ≥ μ‖f‖² for every f in the form domain of the sector.
- Hence λ_1^ε(L) ≥ μ when ϑ = 0.
- And λ_2^ev(L) ≥ μ when ϑ > 0, by min-max: λ_2 ≥ inf_{f ⊥ Φ} Q/‖f‖² = inf_{f ⊥ Φ} (Q + ϑ⟨Φ, f⟩²)/‖f‖² ≥ μ.
  This is paper Lemma `lem:deflation` lifted to the operator.

**Proof** on core vectors x = (x_c, y, z), with x_c ∈ core, y ∈ I_P, z ∈ far:
1. **First square completion** (rh60 (9.2)):
   x(A − μ + ϑφφᵀ)x = ⟨M(x_c + M⁻¹C_core(y, z)), ·⟩ + (y, z)S(y, z) ≥ (y, z)S(y, z),
   where S = (A − μ)_tail − C_coreᵀ M⁻¹ C_core and C_core = P_0 A (I − P_0).
2. **Far block lower bound.** S_far ⪰ T = diag(t′_q) by §6.
3. **Second square completion** (rh60 (9.1)):
   (y, z)S(y, z) ≥ yS_PP y + 2yCz + zTz = ‖T^{1/2}z + T^{−1/2}Cᵀy‖² + y𝒮y, with 𝒮 = S_PP − C T⁻¹ Cᵀ.
4. **Finite remainder.** 𝒮 = S_M − R_M, with R_M ⪰ 0 and ‖R_M‖ ≤ r_M (§7). Then
   S_M ⪰ S_input − ε_asm ⪰ (δ_0 − ε_E − ε_asm) I (§8). Hence 𝒮 ⪰ 0.
5. **Convergence.** Every series converges absolutely on core vectors: entries grow at most polynomially, T⁻¹ is bounded and
   the core has finite rank.

## 4. Stage C: the core (rh60 §4, plus shift and deflation)

**C1. Assembly.** Assemble M_0 (q, r < K) from §2.2 at prec_core with J_core response terms, then
M = M_0 − μI + ϑφφᵀ. Here μ, ϑ and φ are exact dyadics.

**C2. Positivity of M.** Use Elston's `cholesky_blocked` + `exact_residual` (MIT, audited in the Liu audit).
1. Proposal: Cholesky of mid(M) − μ′I at prec_core, with μ′ a dyadic ≈ ½·λ̂_min(M).
2. Exact integer residual at scale 2^{P_core}.
3. This gives m_core := μ″ − ρ_res − K·r_max(M) ≤ λ_min(M). Require m_core > 0. Then ‖M⁻¹‖ ≤ 1/m_core.

rh60 (4.1)–(4.2) uses a dyadic congruence T_0 M T_0ᵀ − I with η < 1 instead. That method is also admissible.

**C3. Certified solves.** Solve for a = M⁻¹u_c, b = M⁻¹v_c and, when ϑ > 0, e = M⁻¹φ and ê = M⁻¹(Λ_c φ).
- Proposal: x_0.
- Arb residual: r = M x_0 − f.
- Enclosure: ‖x − x_0‖₂ ≤ ‖r‖₂/m_core, applied to every coordinate.  [rh60 (4.3)]
- `arb_mat.solve` (rigorous) is also admissible.

**C4. Proposals for deflation runs** (no rigour):
- φ is the lowest eigenvector of mid(M_0), from inverse iteration at prec_core, rounded to 128-significant-bit dyadics.
- ϑ = 4^t, the even power of 2 nearest 2·λ̂_2(M_0), so that √ϑ = 2^t is exact.

## 5. Stage T: exact transfer, post-core generators, source build (rh60 §5)

**T1. Rational sums.**
- R_{x,y}(z) = Σ_{i<K} x_i y_i/(z − λ_i), for x ∈ {u, v} and y ∈ {a, b, e, ê}.
- The transfer matrix 𝒯(z) has m = 2 rows (ϑ = 0) or m = 4 rows (ϑ > 0), acting on g_q = (u_q, v_q)ᵀ:

  | row | 𝒯(z) row |
  |---|---|
  | U | (1 − R_{v,a}, R_{u,a}) |
  | V | (−R_{v,b}, 1 + R_{u,b}) |
  | Y | (R_{v,ê}, −R_{u,ê}) |
  | X | (R_{v,e}, −R_{u,e}) |

  Here 𝒢_q := 𝒯(λ_q) g_q, with U = u − C_coreᵀa, V = v − C_coreᵀb, Y = C_coreᵀê and X = C_coreᵀe.
  The identity (C_coreᵀ y)_q = u_q R_{v,y}(λ_q) − v_q R_{u,y}(λ_q) follows from §2.2.

**T2. Post-core displacement lemma.** With Λ_c M − M Λ_c = u_c v_cᵀ − v_c u_cᵀ + ϑ(Λ_c φ φᵀ − φ (Λ_c φ)ᵀ) and
Λ_t C_coreᵀ − C_coreᵀ Λ_c = u_t v_cᵀ − v_t u_cᵀ:

  (λ_q − λ_r) S_qr = 𝒢_qᵀ J_ϑ 𝒢_r   (q ≠ r, q, r ≥ K),  that is,  Λ_t S − S Λ_t = UVᵀ − VUᵀ + ϑ(YXᵀ − XYᵀ).

Proof: expand Λ_t C_coreᵀ M⁻¹ C_core − C_coreᵀ M⁻¹ C_core Λ_t, using
Λ_c M⁻¹ − M⁻¹ Λ_c = −M⁻¹(Λ_c M − M Λ_c)M⁻¹, then collect terms. Write it out in DERIVATION.md.
- With ϑ = 0 this is rh60 (5.3).
- The core displacement rank goes from 2 to 4 under deflation, and the post-core rank from 2 to 4.
- The μ-shift changes nothing here, because −μI commutes with Λ.

**T3. Diagonal** (rh60 (5.5), unchecked there; spot-checked on 12 modes):

  S_qq = A_qq − μ − Q_q,  Q_q = g_qᵀ 𝒯(λ_q)ᵀ J_ϑ 𝒯′(λ_q) g_q ≥ 0.

Proof:
1. T2's derivation is entrywise and holds verbatim for *virtual* tail rows with arbitrary distinct labels z, w ∉ {λ_i} and
   arbitrary generator rows.
2. Take two virtual rows with the same g. Then c_g(z)ᵀ M⁻¹ c_g(w) = gᵀ𝒯(z)ᵀ J_ϑ [𝒯(w) − 𝒯(z)] g/(w − z), where c_g(z) is the
   coupling column. This uses gᵀJg = 0 and the skew symmetry of J_ϑ.
3. Let w → z. The left side is continuous, and at z = λ_q, g = g_q it equals Q_q.

**T4. Evaluation for K ≤ q < M by convolution** (rh60 (5.6)).
- Partial fractions: 1/(λ_q − λ_i) = (1/(2k_q))[1/(q − i) + 1/(q + i + 2ω)].
- Squared: 1/(λ_q − λ_i)² = (1/(4k_q²))[1/(q − i)² + 1/(q + i + 2ω)² + (1/k_q)(1/(q − i) + 1/(q + i + 2ω))].
- So R(λ_q) and R′(λ_q) = −Σ x_i y_i/(λ_q − λ_i)² are Toeplitz (offset q − i) and Hankel (offset q + i + 2ω) sums.
  Compute them as `arb_poly` products at prec_T. The coefficients are huge and cancel (about 4e147 at L = 2).
- Then round the balls to prec_src.
- Verify every partial-fraction identity in exact fmpq on random small instances.

**T5. Source lists for K ≤ q < M**, all as balls:
- u_q, A_qq, 𝒢_q (m components) and S_qq;
- t′_q for q ≥ N (§6);
- S_a := Σ_{q∈I_P} 𝒢_{qa}² for each component a.

**Pair balancing.** For each skew pair, replace (x, y) by (2^τ x, 2^{−τ} y) (exact), with τ chosen so that the max-norms agree within a
factor 2. For the deflation pair use (2^t Y, 2^t X) with plain J. All later stages see balanced generators.

## 6. Stage F: the far block q ≥ N (rh60 §6)

**6.1 Prime norm.** Replaces rh60 (6.1), which relies on a 4-step graph with float endpoint lookups.
- s(L) is our stage S (`lb/liu/stage_s.py`): Elston's Collatz–Wielandt Schur test `schur_upper`, which is Arb and exact
  dyadic throughout (Liu AUDIT §1b). Run on the window b = Lwin(L) ≥ L, with 𝒩_L the active list.
- Since B_p^ε is −C_L restricted to the sector and compression is monotone, −B_p^ε ⪯ s on each sector and on every far
  compression.
- Known values: s(1.75) = 5.948, s(1.6) = 4.908, s(1.5) = 4.302 and s(1.19) = 2.678. At L = 2, rh60 has ρ = 8.920292;
  s(2) is to be run.

**6.2 Moment bounds** (rh60 (6.2)–(6.3)). Applies to every f = R_{x,y}, with ℓ_* = (K − 1 + ω)² ≥ max λ_i,
θ_i = λ_i/ℓ_*, z_0 > ℓ_* and t_0 = ℓ_*/z_0.
- Moments: m_r = Σ_i x_i y_i θ_i^r for r < R (computed at prec_T before any absolute values are taken).
- Absolute sum: A_f = Σ |x_i y_i|.
- For all z ≥ z_0: |z f(z)| ≤ F0 := Σ_r |m_r| t_0^r + A_f t_0^R/(1 − t_0).
- And: |z² f′(z)| ≤ F1 := Σ_r (r + 1)|m_r| t_0^r + A_f t_0^R (R + 1 − R t_0)/(1 − t_0)².
- Rule for R: increase R until A_f t_0^R ≤ 2^−64 · F0.

**6.3 Diagonal-correction constants** (rh60 (6.4)).
- X(z) = 𝒯(z)ᵀ J_ϑ 𝒯′(z) (2×2).
- From |𝒯_ρa| ≤ |δ_ρa| + F0/z_0 and |𝒯′_ρb| ≤ F1/z² (δ = identity part of the row):
  |X_ab| ≤ L_ab/z² with L_ab := Σ_{ρ,σ} (|δ_ρa| + F0_ρa/z_0)·|(J_b)_ρσ|·F1_σb (PROOFS P15), for z ≥ z_0 = k_N². [R3(b)]
- Then Q_q ≤ (L_11 u_q² + (L_12 + L_21)|u_q| + L_22)/k_q⁴ for q ≥ N, using v_q = 1. The δ entries are those *after* pair
  balancing (δ_U1 = 2^τ, δ_V2 = 2^−τ, and 2^t on the deflation rows). [R3(b)]

**6.4 Phase decomposition** (rh60 (6.5), unchecked there).
- u_q = k_q h_q + r_q, with h_q = ½ + (2/π) S(κ_q).
- r̄(L) := (2L/π²)[1 + e^{−L}/(1 − e^{−4L}) + |α_ε|/(¼ + κ_K²)] bounds |r_q| for q ≥ K. At L = 2 this is about 0.4602 (rh60: 0.461).
- Proof: the terms f(j) = x²/(c_j² + x²) decrease in j, so ∫_0^∞ f ≤ Σ_j f(j) ≤ f(0) + ∫_0^∞ f, where
  ∫_0^∞ f = (x/2)(π/2 − arctan(1/(2x))). Since 0 ≤ (x/2) arctan(1/(2x)) ≤ ¼, G(x) − πx/4 ∈ [−¼, 1].
  The response correction is bounded by Σ η_j = e^{−L}/(1 − e^{−4L}); the pole term by |α|/(¼ + κ²).
- Control (not proof): the Arb max of |r_q| over K ≤ q < M must be ≤ r̄.

**6.5 Oscillation constants** (rh60 (6.6)–(6.7), unchecked there). With φ_n = π y_n/L:
- V = ½ Σ w_n² and V_h = ¼ + (4/π²) V.
- E_1 = Σ w_n/|sin(φ_n/2)|.
- E = Σ_{n≠m} w_n w_m/(2|sin((φ_n − φ_m)/2)|) + Σ_{n,m} w_n w_m/(2|sin((φ_n + φ_m)/2)|).
- E_h = (2/π) E_1 + (4/π²) E.

Proof:
- h² − V_h = (2/π) S + (4/π²)(S² − V). Expand S² with product-to-sum formulas.
- For θ ∉ 2πℤ, |Σ_{q=r}^{s} cos or sin((q + ω)θ)| ≤ 1/|sin(θ/2)|.
- The denominators are nonzero: 0 < y_n < 2L, and log(nm) = 2L is impossible for decimal L. They can still be small, so
  compute them in Arb.
- Abel summation and integral comparison give, with k_N = N + ω:
  - J_2(N) := V_h/(k_N − 1) + E_h/k_N² ≥ Σ_{q≥N} h_q²/k_q²;
  - J_4(N) := 1/(3(k_N − 1)³) ≥ Σ_{q≥N} k_q^{−4}.
- Control: compare with the partial sums over [N, 4N) in Arb.

**6.6 Trace of the core covariance on the far block** (rh60 (6.8)). This sum is ≥ the operator norm, by positive
semidefiniteness:

  Σ_{q≥N} Q_q ≤ L_11 J_2 + (2r̄ L_11 + L_12 + L_21)√(J_2 J_4) + (r̄² L_11 + r̄(L_12 + L_21) + L_22) J_4 =: τ_core(N).  [R3(b)]

**Odd pole** (rh60 (6.9)): Σ_{q≥N} ⟨p_−, ẽ_q⟩² ≤ (2L³/π⁴) cosh²(L/2) J_4(N) =: τ_pole(N).

**6.7 Far bound** (rh60 (6.10)).
- S_far ⪰ T = diag(t′_q), with t_q = H(κ_q) − μ − s − τ_N and τ_N = τ_core(N) + [ε = −1] τ_pole(N).
  The positive responses and the even pole are dropped.
- t′_N := ⌊lb(t_N)⌋_40 (the 2^−40 grid). For N < q < M, t′_q := max(t′_N, ⌊lb(t_q)⌋_40); t′_M := max(t′_N, ⌊lb(t_M)⌋_40) and
  t′_q := t′_M for every q ≥ M. Then t′_N ≤ t′_q ≤ t_q and t′_q > 0 for every q ≥ N (balls are not monotone, so the max is
  needed; PROOFS P19). [R3(a)]
- H is increasing (Lemma `lem:M`), so t_q ≥ t_N for q ≥ N.
- Require t′_N > 0. N rule: §12 (R4).
- This is span_of_dilates' "Lemma A" limit: k_N ≳ 2L·e^{s + τ + t}. With s(2) ≈ 8, N ≈ 5e4; with ρ = 8.92, N ≈ 1.3e5.

## 7. Stage I: the intermediate Schur matrix and the HS tail (rh60 §7)

**7.1 Assembly** (rh60 (7.1)–(7.4)).
- For i ∈ I_P, the far coupling is S_iq = 𝒢_iᵀ J_ϑ 𝒢_q/(λ_i − λ_q).
- For each component pair (β, δ) of the m-vectors, define:
  - Z_βδ(i) = Σ_{q∈[N,M)} 𝒢_qβ 𝒢_qδ/(t′_q (λ_i − λ_q));
  - Z2_βδ(i) = Σ_{q∈[N,M)} 𝒢_qβ 𝒢_qδ/(t′_q (λ_i − λ_q)²).
  - There are m(m+1)/2 lists: 3 for ϑ = 0, 10 for ϑ > 0.
  - Toeplitz/Hankel convolutions, by the partial fractions of T4 with k_i in place of k_q, in Arb at prec_src.
- Put w_i = J_ϑ Z(i) J_ϑᵀ 𝒢_i, h_i = (𝒢_i, w_i) ∈ ℝ^{2m} and 𝒥 = [[J_ϑ, −I_m], [I_m, 0]] (skew). Then:
  - (S_M)_ij = h_iᵀ 𝒥 h_j/(λ_i − λ_j) for i ≠ j;
  - (S_M)_ii = S_ii − 𝒢_iᵀ J_ϑ Z2(i) J_ϑᵀ 𝒢_i.
- Displacement rank: 4 (ϑ = 0; rh60 (7.4)) or 8 (deflated).
- Derivation: partial fractions, 1/((λ_i − λ_q)(λ_j − λ_q)) = [1/(λ_i − λ_q) − 1/(λ_j − λ_q)]/(λ_j − λ_i).
  Check it in exact fmpq on random instances.

**7.2 Assembly error** (rh60 (7.5)).
- S_input is defined exactly by:
  - ĥ_i = mid(h_i) rounded to 2^−P;
  - d̂_i = mid((S_M)_ii) rounded to 2^−P.
- With e_h = max_i ‖h_i − ĥ_i‖_∞ (radius + rounding) and e_d the corresponding bound on the diagonal:
  ε_asm = e_d + H·max_{i≠j} |h_iᵀ𝒥h_j − ĥ_iᵀ𝒥ĥ_j| ≤ e_d + H·Σ_{a,b} |𝒥_ab| (e_h(|ĥ|_a + |ĥ|_b) + e_h²).
- H := (1 + log n)/K ≥ sup_i Σ_{j≠i} 1/|λ_i − λ_j|, since |λ_i − λ_j| ≥ 2K|i − j|.
- Proof: Schur test on a Cauchy-like matrix.

**7.3 Omitted tail q ≥ M** (rh60 (7.6)–(7.8), unchecked there).
- ‖R_M‖ ≤ Σ_{q≥M} ‖c_q‖²/t′_M.
- For the coupling: λ_q − λ_i ≥ k_q²(1 − ϱ²), with ϱ = k_{N−1}/k_M.
- For the generators (Minkowski twice): |𝒢_qρ| ≤ A_ρ k_q |h_q| + A_ρ r̄ + C_ρ, where:
  - A_ρ = |δ_ρ1| + F0[𝒯_ρ1; k_M²]/k_M²;
  - C_ρ = |δ_ρ2| + F0[𝒯_ρ2; k_M²]/k_M²;
  - and v_q = 1.
- Put β_ρ = A_ρ √J_2(M) + (A_ρ r̄ + C_ρ) √J_4(M) ≥ (Σ_{q≥M} 𝒢_qρ²/k_q⁴)^{1/2}. Then

  r_M := [Σ_{a,b} |(J_ϑ)_ab| √S_a β_b]² / (t′_M (1 − ϱ²)²) ≥ ‖R_M‖.

- Control: the finite part over q ∈ [M, 2M), computed by convolution, must be ≤ its share of the bound.

## 8. Stage P: rigorous positivity of S_input − δ_0 I

This replaces rh60 §8: a 64-bit point LDL plus a hand backward-error lemma (8.4) that also assumes IEEE arithmetic and
compiler flags.

**Lemma SR (exact structured LDL with explicit residual).** Our statement and proof; it is the exact-arithmetic analogue of
rh60 (8.3)–(8.5).

**Input.**
- Distinct labels λ_1, …, λ_n.
- Dyadic rows h_j ∈ ℚ^{2m}, a fixed skew 𝒥 and dyadic diagonal d_j.
- Ŝ_jk = h_jᵀ𝒥h_k/(λ_j − λ_k) for j ≠ k, and Ŝ_jj = d_j.
- ⌊·⌋_P is the floor onto the 2^−P grid.

**Recursion.** For i = 1, …, n:
1. p_i := d_i. Require p_i > 0, by exact comparison.
2. For each j > i, in exact integer arithmetic:
   - ν_j = h_jᵀ𝒥h_i;
   - ν̂_j = ⌊ν_j⌋_P;
   - ĉ_j = ν̂_j/(λ_j − λ_i), kept as an exact rational;
   - h′_j = h_j − (ĉ_j/p_i) h_i, then h_j ← ⌊h′_j⌋_P componentwise;
   - d_j ← ⌊d_j − ĉ_j²/p_i⌋_P.
3. Track exactly C_i = max_j |ĉ_j| and G′_i = max_j ‖h′_j‖_∞.

**Claim.** Ŝ = L̂ diag(p) L̂ᵀ + Σ_i E_i, with L̂_ji = ĉ_j/p_i. Each E_i is supported on rows and columns ≥ i, and:
- (E_i)_ji = (ν_j − ν̂_j)/(λ_j − λ_i);
- (E_i)_jj ∈ [0, 2^−P);
- (E_i)_jk = ν^E_jk/(λ_j − λ_k) for j ≠ k > i, where
  ν^E_jk = [ĉ_k(ν_j − ν̂_j) − ĉ_j(ν_k − ν̂_k)]/p_i + (h′_jᵀ𝒥h′_k − h_jᵀ𝒥h_k).

**Proof.**
- The exact Schur update with ĉ has numerator (λ_j − λ_k)Ŝ_jk − [ĉ_k ν_j − ĉ_j ν_k]/p_i, because h_iᵀ𝒥h_i = 0.
- Also (λ_j − λ_k) ĉ_j ĉ_k = ĉ_k ν̂_j − ĉ_j ν̂_k.
- Zero-extend each E_i and induct on i.

**Bound** (PROOFS P23, which supersedes the earlier form here). With e_i = max_j|ν_j − ν̂_j|, ℓ̄_i = max_j|ℓ_j| (ℓ_j = ĉ_j/p_i),
G′_i ≥ max_j‖h′_j‖_∞ and ν̄_i = 2ℓ̄_i e_i + |𝒥|_1 2^−P(2G′_i + 2^−P), the row-sum test gives

  ‖E_i‖ ≤ 2^−P + (e_i + ν̄_i) H_S,  and  ε_E := Σ_i (that bound), accumulated exactly.

- [R6] Multipliers are P-bit dyadics: ℓ_j = ⌊2^P ν_j/((λ_j − λ_i) p_i)⌋·2^−P (one exact integer floor division). Require the
  computed ε_E ≤ 2^−12.
- [R15] H_S is a rational ≥ the Arb upper end of (1 + log n)/K, so ε_E accumulates exactly.

**Conclusion.** If every p_i > 0, then λ_min(S_input) ≥ δ_0 − ε_E.

**Cost.** O(n² m) big-integer operations and O(n m) memory. Reference implementation in Python ints (used by G3); the
production kernel is C/GMP (`code/sr.c`), whose output must be identical to the Python reference on the G3 instances [R5].
- Proposals (floats) are allowed only to choose μ: a float64 version of the same recursion gives p̂_min(μ).
- At P = 96, n = 1.3e5 and H ≈ 0.025, ε_E is about 1e-13 (float estimate). rh60 (8.5) reports 2.3e-5 for its point LDL.

**Machine checks of Lemma SR (gate G3).**
- On random instances with n ≤ 64, compute Ŝ − L̂DL̂ᵀ − ΣE_i in exact fmpq; it must be exactly 0.
- Check the norm bound against the exact ‖ΣE_i‖.
- Cross-check: on the leading 2048×2048 block at L = 2, Lemma SR and Elston's dense `cholesky_blocked` + `exact_residual`
  must both certify ⪰ δ_0 − (their errors).

**Why not ball LDL.** A forward Arb recursion compounds radii. The relative radius obeys roughly
r_j = 1 + Σ_{i<j} c·r_i/(j − i), with c ≈ |entry|/p ~ 0.2–2, which grows exponentially in n (a float model, not measured).
Use Arb ball Cholesky only for dense blocks with n ≤ 6000.

## 9. Shift and deflation choices

- **Odd λ_1** (ϑ = 0, ε = −1) and **even λ_1** (ϑ = 0, ε = +1):
  - μ is the only change: d_k → d_k − μ in the core and on the diagonals (S_qq and t_q).
  - Displacement is unchanged.
  - Proposal model: the Schur margin falls like (λ_1 − μ)/(λ_core − μ). At K = 512, λ_core/λ_1 ≈ 1.8 (float model).
- **Even λ_2** (ϑ > 0):
  - φ and ϑ as in C4.
  - λ_min(M) ≥ λ_min(M_0); the core stays positive whenever μ < λ_min(M_0 + ϑφφᵀ), which is checked in C2.
  - At L = 2, λ_2^ev ≈ 3.05e-273 (Galerkin K = 1024, float) versus U^ev(2) = 1.8468e-283. Deflation is the easy part.
- **Loss.** ℓ_odd := U^od(L)/μ_pass ≥ λ_1^od/μ_pass is an upper bound on the true loss.

## 10. Constants, with source equation and L-dependence

| constant | formula (ours) | rh_60 eq. (a = 2) | L = 2 value / note |
|---|---|---|---|
| c_j | 2j + ½ | (2.3) | — |
| response norm | (4/(1 − e^{−L}))(L + π/2) | (2.7) | 16.52 (< 17) |
| α_± | sinh²(L/2), −cosh²(L/2) | (3.1) | sinh²1, −cosh²1 |
| ⟨r_j, ẽ_q⟩ | √(2/L) γ c √(1 − εη_j)/(c² + κ²) | (3.2) | — |
| pole coefficient | √(2/L) γ s_ε/(¼ + κ²) | after (3.2) | sinh 1, cosh 1 |
| u_q, v_q, λ_q | γ(2L/π²)Φ_ε(κ_q), γ, k² | (3.3) | (2k/π)S + (4/π²)F |
| A_qq | §2.2 | (3.5), (3.6) | gate G0 |
| δ_J | e^{−2c_J L}/(1 − e^{−4L}) | (3.7) | e^{−4c_J}/(1 − e^{−8}) |
| core | m_core (C2) | (4.1), (4.2) | rh60: 3.3055e-283 ev, 5.7369e-278 od (μ = 0) |
| 𝒯, Q_q | §5 | (5.1)–(5.5) | — |
| partial fractions | T4 | (5.6), (7.2) | — |
| s | stage S | ρ (6.1) | ρ = 8.920292 |
| ℓ_*, R | (K − 1 + ω)², rule | (6.2), (6.3) | R = 96 |
| L11, L12, L22 | 6.3 | (6.4) | — |
| r̄ | (2L/π²)[1 + e^{−L}/(1 − e^{−4L}) + abs(α)/(¼ + κ_K²)] | (6.5) | 0.4602 (0.461) |
| V_h, E_h | 6.5, φ_n = πy_n/L | (6.6) | 1.6833134137…, < 232.761 |
| J_2, J_4 | 6.5 | (6.7) | — |
| τ_core, τ_pole | 6.6 | (6.8), (6.9) | < 0.2260 ev, < 0.2227 od at N = 131072 |
| t_q | H(κ_q) − μ − s − τ_N | (6.10) | rh60: t_N > 1.2499 |
| H | (1 + log n)/K | H_* (7.5) | 0.0250 |
| a_M, b_M, v_M → A_ρ, C_ρ, β_ρ | 7.3 | (7.6) | — |
| r_M | 7.3 | (7.7), (7.8) | < 0.1440 ev, < 0.1445 od |
| ε_E | Lemma SR | (8.4), (8.5) | rh60 2.3e-5 → ours ~1e-13 (float estimate) |
| δ_0 | rule, §12 | 0.20 (8.6) | — |

## 11. Steps rh_60 did not machine-check, and our replacement

| rh_60 step | gap | our treatment | check |
|---|---|---|---|
| §2, (2.5)–(2.7): form domain, H^s cutoff | hand argument | §2.4: inequality on C_c^∞, inherited by the closure; no domain identification; Green identity re-proved (§2.1) | Arb kernel check; G0 against eq. (P) |
| (3.4)–(3.6) at a = 2 only | hard-coded | general-L derivation, §2.2 | G0 at each L |
| (5.5) diagonal limit | spot-checked on 12 modes | proof by virtual labels (T3), including deflation | exact fmpq identity (G3); Arb direct c_qᵀM⁻¹c_q at 32 indices (G5) |
| (6.1) prime norm | float endpoint lookups | stage S (Elston Schur test, exact Arb; Liu-audited) | F3-type guard: s ≥ λ_max(−mid B_p core) |
| (6.5) abs(r_q) < 0.461 | "monotone integral comparison" | proof in 6.4; r̄(L) | Arb max over [K, M) |
| (6.6), (6.7) V_h, E_h, J_2, J_4 | Abel bounds | proof in 6.5 | partial sums over [N, 4N) |
| (6.2)–(6.4), (6.8) | arithmetic only | 6.2, 6.3, 6.6 | fmpq on small K |
| (7.5) assembly error | — | 7.2, Schur test | — |
| (7.7) HS tail | unchecked | 7.3, generalised to m pairs | finite part over [M, 2M) |
| (8.1)–(8.5) point LDL + lemma (8.4) | float, hand lemma, IEEE and compiler assumptions | Lemma SR, exact integers, no floats | G3; dense cross-check |
| (9.1), (9.2) | — | Theorem V proof | — |
| end-to-end | no rerun except by the author | full rerun at μ = 0 (G1) | — |

## 12. What PREREG.md must fix

**Proposed pilot defaults** (L = 2, both sectors):
- K = 512.
- prec_core = 64⌈(3b + 512)/64⌉, with b = log2(1/U^ev(L)). This gives 3392 at L = 2.
- P_core = 1536.
- prec_T = 64⌈(1.5b + 128)/64⌉, giving 1600.
- prec_src = 192.
- J by the §2.2 rule.
- R by the 6.2 rule (start at 96).
- **N** [R4]: the smallest multiple of 1024 with N ≥ 4K and lb(t_N) ≥ t_min, using the run's own τ_N(N) (a scalar once the
  core solves are done). t_min = 1 when ϑ = 0 and ½ when ϑ > 0. If the projected Lemma SR time c_D·(N − K)²/2 (P0 benchmark)
  exceeds 10 h, use t_min = ½ [R5].
- M = 4N; M = 8N when r_M > ¼ [R14].
- P = 96.
- δ_0 = the smallest multiple of 2^−8 that is ≥ r_M + ε_asm + 2^−10.
- **Stage S:** K_cells = 16000, iters = 1500.
- **U(2):** rerun fr_sweep with the shipped code, K = 1024, prec 6000, par 0 and 1. The old even value predates the ρ^{−2n+2} fix
  (paper Rem. `rem:rho`).
- **μ ladders** (descending; the float structured LDL picks the first value with p̂_min ≥ 2^−6; at most 2 rigorous retries
  per kind):
  - odd: μ ∈ {⅔, ½, ⅓, ¼, ⅛, 1/10}·U^od(2) [R12: the 1/10 rung decides the loss > 10 kill];
  - even λ_1: not run [R11] (neither the L = 2 verdict nor grid G uses a lower bound on λ_1^ev);
  - even λ_2: μ ∈ {2^−2, 2^−10}·λ̂_2, then 2^4·U^ev(2).
- φ and ϑ by C4. Labels follow the Liu PREREG pattern (certified / pilot / float).

## 13. Gates and controls (Liu pattern)

- **G0 (one form, two codes).** At each L, compare A_qq for q ∈ {0, 1, 2, K−1, K, 2K} and A_qr for
  (q, r) ∈ {(0,1), (1,2), (3,7), (K−1, K)} in each sector. These must overlap with eq. (P) evaluated in Arb on 𝒰_ε ẽ_q and
  𝒰_ε(ẽ_q + ẽ_r). Also reproduce the two §2.2 reference values.
- **G1 (independent reproduction).** At μ = 0 and ϑ = 0, both sectors at L = 2 must PASS before any shifted run counts.
  This is the first independent check of rh_60 Thm 1.1 per sector.
- **G2 (negative controls, N1).** The following must FAIL:
  - even, ϑ = 0, at μ = 1.01·U^ev(2);
  - odd at μ = 1.01·U^od(2).
  In both cases the core stays positive, so the Schur stage is what is tested. Any PASS is a bug: stop and void everything.
  Also run them at L = 1.5.
- **G3 (identities).** Exact fmpq checks on small random instances of:
  - displacement and T2 (both ϑ);
  - the T3 diagonal;
  - the T4 and 7.1 partial fractions;
  - Lemma SR (exact zero residual and the bound).
- **G4 (mutations, at L = 1.5, cheap).** Each mutation must be caught by G0, G2, G3, G5 or a failed run:
  - drop the odd pole (α_− → 0);
  - γ_0 → 1;
  - omit Q_q;
  - s → s/2;
  - drop r_M;
  - flip the sign of the deflation pair;
  - omit τ_N;
  - use M_0 instead of M_0 − μ;
  - perturb one generator by 2^−20 (relative), at a seeded random index of the stage-T output (caught by G5′).
- **G5 (spot checks).** Q_q via a direct Arb solve at 32 indices. Ten S_input entries against a direct dense evaluation.
- **G5′ (second path, every run) [R8].** Every 𝒢_q and S_qq, q ∈ [K, M), from the convolution path must overlap a second
  path: direct sums for q < 2K and the P14 moment series for q ≥ 2K.
- **C-τ (every run) [R7].** ub(Σ_{q∈[N,M)} Q_q) ≤ τ_core(N); in the odd sector also ub(Σ_{[N,M)} ⟨p_−, ẽ_q⟩²) ≤ τ_pole(N).
- **G-S [R9].** s(L) > max(trig Ritz at K = 1600 in both parities, stage S `mu_top_float`); otherwise every run at that L is
  void. It catches gross errors only; s remains imported trust (Liu audit §2).
- **C-r̄, C-J_2, C-r_M (every run).** max_{[K,M)} |r_q| ≤ r̄; Σ_{[N,4N)} h_q²/k_q² ≤ J_2(N); the convolved part over [M, 2M)
  ≤ r_M.
- **Controls at L = 1.19 and L = 1.5.** Cheap: N = 4K, with an intermediate block of 3K.
  - Every certified lower bound must be ≤ U(L). Known: U(1.19) = 8.712e-48; λ_1^od(1.19) ≥ 3.9196e-44 (Elston);
    λ_2^ev(1.19) ≥ 1.2336e-40 (ours).
  - Report how these compare with the Piece III values. The comparison is diagnostic only.
- **G6 (independent audit).** A fresh agent audits the trusted code and DERIVATION.md before any claim.

## 14. Gluing plan

- **Outputs** (schema of `gap/check_steps.py`): `g_<L>_odd.json`, `g_<L>_ev.json` and `g_<L>_l2.json`.
  - Field `certified_lower_bound` = the enclosing ball `arb(μ).lower().str(20)` ("[m +/- r]"), never a rounded midpoint [R2].
  - Field `Ldec` = the exact decimal string of L; every certified path uses `arb(Ldec)`, never `float(L)`; check_steps matches
    files by this exact string [R13]. Stage S may use b = Lwin(L) ≥ L (PROOFS P9(ii)).
  - Also: L, ε, μ, ϑ, K, N, M, R, precisions, m_core, τ_N, t′_N, r_M, ε_asm, ε_E, δ_0, min p_i, the s(L) file with its
    sha256, the PREREG md5, the code sha256, seconds and peak_gb.
  - `upper*.jsonl` holds U(L_i) (field lam0_upper, par 0) from fr_sweep.
- **check_steps.py change** (the only change):
  - Read the grid from a CLI argument (comma list or file) instead of the hard-coded list.
  - A single-point grid applies paper Cor. `cor:criterion` pointwise: U(L) < min(ℓ_2, ℓ^od)(L), compared in Arb
    (ub U < lb of each lower bound) [R1].
  - A PASS requires at least one comparison; a missing input is a FAIL [R1].
  - The pilot gluing directory holds only the rerun U(2) file and the `g_2_odd.json`, `g_2_l2.json` files, because
    check_steps takes the minimum over every `upper*.jsonl` row in its directory [R10].
- **Pilot verdict.** λ_1^ev(2) ≤ U(2) < min(ℓ_2(2), ℓ^od(2)) means a simple, even ground state at L = 2.
  - This is pointwise only.
  - Priority note: a forum value (rh_60 follow-up, unreviewed) already orders the sectors at L = 2.
- **Grid G (later; separate PREREG).**
  - Windows L_0 = 1.4035 (or the last complete Piece III point) < L_1 < … < 2.
  - At each L_{i+1}, ℓ^od and ℓ_2 come from this certifier, or from Elston's (Piece III) where available; any valid lower
    bound may be used (take the max).
  - U(L_i) from fr_sweep (K = 640 or more).
  - Paper Cor. `cor:step` through check_steps.py on the union grid, with min-max monotonicity (Lemma `lem:mono`) across steps.
  - G0 at every window.
  - Window count (float estimate in our route assessment): 41–49 at ℓ ≈ 2.

## 15. Pilot plan on vm4, budget, kill criteria

**Machine.** ssh user@vm4, venv `~/weil/.venv`, working directory `~/rh60route/{code,data,out,logs}`.
- At most 4 cores and 16 GB. Use nice -n 5 and setsid nohup, and kill explicit PIDs only.
- Mirror the results to `highprec/lb/rh60route/`.

**Steps.**
- **P0** (before the stamp): code, plus G3 on small instances only.
- **P1:** write PREREG.md and stamp it.
- **P2:** s(2); U^ev(2) and U^od(2) (about 1 h each); G0.
- **P3:** G1 (2 runs).
- **P4:** G2 (2 runs).
- **P5:** odd ladder (≤ 3 runs) and even λ_2 (≤ 3). Even λ_1 is not run [R11].
- **P6:** controls at 1.19 and 1.5, and G4.
- **P7:** check_steps.py, then RESULTS.md, NOTES.md and IDEAS.md.
- **P8:** G6.

**Budget** (float estimates, unmeasured):
- Per L = 2 run:
  - core 5–15 min;
  - solves and transfer: minutes;
  - assembly 5–15 min;
  - Lemma SR 0.5–3 h on one core (n ≤ 1.3e5, about 1e10–3e11 integer operations);
  - at most about 3 GB.
- About 12 runs at L = 2 is 15–40 core-h, so 4–10 h wall on 4 cores (4 runs in parallel).

**Kill criteria.**
- G0 fails: fix the derivation and do not run.
- G1 fails after the fallbacks (N to 131072, M = 8N, K = 1024): route not reproduced; stop and report.
- Any G2 PASS: void and stop.
- ℓ_odd > 3: the pilot verdict still counts if it holds, but grid G needs a larger K or is not viable.
- Lemma SR over 6 h per run: record it and decide in an amendment. The registered kill criteria are those of PREREG.md §6.

## 16. Review fixes applied (2026-10-31, before the PREREG stamp)

The fixes R1–R16 of `review.md` are applied above, marked [R#]; the log with the exact old and new text is `spec_changes.md`.
Where this SPEC and PROOFS.md differ, PROOFS.md (P1–P23) holds; where either differs from PREREG.md on a registered
parameter, PREREG.md holds.
- R1, R10: `gap/check_steps.py` takes the grid from the command line, has a pointwise branch, needs at least one comparison
  for a PASS and counts missing inputs as FAIL (§14).
- R2, R13: output strings and the exact window string (§14).
- R3: PROOFS corrections (a) t′_q max rule (§6.7), (b) L_12 + L_21 with δ after balancing (§6.3, §6.6), (c) §2.4 constant.
- R4, R14: N rule and M fallback (§12). R5: P0 Lemma SR benchmark on vm4 and a C/GMP kernel (§8).
- R6, R15: P-bit dyadic multipliers, ε_E ≤ 2^−12, rational H_S (§8).
- R7, R8, R9: new gates C-τ, G5′, G-S (§13).
- R11, R12: even λ_1 dropped; 1/10 rung added to the odd ladder; the L = 2 verdict (needs ℓ_odd < 1.7e5) and S2
  (ℓ_odd ≤ 3, grid-G viability) are reported separately (§12, §15).
- R16: a sector-restricted stage S does not follow from the Collatz–Wielandt test (the odd kernel k(x−y) − k(x+y) is not
  positivity preserving); §6.1 keeps the full-window s(L) for both sectors.
