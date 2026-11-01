# Notes on the supplement files

`SPEC.md` and `PROOFS.md` are kept byte-for-byte as stamped (apart from the redactions listed in `REDACTION.sha256`), because
their hashes are recorded in the pre-registration stamps. Corrections and clarifications are therefore listed here instead.

- **SPEC.md, "Pilot verdict", priority note** ("a forum value (rh_60 follow-up, unreviewed) already orders the sectors at
  L = 2"). The precise source is the forum comment `jcjVYEFhSmZlQq-f` by bramble_trace on rStation riemann_hypothesis post 42,
  created 2026-10-26T19:25:56Z (https://rstation.ai/r/riemann_hypothesis/posts/42#comment-jcjVYEFhSmZlQq-f), cited in the paper
  as [rh60gap]. It states, as an unreviewed author calculation, inf sigma(A_2^-) > 8.8e-283 (odd sector, L = 2). It does not
  itself claim the sector ordering; the ordering follows from that bound together with an even upper bound (ours, 1.847e-283, or
  Zhu's 3.19e-283). We have not checked its values, and it is used in no proof. See the paper, Section 1.3.
