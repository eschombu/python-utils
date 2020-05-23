import matplotlib.pyplot as plt
import numpy as np


def plot_hist(bin_edges, counts, ax=None, normalize=False, fill=False, zero_line=True,
              log_bins=False, log_count=False, flip=False, **kwargs):
    if ax is None:
        ax = plt.gca()
    
    if log_count == 'auto':
        nonzero_counts = counts[counts > 0]
        if len(nonzero_counts) > 0:
            counts_log_range = np.log10(np.max(nonzero_counts) / np.min(nonzero_counts))
            counts_95percentile_range = (
                np.log10(np.max(nonzero_counts) / np.percentile(nonzero_counts, 95))
            )
            if counts_log_range > 2 or counts_95percentile_range > 1:
                log_count = True
            else:
                log_count = False
        else:
            log_count = False

    x = np.vstack([bin_edges[:-1], bin_edges[1:]]).T.flatten()
    if normalize:
        counts = counts / np.nansum(counts)
    y = np.vstack([counts, counts]).T.flatten()
    if log_bins:
        if flip:
            if log_count:
                ax.loglog(y, x, **kwargs)
            else:
                if fill:
                    ax.fill_betweenx(y, x, **kwargs)
                    ax.set_yscale('log')
                else:
                    ax.semilogy(y, x, **kwargs)
                    if zero_line:
                        ax.axvline(0, color='k', linestyle=':')
        else:
            if log_count:
                ax.loglog(x, y, **kwargs)
            else:
                if fill:
                    ax.fill_between(x, y, **kwargs)
                    ax.set_xscale('log')
                else:
                    ax.semilogx(x, y, **kwargs)
                    if zero_line:
                        ax.axhline(0, color='k', linestyle=':')
    else:
        if flip:
            if log_count:
                ax.semilogx(y, x, **kwargs)
            else:
                if fill:
                    ax.fill_betweenx(y, x, **kwargs)
                else:
                    ax.plot(y, x, **kwargs)
                    if zero_line:
                        ax.axvline(0, color='k', linestyle=':')
        else:
            if log_count:
                ax.semilogy(x, y, **kwargs)
            else:
                if fill:
                    ax.fill_between(x, y, **kwargs)
                else:
                    ax.plot(x, y, **kwargs)
                    if zero_line:
                        ax.axhline(0, color='k', linestyle=':')
