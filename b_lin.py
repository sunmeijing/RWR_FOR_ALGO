import numpy
import metis
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
import pydot
from scipy.sparse import csgraph

PROB = 0.3


def prepare_nx_graph():
    G = nx.Graph()
    G.add_node(0)
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    G.add_edge(0, 0, weight=1)
    G.add_edge(1, 1, weight=1)
    G.add_edge(2, 2, weight=1)
    G.add_edge(3, 3, weight=1)
    G.add_edge(4, 4, weight=1)
    G.add_edge(1, 2, weight=1)
    # G.add_edge(2, 3, weight=1)
    # G.add_edge(1, 3, weight=1)
    G.add_edge(2, 4, weight=1)
    G.add_edge(1, 4, weight=1)
    G.add_edge(0, 3, weight=3)
    # G.add_edge(0, 2, weight=4)
    G.add_edge(3, 4, weight=5)

    G.graph['edge_weight_attr'] = 'weight'
    return G


def normalize_matrix(W):
    # TODO other algorithm
    return numpy.asmatrix(csgraph.laplacian(W, normed=True))


def low_rank_approx_svd(W2, t):
    # TODO other algorithm
    U, s, V = numpy.linalg.svd(W2, full_matrices=t)
    U = numpy.asmatrix(U)
    V = numpy.asmatrix(V)
    S = numpy.asmatrix(numpy.diag(s))
    print S
    return U, S, V


def offline_b_lin_method(nx_graph, attempt_split_parts=2, prob=PROB, t=False):

    """
    :param nx_graph: networkx graph
    :param attempt_split_parts:
    to split the graph into several parts
    note: might get fewer cuts desired
    :param prob: probability to restart to origin pos
    :param t: the similarity to decompose the W2 matrix
    :return: W_telta, Q1_I, U, A, V
    :bug: if the W2 is a singular matrix then A fails
    """

    # phase 1: graph partition
    G = metis.networkx_to_metis(nx_graph)
    (objval, parts) = metis.part_graph(G, attempt_split_parts)
    # we should normalize parts since we CAN get the FEWER parts

    # record all node index in one partition {partitionId:[nodeIds]}
    groups = {}
    for r, gn in enumerate(parts):
        if gn not in groups.keys():
            groups[gn] = []
        groups[gn].append(r)
    for key in groups.keys():
        groups[key] = sorted(groups[key])
    # print (objval, parts)
    # we build the W_telta as a normalized matrix
    node_size = len(nx_graph.nodes())
    W = numpy.matrix([[0.0]*node_size]*node_size)
    # first we construct the index
    row_idx = []
    for part in groups.keys():
        for idx in groups[part]:
            row_idx.append(idx)

    # then build the W
    for i in range(0, node_size):
        for j in range(0, node_size):
            if row_idx[j] in nx_graph.neighbors(row_idx[i]):
                W[i, j] = nx_graph[row_idx[i]][row_idx[j]]["weight"]
            else:
                W[i, j] = 0
    # finally normalize it
    # we could use other methods to normalize to see the effect
    W_telta = normalize_matrix(W)

    # phase 2 and 3
    # w1 contains all within partition link
    W1_group = {}
    W1 = numpy.matrix([[0.0] * node_size] * node_size)
    cur_k_row = 0
    for gn in groups.keys():
        matrix_len = len(groups[gn])
        W1_group[gn] = numpy.matrix([[0.0]*matrix_len]*matrix_len)
        for i in range(0, matrix_len):
            for j in range(0, matrix_len):
                W1_group[gn][i, j] = W_telta[cur_k_row+i, cur_k_row+j]
                W1[cur_k_row+i, cur_k_row+j] = W_telta[cur_k_row+i, cur_k_row+j]
        cur_k_row += matrix_len
    # w2 contains all without partition link
    W2 = W_telta - W1

    # phase 4
    # pre-compute Q
    Q1_I_group = {}
    for key in W1_group.keys():
        Q1_I_group[key] = \
            (numpy.identity(W1_group[key].shape[0]) - prob*W1_group[key]).I

    # phase 5
    # do low rand approx
    # currently we use the default
    # *we may further use other approx to test*
    # #pymf#
    U,S,V = low_rank_approx_svd(W2, t)
    # TODO if u v s is not full rank matrix we need to compute NB_LIN
    try:
        S_I = S.I
    except Exception:
        return None
    # phase 6 construct Q1_I
    Q1_I = numpy.matrix([[0.0]*node_size]*node_size)
    diag_index = 0
    for gn in groups.keys():
        if gn in Q1_I_group.keys():
            sz = Q1_I_group[gn].shape[0]
            for i in range(0, sz):
                for j in range(0, sz):
                    Q1_I[i+diag_index, j+diag_index] = Q1_I_group[gn][i, j]
            diag_index += sz
    A = (S.I - prob*V*Q1_I*U).I
    return W_telta, Q1_I, U, A, V


def online_b_lin_method(Q1_I, ei, U, A, V, prob = PROB):
    return (1-prob)*(Q1_I*ei+prob*Q1_I*U*A*V*Q1_I*ei)


def pre_compute_method(W_telta, ei, prob = PROB):
    return (1-prob)*(numpy.identity(W_telta.shape[0])-prob*W_telta).I*ei


def on_the_fly_method():
    # TODO
    pass


def help_draw_graph(graph, fn):
    write_dot(G, 'temp_example.dot')
    g = pydot.graph_from_dot_file('temp_example.dot')
    g.write_png(fn)

if __name__ == "__main__":
    W_telta, Q1_I, U, A, V = offline_b_lin_method(prepare_nx_graph(), 2)
    ei = numpy.array([[1], [0], [0], [0], [0]])

    r1 = online_b_lin_method(Q1_I, ei, U, A, V)
    r2 = pre_compute_method(W_telta,ei)
    print r2-r1


