# Piece IV supplement (release 2.0.0): specification, proofs, and a formula → code → record map

This folder holds the derivations behind Piece IV of the paper (§7, Theorem `thm:V`). Before release 2.0.0 they were
"available on request"; the second AI review (Codex, `reviews/`) asked for them to be public, because the paper states
τ_N, r_M, the generators, the diagonal and the assembly debit but did not prove them.

| file | what it is | sha256 |
|---|---|---|
| `PROOFS.md` | P1–P23: first-principles proofs of every formula and constant the certifier uses, and Theorem V (§8) | `7e18f2d0…4c8a2`, **byte-identical** to the file stamped in `data/piece4/GAP.stamp` (line `hp/lb/rh60route/PROOFS.md`) |
| `SPEC.md` | the specification the code was written from (stages C, T, F, I, P; gates; constants table) | redacted copy, see `REDACTION.sha256`; the original's sha256 `c9862cb7…f446` is the `SPEC.md` line of `GAP.stamp` |
| `MAP.md` | this file | — |

`SHA256SUMS` lists the shipped bytes; `check_theorem.sh` checks it and that `PROOFS.md` matches `GAP.stamp`.

**Status.** Both documents were written with an AI assistant (Anthropic's Claude) on 2026-10-31, before the grid was
pre-registered, from the manuscript text of rStation papers 45 and 60 (equation numbers "rh60 (x.y)" only say which step a
lemma replaces) and our own paper and code. They were reviewed only by AI agents. No human has checked them. They contain no
rStation code. Where they differ, PROOFS.md (P1–P23) holds over SPEC.md (SPEC §16); PROOFS §11 lists the corrections (a)–(g)
to SPEC, all applied in the code. SPEC §15 (pilot plan) and §12 (pilot defaults) are history; the registered parameters are
those of `data/piece4/PREREG_GRID.md` and `PREREG_GAP.md`.

**Paths in the documents.** They name the development tree. Shipped counterparts: `code/` and `lb/rh60route/code/` →
`code/rh60route/`; `lb/liu/stage_s.py`, `liu.py` → `code/rh60route/stage_s.py`, `liu.py`; `gap/elston/` → `code/gap/elston/`;
`highprec/fr_sweep.py` → `code/upper/fr_sweep.py`; `gap/check_steps.py` → `code/rh60route/check_steps.py` (the Piece IV
version). `review.md`, `spec_changes.md`, `PREREG.md`, `AUDIT.md`, `FIXES.md`, "Liu AUDIT" and `proofs_spot.py` are not shipped
(available on request, info@genuscore.com). `DERIVATION.md` in SPEC means PROOFS.md.

**Redaction of SPEC.md.** One compute host name and one `user@IP` login line are replaced by `vm4` and `user@vm4`, the same
scheme as `data/piece4/REDACTION.sha256`. Nothing else changed.

## Map: formula → paper → code → record field

Code is `code/rh60route/certify.py` (function `run`) unless another file is named. Record fields are those of every record in
`data/piece4/glue/`, `rule_e/` and `controls/`; "gate X" means `gates["X"]`. All 15 hard gates are listed in paper Table
`tab:gates`. Every certified quantity is an Arb upper (or lower) end or an exact rational.

| PROOFS | quantity | paper | code | record fields and checks |
|---|---|---|---|---|
| P1, P2 | Green identity, Green expansion of Q_L | Prop. `prop:green` | none (identity) | its numerical content is checked through the entries: gates G0-mini, G0i |
| P3 | form core and closure | Thm `thm:V`, proof, first step | none (argument) | — |
| P4, P5 | translation integrals; off-diagonal A_qr = (u_q v_r − v_q u_r)/(λ_q − λ_r); u_q = γ_q (2L/π²) Φ_ε(κ_q), v_q = γ_q | §7.2, displacement identity | `entries.py` `Form.rows` (key `u`), `Form.trig` (S, C); core assembly `M0` | gate G0-mini (4 entries vs eq. (P)), gate G0i and field `G0i` (8 entries, independent mpmath code `mp_entries.py`) |
| P6 | exact diagonal A_qq = H(κ_q) − 2C(κ_q) + [κ_q>0] S(κ_q)/(Lκ_q) + (2/L)γ_q² R_ε(κ_q) | §7.2, diagonal formula | `entries.py` `Form.rows` (key `A`; `R0` at even q = 0) | gates G0-mini, G0i |
| P7 | truncation of the response sums, δ_J | §7.2 | `entries.py` `Form.__init__` (`dJ`, `dJc`), added as balls | — |
| P8 | response-sum norm (used only in P3(b)) | — | none | — |
| P9 | prime norm −B_p^ε ⪯ s(L), window b = ⌈2^24 L⌉/2^24 | (V1), stage S | `stage_s.py`, `liu.py` `Lwin`; read as an exact Fraction from `--s-file` | `s`, `s_float`, `s_sha256`; gate G-S with `G-S_guard` (Ritz values from `ritz.py`, input files in `data/piece4/inputs/`) |
| P10 | core positivity (Lemma IC) and certified solves | (V2) | `certify_core` (Elston's `cholesky_blocked`, `exact_residual`); solves `tri_solve` + residual / `m_core` | `m_core`, `lam_min_core_float` (float, no rigour), `solve_err_a`, `solve_err_b`, `solve_err_e`, `solve_err_eh`; gate V2 |
| C4 (SPEC) | deflation vector φ (128-bit dyadic) and weight ϑ = 4^t | §7.3 | `inv_iter`, `floor_dy(·, 128)`, `theta` | `theta`, `theta_log4`, `lam1hat_M0`, `lam2hat_M0` (floats) |
| P11 | post-core generators 𝒢_q = 𝒯(λ_q)(u_q, v_q)ᵀ; transfer rows R_{x,y}(z) = Σ_{i<K} x_i y_i/(z − λ_i) | §7.3 | rows `TR`, `gen`; R and R′ by `pf_sums` (P13); exact power-of-two pair balancing | `balance`, `A_f_log2max`; gate G5p (second path for every 𝒢_q on [K, M)), gate G5 |
| P12 | diagonal correction S_qq = A_qq − μ − Q_q, Q_q = gᵀ𝒯ᵀJ_ϑ𝒯′g | §7.3 | `Qform`, `Sqq` | gate G5: `G5_Q_maxreldiff`, `G5_parts.Q_and_core_solves` (direct Arb solve at 32 indices) |
| P13 | partial fractions for 1/(λ_q − λ_i) and its square | — | `pf_sums`, `toep`, `hank` | exact checks in gate P0 (grid level) |
| P14 | moment bounds F0, F1 (|zR(z)|, |z²R′(z)| for z ≥ z_0) | §7.3, explicit constants | `F01` (moments `mom`, `Af`, R rule) | recomputed independently in `indep.py` `far` (gate C-ind) |
| P15 | L_ab at z_0 = k_N² | §7.3 | `Lab` | via `tau_core` and gate C-ind |
| P16 | r̄(L) | §7.3 | `rbar` | `rbar`; gate C-rbar with `C-rbar_max` (the Arb max of r_q over [K, M)) |
| P17 | V_h, E_h, J_2(N), J_4(N) | §7.3 | `Vh`, `Eh`, `isn` (asserts every sine ball excludes 0), `J2`, `J4` | `V_h`, `E_h`, `J2`; gate C-J2 with `C-J2_sum` |
| P18 | τ_core, τ_pole, τ_N = τ_core + [ε = −1] τ_pole | (V3), §7.3 | `taus` | `tau_core`, `tau_pole`, `tau_N`; gate C-tau with `C-tau_sumQ`, `C-tau_pole_sum`; gate C-ind |
| P19 | t_q = H(κ_q) − μ − s − τ_N; t′_N = ⌊t_N⌋_40, t′_q = max(t′_N, ⌊t_q⌋_40), t′_q = t′_M for q ≥ M; the N rule | (V3) | `tq`, `floor_dy(·, 40)`, `tp_`, `tpM`, the `N` loop (`--tmin`, `--nstep`) | `N`, `tmin`, `t_N`, `tprime_N`, `tprime_M`; gate V3 |
| P20 | S_M on I_P = [K, N): rows h_i = (𝒢_i, w_i), 𝒥 = [[J_b, −I], [I, 0]], diagonal S_ii − 𝒢_iᵀJ_bZ2(i)J_bᵀ𝒢_i | (V4) input | stage I block: `Z`, `Z2`, `hrows`, `dS`, `Jm` | gate G5, `G5_parts.S_input_entries` (10 entries of S_input against a direct dense evaluation) |
| P21 | ε_asm and H = (1 + log(N − K))/K | (V5) | assembly block: `eh`, `ed`, `habs`, `Hc`, `HS`, `easm`; δ_0 = ⌈r_M + ε_asm + 2^−10⌉_8 | `eps_asm`, `H`, `e_h`, `delta0` |
| P22 | omitted tail r_M | (V5) | `Sa`, `Ar`, `Cr`, `beta`, `varrho`, `rM`; M = 4N, or 8N if r_M > 1/4 | `M`, `r_M`; gate C-rM with `C-rM_finite` (the finite part over [M, 2M)); gate C-ind |
| P23 | Lemma SR (exact structured LDLᵀ) and ε_E | (V4), (V5), Lemma `lem:SR` | `sr.c` (kernel), `sr.py` (`ref`, `kernel`, `eps_E`, `float_ldl`); labels 4λ_q from `entries.Form.lam4` | `SR_fail`, `min_pivot`, `eps_E`, `SR_checksum`, `SR_labels`, `SR_seconds`, `float_pmin` (float, no rigour); gates V4, R6 |
| §8 (Theorem V) | the certificate: lb(δ_0 − ε_E − ε_asm − r_M) > 0 gives Q̄_L + ϑ⟨Φ, ·⟩² ⪰ μ | Thm `thm:V` | `v5`; `certified_lower_bound = lower(μ)` | `V5_margin`, `mu`, `mu_float`, `mu_rel`, `mu_ref`; gate V5; `result`, `failed_gates`, `certified_lower_bound` |

**Independent recomputation (gate C-ind).** `code/rh60route/indep.py` `far` recomputes τ_core, τ_pole, t_N and r_M in mpmath
from P14–P18 and P22 with its own prime list, moments, F0/F1, L_ab and 𝒯 rows. Its inputs are the run's core solves (checked
by G5) and generators (checked by G5′). It requires each run value to lie in [mp, mp·(1 + 10^−3)]. The field `C-ind` holds
the comparison.

**What this supplement does not do.** It does not re-verify stage S's cell evaluation, Elston's integer Cholesky, Arb/FLINT,
or the paper's operator setup (PROOFS §11, items 1–4; paper §7.7).
