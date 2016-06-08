import numpy as np
import math
import util.numpy_helper

KL_L = 20


def kl(p, q, kl_l=KL_L):
    """Kullback-Leibler divergence D(P || Q) for discrete distributions

    Parameters
    ----------
    p, q : array-like, dtype=float, shape=n
    Discrete probability distributions.
    """
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)
    p = util.numpy_helper.normalize_vector(p)
    q = util.numpy_helper.normalize_vector(q)
    #d = np.where(np.logical_and(p > 0, q > 0.001), 1, 0)
    #a = np.sum(np.where(np.logical_and(p > 0, q > 0.001), p * np.log(p / q), 0))
    #b = np.sum(np.where(q == 0, l, 0))
    sums = 0

    for i in range(0, p.shape[0]):
        if q[i] == 0:
            sums += p[i, 0]*kl_l
        elif p[i] == 0:
            sums += 0
        else:
            sums += p[i, 0] * math.log(1.0*p[i, 0]/q[i, 0])
    return sums


def vdist(p, q, kl_l=0):

    p = util.numpy_helper.normalize_vector(p)
    q = util.numpy_helper.normalize_vector(q)
    sums = p.T*q;
    if sums == 0:
        return 9999999
    return 1/sums