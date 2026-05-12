"""configure_sim.py This script is typically run with a shell command
python3 configure_sim.py

This will write a base_dir_name.py discussed later and a
tonic_GABAAR_gbar.py which will contain these:

distribution="constant", "distal", or "ramp" (just one of these)

control() (a function related to unblocking (setting)
gbar_exGABALeak). control() will set the distribution of
gbar_exGABALeak to values that conform to an example of the type
assigned to the "distribution" variable.

label="some string" that is used to identify the type of distribution
and any other identified desired parameters and can be used in either
graph titles, text boxes, or part of folder names.

---

base_dir_name is used as the directory name prefix for folders that
contain figures (figs suffix) or data files (data suffix) that
represent the traces in the (base_dir_name)figs folder. This is
written into a base_dir_name.py file which is then imported into
scripts that write simulation results (figures or data files).

---

Note that blocking (setting to 0) the tonic GABAAR gbar's in the
sections can always be done with set_tonic(0).

Note: Currently the tonic GABAAR receptor mechanism is called
exGABALeak and the gbar is gbar_exGABALeak. If it is desired to use a
different mechanism it is only necessary to supply a different mod
file that has a exGABALeak mechanism and it's associated gbar declared
as a RANGE variable.

There are options to set the distribution to distal plateau's (0
proximal to the soma and then a constant value starting at some start
location start_loc from the soma), or linear ramps from the
g_piecewise_linear() in g_scale.py

To generate the model results and supplement figures verify or
reassign by hand the distribution variable to "constant", "distal", or
"ramp", in the line below and then rerun this program which will
rewrite tonic_GABAAR_gbar.py and base_dir_name.py.  Then follow the
instructions in the readme to generate the figures (after perhaps also
double checking that the value(s) of the gbar are set as desired.).
If it is desired to run a series of gbar_exGABALeak distributions then
the code below can be used as a template to create and run jobs in
batchs while also changing the base_dir_name so that the output files
are placed in separate folders for later examination.

"""
#############
#
# These first below lines are all that are expected to be edited by hand
# before this file is executed to create (write) the two simulation
# configuration files at the end of the below code. The variable,
# base_dir_name is assigned an f-string that automatically
# reports the distribution as it is desirable to identify that in the
# folder names as well as perhaps the date and setting of some
# (arbitrarily chosen) parameter(s).
#
#############

distribution = "constant" # choices are "ramp", "distal", or "constant"
mod_file = 'leak' # can be leak (exGABALeak), tonic (tonic.mod), or
# tonic_hybrid. It is assumed that you copy the appropriate
# deactivated (has file extension deactivate) mod file to
# exGABALeak.mod in the mod_files folder and then recompile the mod
# files (nrnivmodl mod_files, executed in the folder above mod_files)
# before running this script. You also need to set the gbar_factor
# appropriately (to 1 for leak, some higher number for tonic and
# tonic_hybrid (see below)). Note also that tonic and tonic_hybrid
# were only made to work with the constant distribution.

# Uncomment below if using exGABALeak.mod
gbar_factor = 1 # for leak current (no gbar_factor)

# Uncomment below if using tonic.mod from Schulz et al 2018
# The raw gbar_factor below made the -67.3 mV membrane have the same
# tGAR current for the tonic(.mod) mechanism as the constant exGABALeak.
# When observed this made delta Ca enhanced, divisors 2, 4, 8 tried.
# gbar_factor = 59.79812137990484/1 # for tonic.mod (see tGAR_mechanism_plot.py)

# Uncomment below if using hybrid of rectification from synaptic alpha5
# GABAA receptor in an otherwise leak current
# gbar_factor = 3.9278 # ~4 # amplifies the sigmoid left plateau of 0.25
                     # (rectification) back to original gbar value

# double quotes are included below so they appear when
# base_dir_name.py is written even farther below.

#base_dir_name= \
#f'"20241114_{distribution}_{mod_file}_scaled_{gbar_factor:.2f}_"'
base_dir_name='"results/"'

#############

if distribution == 'constant':
    file_str = f"""
distribution = "constant"
tonic_GABAAR_gbar = 0.8*2.7078395847022205e-05*{gbar_factor}
tGAR_label = "const_{mod_file}_0p27factor{gbar_factor:.2f}" # constant distribution about 0.27 pS/um2
def control():
    g_region('d', 'exGABALeak', tonic_GABAAR_gbar)
"""

if distribution == 'distal':
    file_str = f"""
distribution = "distal"
tonic_GABAAR_gbar = 2e-04*{gbar_factor}
tGAR_label = "distal_2" # constant distribution 2 pS/um2
start_loc=200 # for dend distribution of tonic GABAAR
end_loc=378.5 # most distal location is 378.46965982624585 um from soma(0.5)
def control():
    set_tonic(0)
    g_piecewise_linear('d', 'exGABALeak', start_loc, tonic_GABAAR_gbar,
 end_loc, tonic_GABAAR_gbar)
"""

if distribution == 'ramp':
    file_str = f"""
distribution = "ramp"
tonic_GABAAR_gbar = 10e-04*{gbar_factor}
tGAR_label = "ramp_10" # ramp distribution 0 to 10 pS/um2
start_loc=250 # for dend distribution of tonic GABAAR 
end_loc=378.5 # most distal location is 378.46965982624585 um from soma(0.5)
def control():
    set_tonic(0)
    g_piecewise_linear('d', 'exGABALeak', start_loc, 0,
 end_loc, tonic_GABAAR_gbar)
"""

#########
#
# write the distribution to tonic_GABAAR_gbar.py,
# and write base_dir_name assignment to base_dir_name.py
#
#########

preamble = """# this file writen by configure_sim.py
from g_scale import *
from setup_tGARs import * # supplies set_tonic() to reset exGABALeak
# which is helpful when distal or ramp only resets part of mod file default
"""

with open("tonic_GABAAR_gbar.py", 'w') as f:
    f.write(preamble)
    f.write(file_str)

with open("base_dir_name.py", 'w') as f:
    f.write(f"# warning: this file is rewritten by configure_sim.py\n") # warn
    f.write(f"base_dir_name={base_dir_name}\n") # sets data base folder name

# End of code in this script.
# The rest below is documentation on total tonic GABAAR conductance
# showing how can add up gbar density over the dendrite membrane.
'''
tonic_GABAAR_gbar = 2e-4 # a gbar value useful for setting in multiple scripts

for gbar_exGABALeak in [tonic_GABAAR_gbar]:
    if distribution=='distal':
        """# these variables recorded the dendritic area distal to a dendritic
# distance from the soma so that conductance could be normalized to a complete
# amount of conductance in the dendritic tree
>>> total_g
0.4104779607344406
>>> area_past_200=area_past(200)
>>> area_past_250=area_past(250)
>>> area_past_300=area_past(300)
>>> area_past_200, area_past_250, area_past_300
(2052.3898036722, 1359.7593291029032, 537.2377348129988)
>>> 
"""
        area_past_200, area_past_250, area_past_300 = \
        (2052.3898036722, 1359.7593291029032, 537.2377348129988)
        # 20240802 ignore the tonic_GABAAR_gbar.py for now (maybe that
        # file should include whether the distribution is constant or
        # distal and if distal what the start_loc is.
        total_g = 400 # experiment from original value that was 0.4 -
                    # see end of setup_tGARs.py
        if start_loc == 200: gbar_exGABALeak = total_g/area_past_200
        if start_loc == 250: gbar_exGABALeak = total_g/area_past_250
        if start_loc == 300: gbar_exGABALeak = total_g/area_past_300
        # can use the below for the above normalized total conductance
        g_piecewise_linear('d', 'exGABALeak', start_loc, gbar_exGABALeak, end_loc, gbar_exGABALeak)
        # or study ramps of conductance from a start loc to a fixed value at the distal tip
        # Comment out below and comment in above if want to study normalized conductance
        # distal_tip_gbar_exGABALeak = 10e-4 # typical values 2e-4 through 10e-4?
        # g_piecewise_linear('d', 'exGABALeak', start_loc, 0 , \
        #                   end_loc, distal_tip_gbar_exGABALeak)
        # try playing with Ra for a bit
        #for sec in h.allsec():
        #    sec.Ra *= 0.75 # try 25% smaller/larger axial resistance
    else:
         # explore constant distribution instead
        g_region('d', 'exGABALeak', new_gbar)
    """# These calculations found the equivalent constant conductance to a
# distal conductance. A distal conductance of 2 pS/um2 was in place at
# the time of the below interactive calculation which showed 0.27 pS/um2
# constant throughout the dendrites makes the same total conductance as
# a distal distribution of 2 pS/ums.

>>> g=0
>>> for sec in dendrites:
...   for seg in sec:
...     g += seg.gbar_exGABALeak*seg.area()
... 
>>> g
0.4104779607344406
>>> 
>>> area=0
>>> for sec in dendrites:
...   for seg in sec:
...     area += seg.area()
... 
>>> area
15158.872890898396
>>> g/area
2.7078395847022205e-05
>>> 
>>> new_gbar = g/area
>>> g_region('d', 'exGABALeak', new_gbar)
>>> h.dend_5[12].gbar_exGABALeak
2.7078395847022205e-05
>>> 
"""
'''
