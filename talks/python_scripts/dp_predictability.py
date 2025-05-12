#%%
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# ----------------------------------------
# 1) LOAD & PREPARE SHILLER DATA
# ----------------------------------------
url = "http://www.econ.yale.edu/~shiller/data/ie_data.xls"
df = pd.read_excel(url, sheet_name="Data", skiprows=7)

# Data cleaning and preparation
df = df.iloc[:, :3].dropna()
df.columns = ["Date", "Price", "Dividend"]
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df["Dividend"] = pd.to_numeric(df["Dividend"], errors="coerce")

df = df[df["Dividend"] > 0].copy()

# Date processing
df["Year"] = df["Date"].apply(lambda x: int(np.floor(x)))
df["Month"] = df["Date"].apply(lambda x: int((x - np.floor(x))*100) + 1)
df["Date"] = pd.to_datetime(df[["Year", "Month"]].assign(day=1))
df = df.set_index("Date").sort_index()

# Financial metrics calculation
df["dp"] = np.log(df["Dividend"]) - np.log(df["Price"])
df["R"] = (df["Price"] + df["Dividend"]) / df["Price"].shift(1)
df["r"] = np.log(df["R"])  # monthly log return
df.dropna(subset=["dp", "r"], inplace=True)

# Multi-year returns calculation
for k in [1, 3, 5, 10]:
    df[f"r{k}"] = df["r"].cumsum().shift(-k*12) - df["r"].cumsum()

# compute the cumulative 3-year return, e^r3 - 1
df["r3_realized"] = np.exp(df["r3"]) - 1
dp_median = df["dp"].median()

# same for 1
df["r1_realized"] = np.exp(df["r1"]) - 1

# arg max of r1_realized
print(df["r1_realized"].idxmax())
print(df["r1_realized"].idxmin())
# histogram of 1-year realized returns, but put text on the observations of very important events, e.g. recession covid etc

# Define the events with the exact date you want to pull from the DataFrame
events = {
    'End of Great Recession (1932-06)': ('1932-06-01', 0.1, 4),
    'Patient Zero COVID': ('2019-12-01', 0.15, 2),  # Push this one lower
    'Subprime-related losses.': ('2007-12-01', 0.1, 1),
    'End of WWI': ('1918-11-01', 0.15,3)
}

# Plot the histogram

plt.figure(figsize=(12, 6))
n, bins, patches = plt.hist(df['r1_realized'], bins=50, color='skyblue', edgecolor='black', alpha=0.7)

plt.title('Sample: (S&P 500) 1870-2023', fontsize=14)
plt.xlabel('1-Year Realized Returns', fontsize=12)
plt.ylabel('Frequency', fontsize=12)

for label, (date, offset_multiplier, i) in events.items():
    
    try:
        x_pos = df.loc[date, 'r1_realized']  # Get the return for the event
        # Compute dynamic vertical offset based on the multiplier
        y_offset = -plt.ylim()[1] * offset_multiplier
        plt.annotate(
            label,
            xy=(x_pos, 0),             # Arrow lands at y=0
            xytext=(x_pos, y_offset),  # Text placed with dynamic offset
            ha='center',
            arrowprops=dict(facecolor='red', shrink=0.05, width=1, headwidth=6),
            fontsize=10,
            color='red'
        )
    except KeyError:
        print(f"Date {date} not found in your DataFrame index. Check your data!")
    
plt.tight_layout()
plt.show()

# now I want the three histograms on the same plot
bins = 100
plt.hist(df["r1_realized"], bins=bins, alpha=0.5, label="All")
plt.hist(df["r1_realized"][df["dp"] < dp_median], bins=bins, alpha=0.5, label="Low dp")
plt.hist(df["r1_realized"][df["dp"] > dp_median], bins=bins, alpha=0.5, label="High dp")
#plt.title("Histogram of 1-Year Ahead Realized Returns 1871-2023")
# make it wider
plt.gcf().set_size_inches(10, 6)
plt.legend()

# save 
plt.savefig("hi_1y.png")
plt.show()
# Filter data range
df_copy = df.copy()
#df = df["1990":"2025"]

# ----------------------------------------
# Helper Functions
# ----------------------------------------
def annual_performance(log_rets, freq=12):
    """Calculate annualized performance metrics"""
    log_rets = log_rets.dropna()
    mu_m = log_rets.mean()
    sigma_m = log_rets.std()
    
    ann_mean = freq * mu_m
    ann_vol = np.sqrt(freq) * sigma_m
    ann_sharpe = ann_mean / ann_vol if ann_vol > 0 else np.nan
    
    return ann_mean, ann_vol, ann_sharpe

def build_rolling_regression_signal(df_in, reg_window):
    """Rolling regression strategy implementation"""
    df_out = df_in.copy()
    
    col_r3hat = f"r3_hat_{reg_window}"
    col_signal = f"dp_reg_signal_{reg_window}"
    col_strat = f"dp_reg_strat_{reg_window}"
    
    df_out[col_r3hat] = np.nan
    df_out[col_signal] = np.nan
    
    for i in range(reg_window, len(df_out) - 36):
        train_slice = df_out.iloc[i - reg_window:i]
        y = train_slice["r3"]
        X = train_slice["dp"]
        
        valid_idx = y.dropna().index.intersection(X.dropna().index)
        y = y.loc[valid_idx]
        X = X.loc[valid_idx]
        
        if len(y) < 10:
            continue
            
        X_ols = sm.add_constant(X)
        model = sm.OLS(y, X_ols).fit()
        
        dp_i = df_out["dp"].iloc[i]
        if pd.isna(dp_i):
            continue
            
        X_pred = sm.add_constant(pd.Series(dp_i), has_constant="add")
        r3_hat_i = model.predict(X_pred)[0]
        
        df_out.loc[df_out.index[i], col_r3hat] = r3_hat_i
        signal_i = 1 if r3_hat_i > 0 else -1
        df_out.loc[df_out.index[i], col_signal] = signal_i
    
    df_out[col_strat] = df_out[col_signal].shift(1) * df_out["r"]
    return df_out

# ----------------------------------------
# Trading Strategies
# ----------------------------------------
# Benchmark strategy
window_r3 = 120
df["r_rolling_mean"] = df["r"].rolling(window_r3).mean()
df["benchmark_signal"] = np.where(df["r_rolling_mean"] > 0, 1, -1)
df["benchmark_strat"] = df["benchmark_signal"].shift(1) * df["r"]

# DP Rolling Mean strategy
window_mean = 120
df["dp_rolling_mean"] = df["dp"].rolling(window_mean).mean()
df["dp_rolling_signal"] = np.where(df["dp"] > df["dp_rolling_mean"], 1, -1)
df["dp_rolling_strat"] = df["dp_rolling_signal"].shift(1) * df["r"]

# Rolling Regression strategy
w = 120
df = build_rolling_regression_signal(df, w)

# ----------------------------------------
# Performance Evaluation
# ----------------------------------------
strategies = {
    "Benchmark Rolling Average": "benchmark_strat",
    "dp Rolling Mean": "dp_rolling_strat",
    f"dp Rolling Reg ({w}m)": f"dp_reg_strat_{w}"
}

perf_rows = []
for name, col in strategies.items():
    ann_mean, ann_vol, ann_sharpe = annual_performance(df[col])
    perf_rows.append([name, ann_mean, ann_vol, ann_sharpe])

perf_df = pd.DataFrame(
    perf_rows,
    columns=["Strategy", "Annual Mean", "Annual Vol", "Annual Sharpe"]
).round(2)

print("\n=== Annual Performance Comparison ===")
print(f"Sample: {df.index[0].year}-{df.index[-1].year}")
print(perf_df)

# ----------------------------------------
# Visualization
# ----------------------------------------
fig, ax1 = plt.subplots()
df["dp"].plot(ax=ax1, label="dp (left axis)")

# save the current plot as an image
# add labels 
plt.xlabel("Date")
plt.ylabel("Log Dividend-Price Ratio (dp)")
#plt.title("Dividend-Price Ratio (dp)")
# make it wider 
fig.set_size_inches(10, 6)
plt.savefig("dp_plot.png")

fig, ax1 = plt.subplots()
df["dp"].plot(ax=ax1, label="dp (left axis)")
ax2 = ax1.twinx()
df["r3"].plot(ax=ax2, color="red", label="r3 (right axis)")

ax1.set_ylabel("Log Dividend-Price Ratio (dp)", color="blue")
ax2.set_ylabel("3-Year Log Return (r3)", color="red")
#plt.title("dp vs. 3-Year Cumulative Log Returns")
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")
# save the current plot as an image
# make it wider, width 2 times height 
fig.set_size_inches(10, 5)
plt.savefig("dp_vs_r3_plot.png")

# %% 