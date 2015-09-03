#
# Basic Gaussian manipulation and inference utilities. Ported from
# matlab_utilities. Tim Bailey 2015.
#

import numpy as np

def reprow(x, N):
    # Alternatives: return np.tile(x, (N,1))
    # Alternatives: return np.outer(np.ones(N), x)
    return np.tile(x, (N,1))

def repcol_(x, N):
    if len(x.shape) == 1:
        return np.tile(x, (N,1)).T # for [] arrays
    elif x.shape[1] == 1:
        return np.tile(x, (1,N)) # for [[]] column arrays
    else:
        raise ValueError('Must be an array or single-column matrix')

def repcol(x, N):
    return np.outer(x, np.ones(N))

class Scale:
    def __init__(self, mean, sigma):
        self.mean = np.array(mean)
        self.sigma = np.array(sigma)
    def scale(self, x):
        return (x - self.mean) / self.sigma
    def unscale(self, sx):
        return self.mean + sx*self.sigma
