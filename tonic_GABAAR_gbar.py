# this file writen by configure_sim.py
from g_scale import *
from setup_tGARs import * # supplies set_tonic() to reset exGABALeak
# which is helpful when distal or ramp only resets part of mod file default

distribution = "constant"
tonic_GABAAR_gbar = 0.8*2.7078395847022205e-05*1
tGAR_label = "const_leak_0p27factor1.00" # constant distribution about 0.27 pS/um2
def control():
    g_region('d', 'exGABALeak', tonic_GABAAR_gbar)
