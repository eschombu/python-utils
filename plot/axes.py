import matplotlib.pyplot as plt


def zero(ax=None, dim='y'):
    if ax:
        if dim == 'y':
            ax.set_ylim([0, ax.get_ylim()[1]])
        if dim == 'x':
            ax.set_xlim([0, ax.get_xlim()[1]])
    else:
        if dim == 'y':
            plt.ylim([0, plt.gca().get_ylim()[1]])
        if dim == 'x':
            plt.set_xlim([0, plt.gca().get_xlim()[1]])
