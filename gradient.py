"""gradient.py explores the effect of adding a gradient of tonic
gabaar in the Iascone model."""

from tonic_GABAAR import *
from pathlib import Path

from g_scale import *

# sample gbar_exGABALeak values to study in a gradient in the model
# doubling the gbar_exGABALeak values to make similar total amounts to
# flat distribution.
print("soma, 25 ums 50 ums, 100 ums")
[1e-4, 2e-4, 4e-4, 8e-4, 20e-4]
for gbar_exGABALeak in [20e-4]:
    set_tonic(0)
    print(f"linear gbar_exGABALeak proximal 0 to distal {1e4*gbar_exGABALeak}")
    g_piecewise_linear('d', 'exGABALeak', 0, 0, 379, gbar_exGABALeak)
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

