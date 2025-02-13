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
## Benchmark, Mehra and Prescott (1985)
Consider the classical consumption based asset pricing model with power utility and habit formation

$$
\begin{align*}
\max \mathbb{E}_0 \sum_{t=0}^{\infty} \beta^t \frac{C_t^{1-\gamma}}{1-\gamma} \\
\text{s.t.} \quad C_t + A_{t+1} = R_t A_t + Y_t
\end{align*}
$$
where $Y_t$ is the endowment process, $R_t$ is the return on the risky asset, and $A_t$ is the asset holdings. The pricing condition is

$$
\begin{align*}
\mathbb{E}_t[M_{t+1} R_{t+1}] = 1
\end{align*}
$$
where $M_{t+1} = \beta \Big(\frac{C_{t+1}}{C_t}\Big)^{-\gamma}$ is the stochastic discount factor.

---
## Benchmark, Mehra and Prescott (1985) continued

- How would you estimate this model with real data (regardless of the methodology)? 

- One option: Log-linearize the model. 

A log-linearized version of the model is
$$
m_{t+1} = \log \beta - \gamma \Delta c_{t+1} 
$$
if a variable has a lognormal distribution, then
$$
\begin{align*}
\log \mathbb{E}[X] = \mathbb{E}[\log X] + \frac{1}{2} \text{Var}[\log X]
\end{align*}
$$

---
## continued

Using the fundamental asset pricing equation
$$
\begin{align*}
1&=\mathbb{E}_t[M_{t+1}R_{t+1}] \\
0 &= \mathbb{E}_t \log(M_{t+1}R_{t+1} ) + \frac{1}{2} \text{Var}_t[\log(M_{t+1}R_{t+1})] \\
0 &=\mathbb{E}_t m_{t+1} + \mathbb{E}_t r_{t+1} + \frac{1}{2} \text{Var}_t[m_{t+1} + r_{t+1}] \\
0 &= \mathbb{E}_t m_{t+1} + \mathbb{E}_t r_{t+1} + \frac{\sigma^2_m}{2} + \frac{\sigma^2_r}{2} + \sigma_{rm} \\
0 &= \log \beta - \gamma \Delta \mathbb{E}_t c_{t+1}  + \mathbb{E}_t r_{t+1} + \frac{\gamma^2 \sigma_c^2}{2} + \frac{\sigma^2_r}{2} - \gamma \sigma_{rc} \\
\end{align*}
$$

---
## Predictions

$$
\begin{align*}
\mathbb{E}_t r_{t+1} &= -\log \beta + \gamma \Delta \mathbb{E}_t c_{t+1} - \frac{\gamma^2 \sigma_c^2}{2} - \frac{\sigma^2_r}{2} + \gamma \sigma_{rc} \\
r_{f,t+1} &= -\log \beta + \gamma \Delta \mathbb{E}_t c_{t+1} - \frac{\gamma^2 \sigma_c^2}{2}  \\
\mathbb{E}_t [r_{t+1} - r_{f,t+1}] &= \gamma \sigma_{rc} - \frac{\sigma^2_r}{2}  \\
\end{align*}
$$

The whole Equity Premium Puzzle is about the last equation. We need an unrealistic $\gamma$ to match the data. Consumption growth does not covary that much with returns. 


---
## The risk-free puzzle (risk free rates in the data are too low)

$$
r_{f,t+1} = -\log \beta + \gamma \Delta \mathbb{E}_t c_{t+1} - \frac{\gamma^2 \sigma_c^2}{2}
$$
When estimating this model in the data, we find that that investors should have a very low risk aversion and a large $\beta$. Totally the opposite of the conclusion of the equity risk premium puzzle.

---

## Solving the puzzles

- The equity premium puzzle has many different ***solutions***, including habit formation, long-run risk, rare disasters, measurement error, etc.
- The first attempt to solve the risk-free puzzle was to think about Habit. 

---
## Abel 1990

$$
u(C_t, C_{t-1}) = \frac{(C_t/X_t)^{1-\gamma}}{1-\gamma} 
$$
where $X_t=C_{t-1}^\kappa$ is the consumption Habit. 
$$
\begin{align*}
M_{t+1}&= \beta \Big(\frac{C_t}{C_{t-1}}\Big)^{\kappa (\gamma-1)}\Big(\frac{C_{t+1}}{C_t} \Big)^{-\gamma} \\
m_{t+1} &= \log \beta + \kappa (\gamma-1) \Delta c_t- \gamma \Delta c_{t+1} \\
\end{align*}
$$

---
## The extra parameter lets us match the level of the risk free rate better

$$
\begin{align*}
r_{f,t+1} &= -\log \beta - \underbrace{\kappa(\gamma-1) \Delta c_t}_\text{Extra term}  + \gamma \Delta \mathbb{E}_t c_{t+1} - \frac{\gamma^2 \sigma_c^2}{2} 
\end{align*}
$$

Can it help us resolve the equity premium puzzle?

---
# Applying GMM to estimate the model


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

**This is Problem Set 3 due March 23 the day before the exam (groups of max 2)** 