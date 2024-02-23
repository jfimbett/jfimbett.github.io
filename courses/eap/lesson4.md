---
marp: true
paginate: true
title: Empirical Asset Pricing
author: Juan F. Imbet Ph.D.
---

# Lesson 4: GMM in Practice 

---
# Objectives

1. Estimate a Consumption Based Asset Pricing Model using GMM 
2. Face the challenges of estimating a model in practice with real data

---
# Theory

Consider the model with power utility and habit formation (Abel 1990) seen in class

$$
\begin{align*}
M_{t+1} = \delta \Big(\frac{C_t}{C_{t-1}}\Big)^{\kappa (\gamma-1)}\Big(\frac{C_{t+1}}{C_{t}} \Big)^{-\gamma}
\end{align*}
$$
we do not need to log-linearize the model to estimate it using GMM. Let's use the pricing condition 

$$
\begin{align*}
\mathbb{E}_t[M_{t+1} R_{t+1}] = 1
\end{align*}
$$
Take expectations on both sides, and include instruments $z_t$ to get more moments. 
$$
\begin{align*}
\mathbb{E}_t[M_{t+1} R_{t+1}- 1] = 0\\
\mathbb{E}_t[M_{t+1} R_{t+1}- 1]z_t = 0\\
\mathbb{E}_t[(M_{t+1} R_{t+1}- 1)z_t] = 0 \\
\mathbb{E}[\mathbb{E}_t[(M_{t+1} R_{t+1}- 1)z_t]] = 0 \\
\mathbb{E}[(M_{t+1} R_{t+1}- 1)z_t] = 0 
\end{align*}
$$

---
# GMM 

$$
g(\theta) = \mathbb{E}[(M_{t+1}(\theta) R_{t+1}- 1)z_t] = 0
$$
E.g. 
$$
\begin{align*}
g([\gamma, \kappa, \delta]) = \mathbb{E}[\begin{pmatrix}\Big(\delta \Big(\frac{C_t}{C_{t-1}}\Big)^{\kappa (\gamma-1)}\Big(\frac{C_{t+1}}{C_{t}} \Big)^{-\gamma} R_{t+1}- 1\Big) \\ \Big(\delta \Big(\frac{C_t}{C_{t-1}}\Big)^{\kappa (\gamma-1)}\Big(\frac{C_{t+1}}{C_{t}} \Big)^{-\gamma} R_{t+1}- 1\Big) C_t \\ \Big(\delta \Big(\frac{C_t}{C_{t-1}}\Big)^{\kappa (\gamma-1)}\Big(\frac{C_{t+1}}{C_{t}} \Big)^{-\gamma} R_{t+1}- 1\Big)C_{t-1} \\ \Big(\delta \Big(\frac{C_t}{C_{t-1}}\Big)^{\kappa (\gamma-1)}\Big(\frac{C_{t+1}}{C_{t}} \Big)^{-\gamma} R_{t+1}- 1\Big)R_{t} \end{pmatrix}] = 0
\end{align*}
$$

---
# GMM continued 

$$
\begin{align*}
g_T([\gamma, \kappa, \delta]) = \frac{1}{T}\sum_{t=1}^T \begin{pmatrix}\Big(\delta \Big(\frac{C_t}{C_{t-1}}\Big)^{\kappa (\gamma-1)}\Big(\frac{C_{t+1}}{C_{t}} \Big)^{-\gamma} R_{t+1}- 1\Big) \\ \Big(\delta \Big(\frac{C_t}{C_{t-1}}\Big)^{\kappa (\gamma-1)}\Big(\frac{C_{t+1}}{C_{t}} \Big)^{-\gamma} R_{t+1}- 1\Big) C_t \\ \Big(\delta \Big(\frac{C_t}{C_{t-1}}\Big)^{\kappa (\gamma-1)}\Big(\frac{C_{t+1}}{C_{t}} \Big)^{-\gamma} R_{t+1}- 1\Big)C_{t-1} \\ \Big(\delta \Big(\frac{C_t}{C_{t-1}}\Big)^{\kappa (\gamma-1)}\Big(\frac{C_{t+1}}{C_{t}} \Big)^{-\gamma} R_{t+1}- 1\Big)R_{t} \end{pmatrix} = 0
\end{align*}
$$

---
# Data 

Use quarterly data 

- $R_t$ is the return on the US market portfolio, obtain it here from Kenneth French's website https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip returns are at a monthly frequency, so you need to compute the quarterly returns. (Compound the monthly returns to get the quarterly return). Recall that $R$ is already a gross return. 

- $C_t$ is the Real Personal Consumption Expenditures, obtain it here from FRED https://fred.stlouisfed.org/series/PCECC96. 

---

**This is Problem Set 3 due March 17 the day before the exam.** 