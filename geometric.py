#
# Geometric and trig utilities. Ported from matlab_utilities and elsewhere. Tim Bailey 2015.
#

import numpy as np

def pi2pi(angle):
    """
    Normalised angle calculation; bound angle(s) between +/- pi.
    :param angle: Scalar angle or array of angles
    :return: normalised angles
    """
    return (angle + np.pi) % (2*np.pi) - np.pi

def dist_sqr(x1, x2):
    """
    Compute the square distances of each vector in x1 to each vector in x2. To
    compute the set of Euclidean distances, simply compute sqrt(d2). This
    equation is adapted from Netlab, dist2.m, by Ian T Nabney.
    :param x1: matrix of N column vectors
    :param x2: matrix of M column vectors
    :return: d2 - M x N matrix of square distances
    """
    if x1.shape[0] != x2.shape[0]:
        raise ValueError('Vectors must have the same dimension.')

    N1 = x1.shape[1] if len(x1.shape) > 1 else 1
    N2 = x2.shape[1] if len(x2.shape) > 1 else 1
    d2 =  np.tile(np.sum(x2*x2,0), (N1,1)).T \
        + np.tile(np.sum(x1*x1,0), (N2,1))   \
        - 2 * np.dot(x2.T, x1)
    d2[d2<0] = 0 # Ensure rounding errors do not give negative values
    return d2
