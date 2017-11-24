import pyfstat
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('./paper-style.mplstyle')

F0 = 30.0
F1 = -1e-10
F2 = 0
Alpha = np.radians(83.6292)
Delta = np.radians(22.0144)

# Properties of the GW data
sqrtSX = 1e-23
tstart = 1000000000
duration = 100*86400
tend = tstart+duration
tref = .5*(tstart+tend)

depth = 40
label = 'semicoherent_directed_follow_up'
outdir = 'data'

h0 = sqrtSX / depth

data = pyfstat.Writer(
    label=label, outdir=outdir, tref=tref, tstart=tstart, F0=F0, F1=F1,
    F2=F2, duration=duration, Alpha=Alpha, Delta=Delta, h0=h0, sqrtSX=sqrtSX)
data.make_data()

# The predicted twoF, given by lalapps_predictFstat can be accessed by
twoF = data.predict_fstat()
print 'Predicted twoF value: {}\n'.format(twoF)

# Search
VF0 = VF1 = 1e5
DeltaF0 = np.sqrt(VF0) * np.sqrt(3)/(np.pi*duration)
DeltaF1 = np.sqrt(VF1) * np.sqrt(180)/(np.pi*duration**2)
theta_prior = {'F0': {'type': 'unif',
                      'lower': F0-DeltaF0/2.,
                      'upper': F0+DeltaF0/2},
               'F1': {'type': 'unif',
                      'lower': F1-DeltaF1/2.,
                      'upper': F1+DeltaF1/2},
               'F2': F2,
               'Alpha': Alpha,
               'Delta': Delta
               }

ntemps = 3
log10beta_min = -0.5
nwalkers = 100
nsteps = [100, 100]

mcmc = pyfstat.MCMCFollowUpSearch(
    label=label, outdir=outdir,
    sftfilepattern='{}/*{}*sft'.format(outdir, label),
    theta_prior=theta_prior, tref=tref, minStartTime=tstart, maxStartTime=tend,
    nwalkers=nwalkers, nsteps=nsteps, ntemps=ntemps,
    log10beta_min=log10beta_min)

NstarMax = 1000
Nsegs0 = 100
fig, axes = plt.subplots(nrows=2, figsize=(3.4, 3.5))
fig, axes = mcmc.run(
    NstarMax=NstarMax, Nsegs0=Nsegs0, subtractions=[F0, F1], labelpad=0.01,
    plot_det_stat=False, return_fig=True, context='paper', fig=fig,
    axes=axes)
for ax in axes:
    ax.grid()
    ax.set_xticks(np.arange(0, 600, 100))
    ax.set_xticklabels([str(s) for s in np.arange(0, 700, 100)])
axes[-1].set_xlabel(r'$\textrm{Number of steps}$', labelpad=0.1)
fig.tight_layout()
fig.savefig('{}/{}_walkers.png'.format(mcmc.outdir, mcmc.label), dpi=400)
