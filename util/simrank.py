import networkx
import numpy
import itertools
from collections import defaultdict
import copy


def simrank(G, r=0.8, max_iter=100, eps=1e-4):

    nodes = G.nodes()
    nodes_i = {k: v for(k, v) in [(nodes[i], i) for i in range(0, len(nodes))]}

    sim_prev = numpy.zeros(len(nodes))
    sim = numpy.identity(len(nodes))

    for i in range(max_iter):
        if numpy.allclose(sim, sim_prev, atol=eps):
            break
        sim_prev = numpy.copy(sim)
        for u, v in itertools.product(nodes, nodes):
            if u is v:
                continue
            u_ns, v_ns = G.neighbors(u), G.neighbors(v)

            # evaluating the similarity of current iteration nodes pair
            if len(u_ns) == 0 or len(v_ns) == 0:
                # if a node has no predecessors then setting similarity to zero
                sim[nodes_i[u]][nodes_i[v]] = 0
            else:
                s_uv = sum([sim_prev[nodes_i[u_n]][nodes_i[v_n]] for u_n, v_n in itertools.product(u_ns, v_ns)])
                sim[nodes_i[u]][nodes_i[v]] = (r * s_uv) / (len(u_ns) * len(v_ns))


    return sim