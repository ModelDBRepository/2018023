"""soma_clamp.py graphs the spatial (dendritic) voltages when current
is injected at the soma to bring the membrane back to pre-GABA-block
levels.  This is to examine how this might change the dendrite voltage
levels."""

from tonic_GABAAR import *
from pathlib import Path

h.load_file('space_plot.ses')

g=h.save_window_ # the last graph is the space plot graph

def get_graph_lines(g):
    """get_graph_lines(h.Graph[0]) returns a list of tuples xvec, yvec
pairs from the passed graph object"""
    previndex=-1 # -1 gets the first one
    vec_list=[]
    # modified from help(h.Graph[0].getline)
    xline = []
    yline = []
    xvec = h.Vector() 
    yvec = h.Vector() 
    j = 0
    i = 1 
    i = g.getline(-i, xvec, yvec)
    while i != -1:
            # xvec and yvec contain the line with Graph internal index i. 
            # and can be associated with the sequential index j. 
            # print('{} {} {}'.format(j, i, yvec.label))
            vec_list.append((xvec.c(),yvec.c()))
            xline.append(xvec.c())
            yline.append(yvec.cl()) # clone label as well 
            i = g.getline(i, xvec, yvec)
    return vec_list

h.IClamp[0].amp = 0 # turn off pulse to find equilibrium voltages
h.tstop = 200 # 200 ms long enough to fairly settle down
########################
#
# run the model in two sessions, the first of which finds the spatial
# voltage profile and, for later use, the soma equilibrium voltage for
# each level of tonic GABAAR gbar. The second run clamps the soma to
# the previously found RMP for a particular tonic GABAAR gbar level
# and finds the equilibrium (resting) membrane potentials in the
# dendrites in the blocked case.
#
########################

control_spatial_profile={} # a dict of spatial profiles of the
                             # unclamped model neurons. The values are
                             # the gbar_exGABALeak's and the values
                             # are lists of (xvec, yvec) spatial
                             # profiles of equilibrium voltages.
control_soma_RMP={} # The values are the gbar_exGABALeak's and the
                      # values are the soma RMPs.
# First run

for gbar_exGABALeak in [0, 0.5e-4, 1e-4, 2e-4, 4e-4, 10e-4]: # study range of gbar's
    set_tonic(gbar_exGABALeak)
    my_run(h.tstop)
    graph_lines = get_graph_lines(g)
    control_spatial_profile[gbar_exGABALeak] = graph_lines
    control_soma_RMP[gbar_exGABALeak ] = h.soma(0.5).v # althougth
    # there are 36 soma compartments this is likely good enough to
    # consider only where the clamp will be applied.
    print(f"for gbar_exGABALeak = {gbar_exGABALeak} soma(0.5).v = {h.soma(0.5).v:.3f}")

# graph the control spatial profiles
plt.figure()

for gbar in control_spatial_profile:
    lines = control_spatial_profile[gbar]
    for line in lines:
        tmp=plt.plot(line[0], line[1], label=f"{gbar} gbar_exGABALeak")
#plt.legend(loc='best')    
plt.title('Blocked and tonic (0.5, 1, 2, 4, 10 pS/um2) control spatial profiles')
plt.ylabel('V (mV)')
figdir='20240530figdir/'
Path(figdir).mkdir( parents=True, exist_ok=True ) # make sure folder is
plt.tight_layout()
plt.savefig(figdir+'blocked_and_ctrl.png')
# Second run

# turn on a voltage clamp of the soma to the pre-GABA-block levels
SEC = h.SEClamp(h.soma(0.5)) # SEC (Single Elec. Clamp) to distinguish
                             # from sec (section)
SEC.dur1 = 1e9 # keep on forever

SEC.rs = 1e-3 # lowering the resistance from 1000 to 1 kOhm improves space clamp
# In these runs the gbar's are just used as dict keys as the tonic
# GABAAR's are blocked:
set_tonic(0)

clamped_spatial_profile = {}

for gbar_exGABALeak in [0.5e-4, 1e-4, 2e-4, 4e-4, 10e-4]:
    SEC.amp1 = control_soma_RMP[gbar_exGABALeak]
    my_run(h.tstop)
    graph_lines = get_graph_lines(g)
    clamped_spatial_profile[gbar_exGABALeak] = graph_lines

# graph the clamped spatial profiles

plt.figure()

for gbar in clamped_spatial_profile:
    lines = clamped_spatial_profile[gbar]
    for line in lines:
        tmp=plt.plot(line[0], line[1], label=f"{gbar} gbar_exGABALeak")
#plt.legend(loc='best')    
plt.title('Clamped-Blocked spatial profiles')
plt.ylabel('V (mV)')
plt.tight_layout()
plt.savefig(figdir+'clamped_blocked_profiles.png')

# combined clamped and control

plt.figure()

for gbar in clamped_spatial_profile:
    c_lines = clamped_spatial_profile[gbar]
    u_lines = control_spatial_profile[gbar] # the control... shares keys
    for c_line, u_line in zip(c_lines, u_lines):
        tmp=plt.plot(c_line[0], c_line[1], label=f"{gbar} gbar_exGABALeak")
        tmp=plt.plot(u_line[0], u_line[1], label=f"{gbar} gbar_exGABALeak")
        
# plt.legend(loc='best')    
plt.title('Clamped-Blocked and control spatial profiles')
plt.ylabel('V (mV)')
plt.xlabel('distance from soma (um), basal negative, apical positive')
plt.tight_layout()
plt.savefig(figdir+'all_profiles.png')

# single representations of combined clamped and control

plt.figure()

for gbar in clamped_spatial_profile:
    c_lines = clamped_spatial_profile[gbar]
    u_lines = control_spatial_profile[gbar] # the control... shares keys
    for c_line, u_line in zip(c_lines, u_lines):
        tmp=plt.plot(c_line[0], c_line[1], label=f"{gbar} gbar_exGABALeak")
        tmp=plt.plot(u_line[0], u_line[1], label=f"{gbar} gbar_exGABALeak")
        break
    
# plt.legend(loc='best')    
plt.title('Single representations of clamped and control spatial profiles')
plt.ylabel('V (mV)')
plt.xlabel('distance from soma (um), basal negative, apical positive')
plt.tight_layout()
plt.savefig(figdir+'single_rep_all_profiles.png')

# delta V as a function of distance from the soma in representative trace

plt.figure()

for gbar in clamped_spatial_profile:
    c_lines = clamped_spatial_profile[gbar]
    u_lines = control_spatial_profile[gbar] # the control... shares keys
    for c_line, u_line in zip(c_lines, u_lines):
        delta_V=c_line[1].c().sub(u_line[1])
        tmp=plt.plot(c_line[0], delta_V, label=f"{gbar*1e4} pS/um2 gbar_exGABALeak")
        break
    
plt.legend(loc='best')    
plt.title('Single representations of clamped-blocked and control spatial profiles')
plt.ylabel('delta V between clamped-blocked and control membranes (mV)')
plt.xlabel('distance from soma (um), basal negative, apical positive')
plt.tight_layout()
plt.savefig(figdir+'delta_v_profiles.png')


