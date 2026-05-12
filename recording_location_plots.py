"""recording_location_plots.py
Will plot the locations that voltage and other quantities were recorded during
simulations."""

# We will load the morphology and "record_distances" and "dendrite_names"
# by using the script that runs the model in the tGAR blocked state It
# would be faster to run if we didn't run the model however it is a
# short run and it would be longer to figure out how to (write the
# code to) load the model with just those relevant variables.

# first remove the pickle files so that the model will run
from neuron import h, gui
h.system("rm -f data/*.pkl")

from setup_tGARs import * # import many functions and setup recordings
from run_tGAR_blocked import *
# now we have "record_distances" (np.array of the distances from the
# soma that recordings were made) and "dendrite_names" (dict with keys
# of recording distances and values of strings of the segment names
# that are at each recording distance)

# to make a graph of all the recording locations drop an arbitrary point
# process (Exp2Syn was used) because NEURON has native methods to graph
# point process's as a dot on shape graphs which we reuse to indicate
# the recording positions (these extra point processes are never actually
# used in simulations).

extra_syn_list_dict={} # a dictionary of keys of distances records
                       # were made and values of lists of the synapses
                       # added for visualization of the recording
                       # locations.

for distance in dendrite_names:
    tmp_syn_list = [] # a temporary list of synapses
    for seg_str in dendrite_names[distance]: # loop over dend segs at a dist
        seg = eval(f"h.{seg_str}")
        tmp_syn_list.append(h.Exp2Syn(seg))
    extra_syn_list_dict[distance] = tmp_syn_list

shapeSyn = h.Shape()
shapeSyn.label("Recording locations")

# put dots on all the recording locations:
for color_index, dist in enumerate(extra_syn_list_dict):
    color = 2 + color_index%4 # alternate red blue green tan
    style = 4 + color_index%3 # alternate between disk square triangle
    size = 10
    for syn, seg_str in zip(extra_syn_list_dict[dist], dendrite_names[dist]):
        shapeSyn.point_mark(syn, color, style, size)
        # print(f"{seg_str} {color} {style}")
print("""Use the Print & File window manager to print the shape plot as a
postscript (ps) file (for vector graphics version). Ghostscript has
ps2pdf that can convert the ps to a pdf.""")
