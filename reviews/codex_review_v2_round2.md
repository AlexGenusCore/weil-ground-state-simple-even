**Verdict:** I advise public release as a preprint **after minor corrections**. I read all of `main.tex`, the bibliography, generated tables and the complete `supplement/PROOFS.md`, and inspected the principal certification routines. I found no fatal error or demonstrated major mathematical defect. The analytic structure is sound, and the numerical checks I performed support the reported results. The novelty claims are substantially careful: positivity is credited to earlier work, and the proposed advance is certification of simplicity and parity beyond \(L=0.8\). The paper appropriately avoids claiming progress on RH beyond this bounded-window spectral result. This is a positive preprint recommendation, **not an independent certification of every large computation** or a recommendation for journal acceptance without further computational review.

**Numbered issues**

1. **Minor — §6.2, `main.tex:474–476`: ambiguous “Galerkin value.”**  
   The quoted \(1.23364079\times10^{-40}\) appears to concern Elston’s reduced comparison matrix, rather than a Galerkin compression of the full form. As written, it appears inconsistent with Table 2’s certified lower bound
   \[
   \lambda_2^{\mathrm{ev}}(1.19)\ge1.439\times10^{-40}.
   \]
   The code explains why these can coexist: the comparison form lies below \(Q_L\). My direct full-form calculation gave a compatible second-eigenvalue upper bound of \(1.7130698436\times10^{-40}\) using 128 modes.  
   **Fix:** identify the quoted number explicitly as an eigenvalue estimate of the reduced matrix \(A_N\), and avoid comparing its relative accuracy with an eigenvalue of \(Q_L\).

2. **Minor — §5.4 dyadic-window remark, `main.tex:348–349`, and Table 2.**  
   The remark correctly explains coverage using dyadic windows \(\widetilde L_i\ge L_i\). However, Table 2 presents all four bounds as bounds at the printed decimal \(L_i\). Monotonicity transfers lower bounds from \(\widetilde L_i\) to \(L_i\), but does not transfer upper bounds in that direction. The displacement is negligible numerically, yet the distinction matters in a rigorous statement. The small-window argument should also consistently name its actual dyadic anchor.  
   **Fix:** label the records and table as bounds at \(\widetilde L_i\), and state Piece I with that anchor; alternatively, certify a bound for the small change in the trial quotient.

3. **Minor — §7.2–7.3, `main.tex:538–596`: incomplete notation.**  
   The subsequent formulas use \(\gamma_q\) in both sectors, but its odd-sector value is not stated explicitly. The matrices \(J_\vartheta\), \(J_b\), the balancing transformation and the vector \(g_q\) also appear without sufficient definitions in the paper itself. The supplement resolves these points.  
   **Fix:** explicitly set \(\gamma_q=1\) in the odd sector and add the definitions
   \[
   g_q=(u_q,v_q)^T,\qquad
   J=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad
   J_\vartheta=\operatorname{diag}(J,\vartheta J),
   \]
   together with the precise transformation defining \(J_b\).

4. **Minor — §5.2 head matrix, `main.tex:252,308`: Fourier-phase notation.**  
   For odd real basis functions, \(\widehat e_n(t)\) is imaginary. Consequently, the displayed product \(\widehat e_j\widehat e_k\) needs either a conjugate or an explicit convention that the common sector phase has been removed. The implementation uses real representatives and appears consistent.  
   **Fix:** introduce phase-adjusted real transforms, or write the Hermitian product with complex conjugation.

5. **Minor — §1.3 and `refs.bib`, entry `KB`: incomplete description of relevant prior work.**  
   Kramarenko–Byrd’s actual title is *Restricted Weil ground states and real Fourier zeros: A form-core criterion and a certified interval of supports*. Besides the claimed simple-even interval, it states a form-core replacement for the operator-core hypothesis discussed prominently in your introduction. Your caution about applying Connes–van Suijlekom remains appropriate, but this related claim deserves explicit mention. I inspected the author’s public manuscript and the cached Zenodo metadata; I did not validate its numerical certificates. [Author’s manuscript](https://www.academia.edu/176369419/Restricted_Weil_ground_states_and_real_Fourier_zeros_A_form_core_criterion_and_a_certified_interval_of_supports)  
   **Fix:** use the actual title and briefly describe the additional form-core claim, retaining its unrefereed status.

6. **Minor — §10.2, verification commands; `code/gap/check_steps.py` and `code/rh60route/check_steps.py`.**  
   The gluing commands validate comparisons between recorded bounds. They do not independently establish those bounds. Moreover, the Piece IV gluer checks selected provenance/status fields without itself checking all fifteen gate flags; `gen_tables.py` performs the stronger check. All supplied Piece IV records passed that stronger check in my run.  
   **Fix:** distinguish record validation from certificate regeneration, and have the advertised combined checker enforce the full gate/schema checks already present in the table generator.

7. **Minor — §1.4, contribution 2, `main.tex:113`.**  
   Rank-one deflation/interlacing is standard. The contribution here is its useful application to these continuum certificates and the resulting structured implementation. The present wording could suggest novelty of the elementary lemma.  
   **Fix:** say “an application of standard rank-one interlacing” and identify the problem-specific extension.

8. **Typo — Table 8, `main.tex:785–786`.**  
   From the supplied raw records, the \(N_{\rm tot}=800,\ n=7\) entry is approximately \(0.106484\), and the \(N_{\rm tot}=1200,\ n=9\) entry is approximately \(0.117469\). Ordinary rounding to three decimal places gives \(0.106\) and \(0.117\), rather than \(0.107\) and \(0.118\). The reported means, coefficients of variation and fitted parameters reproduce.  
   **Fix:** generate these table entries directly from the records.

9. **Minor — abstract and §§7, 10–11: presentation.**  
   The disclosure is commendably candid, but operational history, gate names and repeated accounts of AI reviews obscure the mathematical argument. A specialist outside the project must work hard to distinguish the proof dependencies from the experimental protocol.  
   **Fix:** shorten the abstract, provide one compact dependency summary, and move repeated protocol/audit history to the supplement. Preserve the failed-grid disclosure and the distinction between illustration and proof.

**Claims independently verified, and how**

- **Form and normalization.** I checked the Fourier and position-side formulas, Plancherel factors, prime-power weights, pole signs and support thresholds. The displayed normalization agrees with CCM’s formula under logarithmic coordinates; \(2\theta'(t)=H(t)\). [CCM, §3](https://arxiv.org/html/2511.22755v1)

- **Operator setup and elementary spectral arguments.** The closability, lower boundedness and compactness arguments work for the stated realization. I checked the parity lemma, spectral criterion, zero-extension monotonicity, step criterion, block estimate, rank-one deflation and second-eigenvalue corollary. No positivity assumption or RH assumption is needed for these arguments.

- **Analytic estimates.** I checked the proofs of the \(h\)-bound, Binet bound, digamma envelope and monotonicity, Bessel bounds and ratio enclosure. The corrected Gauss–Legendre exponent is consistent with Trefethen’s Theorem 19.3 after changing from \(n+1\) points to \(n\) points. [Trefethen, Chapter 19](https://people.math.ethz.ch/~hiptmair/Seminars/RAP_22/TRE13.pdf)

- **Piece I constants.** At 768 bits I reproduced
  \[
  I\le0.593978522651198312,\quad
  C_{\rm ev}\le4.87636167670537617,\quad
  C_{\rm odd}\le0.761665418948983911.
  \]
  With the supplied anchor records, the resulting gap bounds are approximately \(0.4172751225\) and \(0.6624248462\), supporting the printed \(0.4172\) and \(0.6624\).

- **Piece IV derivations.** I checked the Green identity, response expansion and boundedness, displacement algebra, virtual-label diagonal correction, moment estimates, Abel bounds, covariance bounds, assembly debit, omitted-tail estimate and both square completions in P1–P23. The structured \(LDL^T\) residual argument is algebraically valid. I also exercised its Python integer implementation on small instances.

- **Independent matrix entries.** Using separately constructed autocorrelations and position-side integration, I checked 24 trigonometric entries across both parities at \(L=1.4035,\ 1.92364501953125,\ 2\). Maximum discrepancy was \(2.12\times10^{-55}\). Forty Legendre entries at \(L=0.05,\ 0.8,\ 1.19,\ 2.25\) agreed with the recurrence assembly to \(1.58\times10^{-56}\).

- **Selected far-block constants.** At \(L=2\), independent computation gave
  \[
  V_h=1.68331341371549,\qquad E_h=232.760909753130,
  \]
  consistent with the supplement. I independently reconstructed the weighted cell Schur majorant on a small grid and obtained the same bound as the supplied routine.

- **Recorded comparisons and tables.** `check_theorem.sh` completed successfully. The file checks passed; all grid comparisons passed; both rule-E and monotonicity-substitution routes passed. Regenerating `generated.tex` in memory reproduced it byte for byte. All 106 exported Piece IV lower-bound balls enclosed their recorded exact rational \(\mu\).

- **Numerical illustrations.** The kink means and coefficients of variation reproduce. The logarithmic fit gives \(c=0.73972545\), \(b=0.58636450\), with maximum residual about \(0.002075\). The comparisons at \(L=2.25\) reproduce the exponents \(-1052.91975\), \(-504.00296\) and \(-1093.82973\). These checks support the paper’s appropriately limited numerical interpretation.

- **Principal prior-work descriptions.** Zhu’s Theorem 6.2, Suzuki’s Theorem 1.4, CCM’s Theorem 3.6 and Connes–van Suijlekom’s Theorem 6.1 support the descriptions given. In particular, the latter really does impose essential self-adjointness on the trigonometric restriction. [Zhu](https://arxiv.org/html/2608.24827v2), [Suzuki](https://arxiv.org/html/2606.09096v1), [Connes–van Suijlekom](https://arxiv.org/html/2511.23257v1)

- **rStation attribution and scope.** Papers 45 and 60 state positivity results without the continuum ground-state identification claimed here. Paper 83 states unconditional fixed-index upper bounds at the \(4\pi e^{2L}\) scale, as your revised survey acknowledges. I found no inspected source establishing certified simple-even ground states beyond \(0.8\) that invalidates your carefully qualified novelty statement. [Paper 45](https://rstation.ai/problems/riemann_hypothesis/papers/45/v1), [Paper 60](https://rstation.ai/problems/riemann_hypothesis/papers/60), [Paper 83](https://rstation.ai/problems/riemann_hypothesis/papers/83)

**What I could not check**

- I did not regenerate the large window matrices, production C factorizations, all stage-S bounds or the multi-hour upper-bound calculations. Successful gluing is not a substitute for those checks.
- I did not fully audit Elston’s Kaiser integration, every production code path, historical code revisions or the underlying Arb/FLINT implementation.
- I searched arXiv, Zenodo, GitHub and rStation independently. Several Zenodo pages and the specified rStation API endpoints were inaccessible; public rStation paper pages were accessible. Consequently, this was not an exhaustive current API census, and I cannot certify absence of competing prior work.
- I did not verify every peripheral manuscript, every bibliographic theorem number, publication timestamp or the claimed clean-room history.
- I established neither an operator-core result nor a Fourier-zero consequence for your ground state. The paper correctly refrains from claiming them.

No files were modified.