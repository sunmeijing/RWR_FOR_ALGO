import numpy as np
import math
import numpy_helper


def kl(p, q, l=20):
    """Kullback-Leibler divergence D(P || Q) for discrete distributions

    Parameters
    ----------
    p, q : array-like, dtype=float, shape=n
    Discrete probability distributions.
    """
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)
    p = numpy_helper.normalize_vector(p)
    q = numpy_helper.normalize_vector(q)
    #d = np.where(np.logical_and(p > 0, q > 0.001), 1, 0)
    #a = np.sum(np.where(np.logical_and(p > 0, q > 0.001), p * np.log(p / q), 0))
    #b = np.sum(np.where(q == 0, l, 0))
    sums = 0

    for i in range(0, p.shape[0]):
        if q[i] == 0:
            sums += l
        elif p[i] == 0:
            sums += 0
        else:
            sums += p[i,0] * math.log(1.0*p[i,0]/q[i,0])
    return sums