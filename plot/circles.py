import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def create_circles(xy_tuples, radii=None, colors_or_cmapNormInd=None):
    if radii is None:
        radii = np.zeros(len(xy_tuples))
    elif len(radii) == 1:
        radii = np.ones(len(xy_tuples)) * radii
    else:
        radii = np.array(radii)
    
    # Convert color argument to list of matplotlib color specs
    if (colors_or_cmapNormInd is None) or (len(colors_or_cmapNormInd) == 0):
        colors = ['b' for i in xy_tuples]
    elif len(colors_or_cmapNormInd) == 1:
        colors = [colors for i in xy_tuples]
    else:
        colors = np.array(colors_or_cmapNormInd)
        colors = mpl.cm.jet(np.int64(255*colors))

    circles = []
    for i in range(len(xy_tuples)):
        circles.append( plt.Circle(xy_tuples[i], radii[i], color=colors[i]) )
    
    return circles
    # Loop over circles with fig.gca().add_artist(circle_i) to draw circles on axes, e.g.:
    #  fig = plt.figure()
    #  plt.axis(circle_xylims(circles))
    #  for i in range(len(circles)):
    #      # ***USE COPIES OF CIRCLES: For some reason this method changes some attributes
    #      # of the circles when they are drawn ***
    #      ax.add_artist(copy.copy(circles[i]))

def circle_xylims(circles):
    xlims = [np.array([circle.center[0] - circle.radius for circle in circles]).min(), \
        np.array([circle.center[0] + circle.radius for circle in circles]).max()]
    ylims = [np.array([circle.center[1] - circle.radius for circle in circles]).min(), \
        np.array([circle.center[1] + circle.radius for circle in circles]).max()]
    return np.concatenate([xlims, ylims])

def draw_circles(circles, figORax):
    if 'matplotlib.figure.Figure' in str(type(figORax)):
        ax = figORax.gca()
    elif 'matplotlib.figure.Figure' in str(type(figORax)):
        ax = figORax
    else:
        fig = plt.figure()
        ax = fig.gca()
    
    for i in range(len(circles)):
        ax.add_artist(copy.copy(circles[i]))
    
    return ax
    