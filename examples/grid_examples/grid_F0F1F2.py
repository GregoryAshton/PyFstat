import pyfstat
import numpy as np
import matplotlib.pyplot as plt

try:
    from gridcorner import gridcorner
except ImportError:
    raise ImportError(
        "Python module 'gridcorner' not found, please install from "
        "https://gitlab.aei.uni-hannover.de/GregAshton/gridcorner")

F0 = 30.0
F1 = 1e-10
F2 = 0
Alpha = 1.0
Delta = 1.5

# Properties of the GW data
sqrtSX = 1e-23
tstart = 1000000000
duration = 10*86400
tend = tstart+duration
tref = .5*(tstart+tend)

depth = 20
label = 'grid_F0F1F2'
outdir = 'data'

h0 = sqrtSX / depth

data = pyfstat.Writer(
    label=label, outdir=outdir, tref=tref,
    tstart=tstart, F0=F0, F1=F1, F2=F2, duration=duration, Alpha=Alpha,
    Delta=Delta, h0=h0, sqrtSX=sqrtSX)
data.make_data()

m = 0.01
dF0 = np.sqrt(12*m)/(np.pi*duration)
dF1 = np.sqrt(180*m)/(np.pi*duration**2)
dF2 = 1e-17
N = 100
DeltaF0 = N*dF0
DeltaF1 = N*dF1
DeltaF2 = N*dF2
F0s = [F0-DeltaF0/2., F0+DeltaF0/2., dF0]
F1s = [F1-DeltaF1/2., F1+DeltaF1/2., dF1]
F2s = [F2-DeltaF2/2., F2+DeltaF2/2., dF2]
Alphas = [Alpha]
Deltas = [Delta]
search = pyfstat.GridSearch(
    'grid_F0F1F2', 'data', data.sftfilepath, F0s, F1s,
    F2s, Alphas, Deltas, tref, tstart, tend)
search.run()

F0_vals = np.unique(search.data[:, 2]) - F0
F1_vals = np.unique(search.data[:, 3]) - F1
F2_vals = np.unique(search.data[:, 4]) - F2
twoF = search.data[:, -1].reshape((len(F0_vals), len(F1_vals), len(F2_vals)))
xyz = [F0_vals, F1_vals, F2_vals]
labels = ['$f - f_0$', '$\dot{f} - \dot{f}_0$', '$\ddot{f} - \ddot{f}_0$',
          '$\widetilde{2\mathcal{F}}$']
fig, axes = gridcorner(
    twoF, xyz, projection='log_mean', labels=labels, whspace=0.1, factor=1.8)
fig.savefig('{}/{}_projection_matrix.png'.format(outdir, label))
