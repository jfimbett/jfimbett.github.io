# OLS via GMM
using Plots
using Distributions
using LinearAlgebra
using Optim
using ForwardDiff
# Generate data
N = 50
β = [1, 2]
X = [ones(N) rand(N)]
ϵ = rand(Normal(0, 1), N)
y = X * β + ϵ

# OLS
β_hat =  (X'X) \ (X'y)
var_β_hat = (X'X) \ (X' * diagm(0 => ϵ.^2) * X) / N

# GMM
g_T(β, y, X) = [mean(X'*(y - X * β)), mean(y - X * β)]

Q(β, W) = g_T(β, y, X)' * W * g_T(β, y, X)

# first stage
# W = I
β_hat_GMM1 = optimize(β -> Q(β, I), β_hat).minimizer
# in practice you stay here, but we can do a second stage
d = ForwardDiff.jacobian(β -> g_T(β, y, X), β_hat_GMM1)
var_β_hat_GMM1 = inv(d' * I * d)/N


# compute coavriance matrix
var_moments = (1/N)*(g_T(β_hat_GMM1, y, X) * g_T(β_hat_GMM1, y, X)')

# add some small number to the diagonal to make it invertible
var_moments = var_moments +  (1e-2)*rand()*I

# second stage
W = inv(var_moments)
β_hat_GMM2 = optimize(β -> Q(β, W), β_hat).minimizer


# compute coavriance matrix
# approximate partial derivative
d = ForwardDiff.jacobian(β -> g_T(β, y, X), β_hat_GMM2)

# compute var, but use a pseudo-inverse
var_β_hat_GMM2 = pinv(d' * W * d)/N

# print the results, compare ols and GMM
println("OLS1: ", β_hat[1], " ", sqrt(var_β_hat[1,1]))
println("OLS2: ", β_hat[2], " ", sqrt(var_β_hat[2,2]))
println("GMM1 first stage: ", β_hat_GMM1[1], " ", sqrt(var_β_hat_GMM1[1,1]))
println("GMM2 first stage: ", β_hat_GMM1[2], " ", sqrt(var_β_hat_GMM1[2,2]))
println("GMM1 second stage: ", β_hat_GMM2[1], " ", sqrt(var_β_hat_GMM2[1,1]))
println("GMM2 second stage: ", β_hat_GMM2[2], " ", sqrt(var_β_hat_GMM2[2,2]))



