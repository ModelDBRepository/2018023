"""tonic_GABAAR.py examines the effects of a tonic GABAAR channel in a
modified Iascone et al 2020 model"""

from run_simulation_python3 import * # modified Iascone et al model to
                                     # have no synaptic activity and
                                     # not run so can modify further
                                     # and run in this file
import matplotlib.pyplot as plt
plt.ion() # interactive plot mode on

def init_soma_cai():
    """Initialize soma cai to 0.104 uM"""
    for sec in h.somatic:
        sec.cai = 10e-5
    for sec in h.axonal:
        sec.cai= 10e-5
        
def my_run(tstop):
    h.stdinit()
    init_soma_cai()
    h.continuerun(tstop)

h(""" 
objref p
p = new PythonObject()
proc my_run() {
p.my_run($1)
}""")

print("press Init in run control if don't want backwards going line with Keep Lines")
print("""apic are none-tuft apical dendrites, dend_5 are tuft dendrites, and
dend_7 are basal dendrites""")

h.load_file('rig.ses')
h.load_file('dend_v.ses')
h.load_file('prox_dend_v.ses')
h.load_file('very_prox_dend_v.ses')
dendritic=h.SectionList()
for sec in h.allsec():
    secname=str(sec)
    if 'apic' in secname:
        tmp=dendritic.append(sec)
    if 'dend_7' in secname:
        tmp=dendritic.append(sec)
    if 'dend_5' in secname:
        tmp=dendritic.append(sec)

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

for sec in h.allsec():
    sec.e_pas = -70 # up from -75

#############
#
# setup additional recording vectors
#
#############
dend_100=[] # list of 100 um from the soma recording points
dend_100.append(h.Vector().record(h.apic[5](0.5)._ref_v))
dend_100.append(h.Vector().record(h.apic[8](0.5)._ref_v))
dend_100.append(h.Vector().record(h.apic[12](0.5)._ref_v))
dend_100.append(h.Vector().record(h.apic[24](0.5)._ref_v))
dend_100.append(h.Vector().record(h.apic[25](0.5)._ref_v))
dend_100.append(h.Vector().record(h.apic[28](0.5)._ref_v))
dend_100.append(h.Vector().record(h.dend_7[5](0.5)._ref_v))
dend_100.append(h.Vector().record(h.dend_7[21](0.5)._ref_v))
dend_50=[]
dend_50.append(h.Vector().record(h.apic[19](0.5)._ref_v))
dend_50.append(h.Vector().record(h.dend_7[39](0.5)._ref_v))
dend_50.append(h.Vector().record(h.dend_7[41](0.5)._ref_v))
dend_50.append(h.Vector().record(h.dend_7[49](0.5)._ref_v))
dend_25=[]
dend_25.append(h.Vector().record(h.apic[1](0.5)._ref_v))
dend_25.append(h.Vector().record(h.apic[22](0.5)._ref_v))
dend_25.append(h.Vector().record(h.dend_7[10](0.5)._ref_v))
dend_25.append(h.Vector().record(h.dend_7[34](0.5)._ref_v))
dend_25.append(h.Vector().record(h.dend_7[40](0.5)._ref_v))

#############
#
# run with blocked tonic GABAAR
#
#############

h.tstop=400
# run with 2 pS/um2 g_pas
set_g_pas(2e-4)
set_tonic(0)
h.v_init = -60.3
my_run(400) # not necessary to run

tmp=h.Graph[0].exec_menu("Keep Lines")
tmp=h.Graph[1].exec_menu("Keep Lines")
tmp=h.Graph[2].exec_menu("Keep Lines")
tmp=h.Graph[3].exec_menu("Keep Lines")

#############
#
# store blocked tonic GABAAR pre bAP V's
#
#############
pre_bAP_index=2000 # corresponds to time 200 which is when current pulse starts

blocked_soma=[soma_voltageVector[pre_bAP_index]] # list of blocked soma voltage
blocked_dend_100=[] # list of blocked_dend_100
blocked_dend_50=[] # list of blocked_dend_50
blocked_dend_25=[] # list of blocked_dend_25

for vector in dend_100:
    blocked_dend_100.append(vector[pre_bAP_index])
for vector in dend_50:
    blocked_dend_50.append(vector[pre_bAP_index])
for vector in dend_25:
    blocked_dend_25.append(vector[pre_bAP_index])

#############
#
# run with control tonic GABAAR
#
#############
gbar_exGABALeak=3e-4
# sample gbar_exGABALeak values to study in model
[0.5e-4, 1e-4, 2e-4, 4e-4, 10e-4]
for gbar_exGABALeak in []:
    set_tonic(gbar_exGABALeak)
    h.v_init=-66
    my_run(400)

    #############
    #
    # store control tonic GABAAR pre bAP V's
    #
    #############

    control_soma=[soma_voltageVector[pre_bAP_index]] # list of control
                                                     # soma voltage
    control_dend_100=[] # list of control_dend_100
    control_dend_50=[] # list of control_dend_50
    control_dend_25=[] # list of control_dend_25

    for vector in dend_100:
        control_dend_100.append(vector[pre_bAP_index])
    for vector in dend_50:
        control_dend_50.append(vector[pre_bAP_index])
    for vector in dend_25:
        control_dend_25.append(vector[pre_bAP_index])

    delta_bAP_V_soma=control_soma[0]-blocked_soma[0]
    delta_bAP_V_dend_100=[]
    for element in zip(control_dend_100, blocked_dend_100):
        delta_bAP_V_dend_100.append(element[0]-element[1])
    delta_bAP_V_dend_50=[]
    for element in zip(control_dend_50, blocked_dend_50):
        delta_bAP_V_dend_50.append(element[0]-element[1])
    delta_bAP_V_dend_25=[]
    for element in zip(control_dend_25, blocked_dend_25):
        delta_bAP_V_dend_25.append(element[0]-element[1])


    print(f"{gbar_exGABALeak*1e4}, " + \
   f"{np.mean(delta_bAP_V_soma):.3f}+-{np.std(delta_bAP_V_soma):.3f} " + \
   f"{np.mean(delta_bAP_V_dend_25):.3f}+-{np.std(delta_bAP_V_dend_25):.3f} " + \
   f"{np.mean(delta_bAP_V_dend_50):.3f}+-{np.std(delta_bAP_V_dend_50):.3f} " + \
   f"{np.mean(delta_bAP_V_dend_100):.3f}+-{np.std(delta_bAP_V_dend_100):.3f} ")

def find_dends(near, far):
    """find_dends(90, 110) will find the dendrite sections whose (0.5)
location(s) are greater than 90 ums and less than 110 microns from the
soma"""   
    for sec in dendritic:
        distance = h.distance(h.soma(0.5), sec(0.5))
        if distance > near and distance < far:
            print(sec, distance)

