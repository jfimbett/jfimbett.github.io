---
marp: true
header: 'Investment Funds Risks'
footer: 'Juan F. Imbet *Ph.D.*'
paginate: true
---

# Investment Funds Risks

## University of Luxembourg

## Juan F. Imbet *Ph.D.*

---

## About Me

- Assistant Professor of Finance at Paris Dauphine University - Paris Sciences et Lettres. 
- Ph.D. in Finance from Pompeu Fabra Universit and the Barcelona School of Economics.
- External Member of the Institute for Advanced Studies in Luxembourg.
- Researcher in Financial Economics and Asset Management.
- Instructor of courses on Data Science and Finance (Python). 
- juan.imbet@dauphine.psl.eu

---

## Outline

- 25/11/2024:  Active Investment
- 26/11/2024: Equity Strategies
- 27/11/2024: Asset Allocation and Macro Strategies
- 29/11/2024: Arbitrage Strategies

---

## References

- Pedersen L. H. (2019). Efficiently Inefficient: How Smart Money Invests and Market Prices Are Determined. Princeton University Press.

## Requirements

- Statistics: Confidence intervals, t-tests, regressions.
- Asset Pricing: CAPM, Fama-French 3-factor model.
- Any programming language (Python, R, Matlab).
- Basic Finance: Risk, Return, Portfolio Theory.



---

# Part 1: Active Investment

---
## Understanding Hedge Funds 

---

## Introduction

- There are many types of active investors. Some of them are classified as **Hedge Funds**
- Hedge funds are investment pools that are relatively unconstrained in what they do. 
- They are relatively unregulated (for now), charge very high fees, and will not necessarily give you your money back when you want it. 
- They are supposed to make money all the time, and when they fail at this, their investors tend to redeem. 
- They are generally run for rich people by rich people. (e.g. clients in Geneva and run in Greenwhich Connecticut).

---
## Hedge Funds vs Mutual Funds

- Hedge funds have a lot of freedome in the trading that they do, as well as limited requirements. 
- In exchange for this freedome they are restricted in how they can raise money. 
- In terms of freedom, hedge funds can use levearge, short-selling, derivatives, and incentive fees. 
- Hedge fund investor smust be accredited investors (they need to be rich).
- The first formal hedge fund is believed to have been a fund created by Alfred Winslow Jones in 1949.  
- In the 1990s the hedge fund industry sa a dramatically increased interest as institutional investors began to embrace hedge funds. 
---
## Objectives and Fees

- The objective of asset managers is to add value tot heir investors by making money relative to a becnhmark.
- Mutual funds typically have a market index as a benchmark.
- Hedge funds are not trying to beat the stock market but, ather, trying to make money in any environment.
- This is where the **Hedge** term comes from.
- E.g. hedge fund investors would normally punish a hedge fund which is down by 10% even if the stock market is down by 20%.

---
## Objectives and Fees

- While fees vary greatly across funds, the classic hedge fund fee structure has been "2 and 20". A 2% management fee paid regardless of returns, and a 20% performance fee. 
- A hedge fund's performance fee is often subject to a high-water mark, which means that the fund must make up for losses before it can collect a performance fee.
- This means that it normally only collects profits when it reaches a new high in terms of the value of the fund.

---
## Performance

- A number of famous hedge fund managers have produced spectacular returns over the years. But hese managers do not represent the typical hedge fund. Are they good or just lucky?
- This question is very hard to answer fr several reasons. First, the data on hedge fund returns are rather poor as they are avaiable only over a limited tiem period and subject to important **biases**, 
- Hedge funds report their returns to promote themselves in many cases. 
- When they decide to start reporting information to data providers, the information is backfilled. This means that they might only decide to report their returns when they have a good track record.

---

## Organization of Hedge Funds

Hedge funds are contractually organized in different ways, but the typical **master-feeder** structure (in the US, but in many cases also in Europe) is as follows:

---
## Explanation

- The structure is not as complicated as it looks. 
- Contractually there is a distinction between the *fund*, where the money is, and the *management company*, where the traaders and other staff are.
- An investor in a hedge fund invests in a *feeder fund*, whose sole purpose in life is to invest in the *master fund* where the trading is done.
- This structure is useful since it allows the manager to focus on running a single master fund while at the same time creating different investment products (the feeder funds) for different types of investors.
- Typically US investors prefer a feeder func that is registered in the US, while non residents prefer an offshore feeder fund.
- These offshore funds are typically domiciled in the Cayman Islands.
- For different currencies, there can be different feeder funds each one hedged to the currency of the investor.

---
## Explanation
- This feeder/master structure is also useful for risk management. If the master fund has a volatility of 20%, the feeder fund can have half the volatility by investing half the money in the master fund and the other half in money market funds.
- The master fund has a poopl of money, and this is where all the trades are carried out. 
- The fund has an Investment Management Agreement (IMA) with the management company. The MC provides investment services, including strategy development, implementation, and trading. This is where all the employees work. 
- The master fund is typically organized as a partnership, where the feeder funds are the limited partners, and the general partner is the company that owns the management company. (E.g. JP Morgan Chase and Jp Morgan Chase Investment Management).

---
### Explanation

- The hedge fund also contracts with agents who handle trading, custody, clearing, and other services.
- For exchange-traded instruments, the hedge fund will typically have a prime broker who will provide leverage, short-selling, and other services.

Some nomenclature:
- NYSE: New York Stock Exchange
- CME: Chicago Mercantile Exchange
- DTCC: Depository Trust & Clearing Corporation
- OCC: Options Clearing Corporation

---
## Hedge Funds' Role in the Economy

- Hedge funds often face criticism in the media. 
- Companies do not like to see their shares shorted, since this indicates a belief that the company's share price could go down. 
- Short sellers, including hedge funds, are sometimes accused of being the source of a company's problem. 
- However, hedge funds play several useful rols in the economy. 
- They make markets more efficient by collecting information.
- They also provide diversification to accredited investors.  

---

## Evaluating Trading Strategies
### Performance Measures

---
## Alpha and Beta

- The most basic measure of trading performance is, ofcourse, the return $R_t$ in a period $t$. The return is often separated into itrs alpha and beta (abussing notation a bit). Beta is the strategy's market exposure, while alpha is the excess return after accounring for performance due to market movements. 
- Defining the excess return on top of the risk free rate $R^e_t=R_t-R^f$
$$
R^e_t=\alpha+\beta R^{me}_t+\epsilon_t
$$
-where $R^{me}_t$ is the market excess return and $\epsilon_t$ is the residual return.
- Here beta measures the strategy's tendency to follow the market. While $\epsilon_t$ measures the idiosyncratic return. 
- The idiosyncratic return can be positive or negative but in average is zero. 

---
## Alpha and Beta

- Knowing a strategy's beta is useful for many reasons. 
- If you want to mix a hedge fund with another investment, the beta risk is not diversified away while idiosyncratic risk is.
- Furthermore, market exposure ("beta risk") is easy to obtain at very low fees, for example, by buying index funds. *You should not be paying large fees for beta risk*.
- Many hedge funds are ( or claim to be) market neutral. This means that their performance is independent of what happens in the market (i.e. $\beta=0$).
- Another use of beta is that it tells us how to make a strategy market neutral. If a strategy has a beta of 2, we can make it market neutral by shorting twice the market.
$$
\text{market-neutral excess return}=\alpha+\epsilon_t
$$
$$
\mathbb{E}[\text{market-neutral excess return}]=\alpha
$$

---
## Alpha and Beta

- Alpha is cleariest the sexiest term in the regression. 
- It is the Holy Grail all active managers seek. 
- A hedge-fund's quest for alpha *defies* the Capital Asset Pricing Model (CAPM), since they would be compensated for risk that is not systematic.
- A hedge fund's alpha and beta are estiamted with significant error. Hencem if a hedge fund has an estimated alpha of 6%, how do we know if this is luck or skill?
- Researches often look at the t-statistic. 
- We can also compute a strategy's excess return above and beyond several risk exposures, e.g. the Fama-French 3-factor model.
$$
R^e_t=\alpha+\beta R^{me}_t+\beta^{smb} R^{smb}_t+\beta^{hml} R^{hml}_t+\epsilon_t
$$

---
## Risk-reward ratios

- As we have seen, a positive alpha is good while a negative alpha is bad. 
- However, is a high positive alpha always better then a low positive alpha? Not always. 
- The alpha tells youthe size of the market-neutral returns that a strategy delivers, it does not say at what risk. 
- Second, alpha depends on how a strategy  is scaled. For instance, a stice-leveraged strategy has twice the alpha of an unlevered version. 
- Risk-reqard ratios resolve these issues. At a basic level, potential investors in a hedge fund want to know how the future expected excess returns compare to the risk that the hedge fund is taking. 
- The Sharpe Ratio (SR) is a measure of just that (some people call it the risk adjusted return, but again this is a misnomer).

---
## Sharpe Ratio

$$
SR=\frac{\mathbb{E}[R^e_t]}{\sigma(R^e_t)}
$$

---
## The Information Ratio

- The SR gives the hedge fund credit for all excess returns,but we learned that some of these excess returns are due to market exposure.
- The IR addresses this by focusing on the risk-adjusted *abnormal* return, or just the risk-adjusted alpha
$$
IR=\frac{\mathbb{E}[\alpha]}{\sigma(\epsilon)}
$$

- If the hedge fund has a benchmark which is not the market, the IR is computed with respect to this benchmark.

---
## You can't eat alpha

- Suppose, for instance, that a hedge fund beats the risk-free rate by 3% at a tiny risk of 2% with a great SR of 1.5. Some investors might say, "Well, it's still just 3%. I was hoping for more return". 
- Whether this is a fair criticism or not depends on several things. In particular if the low risk is long-term or show-term. 
- If we suppose the risk is really that low, you can apply leverage to the strategy to achieve higher return and risk. 

---
## alpha-to-margin (AM) ratio

$$
AM = \frac{\alpha}{\text{margin}}
$$

- The idea behind is to compute the return on a *maximally leveraged" version of a amrket neutral strategy. 
- While hedge funds can apply leverage to any strategey, there is a maximum amount of leverage that depends on their margin requirements (more on this later). The maximum leverage is therefore 1/margin.
- There is a close relationship beween the AM ratio and the IR
$$
AM = IR \times \frac{\sigma(\epsilon)}{\text{margin}}

$$

---
## Time horizons (annualization)

- THe horizon we use to compute performance/risk measures matters.
- Some of them can be annualized easily (assuming 252 trading days)
$$
E[R^e_{\text{annualized}}]=252 \times E[R^e_{\text{daily}}]
$$
$$
\sigma(R^e_{\text{annualized}})=\sqrt{252} \times \sigma(R^e_{\text{daily}})
$$
$$
SR_{\text{annualized}}=\sqrt{252} \times SR_{\text{daily}}
$$

---
## Strategies seem riskier the higher the frequency

- Consider estimating the probability of having negative excess returns. Assume excess returns follow a normal distribution (not always realistic), call $z$ the standard normal distribution
$$
Pr(R^e<0)=Pr(E[R^e]+\sigma z<0)=Pr(z<-SR)
$$

- A high frequency trader can observe very frequent losses even on a highly profitable strategy. 

---

## High Water Mark 

- The highest price (cumulative return) achieved in the past 

$$
HWM_t = \max_{s\leq t} P_s
$$

## Drawdown

$$
DD_t = \frac{HWM_t - P_t}{HWM_t}
$$

## Maximum Drawdown

$$
MDD_T = \max_{t \leq T} DD_t
$$

---
## Adjusting for Stale Prices

- Hedge funds' investments are often illiquid, and their prices are not always available.
- How would you compute a beta if data is not available at every frequency?

$$
R_t^e = \alpha^\text{adjusted} + \beta_0 R^{me}_t + \beta_1 R^{me}_{t-1} + ... + \beta_k R^{me}_{t-k} + \epsilon_t^\text{adjusted}
$$

$$
\beta^\text{all-in} = \beta_0 + \beta_1 + ... + \beta_k
$$
- Adjust ratios accordingly.
$$
IR^\text{adjusted} = \frac{\alpha^\text{adjusted}}{\sigma(\epsilon^\text{adjusted})}
$$

---
## Finding and Backtesting Investment Strategies

---
## Good Strategies are Hard (but not impossible) to Find

- Production of information. 
- Access to information (legal vs illegal).
- Behavioral biases and limits to arbitrage.
- Compensation for liquidity. 
- Compensation for funding costs.

---
## How to backtest a strategy

- Universe
- Signals
- Trading Rules
- Time Lags 
- Portfolio Rebalancing
- Enter/Exit Rules

---
## identifying good signals. 

Consider a signal $S_t$ that predicts returns

$$
R_{t+1}^e = a+b S_t + \epsilon_{t+1}
$$

OLS estimator

$$
\hat{b} = \frac{\sum_{t=1}^T (S_t-\bar{S})R_{t+1}}{\sum_{t=1}^T (S_t-\bar{S})^2} = \sum_t x_t R_{t+1}
$$
where
$$
x_t = k \times (S_t-\bar{S})
$$
$$
k = \frac{1}{\sum_{t=1}^T (S_t-\bar{S})^2}
$$

---
## Identifying good signals

- In a time series regression the OLS estimate of the regression gives you the cumulative return of a timing strategy.
- For the strategy to be profitable, it must be positive. 
- However, it only provides evidence insample, since it assumes that the unconditional mean of the signal is known in advance.

---
## Cross sectional signals

$$
R^i_{t+1} = a + b S_t^i + \epsilon_{i, t+1}
$$
Fix a date $t$ and estimate the regression for all assets $i$ in the universe.
$$
\hat{b}_t = \frac{\sum_{i=1}^N (S_t^i-\bar{S})R_{t+1}^i}{\sum_{i=1}^N (S_t^i-\bar{S})^2} = \sum_i x_t^i R_{t+1}^i
$$
where
$$
x_t^i = k \times (S_t^i-\bar{S})
$$
$$
k = \frac{1}{\sum_{i=1}^N (S_t^i-\bar{S})^2}
$$

---
## Fama MacBeth regressions use the same concept 

$$
\hat{b} = \sum_t \hat{b}_t/T
$$
$$
\sigma(\hat{b}) = \sqrt{\sum_t (\hat{b}_t - \hat{b})^2/(T-1)}
$$

- The SR of the security selection strategy is 
$$
SR = \frac{\hat{b}}{\sigma(\hat{b})}
$$
which is related to the $t$-statistic of the cross-sectional regression.
$$
t = \sqrt{T}\frac{\hat{b}}{\sigma(\hat{b})}
$$

---

## Portfolio Management - Basics

- Consider the following static portfolio allocation problem:
  - Universe of $i \in \{1, ..., N\}$ tradeable assets with random return $r_i$.
  - Finite first and second moments: $\mathbb{E}[r_i] < \infty$, $\mathbb{E}[r_i^2] < \infty$.
  - No transaction costs or short-sell restrictions.
  - Investors maximize a utility function $U:\mathbf{R}^N \rightarrow \mathbf{R}$ dependent on moments of $r_i$ and possibly other characteristics.

---

## Example

$$
\max_\mathbf{\theta} \theta'\mu - \frac{\gamma}{2} \theta' \Sigma \theta
$$
$$
\text{Subject to } \theta'\mathbf{u} = 1
$$

where

$$
\theta = \begin{bmatrix}
\theta_1 \\
\vdots \\
\theta_N
\end{bmatrix}, \quad
\mathbf{u} = \begin{bmatrix}
1 \\
\vdots \\
1
\end{bmatrix}, \quad
\mu = \begin{bmatrix}
\mathbb{E}[r_1] \\
\vdots \\
\mathbb{E}[r_N]
\end{bmatrix}, \quad
\Sigma = \begin{bmatrix}
\sigma_1^2 & \ldots & \sigma_{1N} \\
\vdots & \ddots & \vdots \\
\sigma_{N1} & \ldots & \sigma_N^2
\end{bmatrix}.
$$

Parameter $\gamma$ captures risk aversion.

---

## Closed Form Solution

The problem allows for a closed-form solution ($\gamma > 0$):

$$
\mathcal{L} = \theta'\mu - \frac{\gamma}{2} \theta' \Sigma \theta - \lambda (\theta'\mathbf{u} - 1)
$$

$$
\mathcal{L}_\theta = \mu - \gamma \Sigma \theta - \lambda \mathbf{u} = 0 \implies \theta = \frac{1}{\gamma} \Sigma^{-1} (\mu - \lambda \mathbf{u})
$$

$$
\lambda = \frac{\mathbf{u}'\Sigma^{-1}\mu - \gamma}{\mathbf{u}'\Sigma^{-1}\mathbf{u}}
$$

$$
\theta = \frac{1}{\gamma} \Sigma^{-1} \left( \mu - \frac{\mathbf{u}'\Sigma^{-1}\mu - \gamma}{\mathbf{u}'\Sigma^{-1}\mathbf{u}} \mathbf{u} \right).
$$

---

## Is it realistic?

This simple portfolio allocation problem often fails to capture the complexity of financial markets:

- Irrelevant for asset managers using numerical methods.
- Realistic models can be solved with state-of-the-art methods and solvers.
- Bottlenecks occur when $N$ is large, as complex problems are often NP-Hard.
- Realistic problems require convex and mixed-integer formulations.
- Risk management decisions influence portfolio manager strategies.

---

## Risk Management Decision: Market Exposure

To control market risk ($\beta$):

$$
\max_\mathbf{\theta} \theta'\mu - \frac{\gamma}{2} \theta' \Sigma \theta
$$

$$
\text{Subject to } \theta'\mathbf{u} = 1, \quad \theta'\mathbf{\beta} = \bar{\beta}
$$

where $\bar{\beta} \in \mathbb{R}$ and $\mathbf{\beta} = [\beta_1, ..., \beta_N]$.

---

## Factor Exposure and Concentration

Consider a multi-factor model with $K$ factors:

$$
r_t = \mathbf{B}f_t + \epsilon_t
$$

where $\mathbf{B} \in \mathbb{R}^{N \times K}$ and $\bar{\beta} \in \mathbb{R}^K$.

$$
\max_\mathbf{\theta} \theta'\mu - \frac{\gamma}{2} \theta' \Sigma \theta
$$

$$
\text{Subject to } \theta'\mathbf{u} = 1, \quad \mathbf{B}'\theta = \bar{\beta}, \quad \bar{b} \geq \theta \geq \underline{b}.
$$

---

## Value at Risk (VaR)

VaR measures the risk of loss for an investment:

$$
VaR_\alpha(X) = -\inf\{x \in \mathbb{R} : F_X(x) > \alpha\}.
$$

For a given portfolio, time horizon, and probability $\alpha$, $\alpha$-VaR is the maximum possible loss, excluding worse outcomes with a combined probability of at most $\alpha$.

Approaches to compute $F_X$:
- Historical data
- Distribution assumptions
- Non-parametric methods

---

## Leverage

Leverage boosts investment performance at the expense of higher risk:

$$
L = \frac{\text{Total Value of Positions}}{\text{Capital}}.
$$

For a fund receiving $X$ dollars:

$$
L = \theta^+ + \theta^-
$$

where $\theta^+$ and $\theta^-$ are the fractions for long and short positions, respectively.

---

## Introducing Leverage

To model leverage with cash ($\theta_c$):

$$
\max_\mathbf{\theta} \theta'\mu - \frac{\gamma}{2} \theta' \Sigma \theta
$$

$$
\text{Subject to } \theta'\mathbf{u} + \theta_c = 1, \quad \theta = \theta^+ - \theta^-, \quad \theta^+ \geq 0, \quad \theta^- \geq 0.
$$

---

# Controlling Leverage

$$
\max_\mathbf{\theta} \theta'\mu - \frac{\gamma}{2} \theta' \Sigma \theta
$$

$$
\text{Subject to } \theta'\mathbf{u} + \theta_c = 1, \quad \mathbf{u}'(\theta^+ + \theta^-) \leq L.
$$

Arbitrage funds may use leverage up to $\times 10$, while mutual funds tend to have leverage close to $1$.

---

## Liquidity

Introducing cash allows liquidity management, essential for institutions facing withdrawals:

$$
\theta_c \geq \bar{c} \geq 0.
$$

---

# Non-Convex Non-Linear Dynamics

Real-world features requiring advanced modeling include:

- Sector concentration
- Portfolio size
- Higher moments
- Transaction costs
- Asset liquidity
- Heterogeneous preferences


