from pyfstat import Writer, GlitchWriter
import numpy as np

outdir = 'data'
# First, we generate data with a reasonably strong smooth signal

# Define parameters of the Crab pulsar as an example
F0 = 30.0
F1 = -1e-10
F2 = 0
Alpha = np.radians(83.6292)
Delta = np.radians(22.0144)

# Signal strength
h0 = 5e-24

# Properties of the GW data
sqrtSX = 1e-22
tstart = 1000000000
duration = 100*86400
tend = tstart+duration
tref = tstart + 0.5*duration

data = Writer(
    label='0_glitch', outdir=outdir, tref=tref, tstart=tstart, F0=F0, F1=F1,
    F2=F2, duration=duration, Alpha=Alpha, Delta=Delta, h0=h0, sqrtSX=sqrtSX)
data.make_data()

# The predicted twoF, given by lalapps_predictFstat can be accessed by
twoF = data.predict_fstat()
print 'Predicted twoF value: {}\n'.format(twoF)

# Next, taking the same signal parameters, we include a glitch half way through
dtglitch = duration/2.0
delta_F0 = 5e-6
delta_F1 = 0

glitch_data = GlitchWriter(
    label='1_glitch', outdir=outdir, tref=tref, tstart=tstart, F0=F0, F1=F1,
    F2=F2, duration=duration, Alpha=Alpha, Delta=Delta, h0=h0, sqrtSX=sqrtSX,
    dtglitch=dtglitch, delta_F0=delta_F0, delta_F1=delta_F1)
glitch_data.make_data()

# Making data with two glitches

dtglitch_2 = [duration/4.0, 4*duration/5.0]
delta_phi_2 = [0, 0]
delta_F0_2 = [4e-6, 3e-7]
delta_F1_2 = [0, 0]
delta_F2_2 = [0, 0]

two_glitch_data = GlitchWriter(
    label='2_glitch', outdir=outdir, tref=tref, tstart=tstart, F0=F0, F1=F1,
    F2=F2, duration=duration, Alpha=Alpha, Delta=Delta, h0=h0, sqrtSX=sqrtSX,
    dtglitch=dtglitch_2, delta_phi=delta_phi_2, delta_F0=delta_F0_2,
    delta_F1=delta_F1_2, delta_F2=delta_F2_2)
two_glitch_data.make_data()
