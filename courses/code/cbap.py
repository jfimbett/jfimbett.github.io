
#%%
import pandas_datareader as pdr
import datetime
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
start = datetime.datetime(1960, 1, 1)
end = datetime.datetime(2021, 12, 31)

# Download consumption data
c = pdr.data.DataReader("PCE", "fred", start, end)
# rename index to t_month
c.index.name = "t_month"
# rename column to c
c.columns = ["c"]
# make dates end of month
c.index = c.index + pd.offsets.MonthEnd(0)

# compute the log(c_t) - log(c_t-1)
dc = np.log(c).diff().dropna()

# plot consumption growth
dc.plot()
# %%
# get market returns from French's website
m = pdr.data.DataReader("F-F_Research_Data_Factors", "famafrench", start, end)[0]
# make m.index datetime using the first day
m.index = pd.to_datetime(m.index.astype(str) + "-01", format="%Y-%m-%d")
# move them to the last day of month
m.index = m.index + pd.offsets.MonthEnd(0)
# plot Mkt-RF
m["Mkt-RF"].plot()
m["Mkt"] = m["Mkt-RF"] + m["RF"]
# %%
# compute the volatility of consumption growth
dc_std = dc.std().values[0]
# volatility of market returns (divide them by 100 to get them in percentage)
m_std = m["Mkt"].std() / 100
# compute the correlation between consumption growth and market returns
dc_m_corr = dc.corrwith(m["Mkt"]/100)
dc_m_corr = dc_m_corr.values[0]
# a lognormal consumption model with power utility implies that
# E[Mkt-RF] + 0.5*\sigma_m^2 = \gamma * \sigma_c * \sigma_m * \rho

f = lambda g : m["Mkt-RF"].mean()/100 + 0.5 * m_std**2 - g* dc_m_corr*dc_std * m_std

# find the root of f
from scipy.optimize import root
g = root(f, 0.5).x[0]
# print the result
print(f"gamma = {g:.2f}") # required coeff of risk aversion is way to large

# %%
