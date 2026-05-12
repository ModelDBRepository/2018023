from neuron import h
from setup_tGARs import *
def find_rheobase():
    """rheobase=find_rheobase() when called with a h.IClamp[0].amp that
initiates an AP will divide by two until there is no AP and then will
try next 1/2 between the last amp that caused the AP and the amp that
did not until that interval is less than 1e-4 nA and then finally
returns the amp that was the smallest found so far that will fire an
AP."""
    last_AP_amp=h.IClamp[0].amp
    interval_AP_amp=last_AP_amp
    # setup model to run a reasonable length of time
    h.IClamp[0].dur=1e6
    save_tstop=h.tstop
    h.tstop=1000
    bottom_AP_amp = 0 # an amplitude known or believed not to make an AP
    while interval_AP_amp > 1e-4:
        # try smaller current
        h.IClamp[0].amp = (last_AP_amp + bottom_AP_amp) / 2
        # run model
        my_run(h.tstop)
        # was there an AP?
        if AP_t_vec.size():
            last_AP_amp=h.IClamp[0].amp
        else:
            bottom_AP_amp=h.IClamp[0].amp
        interval_AP_amp = last_AP_amp - bottom_AP_amp
    return last_AP_amp

def find_AP_time(AP_time):
    """amp=find_AP_time() when called with a h.IClamp[0].amp that
initiates an AP before AP_time, will divide by two until there is no
AP before and then will try next 1/2 between the last amp that caused
the AP before AP_time and the amp that did not until that interval is
less than 1e-4 nA and then finally returns the amp that was the
smallest found so far that will fire an AP just before AP_time.

    """
    print(f"searching for {AP_time}'s current")
    last_AP_amp=h.IClamp[0].amp
    interval_AP_amp=last_AP_amp
    # setup model to run a reasonable length of time
    h.IClamp[0].dur=1e6
    save_tstop=h.tstop
    h.tstop=400
    bottom_AP_amp = 0.11609 # an amplitude knownto be rheobase for AP
    while interval_AP_amp > 1e-6:
        # try smaller current
        h.IClamp[0].amp = (last_AP_amp + bottom_AP_amp) / 2
        print(f"Checking {h.IClamp[0].amp}")
        # run model
        my_run(h.tstop)
        # was there an AP before AP time?
        print(f"There were {AP_t_vec.size()} elements in the AP time(s) file")
        if AP_t_vec.size():
            current_AP_time = AP_t_vec.x[0]
            print(f"The AP happened at {current_AP_time}")
            if current_AP_time <= AP_time:
                last_AP_amp=h.IClamp[0].amp
                print(f"The last_AP_amp was updated to {last_AP_amp}")
            else:
                # if AP occurred after the AP_time it is too small a current
                bottom_AP_amp=h.IClamp[0].amp
                print(f"A) the bottom_AP_amp was updated to {bottom_AP_amp}")
        else:
            bottom_AP_amp=h.IClamp[0].amp
            print(f"B) the bottom_AP_amp was updated to {bottom_AP_amp}")
        interval_AP_amp = last_AP_amp - bottom_AP_amp
        print(f"interval_AP_amp updated to {interval_AP_amp}")
    return last_AP_amp


# to run below script start with run_tGAR_control.py
# python -i run_tGAR_control.py
# then on interactive prompt import this script
# from find_rheobase import *
# (takes a few hours to run below)

# have an AP before the time
# being searched for a current for
h.IClamp[0].amp=1
h.tstop=400 # (384.2 was time of rheobase AP)
# find currents for control model to fire AP's at 10, 20, ..., 380 ms
# (prior knowledge is that the rheobase AP's fire at 384.2 ms

AP_times=[x for x in np.arange(210, 390, 10)]
AP_time_current_pairs=[] # make a list of lists of AP_times and the
                         # currents required to reach them
for AP_time in AP_times:
    AP_time_current_pairs.append((AP_time, find_AP_time(AP_time)))
    print(f"{(AP_time, find_AP_time(AP_time))}")
    h.IClamp[0].amp=AP_time_current_pairs[-1][-1] # last entry has an
                                                  # associated AP_time
                                                  # before the next
                                                  # one

with open('AP_time_current_pairs.pkl', 'wb') as f:
    pickle.dump(AP_time_current_pairs, f)
    
