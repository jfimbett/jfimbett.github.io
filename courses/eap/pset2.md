---
Author: "Juan F. Imbet Ph.D."
---
# Problem Set 2

## Empirical Asset Pricing

## M2 104

## Paris Dauphine - PSL

The problem set together with the code needs to be emailed to juan.imbet@dauphine.psl.eu *before* March 7 23:59. You can solve the problem sets in groups of maximum *2* people. 

# Setup

Consider the following factor model with 5 assets and 2 factors with the appropriate dimensions of the parameters:

$$
\begin{align*}
\underbrace{R_{t}^e}_{5 \times 1} &= \underbrace{a}_{5 \times 1} + \underbrace{\beta}_{5 \times 2} \underbrace{f_t}_{2 \times 1} + \underbrace{\epsilon_{t}}_{5 \times 1} \\
\end{align*}
$$
with $\epsilon_t \sim \mathcal{N}(0, \Sigma)$, where $\Sigma$ is a non-diagonal covariance matrix. And $f_t \sim \mathcal{N}(\mu_f, \Sigma_f)$, where $\Sigma_f$ is the covariance matrix of the factor realizations, and $\mu_f$ is the expected value of the factor returns. 

the true values of the parameters are:
$$
a = \begin{pmatrix} 0.0 \\ 0.0 \\ 0.0 \\ 0.0 \\ 0.0 \end{pmatrix}, \quad \beta = \begin{pmatrix} 0.5 & 0.0 \\ 0.0 & 0.5 \\ 0.5 & 0.5 \\ 0.3 & 1.2 \\ 0.7 & 0.4 \end{pmatrix}, \quad \Sigma = \begin{pmatrix} 1.0 & 0.5 & 0.5 & 0.5 & 0.5 \\ 0.5 & 1.0 & 0.5 & 0.0 & 0.0 \\ 0.5 & 0.5 & 1.0 & 0.0 & 0.0 \\ 0.5 & 0.0 & 0.0 & 1.0 & 0.5 \\ 0.5 & 0.0 & 0.0 & 0.5 & 1.0 \end{pmatrix}
$$
and
$$
\mu_f = \begin{pmatrix} 0.05 \\ 0.07 \end{pmatrix}, \quad \Sigma_f = \begin{pmatrix} 1.0 & 0.5 \\ 0.5 & 1.0 \end{pmatrix}
$$

---
# Question 1 (4 points)
Create a function that given a time horizon $T$ simulates the dynamics of the system above. The function should return both time series $R_t^e$ and $f_t$. 

<div style="page-break-after: always;"></div>

---
# Question 2 (4 points)
Create a function that given simulated data $R_t^e$ estimates using OLS and GLS the parameters $\hat{\alpha}$ and $\hat{\lambda}$ (together with their standard errors) in the following model (assume that you only know the true values of $\Sigma$, $\Sigma_f$ and $\beta$ so you dont need to estimate them):
$$
E_T[R_{t}^e] = \alpha + \beta \lambda
$$

---
# Question 3 (4 points)
For a given $T=10$ repeat the above exercise 1000 times and plot the distribution of the estimated parameters $\hat{\alpha}$ and $\hat{\lambda}$ (together with the true values). What do you observe? The true values of $\alpha$ are $a$ and the true values of $\lambda$ are $\mu_f$.

---
# Question 4 (4 points)
Repeat the above exercise, but for each estimated parameter consider the distribution of the ratio
$$
\frac{\hat{\theta}-\theta}{\text{s.e.}(\hat{\theta})}
$$
can you find any difference in the distribution of the ratios between OLS and GLS? Hint: look at the tails of the distribution. Comment on the results.

---
# Question 5 (4 points)

Assume now that you do not know the true values of $\beta$, $\Sigma$ and $\Sigma_f$. For a fixed $T=10$ and 1000 simulations, compare the expected value of your estimators. Does estimation error affect the expected value of $\hat{\alpha}$ and $\hat{\lambda}$? Comment on the results.