"""ap_stats.py

threshold_t, baseline, peak, height, half_width, width=\
ap_stat(NEURON_v_vec, dt=0.1, Extended=False)

Call with extended=True to return data to plot 

threshold_t, threshold_v, baseline, peak, height, half_width, width, \
baseline_t, peak_t, half_width_t, width_t = ap_stat(NEURON_v_vec, \
dt=0.1, extended=True)

attempts to return lists of threshold_t (times), baselines
(mV), peaks (mV), etc.  If the NEURON_v_vec time step is different
than 0.1 ms, assign it with the optional dt argument.  The APs are
detected by dV/dt exceeding SD plus the mean of the dV/dt (the
derivative of the passed voltage trace), and then the baselines are
assigned the voltages from 0.5 ms before the threshold detection. The
peak is the max in a time window after the threshold crossing, and the
half width is the interpolated half width. The full width is
determined by the width at the threshold crossing.

Guan D et al 2007 J Neurophys defined the threshold as where a sharp
increase in dV/dt occurs. The above method of detecting the threshold
was inspired by this.

"""

import numpy as np

def ap_stat(NEURON_v_vec, dt = 0.1, extended = False):
    """ap_stat():

threshold_t, baseline, peak, height, half_width, width=\
ap_stat(NEURON_v_vec, dt=0.1, extended=False)

Call with extended=True to return data to plot 

threshold_t, threshold_v, baseline, peak, height, half_width, width, \
baseline_t, peak_t, half_width_t, width_t = ap_stat(NEURON_v_vec, \
dt=0.1, extended=True)

attempts to return lists of threshold_t (times), baselines
(mV), peaks (mV), etc.  If the NEURON_v_vec time step is different
than 0.1 ms, assign it with the optional dt argument.  The APs are
detected by dV/dt exceeding SD plus the mean of the dV/dt (the
derivative of the passed voltage trace), and then the baselines are
assigned the voltages from 0.5 ms before the threshold detection. The
peak is the max in a time window after the threshold crossing, and the
half width is the interpolated half width. The full width is
determined by the width at the threshold crossing.

Guan D et al 2007 J Neurophys defined the threshold as where a sharp
increase in dV/dt occurs. The above method of detecting the threshold
was inspired by this.
"""
    v = np.array(NEURON_v_vec)
    # mean_v = np.mean(v)
    # std_v = np.std(v)
    # threshold = mean_v + 5 * std_v
    # print(f"threshold is {threshold}")
    # vec_indicies = np.argwhere(v > threshold)
    # above didn't pan out so well so instead will use threshold
    # crossings of dVdt (the above worked for an invivo neuron firing
    # at a low frequency but not for a slice neuron firing at a high
    # frequency)
    dVdt = np.diff(v)
    mean_dVdt = np.mean(dVdt)
    std_dVdt = np.std(dVdt)
    dVdt_threshold = mean_dVdt + std_dVdt
    # helpful
    # https://danielmuellerkomorowska.com/2020/05/30/threshold-detection-in-numpy/
    # Only interested in the up crossings which will be stored in
    # threshold_t
    updown_crossings_logic =  np.diff(dVdt > dVdt_threshold, prepend=False)
    # times dt in the below converts indicies to times
    threshold_t_index = np.argwhere(updown_crossings_logic)[::2,0]
    threshold_t = threshold_t_index * dt
    # special section to test for if voltage at the end of the trace
    # returns to below the last threshold.  If it does not then try
    # removing the last threshold time from threshold_t so that that
    # last threshold crossing is not analyzed.
    last_threshold = v[int(threshold_t[-1]/dt)]
    if v[-1]>=last_threshold:
        print("""It has been detected that voltages at the end of the trace are not
below the last AP threshold so the detection of the last peak has been
removed since the voltage trace did not return to baseline it is not
possible to measure the width of the peak etc.""")
        np.array(list(threshold_t).pop()) # pop() removes the last
        # element in the list assume the peak occurs within
        # time_window milliseconds and find the number of indicies
        # corresponging to this
    time_window = 10
    window_indicies = int(time_window/dt)
    # assume that the baselines occur 0.5 ms before the threshold
    delta_t_to_baseline = -0.5
    delta_indicies_to_baseline = int(delta_t_to_baseline / dt)
    # find the baseline, peak, height, half_width, and width
    baseline = []
    peak = []
    height = []
    half_width = []
    width = []
    baseline_t = []
    peak_t = []
    half_width_t = []
    width_t = []
    for threshold_time in threshold_t:
        threshold_index = int(threshold_time/dt)
        baseline.append(v[threshold_index + delta_indicies_to_baseline])
        baseline_t.append(threshold_index + delta_indicies_to_baseline)
        local_AP = v[threshold_index : threshold_index + window_indicies]
        peak.append(max(local_AP))
        peak_t.append((threshold_index+local_AP.argmax(axis=0))*dt)
        height.append(peak[-1] - baseline[-1])
        ############################################################
        #
        # find the half_width by interpolating where the half peak x
        # coordinates start and end
        #
        # ##########################################################
        half_peak = baseline[-1] + 0.5 * height[-1] # now determine
        # the interpolated values (x_s, y_s), (x_e, y_e) where x,y
        # will be the start and end index fraction, voltage pairs and
        # s and e stand for start and end of the half width. y_s = y_e
        # = half peak.
        y_s = half_peak # need to find the x's that
        y_e = half_peak # are associated with the start and end:
        # Other pairs (x1, y1), (x2, y2) are the whole
        # number indicies x's and voltage's y that surround the (x_s,
        # y_s) and (x3, y3), (x4, y4) are the time series pairs that
        # surround's the half width end point (x_e, y_e).
        #
        # Note: (x, y)'s start in the local_AP and then the x's are
        # transformed to be indicies in v when saved in time lists.
        # 1) Find first (x2, y2) where y2 > half_peak This point
        # will be just after the half width starts. The x2s_logic
        # vector is of true false values of the same size as
        # local_AP. The diff makes all of them false except when the
        # value crosses the threshold going up or down.
        x2s_logic = np.diff(local_AP > half_peak, prepend=False)
        # The argwhere command below extracts the indicies of the
        # rising threshold crossings
        x2s = np.argwhere(x2s_logic)[::2, 0]
        x2 = x2s[0]
        y2 = local_AP[x2]
        x1 = x2 - 1
        y1 = local_AP[x1]
        x4s_logic = np.diff(local_AP[x2:] > half_peak, prepend=False)
        x4s_candidate = np.argwhere(x4s_logic)[:, 0] # check if trace
        # finishes before trace drops below half peak
        return_below_half_peak = True
        if len(x4s_candidate)<=1: # if true the trace does not return
            # below baseline
            return_below_half_peak = False
            x4s = len(x4s_logic)-1 # arbitrarily set index to end of trace
            print('A waveform that did not drop below baseline was detected')
            print('check that an AP is cutoff at the end of your trace')
            print('length arbitrarily set to length available')
        else:
            x4s = np.argwhere(x4s_logic)[:, 0][1] # find first below half_peak
        x4 = x4s + x2  # need to add x2 to transform x4 back to local_AP
        y4 = local_AP[x4]
        x3 = x4 - 1
        y3 = local_AP[x3]
        # in below s and e represent start and end of half width and these
        # formuli are used to find the interpolated values
        # use y = ( (y2-y1)/(x2-x1) ) * x + b_s where (x, y) will be (x_s, y_s)
        # use y = ( (y4-y3)/(x4-x3) ) * x + b_e where (x, y) will be (x_e, y_e)
        # find b_s, b_e
        b_s = y1 - ( (y2-y1)/(x2-x1) ) * x1
        b_e = y3 - ( (y4-y3)/(x4-x3) ) * x3
        # can interpolate to values of x_s, x_e
        x_s = (y_s - b_s) * (x2 - x1) / (y2 - y1)
        x_e = (y_e - b_e) * (x4 - x3) / (y4 - y3)
        half_width.append( (x_e - x_s) * dt )
        half_width_t.append( (threshold_index + x_s) * dt )
        #############################################################
        #
        # now find the width of the spike based on where the baseline
        # voltage is passed at the end of the AP.
        #
        #############################################################
        if return_below_half_peak:
            return_below_thresh_logic = np.diff(local_AP < local_AP[0], prepend=False)
            try:
                width_end = np.argwhere(return_below_thresh_logic)[::2, 0][0]
            except:
                print("Error in:")
                print("width_end = " \
                      + "np.argwhere(return_below_thresh_logic)[::2, 0][0]")
                print("np.shape(return_below_thresh_logic) = ", \
                      np.shape(return_below_thresh_logic))
                print("exiting ap_stat returning local_AP, baseline, " \
                      + " return_below_thresh_logic, and as many " \
                      + "None values as needed for variables")
                if extended:
                    return local_AP, baseline, return_below_thresh_logic, \
                        None, None, None, None, None, None, None, None
                else:
                    return local_AP, baseline, return_below_thresh_logic, \
                        None, None, None
        else:
            width_end = len(local_AP) - 1 # error message printed above
        width.append( width_end * dt ) # don't bother to
        # interpolate a crude measurement that starts at the threshold
        # crossing and finishes when the AP crosses to below the
        # baseline
        width_t.append( (threshold_index + width_end) * dt )
    if extended:
        threshold_v = [NEURON_v_vec[int(t/dt)] for t in threshold_t]
        return threshold_t, threshold_v, baseline, peak, height, \
    half_width, width, baseline_t, peak_t, half_width_t, width_t
    else:
        return threshold_t, baseline, peak, height, \
    half_width, width
