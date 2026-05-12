#!/bin/bash
# sensitivity_v_range_ca_chan_vshift.sh cycles through LVA, HVA vShift
# values creating a base_dir_name that reflects this while also
# writing new Ca_LVAst.mod, or CaH.mod files with the appropriate
# vShift's in it, and then compiling the mod files and regenerating
# all the figures.

# execute before running script: conda activate python38env
echo start time
date
# assign some constants.
# HVA vShift=0 by default
# diagnostic setting `-20 20 20` iterates over -20 0 20

# seq has start step end arguments in that order
for v in `seq -30 10 10`; do # originally -20 to 20
    vShift_LVA=$v
    # echo vShift_LVA $vShift_LVA
    vShift_HVA=0 # $v # change to 0 if uninterested in shifting HVA
    echo for vShift $v vShift_LVA is $vShift_LVA and vShift_HVA \
	 is $vShift_HVA
    # change some line to set vShift in LVA mod file for both inf and tau's or just inf('s) (uncomment one of the three below)
    # another option allows comparison to an m*h model (LVA was m^2 h)
    # sed -e "22s/.*/\	vShift\ =\ ${vShift_LVA}\ (mV)\ :\ negative\ value\ shifts\ curves\ to\ the\ right/" mod_files/Ca_LVAst.mod.orig > mod_files/Ca_LVAst.mod
    # sed -e "22s/.*/\	vShift\ =\ ${vShift_LVA}\ (mV)\ :\ negative\ value\ shifts\ curves\ to\ the\ right/" mod_files/Ca_LVAst.mod.template_h_vShift_only > mod_files/Ca_LVAst.mod
    sed -e "22s/.*/\	vShift\ =\ ${vShift_LVA}\ (mV)\ :\ negative\ value\ shifts\ curves\ to\ the\ right/" mod_files/Ca_LVAst.mod.template_m_vShift_only > mod_files/Ca_LVAst.mod
    # sed -e "22s/.*/\	vShift\ =\ ${vShift_LVA}\ (mV)\ :\ negative\ value\ shifts\ curves\ to\ the\ right/" mod_files/Ca_LVAst_act_inact.mod.orig > mod_files/Ca_LVAst.mod
    # sed -e "22s/.*/\	vShift\ =\ ${vShift_LVA}\ (mV)\ :\ negative\ value\ shifts\ curves\ to\ the\ right/" mod_files/Ca_LVAst_act_inact_3rd_pwr.mod.orig > mod_files/Ca_LVAst.mod
    # try HCA time constants in LVA
    # sed -e "22s/.*/\	vShift\ =\ ${vShift_LVA}\ (mV)\ :\ negative\ value\ shifts\ curves\ to\ the\ right/" mod_files/permuted_taus/Ca_LVAst.mod > mod_files/Ca_LVAst.mod
    # echo verify update in the new mod file:
    # head -24 mod_files/Ca_LVAst.mod | tail -6
    # echo
    # change line 38 to set vShift in HVA mod file for both inf and tau's or just inf's (uncomment one of the two below)
    sed -e "38s/.*/\	vShift\ =\ ${vShift_HVA}\ (mV)\ :\ vShift\'s\ made\ possible\ with\ this\ parameter/" mod_files/CaH.mod.template > mod_files/CaH.mod
    # sed -e "38s/.*/\	vShift\ =\ ${vShift_HVA}\ (mV)\ :\ vShift\'s\ made\ possible\ with\ this\ parameter/" mod_files/CaH_act_inact.mod.orig > mod_files/CaH.mod
    # sed -e "38s/.*/\	vShift\ =\ ${vShift_HVA}\ (mV)\ :\ vShift\'s\ made\ possible\ with\ this\ parameter/" mod_files/CaH_act_inact_2nd_pwr.mod.orig > mod_files/CaH.mod
    # try LVA time constants in HVA
    # sed -e "38s/.*/\	vShift\ =\ ${vShift_HVA}\ (mV)\ :\ vShift\'s\ made\ possible\ with\ this\ parameter/" mod_files/permuted_taus/CaH.mod > mod_files/CaH.mod
    # echo verify update in the new mod file:
    # head -40 mod_files/CaH.mod | tail -6
    # echo
    # set base dir name to reflect date and vShift value in configure_sim.py
    # since that will write it into base_dir_name.py
    sed -e "96s/.*/base_dir_name=\'\"20260304_vshift${v}\/\"\'/" configure_sim.py.orig > configure_sim.py
    # echo verify update in the new configure_sim.py file:
    # head -98 configure_sim.py | tail -6
    # echo 
    # echo create the figures and data for this ${halfway_v} halfway_v setting
    ./configure_and_run.sh
    python3 calc_ca_suppr.py 0
done
# restore the default HVA and LVA for interactive use working as expected
cp mod_files/Ca_LVAst.mod.template mod_files/Ca_LVAst.mod
cp mod_files/CaH.mod.template mod_files/CaH.mod
echo all done at
date
