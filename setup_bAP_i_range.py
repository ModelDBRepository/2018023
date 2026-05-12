"""setup the AP current stimulus based on AP_time_current_pairs and a
passed index to these pairs. Let the first element in the pair (the
time of the AP) be the base_dir_name.py suffix and the second element
needs to be assigned to the h.IClamp[0].amp throughout calc_ca_suppr
and figs_incl_suppl.py"""

import sys
print(sys.argv)
AP_i_index=eval(sys.argv[-1])

from bAP_current_pairs import *

print(AP_current_pairs[AP_i_index])
AP_current=AP_current_pairs[AP_i_index][0]

from neuron import h

# setup base_dir_name

h.system(rf'''sed -e "96s/.*/base_dir_name=\'\"20260123_AP_current{AP_current}\/\"\'/" configure_sim.py.orig > configure_sim.py''')

# setup current amplitude and tstop

amplitude=AP_current_pairs[AP_i_index][1]

# change tstop on line 35 and 43 and add a IClamp[0].amp setting on line 41
# of run_tGAR_blocked.py
h.system(r'sed -e "35s/.*/    h.tstop=300/" run_tGAR_blocked.py.template > run_tGAR_blocked.py.tmp')
h.system(fr'sed -e "41s/.*/    h.IClamp[0].amp={amplitude}/" run_tGAR_blocked.py.tmp > run_tGAR_blocked.py.tmp1')
h.system(r'sed -e "43s/.*/    my_run(300)/" run_tGAR_blocked.py.tmp1 > run_tGAR_blocked.py')

# add IClamp[0].amp setting on line 66
h.system(fr'sed -e "66s/.*/h.IClamp[0].amp={amplitude}/" run_tGAR_control.py.template > run_tGAR_control.py.tmp')

# change line 71 to "tstop" of 300
h.system(r'sed -e "71s/.*/my_run(300)/" run_tGAR_control.py.tmp > run_tGAR_control.py')

# these changes will be persistent when figs_incl_suppl.py and
# ca_calc_suppr.py are run.


