# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


def compute_threshold(signal, alpha, window_width):

    df = pd.DataFrame({'signal': np.abs(signal)})
    q1 = df.rolling(window_width, center=True,
                    min_periods=1).quantile(.25).signal.to_numpy()
    q3 = df.rolling(window_width, center=True,
                    min_periods=1).quantile(.75).signal.to_numpy()
    th = alpha * ((q3 - q1) / 2)

    return th


def update_indices(source_idcs, update_idcs, update):
    """
    for every element s in source_idcs, change every element u in update_idcs
    accoridng to update, if u is larger than s
    """
    update_idcs_buffer = update_idcs
    for s in source_idcs:
        # for each list, find the indices (of indices) that need to be updated
        updates = [i for i, j in enumerate(update_idcs) if j > s]
#        print('updates: {}'.format(updates))
        for u in updates:
            update_idcs_buffer[u] += update
#        print('update_idcs: {}'.format(update_idcs_buffer))
    return update_idcs_buffer


def interp_stats(peaks, stats, nsamp):
    """
    interpolate descriptive statistics over the entire duration of the
    signal: samples up until first peak and from last peak to end of signal
    are set to the value of the first and last element of stats respectively;
    linear (2nd order) interpolation is chosen since cubic (4th order)
    interpolation can lead to biologically implausible interpolated values
    and erratic fluctuations due to overfitting
    """
    f = interp1d(np.ravel(peaks), stats, kind='slinear',
                 bounds_error=False, fill_value=([stats[0]], [stats[-1]]))
    # internally, for consistency in plotting etc., keep original sampling
    # rate
    samples = np.arange(0, nsamp)
    statsintp = f(samples)

    return statsintp
