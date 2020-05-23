import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm


def colors_by_value(x, lims=None, cmap='jet', n=256, alpha=True):
    if lims is None:
        lims = min(x), max(x)
    elif isinstance(lims, str) and lims == 'none':
        lims = [0, n - 1]
    elif len(lims) == 1:
        lims = [0, lims]
    x_norm = (x - lims[0]) / (lims[1] - lims[0])
    colors = mpl.cm.get_cmap(cmap, n)(x_norm)
    if isinstance(alpha, bool):
        if alpha:
            return colors
        else:
            return colors[:,:3]
    else:
        return np.concatenate([colors[:,:3], alpha * np.ones((len(colors), 1))], axis=1)


# Color parts of a line based on its properties, e.g., slope.
# From http://wiki.scipy.org/Cookbook/Matplotlib/MulticoloredLine
def multi_color_line(x, y, c, cmap=ListedColormap(['r', 'b']), boundaries=[0, 0.5, 1]):
    norm = BoundaryNorm(boundaries, cmap.N)

    # Create a set of line segments so that we can color them individually
    # This creates the points as a N x 1 x 2 array so that we can stack points
    # together easily to get the segments. The segments array for line collection
    # needs to be numlines x points per line x 2 (x and y)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create the line collection object, setting the colormapping parameters.
    # Have to set the actual values used for colormapping separately.
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(c)
    lc.set_linewidth(2)
    plt.gca().add_collection(lc)
    plt.show()

