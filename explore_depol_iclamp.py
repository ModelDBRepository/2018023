""" explore the calcium data written from sensitivity_depol_iclamp.sh
"""

from glob import glob
import numpy as np
import matplotlib.pyplot as plt
plt.ion()
date_string="20260123"
control_files=glob(date_string+"*amp_index*/data/loc200_ica_trace/loc200*_control.txt")
blocked_files=glob(date_string+"*amp_index*/data/loc200_ica_trace/loc200*_blocked.txt")

# store all the calcium current traces in an ica_dict
ica_dict={}

# control ca currents
for file in control_files:
    ctrl_target_v_index = eval(file.split("_amp_index")[1].split("/data")[0])
    # retrieve the ca current trace
    ica = np.loadtxt(file)
    ica_dict[(ctrl_target_v_index, "control")] = ica

# blocked ca currents
for file in blocked_files:
    ctrl_target_v_index = eval(file.split("_amp_index")[1].split("/data")[0])
    # retrieve the ca current trace
    ica = np.loadtxt(file)
    ica_dict[(ctrl_target_v_index, "blocked")] = ica

ica_amp={} # dict of ica amplitudes

for k in ica_dict:
    ica_amp[k]=abs(min(ica_dict[k]))

# -----
# summarize suppression data from files like:
# Iascone_tonic_gabaar/20251002_amp_index0/ca_suppr/delta_ca_lva_mean.txt

mean_lva_files=glob(date_string+'*amp_index*/ca_suppr/delta_ca_lva_mean.txt')
std_lva_files=glob(date_string+'*amp_index*/ca_suppr/delta_ca_lva_std.txt')

mean_hva_files=glob(date_string+'*amp_index*/ca_suppr/delta_ca_hva_mean.txt')
std_hva_files=glob(date_string+'*amp_index*/ca_suppr/delta_ca_hva_std.txt')

mean_total_files=glob(date_string+'*amp_index*/ca_suppr/delta_ca_total_mean.txt')
std_total_files=glob(date_string+'*amp_index*/ca_suppr/delta_ca_total_std.txt')
# 20251124vShift_0_LVA_0p6IClamp_amp_index3
# loc_points=np.loadtxt(date_string+'_amp_index0/ca_suppr/v.txt') # v.txt
loc_points=np.loadtxt(date_string+'vShift_0_LVA_0p6IClamp_amp_index0/ca_suppr/v.txt') # v.txt
# bad name for distance vector location points
# loc_points[7] is 200 so an index of 7 corresponds to the 200 um location

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
    ctrl_target_v_index=eval(mean_lva_file.split("_amp_index")[1].split("/")[0])
    mean_data=np.loadtxt(mean_lva_file)
    gfl[(ctrl_target_v_index, 'mean')] = mean_data[loc_index]

for mean_hva_file in mean_hva_files:
    ctrl_target_v_index=eval(mean_hva_file.split("_amp_index")[1].split("/")[0])
    mean_data=np.loadtxt(mean_hva_file)
    gfh[(ctrl_target_v_index, 'mean')] = mean_data[loc_index]

for mean_total_file in mean_total_files:
    ctrl_target_v_index=eval(mean_total_file.split("_amp_index")[1].split("/")[0])
    mean_data=np.loadtxt(mean_total_file)
    gft[(ctrl_target_v_index, 'mean')] = mean_data[loc_index]

for std_lva_file in std_lva_files:
    ctrl_target_v_index=eval(std_lva_file.split("_amp_index")[1].split("/")[0])
    std_data=np.loadtxt(std_lva_file)
    gfl[(ctrl_target_v_index, 'std')] = std_data[loc_index]

for std_hva_file in std_hva_files:
    ctrl_target_v_index=eval(std_hva_file.split("_amp_index")[1].split("/")[0])
    std_data=np.loadtxt(std_hva_file)
    gfh[(ctrl_target_v_index, 'std')] = std_data[loc_index]

for std_total_file in std_total_files:
    ctrl_target_v_index=eval(std_total_file.split("_amp_index")[1].split("/")[0])
    std_data=np.loadtxt(std_total_file)
    gft[(ctrl_target_v_index, 'std')] = std_data[loc_index]

fig, ax0 = plt.subplots(nrows=1, sharex=True)
baseline_values = [x for x in range(-70, -59, 2)]

for k in gfl: # just some dict to get the k[0] from.
    # plot the means
    v=baseline_values[k[0]] # the target control voltage
    plt.plot(v, gfl[(k[0], 'mean')], marker='.', color='purple')
    plt.plot(v, gfh[(k[0], 'mean')], marker='.', color='orange')
    plt.plot(v, gft[(k[0], 'mean')], marker='.', color='black')
    # add std errorbars around the means
    ax0.errorbar(v, gfh[(k[0], 'mean')], yerr=gfh[(k[0], 'std')],
                 lw=1, capsize=2, capthick=1, color='orange', label='HVA only')
    ax0.errorbar(v, gfl[(k[0], 'mean')], yerr=gfl[(k[0], 'std')],
                 lw=1, capsize=2, capthick=1, color='purple', label='LVA only')
    ax0.errorbar(v, gft[(k[0], 'mean')], yerr=gft[(k[0], 'std')],
                 lw=1, capsize=2, capthick=1, color='black', label='Average')

plt.title('Delta Ca2+ suppression (HVA LVA) vs soma control target v ')
plt.ylabel("delta ca suppr loc 200 um")
plt.xlabel("soma control target v (mV)")
ax0.text(-70, 0.2,"""Ca suppression vs depolarized
soma control v's.
HVA (orange), LVA (purple), mean (black)""")
# plt.legend(loc='best') # unfortunately the legend repeats for all the data
plt.savefig('delta_ca_suppr_depol_iclamp.pdf')
plt.savefig('delta_ca_suppr_depol_iclamp.png')
