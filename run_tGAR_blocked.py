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

file_path = 'data/blocked_tGAR_data.pkl'
if os.path.exists(file_path): os.remove(file_path) # keep in place for
# safety and then try removing to see if get the same result
if os.path.exists(file_path):
    # No work necessary in this script if the above pkl exists.
    # If desired to recreate above pickle file, simply move or delete it
    print(f"blocked tGAR pickle {file_path} exists - ", end='')
    print("(blocked data will be loaded in run_tGAR_control.py)")
else:
    print(f"recreating blocked tGAR pickle {file_path}")
    from setup_tGARs import * # import many functions and setup recordings
    
    #############
    #
    # run with blocked tonic GABAAR
    #
    #############

    h.tstop=400
    set_tonic(0) # block tonic GABAAR.  As in the wetlab experiments
    # use the control tonic GABAAR (tGAR) case depolarizing current
    # clamp amplitude again in this blocked tGAR case.
    depol_iclamp.amp=depol_iv_pairs_dict['control'][amp_index][0]
    h.v_init=depol_iv_pairs_dict['control'][amp_index][1]

    h.init()
    my_run(400)

    #############
    #
    # Store blocked tonic GABAAR V's, ica's, cai's.
    # The key of 0 represents the tonic GABAAR gbar and
    # later other traces get stored in the session record
    # dictionaries under other tonic GABAAR gbar conditions
    #
    #############
    
    tGAR_status = 'blocked' # tonic GABAA Receptor key for dicts
    session_record[tGAR_status]=deepcopy(dendrite_records) # 
    ica_lva_session_record[tGAR_status]=deepcopy(ica_lva_records) # 
    ica_hva_session_record[tGAR_status]=deepcopy(ica_hva_records) # 
    cai_session_record[tGAR_status]=deepcopy(cai_records) #

    g_lva_session_record[tGAR_status]=deepcopy(g_lva_records) #
    g_hva_session_record[tGAR_status]=deepcopy(g_hva_records) #
    m_lva_session_record[tGAR_status]=deepcopy(m_lva_records) #
    h_lva_session_record[tGAR_status]=deepcopy(h_lva_records) #
    m_hva_session_record[tGAR_status]=deepcopy(m_hva_records) #
    h_hva_session_record[tGAR_status]=deepcopy(h_hva_records) #

    soma_v_session_record[tGAR_status]=deepcopy(soma_voltageVector)
    soma_AP_t_session_record[tGAR_status]=deepcopy(AP_t_vec)
    bAP_stimulation_session_record[tGAR_status]=deepcopy(bAP_stimulation_record)

    #############
    #
    # store blocked tonic GABAAR pre bAP V's
    #
    #############

    pre_bAP_index=2000 # corresponds to time 200 ms when current pulse starts

    blocked_soma=[soma_voltageVector[pre_bAP_index]] # list of blocked soma voltage

    blocked_soma_vec = deepcopy(soma_voltageVector)

    # store more general records results of this blocked tonic GABAAR results

    blocked_dend_preAP_v = {} # keys are record distances, values are
    # lists of pre_bAP voltages at those locations
    for location in record_distances:
        blocked_dend_preAP_v[location] = [v_trace.x[pre_bAP_index] for v_trace in
            [v_traces for v_traces in dendrite_records[location]]]

    #############
    #
    # pickle blocked tonic GABAAR variables
    #
    #############

    with open('data/blocked_tGAR_data.pkl', 'wb') as f:
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

