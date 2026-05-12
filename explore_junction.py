"""explore the calcium data written from sensitivity_depol_iclamp.sh
when it is run alternately with and without the junction potential
correction in the LVA.
"""

from glob import glob
import numpy as np
import matplotlib.pyplot as plt
plt.ion()

# read in the mean values of ca suppression in the cases of having or
# not having the junction potential correction in the LVA.

topdir_string="junction/"
mean_jnc_lva_files=\
    glob(topdir_string+'*amp_index*/ca_suppr/delta_ca_lva_mean.txt')
topdir_string="no_junction/"
mean_no_jnc_lva_files=\
    glob(topdir_string+'*amp_index*/ca_suppr/delta_ca_lva_mean.txt')

# create generic junction and "no junction" from lva (gfl) ca channels,
# Example gfl[(amp_index, 'mean')]

# loc_index=0, 1, 7 # corresponds to 0, 25, 200 ums

gfl_jnc = {}
gfl_no_jnc = {}

# extract the data for the mean's for suppr from the generic
# ca chan derived from the lva

for mean_jnc_lva_file in mean_jnc_lva_files:
    ctrl_target_v_index=eval(mean_jnc_lva_file.split("_amp_index")[1].split("/")[0])
    mean_data=np.loadtxt(mean_jnc_lva_file)
    gfl_jnc[(ctrl_target_v_index, 'mean')] = mean_data

for mean_no_jnc_lva_file in mean_no_jnc_lva_files:
    ctrl_target_v_index=eval(mean_no_jnc_lva_file.split("_amp_index")[1].split("/")[0])
    mean_data=np.loadtxt(mean_no_jnc_lva_file)
    gfl_no_jnc[(ctrl_target_v_index, 'mean')] = mean_data


# loc_points are the distances from the soma to the compartments where
# there was ca measurement
loc_points=np.loadtxt(topdir_string+'20260115vShift_0_LVA_0p6IClamp_amp_index0/ca_suppr/v.txt')

baseline_values = [x for x in range(-70, -59, 2)]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d') # Use '3d' projection

# plot the data with orange for junction and blue for no junction.
# Ca suppression on z, the depolarization v on y, and the distance
# from the soma on the x axis.

xline = loc_points # same location data for all data
for k in gfl_jnc:
    v=baseline_values[k[0]] # the target control voltage
    yline = [v for x in range(len(loc_points))]
    zline = gfl_jnc[k]
    ax.plot3D(xline, yline, zline, 'orange')

for k in gfl_no_jnc:
    v=baseline_values[k[0]] # the target control voltage
    yline = [v for x in range(len(loc_points))]
    zline = gfl_no_jnc[k]
    ax.plot3D(xline, yline, zline, 'blue')

# now that I see the data is somewhat separated by baseline v - plot
# again in 2D
# note the following values guided selection of a line width formula
# >>> line_size=[(v+72)/5 for v in baseline_values]
# >>> line_size
# [0.4, 0.8, 1.2, 1.6, 2.0, 2.4]
# >>> 

plt.figure() # new 2D plot
for k in gfl_jnc:
    v=baseline_values[k[0]] # the target control voltage
    zline = gfl_jnc[k]
    plt.plot(xline, zline, 'orange', linewidth=(v+72)/5, label=f'baseline {v} jnc')
    zline = gfl_no_jnc[k]
    plt.plot(xline, zline, 'blue', linewidth=(v+72)/5, label=f'baseline {v} no jnc')

plt.xlim((0,620))
plt.legend(loc='best')

plt.title('Junction correction or not in LVA Delta Ca2+ suppr vs dist. from soma')
plt.ylabel("delta ca suppr")
plt.xlabel("distance from soma (um)")
# ax0.text(-70, 0.2,"""Ca suppression vs depolarized
# soma control v's.
# HVA (orange), LVA (purple), mean (black)""")
plt.show()

plt.savefig('delta_ca_suppr_jnc_no_jnc.pdf')
plt.savefig('delta_ca_suppr_jnc_no_jnc.png')

#########
#
# plot soma and dend v's
#
#########

# read in soma v's


topdir_string="junction/"
jnc_soma_v_control_files=\
  glob(topdir_string+'*amp_index*/data/soma_v_trace/soma_v_control.txt')
jnc_soma_v_blocked_files=\
  glob(topdir_string+'*amp_index*/data/soma_v_trace/soma_v_blocked.txt')

topdir_string="no_junction/"
no_jnc_soma_v_control_files=\
  glob(topdir_string+'*amp_index*/data/soma_v_trace/soma_v_control.txt')
no_jnc_soma_v_blocked_files=\
  glob(topdir_string+'*amp_index*/data/soma_v_trace/soma_v_blocked.txt')

# create junction and "no junction" soma v dicts
# Example 

soma_v_jnc = {}
soma_v_no_jnc = {}

# extract the data from the control, blocked, and time files

# control

for jnc_soma_v_control_file in jnc_soma_v_control_files:
    ctrl_target_v_index = \
  eval(jnc_soma_v_control_file.split("_amp_index")[1].split("/")[0])
    soma_v = np.loadtxt(jnc_soma_v_control_file)
    soma_v_jnc[(ctrl_target_v_index, 'control')] = soma_v

for jnc_soma_v_blocked_file in jnc_soma_v_blocked_files:
    ctrl_target_v_index = \
  eval(jnc_soma_v_blocked_file.split("_amp_index")[1].split("/")[0])
    soma_v = np.loadtxt(jnc_soma_v_blocked_file)
    soma_v_jnc[(ctrl_target_v_index, 'blocked')] = soma_v
    
# no jnc

for no_jnc_soma_v_control_file in no_jnc_soma_v_control_files:
    ctrl_target_v_index = \
  eval(no_jnc_soma_v_control_file.split("_amp_index")[1].split("/")[0])
    soma_v = np.loadtxt(no_jnc_soma_v_control_file)
    soma_v_no_jnc[(ctrl_target_v_index, 'control')] = soma_v

for no_jnc_soma_v_blocked_file in no_jnc_soma_v_blocked_files:
    ctrl_target_v_index = \
  eval(no_jnc_soma_v_blocked_file.split("_amp_index")[1].split("/")[0])
    soma_v = np.loadtxt(no_jnc_soma_v_blocked_file)
    soma_v_no_jnc[(ctrl_target_v_index, 'blocked')] = soma_v

# time
identical_t_vec_files = \
  glob(topdir_string+'*amp_index*/data/soma_v_trace/t_vec.txt')
for identical_t_vec_file in identical_t_vec_files:
    break # the first one same as all the others

t_vec = np.loadtxt(identical_t_vec_file)

# graph together with orange junction, blue no jnc, solid control,
# dashed blocked, baseline thickness

plt.figure()

for baseline_v_index, condition in soma_v_no_jnc:
    v=baseline_values[baseline_v_index] # the target control voltage
    if condition == 'blocked':
        # blocked plotted as dashed line
        plt.plot(t_vec, soma_v_no_jnc[(baseline_v_index, condition)]
             , 'blue', linewidth=(v+72)/5, linestyle='--',
             label=f'baseline {v} no jnc')
        # use the same combination for jnc potential correction data
        plt.plot(t_vec, soma_v_jnc[(baseline_v_index, condition)]
             , 'orange', linewidth=(v+72)/5, linestyle='--',
             label=f'baseline {v} jnc')
    else:
        # if not blocked then control represented by solid line
        plt.plot(t_vec, soma_v_no_jnc[(baseline_v_index, condition)]
             , 'blue', linewidth=(v+72)/5, linestyle='-',
             label=f'baseline {v} no jnc')
        plt.plot(t_vec, soma_v_jnc[(baseline_v_index, condition)]
             , 'orange', linewidth=(v+72)/5, linestyle='-',
             label=f'baseline {v} no jnc')

plt.title('soma v for jnc(orange)/no jnc(blue), cntrl/blcked(dashed)')
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')

plt.xlim((197,220))
plt.ylim((-80, 50))

# dend v

# read in dend v's
# first use the first 100 at loc 200 um's: loc200_apic11_0p969027_blocked.txt

topdir_string="junction/"
jnc_apic11_v_control_files=\
  glob(topdir_string+\
       '*amp_index*/data/loc200_v_traces/loc200_apic11_0p969027_blocked.txt')
jnc_apic11_v_blocked_files=\
  glob(topdir_string+\
       '*amp_index*/data/loc200_v_traces/loc200_apic11_0p969027_blocked.txt')

topdir_string="no_junction/"
no_jnc_apic11_v_control_files=\
  glob(topdir_string+\
       '*amp_index*/data/loc200_v_traces/loc200_apic11_0p969027_blocked.txt')
no_jnc_apic11_v_blocked_files=\
  glob(topdir_string+\
       '*amp_index*/data/loc200_v_traces/loc200_apic11_0p969027_blocked.txt')

# create junction and "no junction" apic11 v dicts
# Example 

apic11_v_jnc = {}
apic11_v_no_jnc = {}

# extract the data from the control, blocked, and time files

# control

for jnc_apic11_v_control_file in jnc_apic11_v_control_files:
    ctrl_target_v_index = \
  eval(jnc_apic11_v_control_file.split("_amp_index")[1].split("/")[0])
    apic11_v = np.loadtxt(jnc_apic11_v_control_file)
    apic11_v_jnc[(ctrl_target_v_index, 'control')] = apic11_v

for jnc_apic11_v_blocked_file in jnc_apic11_v_blocked_files:
    ctrl_target_v_index = \
  eval(jnc_apic11_v_blocked_file.split("_amp_index")[1].split("/")[0])
    apic11_v = np.loadtxt(jnc_apic11_v_blocked_file)
    apic11_v_jnc[(ctrl_target_v_index, 'blocked')] = apic11_v
    
# no jnc

for no_jnc_apic11_v_control_file in no_jnc_apic11_v_control_files:
    ctrl_target_v_index = \
  eval(no_jnc_apic11_v_control_file.split("_amp_index")[1].split("/")[0])
    apic11_v = np.loadtxt(no_jnc_apic11_v_control_file)
    apic11_v_no_jnc[(ctrl_target_v_index, 'control')] = apic11_v

for no_jnc_apic11_v_blocked_file in no_jnc_apic11_v_blocked_files:
    ctrl_target_v_index = \
  eval(no_jnc_apic11_v_blocked_file.split("_amp_index")[1].split("/")[0])
    apic11_v = np.loadtxt(no_jnc_apic11_v_blocked_file)
    apic11_v_no_jnc[(ctrl_target_v_index, 'blocked')] = apic11_v

# time
identical_t_vec_files = \
  glob(topdir_string+'*amp_index*/data/apic11_v_trace/t_vec.txt')
for identical_t_vec_file in identical_t_vec_files:
    break # the first one same as all the others

t_vec = np.loadtxt(identical_t_vec_file)

# graph together with orange junction, blue no jnc, solid control,
# dashed blocked, baseline thickness

plt.figure()

for baseline_v_index, condition in apic11_v_no_jnc:
    v=baseline_values[baseline_v_index] # the target control voltage
    if condition == 'blocked':
        # blocked plotted as dashed line
        plt.plot(t_vec, apic11_v_no_jnc[(baseline_v_index, condition)]
             , 'blue', linewidth=(v+72)/5, linestyle='--',
             label=f'baseline {v} no jnc')
        # use the same combination for jnc potential correction data
        plt.plot(t_vec, apic11_v_jnc[(baseline_v_index, condition)]
             , 'orange', linewidth=(v+72)/5, linestyle='--',
             label=f'baseline {v} jnc')
    else:
        # if not blocked then control represented by solid line
        plt.plot(t_vec, apic11_v_no_jnc[(baseline_v_index, condition)]
             , 'blue', linewidth=(v+72)/5, linestyle='-',
             label=f'baseline {v} no jnc')
        plt.plot(t_vec, apic11_v_jnc[(baseline_v_index, condition)]
             , 'orange', linewidth=(v+72)/5, linestyle='-',
             label=f'baseline {v} no jnc')

plt.title('apic11 v for jnc(orange)/no jnc(blue), cntrl/blcked(dashed)')
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')

plt.xlim((200,220))
plt.ylim((-80, 30))

###################
#
# read/plot remaining qty's
#
###################


# pseudo code: read one of the amp_index data folder's files to find
# remaining qtys to graph. create them all as single graphs with all
# the target control baseline voltage traces as well as the presence
# of jnc potential or not.

'''

# loc_points are the distances from the soma to the compartments where
# there was ca measurement
loc_points=np.loadtxt(topdir_string+'20260115vShift_0_LVA_0p6IClamp_amp_index0/ca_suppr/v.txt')

baseline_values = [x for x in range(-70, -59, 2)]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d') # Use '3d' projection

# plot the data with orange for junction and blue for no junction.
# Ca suppression on z, the depolarization v on y, and the distance
# from the soma on the x axis.

xline = loc_points # same location data for all data
for k in gfl_jnc:
    v=baseline_values[k[0]] # the target control voltage
    yline = [v for x in range(len(loc_points))]
    zline = gfl_jnc[k]
    ax.plot3D(xline, yline, zline, 'orange')

for k in gfl_no_jnc:
    v=baseline_values[k[0]] # the target control voltage
    yline = [v for x in range(len(loc_points))]
    zline = gfl_no_jnc[k]
    ax.plot3D(xline, yline, zline, 'blue')

# now that I see the data is somewhat separated by baseline v - plot
# again in 2D
# note the following values guided selection of a line width formula
# >>> line_size=[(v+72)/5 for v in baseline_values]
# >>> line_size
# [0.4, 0.8, 1.2, 1.6, 2.0, 2.4]
# >>> 

plt.figure() # new 2D plot
for k in gfl_jnc:
    v=baseline_values[k[0]] # the target control voltage
    zline = gfl_jnc[k]
    plt.plot(xline, zline, 'orange', linewidth=(v+72)/5, label=f'baseline {v} jnc')
    zline = gfl_no_jnc[k]
    plt.plot(xline, zline, 'blue', linewidth=(v+72)/5, label=f'baseline {v} no jnc')

plt.xlim((0,620))
plt.legend(loc='best')

plt.title('Junction correction or not in LVA Delta Ca2+ suppr vs dist. from soma')
plt.ylabel("delta ca suppr")
plt.xlabel("distance from soma (um)")
# ax0.text(-70, 0.2,"""Ca suppression vs depolarized
# soma control v's.
# HVA (orange), LVA (purple), mean (black)""")
plt.show()

plt.savefig('delta_ca_suppr_jnc_no_jnc.pdf')
plt.savefig('delta_ca_suppr_jnc_no_jnc.png')

'''
