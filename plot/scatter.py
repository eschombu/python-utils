import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd

from .histogram import plot_hist


def scatter_2d(df, cols, labels=None, colors=None, xbins_log=False, ybins_log=False,
               xhist_log=False, yhist_log=False, xlim=None, ylim=None, nbins_x=50, nbins_y=50,
               square=False, jitter=False, axs=None, figsize=None, legend_suffix='',
               target_line=False, normalize_hists=True, **kwargs):
    """
    Compare two features across the dataset for multiple labels.
    
    Plot features values for each example against each other, coloring the points by their
    label. Histograms for each dimension are shown aligned on the edges of the plot. Includes
    optional arguments for log scales.
    """
    if not isinstance(df, pd.DataFrame):
        cols = ['x', 'y']
        df = pd.DataFrame({'x': df, 'y': cols})

    if isinstance(jitter, bool) and jitter:
        jitter = 100

    tmp = {}
    if labels is None:
        label_vals = ['']
        tmp[''] = df[cols].values
    elif len(labels) == len(df):
        label_vals = np.unique(labels)
        for label in label_vals:
            tmp[label] = df[np.asarray(labels) == label][cols].values
    else:
        label_vals = df[labels].unique()
        for label in label_vals:
            tmp[label] = df[df[labels] == label][cols].values

    default_colors = ['b', 'r', 'g', 'm', 'c', 'y']
    if colors is None and len(label_vals) > 1:
        if len(label_vals) > len(default_colors):
            default_colors = mpl.cm.jet(np.linspace(0, 1, len(label_vals)))
        colors = {v: c for v, c in zip(label_vals, default_colors)}

    tmp_cat = np.concatenate(list(tmp.values()))
    tmp_x = tmp_cat[:,0]
    tmp_y = tmp_cat[:,1]
    if xlim is None:
        if xbins_log:
            xmin = np.nanmin(tmp_x[tmp_x > 0])
            xmax = np.nanmax(tmp_x[tmp_x > 0])
        else:
            xmin = np.nanmin(tmp_x)
            xmax = np.nanmax(tmp_x)
    else:
        xmin, xmax = xlim

    if ylim is None:
        if ybins_log:
            ymin = np.nanmin(tmp_y[tmp_y > 0])
            ymax = np.nanmax(tmp_y[tmp_y > 0])
        else:
            ymin = np.nanmin(tmp_y)
            ymax = np.nanmax(tmp_y)
    else:
        ymin, ymax = ylim

    if xbins_log:
        xbins = np.linspace(np.log10(xmin), np.log10(xmax), nbins_x + 1)
    else:
        xbins = np.linspace(xmin, xmax, nbins_x + 1)
    if ybins_log:
        ybins = np.linspace(np.log10(ymin), np.log10(ymax), nbins_y + 1)
    else:
        ybins = np.linspace(ymin, ymax, nbins_y + 1)

    if axs is None:
        fig = plt.figure(figsize=figsize)
        grid = plt.GridSpec(5, 5, wspace=0.1, hspace=0.1)
        axs = [plt.subplot(grid[1:,:4]), plt.subplot(grid[0,:4]), plt.subplot(grid[1:,4])]
    for label in label_vals:
        if 'label' in kwargs:
            label_kwarg = {}
        elif label:
            label_kwarg = {'label': str(label) + legend_suffix}
        if colors is not None:
            if len(label_vals) > 1:
                color = colors[label]
            else:
                color = colors
        elif len(label_vals) > 1:
            color = colors[list(label_vals).index(label)]
        else:
            color = None
        if xbins_log and ybins_log:
            if jitter:
                r = 2 * (np.random.rand(len(tmp[label])) - 0.5)
                xjit = (np.log10(xmax) - np.log10(xmin)) / jitter * r
                r = 2 * (np.random.rand(len(tmp[label])) - 0.5)
                yjit = (np.log10(ymax) - np.log10(ymin)) / jitter * r
            else:
                xjit = 1
                yjit = 1
            axs[0].loglog(tmp[label][:,0] * xjit, tmp[label][:,1] * yjit,
                          'o', color=color, **label_kwarg, **kwargs)
        elif xbins_log:
            if jitter:
                r = 2 * (np.random.rand(len(tmp[label])) - 0.5)
                xjit = (np.log10(xmax) - np.log10(xmin)) / jitter * r
                r = 2 * (np.random.rand(len(tmp[label])) - 0.5)
                yjit = (ymax - ymin) / jitter * r
            else:
                xjit = 1
                yjit = 0
            axs[0].semilogx(tmp[label][:,0] * xjit, tmp[label][:,1] + yjit,
                            'o', color=color, **label_kwarg, **kwargs)
        elif ybins_log:
            if jitter:
                r = 2 * (np.random.rand(len(tmp[label])) - 0.5)
                xjit = (xmax - xmin) / jitter * r
                r = 2 * (np.random.rand(len(tmp[label])) - 0.5)
                yjit = (np.log10(ymax) - np.log10(ymin)) / jitter * r
            else:
                xjit = 0
                yjit = 1
            axs[0].semilogy(tmp[label][:,0] + xjit, tmp[label][:,1] * yjit,
                            'o', color=color, **label_kwarg, **kwargs)
        else:
            if jitter:
                r = 2 * (np.random.rand(len(tmp[label])) - 0.5)
                xjit = (xmax - xmin) / jitter * r
                r = 2 * (np.random.rand(len(tmp[label])) - 0.5)
                yjit = (ymax - ymin) / jitter * r
            else:
                xjit = 0
                yjit = 0
            axs[0].plot(tmp[label][:,0] + xjit, tmp[label][:,1] + yjit,
                        'o', color=color, **label_kwarg, **kwargs)
        if len(label_vals) > 1 or 'label' in kwargs:
            axs[0].legend(bbox_to_anchor=(1.02, 1.02), loc="lower left")
        if xbins_log:
            tmp_hist_bins = np.power(10, xbins)
        else:
            tmp_hist_bins = xbins

        plot_hist(tmp_hist_bins, np.histogram(tmp[label][:,0], tmp_hist_bins)[0], ax=axs[1],
                  log_bins=xbins_log, log_count=xhist_log, normalize=normalize_hists,
                  color=color, zero_line=False, **kwargs)

        if ybins_log:
            tmp_hist_bins = np.power(10, ybins)
        else:
            tmp_hist_bins = ybins
        plot_hist(tmp_hist_bins, np.histogram(tmp[label][:,1], tmp_hist_bins)[0], ax=axs[2],
                  flip=True, log_bins=ybins_log, log_count=yhist_log, normalize=normalize_hists,
                  color=color, zero_line=False, **kwargs)

    if not xhist_log:
        zero(axs[1])
    if not yhist_log:
        zero(axs[2], 'x')

    if xlim is None:
        xlim = axs[0].get_xlim()
    if ylim is None:
        ylim = axs[0].get_ylim()
    if square:
        lims = [min(xlim[0], ylim[0]), max(xlim[1], ylim[1])]
        axs[0].set_xlim(lims)
        axs[0].set_ylim(lims)
        axs[1].set_xlim(lims)
        axs[2].set_ylim(lims)
    else:
        axs[1].set_xlim(xlim)
        axs[2].set_ylim(ylim)

    if target_line:
        axs[0].plot(xlim, ylim, 'k:', alpha=0.3)

    axs[0].set_xlabel(cols[0])
    axs[0].set_ylabel(cols[1])
    axs[1].set_xticklabels([])
    axs[2].set_yticklabels([])

    return axs


def scatter_3d(df, cols, labels=None, figsize=None, log_axes=None):
    tmp = {}
    if labels is None:
        label_vals = ['good', 'bad']
        for label in label_vals:
            tmp[label] = df[df['label'] == label][cols].values
    else:
        label_vals = np.unique(labels)
        for label in label_vals:
            tmp[label] = df[np.asarray(labels) == label][cols].values
    
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    for label, marker in zip(label_vals, ('^', 'o')):
        ax.scatter(tmp[label][:,0], tmp[label][:,1], tmp[label][:,2], marker=marker, label=label)
    if log_axes is not None:
        pass # log scales not currently supported in 3D plots
                
    ax.set_xlabel(cols[0])
    ax.set_ylabel(cols[1])
    ax.set_zlabel(cols[2])
    ax.legend()
    return fig, ax