---
marp: true
paginate: true
title: Empirical Asset Pricing
author: Juan F. Imbet Ph.D.
---

# Lesson 1A: Campbell and Shiller Decomposition

## Juan F. Imbet Ph.D.
## Empirical Asset Pricing

---

# The Equity Premium

- Average returns on stocks $r_m$ are higher than the returns on short-term nominal bonds $r_f$.
- The Equity premium $\mathbb{E}[r_m - r_f]$ and Sharpe ratio for the U.S. is robust across samples. For a long sample from 1926.7-2021.7, the equity risk premium in the U.S. is 8.3%, return volatility is 18.5% and the Sharpe Ratio is 0.45.
- The Equity risk premium is similarly large for Europe and Asia Pacific, excluding Japan. 
- Japan is a surprising **outlier** with no equity risk premium, bonds and stocks have had almost the same expected return. 

---
# The Equity Premium (Cont.)
- Equity returns are volatile, which makes it challengin to estimate the equity premium precisely. Even with 95 years of data we have a standard error of $18.5/\sqrt{95} \approx 2\%$. A 95% confidence interval ranges from 4% to 12% ($t$-statistics of around 2 $\times$ the standard error. )
- Avdis and Wachter (2017) provide unconditional maximum likelihood estimators of the equity risk premium. 

---
# Time-series predictability and excess volatility

- Campbell and Shiller (1988) develop a log-linear approximation of returns that results in a useful accounting identity to udnerstand the link between stock prices, fundamentals and expected returns. 

$$
r_{t+1} = \log\Big(\frac{P_{t+1}+D_{t+1}}{P_t}\Big) = \Delta d_{t+1} - pd_t + \log\Big(1+\frac{P_{t+1}}{D_{t+1}}\Big)
$$

where $pd_t = \log\Big(\frac{P_t}{D_t}\Big)$ is the log price-dividend ratio, and $\Delta d_{t+1} = \log\Big(\frac{D_{t+1}}{D_t}\Big)$ is the log dividend growth rate.

---
# Campbell-Shiller decomposition
Apply a first order Taylor expansion to the last term

$$
\log\Big(1+\frac{P_{t+1}}{D_{t+1}}\Big) \approx \kappa_0 + \kappa_1 pd_{t+1}
$$

where

$$
\kappa_1 = \frac{e^{\bar{pd}}}{1+e^{\bar{pd}}}
$$
and
$$
\kappa_0 = \log(1+e^{bar{pd}}) - \kappa_1 \bar{pd}
$$
We can approximate returns as
$$
r_{t+1} \approx \kappa_0 + \Delta d_{t+1} + \kappa_1 pd_{t+1} - pd_t
$$

---
# Campbell-Shiller decomposition (Cont.)
Iterate forward

$$
pd_t = \frac{\kappa_0}{1-\kappa_1} + \sum_{j=0}^{\infty} \kappa_1^j \Delta d_{t+j} - \sum_{j=0}^{\infty} \kappa_1^j r_{t+j}
$$

And the transversality condition
$$
\lim_{j\to\infty} \kappa_1^j \mathbb{E}[pd_{t+j}] = 0
$$

Note: You can use that transversality condition to test for bubbles. Giglio, Maggiori
and Stroebel (2016) use this approach to test for bubbles over 700 years of data in the
UK

---
# Present Value Relation

The equation holds ex-post as well as ex ante. 

$$
pd_t = \frac{\kappa_0}{1-\kappa_1} + \underbrace{\mathbb{E}_t \sum_{j=0}^{\infty} \kappa_1^j \Delta d_{t+j}}_{\Delta d_t^H} - \underbrace{\mathbb{E}_t\sum_{j=0}^{\infty} \kappa_1^j r_{t+j}}_{ r_t^H}
$$

- Movements in prices can be attributed to fluctuations in exected growth rates, expected returns or both. 

---
# Present-value relation (variances)

$$
Var(pd_t)=Var(\Delta d_t^H) + Var( r_t^H) - 2Cov(\Delta d_t^H,  r_t^H)
$$

Expected discounted future dividend growth rates or returns have to be volatile or they
have to be negatively correlated if prices are to be volatile.

- Shiller (1981) provides the first evidence that prices appear to move more than
what is implied by expected dividends, even realized dividends. This is the
celebrated excess volatility puzzle.


---
# Present-value relation (covariances)

$$
\begin{align*}
Var(pd_t) &= Cov(\Delta d_t^H-r_t^H, pd_t) \\
&= Cov(\Delta d_t^H, pd_t) - Cov(r_t^H, pd_t) \\
1 &=Cov(\Delta d_t^H-r_t^H, pd_t) \\
&= \frac{Cov(\Delta d_t^H, pd_t)}{Var(pd_t)} - \frac{Cov(r_t^H, pd_t)}{Var(pd_t)}
\end{align*}
$$

- First term is the slope of a regression predicting future dividend growth rates with the price-dividend ratio.
- Second term is the slope of a regression predicting future returns with the price-dividend ratio.
- he sum of both slopes has to be equal to one. The dog that did not bark (Lettau
and Van Nieuwerburgh, 2008 and Cochrane, 2008)

---
# Empirical Evidence

- Typical empirical framework ($pd_t = -dp_t$)

$$
\begin{align*}
\Delta d_{t+1}= a_d + \kappa_d dp_t + \epsilon_{d, t+1} \\
r_{t+1} = a_r + \kappa_r dp_t + \epsilon_{r,t+1} \\
dp_{t+1} = a_p \phi dp_t + \epsilon_{p,t+1}
\end{align*}
$$

---
# Coefficient Restrictions

We know that approximately

$$
\begin{align*}
r_{t+1} = \kappa_0 + \Delta d_{t+1} - \kappa_1 dp_{t+1} + dp_t \\
r_{t+1} = \kappa_0 + \Delta d_{t+1} - \kappa_1(a_p \phi dp_t + \epsilon_{p,t+1}) + dp_t \\
r_{t+1}-\Delta d_{t+1} = (1-\phi \kappa_1) dp_t + \kappa_0 - \kappa_1(a_p + \epsilon_{p,t+1}) \\
Cov(r_{t+1}, (1-\phi \kappa_1) dp_t) - Cov(\Delta d_{t+1}, (1-\phi \kappa_1) dp_t) = (1-\phi \kappa_1)^2 Var(dp_t)
\end{align*}
$$
The present value relation implies a coefficient restriction of the form
$$
\kappa_r - \kappa_d = (1-\phi \kappa_1)
$$

Why is it different from one?