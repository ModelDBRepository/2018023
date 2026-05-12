"""g_scale.py

g_scale(mech_str, scale, g='gbar') will scale the mech in mech_str where
ever it is present in the model by the "scale" as a multiplicative
factor of gbar_mech or a supplied conductance prefix g.

g_all(mech_str, set, g='gbar') will set the mech in mech_str where
ever it is present in the model by the "set" as gbar_mech or a
supplied conductance prefix g instead of gbar.

g_region(region, mech_str, set, g='gbar') will set the mech in mech_str in
the 'axon', 'soma', or 'dendrite' region of the model's gbar_mech or a
supplied conductance prefix g instead of gbar. The region is detected
on the first letter of the passed region string so 'a', 's', or 'd'
will work as well.

"""

from neuron import h
from run_simulation_python3 import *

def g_scale(mech_str, scale, g='gbar'):
    """g_scale(mech_str, scale, g='gbar') will scale the mech in mech_str where
ever it is present in the model by the "scale" as a multiplicative
factor of gbar_mech or a supplied conductance prefix g."""
    for sec in h.allsec():
        if h.ismembrane(mech_str, sec=sec):
            # there are two formats: for accessing sections that are spines
            # and another for accessing sections that are not spines:
            if 'spine' in str(sec):
                # below returns the 1000 in Spine[1000].spine
                spine_number_string=str(sec).split('[')[1].split(']')[0]
                cmd = \
                f"spines[{spine_number_string}]" \
                + f".{g}_{mech_str} *= {scale}"
                exec(cmd)
            else:
                for seg in sec: # assume that the gmax_mech is a range
                        # variable in case it is distance dependent
                    exec(f"h.{seg}.{g}_{mech_str} *= {scale}")

def g_all(mech_str, set_value, g='gbar'):
    """g_all(mech_str, set_value, g='gbar') will set the mech in mech_str where
ever it is present in the model by the "set_value" as gbar_mech or a
supplied conductance prefix g instead of gbar.
"""
    if mech_str=='pass' and g=='gbar':
        g='g' # if I forgot to set g for pass then correct that
    for sec in h.allsec():
        if h.ismembrane(mech_str, sec=sec):
            # there are two formats: for accessing sections that are spines
            # and another for accessing sections that are not spines:
            if 'spine' in str(sec):
                # below returns the 1000 in Spine[1000].spine
                spine_number_string=str(sec).split('[')[1].split(']')[0]
                cmd = \
                f"spines[{spine_number_string}]" \
                + f".{g}_{mech_str} = {set_value}"
                exec(cmd)
            else:
                for seg in sec: # assume that the gmax_mech is a range
                        # variable in case it is distance dependent
                    exec(f"h.{seg}.{g}_{mech_str} = {set_value}")
g_set=g_all # sometimes I type g_set when I mean g_all

def g_region(region, mech_str, set_value, g='gbar'):
    """g_region(region, mech_str, set_value, g='gbar') will set the mech in
mech_str in the model region 'a', 's', 'd' for axon soma or dendrite
to the "set_value" as gbar_mech or a supplied conductance prefix g
instead of gbar.

    """
    if mech_str=='pass' and g=='gbar':
        g='g' # if I forgot to set g for pass then correct that
    axon_regions = ['axon'] # matches for axon compartments
    soma_regions = ['soma', 'dend_0'] # matches for soma compartments
    dend_regions = ['dend_5', 'dend_7', 'spine', 'apic'] # matches for dend
                                                 # compartments
    matching_regions = 'unassigned'
    if region[0] == 'a':
        matching_regions = axon_regions
    if region[0] == 's':
        matching_regions = soma_regions
    if region[0] == 'd':
        matching_regions = dend_regions
    if matching_regions == 'unassigned':
        print("invalid region passed to gset(region, mech_str, set_value, g='gbar')")
        print("please use 'a' axon, 's' soma, or 'd' dendrite for region")
        return

    for sec in h.allsec():
        sec_in_region = False
        for region_sec in matching_regions:
            if region_sec in str(sec):
                sec_in_region = True
        if sec_in_region:
            if h.ismembrane(mech_str, sec=sec):
                # there are two formats: for accessing sections that are spines
                # and another for accessing sections that are not spines:
                if 'spine' in str(sec):
                    # below returns the 1000 in Spine[1000].spine
                    spine_number_string=str(sec).split('[')[1].split(']')[0]
                    cmd = \
                    f"spines[{spine_number_string}]" \
                    + f".{g}_{mech_str} = {set_value}"
                    exec(cmd)
                else:
                    for seg in sec: # assume that the gmax_mech is a range
                            # variable in case it is distance dependent
                        exec(f"h.{seg}.{g}_{mech_str} = {set_value}")

def g_linear_decay(region, mech_str, set_value_proximal, set_value_distal, g='gbar'):
    """g_linear_decay(region, mech_str, set_value_proximal,
set_value_distal, g='gbar') will set the mech in mech_str in the model
region 'a', 's', 'd' for axon soma or dendrite to interpolated value
starting at set_value_proximal and changing to set_value_distal at the
farthest reaches of the cell as gbar_mech or a supplied conductance
prefix g instead of gbar.

    """
    m=0 # find the farthest distance in the cell to run interpolation
        # from proximal to distal with
    for sec in h.allsec():
        if h.distance(sec(0.5), h.soma(0.5))>m:
            m=h.distance(sec(0.5), h.soma(0.5))
    if mech_str=='pass' and g=='gbar':
        g='g' # if I forgot to set g for pass then correct that
    axon_regions = ['axon'] # matches for axon compartments
    soma_regions = ['soma', 'dend_0'] # matches for soma compartments
    dend_regions = ['dend_5', 'dend_7', 'spine', 'apic'] # matches for dend
                                                 # compartments
    matching_regions = 'unassigned'
    if region[0] == 'a':
        matching_regions = axon_regions
    if region[0] == 's':
        matching_regions = soma_regions
    if region[0] == 'd':
        matching_regions = dend_regions
    if matching_regions == 'unassigned':
        print("invalid region passed to gset(region, mech_str, set_value, g='gbar')")
        print("please use 'a' axon, 's' soma, or 'd' dendrite for region")
        return

    for sec in h.allsec():
        sec_in_region = False
        for region_sec in matching_regions:
            if region_sec in str(sec):
                sec_in_region = True
        if sec_in_region:
            if h.ismembrane(mech_str, sec=sec):
                # there are two formats: for accessing sections that are spines
                # and another for accessing sections that are not spines:
                if 'spine' in str(sec):
                    # below returns the 1000 in Spine[1000].spine
                    spine_number_string=str(sec).split('[')[1].split(']')[0]
                    current_distance = h.distance(sec(0.5), h.soma(0.5))
                    scaled_value = set_value_distal*(current_distance/m) + \
                           set_value_proximal*((m-current_distance)/m)
                    cmd = \
                    f"spines[{spine_number_string}]" \
                    + f".{g}_{mech_str} = {scaled_value}"
                    exec(cmd)
                else:
                    for seg in sec: # assume that the gmax_mech is a range
                            # variable in case it is distance dependent
                        current_distance = h.distance(seg, h.soma(0.5))
                        scaled_value = set_value_distal*(current_distance/m) + \
                               set_value_proximal*((m-current_distance)/m)
                        exec(f"h.{seg}.{g}_{mech_str} = {scaled_value}")

def g_exp_decay(region, mech_str, set_value_proximal, space_constant, g='gbar'):
    """g_exp_decay(region, mech_str, set_value_proximal, space_constant,
g='gbar') will set the mech in mech_str in the model region 'a', 's',
'd' for axon soma or dendrite to set_value_proximal *
exp(-distance/space_constant) as gbar_mech or a supplied conductance
prefix g instead of gbar.

    """
    m=0 # find the farthest distance in the cell to run interpolation
        # from proximal to distal with
    for sec in h.allsec():
        if h.distance(sec(0.5), h.soma(0.5))>m:
            m=h.distance(sec(0.5), h.soma(0.5))
    if mech_str=='pass' and g=='gbar':
        g='g' # if I forgot to set g for pass then correct that
    axon_regions = ['axon'] # matches for axon compartments
    soma_regions = ['soma', 'dend_0'] # matches for soma compartments
    dend_regions = ['dend_5', 'dend_7', 'spine', 'apic'] # matches for dend
                                                 # compartments
    matching_regions = 'unassigned'
    if region[0] == 'a':
        matching_regions = axon_regions
    if region[0] == 's':
        matching_regions = soma_regions
    if region[0] == 'd':
        matching_regions = dend_regions
    if matching_regions == 'unassigned':
        print("invalid region passed to gset(region, mech_str, set_value, g='gbar')")
        print("please use 'a' axon, 's' soma, or 'd' dendrite for region")
        return

    for sec in h.allsec():
        sec_in_region = False
        for region_sec in matching_regions:
            if region_sec in str(sec):
                sec_in_region = True
        if sec_in_region:
            if h.ismembrane(mech_str, sec=sec):
                # there are two formats: for accessing sections that are spines
                # and another for accessing sections that are not spines:
                if 'spine' in str(sec):
                    # below returns the 1000 in Spine[1000].spine
                    spine_number_string=str(sec).split('[')[1].split(']')[0]
                    current_distance = h.distance(sec(0.5), h.soma(0.5))
                    scaled_value = set_value_proximal \
                                   * np.exp(-current_distance/space_constant)
                    cmd = \
                    f"spines[{spine_number_string}]" \
                    + f".{g}_{mech_str} = {scaled_value}"
                    exec(cmd)
                else:
                    for seg in sec: # assume that the gmax_mech is a range
                            # variable in case it is distance dependent
                        current_distance = h.distance(seg, h.soma(0.5))
                        scaled_value = set_value_proximal \
                                   * np.exp(-current_distance/space_constant)
                        exec(f"h.{seg}.{g}_{mech_str} = {scaled_value}")

def g_exp_reach(region, mech_str, proximal_value, distal_value, space_constant, g='gbar'):
    """g_exp_reach(region, mech_str, proximal_value, space_constant,
g='gbar') will set the mech in mech_str in the model region 'a', 's',
'd' for axon soma or dendrite to gbar_mech = proximal_value + C2 *
(1-exp(-distance/space_constant)) (or a supplied conductance prefix g
instead of gbar).
    """
    m=0 # find the farthest distance in the cell to run interpolation
        # from proximal to distal with
    for sec in h.allsec():
        if h.distance(sec(0.5), h.soma(0.5))>m:
            m=h.distance(sec(0.5), h.soma(0.5))
    if mech_str=='pass' and g=='gbar':
        g='g' # if I forgot to set g for pass then correct that
    axon_regions = ['axon'] # matches for axon compartments
    soma_regions = ['soma', 'dend_0'] # matches for soma compartments
    dend_regions = ['dend_5', 'dend_7', 'spine', 'apic'] # matches for dend
                                                 # compartments
    matching_regions = 'unassigned'
    if region[0] == 'a':
        matching_regions = axon_regions
    if region[0] == 's':
        matching_regions = soma_regions
    if region[0] == 'd':
        matching_regions = dend_regions
    if matching_regions == 'unassigned':
        print("invalid region passed to gset(region, mech_str, set_value, g='gbar')")
        print("please use 'a' axon, 's' soma, or 'd' dendrite for region")
        return
    #
    C2=(distal_value - proximal_value)/(1-np.exp(-m/space_constant))
    for sec in h.allsec():
        sec_in_region = False
        for region_sec in matching_regions:
            if region_sec in str(sec):
                sec_in_region = True
        if sec_in_region:
            if h.ismembrane(mech_str, sec=sec):
                # there are two formats: for accessing sections that are spines
                # and another for accessing sections that are not spines:
                if 'spine' in str(sec):
                    # below returns the 1000 in Spine[1000].spine
                    spine_number_string=str(sec).split('[')[1].split(']')[0]
                    current_distance = h.distance(sec(0.5), h.soma(0.5))
                    scaled_value = proximal_value + C2 * \
                        (1-np.exp(-current_distance/space_constant))
                    cmd = \
                    f"spines[{spine_number_string}]" \
                    + f".{g}_{mech_str} = {scaled_value}"
                    exec(cmd)
                else:
                    for seg in sec: # assume that the gmax_mech is a range
                            # variable in case it is distance dependent
                        current_distance = h.distance(seg, h.soma(0.5))
                        scaled_value = proximal_value + C2 * \
                             (1-np.exp(-current_distance/space_constant))
                        exec(f"h.{seg}.{g}_{mech_str} = {scaled_value}")

def g_piecewise_linear(region, mech_str, start_distance, start_value, \
                       end_distance, end_value, g='gbar'):
    """g_piecewise_linear(region, mech_str, start_distance, start_value,
end_distance, end_value, g='gbar') will set the gbar_mech (or a
supplied conductance prefix g instead of gbar) the model region 'a',
's', 'd' for axon soma or dendrite to interpolated value starting at
start_value at start_distance and changing to end_value at the
end_distance.
    """
    if mech_str=='pass' and g=='gbar':
        g='g' # if I forgot to set g for pass then correct that
    axon_regions = ['axon'] # matches for axon compartments
    soma_regions = ['soma', 'dend_0'] # matches for soma compartments
    dend_regions = ['dend_5', 'dend_7', 'spine', 'apic'] # matches for dend
                                                 # compartments
    matching_regions = 'unassigned'
    if region[0] == 'a':
        matching_regions = axon_regions
    if region[0] == 's':
        matching_regions = soma_regions
    if region[0] == 'd':
        matching_regions = dend_regions
    if matching_regions == 'unassigned':
        print("invalid region passed to gset(region, mech_str, set_value, g='gbar')")
        print("please use 'a' axon, 's' soma, or 'd' dendrite for region")
        return
    slope = (end_value - start_value) / (end_distance - start_distance)
    for sec in h.allsec():
        sec_in_region = False
        for region_sec in matching_regions:
            if region_sec in str(sec):
                sec_in_region = True
        if sec_in_region:
            if h.ismembrane(mech_str, sec=sec):
                # there are two formats: for accessing sections that are spines
                # and another for accessing sections that are not spines:
                if 'spine' in str(sec):
                    # below returns the 1000 in Spine[1000].spine
                    spine_number_string=str(sec).split('[')[1].split(']')[0]
                    current_distance = h.distance(sec(0.5), h.soma(0.5))
                    if start_distance < current_distance < end_distance :
                        scaled_value = start_value + \
                            slope * (current_distance - start_distance)
                        cmd = \
                        f"spines[{spine_number_string}]" \
                        + f".{g}_{mech_str} = {scaled_value}"
                        exec(cmd)
                else:
                    for seg in sec: # assume that the gmax_mech is a range
                            # variable in case it is distance dependent
                        current_distance = h.distance(seg, h.soma(0.5))
                        if start_distance < current_distance < end_distance :
                            scaled_value = start_value + \
                                slope * (current_distance - start_distance)
                            exec(f"h.{seg}.{g}_{mech_str} = {scaled_value}")
