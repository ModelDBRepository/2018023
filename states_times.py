"""
states_times(channel_dict)
graphs the steady states and time constants for hodgkin huxley models where
a channel_dict example shows the format for the argument to this function:
states_times({"mech":"na", "gates":["m","h"], "powers":[3, 1]},"taus":["tauh", "taum"]})
 
"""
from neuron import h, gui
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

def states_times(channel_dict, explore_vshift=False, vshift_range=[], send=False, graph=True, soma=None):
    """states_times(channel_dict)
graphs the steady states and time constants for hodgkin huxley models where
a channel_dict example shows the format for the argument to this function:
states_times({"mech":"na", "gates":["m","h"], "powers":[3, 1]},"taus":["tauh", "taum"]})
If explore_vshift_range is set True then a list of vshift can be provided in 
vshift_range and the mech's curves will be generated for those as well.
send=True will cause the function to return the kinetics vectors in a tuple
(v_vec, s_dict, t_dict) that includes the x axis and the y vectors for the
states and time constants. Note that the "powers" values are ignored here
however can be used later for if it is desired to graph those powers of the
kinetics.
"""
    # use soma to map out steady states and time constants
    if soma==None:
        soma = h.Section(name="soma")
        soma.insert(channel_dict['mech'])
    if channel_dict['mech']=='kv42p':
        print(f"soma.mTau_split_kv42p={soma.mTau_split_kv42p}")
    num_of_gates = len(channel_dict["gates"])
    num_of_taus =len(channel_dict["taus"])
    # create vectors for recording the steady state (infinity) curves
    steady_state_vec_dict = {}
    for gate_index in range(num_of_gates):
        steady_state_vec_dict[gate_index] = h.Vector()
     # create vectors for recording the time constants (tau) curves
    tau_vec_dict = {}
    for tau_index in range(num_of_taus):
         tau_vec_dict[tau_index] = h.Vector()
     # create commands to record the steady state and time constants

    gate_cmd = ""
    gate_print = ""
    cd = channel_dict
    # choose two different forms for steady_state_vec_dict and tau_vec_dict
    # a simple one that has keys of gate_index and tau_index if explore_vshift
    # is false and tuple keys (gate_index, vshift_index),
    # (tau_index, vshift_index) if explore_vshift is true and in that case the
    # vshift_index goes from 0 to len(vshift_range)-1 and the mechs are re-run
    # with those values
    if explore_vshift:
        for vshift_index in range(vshift_range):
            for gate_index in range(num_of_gates):
                gate_cmd += "steady_state_vec_dict[("+str(gate_index) \
                            + "," + str(vshift_index) \
                       + ")].append(soma(0.5)." \
                       + cd['gates'][gate_index]+'_'+cd["mech"]+")\n"
#                gate_print += "print(soma(0.5)." \
#                       + cd['gates'][gate_index]+'_'+cd["mech"]+")\n"

            tau_cmd = ""
            tau_print = ""
            for tau_index in range(num_of_taus):
                tau_cmd += "tau_vec_dict[("+str(tau_index) \
                            + "," + str(vshift_index) \
                       + ")].append(soma(0.5)." \
                       + cd['taus'][tau_index]+'_'+cd["mech"]+")\n"
#                tau_print += "print(soma(0.5)." \
#                       + cd['taus'][tau_index]+'_'+cd["mech"]+")\n"
########### keep developing here if desired in the meantime can explore by just changing
########### the assignment of vshift in the mod file by hand
    else:
        for gate_index in range(num_of_gates):
            gate_cmd += "steady_state_vec_dict["+str(gate_index) \
                   + "].append(soma(0.5)." \
                   + cd['gates'][gate_index]+'_'+cd["mech"]+")\n"
            gate_print += "print(soma(0.5)." \
                   + cd['gates'][gate_index]+'_'+cd["mech"]+")\n"

        tau_cmd = ""
        tau_print = ""
        for tau_index in range(num_of_taus):
            tau_cmd += "tau_vec_dict["+str(tau_index) \
                   + "].append(soma(0.5)." \
                   + cd['taus'][tau_index]+'_'+cd["mech"]+")\n"
            tau_print += "print(soma(0.5)." \
                   + cd['taus'][tau_index]+'_'+cd["mech"]+")\n"

    v_vec = h.Vector() # record the voltages as well
    if "celsius" in cd:
        h.celsius = float(cd["celsius"])
    if explore_vshift:
        pass
    else:
        for v_init in range(-100, 50):
            v_vec.append(v_init)
            h.finitialize(v_init)
            # print(str(soma(0.5).v))
            exec(gate_cmd)
            # print(gate_cmd)
            # print("gate_print")
            # exec(gate_print)
            exec(tau_cmd)
    s_dict = steady_state_vec_dict
    t_dict = tau_vec_dict

    if graph==True:
        fig = plt.figure(figsize=(12,8)) # horizontal, vertical inches
        gs1 = gridspec.GridSpec(1, 2)
        gs1.update(wspace=0.25, hspace=0.5)  # set the spacing between axes.

        ax1 = plt.subplot(gs1[0])
        # ax1.imshow([[0,1],[2,1]])
        for gate_index in range(num_of_gates):
            plt.plot(v_vec, s_dict[gate_index])
        plt.ylabel('states')
        plt.title(str(', '.join(cd['gates'])))


        ax2 = plt.subplot(gs1[1])
        # ax2.imshow([[2,1],[0,1]])
        for tau_index in range(num_of_taus):
            plt.plot(v_vec, t_dict[tau_index])
        plt.ylabel('tau (ms)')

        # ax1.axis('off')
        # ax2.axis('off')

        ax1.text(1.1,-0.1, "V (mV)", size=12, ha="center", 
                 transform=ax1.transAxes)
        # ax2.text(0.5,-0.1, "(b) my other label", size=12, ha="center", 
        #          transform=ax2.transAxes)
        plt.title(str(', '.join(cd['taus'])))
        plt.ylabel('tau (ms)')
        plt.ion()

        fig = plt.gcf()
        fig.suptitle(cd['mech'], fontsize=14)

        # plt.tight_layout()

        plt.show()
        plt.savefig(cd['mech']+'.png')
        plt.savefig(cd['mech']+'.pdf')

    if send==True:
        return (v_vec, s_dict, t_dict)

if __name__=="__main__":
    channel_dict = {"mech": "NaTa_t",
                "gates": ["mInf", "hInf"],
                "taus": ["mTau", "hTau"],
                "powers": [3, 1]}
    states_times(channel_dict)
