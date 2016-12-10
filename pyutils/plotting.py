#
#
#

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 3D plots
def plot3(x, y, z, form='-', title = '', ax=None):
    if not ax:
        #ax = plt.gcf().add_subplot(111, projection='3d')
        ax = plt.gca(projection='3d')
    ax.plot(x, y, z, form)
    return ax

def set_axes_equal(ax=None):
    # Set equal-axes for 3D plots. Adapted from:
    #http://stackoverflow.com/questions/13685386/matplotlib-equal-unit-length-with-equal-aspect-ratio-z-axis-is-not-equal-to
    if ax is None:
        ax = plt.gca(projection='3d')
    xlim, ylim, zlim = ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()
    radius = 0.5 * max(np.diff((xlim, ylim, zlim)))
    bound = [-radius, radius]
    ax.set_xlim3d(bound + np.mean(xlim))
    ax.set_ylim3d(bound + np.mean(ylim))
    ax.set_zlim3d(bound + np.mean(zlim))

def line_plot_conversion(a, b):
    # Assumes points are matrix of row-vectors; FIXME: do I prefer column-vectors?
    M, N = a.shape
    nans = np.tile(np.nan*np.zeros(N), (M,1))
    block = np.hstack((a, b, nans))
    flat = block.flatten('C')
    return flat.reshape(M*3, N)

def annotate_angled(text, xy, angle=0, ax=None):
    if ax is None:
        ax = plt
    an = ax.annotate(text, xy=xy, horizontalalignment='left', verticalalignment='bottom')
    an.set_rotation(angle)
    return an

