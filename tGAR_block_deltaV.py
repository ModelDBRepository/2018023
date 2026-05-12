import matplotlib.pyplot as plt
plt.ion()
import numpy as np
from glob import glob

template_path= \
"20260123vShift_0_LVA_0p6IClamp_amp_index*/data/loc200_v_traces/loc200*"

t_vec_path= \
"20260123vShift_0_LVA_0p6IClamp_amp_index*/data/loc200_v_traces/t*"
t_vecs = glob(t_vec_path)
t_vec = np.loadtxt(t_vecs[0])
# verified that t_vec[2000] = 200 (ms) the last time point before the bAP stim effects
pre_bAP_index = 2000

files = glob(template_path)

blocked_dend_v = {} # dict of pre_bAP v with keys of index for soma control target v
# and 200 um location dendrite name for blocked tonic GABA A receptor (tGAR) sims
control_dend_v = {} # dict of pre_bAP v with keys of index for soma control target v
# and 200 um location dendrite name for control tonic GABA A receptor (tGAR) sims

blocked_dend_list_dict = {} # keys of index value of list of voltages
control_dend_list_dict = {}


for file in files:
    index = int(file.split('index')[1].split('/')[0])
    dend_name = file.split('loc200_')[2].split('_control')[0].split('_block')[0]
    status = file.split('_')[-1].split('.')[0]
    v_trace = np.loadtxt(file)
    if status=='control':
        control_dend_v[(dend_name, index)] = v_trace[pre_bAP_index]
    else:
        blocked_dend_v[(dend_name, index)] = v_trace[pre_bAP_index]
    
ctrl_v_of_index = [i for i in range(-70, -58, 2)]

delta_dend_list_dict = {}  # k of pre_bAP index value of list of delta v's for dends 

for k in control_dend_v:
    pre_bAP_index = k[1]
    dend_name = k[0]
    if pre_bAP_index in delta_dend_list_dict:
        delta_dend_list_dict[pre_bAP_index].append( \
            blocked_dend_v[k] - control_dend_v[k] )
    else:
        delta_dend_list_dict[pre_bAP_index] = [ \
            blocked_dend_v[k] - control_dend_v[k] ]

# delta v fig

plt.figure()

for index in delta_dend_list_dict:
    ctrl_V = ctrl_v_of_index[index]
    for delta_v in delta_dend_list_dict[index]:
        plt.plot(ctrl_V, delta_v, marker='o', linestyle='None', color='black')

plt.title('$\Delta$V')
plt.xlabel('pre bAP v (mV)')
plt.ylabel('$\Delta$V = blocked dend loc 200 - control dend loc 200')
plt.show()

# g_GABA Block (mV) fig

plt.figure()

for k in control_dend_v:
    pre_bAP_index = k[1]
    dend_name = k[0]
    ctrl_V = ctrl_v_of_index[pre_bAP_index]
    plt.plot(ctrl_V, control_dend_v[k], marker='o', linestyle='None', color='black')
    plt.plot(ctrl_V, blocked_dend_v[k], marker='o', linestyle='None', color='red')

plt.title('location 200 um Dendritic Vm')
plt.ylabel('pre bAP Vm (mV) blocked $g_{GABA}$ (red), control (black)')
plt.xlabel('Control soma target Vm (mV)')
plt.show()
        
        
