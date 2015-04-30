#
# Basic Gaussian manipulation and inference utilities. Ported from
# matlab_utilities. Tim Bailey 2015.
#

import numpy as np
import scipy.linalg as sci

# Evaluate a Gaussian with covariance S at distance v from the mean
def gauss_evaluate(v, S, logflag=False):
    """
    gauss_evaluate() - evaluate multivariate Gaussian function with covariance S at offsets v
    :param v:
    :param S:
    :param logflag: (optional)
    :return w:
    """
    D = v.size
    L = sci.cholesky(S, lower=True)
    f = sci.solve_triangular(L, v, lower=True)
    E = -0.5 * np.sum(f*f, axis=0)
    if logflag:
        C = 0.5*D*np.log(2*np.pi) + np.sum(np.log(L.diagonal()))
        w = E - C
    else:
        C = (2*np.pi)**(D/2.) * np.prod(L.diagonal())
        w = np.exp(E) / C
    return w

def gauss_power(P, r):
    """
    Compute the covariance and weight of P**r
    :param P:
    :param r:
    :return w:
    """
    d = P.shape[0]
    # FIXME: Need an equivalent to eig in python

def chi_square_density(x, n):
    """
    Compute n-dof Chi-square density function at points x
    Reference: Papoulis, "Probability, Random Variables and Stochastic Processes", 4th Ed., 2002, p89.
    :param x: x-axis coordinates
    :param n: degrees of freedom
    :return: f(x) - Chi-square probability density function
    """
    k = n/2
    C = 2**k * gamma(k) # FIXME: Need python gamma function
    return x**(k-1) * exp(-x/2) / C

def chi_square_mass(x,n):
    """
    Compute n-dof Chi-square mass function at points x
    Reference: Press, "Numerical Recipes in C", 2nd Ed., 1992, page 221.
    :param x:
    :param n:
    :return:
    """
    #if np.any(x<0): # Probably don't need this exception if inverse-gamma checks anyway
    #    raise
    return gammainc(x/2, n/2) # FIXME: Need inverse gamma function


#
# Tests
#
if __name__ == '__main__':
    # FIXME: add tests here
