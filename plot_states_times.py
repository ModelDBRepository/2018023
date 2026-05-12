"""plot_states_times.py
plots states and times from collected channels

The channels need to have their Inf and Tau functions exposed in the
mod files via the RANGE declaration.
"""

from solo_ap import *
from tonic_GABAAR_distal import * # this makes running this script standalone
from states_times import *
from pathlib import Path
from write_vec import write_vec
from base_dir_name import base_dir_name
from copy import deepcopy
from find_intersection import find_intersection

channel_dict={"mech":"Ca_LVAst",
 "gates": ["mInf", "hInf"],
 "taus": ["mTau", "hTau"],
 "powers": [2, 1]}
Ca_LVAst_tuple=states_times(channel_dict, send=True, graph=False)

plt.ion()

plt.figure()
plt.plot(Ca_LVAst_tuple[0], Ca_LVAst_tuple[1][0],linestyle=':', linewidth=1)
plt.plot(Ca_LVAst_tuple[0], Ca_LVAst_tuple[1][1],linestyle='-', linewidth=1)
m_lva=deepcopy( Ca_LVAst_tuple[1][0])
m2_lva=np.power(m_lva, 2)
m3_lva=np.power(m_lva, 3)
# intersection_lva = find_intersection(Ca_LVAst_tuple[0], Ca_LVAst_tuple[1][1],
#                                  m2_lva)
# print(f"intersection of LVA h, m^2: {intersection_lva}")
# plt.plot(*zip(*intersection_lva), 'go', alpha=0.7, ms=10)

plt.plot(Ca_LVAst_tuple[0], m2_lva, linestyle='-', linewidth=1)
plt.plot(Ca_LVAst_tuple[0], m3_lva, linestyle='-', linewidth=1)

# plt.title('LVA states, m^2 used by default')
plt.title('LVA states (1st power of m used in model)')
# plt.xlabel('v (mV), intersection '+ f"{intersection_lva[0][0]:.3f}," +
#            f"{intersection_lva[0][1]:.3f}")
plt.xlabel('v (mV)')
plt.ylabel('infinity curves (1), 2nd, 3rd powers of m')
plt.show()

LVAst_folder = "LVAst_kinetics_figs/"
kineticsdir= base_dir_name+LVAst_folder
Path(kineticsdir).mkdir( parents=True, exist_ok=True )
# plt.savefig(kineticsdir+'LVAst_states.svg')
plt.savefig(kineticsdir+'LVAst_states.pdf')
plt.savefig(kineticsdir+'LVAst_states.png')

plt.figure()
plt.plot(Ca_LVAst_tuple[0], Ca_LVAst_tuple[2][0],linestyle=':', linewidth=1)
plt.plot(Ca_LVAst_tuple[0], Ca_LVAst_tuple[2][1],linestyle='-', linewidth=1)
plt.title('LVA time constants')
plt.ylabel('time constant (ms)')
plt.xlabel('v (mV)')
plt.show()

plt.savefig(kineticsdir+'LVAst_taus.pdf')
plt.savefig(kineticsdir+'LVAst_taus.png')

LVAst_folder = "LVAst_kinetics_data/"
kineticsdir= base_dir_name+LVAst_folder
Path(kineticsdir).mkdir( parents=True, exist_ok=True )
# write_vec(kineticsdir+"LVAst_minf.txt",  Ca_LVAst_tuple[1][0])
# write_vec(kineticsdir+"LVAst_hinf.txt",  Ca_LVAst_tuple[1][1])
# v_vec, s_dict, t_dict = states_times({'mech':"Ca_LVAst", 'gates':['mInf','hInf'], 'powers':[2, 1], 'taus':['mTau', 'hTau_slow', 'hTau_fast']}, send=True)
s_dict=Ca_LVAst_tuple[1]
write_vec(kineticsdir+'mInf_Ca_LVAst.txt', s_dict[0])
write_vec(kineticsdir+'hInf_Ca_LVAst.txt', s_dict[1])
v_vec = Ca_LVAst_tuple[0]
write_vec(kineticsdir+'v_vec_for_Ca_LVAst.txt', v_vec)
t_dict = Ca_LVAst_tuple[2]
write_vec(kineticsdir+'mTau_Ca_LVAst.txt', t_dict[0])
write_vec(kineticsdir+'hTau_Ca_LVAst.txt', t_dict[1])

##
# HVA
##
channel_dict={"mech":"Ca_HVA",
 "gates": ["mInf", "hInf"],
 "taus": ["mTau", "hTau"],
 "powers": [2, 1]}
Ca_HVA_tuple=states_times(channel_dict, send=True, graph=False)


plt.figure()
plt.plot(Ca_HVA_tuple[0], Ca_HVA_tuple[1][0],linestyle=':', linewidth=1)
plt.plot(Ca_HVA_tuple[0], Ca_HVA_tuple[1][1],linestyle='-', linewidth=1)
m_hva=deepcopy( Ca_HVA_tuple[1][0])
m2_hva=np.power(m_hva, 2)
m3_hva=np.power(m_hva, 3)
# intersection_hva = find_intersection(Ca_HVA_tuple[0], Ca_HVA_tuple[1][1],
#                                  m3_hva)
# print(f"intersection of HVA h, m^3: {intersection_hva}")
# plt.plot(*zip(*intersection_hva), 'go', alpha=0.7, ms=10)

plt.plot(Ca_HVA_tuple[0], m2_hva, linestyle='-', linewidth=1)
plt.plot(Ca_HVA_tuple[0], m3_hva, linestyle='-', linewidth=1)
#plt.title('HVA states, (powers of m for illustration)')
plt.title('HVA states (1st power of m used in model)')
# plt.xlabel('v (mV), intersection '+ f"{intersection_hva[0][0]:.3f}," +
#           f"{intersection_hva[0][1]:.3f}")
plt.xlabel('v (mV)')
 
plt.ylabel('infinity curves (1), 2nd, 3rd, powers of m')
plt.show()

HVA_folder = "HVA_kinetics_figs/"
kineticsdir= base_dir_name+HVA_folder
Path(kineticsdir).mkdir( parents=True, exist_ok=True )
# plt.savefig(kineticsdir+'HVA_states.svg')
plt.savefig(kineticsdir+'HVA_states.pdf')
plt.savefig(kineticsdir+'HVA_states.png')

plt.figure()
plt.plot(Ca_HVA_tuple[0], Ca_HVA_tuple[2][0],linestyle=':', linewidth=1)
plt.plot(Ca_HVA_tuple[0], Ca_HVA_tuple[2][1],linestyle='-', linewidth=1)
# plt.plot(Ca_HVA_tuple[0], Ca_HVA_tuple[2][2],linestyle='-', linewidth=1)
plt.title('HVA time constants')
plt.ylabel('time constant (ms)')
plt.xlabel('v (mV)')
plt.show()

plt.savefig(kineticsdir+'HVA_taus.pdf')
plt.savefig(kineticsdir+'HVA_taus.png')

HVA_folder = "HVA_kinetics_data/"
kineticsdir= base_dir_name+HVA_folder
Path(kineticsdir).mkdir( parents=True, exist_ok=True )
# v_vec, s_dict, t_dict = states_times({'mech':"Ca_HVA", 'gates':['mInf','hInf'], 'powers':[2, 1], 'taus':['mTau', 'hTau_slow', 'hTau_fast']}, send=True)
s_dict = Ca_HVA_tuple[1]
write_vec(kineticsdir+'mInf_Ca_HVA.txt', s_dict[0])
write_vec(kineticsdir+'hInf_Ca_HVA.txt', s_dict[1])
v_vec = Ca_HVA_tuple[0]
write_vec(kineticsdir+'v_vec_for_Ca_HVA.txt', v_vec)
t_dict = Ca_HVA_tuple[2]
#write_vec('mInf_Ca_HVA.txt', s_dict[0])
write_vec(kineticsdir+'mTau_Ca_HVA.txt', t_dict[0])
write_vec(kineticsdir+'hTau_Ca_HVA.txt', t_dict[1])

# NaTs2_t

channel_dict={"mech":"NaTs2_t",
 "gates": ["mInf", "hInf"],
 "taus": ["mTau", "hTau"],
 "powers": [3, 1]}
NaTs2_t_tuple=states_times(channel_dict, send=True, graph=False)


plt.figure()
plt.plot(NaTs2_t_tuple[0], NaTs2_t_tuple[1][0],linestyle=':', linewidth=1)
plt.plot(NaTs2_t_tuple[0], NaTs2_t_tuple[1][1],linestyle='-', linewidth=1)
plt.title('NaTs2_t states')
plt.xlabel('v (mV)')
plt.ylabel('infinity curves (1)')
plt.show()

plt.figure()
plt.plot(NaTs2_t_tuple[0], NaTs2_t_tuple[2][0],linestyle=':', linewidth=1)
plt.plot(NaTs2_t_tuple[0], NaTs2_t_tuple[2][1],linestyle='-', linewidth=1)
plt.title('NaTs2_t time constants')
plt.ylabel('time constant (ms)')
plt.xlabel('v (mV)')
plt.show()

# NaTa_t

channel_dict={"mech":"NaTa_t",
 "gates": ["mInf", "hInf"],
 "taus": ["mTau", "hTau"],
 "powers": [3, 1]}
NaTa_t_tuple=states_times(channel_dict, send=True, graph=False)


plt.figure()
plt.plot(NaTa_t_tuple[0], NaTa_t_tuple[1][0],linestyle=':', linewidth=1)
plt.plot(NaTa_t_tuple[0], NaTa_t_tuple[1][1],linestyle='-', linewidth=1)
plt.title('NaTa_t states')
plt.xlabel('v (mV)')
plt.ylabel('infinity curves (1)')
plt.show()

plt.figure()
plt.plot(NaTa_t_tuple[0], NaTa_t_tuple[2][0],linestyle=':', linewidth=1)
plt.plot(NaTa_t_tuple[0], NaTa_t_tuple[2][1],linestyle='-', linewidth=1)
plt.title('NaTa_t time constants')
plt.ylabel('time constant (ms)')
plt.xlabel('v (mV)')
plt.show()

