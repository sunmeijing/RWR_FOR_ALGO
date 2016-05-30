import networkx as nx
import pydot

def prepare_test_nx_graph():
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
    G.add_edge(0, 1, weight=3)
    G.add_edge(0, 2, weight=2)
    # G.add_edge(2, 3, weight=1)
    G.add_edge(1, 3, weight=1)
    G.add_edge(2, 4, weight=1)
    G.add_edge(1, 4, weight=1)
    G.add_edge(0, 3, weight=3)
    G.add_edge(0, 2, weight=4)
    G.add_edge(3, 4, weight=5)

    G.graph['edge_weight_attr'] = 'weight'
    return G


def help_draw_graph(graph, fn):
    write_dot(G, 'temp_example.dot')
    g = pydot.graph_from_dot_file('temp_example.dot')
    g.write_png(fn)


def construct_from_dict(dic):
    def add(G, mp, key, it):
        if key not in mp.keys():
            G.add_node(it)
            mp[key] = it
            it += 1
        return it
    G = nx.Graph()
    mp = {}
    i = 0
    for key in dic.keys():
        i = add(G, mp, key, i)
        for link in dic[key]:
            i = add(G, mp, link, i)
    for key in dic.keys():
        for link in dic[key]:
            G.add_edge(mp[key], mp[link], weight=1)

    return G, mp
