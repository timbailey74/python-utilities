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



    [D1,N1] = size(x1);
[D2,N2] = size(x2);

if D1 ~= D2, error('Vectors must have the same dimension'), end

d2 = (ones(N1,1)*sum(x2.^2, 1))' + ...
      ones(N2,1)*sum(x1.^2, 1) - ...
      2.*(x2'*x1);

d2(d2<0) = 0; % ensure rounding errors do not give negative values
