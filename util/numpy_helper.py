import numpy as np
import networkx as nx


def normalize_vector(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v/norm


def normalize_matrix(g):

    # laplace
    # then build the W
    # node_size = len(g.nodes())
    # for i in range(0, node_size):
    #    for j in range(0, node_size):
    #        if row_idx[j] in g.neighbors(row_idx[i]):
    #            W[i, j] = g[row_idx[i]][row_idx[j]]["weight"]
    #        else:
    #            W[i, j] = 0
    # return numpy.asmatrix(csgraph.laplacian(W, normed=True))
    # row normal
    w, _ = nx.attr_matrix(g, edge_attr="weight", normalized=True)
    return w