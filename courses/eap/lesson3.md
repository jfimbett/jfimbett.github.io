---
marp: true
paginate: true
title: Empirical Asset Pricing
author: Juan F. Imbet Ph.D.
---

# Lesson 3: GMM Estimation

---
# Introduction

- GMM stands for Generalized Method of Moments. It is a generalization of the method of moments estimator.
- It was formalized by Hansen (1982), and since has become one of the most widely used methods of estimation for models in economics and finance.
- It is the basis for methods like the Simulated Method of Moments (SMM) and the Indirect Inference (II) estimator.
- The power of GMM is that it allows us to estimate models without having to specify the distribution of the data.

---
# The method of moments estimator (Chebyshev)

- It was introduced by Pafnuty Chebyshev in 1887 in the proof of the central limit theorem.
- Suppose you need to estimate $k$ unknown parameters $\theta_1, ..., \theta_k$ that characterize the distribution of a random variable $X$. 
$$
f_X(x; \theta_1, ..., \theta_k)
$$
Now, assume that the first $k$ moments can be expressed as a function of the parameters:
$$
\begin{align*}
\mu_1 = E[X] &= g_1(\theta_1, ..., \theta_k) \\
\mu_2 = E[X^2] &= g_2(\theta_1, ..., \theta_k) \\
&\vdots \\
\mu_k = E[X^k] &= g_k(\theta_1, ..., \theta_k) \\
\end{align*}
$$

---
# The method of moments (cont.)

- Estimate the population moment with the sample moment
$$
\begin{align*}
\hat{\mu}_j &= \frac{1}{n} \sum_{i=1}^n x_i^j \\
\end{align*}
$$
- Solve the system of equations
$$
\begin{align*}
\hat{\mu}_1 &= g_1(\hat{\theta}_1, ..., \hat{\theta}_k) \\
\hat{\mu}_2 &= g_2(\hat{\theta}_1, ..., \hat{\theta}_k) \\
&\vdots \\
\hat{\mu}_k &= g_k(\hat{\theta}_1, ..., \hat{\theta}_k) \\
\end{align*}
$$

---
# Example, normal distribution

$$
\begin{align*}
\mu_1 &= E[X] = \int_{-\infty}^{\infty} x f_X(x; \mu, \sigma) dx = \\
\mu_2 &= E[X^2] = \int_{-\infty}^{\infty} x^2 f_X(x; \mu, \sigma) dx \\
\end{align*}
$$

- After observing a sample of $n$ observations $\{x_1, ..., x_n\}$, we can estimate the population moments with the sample moments
$$
\begin{align*}
\hat{\mu}_1 &= \frac{1}{n} \sum_{i=1}^n x_i \\
\hat{\mu}_2 &= \frac{1}{n} \sum_{i=1}^n x_i^2 \\
\end{align*}
$$
- And solve numerically the system of equations.


---
# GMM

- When the number of moments is equal to the number of parameters there is a unique solution to the system of equations.
- However, we cannot compute the standard errors of the estimates. For this task we need to use the GMM estimator, and include more moments. 

---
# GMM (cont.)

- Notation in Wooldride

- $w_i$ is a ($M \times 1$) i.i.d. vector of random variables for observation $i$. 
- $\theta$ is a ($P \times 1$) vector of unknown coefficients (parameters).
- $g(w_i, \theta)$ is a ($L \times 1$) vector of functions $g:\mathbb{R}^M \times \mathbb{R}^P \rightarrow \mathbb{R}^L \text{  } L \geq P$
- Function $g$ can be potentially non linear. 
- Let $\theta_0$ be the true value of $\theta$. 
- Let $\hat{\theta}$ be an estimator of $\theta$.
- The hat and naught notation is used to denote estimators and true values, respectively.

---
# Moment Restrictions

- GMM is based on the idea that the moment restrictions shouldbe zero in expectation (e.g. the difference between the sample and population moments). 
$$
\mathbb{E}[g(w_i, \theta_0)] = 0
$$
Which in the sample can be written as
$$
\frac{1}{N} \sum_{i=1}^N g(w_i, \theta) = 0
$$
We want to choose $\hat{\theta}$ such that $N^{-1} \sum_{i=1}^N g(w_i, \hat{\theta})$ is as close to zero as possible. 

---
# Criterion Function

- If we have more moments than parameters there might not be a solution to the system of equations, but we can make those moments as close to zero as possible.
- Hint, minimize a weighted sum of squared moments. 
- How much importance you give to each moment will be discussed later. 
- The estimator $\hat{\theta}$ uses the following function (criterion) as a function to minimize. 
$$
Q_N(\theta) = \Big[N^{-1}\sum_{i=1}^N g(w_i, \theta)\Big]' \hat{W} \Big[N^{-1}\sum_{i=1}^N g(w_i, \theta)\Big]
$$
where $\hat{W}$ is a positive definite weighting matrix that converges in probbaility to $W_0$. 

---
# Asymptotic Properties

*Hansen (1982) Large Sample Properties of Generalized Method of Moments*,
**Econometrica**. Two-stage procedure, for any positive semidefined matrix $W$ e.g. $I$. 

$$
\begin{align*}

\hat{\theta} &= \arg \min_{\theta} \Big[ g_T( \theta)\Big]' \hat{W} \Big[ g_T( \theta)\Big] \\
\end{align*}
$$
FOC
$$
\begin{align*}
\frac{\partial g_T(\theta)}{\partial \theta}W g_T(\theta)=0
\end{align*}
$$