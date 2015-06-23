#
# Basic Gaussian manipulation and inference utilities. Ported from
# matlab_utilities. Tim Bailey 2015.
#

import numpy as np
import scipy.linalg as sci
import scipy.special as sp
from basic import *

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
    f = sci.solve_triangular(L, v, lower=True) # 'normalised' innovation; f = inv(L)*v
    E = -0.5 * np.sum(f*f, axis=0)
    if logflag:
        C = 0.5*D*np.log(2*np.pi) + np.sum(np.log(L.diagonal()))
        w = E - C
    else:
        C = (2*np.pi)**(D/2.) * np.prod(L.diagonal())
        w = np.exp(E) / C
    return w

# Draw samples from a multivariate Gaussian
def gauss_samples(x, P, n):
    """
    :param x: mean vector
    :param P: covariance matrix
    :param n: number of samples
    :return: samples from Gauss(x,P); a matrix of n vectors
    """
    L = sci.cholesky(P, lower=True)
    X = np.random.standard_normal((len(x), n))
    return np.dot(L, X) + repcol(x, n)

def gauss_power(P, r):
    """
    Compute the covariance and weight of Gauss(x,P)**r
    :param P: covariance matrix
    :param r: exponent, such that we want
    :return (w, P/r): weight and covariance of Gauss(x,P)**r == w*Gauss(x,P/r)
    """
    s = r - 1
    d = P.shape[0]
    e = sci.eigh(P, eigvals_only = True) # real-symmetric eigen-vals
    w = 1 / np.sqrt((2*np.pi)**(d*s) * r**d * np.prod(e**s))
    return w, P/r

def sample_mean(x):
    n = x.shape[1]
    xm = np.sum(x, 1) / n
    P = np.dot(x, x.T) / n - np.outer(xm, xm)
    # Note: Need dot for the matrix expression and outer for the vector
    # expression. To call np.dot(xm, xm.T), we would first need to write
    # xm = xm[:,np.newaxis]

# Compute mean and covariance from set of weighted samples
def sample_mean_weighted(x, w, normalised_weights=True):
    if normalised_weights:
        if abs(1 - sum(w)) > 1e-12:
            raise ArithmeticError('Weights should be normalised')
        if sum(w!=0) <= len(x):
            raise ArithmeticError('Samples form a hyperplane, covariance rank deficient')
    w = reprow(w, x.shape[0])
    xm = np.sum(w*x, 1)
    xc = x - repcol(xm, x.shape[1])
    P = np.dot(w*xc, xc.T)
    return xm, P

def chi_square_density(x, n):
    """
    Compute n-dof Chi-square density function at points x
    Reference: Papoulis, "Probability, Random Variables and Stochastic Processes", 4th Ed., 2002, p89.
    :param x: x-axis coordinates
    :param n: degrees of freedom
    :return: f(x) - Chi-square probability density function
    """
    k = n/2
    C = 2**k * sp.gamma(k)
    return x**(k-1) * np.exp(-x/2) / C

def chi_square_mass(x,n):
    """
    Compute n-dof Chi-square mass function at points x
    Reference: Press, "Numerical Recipes in C", 2nd Ed., 1992, page 221.
    :param x:
    :param n:
    :return:
    """
    return sp.gammainc(x/2, n/2)

#
# Tests
#
if __name__ == '__main__':
    print(chi_square_mass(6,2))

    P = np.random.rand(3,3)
    P = np.dot(P, P.T)
    w, Pr = gauss_power(P, 2.3)

