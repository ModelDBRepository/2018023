"""This post-processing script will compute the ratio between the
blocked and control conditions of m and h for the LVA and HVA channels
within the calcium accumulation window. Then it takes the averages of
these ratios to see if the dominant change between the blocked and
control conditions is the LVA h state."""

import numpy as np
import matplotlib.pyplot as plt
plt.ion()

#######
#
# prepare a list of folders that contain
# data that we will analyze
#
#######

"""
sample data folder:
(python38env) MacBook-Pro-44:Iascone_tonic_gabaar morse$ ls 20251215sent/depol_iclamp_results/20251215vShift_0_LVA_0p6IClamp_amp_index3/data/loc200_m_hva_trace/
loc200_m_hva_apic11_0p969027_blocked.txt	t_vec.txt
loc200_m_hva_apic11_0p969027_control.txt
"""

folders=[
"20251215sent/depol_iclamp_results/20251215vShift_0_LVA_0p6IClamp_amp_index3/data/"    ]

########
#
# read in the data
#
########

"""
get the source data so we can form the following quantities
ratio_h_LVA= blocked_h_LVA/control_h_LVA
ratio_m_LVA= blocked_m_LVA/control_h_LVA
ratio_h_HVA= blocked_h_HVA/control_h_HVA
ratio_m_HVA= blocked_m_HVA/control_m_HVA
"""

for folder in folders: # process any folder in the folders list
    # load in the data
    # HVA
    m_HVA_blocked = np.loadtxt(folder + \
        'loc200_m_hva_trace/loc200_m_hva_apic11_0p969027_blocked.txt')
    m_HVA_control = np.loadtxt(folder + \
        'loc200_m_hva_trace/loc200_m_hva_apic11_0p969027_control.txt')
    h_HVA_blocked = np.loadtxt(folder + \
        'loc200_h_hva_trace/loc200_h_hva_apic11_0p969027_blocked.txt')
    h_HVA_control = np.loadtxt(folder + \
        'loc200_h_hva_trace/loc200_h_hva_apic11_0p969027_control.txt')
    # LVA
    m_LVA_blocked = np.loadtxt(folder + \
        'loc200_m_lva_trace/loc200_m_lva_apic11_0p969027_blocked.txt')
    m_LVA_control = np.loadtxt(folder + \
        'loc200_m_lva_trace/loc200_m_lva_apic11_0p969027_control.txt')
    h_LVA_blocked = np.loadtxt(folder + \
        'loc200_h_lva_trace/loc200_h_lva_apic11_0p969027_blocked.txt')
    h_LVA_control = np.loadtxt(folder + \
        'loc200_h_lva_trace/loc200_h_lva_apic11_0p969027_control.txt')
    # t_vec and blocked and control ca accumulation window (ca signal
    # is added up calcium ions during a 20 ms time window starting at
    # a detection of the soma AP (when the soma membrane v passes 0)).
    t_vec = np.loadtxt(folder + \
        'loc200_m_hva_trace/t_vec.txt')
    ca_accum_win_blocked = np.loadtxt(folder + \
        '../protocol/ca_accum_win_vec0.txt')
    ca_accum_win_control = np.loadtxt(folder + \
        '../protocol/ca_accum_win_vec1.txt')
    # These masks provide the time point indicies during the
    # respective ca accum win
    blocked_mask=(ca_accum_win_blocked ==1)
    control_mask=(ca_accum_win_control ==1)

#######
#
# h_HVA
#
#######
plt.figure(1)
h_HVA_blocked_win=h_HVA_blocked[blocked_mask]
h_HVA_control_win=h_HVA_control[control_mask]

common_t_vec=[round(t,3) for t in np.arange(0, (len(h_HVA_blocked_win)*0.1), 0.1)]
plt.plot(common_t_vec, h_HVA_blocked_win, label='h_HVA blocked')
plt.plot(common_t_vec, h_HVA_control_win, label='h_HVA control') 
plt.xlabel('time relative to Ca accumulation window (ms)')
plt.ylabel('h_HVA (1)')
plt.title('h_HVA during Ca accumulation window')
plt.legend(loc='best')

plt.figure(2)
ratio_h_HVA_blocked2control=h_HVA_blocked_win/h_HVA_control_win
plt.plot(common_t_vec, ratio_h_HVA_blocked2control,
         label='h_HVA blocked/control')
plt.xlabel('time relative to Ca accumulation window (ms)')
plt.ylabel('ratio h_HVA blocked/control during Ca window (1)')
plt.title('blocked/control ratio of h_HVA during Ca accumulation window')
ave_ratio_h_HVA_blocked2control=np.mean(ratio_h_HVA_blocked2control)
ave_ratio_h_HVA = ave_ratio_h_HVA_blocked2control
plt.plot([common_t_vec[0], common_t_vec[-1]],
         [ave_ratio_h_HVA, ave_ratio_h_HVA], label='ave ratio h_HVA')
plt.legend(loc='best')

#######
#
# m_HVA
#
#######
plt.figure(3)

m_HVA_blocked_win=m_HVA_blocked[blocked_mask]
m_HVA_control_win=m_HVA_control[control_mask]

common_t_vec=[round(t,3) for t in np.arange(0, (len(m_HVA_blocked_win)*0.1), 0.1)]
plt.plot(common_t_vec, m_HVA_blocked_win, label='m_HVA blocked')
plt.plot(common_t_vec, m_HVA_control_win, label='m_HVA control') 
plt.xlabel('time relative to Ca accumulation window (ms)')
plt.ylabel('m_HVA (1)')
plt.title('m_HVA during Ca accumulation window')
plt.legend(loc='best')

plt.figure(4)
ratio_m_HVA_blocked2control=m_HVA_blocked_win/m_HVA_control_win
plt.plot(common_t_vec, ratio_m_HVA_blocked2control,
         label='m_HVA blocked/control')
plt.xlabel('time relative to Ca accumulation window (ms)')
plt.ylabel('ratio m_HVA blocked/control during Ca window (1)')
plt.title('blocked/control ratio of m_HVA during Ca accumulation window')
ave_ratio_m_HVA_blocked2control=np.mean(ratio_m_HVA_blocked2control)
ave_ratio_m_HVA = ave_ratio_m_HVA_blocked2control
plt.plot([common_t_vec[0], common_t_vec[-1]],
         [ave_ratio_m_HVA, ave_ratio_m_HVA], label='ave ratio m_HVA')
plt.legend(loc='best')

#######
#
# h_LVA
#
#######
plt.figure(5)

h_LVA_blocked_win=h_LVA_blocked[blocked_mask]
h_LVA_control_win=h_LVA_control[control_mask]

common_t_vec=[round(t,3) for t in np.arange(0, (len(h_LVA_blocked_win)*0.1), 0.1)]
plt.plot(common_t_vec, h_LVA_blocked_win, label='h_LVA blocked')
plt.plot(common_t_vec, h_LVA_control_win, label='h_LVA control') 
plt.xlabel('time relative to Ca accumulation window (ms)')
plt.ylabel('h_LVA (1)')
plt.title('h_LVA during Ca accumulation window')
plt.legend(loc='best')

plt.figure(6)
ratio_h_LVA_blocked2control=h_LVA_blocked_win/h_LVA_control_win
plt.plot(common_t_vec, ratio_h_LVA_blocked2control,
         label='h_LVA blocked/control')
plt.xlabel('time relative to Ca accumulation window (ms)')
plt.ylabel('ratio h_LVA blocked/control during Ca window (1)')
plt.title('blocked/control ratio of h_LVA during Ca accumulation window')
ave_ratio_h_LVA_blocked2control=np.mean(ratio_h_LVA_blocked2control)
ave_ratio_h_LVA = ave_ratio_h_LVA_blocked2control
plt.plot([common_t_vec[0], common_t_vec[-1]],
         [ave_ratio_h_LVA, ave_ratio_h_LVA], label='ave ratio h_LVA')
plt.legend(loc='best')

#######
#
# m_LVA
#
#######
plt.figure(7)

m_LVA_blocked_win=m_LVA_blocked[blocked_mask]
m_LVA_control_win=m_LVA_control[control_mask]

common_t_vec=[round(t,3) for t in np.arange(0, (len(m_LVA_blocked_win)*0.1), 0.1)]
plt.plot(common_t_vec, m_LVA_blocked_win, label='m_LVA blocked')
plt.plot(common_t_vec, m_LVA_control_win, label='m_LVA control') 
plt.xlabel('time relative to Ca accumulation window (ms)')
plt.ylabel('m_LVA (1)')
plt.title('m_LVA during Ca accumulation window')
plt.legend(loc='best')

plt.figure(8)
ratio_m_LVA_blocked2control=m_LVA_blocked_win/m_LVA_control_win
plt.plot(common_t_vec, ratio_m_LVA_blocked2control,
         label='m_LVA blocked/control')
plt.xlabel('time relative to Ca accumulation window (ms)')
plt.ylabel('ratio m_LVA blocked/control during Ca window (1)')
plt.title('blocked/control ratio of m_LVA during Ca accumulation window')
ave_ratio_m_LVA_blocked2control=np.mean(ratio_m_LVA_blocked2control)
ave_ratio_m_LVA = ave_ratio_m_LVA_blocked2control
plt.plot([common_t_vec[0], common_t_vec[-1]],
         [ave_ratio_m_LVA, ave_ratio_m_LVA], label='ave ratio m_LVA')
plt.legend(loc='best')


