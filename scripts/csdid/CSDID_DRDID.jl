module CSDID_DRDID

using Statistics
using StatsFuns  # for logistic()
# optionally: using DataFrames, etc., if you want a DataFrame-based API

"""
In Stata, the function `_xtreg_chk_cl2' ensures that panel IDs are nested
within a cluster variable.  It's a data-validation check.  In Julia, we'd just
check by a groupby operation or skip entirely.
"""
function check_nested_clusters(ivar::Vector{Int}, clvar::Vector{Int})
    # This is a stub equivalent to _xtreg_chk_cl2
    # In Stata: it sorts by cluster, checks if the same panel appears in
    # multiple clusters.  We can do that check if needed.
    return
end


"""
In Stata, `_coef_table_header', `_coef_table', `_get_diopts' control how
results are displayed in the console. In Julia, you typically just return
numbers, so we omit that UI logic.  This is a stub.
"""
function stub_ui_code()
    # No operation
end


"""
Similarly `_het_did_gmm' sets up GMM calls for more general usage. In Julia,
we typically do direct matrix or function calls.  So we omit it or treat it
as a stub.
"""
function stub_gmm_code()
    # No operation
end

# -------------------------------------------------------------------------
#  The main DR DiD logic in `drdid.ado` and `csdid.ado` is below
# -------------------------------------------------------------------------

"""
    ipw_abadie_panel(dy, psxb, treat, w)

Implements the panel version of Abadie's (2005) IPW DiD.  This corresponds
to the `ipw_abadie_panel()` Mata function in `drdid.ado`.
- `dy`   = Y_{i,t1} - Y_{i,t0} for each panel unit i
- `psxb` = logistic score's linear predictor, so that pscore = logistic(psxb[i])
- `treat`= {0 or 1}, whether unit is treated or not
- `w`    = sampling weights (or just fill with 1.0 if none)
Returns `(att, infl)`, the average treatment effect plus influence function.
"""
function ipw_abadie_panel(
    dy::Vector{Float64},
    psxb::Vector{Float64},
    treat::Vector{Float64},
    w   ::Vector{Float64}
)::Tuple{Float64,Vector{Float64}}
    n = length(dy)
    @assert length(psxb) == n && length(treat) == n && length(w) == n

    # logistic of psxb => pscore
    psc = logistic.(psxb)

    # Weighted sums
    w_1 = similar(w)
    w_0 = similar(w)
    s1, s0 = 0.0, 0.0
    for i in 1:n
        w_1[i] = w[i]*treat[i]
        s1    += w_1[i]
        w_0[i] = w[i]*psc[i]*(1.0 - treat[i]) / (1.0 - psc[i] + 1e-14)
        s0    += w_0[i]
    end
    # normalize so they sum to 1
    for i in 1:n
        w_1[i] /= (s1 + 1e-14)
        w_0[i] /= (s0 + 1e-14)
    end

    # The IPW DiD ATT = mean( (w_1 - w_0).*dy )
    att = sum((w_1 .- w_0) .* dy)
    # Influence function
    infl = similar(dy)
    for i in 1:n
        infl[i] = (w_1[i] - w_0[i])*dy[i] - att
    end
    return att, infl
end


"""
    drdid_panel(dy, xb, psxb, treat, w)

Doubly Robust DiD for panel data: regression + IPW (the function `drdid_panel()`
in `drdid.ado`).  `dy[i]` = Y_{i,t1} - Y_{i,t0}, `xb[i]` = predicted (OLS) difference
for the control group, `psxb[i]` => logistic => pscore, etc.
"""
function drdid_panel(
    dy   ::Vector{Float64},
    xb   ::Vector{Float64},   # outcome-regression fitted values on the control group
    psxb ::Vector{Float64},   # logistic predictor => pscore
    treat::Vector{Float64},
    w    ::Vector{Float64}
)::Tuple{Float64,Vector{Float64}}
    n = length(dy)
    @assert length(xb) == n && length(psxb) == n
    @assert length(treat) == n && length(w) == n

    psc = logistic.(psxb)

    # stabilized IPW
    w_1 = similar(w)
    w_0 = similar(w)
    s1, s0 = 0.0, 0.0
    for i in 1:n
        w_1[i] = w[i]*treat[i]
        s1    += w_1[i]
        w_0[i] = w[i]*psc[i]*(1.0 - treat[i])/(1.0 - psc[i] + 1e-14)
        s0    += w_0[i]
    end
    for i in 1:n
        w_1[i] /= (s1+1e-14)
        w_0[i] /= (s0+1e-14)
    end

    # DR moment is (dy - xb). So ATT = mean( (w_1 - w_0)*(dy - xb) ).
    z = similar(dy)
    for i in 1:n
        z[i] = dy[i] - xb[i]
    end
    att = sum((w_1 .- w_0) .* z)
    infl = Vector{Float64}(undef, n)
    for i in 1:n
        infl[i] = (w_1[i] - w_0[i])*z[i] - att
    end
    return att, infl
end


"""
    ipw_abadie_rc(y, tmt, treat, psxb, w)

This matches the repeated-cross-section version of Abadie IPW 2x2 DiD
(`ipw_abadie_rc` in `drdid.ado`).
- y    = outcome
- tmt  = time indicator {0,1}
- treat= treat indicator {0,1}
- psxb => logistic => pscore
- w    = sampling weights
Returns `(att, infl)`.
"""
function ipw_abadie_rc(
    y::Vector{Float64},
    tmt::Vector{Float64},
    treat::Vector{Float64},
    psxb::Vector{Float64},
    w::Vector{Float64}
)::Tuple{Float64,Vector{Float64}}
    n = length(y)
    @assert length(tmt) == n && length(treat) == n
    @assert length(psxb) == n && length(w) == n

    psc = logistic.(psxb)

    # Four subgroups: (D=1,t=0), (D=1,t=1), (D=0,t=0), (D=0,t=1) with IPW for the controls
    w10 = Vector{Float64}(undef, n)  # D=1, t=0
    w11 = Vector{Float64}(undef, n)  # D=1, t=1
    w00 = Vector{Float64}(undef, n)  # D=0, t=0
    w01 = Vector{Float64}(undef, n)  # D=0, t=1

    s10=s11=s00=s01=0.0
    for i in 1:n
        if treat[i]==1.0 && tmt[i]==0.0
            w10[i] = w[i]
            s10   += w10[i]
        else
            w10[i] = 0.0
        end
        if treat[i]==1.0 && tmt[i]==1.0
            w11[i] = w[i]
            s11   += w11[i]
        else
            w11[i] = 0.0
        end
        if treat[i]==0.0 && tmt[i]==0.0
            w00[i] = w[i]*psc[i]/(1.0 - psc[i] + 1e-14)
            s00   += w00[i]
        else
            w00[i] = 0.0
        end
        if treat[i]==0.0 && tmt[i]==1.0
            w01[i] = w[i]*psc[i]/(1.0 - psc[i] + 1e-14)
            s01   += w01[i]
        else
            w01[i] = 0.0
        end
    end
    for i in 1:n
        if s10 > 0 w10[i] /= s10 end
        if s11 > 0 w11[i] /= s11 end
        if s00 > 0 w00[i] /= s00 end
        if s01 > 0 w01[i] /= s01 end
    end
    # group means
    mean10 = sum(w10[i]*y[i] for i in 1:n)
    mean11 = sum(w11[i]*y[i] for i in 1:n)
    mean00 = sum(w00[i]*y[i] for i in 1:n)
    mean01 = sum(w01[i]*y[i] for i in 1:n)

    # DiD => (mean11 - mean10) - (mean01 - mean00)
    att = (mean11 - mean10) - (mean01 - mean00)

    # Influence function
    infl = Vector{Float64}(undef, n)
    for i in 1:n
        infl[i] = (w11[i]*y[i] - mean11) -
                  (w10[i]*y[i] - mean10) -
                  (w01[i]*y[i] - mean01) +
                  (w00[i]*y[i] - mean00)
        # That sums to att over i
        infl[i] = infl[i]
    end

    return att, infl
end

# In a real system you might define cluster-robust or wild bootstrap routines
# here.  In Stata, `_coef_table`, `_het_did_gmm`, etc. do the final table
# printing or GMM aggregator.

end  # module CSDID_DRDID
