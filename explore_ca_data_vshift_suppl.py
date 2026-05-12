""" explore the calcium data written from sensitivity_v_range_ca_chan_vshift.sh
"""

from glob import glob
import numpy as np
import matplotlib.pyplot as plt
plt.ion()
date_string="20260304" # 20251120 excludes shifting tau's "20251110"
control_files=glob(date_string+"_vshift*/data/loc200_ica_trace/loc200*_control.txt")
blocked_files=glob(date_string+"_vshift*/data/loc200_ica_trace/loc200*_blocked.txt")

# store all the calcium current traces in an ica_dict
ica_dict={}

# control ca currents
for file in control_files:
    # extract the x axis of the ca currents:
    vshift = eval(file.split("_vshift")[1].split("/data")[0])
    # retrieve the ca current trace
    ica = np.loadtxt(file)
    ica_dict[(vshift, "control")] = ica

# blocked ca currents
for file in blocked_files:
    vshift = eval(file.split("_vshift")[1].split("/data")[0])
    # retrieve the ca current trace
    ica = np.loadtxt(file)
    ica_dict[(vshift, "blocked")] = ica

ica_amp={} # dict of ica amplitudes

for k in ica_dict:
    ica_amp[k]=abs(min(ica_dict[k]))

# -----
# summarize suppression data from files like:
# Iascone_tonic_gabaar/20250826_vshift-50/_ca_suppr/delta_ca_lva_mean.txt

mean_lva_files=glob(date_string+'_vshift*/ca_suppr/delta_ca_lva_mean.txt')
std_lva_files=glob(date_string+'_vshift*/ca_suppr/delta_ca_lva_std.txt')

mean_hva_files=glob(date_string+'_vshift*/ca_suppr/delta_ca_hva_mean.txt')
std_hva_files=glob(date_string+'_vshift*/ca_suppr/delta_ca_hva_std.txt')

mean_total_files=glob(date_string+'_vshift*/ca_suppr/delta_ca_total_mean.txt')
std_total_files=glob(date_string+'_vshift*/ca_suppr/delta_ca_total_std.txt')

# loc_points=np.loadtxt(date_string+'_vshift-60/ca_suppr/v.txt') # v.txt
loc_points=np.loadtxt(date_string+'_vshift-20/ca_suppr/v.txt') # v.txt
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
    vshift=eval(mean_lva_file.split("_vshift")[1].split("/")[0])
    mean_data=np.loadtxt(mean_lva_file)
    gfl[(vshift, 'mean')] = mean_data[loc_index]

for mean_hva_file in mean_hva_files:
    vshift=eval(mean_hva_file.split("_vshift")[1].split("/")[0])
    mean_data=np.loadtxt(mean_hva_file)
    gfh[(vshift, 'mean')] = mean_data[loc_index]

for mean_total_file in mean_total_files:
    vshift=eval(mean_total_file.split("_vshift")[1].split("/")[0])
    mean_data=np.loadtxt(mean_total_file)
    gft[(vshift, 'mean')] = mean_data[loc_index]

for std_lva_file in std_lva_files:
    vshift=eval(std_lva_file.split("_vshift")[1].split("/")[0])
    std_data=np.loadtxt(std_lva_file)
    gfl[(vshift, 'std')] = std_data[loc_index]

for std_hva_file in std_hva_files:
    vshift=eval(std_hva_file.split("_vshift")[1].split("/")[0])
    std_data=np.loadtxt(std_hva_file)
    gfh[(vshift, 'std')] = std_data[loc_index]

for std_total_file in std_total_files:
    vshift=eval(std_total_file.split("_vshift")[1].split("/")[0])
    std_data=np.loadtxt(std_total_file)
    gft[(vshift, 'std')] = std_data[loc_index]

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

plt.title('Delta Ca2+ Ca chans (HVA LVA) vs vshift ')
plt.ylabel("delta ca suppr loc 200 um")
# plt.xlabel("vShift (mV) (h inf LVA curve only)")
plt.xlabel("vShift (mV) (m inf LVA curve only)")
#plt.xlabel("vShift (mV) (LVA m, h inf's only )")
# ax0.text(-60, 1.4,"""Generic Ca Chans created by moving crossover
#ax0.text(-45, 1.4,"""Generic Ca Chans created by moving crossover
# ax0.text(-40, .7,"""Generic Ca Chans created by moving crossover
# of act and inact curves (also called halfway point)
# of HVA (orange), LVA (purple), mean (black)
# Diagnostic: HVA has LVA time constants""")


plt.savefig('delta_ca_suppr_vshift.pdf')
plt.savefig('delta_ca_suppr_vshift.png')


