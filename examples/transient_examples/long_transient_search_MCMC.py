#!/usr/bin/env python

import pyfstat

F0 = 30.0
F1 = -1e-10
F2 = 0
Alpha = 0.5
Delta = 1

minStartTime = 1000000000
maxStartTime = minStartTime + 200 * 86400
Tspan = maxStartTime - minStartTime
tref = minStartTime

DeltaF0 = 6e-7
DeltaF1 = 1e-13

theta_prior = {
    "F0": {"type": "unif", "lower": F0 - DeltaF0 / 2.0, "upper": F0 + DeltaF0 / 2.0},
    "F1": {"type": "unif", "lower": F1 - DeltaF1 / 2.0, "upper": F1 + DeltaF1 / 2.0},
    "F2": F2,
    "Alpha": Alpha,
    "Delta": Delta,
    "transient_tstart": minStartTime,
    "transient_duration": {
        "type": "halfnorm",
        "loc": 0.001 * Tspan,
        "scale": 0.5 * Tspan,
    },
}

ntemps = 2
log10beta_min = -1
nwalkers = 100
nsteps = [100, 100]

mcmc = pyfstat.MCMCTransientSearch(
    label="transient_search",
    outdir="data_l",
    sftfilepattern="data_l/*simulated_transient_signal*sft",
    theta_prior=theta_prior,
    tref=tref,
    minStartTime=minStartTime,
    maxStartTime=maxStartTime,
    nsteps=nsteps,
    nwalkers=nwalkers,
    ntemps=ntemps,
    log10beta_min=log10beta_min,
    transientWindowType="rect",
)
mcmc.run()
mcmc.plot_corner(label_offset=0.7)
mcmc.print_summary()
