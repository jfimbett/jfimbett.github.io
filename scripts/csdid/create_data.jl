using Random, Distributions, DataFrames, CSV

# -------------------------------------------------------------------
# Step 1: Generate random panel data
# -------------------------------------------------------------------

# Set a reproducible random seed
Random.seed!(12345)

# Choose number of units
n = 200

# We’ll have each unit observed at time=0 and time=1
df = DataFrame(
    id   = repeat(1:n, inner=2),
    time = repeat([0,1], n)
)

# Half the sample is "treated" => treat=1 for id ≤ 100
df.treat = map(i -> i <= 100 ? 1 : 0, df.id)

# For demonstration, define random noise and “true” outcomes
df.e0 = rand(Normal(0,1), 2n)
df.e1 = rand(Normal(0,1), 2n)

# Suppose Y0 = 5 + 0.5*id + e0, Y1 = 6 + 0.5*id + 2*treat + e1
df.Y0 = similar(df.e0)
df.Y1 = similar(df.e0)
for row in eachrow(df)
    row.Y0 = 5 + 0.5*row.id + row.e0
    row.Y1 = 6 + 0.5*row.id + 2*row.treat + row.e1
end

# Observed Y is Y0 when time=0, Y1 when time=1:
df.Y = map(r -> r.time==0 ? r.Y0 : r.Y1, eachrow(df))

# -------------------------------------------------------------------
# Step 2: Keep only the final columns & write out as CSV
# -------------------------------------------------------------------
select!(df, [:id, :time, :treat, :Y])   # discard intermediate columns
CSV.write("fake_panel_data.csv", df)

println("Created file: fake_panel_data.csv")
println("Preview of first 6 rows:")
show(first(df, 6))
