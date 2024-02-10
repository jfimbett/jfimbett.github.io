# Estimating asset pricing models via OLS and GLS
#%%
import pandas as pd 
import numpy as np
import pandas_datareader as pdr
import statsmodels.api as sm
# retrieve data, capm, FF3F, FF5F, Mom and testing portfolios

pdr.famafrench.get_available_datasets()

#%%
# industry portfolios
# '49_Industry_Portfolios'
df_10 = pdr.famafrench.FamaFrenchReader('10_Industry_Portfolios', start='1926-07', end='2020-12').read()[0]

#%%
# factors
# 'F-F_Research_Data_5_Factors_2x3'
df_5 = pdr.famafrench.FamaFrenchReader('F-F_Research_Data_5_Factors_2x3', start='1926-07', end='2020-12').read()[0]

# momentum factor
# 'F-F_Momentum_Factor'
df_mom = pdr.famafrench.FamaFrenchReader('F-F_Momentum_Factor', start='1926-07', end='2020-12').read()[0]


assets = df_10.columns
factors = list(df_5.columns) + list(df_mom.columns)
# remove RF
factors.remove('RF')
# trim spaces
factors = [x.strip() for x in factors]
assets = [x.strip() for x in assets]
# merge them all on index
df = pd.merge(df_10, df_5, on='Date')
df = pd.merge(df, df_mom, on='Date')
df.head()

# trim spaces in column names
df.columns = df.columns.str.strip()
# compute excess returns
for asset in assets:
    df[asset] = df[asset] - df['RF']
# remove RF
df = df.drop(columns=['RF'])

# average excess returns
ER = df[assets].mean()

#%%
# compute betas wrt to all factors
betas = np.zeros((len(assets), len(factors)))
a = np.zeros(len(assets))
# residuals
residuals = np.zeros((len(assets), len(df)))
for i, asset in enumerate(assets):

    # do also ts with OLS to store residuals and constants
    model = sm.OLS(df[asset], sm.add_constant(df[factors]))
    betas[i,:] = model.fit().params[1:]
    a[i] = model.fit().params[0]
    residuals[i,:] = model.fit().resid

Sigma_e = np.cov(residuals)


# OLS estimation, first using library for estimation

# no constant
# fit
# name the variables
b = pd.DataFrame(betas, columns=factors)
b.index = assets
model = sm.OLS(ER, b)
# rename the columns
model = model.fit()
# print results, recall that it assumes homoskedasticity
print(model.summary())

#%%
# let's try to recover the point estimates
# and compute proper s.e. 
from numpy.linalg import inv
lambda_model = model.params
# name the column
lambda_ols = inv(betas.T @ betas) @ betas.T @ ER
# print results
for i, factor in enumerate(factors):
    print(f"Price of risk of {factor}: {lambda_model[i]:.4f} vs {lambda_ols[i]:.4f}")

#%%
# Standard error assuming homoskedasticity
# compute residuals
residuals = ER - betas @ lambda_model
# compute variance
var = (1/(len(residuals) - len(factors)))*(residuals.T @ residuals)*np.eye(len(assets))
# compute covariance matrix
cov = inv(betas.T @ betas) @ betas.T @ var @ betas @ inv(betas.T @ betas)
# compute standard errors
se = np.sqrt(np.diag(cov))
se_model = model.bse
# print results comparing with library
for i, factor in enumerate(factors):
    print(f"S.E. of {factor}: {se_model[i]:.4f} vs {se[i]:.4f}")

#%%
# compute the appropriate s.e. for OLS
# Factor covariance
Sigma_f = np.cov(df[factors].T)


T = len(df)
Var_lambda = (1/T)*(Sigma_f + inv(betas.T@betas)@betas.T@Sigma_e@betas@inv(betas.T@betas))
# compute standard errors
se = np.sqrt(np.diag(Var_lambda))
# print results 
for i, factor in enumerate(factors):
    print(f"S.E. of {factor} hom vs het: {se_model[i]:.4f} vs {se[i]:.4f}")

# estimate alphas
alpha = ER - betas @ lambda_ols
# %%
# plot predicted vs actual ER
import matplotlib.pyplot as plt
PER=betas @ lambda_ols
plt.scatter(PER, ER)
plt.xlabel('Predicted')
plt.ylabel('Actual')
# names of assets

plt.plot(PER, PER, color='black')

# print vertical lines from predicted to actual
for i, asset in enumerate(assets):
    plt.plot([PER[i], PER[i]], [PER[i], ER[i]], color='red', linestyle='dashed')
plt.show()

#%% 
# GLS
model = sm.GLS(ER, b, sigma=(1/T)*(betas @ Sigma_f @ betas.T+Sigma_e))
model = model.fit()
print(model.summary())
lambdas_gls = model.params
# store se
se_gls = model.bse
# %%
# compare ols and gls

for i, factor in enumerate(factors):
    print(f"OLS vs GLS for {factor}: {lambda_ols[i]:.4f} vs {lambdas_gls[i]:.4f}")

# %%
# can we recover it?
l_gls_ = inv(betas.T@inv(betas@Sigma_f@betas.T+Sigma_e)@betas)@(betas.T@inv(betas@Sigma_f@betas.T+Sigma_e))@ER
# look that Sigma_f doesnt matter
l_gls = inv(betas.T@inv(Sigma_e)@betas)@(betas.T@inv(Sigma_e))@ER
# %%
v_l_gls = (1/T)*inv(betas.T@inv(betas@Sigma_f@betas.T+Sigma_e)@betas)
v_l_gls = (1/T)*inv(betas.T@inv(betas@Sigma_f@betas.T+Sigma_e)@betas)
# s.e. 
se_gls_ = np.sqrt(np.diag(v_l_gls))
# %%
# comapre standard errors
for i, factor in enumerate(factors):
    print(f"OLS vs GLS for {factor}: {se[i]:.4f} vs {se_gls_[i]:.4f}")
# %%
