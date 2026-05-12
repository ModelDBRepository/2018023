"""tonic_GABAAR.py examines the effects of a tonic GABAAR channel in a
modified Iascone et al 2020 model"""

from solo_ap import * # turns off bAP stim once AP detected
from run_simulation_python3 import * # modified Iascone et al model to
                                     # have no synaptic activity and
                                     # not run so can modify further
                                     # and run in this file
from g_scale import * # includes g_piecewise_linear
import matplotlib.pyplot as plt
from copy import deepcopy
from pathlib import Path
from write_vec import *

plt.ion() # interactive plot mode on

from setup_tGARs import * # import many functions and setup recordings

#############
#
# retrieve data from run with blocked tonic GABAAR
#
#############

# simulation data from a run where tGARs were blocked:
blocked_file_path = 'data/blocked_tGAR_data.pkl'
use_file_path = blocked_file_path
    
# using a pickle that contains blocked and/or control (possibly levels of) tGARs
with open(use_file_path, 'rb') as f:
    h.tstop = pickle.load(f)
    session_record.update(pickle.load(f)) # if these are assigned instead of
    # update's then the scope of these dict's are lost in integrated_charge()
    ica_lva_session_record.update(pickle.load(f))
    ica_hva_session_record.update(pickle.load(f))
    cai_session_record.update(pickle.load(f))
    #
    g_lva_session_record.update(pickle.load(f))
    g_hva_session_record.update(pickle.load(f))
    m_lva_session_record.update(pickle.load(f))
    h_lva_session_record.update(pickle.load(f))
    m_hva_session_record.update(pickle.load(f))
    h_hva_session_record.update(pickle.load(f))
    #
    pre_bAP_index = pickle.load(f)
    blocked_soma = pickle.load(f)
    blocked_soma_vec = pickle.load(f)
    record_distances = pickle.load(f)
    blocked_dend_preAP_v = pickle.load(f)
    
#############
#
# run with control tonic GABAAR
#
#############

# already defined in setup_tGARs.py
# start_loc=200 # 200 250 300
# end_loc=378.5 # most distal location is 378.46965982624585 um from soma(0.5)

plt.figure()

# sample gbar_exGABALeak values previously studied in model in
# constant and distal distributions [0.5e-4, 1e-4, 2e-4, 3e-4, 4e-4,
# 10e-4]
 
from tonic_GABAAR_gbar import * # tonic_GABAAR_gbar, control() sets tGAR gbars
control() #
depol_iclamp.amp = depol_iv_pairs_dict['control'][amp_index][0]
h.v_init=depol_iv_pairs_dict['control'][amp_index][1] # -66
my_run(400)

#############
#
# store control tonic GABAAR (tGAR) pre bAP V's
#
#############

# The control(s) is/are always compared to a blocked case (0 pS/um2
# tGAR (gbar_exGABALeak))

control_soma=[soma_voltageVector[pre_bAP_index]] # list of control
                                                 # soma voltage
delta_bAP_V_soma=control_soma[0]-blocked_soma[0]

control_soma_vec = deepcopy(soma_voltageVector)

# store more general records results of this control tonic GABAAR results

control_dend_preAP_v = {} # keys are record distances, values are
# lists of pre_bAP voltages at those locations
for location in record_distances:
    control_dend_preAP_v[location]= [v_trace.x[pre_bAP_index] for v_trace in
        [v_traces for v_traces in deepcopy(dendrite_records[location])]]

delta_bAP_V_dend = {} # keys are record locations, values are
                      # lists of delta V's at those locations
for location in record_distances:
    delta_bAP_V_dend[location]= np.array(control_dend_preAP_v[location]) - \
    np.array(blocked_dend_preAP_v[location])
data= \
[f"{np.mean(delta_bAP_V_dend[x]):.3f}+-{np.std(delta_bAP_V_dend[x]):.3f}"
      for x in delta_bAP_V_dend]
data_string = ', '.join(data)
# for plotting like
# https://stackoverflow.com/questions/22481854/plot-mean-and-standard-deviation
x =record_distances
y = [np.mean(delta_bAP_V_dend[x]) for x in delta_bAP_V_dend]
e = [np.std(delta_bAP_V_dend[x]) for x in delta_bAP_V_dend]
if distribution=='distal':
    plt.errorbar(x, y, yerr=e, fmt='-o',
             label=f"distal")
else:
    plt.errorbar(x, y, yerr=e, fmt='-o',
             label=f"constant")

#############
#
# store control(s) tonic GABAAR V's, ica's, cai's
# 
#############

tGAR_status='control'

session_record[tGAR_status]=deepcopy(dendrite_records)
ica_lva_session_record[tGAR_status]=deepcopy(ica_lva_records)
ica_hva_session_record[tGAR_status]=deepcopy(ica_hva_records)
cai_session_record[tGAR_status]=deepcopy(cai_records)
g_lva_session_record[tGAR_status]=deepcopy(g_lva_records)
g_hva_session_record[tGAR_status]=deepcopy(g_hva_records)
m_lva_session_record[tGAR_status]=deepcopy(m_lva_records)
h_lva_session_record[tGAR_status]=deepcopy(h_lva_records)
m_hva_session_record[tGAR_status]=deepcopy(m_hva_records)
h_hva_session_record[tGAR_status]=deepcopy(h_hva_records)

soma_v_session_record[tGAR_status]=deepcopy(soma_voltageVector)
soma_AP_t_session_record[tGAR_status]=deepcopy(AP_t_vec)
bAP_stimulation_session_record[tGAR_status]=deepcopy(bAP_stimulation_record)

print(f"{distribution} {tGAR_label}, " + data_string)
tmp=plt.title(
f'delta V between blocked and {distribution} control tonic GABAAR')
tmp=plt.ylabel('pre bAP delta V (mV)')
tmp=plt.xlabel('dendritic distance from the soma, no SK')
tmp=plt.legend(loc='best')
tmp=plt.close() # not interested in this figure

# both_tgAR_data.pkl contains both control and blocked simulation data
with open('data/both_tGAR_data.pkl', 'wb') as f:
    pickle.dump(h.tstop, f)
    pickle.dump(session_record,f)
    pickle.dump(ica_lva_session_record, f)
    pickle.dump(ica_hva_session_record, f)
    pickle.dump(cai_session_record, f)
    #
    pickle.dump(g_lva_session_record, f)
    pickle.dump(g_hva_session_record, f)
    pickle.dump(m_lva_session_record, f)
    pickle.dump(h_lva_session_record, f)
    pickle.dump(m_hva_session_record, f)
    pickle.dump(h_hva_session_record, f)
    #
    pickle.dump(pre_bAP_index, f)
    pickle.dump(blocked_soma, f)
    pickle.dump(blocked_soma_vec, f)
    pickle.dump(record_distances, f)
    pickle.dump(blocked_dend_preAP_v, f)
    #
    pickle.dump(control_soma, f)
    pickle.dump(delta_bAP_V_soma, f)
    pickle.dump(control_soma_vec, f)
    pickle.dump(control_dend_preAP_v, f)
    pickle.dump(delta_bAP_V_dend, f)
    pickle.dump(data_string, f)
    pickle.dump(distribution, f)
