# Responses to the second Codex review of release candidate 2.0.0 (review of 2026-11-01, 04:38)

Review: `reviews/codex_review_v2_round2.md` (OpenAI Codex, read-only, with web search). It advised public release as a
preprint after minor corrections. It also said that this is not an independent certification of every large computation.
We accept all nine points. No certified number that enters the proof changes.

Section, remark and table numbers below are those of the revised `paper/main.pdf`; the headings keep your numbering. The
review's "Table 8" (source lines 785–786) is the kink table, Table 9 in the compiled PDF.

These responses were drafted with an AI assistant (Anthropic's Claude), like the rest of this work. The fixes have not yet
been reviewed by Codex or by a human.

**1. Ambiguous "Galerkin value" (§6.2).** Accepted.
- The number 1.23364079e−40 is now labelled as the certifier's floating-point estimate of λ₁(A_N + vvᵀ). That estimate
  approximates λ₂(A_N) of Elston's reduced comparison matrix; it is not an estimate of an eigenvalue of Q_L.
- The text now says that R′ lies below Q_L, so the estimate says nothing about how close the certified bound is to
  λ₂^ev(1.19). It points to the bound λ₂^ev(1.19) ≥ 1.439e−40 from Table 2 and Lemma 3.1, and it makes no accuracy
  comparison.

**2. Dyadic anchors (Remark 5.12, Theorem 4.1, §5.1, Table 2).** Accepted. We checked every use of an upper bound against
the code and records. We found one use away from its anchor, which we fixed. It entered no step of the theorem.
- **Anchors.** In Pieces I–II, `certify.Window` sets L = `arb(L_i).upper()`. That is the upper end of the Arb ball of the
  decimal string at the run's working precision: 768 bits for L ≤ 0.8 and 1536 bits for 0.84–0.97. For L ≥ 0.98 the base
  precision was not logged; the default is 768. All four bounds of a row (ℓ₁, U, ℓ₂, ℓ^odd), including the Rayleigh upper
  bound, are computed at this anchor L̃_i. We measured L̃_i − L_i < 2^−767 at 768 and 1536 bits.
- **New Remark 5.12(b)** states how bounds transfer. Lower bounds transfer down to L_i by Lemma 3.1. U(L̃_i) bounds
  λ₁^ev(L̃_i) only and is used only there.
- **Pieces I–II.** `theorem.py --check` compares consecutive rows, so it proves the steps [L̃_i, L̃_{i+1}].
  - Theorem 4.1 items (1)–(2) now name (0, L̃₀] and the steps [L̃_i, L̃_{i+1}]. Together they cover
    (0, L̃₃₀] ⊃ (0, 1.19].
  - Piece I (§5.1) is anchored at L̃₀. Its constants are enclosed on the 768-bit ball of 0.05. That ball's upper end is
    L̃₀, and the factor L₀ in the gap bounds is now L̃₀.
  - `check_theorem.sh` now pins `CERT_PREC=768` for this check, so the ball is the one used in the certificate run.
- **Table 2.** The caption and column heads now say that every bound is a bound at L̃_i. The lower bounds also hold at
  L_i; U does not.
- **Pieces III–IV and §8.** Elston's certifier, the Piece IV certifier and `fr_sweep.py` all take the window as a decimal
  string. They evaluate everything that depends on L on the Arb ball of that string, which contains the decimal. Their
  anchor is therefore the printed L_i (Remark 5.12(c)).
- **Junction at 1.19.** The first Piece III step [1.19, 1.2205] uses U(1.19) ≤ 8.712e−48. That is the K = 640 bound at
  the decimal 1.19, not Table 2's 1.312e−47, which is a bound at L̃₃₀. `code/gap/check_steps.py` no longer seeds U(1.19)
  with Piece II's value. It was never the minimum, so the output is unchanged and identical to `data/piece3/check.log`.
  Even if it had been used, that step would have been [L̃₃₀, 1.2205], which is still contiguous with Piece II.
- **The fix.** §6.2's pointwise check at L = 1.19 compared Table 2's U(1.19), a bound at L̃₃₀, with Elston's lower bounds
  at the decimal 1.19. That was an upper bound away from its anchor. It now uses the K = 640 bound at 1.19, and the ratio
  is ≥ 4499 (was 2987). This check enters no step.
- The stamped `code/rh60route/check_steps.py` also carries the 1.312e−47 seed for L = 1.19. 1.19 is not on the Piece IV
  grid, so the seed is never read there. We left the file unchanged, because its hash is in `GAP.stamp`.

**3. Notation in §7.2–7.3.** Accepted.
- §7.2 now says that γ_q := 1 for every q in the odd sector. It defines g_q = (u_q, v_q)ᵀ and J = [[0, 1], [−1, 0]],
  with (λ_q − λ_r)A_qr = g_qᵀ J g_r.
- §7.3 defines J_ϑ = J (m = 2) or diag(J, ϑJ) (m = 4), the entrywise derivative 𝒯′, and the identity
  (λ_q − λ_r)𝒮_qr = 𝒢_qᵀ J_ϑ 𝒢_r.
- A new item, "Balancing", gives the transformation that `certify.py` applies. The rows of 𝒯 are multiplied by
  B = diag(2^τ, 2^−τ), or by diag(2^τ, 2^−τ, 2^{t+τ′}, 2^{t−τ′}) with ϑ = 4^t. Then J_b := B⁻¹ J_ϑ B⁻¹, which equals J
  or diag(J, J). After this point 𝒯, δ and 𝒢_q denote the balanced quantities. This is the convention of P15, P20 and
  P22.

**4. Fourier phase in the head matrix (§5.2).** Accepted.
- §5.2 now states ê_n(t) = iⁿ c_n 2L j_n(Lt), which is imaginary for odd n.
- It introduces the phase-adjusted real transforms ě_n := i^{−σ} ê_n, with σ = 0 (even) or 1 (odd). Then
  ě_j ě_k = ê_j conj(ê_k) on the real axis and |F|² = (Σ a_m ě_{n(m)})².
- The head matrix, the strip bound and the tail bounds now use ě. This is the real representative that the code uses.

**5. Kramarenko-Byrd (§1.2, §1.3, `refs.bib`).** Accepted.
- We checked the metadata with the Zenodo API (record 23007100, version 1.0, 2026-09-27). The creator is
  Kramarenko-Byrd, Pavel V. The title is *Restricted Weil ground states and real Fourier zeros: A form-core criterion and a
  certified interval of supports*. The bib entry now uses this title and the DOI 10.5281/zenodo.23007100, and it no longer
  says "title paraphrased".
- §1.3 now describes both claims of the deposit:
  - a form-core criterion meant to replace the operator-core hypothesis of Connes–van Suijlekom, Thm. 6.1, with its
    hypotheses stated to hold for the restricted Weil form at every finite support;
  - a certified simple-even ground state on 0 < L ≤ 4/5, and hence, with the criterion, real Fourier zeros there.
- We say that we have checked neither claim, nor whether its realisation agrees with our A_L. We draw no conclusion about
  zeros from it, and the deposit stays marked as unrefereed.
- §1.2 now points to this claim where it says that we have no form-core substitute.

**6. Record validation versus regeneration (§10.2, checkers).** Accepted.
- **§10.2.** It is rewritten around two kinds of check.
  - *Record validation* takes seconds. It shows that the recorded bounds, if correct, prove the theorem.
  - *Certificate regeneration* takes hours per window. Only it tests whether a bound is correct.
  - Each command is labelled as one or the other. The dependency summary, `check_theorem.sh`, README and REVIEWING.md
    say the same.
- **`check_theorem.sh` now runs `paper/gen_tables.py` as a record validator.** Its output must equal `paper/generated.tex`
  byte for byte. The check is strengthened:
  - the gate set must be exactly the 15 hard gates of `certify.py`, all `true`;
  - every glued record's `certified_lower_bound` ball must contain its exact μ (your check);
  - every Piece III record must have `args.a` equal to its window, and the right sector and deflation flag;
  - the script refuses to run under `python -O`, because its checks are asserts.
- **Stamped checker unchanged.** `code/rh60route/check_steps.py` is unchanged, because its hash is in `GAP.stamp`. Its
  docstring and the paper say what it checks.
- **Tests.** We re-ran `check_theorem.sh` on the shipped data. It passes, including both Piece IV routes (53 steps each,
  minimum ratio 2.099). We then set `gates.V4 = false` in `data/piece4/glue/g_2_odd.json` in a temporary copy.
  - With `data/piece4/SHA256SUMS` updated to match, the stamped Piece IV gluing still passes both routes. The new
    validation fails, and the script ends "NOT CERTIFIED: record validation (paper/gen_tables.py)" with exit 1.
  - Without the SHA256SUMS update, the script now fails at the hash check ("FAIL: data hashes", exit 1).
- **A defect the second test exposed.** Before this fix, a data-hash mismatch printed sha256sum's warning but did not stop
  the script. Under `set -e`, a failure inside an `&&` list does not exit. The data-hash line now ends in an explicit
  `|| { echo "FAIL: data hashes"; exit 1; }`. The supplement-hash line already had one. On the shipped data no hash ever
  failed, so no earlier result is affected.

**7. Contribution 2 (§1.4).** Accepted.
- It now reads "an application of standard rank-one interlacing" and says that the lemma itself is elementary and not
  new.
- It names the problem-specific part:
  - in Piece III, the deflation is inserted into Elston's certifier at no extra assembly cost;
  - in Piece IV, it is lifted to the operator (the certificate inequality) and carried through the structured Schur
    elimination as a second generator pair, which raises the displacement rank from 2 to 4.
- Rank-one interlacing is added to "Not claimed as new".

**8. Kink table (Table 9; your Table 8).** Accepted.
- The rows are now generated from `data/kinks/kink_119_<N>.json` by `paper/gen_tables.py` (macro `\KINKrows`). The
  script uses the y > 0 breakpoints, normalises by weight and f(L), rounds to three decimals, and computes the CV with the
  population standard deviation.
- The two entries change: N_tot = 800, n = 7 is 0.106 (from 0.106484; was 0.107), and N_tot = 1200, n = 9 is 0.117
  (from 0.117469; was 0.118). All other entries, the means and the CVs are unchanged.
- The caption says how the rows are generated.

**9. Presentation (abstract, §§4, 7, 10).** Accepted.
- **Abstract.** It is shortened from about 400 to about 200 words. It keeps the result, the four methods with credit,
  the failed-grid disclosure, the novelty status, the statement that no conclusion about zeros is drawn, and the
  AI-review status.
- **Dependency summary.** A new paragraph follows Theorem 4.1. For each item it lists the lemmas, the code, the records
  and the imported trust it depends on. It states that, in Piece IV, only (V1)–(V5) are premises. The other gates, the
  pre-registration, the cross-checks and §9 are tests or illustrations. The checking scripts validate records and do not
  regenerate certificates.
- **Remark 4.2** is cut to the disclosure that the registered grid failed and that the open step has two proofs.
- **Moved to `supplement/AUDITS.md`.** The full clean-room protocol (§7.1 keeps a short summary and the credit), the
  per-piece review history (§10.3 is now one paragraph), and the "earlier drafts" note in Remark 7.5. AUDITS.md is listed
  in `supplement/SHA256SUMS` and MAP.md.
- **Kept in the paper.** The failed-grid disclosure (Remarks 4.2, 7.1, 7.5 and §7.6) and the distinction between
  illustration and proof (§9 and the dependency summary).
- References to "the second AI review" now say which Codex round is meant.

**Other changes.**
- `paper/generated.tex` is regenerated. Its only change is the new `\KINKrows` macro. Every Piece IV and Piece III number
  is byte-identical.
- The paper compiles with no new warnings.
- `reviews/REDACTION.sha256` records this review. Its text contained no local path, so the shipped copy is byte-identical
  to the original. The session log is not shipped.
