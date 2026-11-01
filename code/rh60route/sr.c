/* Lemma SR (PROOFS P23, SPEC §8 with review fixes R5, R6): exact structured LDL^T of a Cauchy-like matrix
     S_jk = h_j^T Jm h_k / (lam_j - lam_k) (j != k),  S_jj = d_j,  with the labels passed explicitly per row as the exact
   integers lab_j = 4 lam_j (AUDIT F3; the kernel no longer derives them from q0/w2), in exact integers (GMP).
   Rows are scaled: H_j = 2^P h_j, D_j = 2^P d_j. Multipliers are P-bit dyadics
     Lint_j = floor(nu_j / (Delta_ji D_i)),  nu_j = H_j^T Jm H_i,  Delta_ji = (lab_j - lab_i)/4
     (exact integer; the kernel checks that lab is strictly increasing with steps = 0 mod 4, else exit 3).
   Updates: H_j <- H_j - ceil(Lint_j H_i / 2^P),  D_j <- D_j - ceil(D_i Lint_j^2 / 2^{2P}).
   Per step i it records E_i = max_j rem_j (= 2^{2P} e_i), Lm_i = max_j |Lint_j| (= 2^P lbar_i), Gm_i = max_j |H_j(new)| + 1
   (>= 2^P G'_i), and accumulates  T = sum_i [E_i 2^P + 2 Lm_i E_i + J1 (2 Gm_i + 1) 2^P],  so that
     eps_E = n 2^-P + H_S T / 2^{3P}   (computed exactly in Python from T).
   Method credit: the structured Schur recursion follows rh_60 v1 (bramble_trace, unrefereed AI-agent preprint) in spirit; this
   exact-integer version with explicit residual is ours (PROOFS P23). Clean room: no rStation code was used.
   Input (text): "n D P" / D*D ints of Jm / n lines of D+1 hex ints (H_j..., D_j) and one decimal label lab_j. Output: one line of key=value. */
#include <stdio.h>
#include <stdlib.h>
#include <gmp.h>

int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r");
    long n, D, P;
    if (fscanf(f, "%ld %ld %ld", &n, &D, &P) != 3) return 2;
    long *Jm = malloc(D * D * sizeof(long)), J1 = 0;
    for (long a = 0; a < D * D; a++) { if (fscanf(f, "%ld", &Jm[a]) != 1) return 2; J1 += labs(Jm[a]); }
    mpz_t *H = malloc(n * D * sizeof(mpz_t)), *Dv = malloc(n * sizeof(mpz_t));
    long *lab = malloc(n * sizeof(long));
    char buf[4096];
    for (long j = 0; j < n; j++) {
        for (long a = 0; a < D; a++) { mpz_init(H[j * D + a]); if (fscanf(f, "%4095s", buf) != 1 || mpz_set_str(H[j * D + a], buf, 16)) return 2; }
        mpz_init(Dv[j]); if (fscanf(f, "%4095s", buf) != 1 || mpz_set_str(Dv[j], buf, 16)) return 2;
        if (fscanf(f, "%ld", &lab[j]) != 1) return 2;
        if (j > 0 && (lab[j] <= lab[j - 1] || (lab[j] - lab[j - 1]) % 4)) return 3;  /* labels: increasing, 4 | steps */
    }
    fclose(f);
    mpz_t *g = malloc(D * sizeof(mpz_t)), nu, den, Lint, rem, t, E, Lm, Gm, T, minp, sump, sumL, tmp;
    for (long a = 0; a < D; a++) mpz_init(g[a]);
    mpz_inits(nu, den, Lint, rem, t, E, Lm, Gm, T, minp, sump, sumL, tmp, NULL);
    long fail = -1;
    mpz_set(minp, Dv[0]);
    for (long i = 0; i < n; i++) {
        if (mpz_sgn(Dv[i]) <= 0) { fail = i; break; }
        if (mpz_cmp(Dv[i], minp) < 0) mpz_set(minp, Dv[i]);
        mpz_add(sump, sump, Dv[i]);
        for (long a = 0; a < D; a++) {             /* g = Jm H_i */
            mpz_set_ui(g[a], 0);
            for (long b = 0; b < D; b++) {
                long c = Jm[a * D + b];
                if (c > 0) mpz_addmul_ui(g[a], H[i * D + b], c); else if (c < 0) mpz_submul_ui(g[a], H[i * D + b], -c);
            }
        }
        mpz_set_ui(E, 0); mpz_set_ui(Lm, 0); mpz_set_ui(Gm, 0);
        for (long j = i + 1; j < n; j++) {
            mpz_t *Hj = &H[j * D];
            mpz_mul(nu, Hj[0], g[0]);
            for (long a = 1; a < D; a++) mpz_addmul(nu, Hj[a], g[a]);
            unsigned long Delta = (unsigned long)((lab[j] - lab[i]) / 4);
            mpz_mul_ui(den, Dv[i], Delta);
            mpz_fdiv_qr(Lint, rem, nu, den);       /* 0 <= rem < den */
            if (mpz_cmp(rem, E) > 0) mpz_set(E, rem);
            if (mpz_cmpabs(Lint, Lm) > 0) mpz_abs(Lm, Lint);
            mpz_add(sumL, sumL, Lint);
            for (long a = 0; a < D; a++) {
                mpz_mul(t, Lint, H[i * D + a]);
                mpz_cdiv_q_2exp(t, t, P);
                mpz_sub(Hj[a], Hj[a], t);
                if (mpz_cmpabs(Hj[a], Gm) > 0) mpz_abs(Gm, Hj[a]);
            }
            mpz_mul(t, Lint, Lint); mpz_mul(t, t, Dv[i]); mpz_cdiv_q_2exp(t, t, 2 * P);
            mpz_sub(Dv[j], Dv[j], t);
        }
        mpz_add_ui(Gm, Gm, 1);
        /* T += E 2^P + 2 Lm E + J1 (2 Gm + 1) 2^P */
        mpz_mul_2exp(tmp, E, P); mpz_add(T, T, tmp);
        mpz_mul(tmp, Lm, E); mpz_mul_2exp(tmp, tmp, 1); mpz_add(T, T, tmp);
        mpz_mul_2exp(tmp, Gm, 1); mpz_add_ui(tmp, tmp, 1); mpz_mul_ui(tmp, tmp, J1); mpz_mul_2exp(tmp, tmp, P); mpz_add(T, T, tmp);
        if (i % 4096 == 0) { fprintf(stderr, "i=%ld\n", i); fflush(stderr); }
    }
    printf("fail=%ld n=%ld D=%ld P=%ld J1=%ld T=%s", fail, n, D, P, J1, mpz_get_str(NULL, 16, T));
    printf(" minp=%s", mpz_get_str(NULL, 16, minp));
    printf(" sump=%s", mpz_get_str(NULL, 16, sump));
    printf(" sumL=%s", mpz_get_str(NULL, 16, sumL));
    if (fail >= 0) printf(" failpivot=%s", mpz_get_str(NULL, 16, Dv[fail]));
    printf("\n");
    return 0;
}
