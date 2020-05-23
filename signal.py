import numpy as np


def zscore(x):
    m = np.mean(x)
    s = np.std(x)
    return (x - m) / s


def smooth(x, n_smooth=1001, n_downsample=None):
    nhalf = int(n_smooth / 2)
    pad = np.nan * np.ones(nhalf)
    y = np.concatenate([pad, x, pad])
    y = np.vstack([y[i:(len(y) - (n_smooth - 1 - i))] for i in range(n_smooth)])
    y = np.nanmean(y, axis=0)
    if n_downsample is not None and downsample > 1:
        y = y[int(n_downsample/2)::n_downsample]
    return y


