"""notes for creating a depolarization stimulus that will bring the
cell up to various depolarized voltages before the bAP is initiated by
a different (historically previous) IClamp. """

"""
# prediction from interactive use of current needed to depolarize 10 mv:
# with no depolarizing current injection
>>> soma_voltageVector[2000]
-72.46931484639535
# method: turn on a voltage clamp with the voltage desired specified
# run the model for 200 ms
# readout the voltage clamp (command current) and store it in a vector
# of command currents to depolarize the cell to baseline values 
# [-70, -65, -60, -55]
"""
from setup_tGARs import *
from tonic_GABAAR_distal import *

print("Loaded model, entering voltage clamp command current discovery phase")
print("Control condition: GABAAR's present at gbar={tonic_GABAAR_gbar}")
# assume that the current version of tonic_GABAAR_distal includes
# a depol_iclamp (IClamp[X]) and turn it off so that can find amplitude
# values without its influence

depol_iclamp.amp = 0

# create a dictionary that has "control" or "blocked" as its keyes
# and a list of pairs of depolarizing currents and their corresponding
# target soma voltages as its values.
depol_iv_pairs_dict = {}

# baseline_values = [x for x in range(-70, -54, 1)] # [-70, -65, -60, -55]
# control target voltage depol iclamp currents have non spiking blocked
# tGAR models only at -60 mV and below
baseline_values = [x for x in range(-70, -59, 2)]
vc = h.VClamp(h.soma(0.5))

vc.dur[0] = 1e6
control_depol_iv_pairs = []
baseline_time = 2000 # bAP initiated at t=200 ms (dt=0.1)

# In the control case (with tonic GABAAR's functioning)
# find the command currents that were necessary to depolarize the soma
# to the voltage clamped baseline currents:
for baseline_value in baseline_values:
    vc.amp[0] = baseline_value
    h.my_run(200) # run to right before bAP to find VClamp i for baseline_value
    print(f"depolarized to {soma_voltageVector[baseline_time]} with current " +\
          f"{vc.i}")
    control_depol_iv_pairs.append((vc.i, baseline_value))

depol_iv_pairs_dict['control']=control_depol_iv_pairs

print("Blocked condition: GABAAR's absent")

# In the blocked case (with tonic GABAAR's conductances set to 0)
set_tonic(0)
blocked_depol_iv_pairs = []
# find the command currents that were necessary to depolarize the soma
# to the voltage clamped baseline currents:
for baseline_value in baseline_values:
    vc.amp[0] = baseline_value
    h.my_run(200) # run to right before bAP to find VClamp i for baseline_value
    print(f"depolarized to {soma_voltageVector[baseline_time]} with current " +\
          f"{vc.i}")
    blocked_depol_iv_pairs.append((vc.i, baseline_value))

depol_iv_pairs_dict['blocked']=blocked_depol_iv_pairs

print("Saving v clamp command currents for i clamp")
# save the currents that were found: now just save one file in archive dir
"""with open('data/control_depol_iv_pairs.pkl', 'wb') as f:
    pickle.dump(control_depol_iv_pairs, f)
with open('data/blocked_depol_iv_pairs.pkl', 'wb') as f:
    pickle.dump(blocked_depol_iv_pairs, f)
"""
with open('archive/depol_iv_pairs_dict.pkl', 'wb') as f:
    pickle.dump(depol_iv_pairs_dict, f)

# turn off the voltage clamp and verify that current clamp application
# of those currents will reproduce the desired baseline voltages

print("Verifying in i clamp")

vc.dur[0]=0 # turn off voltage clamp so doesn't interfere with current clamp

# create the current clamp (IClamp)
depol_stim = h.IClamp(h.soma(0.5)) # same loc as bAP stim

depol_stim.dur = 1e6 # make the current last essentially for the
                     # length of any practical simulation
currentclamp_iv_pairs=[]
currentclamp_iv_pairs_dict={}

print("Blocked case") # block case left over from above
test_time = 200
h.IClamp[0].amp=0 # turn off bAP pulse in case want to extend test_time past it
for iv_pair in blocked_depol_iv_pairs:
    depol_stim.amp = iv_pair[0] # the command current found previously
    h.v_init = iv_pair[1]
    tmp=h.my_run(test_time) # run to right before bAP to find VClamp i for
                      # baseline_value
    # print(f"depolarized to {soma_voltageVector[baseline_time]:.5f} " +\
    print(f"depolarized to {soma_voltageVector[int(test_time/h.dt)]:.5f} " +\
          "with current "+\
          f"{depol_stim.amp:.5f}, target was {iv_pair[1]}")
    currentclamp_iv_pairs.append((depol_stim.amp,
                                  soma_voltageVector[baseline_time]))
currentclamp_iv_pairs_dict['blocked']=currentclamp_iv_pairs

print("Control case")
set_tonic(tonic_GABAAR_gbar)
currentclamp_iv_pairs=[]

for iv_pair in control_depol_iv_pairs:
    depol_stim.amp = iv_pair[0] # the command current found previously
    h.v_init = iv_pair[1]
    tmp=h.my_run(test_time) # run to right before bAP to find VClamp i for
                      # baseline_value
    print(f"depolarized to {soma_voltageVector[int(test_time/h.dt)]:.5f} " +\
          "with current "+\
          f"{depol_stim.amp:.5f}, target was {iv_pair[1]}")
    currentclamp_iv_pairs.append((depol_stim.amp,
                                  soma_voltageVector[baseline_time]))

currentclamp_iv_pairs_dict['control']=currentclamp_iv_pairs


