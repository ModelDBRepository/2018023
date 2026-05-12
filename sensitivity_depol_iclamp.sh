#!/bin/bash

# sensitivity_depol_iclamp.sh loops over current clamp amplitudes,
# writing a depol_iclamp.py with those amplitudes that cause the soma
# voltage to reach those various target voltages at the moment before
# the bAP is triggered by another current clamp. This script also
# creates a base_dir_name that reflects this.

# increment 1 production (15 settings), 10 test case (2 settings)
# execute before running script: conda activate python38env
echo start time
date

# python control target v list [x for x in range(-70, -54, 1)] has 16
# elements where it was found that only -60 mV and below had
# nonspiking corresponding blocked tGAR models new python control
# target v list [x for x in range(-70, -59, 2)] has 6 elements [-70,
# -68, -66, -64, -62, 60]
nrnivmodl mod_files
python depol_stim.py # will make (sure) depolarization currents for
		     # target baseline voltages match the current
		     # model. This needs to be run if the mod files
		     # changed because that can affect the amount of
		     # current that needs to be injected for the model
		     # to reach a target baseline (pre-bAP) level.
for amp_index in `seq 0 5`; do
    # remove pickle files to recreate
    rm -f data/blocked_tGAR_data.pkl data/both_tGAR_data.pkl
    echo processing depolarizing current amp index $amp_index
    # change line 17 to set depol_iclamp.amp in depol_iclamp.py (from ... .orig)
    sed -e "18s/.*/amp_index=${amp_index}/" depol_iclamp.py.orig > depol_iclamp.py
    # echo verify update in the new depol_iclamp.py file
    # cat depol_iclamp.py | tail -2
    # echo
    # set base dir name to reflect date and e_pas value in configure_sim.py
    # since that will write it into base_dir_name.py
    sed -e "96s/.*/base_dir_name=\'\"20260123vShift_0_LVA_0p6IClamp_amp_index${amp_index}\/\"\'/" configure_sim.py.orig > configure_sim.py
    # echo verify update in the new configure_sim.py file:
    # head -98 configure_sim.py | tail -6
    echo 
    echo create the figures and data for this ${amp_index} setting
    ./configure_and_run.sh
    python3 calc_ca_suppr.py 0
done
# reset the depol_iclamp.py to amp_index=3 as the default for interactive
# use or if running other scripts like sensitivity_v_range_ca_chan_vshift.sh
sed -e "18s/.*/amp_index=3/" depol_iclamp.py.orig > depol_iclamp.py
echo all done at
date
