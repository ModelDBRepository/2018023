"""figs_incl_suppl.py

Plot figures and supplementary figures
"""

from solo_ap import *
from tonic_GABAAR_distal import *
from base_dir_name import base_dir_name
base_dir_label=base_dir_name.replace('/','')
data_dir=base_dir_name + 'data/' 
Path(data_dir).mkdir( parents=True, exist_ok=True )

def niceify(filename):
    return filename.replace(' ', '').replace('(',''). \
        replace(').','.').replace('.','p').replace('[',''). \
        replace(']','_').replace(')','_').replace('/','_per_')

################################
#
# use the voltage data recorded in session_record to plot
# all v traces loc ums from the soma
#
################################

loc=200
tmp_dir = data_dir+f'/loc{loc}_v_traces/'
Path(tmp_dir).mkdir( parents=True, exist_ok=True )
plt.figure()

for k in ['blocked', 'control']: # blocked and control gbar_exGABALeak
    for i,vec in enumerate(session_record[k][loc]):
        label=f"{dendrite_names[loc][i]} {k}"
        if k=='control': # control in black, blocked in red
            tmp=plt.plot(t_vec, vec, 'k', label=label)
        else:
            tmp=plt.plot(t_vec, vec, 'r', label=label)
        write_vec(tmp_dir+f'loc{loc}_'+niceify(label)+'.txt', vec)
write_vec(tmp_dir+'t_vec.txt', t_vec)
tmp=plt.xlim(195, 235)
tmp=plt.legend(loc='best')
tmp=plt.title(f"bAPs at dendrite locations {loc} ums from soma")
tmp=plt.xlabel('time (ms), soma current injection at 200 ms, '+base_dir_label)
tmp=plt.ylabel('voltage (mV)')
tmp=plt.close() # not interested in this figure

################################
#
# compartments the data we show are from
#
################################

"""Method:

1) insert point process into the cell such as Exp2Syn at locations
data was recorded (this is the only code that needs to be executed the
rest is by using the GUI)
2) In the point process group manager select to view Exp2Syn
3) select each Exp2Syn one at a time and a blue dot appears on the
last Exp2Syn selected
4) select the IClamp to illuminate the soma with a red dot so that the
soma is also learly indicated
5) expand the size of the point process group manager to the biggest
size (on my three monitors) because I have not figured out how to get
a vector graphics version stored yet (saving the point process manager
as a ps file doesn't seem to capture the morphology)
6) screenshot the cell (probably want to use either the Centroid or
Show Diam view.

"""

dendrite_segments={}
for k in dendrite_names:
    segment_list = []
    for segment_name in dendrite_names[k]:
        segment = eval(f'h.{segment_name}')
        segment_list.append(segment)
    dendrite_segments[k] = segment_list

# this example shows an insertion of the Exp2Syn at the locations loc
# um from the soma
syns=[]
for seg in dendrite_segments[loc]:
    syns.append(h.Exp2Syn(seg))

################################
#
# plot a single dendritic trace loc ums from the soma
#
################################

# in case need to reset t_vec
# t_vec=[t for t in np.arange(0, int((vec.size()-1)*h.dt)+h.dt, h.dt)]

# these traces were written to files already above

plt.figure()

member_i=0 # note apic[4](0.297) currently selected by this 0 index

for k in ['blocked', 'control']:
    vec=session_record[k][loc][member_i]
    label=f"{dendrite_names[loc][member_i]} {k}"
    if k=='control':
        tmp=plt.plot(t_vec, vec, 'k', label=label)
    else:
        tmp=plt.plot(t_vec, vec, 'r', label=label)
# these traces were written already above
tmp=plt.xlim(195, 235)
tmp=plt.legend(loc='best')
tmp=plt.title(
    f"bAPs at dendrite {dendrite_names[loc][member_i]} ({loc} ums from soma)")
tmp=plt.xlabel('time (ms), soma current injection at 200 ms, '+base_dir_label)
tmp=plt.ylabel('voltage (mV)')

################################
#

# use the i_ca data recorded in ica_hva_session_record ica_lva_session_record to plot
# all ica traces loc ums from the soma

#
################################


plt.figure()

member_i = 0
for k in ['blocked', 'control']:
    for i, ica_vec_tuple in \
  enumerate(zip(ica_hva_session_record[k][loc],ica_lva_session_record[k][loc])):
        ica_hva = ica_vec_tuple[0]
        ica_lva = ica_vec_tuple[1]
        vec = ica_vec_tuple[0]+ica_vec_tuple[1] # ica_lva + ica_hva
        label=f"{dendrite_names[loc][i]} {k}"
        if k=='control':
            tmp=plt.plot(t_vec, vec, 'k', label=label+" total")
            tmp=plt.plot(t_vec, ica_hva, color="#446ccf", label=label+" HVA") # Han Blue
            tmp=plt.plot(t_vec, ica_lva, color="#b57edc", label=label+" LVA") # Lavender
        else:
            tmp=plt.plot(t_vec, vec, 'r', label=label+" total")
            tmp=plt.plot(t_vec, ica_hva, '#C90016', label=label+" HVA") # Harvard Crimson
            tmp=plt.plot(t_vec, ica_lva, '#B5651D', label=label+" LVA") # Light Brown

tmp=plt.xlim(195, 235)
tmp=plt.legend(loc='best')
tmp=plt.title(f"ica at dendrite locations {loc} ums from soma")
tmp=plt.xlabel('time (ms), soma current injection at 200 ms, '+base_dir_label)
tmp=plt.ylabel('ica = ica_lva + ica_hva (mA/cm2)')
plt.close() # not interested in these now

################################
#
# use the i_ca data recorded in ica_hva_session_record
# ica_lva_session_record to plot example ica traces loc ums from the
# soma
#
################################

tmp_dir = data_dir+f'/loc{loc}_ica_trace/'
Path(tmp_dir).mkdir( parents=True, exist_ok=True )
plt.figure()
color_dict={'blocked':'red', 'control':'black'}
for k in ['blocked', 'control']:
    ica_vec_tuple = (ica_hva_session_record[k][loc][member_i],
                     ica_lva_session_record[k][loc][member_i])
    vec = ica_vec_tuple[0]+ica_vec_tuple[1] # ica_lva + ica_hva
    label=f"{dendrite_names[loc][member_i]} {k}"
    if k=='control':
        tmp=plt.plot(t_vec, vec, 'k', label=label+" total")
    else:
        tmp=plt.plot(t_vec, vec, 'r', label=label+" total")
    write_vec(tmp_dir+f'loc{loc}_ica_'+niceify(label)+'.txt', vec)
    # 
    # optionally display and store HVA, LVA components
    ica_hva = ica_vec_tuple[0]
    ica_lva = ica_vec_tuple[1]
    vec = ica_vec_tuple[0]+ica_vec_tuple[1] # ica_lva + ica_hva
    label=f"{dendrite_names[loc][member_i]} {k}"
    if k=='control':
        tmp=plt.plot(t_vec, ica_hva, color="#446ccf", label=label+" HVA") # Han Blue
        tmp=plt.plot(t_vec, ica_lva, color="#b57edc", label=label+" LVA") # Lavender
    else:
        tmp=plt.plot(t_vec, ica_hva, 'orange', label=label+" HVA")
        tmp=plt.plot(t_vec, ica_lva, '#B5651D', label=label+" LVA") # Light Brown
    write_vec(tmp_dir+f'loc{loc}_ica_'+niceify(label)+'HVA.txt', ica_hva)
    write_vec(tmp_dir+f'loc{loc}_ica_'+niceify(label)+'LVA.txt', ica_lva)
    # prepare to add the ca accumulation window to the graph
    AP_t = soma_AP_t_session_record[k][0]
    start_time_index, end_time_index = find_window(AP_t)
    ca_accum_starttime = round(t_vec.x[start_time_index], 3) # round
    ca_accum_endtime = round(t_vec.x[end_time_index], 3) # gets
    # rid of binary imperfections in base 10 time value
    # add the ca accumulation window to the graph
    plt.plot([0, ca_accum_starttime, ca_accum_starttime, ca_accum_endtime, \
              ca_accum_endtime, h.tstop], \
             [0, 0, -1e-6, -1e-6, 0, 0], color=color_dict[k], linewidth=0.5, \
             label=f"ca accum window {k}")
    # the calc_ca_suppr.py writes this ca accum window data with 0 and
    # 1's instead and with the same time points as the simulation to
    # the protocol folder
write_vec(tmp_dir+'t_vec.txt', t_vec)
tmp=plt.xlim(195, 235)
tmp=plt.legend(loc='best')
tmp=plt.title(f"ica at dendrite locations {loc} ums from soma")
tmp=plt.xlabel('time (ms), soma current injection at 200 ms, '+base_dir_label)
tmp=plt.ylabel('ica = ica_lva + ica_hva (mA/cm2)')

################################
#
# plot a single g_lva dendritic trace loc ums from the soma
#
################################

# in case need to reset t_vec
# t_vec=[t for t in np.arange(0, int((vec.size()-1)*h.dt)+h.dt, h.dt)]

tmp_dir = data_dir+f'/loc{loc}_g_lva_trace/'
Path(tmp_dir).mkdir( parents=True, exist_ok=True )
plt.figure()

member_i=0

for k in ['blocked', 'control']:
    vec=g_lva_session_record[k][loc][member_i]
    label=f"{dendrite_names[loc][member_i]} {k}"
    if k=='control':
        tmp=plt.plot(t_vec, vec, 'k', label=label)
    else:
        tmp=plt.plot(t_vec, vec, 'r', label=label)
    write_vec(tmp_dir+f'loc{loc}_g_lva_'+niceify(label)+'.txt', vec)
write_vec(tmp_dir+'t_vec.txt', t_vec)
tmp=plt.xlim(195, 235)
tmp=plt.legend(loc='best')
tmp=plt.title(
    f"g_LVA at dendrite {dendrite_names[loc][member_i]} ({loc} ums from soma)")
tmp=plt.xlabel('time (ms), soma current injection at 200 ms, '+base_dir_label)
tmp=plt.ylabel('conductance (S/cm2)')

################################
#
# plot a single g_hva dendritic trace loc ums from the soma
#
################################

# in case need to reset t_vec
# t_vec=[t for t in np.arange(0, int((vec.size()-1)*h.dt)+h.dt, h.dt)]

tmp_dir = data_dir+f'/loc{loc}_g_hva_trace/'
Path(tmp_dir).mkdir( parents=True, exist_ok=True )

plt.figure()

member_i=0

for k in ['blocked', 'control']:
    vec=g_hva_session_record[k][loc][member_i]
    label=f"{dendrite_names[loc][member_i]} {k}"
    if k=='control':
        tmp=plt.plot(t_vec, vec, 'k', label=label)
    else:
        tmp=plt.plot(t_vec, vec, 'r', label=label)
    write_vec(tmp_dir+f'loc{loc}_g_hva_'+niceify(label)+'.txt', vec)
write_vec(tmp_dir+'t_vec.txt', t_vec)

tmp=plt.xlim(195, 235)
tmp=plt.legend(loc='best')
tmp=plt.title(
    f"g_HVA at dendrite {dendrite_names[loc][member_i]} ({loc} ums from soma)")
tmp=plt.xlabel('time (ms), soma current injection at 200 ms, '+base_dir_label)
tmp=plt.ylabel('conductance (S/cm2)')

################################
#
# plot a single m_lva dendritic trace loc ums from the soma
#
################################

# in case need to reset t_vec
# t_vec=[t for t in np.arange(0, int((vec.size()-1)*h.dt)+h.dt, h.dt)]

tmp_dir = data_dir+f'/loc{loc}_m_lva_trace/'
Path(tmp_dir).mkdir( parents=True, exist_ok=True )
plt.figure()

member_i=0

for k in ['blocked', 'control']:
    vec=m_lva_session_record[k][loc][member_i]
    label=f"{dendrite_names[loc][member_i]} {k}"
    if k=='control':
        tmp=plt.plot(t_vec, vec, 'k', label=label)
    else:
        tmp=plt.plot(t_vec, vec, 'r', label=label)
    write_vec(tmp_dir+f'loc{loc}_m_lva_'+niceify(label)+'.txt', vec)
write_vec(tmp_dir+'t_vec.txt', t_vec)

tmp=plt.xlim(195, 235)
tmp=plt.ylim(0, 1)
tmp=plt.legend(loc='best')
tmp=plt.title(
    f"m_LVA at dendrite {dendrite_names[loc][member_i]} ({loc} ums from soma)")
tmp=plt.xlabel('time (ms), soma current injection at 200 ms, '+base_dir_label)
tmp=plt.ylabel('m activation gate (1)')

################################
#
# plot a single h_lva dendritic trace loc ums from the soma
#
################################

# in case need to reset t_vec
# t_vec=[t for t in np.arange(0, int((vec.size()-1)*h.dt)+h.dt, h.dt)]

tmp_dir = data_dir+f'/loc{loc}_h_lva_trace/'
Path(tmp_dir).mkdir( parents=True, exist_ok=True )
plt.figure()

member_i=0

for k in ['blocked', 'control']:
    vec=h_lva_session_record[k][loc][member_i]
    label=f"{dendrite_names[loc][member_i]} {k}"
    if k=='control':
        tmp=plt.plot(t_vec, vec, 'k', label=label)
    else:
        tmp=plt.plot(t_vec, vec, 'r', label=label)
    write_vec(tmp_dir+f'loc{loc}_h_lva_'+niceify(label)+'.txt', vec)
write_vec(tmp_dir+'t_vec.txt', t_vec)

tmp=plt.xlim(195, 235)
tmp=plt.ylim(0, 1)
tmp=plt.legend(loc='best')
tmp=plt.title(
    f"h_LVA at dendrite {dendrite_names[loc][member_i]} ({loc} ums from soma)")
tmp=plt.xlabel('time (ms), soma current injection at 200 ms, '+base_dir_label)
tmp=plt.ylabel('h activation gate (1)')

################################
#
# plot a single m_hva dendritic trace loc ums from the soma
#
################################

# in case need to reset t_vec
# t_vec=[t for t in np.arange(0, int((vec.size()-1)*h.dt)+h.dt, h.dt)]

tmp_dir = data_dir+f'/loc{loc}_m_hva_trace/'
Path(tmp_dir).mkdir( parents=True, exist_ok=True )
plt.figure()

member_i=0

for k in ['blocked', 'control']:
    vec=m_hva_session_record[k][loc][member_i]
    label=f"{dendrite_names[loc][member_i]} {k}"
    if k=='control':
        tmp=plt.plot(t_vec, vec, 'k', label=label)
    else:
        tmp=plt.plot(t_vec, vec, 'r', label=label)
    write_vec(tmp_dir+f'loc{loc}_m_hva_'+niceify(label)+'.txt', vec)
write_vec(tmp_dir+'t_vec.txt', t_vec)

tmp=plt.xlim(195, 235)
tmp=plt.ylim(0, 1)
tmp=plt.legend(loc='best')
tmp=plt.title(
    f"m_HVA at dendrite {dendrite_names[loc][member_i]} ({loc} ums from soma)")
tmp=plt.xlabel('time (ms), soma current injection at 200 ms, '+base_dir_label)
tmp=plt.ylabel('m activation gate (1)')

################################
#
# plot a single h_hva dendritic trace loc ums from the soma
#
################################

# in case need to reset t_vec
# t_vec=[t for t in np.arange(0, int((vec.size()-1)*h.dt)+h.dt, h.dt)]

tmp_dir = data_dir+f'/loc{loc}_h_hva_trace/'
Path(tmp_dir).mkdir( parents=True, exist_ok=True )
plt.figure()

member_i=0

for k in ['blocked', 'control']:
    vec=h_hva_session_record[k][loc][member_i]
    label=f"{dendrite_names[loc][member_i]} {k}"
    if k=='control':
        tmp=plt.plot(t_vec, vec, 'k', label=label)
    else:
        tmp=plt.plot(t_vec, vec, 'r', label=label)
    write_vec(tmp_dir+f'loc{loc}_h_hva_'+niceify(label)+'.txt', vec)
write_vec(tmp_dir+'t_vec.txt', t_vec)

tmp=plt.xlim(195, 235)
tmp=plt.ylim(0, 1)
tmp=plt.legend(loc='best')
tmp=plt.title(
    f"h_HVA at dendrite {dendrite_names[loc][member_i]} ({loc} ums from soma)")
tmp=plt.xlabel('time (ms), soma current injection at 200 ms, '+base_dir_label)
tmp=plt.ylabel('h activation gate (1)')


################################
#
# plot soma v traces
#
################################

# for figure 3B v traces

tmp_dir = data_dir+f'/soma_v_trace/'
Path(tmp_dir).mkdir( parents=True, exist_ok=True )
plt.figure()
tmp=plt.plot(t_vec, control_soma_vec, 'k', label=f"soma control")
write_vec(tmp_dir+f'soma_v_control.txt', control_soma_vec)
tmp=plt.plot(t_vec, blocked_soma_vec, 'r', label=f"soma blocked tGARs")
write_vec(tmp_dir+f'soma_v_blocked.txt', blocked_soma_vec)
write_vec(tmp_dir+'t_vec.txt', t_vec)
write_vec(tmp_dir+'bAP_stimulation_control.txt',
          bAP_stimulation_session_record['control'])
write_vec(tmp_dir+'bAP_stimulation_blocked.txt',
          bAP_stimulation_session_record['blocked'])

# add the bAP stimulus current clamp amplitude as a trace to the
# soma v plot
tmp=plt.plot(t_vec, bAP_stimulation_session_record['control'].c().mul(10),
             'k', label=f"bAP stimulus control", linewidth=0.5)
tmp=plt.plot(t_vec, bAP_stimulation_session_record['blocked'].c().mul(10),
             'r', label=f"bAP stimulus blocked tGARs", linewidth=0.5)

pre_pulse_index=2000 # corresponds to time 200 ms when current pulse starts
pre_bAP_control=control_soma_vec[pre_pulse_index]
pre_bAP_blocked=blocked_soma_vec[pre_pulse_index]

tmp=plt.xlim(195, 235)
tmp=plt.ylim(-75, 50)
tmp=plt.legend(loc='best')
tmp=plt.title(
    f"Soma voltage during control and blocked tonic GABAARs (tGARs)")
tmp=plt.xlabel('time (ms), soma current injection at 200 ms, '+base_dir_label)
tmp=plt.ylabel("voltage (mV), pre bAP V's "+ \
               f"{pre_bAP_control:.2f}, {pre_bAP_blocked:.2f}")

################################
#
# Make Rin measurement from hyperpol current injection
#
################################

# Currently the model simulations ran last with tGARs in place so it
# is convenient to measure the Rin in this (control) case - especially
# since this method will work regardless of whether a constant or a
# distal distribution is selected.

# Setup the run for equilibration (100 ms), pre-current clamp
# injection (100 ms), the hyperpolarizing current injection (200 ms)
# and after the current injection (100 ms) to both measure the Rin and
# make a figure of the voltage traces containing the hyperpolarizing
# current injection.

h.tstop = 500 # a sum of the above time intervals

h.IClamp[0].delay = 200
h.IClamp[0].dur = 200
h.IClamp[0].amp = -0.05 # an arbitrary small hyperpolarizing current
                        # injection
###############
#
# run model with control tGARs to measure Rin
#
###############
               
h.init()
# set the depolarizing iclamp to the control level:
depol_iclamp.amp = depol_iv_pairs_dict['control'][amp_index][0]
h.v_init=depol_iv_pairs_dict['control'][amp_index][1] # -66

h.my_run(h.tstop)

# store control hyperpolarizing pulse response for measure Rin_control
control_Rin_v_vec = deepcopy(soma_voltageVector)
pre_pulse_index=2000 # corresponds to time 200 ms when current pulse starts
post_pulse_index=4000 # corresponds to time 400 ms when current pulse ends

# below numerator made negative to cancel negative in denominator to
# make overall possitive
control_Rin = \
    (control_Rin_v_vec[post_pulse_index]-control_Rin_v_vec[pre_pulse_index]) \
                              / h.IClamp[0].amp
pre_bAP_control=control_Rin_v_vec[pre_pulse_index]

###############
#
# run model with blocked tGARs with control depol iclamp to measure Rin
# at the new v levels in the soma and dendrites (wetlab analog).
#
###############

set_tonic(0) # turn off apical tGARs

h.init()
# set the depolarizing current to the control level as in the wetlab
# experiments for the blocked state
depol_iclamp.amp=depol_iv_pairs_dict['control'][amp_index][0]
h.v_init=depol_iv_pairs_dict['control'][amp_index][1]

h.my_run(h.tstop)

# store blocked hyperpolarizing pulse response for measure Rin_blocked
blocked_Rin_v_vec = deepcopy(soma_voltageVector)
pre_pulse_index=2000 # corresponds to time 200 ms when current pulse starts
post_pulse_index=4000 # corresponds to time 400 ms when current pulse ends

# below numerator made negative to cancel negative in denominator to
# make overall possitive
blocked_Rin = \
    (blocked_Rin_v_vec[post_pulse_index]-blocked_Rin_v_vec[pre_pulse_index]) \
                              / h.IClamp[0].amp
pre_bAP_blocked=blocked_Rin_v_vec[pre_pulse_index]

print(f"Control Rin = {control_Rin}, blocked_Rin = {blocked_Rin}")

###############
#
# run model with blocked tGARs at the control target v to measure Rin
# for what the blocked tGARs contributes at the target voltage (curiosity)
#
###############

set_tonic(0) # turn off apical tGARs

h.init()
# set the depolarizing current to the blocked level
depol_iclamp.amp=depol_iv_pairs_dict['blocked'][amp_index][0]
h.v_init=depol_iv_pairs_dict['blocked'][amp_index][1]

h.my_run(h.tstop)

# store blocked hyperpolarizing pulse response for measure Rin_blocked
blocked_Rin_v_vec2 = deepcopy(soma_voltageVector)
pre_pulse_index=2000 # corresponds to time 200 ms when current pulse starts
post_pulse_index=4000 # corresponds to time 400 ms when current pulse ends

# below numerator made negative to cancel negative in denominator to
# make overall possitive
blocked_Rin2 = \
    (blocked_Rin_v_vec2[post_pulse_index]-blocked_Rin_v_vec2[pre_pulse_index]) \
                              / h.IClamp[0].amp
pre_bAP_blocked2=blocked_Rin_v_vec2[pre_pulse_index]

print("For blocked tGARs when soma at control target v, blocked_Rin2 = "+\
      f"{blocked_Rin2}")

################################
#
# plot soma v traces during Rin measurement
#
################################

# for figure 3B v traces inset
# The excerpt goes from 100 ms before the current clamp to the end of the sim.
t_vec_excerpt=\
[t for t in np.arange(h.IClamp[0].delay-100, h.tstop+h.dt, h.dt)]

tmp_dir = data_dir+f'/soma_Rin_v_trace/'
Path(tmp_dir).mkdir( parents=True, exist_ok=True )
plt.figure()
label=f"control Rin={control_Rin:4.1f} MOhm"
vec=np.array(control_Rin_v_vec)[1000:5001]
tmp=plt.plot(t_vec_excerpt, vec, 'k', label=label)
write_vec(tmp_dir+f'soma_v_'+niceify(label)+'.txt', vec)
write_vec(tmp_dir+'t_vec_matching', t_vec_excerpt) # matching v_trace data

vec=np.array(blocked_Rin_v_vec)[1000:5001]
label=f"blocked tGARs Rin={blocked_Rin:4.1f} MOhm"
tmp=plt.plot(t_vec_excerpt, vec, 'r', label=label)

write_vec(tmp_dir+f'soma_v_'+niceify(label)+'.txt', vec)

vec=np.array(blocked_Rin_v_vec2)[1000:5001]
label=f"blocked tGARs at ctrl v Rin2={blocked_Rin:4.1f} MOhm"
tmp=plt.plot(t_vec_excerpt, vec, 'r', label=label)

write_vec(tmp_dir+f'soma_v_'+niceify(label)+'.txt', vec)

tmp=plt.xlim(100, 500)
tmp=plt.ylim(-75, -50)
tmp=plt.legend(loc='best')
tmp=plt.title(
    f"Rin measurement from soma v during control and blocked tGARs")
tmp=plt.xlabel("time (ms), 0.05 nA hyperpolarizing injection at 200 ms, " + \
               f"Rin ratio = {control_Rin/blocked_Rin:4.2f}, "+base_dir_label)
tmp=plt.ylabel("voltage (mV), pre bAP V's "+\
        f"{pre_bAP_control:.2f}, {pre_bAP_blocked2:.2f}, {pre_bAP_blocked:.2f}")

################################
#
# plot soma pre-bAP v's as equilibrium v (Fig 3C)
#
################################

"""Here are the relevant stored quantities:
blocked_soma=[soma_voltageVector[pre_bAP_index]] # list of blocked soma voltage

# store more general records results of this blocked tonic GABAAR results

blocked_dend_preAP_v = {} # values are record distances, values are
# lists of pre_bAP voltages at those locations
for location in record_distances:
    blocked_dend_preAP_v[location] = lists of pre bAP voltages at that location
		       
# control soma pre bAP voltage
control_soma=[soma_voltageVector[pre_bAP_index]]

    for location in record_distances:
control_dend_preAP_v[location] = lists of pre bAP voltages at that location
"""
tmp_dir = data_dir+f'/preAP_v_soma_and_apical/'
Path(tmp_dir).mkdir( parents=True, exist_ok=True )
plt.figure()

# legend not needed for this because red blocked, black control

# plot soma control and blocked pre bAP v

plt.plot(0,blocked_soma, 'ro', linewidth=2, markersize=4)
plt.plot(0,control_soma, 'ko', linewidth=2, markersize=4)
with open(tmp_dir+'blocked_soma_v.txt', 'w') as f:
    f.write(f"{blocked_soma}\n")
with open(tmp_dir+'control_soma_v.txt', 'w') as f:
    f.write(f"{control_soma}\n")
    
# plot dend control and blocked pre bAP v's with errorbars

x =record_distances

# first find statistics for each record distance then plot

# control voltages first
y = np.array([np.mean(control_dend_preAP_v[dist]) for dist in record_distances])
e = np.array([np.std(control_dend_preAP_v[dist]) for dist in record_distances])
label=f"{distribution} distribution"
if distribution=='distal':
    tmp=plt.errorbar(x, y, yerr=e, linestyle='None', fmt='-ko', label=label)
else:
    tmp=plt.errorbar(x, y, yerr=e, fmt='-ko', label=label)
write_vec(tmp_dir+'mean_'+niceify(label)+'.txt', y)
write_vec(tmp_dir+'std_'+niceify(label)+'.txt', e)
    
# blocked voltages second
y = np.array([np.mean(blocked_dend_preAP_v[dist]) for dist in record_distances])
e = np.array([np.std(blocked_dend_preAP_v[dist]) for dist in record_distances])
# there is only one blocked tGAR distribution: 0 pS/um2 everywhere
label=f"blocked"
tmp=plt.errorbar(x, y, yerr=e, fmt='-ro', label=label)
write_vec(tmp_dir+'mean_'+niceify(label)+'.txt', y)
write_vec(tmp_dir+'std_'+niceify(label)+'.txt', e)

tmp=plt.title('Equilibrium Apical Dendrite V vs Distance from the Soma')
tmp=plt.xlabel('distance to the soma (um), '+base_dir_label)
tmp=plt.ylabel('v (mV)')

###########
#
# save all open figs in a fig folder
#
###########

named_figs_folder=base_dir_name+'figs/'

Path(named_figs_folder).mkdir( parents=True, exist_ok=True )
for i in plt.get_fignums():
    tmp=plt.figure(i)
    ax=plt.gca()
    print(ax.get_title())
    tmp_title=(ax.get_title() + '.').replace(' ', '').replace('(',''). \
        replace(').','.').replace('.','p').replace('[',''). \
        replace(']','_').replace(')','_')+'png'
    tmp=plt.savefig(named_figs_folder + tmp_title.replace('ppng', '.png'))
    tmp=plt.savefig(named_figs_folder + tmp_title.replace('ppng', '.png').replace('png', 'pdf')) # also write pdfs
