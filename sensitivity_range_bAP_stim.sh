#!/bin/bash

# sensitivity_small_bAP_stim.sh explores a small current injections
# affect on ca suppression

# execute before running script: conda activate python38env
echo start time
date

# the current injection for bAP assumes that the amp_index=3
# (-64 mV baseline depolarization in the control)

nrnivmodl mod_files
# python depol_stim.py # will make (sure) depolarization currents for
		     # target baseline voltages match the current
		     # model. This needs to be run if the mod files
		     # changed because that can affect the amount of
		     # current that needs to be injected for the model
		     # to reach a target baseline (pre-bAP) level.
rm -f data/blocked_tGAR_data.pkl data/both_tGAR_data.pkl
declare -x amp_index=3
echo processing depolarizing current amp index $amp_index

for AP_i_index in `seq 0 1 4`; do
    echo $AP_i_index
    python setup_bAP_i_range.py $AP_i_index
    ./configure_and_run.sh
done

# restore for interactive
# use or if running other scripts like sensitivity_v_range_ca_chan_vshift.sh
#sed -e "18s/.*/amp_index=3/" depol_iclamp.py.orig > depol_iclamp.py
#cp rig.ses.orig rig.ses
#cp run_tGAR_blocked.py.template run_tGAR_blocked.py
#cp run_tGAR_control.py.template run_tGAR_control.py

echo all done at
date
