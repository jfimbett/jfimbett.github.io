using Plots
using Parameters
using LinearAlgebra
using Random
using Distributions

@with_kw mutable struct Params
    # Model parameters
    β::Array{Float64,2} = zeros(5, 2)
    Σ::Array{Float64,2} = zeros(5, 5)
    Σ_f::Array{Float64,2} = zeros(2, 2)
    μ_f::Array{Float64,1} = zeros(2)
    a::Array{Float64,1} = zeros(5)
end

function initialize()
    β = zeros(5, 2)
    β[1,:] = [0.5, 0.0]
    β[2,:] = [0.0, 0.5]
    β[3,:] = [0.5, 0.5]
    β[4,:] = [0.3, 1.2]
    β[5,:] = [0.7, 0.4]

    Σ= zeros(5, 5)
    Σ[1,:] =  [1.0, 0.5, 0.5, 0.5, 0.5]
    Σ[2,:] =  [0.5, 1.0, 0.5, 0.0, 0.0]
    Σ[3,:] =  [0.5, 0.5, 1.0, 0.0, 0.0]
    Σ[4,:] =  [0.5, 0.0, 0.0, 1.0, 0.5]
    Σ[5,:] =  [0.5, 0.0, 0.0, 0.5, 1.0]

     # compute determinant 
     @assert det(Σ) > 0.0 "Σ must be positive definite"

     Σ_f = zeros(2,2)
     Σ_f[1,:] = [1.0, 0.5]
     Σ_f[2,:] = [0.5, 1.0]
 
 
     # compute determinant
     @assert det(Σ_f) > 0.0 "Σ_f must be positive definite"
 
     μ_f = [0.05, 0.07]
 
    return Params(β=β, Σ=Σ, Σ_f=Σ_f, μ_f=μ_f)
end

p = initialize()

function simulate(p::Params, T::Int64)
    @unpack β, Σ, Σ_f, μ_f, a = p

    # Simulate T observations of the factors
    f = rand(MvNormal(μ_f, Σ_f), T)
    ϵ = rand(MvNormal(zeros(5), Σ), T)
    # Simulate T observations of the returns
    Re = zeros(5, T)
    for t in 1:T
        Re[:,t] = a + β * f[:,t] + ϵ[:,t]
    end

    return Re, f
end

Re, f = simulate(p, 1000)
function cross_estimation(Re, p::Params)
    # compute sample means
    E_TRe = mean(Re, dims=2)
    T = size(Re, 2)
    @unpack β, Σ, Σ_f, μ_f, a = p
    # compute ols and gls
    λ_hat_ols = inv(β'*β)*β'*E_TRe
    α_hat_ols = E_TRe - β*λ_hat_ols

    Ω = (1/T)*(β*Σ_f*β' + Σ)

    λ_hat_gls = inv(β'*inv(Ω)*β)*β'*inv(Ω)*E_TRe
    α_hat_gls = E_TRe - β*λ_hat_gls

    # standard errors
    se_λ_ols = inv(β'*β)*β'*Ω*β*inv(β'*β)

    se_α_ols = (I-β*inv(β'*β)*β')*Ω*(I-β*inv(β'*β)*β')'


    # now gls se
    se_λ_gls = inv(β'*inv(Ω)*β)
    se_α_gls = (1/T)*(I-β*inv(β'*inv(Σ)*β)*β'*inv(Σ))*Σ*(I-β*inv(β'*inv(Σ)*β)*β'*inv(Σ))'
    return λ_hat_ols, α_hat_ols, se_λ_ols, se_α_ols, λ_hat_gls, α_hat_gls, se_λ_gls, se_α_gls
    
end

# function to print nicely the results
# put the se next to the estimate
function print_results(λ_hat, se_λ, α_hat, se_α)
    for i in 1:2
        println("λ$(i) = $(round(λ_hat[i], digits=3)) s.d.  $(round(sqrt(se_λ[i,i]), digits=3))")
    end
    for i in 1:5
        println("α$(i) = $(round(α_hat[i], digits=3)) s.d.  $(round(sqrt(se_α[i,i]), digits=3))")
    end
end


# distribution of the estimates
function plot_distribution(T=100, N=1000, p=initialize())

    @unpack β, Σ, Σ_f, μ_f, a = p

    λ_ols = zeros(2, N)
    λ_gls = zeros(2, N)
    α_ols = zeros(5, N)
    α_gls = zeros(5, N)

    t_ols = zeros(2, N)
    t_gls = zeros(2, N)

    tα_ols = zeros(5, N)
    tα_gls = zeros(5, N)

    for i in 1:N
        Re, f = simulate(p, T)
        λ_hat_ols, α_hat_ols, se_λ_ols, se_α_ols, λ_hat_gls, α_hat_gls, se_λ_gls, se_α_gls = cross_estimation(Re, p)
        λ_ols[:,i] = λ_hat_ols
        λ_gls[:,i] = λ_hat_gls
        α_ols[:,i] = α_hat_ols
        α_gls[:,i] = α_hat_gls

        t_ols[:,i] = (λ_hat_ols - μ_f)./sqrt.(diag(se_λ_ols))
        t_gls[:,i] = (λ_hat_gls - μ_f)./sqrt.(diag(se_λ_gls))

        tα_ols[:,i] = (α_hat_ols - a)./sqrt.(diag(se_α_ols))
        tα_gls[:,i] = (α_hat_gls - a)./sqrt.(diag(se_α_gls))

    end

    # plot histograms
    function create_histogramλ(i)
        p_1 = histogram(λ_ols[i,:], label="λ_$i ols", normalize=:pdf)
        # true value
        vline!([p.μ_f[i]], label="true value", color="black")
        # average value for each estimator
        vline!([mean(λ_ols[i,:])], label="mean ols", color="red")
        # fit normal
        px(x) = pdf(Normal(mean(λ_ols[i,:]), sqrt(var(λ_ols[i,:]))), x)
        plot!(px, label="fit ols", color="red")

        p_2 = histogram(λ_gls[i,:], label="λ_$i gls", normalize=:pdf)
        # true value
        vline!([p.μ_f[i]], label="true value", color="black")
        vline!([mean(λ_gls[i,:])], label="mean gls", color="blue")

        # fit
        px(x) = pdf(Normal(mean(λ_gls[i,:]), sqrt(var(λ_gls[i,:]))), x)
        plot!(px, label="fit gls", color="blue")

        return p_1, p_2
    end

    function create_histogramα(i)
        p_1 = histogram(α_ols[i,:], label="α_$i ols", normalize=:pdf)
        # true value
        vline!([p.a[i]], label="true value", color="black")
        # average value for each estimator
        vline!([mean(α_ols[i,:])], label="mean ols", color="red")
        p(x) = pdf(Normal(mean(α_ols[i,:]), sqrt(var(α_ols[i,:]))), x)
        plot!(p, label="fit ols", color="red")

        p_2 = histogram(α_gls[i,:], label="α_$i gls", normalize=:pdf)
        vline!([p.a[i]], label="true value", color="black")
        vline!([mean(α_gls[i,:])], label="mean gls", color="blue")

        p(x) = pdf(Normal(mean(α_gls[i,:]), sqrt(var(α_gls[i,:]))), x)
        plot!(p, label="fit gls", color="blue")

        return p_1, p_2
    end

    p1, p2 = create_histogramλ(1)
    p3, p4 = create_histogramλ(2)
    plot(p1, p2, p3, p4, layout=(2,2), legend=:topleft)

    # plot histograms for t 
    p5 = histogram(t_ols[1,:], label="t_1 ols", normalize=:pdf)
    p6 = histogram(t_gls[1,:], label="t_1 gls", normalize=:pdf)
    p7 = histogram(t_ols[2,:], label="t_2 ols", normalize=:pdf)
    p8 = histogram(t_gls[2,:], label="t_2 gls", normalize=:pdf)
    plot(p5, p6, p7, p8, layout=(2,2), legend=:topleft)

    
   
end

plot_distribution(10, 1000)