from setup_tGARs import *
from tonic_GABAAR_distal import *
from plot_states_times import *

plt.figure()
plt.plot(Ca_LVAst_tuple[0], Ca_LVAst_tuple[1][0],linestyle=':', linewidth=1,
         label='LVA mInf')
plt.plot(Ca_LVAst_tuple[0], Ca_LVAst_tuple[1][1],linestyle='-', linewidth=1,
         label='LVA hInf')
plt.plot(Ca_HVA_tuple[0], Ca_HVA_tuple[1][0],linestyle='-.', linewidth=1,
         label='HVA mInf')
plt.plot(Ca_HVA_tuple[0], Ca_HVA_tuple[1][1],linestyle='-', linewidth=1,
         label='HVA hInf')

plt.title('LVA  and HVA states')
plt.xlabel('v (mV)')
plt.ylabel('infinity curves (1)')
plt.legend(loc='best')

if 0: # compare to human HVA expressed in HEK cells
    plt.figure()
    plt.plot(Ca_LVAst_tuple[0], np.power(Ca_LVAst_tuple[1][0], 2),
             linestyle=':', linewidth=1, label='LVA mInf squared')
    plt.plot(Ca_LVAst_tuple[0], Ca_LVAst_tuple[1][1],linestyle='-', linewidth=1,
             label='LVA hInf')
    plt.plot(Ca_HVA_tuple[0], np.power(Ca_HVA_tuple[1][0], 3),
             linestyle='-.', linewidth=1, label='HVA mInf cubed')
    plt.plot(Ca_HVA_tuple[0], Ca_HVA_tuple[1][1],linestyle='-', linewidth=1,
             label='HVA hInf')
    # add Gao et al 2023 experimental data on WT R in model cells
    act=np.loadtxt('gao_act.txt')
    inact=np.loadtxt('gao_inact.txt')
    plt.plot(act[:,0], act[:,1], label='Gao et al 2023 G/Gmax activation')
    plt.plot(inact[:,0], inact[:,1], label='Gao et al 2023 G/Gmax inactivation')
    plt.title('LVA m_inf^2, HVA m_inf^3 states, and Gao et al Fig 2b WT')
    plt.xlabel('v (mV)')
    plt.ylabel('(powers of) infinity curves (1)')
    plt.legend(loc='best')
