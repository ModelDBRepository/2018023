""" explore the calcium data written from sensitivity_small_bAP_stim.sh
such as in
Iascone_tonic_gabaar/20251224_AP_time220/_ca_suppr/
delta_ca_lva_mean.txt	delta_ca_total_std.txt
delta_ca_hva_mean.txt	delta_ca_lva_std.txt	v.txt
delta_ca_hva_std.txt	delta_ca_total_mean.txt
"""

from glob import glob
import numpy as np
import matplotlib.pyplot as plt
plt.ion()
date_string="20260123" # 20251120 excludes shifting tau's "20251110"
control_files=glob(date_string+"_AP_current*/data/loc200_ica_trace/loc200*_control.txt")
blocked_files=glob(date_string+"_AP_current*/data/loc200_ica_trace/loc200*_blocked.txt")

# store all the calcium current traces in an ica_dict
ica_dict={}

# control ca currents
for file in control_files:
    # extract the associated AP current:
    AP_current = eval(file.split("_AP_current")[1].split("/data")[0])
    # retrieve the ca current trace
    ica = np.loadtxt(file)
    ica_dict[(AP_current, "control")] = ica

# blocked ca currents
for file in blocked_files:
    # extract the associated AP current:
    AP_current = eval(file.split("_AP_current")[1].split("/data")[0])
    # retrieve the ca current trace
    ica = np.loadtxt(file)
    ica_dict[(AP_current, "blocked")] = ica

ica_amp={} # dict of ica amplitudes

for k in ica_dict:
    ica_amp[k]=abs(min(ica_dict[k]))

# -----
# summarize suppression data from files like:
# Iascone_tonic_gabaar/20251224_AP_time210/_ca_suppr/delta_ca_lva_mean.txt

mean_lva_files=glob(date_string+'_AP_current*/ca_suppr/delta_ca_lva_mean.txt')
std_lva_files=glob(date_string+'_AP_current*/ca_suppr/delta_ca_lva_std.txt')

mean_hva_files=glob(date_string+'_AP_current*/ca_suppr/delta_ca_hva_mean.txt')
std_hva_files=glob(date_string+'_AP_current*/ca_suppr/delta_ca_hva_std.txt')

mean_total_files=glob(date_string+'_AP_current*/ca_suppr/delta_ca_total_mean.txt')
std_total_files=glob(date_string+'_AP_current*/ca_suppr/delta_ca_total_std.txt')

# loc_points=np.loadtxt(date_string+'_AP_current-60/ca_suppr/v.txt') # v.txt
loc_points=np.loadtxt(date_string+'_AP_current1.0/ca_suppr/v.txt') # v.txt
# bad name for distance vector location points
# loc_points[7] is 200 so an index of 7 corresponds to the 200 um location

# when lva and hva channels have voltage shifted act, inact, and/or
# tau curves, the channel models lose their identity as lva or hva
# channels.  For this reasons we call the data "generic from" when
# based on these channels with shifted components.
# create generic from lva (gfl), generic from hva (gfh) ca channels,
# and their combined generic from total (gft) dicts for plotting the
# 200 um loc data. Examples gfl[(halfway, 'mean')], gfl[(halfway,
# 'std')]. Can consider adding a location tuple entry to this dict if
# want to plot other locations.

loc_index=7 # corresponds to 200 ums

gfl = {}
gfh = {}
gft = {}

# extract the data for the mean and std's for suppr from the generic
# ca chan derived from the lva

for mean_lva_file in mean_lva_files:
    AP_current=eval(mean_lva_file.split("_AP_current")[1].split("/")[0])
    mean_data=np.loadtxt(mean_lva_file)
    gfl[(AP_current, 'mean')] = mean_data[loc_index]

for mean_hva_file in mean_hva_files:
    AP_current=eval(mean_hva_file.split("_AP_current")[1].split("/")[0])
    mean_data=np.loadtxt(mean_hva_file)
    gfh[(AP_current, 'mean')] = mean_data[loc_index]

for mean_total_file in mean_total_files:
    AP_current=eval(mean_total_file.split("_AP_current")[1].split("/")[0])
    mean_data=np.loadtxt(mean_total_file)
    gft[(AP_current, 'mean')] = mean_data[loc_index]

for std_lva_file in std_lva_files:
    AP_current=eval(std_lva_file.split("_AP_current")[1].split("/")[0])
    std_data=np.loadtxt(std_lva_file)
    gfl[(AP_current, 'std')] = std_data[loc_index]

for std_hva_file in std_hva_files:
    AP_current=eval(std_hva_file.split("_AP_current")[1].split("/")[0])
    std_data=np.loadtxt(std_hva_file)
    gfh[(AP_current, 'std')] = std_data[loc_index]

for std_total_file in std_total_files:
    AP_current=eval(std_total_file.split("_AP_current")[1].split("/")[0])
    std_data=np.loadtxt(std_total_file)
    gft[(AP_current, 'std')] = std_data[loc_index]

fig, ax0 = plt.subplots(nrows=1, sharex=True)

for k in gfl: # just some dict to get the k[0] from.
    # plot the means
    plt.plot(k[0], gfl[(k[0], 'mean')], marker='.', color='purple')
    plt.plot(k[0], gfh[(k[0], 'mean')], marker='.', color='orange')
    plt.plot(k[0], gft[(k[0], 'mean')], marker='.', color='black')
    # add std errorbars around the means
    ax0.errorbar(k[0], gfh[(k[0], 'mean')], yerr=gfh[(k[0], 'std')],
                 lw=1, capsize=2, capthick=1, color='orange', label='HVA only')
    ax0.errorbar(k[0], gfl[(k[0], 'mean')], yerr=gfl[(k[0], 'std')],
                 lw=1, capsize=2, capthick=1, color='purple', label='LVA only')
    ax0.errorbar(k[0], gft[(k[0], 'mean')], yerr=gft[(k[0], 'std')],
                 lw=1, capsize=2, capthick=1, color='black', label='Average')
plt.title('Delta Ca2+ Ca chans (HVA LVA) vs stim of control AP')
plt.ylabel("delta ca suppr loc 200 um")
plt.xlabel("stimulus amplitude for AP (nA)")
plt.savefig('delta_ca_suppr_AP_current.pdf')
plt.savefig('delta_ca_suppr_AP_current.png')
# include earlier data to verify that calculation is the same:

import os
"""
source="/Users/morse/Documents/projects/HigleyLab/tonic_gabaar/Iascone_tonic_gabaar/20251031vShift_0_LVA_0p6IClamp_amp_index3/_ca_suppr"
local_source="20251126vShift_0_LVA_0p6IClamp_amp_index3/_ca_suppr/"
#local_source="20251126vShift_0_LVA_0p6IClamp_amp_index5/_ca_suppr/"
os.chdir(local_source)
data_dict={}
data_files = glob('delta_ca*txt')

for file in data_files:
    key=file.replace("delta_ca_","").replace(".txt","")
    data_dict[key]=np.loadtxt(file)
    
loc_index=7 # corresponds to 200 ums in v.txt and corresponding data
            # in data_dict values


loc_vec=np.loadtxt('v.txt')

# we need to load these corresponding values with the data from the
# 20251031...index3 folder

x_coord = 0.6 # place to display old data (different powers m) to
              # compare to new (0) (compares running new
              # sensitivity_v_range_ca_chan.sh results with
              # sensitivity_depol_iclamp.sh results)

ax0.errorbar(x_coord, data_dict['hva_mean'][loc_index],
             yerr=data_dict['hva_std'][loc_index], lw=1, capsize=2,
             capthick=1, color='orange', label='HVA only')
ax0.errorbar(x_coord, data_dict['lva_mean'][loc_index],
             yerr=data_dict['lva_std'][loc_index], lw=1, capsize=2,
             capthick=1, color='purple', label='LVA only')
ax0.errorbar(x_coord, data_dict['total_mean'][loc_index],
             yerr=data_dict['total_std'][loc_index], lw=1, capsize=2,
             capthick=1, color='black', label='Average')

# rise out of 20251031vShift_0_LVA_0p6IClamp_amp_index3/_ca_suppr
plt.savefig('../../delta_ca_suppr_AP_current_compare.pdf')
plt.savefig('../../delta_ca_suppr_AP_current_compare.png')

##########
#
# suppression (or enhancement) vs AP stim current
#
##########

fig, ax0 = plt.subplots(nrows=1, sharex=True)

from bAP_current_pairs import AP_current_pairs
AP_current_dict={}
for element in AP_current_pairs:
    AP_current_dict[element[0]] = element[1]

for k in gfl: # just some dict to get the k[0] from.
    # plot the means
    plt.plot(AP_current_dict[k[0]], gfl[(k[0], 'mean')], marker='.', color='purple')
    plt.plot(AP_current_dict[k[0]], gfh[(k[0], 'mean')], marker='.', color='orange')
    plt.plot(AP_current_dict[k[0]], gft[(k[0], 'mean')], marker='.', color='black')
    # add std errorbars around the means
    ax0.errorbar(AP_current_dict[k[0]], gfh[(k[0], 'mean')], yerr=gfh[(k[0], 'std')],
                 lw=1, capsize=2, capthick=1, color='orange', label='HVA only')
    ax0.errorbar(AP_current_dict[k[0]], gfl[(k[0], 'mean')], yerr=gfl[(k[0], 'std')],
                 lw=1, capsize=2, capthick=1, color='purple', label='LVA only')
    ax0.errorbar(AP_current_dict[k[0]], gft[(k[0], 'mean')], yerr=gft[(k[0], 'std')],
                 lw=1, capsize=2, capthick=1, color='black', label='Average')

plt.title('Delta Ca2+ Ca chans (HVA LVA) vs bAP stimulus current')
plt.ylabel("delta ca suppr loc 200 um")
plt.xlabel("bAP stimulus current (nA)")


plt.savefig('delta_ca_suppr_AP_stim_current.pdf')
plt.savefig('delta_ca_suppr_AP_stim_current.png')

"""
