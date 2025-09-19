using CSV, DataFrames
using GLM, StatsModels  # for logistic/OLS regressions
using StatsFuns         # for logistic() in case needed

# Now you can bring the module's functions into scope:
include("CSDID_DRDID.jl")
using .CSDID_DRDID: ipw_abadie_panel, drdid_panel


# -------------------------------------------------------------------
# Step A: Load the CSV and split into time=0 vs. time=1
# -------------------------------------------------------------------
df = CSV.read("fake_panel_data.csv", DataFrame)

# df is assumed to have columns: :id, :time, :treat, :Y
# We'll make a wide-format dataset with Y0 and Y1:

df0 = filter(:time => ==(0), df)
df1 = filter(:time => ==(1), df)

# rename the outcome column in each subset
rename!(df0, :Y => :Y0)
rename!(df1, :Y => :Y1)

# Merge them on :id so each row has Y0, Y1, treat, etc.
dfpanel = innerjoin(
    select(df0, [:id, :treat, :Y0]),
    select(df1, [:id, :Y1]),
    on=:id
)


# Create ∆Y = Y1 - Y0
dfpanel.dy = dfpanel.Y1 .- dfpanel.Y0

# some random covariates
dfpanel.x = rand(Normal(0, 1), size(dfpanel, 1))
# -------------------------------------------------------------------
# Step B: Fit a logistic model (treat ~ 1) to get pscore predictor
# -------------------------------------------------------------------
# Here we have no covariates except the intercept.  In practice, you
# might include additional X.  "psxb" is the linear predictor.
# Ensure treat is binary and drop rows with missing values
dfpanel.treat = ifelse.(dfpanel.treat .== 1, 1, 0)  # Ensure binary treatment indicator
dfpanel = dropmissing(dfpanel, [:treat, :dy])       # Drop rows with missing values

logmod = glm(@formula(treat ~ x),  
             dfpanel,
             Binomial(), LogitLink())  # Specify Binomial distribution and Logit link
dfpanel.psxb = predict(logmod, dfpanel)

# We'll assume everyone has weight = 1 for simplicity
w = ones(size(dfpanel, 1))

# treat to float 
dfpanel.treat = convert(Vector{Float64}, dfpanel.treat)
# convert x to float
dfpanel.psxb = convert(Vector{Float64}, dfpanel.psxb)
# -------------------------------------------------------------------
# Step C: IPW Abadie (2005) Panel DiD
# -------------------------------------------------------------------
att_ipw, infl_ipw = ipw_abadie_panel(
    dfpanel.dy,       # ∆Y
    dfpanel.psxb,     # logit linear predictor
    dfpanel.treat,    # treat indicator
    w                 # weights
)
println("IPW Abadie(2005) Panel DiD estimate = $att_ipw")

# -------------------------------------------------------------------
# Step D: DR DiD (Sant'Anna & Zhao)
# -------------------------------------------------------------------
# We also need an OLS "outcome-regression" for ∆Y among controls.
# For simplicity, we again use only an intercept:
using GLM
ctrlmod = lm(@formula(dy ~ x),
             dfpanel[dfpanel.treat .== 0, :])  # only control group
dfpanel.xb = predict(ctrlmod, dfpanel)

# xb to float 
dfpanel.xb = convert(Vector{Float64}, dfpanel.xb)
# Now pass (dy, xb, psxb, treat, w) to drdid_panel:
att_dr, infl_dr = drdid_panel(
    dfpanel.dy,   # ∆Y
    dfpanel.xb,   # OLS fitted values among controls
    dfpanel.psxb, # logistic predictor => pscore
    dfpanel.treat,
    w
)
println("Doubly Robust DiD estimate = $att_dr")
