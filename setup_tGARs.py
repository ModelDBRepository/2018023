"""setup_tGARs.py sets up a tonic GABAA receptor model so
tonic_GABAAR_distal.py can examine, by running, the effects of a tonic GABAAR
channel in a modified Iascone et al 2020 model

setup_tGARs.py defines all the functions while tonic_GABAAR_distal.py
runs the model while making modifcations to it such as blocking the
tGAR currents by setting the max conductance to 0 or setting the tGAR
max conductance to particular values.
"""

from run_simulation_python3 import * # modified Iascone et al model to
                                     # have no synaptic activity and
                                     # not run so can modify further
                                     # and run in this file
from g_scale import * # includes g_piecewise_linear
from copy import deepcopy
from pathlib import Path
from write_vec import *
from ap_stats import ap_stat
import matplotlib.pyplot as plt
plt.ion() # interactive plot mode on
from glob import glob
from base_dir_name import base_dir_name

# variable declarations to share between setup_tGARs.py functions
# and setup_GABAAR_distal.py

###############################
#
# X_session_record dicts will have keys of tGARs gbar status
# ('control' or 'blocked'), and then a recording location key inherited
# from an assignment to the recording dictionaries defined further
# below
#
###############################

session_record={} # key (for here and below dicts) are 'control' or
                  # 'blocked' (gbar_exGABALeak), values are either the
                  # dicts with keys of location whose values are
                  # dendrite v recordings, or vectors of recordings at
                  # the soma (such as soma voltage or current clamp
                  # injection).
            
ica_lva_session_record={} # value are the dendrite records of ica_lva
ica_hva_session_record={} # value are the dendrite records of ica_hva
cai_session_record={} # value are cai dendrite records
g_lva_session_record={} # value g_lva dendrite records
g_hva_session_record={} # value g_hva dendrite records
m_lva_session_record={} # value m_lva dendrite records
h_lva_session_record={} # value h_lva dendrite records
m_hva_session_record={} # value m_hva dendrite records
h_hva_session_record={} # value h_hva dendrite records
soma_v_session_record={} # value soma_voltageVector (doesn't have loc keys)
soma_AP_t_session_record={} # value is vector of times of somatic APs
bAP_stimulation_session_record={} # value is IClamp[0].amp time series vec

# NEURON SectionList and python list of sections for general use

dendritic=h.SectionList()
for sec in h.allsec():
    secname=str(sec)
    if 'apic' in secname:
        tmp=dendritic.append(sec)
    if 'dend_7' in secname:
        tmp=dendritic.append(sec)
    if 'dend_5' in secname:
        tmp=dendritic.append(sec)

dendrites=[sec for sec in dendritic] # list to check if sec is a dendrite

def init_soma_cai():
    """Initialize soma cai to 0.104 uM for faster v equilibrium"""
    for sec in h.somatic:
        sec.cai = 10e-5
    for sec in h.axonal:
        sec.cai= 10e-5
    for sec in dendritic:
        sec.cai= 10e-5

# setup some number of AP recording vectors
AP_t_vec=h.Vector() # the times of APs are found by using NetCon's AP detection
netcon=h.NetCon(h.soma(0.5)._ref_v, None, sec=h.soma)
tmp=netcon.record(AP_t_vec)

def myadvance(): # see solo_ap.py where hoc's fadvance is assigned to myadvance
    # if not (round(h.t,1)+10)%10: print(f'h.t={h.t:.0f}') # every 10 ms print
    h.fadvance()
    if len(AP_t_vec) and h.IClamp[0].amp: # if AP appeared and stim on
        h.IClamp[0].amp = 0 # turn off stim when AP appears
        Path(base_dir_name).mkdir( parents=True, exist_ok=True )
        protocol_dir=base_dir_name + "protocol/"
        Path(protocol_dir).mkdir( parents=True, exist_ok=True )
        with open(protocol_dir+'AP_iclamp_endtime.txt', 'a') as f:
            # save the time of the end of the AP current clamp and the
            # name of the calling script and the amp_index which implies
            # what the control target voltage was
            AP_iclamp_endtime = round(h.t, 3) # gets rid of binary
            # imperfections in base 10 time value
            f.write(f"{AP_iclamp_endtime} " + sys.argv[0] + \
                    f"_{amp_index}\n")

# h('proc advance() {nrnpython("myadvance()")}') # nrn.readthedocs.io example

def my_run(tstop):
    h.stdinit()
    init_soma_cai()
    save_iclamp0amp=h.IClamp[0].amp # turn off when AP detected, then restore
    h.continuerun(tstop)
    h.IClamp[0].amp=save_iclamp0amp
    from depol_iclamp import amp_index
    Path(base_dir_name).mkdir( parents=True, exist_ok=True )
    with open(base_dir_name+'num_of_APs.txt', 'a') as f:
        f.write(f"{AP_t_vec.size()} "+sys.argv[0]+f"_{amp_index}\n")
    with open(base_dir_name+'time_of_APs.txt', 'a') as f:
        for element in AP_t_vec:
            f.write(f"{element} "+sys.argv[0]+f"_{amp_index}\n")

def insert_ca():
    for sec in dendrites:
        sec.insert("CaDynamics_E2")
        sec.insert("Ca_LVAst")
        sec.insert("Ca_HVA")
        sec.gCa_LVAstbar_Ca_LVAst = 1e-7 # small max conductances aid studies that manipulate ca chan kinetics
        sec.gCa_HVAbar_Ca_HVA = 1e-7     # by not letting the ca chan affect the membrane v trajectory
    for sec in h.somatic:
        sec.gCa_LVAstbar_Ca_LVAst = 1e-7 # for uniformity changes from default 7.78 pS/um2
        sec.gCa_HVAbar_Ca_HVA = 1e-7  # for uniformity changes from default 3.74 pS/um2
        
print("Documentation:")
print("""apic[] are none-tuft apical dendrites, dend_5[] are tuft dendrites,
dend_7[] are basal dendrites, and dend_0[] are part of soma.""")

h.load_file('rig.ses')
h.load_file('dend_v.ses')
h.load_file('prox_dend_v.ses')
h.load_file('very_prox_dend_v.ses')
h.load_file('rn.hoc')

"""tmp=h.Graph[0].exec_menu("Keep Lines")
tmp=h.Graph[1].exec_menu("Keep Lines")
tmp=h.Graph[2].exec_menu("Keep Lines")
tmp=h.Graph[3].exec_menu("Keep Lines")"""

for sec in dendritic:
    tmp=sec.insert('exGABALeak')

def set_tonic(gbar, verbose=False):
    if verbose:
        print(f'setting gbar_exGABALeak = {gbar*1e4} pS/um2 everywhere')
    for sec in dendritic:
        sec.gbar_exGABALeak = gbar

def set_g_pas(gbar):
    print(f'setting g_pas = {gbar*1e4} pS/um2 everywhere')
    for sec in h.allsec():
        sec.g_pas = gbar

def find_dends(near, far):
    """find_dends(90, 110) will find the dendrite segments whose
location(s) are greater than 90 ums and less than 110 microns from the
soma"""   
    for sec in dendritic:
        for seg in sec:
            distance = h.distance(h.soma(0.5), seg)
            if distance > near and distance < far:
                print(seg, distance)

def find_apical(near, far, send=False):
    """find_apical(near, far, send=False) 
find_apical(90, 110) will find the apical dendrite segments whose
locations are greater than 90 ums and less than 110 microns from the
soma. If send=True is passed then find_apical will return the list of
segments it found in the range between near and far.

    """
    segments=[]
    for sec in h.apical:
        for seg in sec:
            distance = h.distance(h.soma(0.5), seg)
            if distance > near and distance < far:
                if send==False: print(seg, distance)
                segments.append(seg)
    if send:
        return segments

for sec in h.allsec():
    sec.e_pas = -70 # up from -75

#############
#
# setup additional record vectors: the basic idea is these vector
# recordings are (deepcopy) loaded into the session dictionaries after
# a run.  The use of deepcopy allows for values to be preserved when
# the next simulations are run under different conditions (tGARs
# blocked or control).
#
#############

### more complete list of locations:
record_distances=np.array([x for x in range(25, 400, 25)]) # 325 or 400 end
# all the below dicts have keys of record distances from record_distances
dendrite_names={} # values of dendrite names
dendrite_records={} # values of dendrite v trajs
ica_lva_records={} #  values of dendrite ica_Ca_LVAst
ica_hva_records={} # values of dendrite ica_Ca_HVA
cai_records={} # values of dendrite cai

g_lva_records={} # key is record_distances, value g_lva dendrite records
g_hva_records={} # key is record_distances, value g_hva dendrite records
m_lva_records={} # key is record_distances, value m_lva dendrite records
h_lva_records={} # key is record_distances, value h_lva dendrite records
m_hva_records={} # key is record_distances, value m_hva dendrite records
h_hva_records={} # key is record_distances, value h_hva dendrite records

insert_ca() # put ca channels in dendrites so that can record from them

################
#
# create distance_records[location] dictionary of recorded vectors
# and similarly dendrite_names, ica_lva_records, ica_hva_records, cai_records
#
################

print('Compartments that were recorded at these distances from the soma:')

distance_threshold = 0.5
for distance in record_distances:
    segments = find_apical(distance-distance_threshold,
                           distance+distance_threshold, send=True)
    print(distance, segments)
    dendrite_names[distance]=[str(seg) for seg in segments]
    dendrite_records[distance]=[h.Vector().record(seg._ref_v)
                                for seg in segments]
    ica_lva_records[distance]=[
        h.Vector().record(seg._ref_ica_Ca_LVAst)
        for seg in segments]
    ica_hva_records[distance]=[
        h.Vector().record(seg._ref_ica_Ca_HVA)
        for seg in segments]
    cai_records[distance]= [
        h.Vector().record(seg._ref_cai)
    for seg in segments]

    g_lva_records[distance]= [
        h.Vector().record(seg._ref_gCa_LVAst_Ca_LVAst)
    for seg in segments]
    g_hva_records[distance]= [
        h.Vector().record(seg._ref_gCa_Ca_HVA)
    for seg in segments]
    m_lva_records[distance]= [
        h.Vector().record(seg._ref_m_Ca_LVAst)
    for seg in segments]
    h_lva_records[distance]= [
        h.Vector().record(seg._ref_h_Ca_LVAst)
    for seg in segments]
    m_hva_records[distance]= [
        h.Vector().record(seg._ref_m_Ca_HVA)
    for seg in segments]
    h_hva_records[distance]= [
        h.Vector().record(seg._ref_h_Ca_HVA)
    for seg in segments]
    
t_vec=h.Vector().record(h._ref_t)
distal_dend_v=h.Vector().record(h.dend_5[12](1)._ref_v) # record the
# distal v after running can examine the height of the most distal bAP

# Record the bAP stimulation current clamp amplitude during the simulation
bAP_stimulation_record = h.Vector().record(h.IClamp[0]._ref_i)
# Above will be a value in bAP_stimulation_session_record with key tGAR_status.

# run with setting g_pas leak channel here
set_g_pas(3.e-5) # old values 3.85e-5 4.8e-5=(1.6*0.3e-4) # trying
                  # 30% greater
for sec in h.allsec():
    sec.e_pas = -70 # up from -75
    if h.ismembrane('exGABALeak', sec=sec):
        sec.Erev_exGABALeak = -75

# try with SK off
for sec in h.allsec():
    if h.ismembrane('SK_E2', sec=sec):
        sec.gSK_E2bar_SK_E2 = 0

# try doubling Na in the dendrites

for sec in h.apical: # no Na in basal at the moment
    sec.gNaTs2_tbar_NaTs2_t *= 2
        
soma=h.soma # convenience
h.v_init = -65

# turn off h current
for sec in h.allsec():
    if h.ismembrane('Ih', sec=sec):
        sec.gIhbar_Ih=0

# print(f"Rin = {h.rn():.3f},") # running h.rn deletes the recorded v traces
# printing the below stuff is OK however not necessary:
# print(f"{soma(0.5).v:.3f} mV soma," + \
#    f"{soma.g_pas*1e4:0.3f} pS/um2 g_pas and without tonic GABAAR activation")
# index=dendrite_records[25][0].size()-1

# print(f"last element of dendrite_records[25][0] = " + \
#      f"{dendrite_records[25][0].x[index]}")
# print(f"length of a dendrite_record[25][0] = {len(dendrite_records[25][0])}")

tmp=h.Graph[0].exec_menu("Keep Lines")
tmp=h.Graph[1].exec_menu("Keep Lines")
tmp=h.Graph[2].exec_menu("Keep Lines")
tmp=h.Graph[3].exec_menu("Keep Lines")

    
start_loc=200 # for dend distribution of both tonic GABAAR and v-gated Na 
end_loc=378.5 # most distal location is 378.46965982624585 um from soma(0.5)
# from tonic_GABAAR_gbar import tonic_GABAAR_gbar

def passive_axon():
    for sec in h.axonal:
        sec.gCa_HVAbar_Ca_HVA = 0
        sec.gSKv3_1bar_SKv3_1 = 0
        sec.gSK_E2bar_SK_E2 = 0
        sec.gNap_Et2bar_Nap_Et2 = 0
        sec.gK_Pstbar_K_Pst = 0
        sec.gK_Tstbar_K_Tst = 0
        sec.gCa_LVAstbar_Ca_LVAst = 0
        sec.gNaTa_tbar_NaTa_t = 0

passive_axon()
print('set axon to be passive')

def set_dend_nav(gbar):
    """set_dend_nav(gbar) set apical (basal has no nav) nav to gbar"""
    for sec in h.apical:
        sec.gNaTs2_tbar_NaTs2_t = gbar

# for sec in h.somatic:
#       sec.gNaTs2_tbar_NaTs2_t = 2 # try roughly doubling the soma conductance

def rin_deflection():
    h.IClamp[0].dur=200
    h.IClamp[0].amp=-0.1
    h.tstop=500
    h.my_run(h.tstop)

def plot_many(locs='all', legend=False):
    """plot_many(locs='all') can plot all if no locs are sent or
particular locs of the dendrite_records if locs list is supplied as
an argument to the function. locs must be a subset of [25, 50, ...,
275, 300]
"""
    t_vec=[t for t in np.arange(0, h.tstop+h.dt, h.dt)]
    plt.figure()
    if locs=='all':
        for loc in dendrite_records:
            for vec in dendrite_records[loc]:
                tmp = plt.plot(t_vec, vec, label=vec)
        tmp = plt.title('many vectors examples at locs 25, 50, ... 300')
    else:
        for loc in locs:
            for vec, name in zip(dendrite_records[loc], dendrite_names[loc]):
                tmp = plt.plot(t_vec, vec, label=name)
        tmp = plt.title(f'locs={locs}')
    tmp=plt.xlabel('t (ms)')
    tmp=plt.ylabel('v (mV)')
    if legend:
        tmp=plt.legend(loc='best')

def plot_compare(session_record, locs='all', legend=False, number='all', \
                 verbose=False, ylabel='v (mV)', xlim=(0, h.tstop)):
    """plot_compare(session_record, locs='all', legend=False,
number='all', ylabel='v (mV)', xlim=(0, h.tstop)) can plot all
gbar_exGABALeak dendrite_records if no locs list is sent or
particular locs if a list of them is supplied as an argument to the
function. locs must be a subset of [25, 50, ..., 275,
300]. number='all' plots all record vectors at the locs
locations. If number=X then upto X (or the number available if less
than X) record vectors are plotted. Example plot to cut and paste
onto the command line:
for loc in range(25, 325, 25):
    plot_compare(session_record, [loc], number=2, legend=True)
    tmp=plt.xlim((199,210))
>>> record_distances
array([ 25,  50,  75, 100, 125, 150, 175, 200, 225, 250, 275, 300])
for fig, loc in enumerate(record_distances):
    plt.figure(fig+1)
    plt.savefig(f"20240604/loc{loc}.png")

    """
    t_vec=[t for t in np.arange(0, h.tstop+h.dt, h.dt)]
    plt.figure()
    for tGAR_status in session_record: # the keys of the
# session_record are 'blocked' or 'control' (gbar_exGABALeak's) and
# the values are the dendrite record vectors
        if verbose:
            print(f"tGAR_status={tGAR_status}")
        dendrite_records = session_record[tGAR_status]
        if locs=='all':
            for loc in dendrite_records:
                count_plots =0
                for vec in dendrite_records[loc]:
                    tmp = plt.plot(t_vec, vec, label=f'{vec} {tGAR_status}')
                    count_plots += 1
                    if str(type(number))!="<class 'str'>": # assume
                        # number a number if not a string
                        if count_plots >= number: break 
            tmp = plt.title('many vectors examples at locs 25, 50, ... 300')
        else:
            for loc in locs:
                count_plots =0
                for vec, name in zip(dendrite_records[loc], dendrite_names[loc]):
                    count_plots += 1
                    if str(type(number))!="<class 'str'>" and count_plots > number: break
                    # assume number a number if not a string
                    tmp = plt.plot(t_vec, vec, label=f'{name} {tGAR_status}')
            tmp = plt.title(f'locs={locs}')
        tmp=plt.xlabel('t (ms)')
        if legend:
            tmp=plt.legend(loc='best')
        tmp=plt.xlim(xlim[0], xlim[1])
        tmp=plt.ylabel(ylabel)
        tmp=plt.tight_layout()

def rin_result():
    start_v_index = 2000
    stop_v_index = 4000-1
    i=-h.IClamp[0].amp
    return (soma_voltageVector.x[start_v_index]-soma_voltageVector.x[stop_v_index])/i

def ica_Ca_HVA_family():
    for record_distance in record_distances:
        plot_compare(ica_hva_session_record, locs=[record_distance], \
                     number=2, ylabel='ica_Ca_HVA (mA/cm2)', legend=True, \
                     xlim=(200, 220))
        
def ica_Ca_LVA_family():
    for record_distance in record_distances:
        plot_compare(ica_lva_session_record, locs=[record_distance], \
                     number=2, ylabel='ica_Ca_LVAst (mA/cm2)', legend=True, \
                     xlim=(200, 220))
        
def cai_family():
    for record_distance in record_distances:
        plot_compare(cai_session_record, locs=[record_distance], \
                     number=2, ylabel='cai (mM)', legend=True, \
                     xlim=(200, 220))

def save_ca_data():
    """creates and saves ca data figures"""
    basedir='ca_data/'
    figdir=basedir + 'cai/'
    Path(figdir).mkdir( parents=True, exist_ok=True )
    plt.close('all')
    # plot and save cai
    cai_family()
    for num in range(1, 13):
        plt.figure(num)
        plt.savefig(figdir+f'cai_dend_dist_{record_distances[num-1]}.png')
    plt.close('all')
    # plot and save LVA
    figdir=basedir + 'ica_LVA/'
    Path(figdir).mkdir( parents=True, exist_ok=True )
    ica_Ca_LVA_family()
    for num in range(1, 13):
        plt.figure(num)
        plt.savefig(
        figdir+f'ica_Ca_LVAst_dend_dist_{record_distances[num-1]}.png')
    plt.close('all')
    # plot and save HVA
    ica_Ca_HVA_family()
    figdir=basedir + 'ica_HVA/'
    Path(figdir).mkdir( parents=True, exist_ok=True )
    for num in range(1, 13):
        plt.figure(num)
        plt.savefig(
        figdir+f'ica_Ca_HVA_dend_dist_{record_distances[num-1]}.png')
    plt.close('all')

def find_window(AP_t):
    """find_window() will return the start_time_index, end_time_index for
the start and end of a window that ca accumulation is measured.
t_vec.x[start_time_index] will give the ms start time of the ca accum
window and similarly for end_time)index. Example call

start_time_index, end_time_index = find_window(AP_t)

where AP_t is the time in ms that the NetCon AP detector returned (the
time that NetCon observed the soma membrane voltage exceeded a
threshold = 0mV).

    """
    start_time_index = int((AP_t)/h.dt) # start from time of detection of AP
    end_time_index = start_time_index + int(20/h.dt) # 20 ms time window
    return start_time_index, end_time_index

def integrated_charge(send=False, record_keys=['blocked', 'control']):
    """Integrated charge(send=False)

Since the ica currents are in units of mA/cm2
that is the same as (mC/s)*(1/cm2). If we integrate that over one time
step it is multiplying each value by 0.1 ms.

0.1 1e-3 s * (mC/s) * (1/cm2) = 1e-4 mC/cm2

If we add up all the ica currents and multiply by 1e-4 what is left is
in units of mC/cm2.  An important point here is that the calcium
current added is a purposely small amount so that it does not alter
the v trajectory.  This means that the mC/cm2 units are arbitrary
instead.  The purpose of using these small amounts of Ca current were
so that we could explore altering the kinetics and time constants of
the Ca currents to see the difference in calcium currents between
blocked GABAAR and control (not blocked GABAAR) conditions without
altering the membrane v trajectory. This allowed us to study the way
"different" ca channels would provide altered ca signals (GABAAR
dependent).

The data will be stored in dictionary's that have keys of tuples of
distance to the soma and whether blocked (0) or not (e.g. currently 5
pS/um2 tGAR g).

To return the vectors representing the x coordinate (v) and the mean
and std values, set the send parameter to True:
v, delta_ca_hva_mean, delta_ca_hva_std, delta_ca_lva_mean, \
delta_ca_lva_std, hva_ca_num_denom, lva_ca_num_denom, \
delta_ca_total_mean, delta_ca_total_std,=integrated_charge(send=True)

    """
    from base_dir_name import base_dir_name
    # these charge dicts will hold the charge at dendritic locations
    # and tonic GABAAR receptor state (pS/um2) as keys, e.g. (25, 0)
    # and the integrated charge as values.
    ica_hva_charge_mean = {}
    ica_lva_charge_mean = {}
    ica_total_charge_mean = {}
    ica_hva_charge_std = {}
    ica_lva_charge_std = {}
    ica_total_charge_std = {}
    # below are now set relative to the AP time
    # start_time_index = 2000 # 2000 index corresponds to 200 ms
    # end_time_index = 2200 # 2200 index corresponds to 220 ms (dt=0.1)
    ica_hva_sums_dict = {}
    ica_lva_sums_dict = {}
    ica_total_sums_dict = {}
    for tGAR_status in record_keys: # blocked, control find the time
        # of the bAP to make the start and end time indicies
        # relative to the bAP
        AP_t = soma_AP_t_session_record[tGAR_status][0]
        start_time_index, end_time_index = find_window(AP_t)
        print(f"tGAR_status {tGAR_status}")
        print(f"soma peak time {AP_t} start_time_index {start_time_index} "+\
              f"end_time_index {end_time_index}")
        # write the start and end time of ca accumulation window to data folder
        Path(base_dir_name).mkdir( parents=True, exist_ok=True )
        protocol_dir=base_dir_name + "protocol/"
        Path(protocol_dir).mkdir( parents=True, exist_ok=True )
        with open(protocol_dir+'ca_accum_window.txt', 'a') as f:
            ca_accum_starttime = round(t_vec.x[start_time_index], 3) # round
            ca_accum_endtime = round(t_vec.x[end_time_index], 3) # gets
            # rid of binary imperfections in base 10 time value
            f.write(f"{ca_accum_starttime} {ca_accum_endtime} "+\
                    sys.argv[0]+f"_{amp_index}\n")
        # create and write a vector that corresponds to the ca
        # accumulation window
        ca_accum_win_vec=h.Vector()
        t=[x for x in np.arange(0, h.tstop+h.dt, h.dt)]
        X=len(glob(protocol_dir+"ca_accum_win_vec*.txt"))
        win_vec=[1 if (t>=ca_accum_starttime and t<=ca_accum_endtime) \
                 else 0  for t in t_vec]
        write_vec(protocol_dir+f"ca_accum_win_vec{X}.txt", win_vec)
        write_vec(protocol_dir+f"t.txt", t_vec) # all the same
        print(f"we have written {len(win_vec)} sized win_vec")
        print(f"and {len(t_vec)} sized t_vec to")
        print(protocol_dir+f"ca_accum_win_vec{X}.txt and")
        print(protocol_dir+f"t.txt")
        for record_distance in record_distances: # dend position loop
           tuple_key = (record_distance, tGAR_status)
           # calculate the mean and std of ica values at nearby locations
           # ica_hva
           ica_hva_vectors_tmp = \
           ica_hva_session_record[tGAR_status][record_distance]
           ica_hva_sums_list_tmp = []
           for vector in ica_hva_vectors_tmp:
               ica_hva_sums_list_tmp.append(
                  vector.c(start_time_index, end_time_index).sum())
           # ica_lva
           ica_lva_vectors_tmp = \
           ica_lva_session_record[tGAR_status][record_distance]
           ica_lva_sums_list_tmp = []
           for vector in ica_lva_vectors_tmp:
               ica_lva_sums_list_tmp.append(
                  vector.c(start_time_index, end_time_index).sum())
           # sum of ica_hva, ica_lva currents at records near a location
           #ica_total_sums_list_tmp = \
           #     (1-LVA_portion) * np.array(ica_hva_sums_list_tmp) + \
           #    LVA_portion * np.array(ica_lva_sums_list_tmp)
           # need the vectors of the
           # integrated charge (sums) at each location to find the
           # differences between the blocked and control cases later
           ica_hva_sums_dict[tuple_key] = ica_hva_sums_list_tmp
           ica_lva_sums_dict[tuple_key] = ica_lva_sums_list_tmp
           # ica_total_sums_dict[tuple_key] = ica_total_sums_list_tmp
    # graph the results
    plt.figure()
    # fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)
    fig, ax0 = plt.subplots(nrows=1, sharex=True)
    x=np.array(record_distances)
    delta_ca_hva_mean=[]
    delta_ca_lva_mean=[]
    delta_ca_total_mean=[]
    delta_ca_hva_std=[]
    delta_ca_lva_std=[]
    delta_ca_total_std=[]
    # also store the numerators (blocked) and denominators (control) of the
    # integrated Ca2+ currents
    lva_ca_num_denom=[] # a list of lists (see hva comment below)
    hva_ca_num_denom=[] # a list of lists of the numerators and
    # denominators of summed ca at the different dendrites present at
    # the different recording distances (compartments within a
    # threshold like 0.5 um from these points) (25, 50, 75, ...)
    for record_distance in record_distances: # dend position loop
        # charges by the control sum of charges at each dendritic
        # location
        blocked_key=(record_distance, record_keys[0]) # blocked is
        # usually record_keys[0] which represents the tGAR_status
        # value in the blocked case
        control_key=(record_distance, record_keys[1]) # 'control' is
        # usually record_keys[1] which represents the tGAR_status
        # value in the control (normal) case
        delta_ca_hva_vec = [blocked_sum/control_sum for blocked_sum,
                            control_sum in \
                            zip(ica_hva_sums_dict[blocked_key],
                                ica_hva_sums_dict[control_key])]
        delta_ca_hva_mean.append(np.mean(delta_ca_hva_vec))
        delta_ca_hva_std.append(np.std(delta_ca_hva_vec))

        delta_ca_lva_vec = [blocked_sum/control_sum for blocked_sum,
                            control_sum in \
                            zip(ica_lva_sums_dict[blocked_key],
                                ica_lva_sums_dict[control_key])]
        delta_ca_lva_mean.append(np.mean(delta_ca_lva_vec))
        delta_ca_lva_std.append(np.std(delta_ca_lva_vec))

        #delta_ca_total_vec = [blocked_sum/control_sum for blocked_sum,
        #                      control_sum in \
        #                      zip(ica_total_sums_dict[blocked_key],
        #                          ica_total_sums_dict[control_key])]
        #delta_ca_total_mean.append(np.mean(delta_ca_total_vec))
        # delta_ca_total_std.append(np.std(delta_ca_total_vec))
        # numerators and denominators
        hva_ca_num_denom_lists = [[blocked_sum, control_sum] for
                                  blocked_sum, control_sum in \
                                  zip(ica_hva_sums_dict[blocked_key],
                                      ica_hva_sums_dict[control_key])]
        hva_ca_num_denom.append(hva_ca_num_denom_lists)
        lva_ca_num_denom_lists = [[blocked_sum, control_sum] for
                                  blocked_sum, control_sum in \
                                  zip(ica_lva_sums_dict[blocked_key],
                                      ica_lva_sums_dict[control_key])]
        lva_ca_num_denom.append(lva_ca_num_denom_lists)
    # graph the prepared quantities:
    ax0.errorbar(x, delta_ca_hva_mean, yerr=delta_ca_hva_std,
                 lw=1, capsize=2, capthick=1, color='orange', label='HVA only')
    ax0.errorbar(x, delta_ca_lva_mean, yerr=delta_ca_lva_std,
                 lw=1, capsize=2, capthick=1, color='purple', label='LVA only')
    # take average as representative combination
    delta_ca_total_mean = [np.average([delta_ca_hva_tmp, delta_ca_lva_tmp])
                           for delta_ca_hva_tmp, delta_ca_lva_tmp in
                           zip(delta_ca_hva_mean, delta_ca_lva_mean)]
    delta_ca_total_std = [np.average([delta_ca_hva_tmp, delta_ca_lva_tmp])
                           for delta_ca_hva_tmp, delta_ca_lva_tmp in
                           zip(delta_ca_hva_std, delta_ca_lva_std)]
    ax0.errorbar(x, delta_ca_total_mean, yerr=delta_ca_total_std,
                 lw=1, capsize=2, capthick=1, color='black', label='Average')
    plt.ylim(0, 1.7)
    plt.xlim(11.25, 313.75)
    plt.title('Delta Ca2+ HVA LVA')
    plt.xlabel('distance to soma (um)')
    plt.ylabel('Delta Ca2+ (baseline)')
    plt.legend(loc='best')
    from base_dir_name import base_dir_name
    base_dir_label=base_dir_name.replace('/','')
    plt.text(50, 0.2, base_dir_label) # add folder base name to plot to
                                     # report parameters given
    if send:
        # note that x is the voltages along the x axis where the
        # mean's and std's were calculated
        return x, delta_ca_hva_mean, delta_ca_hva_std, delta_ca_lva_mean, \
            delta_ca_lva_std, hva_ca_num_denom, lva_ca_num_denom, \
            delta_ca_total_mean, delta_ca_total_std

def save_suppression(foldername, v, delta_ca_hva_mean,
                     delta_ca_hva_std, delta_ca_lva_mean,
                     delta_ca_lva_std, hva_ca_num_denom,
                     lva_ca_num_denom, \
                     delta_ca_total_mean, delta_ca_total_std):
    """Save the results of 
v, delta_ca_hva_mean, delta_ca_hva_std, delta_ca_lva_mean, \
delta_ca_lva_std, hva_ca_num_denom, lva_ca_num_denom = \
integrated_charge(send=True)
with commands like
foldername='20240610_LVA2/'

save_suppression(foldername, v, delta_ca_hva_mean, delta_ca_hva_std,
                      delta_ca_lva_mean, delta_ca_lva_std,
                      hva_ca_num_denom, lva_ca_num_denom)

    """
    Path(foldername).mkdir(parents=True, exist_ok=True)
    if foldername[-1]!='/':
        foldername += '/'
    for vec, vec_name in zip([v, delta_ca_hva_mean, delta_ca_hva_std, \
                              delta_ca_lva_mean, delta_ca_lva_std, \
                              delta_ca_total_mean, delta_ca_total_std], \
                             ['v', 'delta_ca_hva_mean', 'delta_ca_hva_std',\
                              'delta_ca_lva_mean', 'delta_ca_lva_std',\
                              'delta_ca_total_mean', 'delta_ca_total_std']):
        write_vec(foldername+vec_name+'.txt', vec)
        
def plot_num_denom():
    """plot_num_denom() plots the numerator and denominator of the delta
ca2+.  Plot the numerator (blocked) with red plus signs and the
denominators (control) with blue circles each as a function of
distance from the soma
Run the below to make the variables available for this function:
v, delta_ca_hva_mean, delta_ca_hva_std, delta_ca_lva_mean, \
delta_ca_lva_std, hva_ca_num_denom, lva_ca_num_denom=integrated_charge(send=True)
then can run plot_un_denom().
"""
    ####
    #
    # HVA
    #
    ####
    plt.figure()
    num_means = [] # find the means for numerator and denominator at each
    denom_means = [] #  distance
    for distance, num_denom in zip(record_distances, hva_ca_num_denom):
        for numerator, denominator in num_denom:
            plt.plot(distance, numerator, 'r+')
            plt.plot(distance, denominator, 'bo')
        numerators = [num_denom_pair[0] for num_denom_pair in num_denom] # this distance
        num_means.append(np.mean(numerators))
        denominators = [num_denom_pair[1] for num_denom_pair in num_denom] # this distance
        denom_means.append(np.mean(denominators))
    plt.plot(record_distances, num_means, 'r', label='blocked')
    plt.plot(record_distances, denom_means, 'b', label='control')
    plt.title("HVA numerators (blocked) and denominators (control) of delta Ca2+")
    plt.xlabel("dendrite compartments distances from the soma (um)")
    plt.ylabel("integrated Ca2+ current")
    plt.tight_layout()
    plt.legend(loc='best')
    ####
    #
    # LVA
    #
    ####
    plt.figure()
    num_means = [] # find the means for numerator and denominator at each
    denom_means = [] #  distance
    for distance, num_denom in zip(record_distances, lva_ca_num_denom):
        for numerator, denominator in num_denom:
            plt.plot(distance, numerator, 'r+')
            plt.plot(distance, denominator, 'bo')
        numerators = [num_denom_pair[0] for num_denom_pair in num_denom] # this distance
        num_means.append(np.mean(numerators))
        denominators = [num_denom_pair[1] for num_denom_pair in num_denom] # this distance
        denom_means.append(np.mean(denominators))
    plt.plot(record_distances, num_means, 'r', label='blocked')
    plt.plot(record_distances, denom_means, 'b', label='control')
    plt.title("LVA numerators (blocked) and denominators (control) of delta Ca2+")
    plt.xlabel("dendrite compartments distances from the soma (um)")
    plt.ylabel("integrated Ca2+ current")
    plt.tight_layout()
    plt.legend(loc='best')

def area_past(distance):
    """area_past(distance) calculates the apical dendrite area at or past
a distance (ums from the soma) for use in finding the density of tGARs
if redistributed to that location.
    """
    area=0
    for sec in h.apical:
        for seg in sec:
            d_from_soma = h.distance(h.soma(0.5), seg)
            if d_from_soma >= distance:
                area += seg.area()
    return area

"""
g=0
for sec in dendrites:
    for seg in sec:
        g += seg.gbar_exGABALeak*seg.area()
total_g = g
"""

total_g = 0.4104779607344406 # handy number to have around calculated
# from above when a distal distribution of tGARs of 2 pS/um2 in apical
# from 200 ums from soma to tips. This is the whole cell tGAR
# conductance.

# finish setup of voltage gated Na channel in the dendrites
# set_dend_nav(0)
old_gbar = 0.016018
g_piecewise_linear('d', 'NaTs2_t', start_loc, old_gbar,
                   end_loc, 0,g='gNaTs2_tbar')

# after running can examine the height of the most distal bAPs which
# the above distance (from soma) dependent decrement in v-gated Na
# gbar helps keep bAP maximums not having distance dependent growth.

# information messages that could be nixed:

print(f"""possible functions to use:
g_piecewise_linear('d','exGABALeak', {start_loc}, gbar_exGABALeak, {end_loc}, gbar_exGABALeak)
where gbar_exGABALeak is varied in below loop to the indicated pS/um2 values.
Column Headers: (voltages are in mV)""")
"""print(f"gbar_exGABALeak (pS/um2), Rin MOhm, " + \
   f"mean delta pre-AP soma V+-std, " + \
   f"mean delta pre-AP shaft V at 25 ums+-std, " + \
   f"mean delta pre-AP shaft V at 50 ums+-std, " + \
   f"mean delta pre-AP shaft V at 100 ums+-std")
"""
print(f"gbar_exGABALeak (pS/um2), " + \
   f"mean delta pre-AP V+-std at 25, 50, ..., 300 ums from soma")

def snapshot_tGAR_gbar():
    """As a debugging tool snapshot_tGAR_gbar() provides a list of lists
of distance, gbar_exGABALeak values at distances from the soma
"""
    tGAR_gbar_list = []
    tGAR_dist_list = []
    for sec in h.allsec():
        if h.ismembrane('exGABALeak', sec=sec):
            for seg in sec:
                distance_from_soma = h.distance(seg, h.soma(0.5))
                tGAR_dist_list.append(distance_from_soma)
                tGAR_gbar_list.append(seg.gbar_exGABALeak)
    return tGAR_dist_list, tGAR_gbar_list

def graph_debug_snapshots(track_gbar):
    plt.figure()
    for k in track_gbar:
        plt.plot(track_gbar[k][0], track_gbar[k][1], marker='o', label=k, linestyle='none')
    plt.legend(loc='best')

# adding another current clamp (IClamp), depol_iclamp, that is used to
# depolarize the soma to a target voltage (similarly to the
# experiment, it also stays on for the duration of the
# simulation). This modification to this script is down here because
# earlier portions of this script are rewritten by scripts that set or
# loop over setting e_pas.

from depol_iclamp import * # turns on an iclamp that will be used to depol soma
