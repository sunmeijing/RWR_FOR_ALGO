import numpy as np

from algo import random_walk
from util import kl, simrank, numpy_helper, tfidf_util, graph_util

PROB = 0.85


def compute_document_signature(W_telta, Ed, candidates, mentions, tfidf, prob=PROB):
    # TODO
    node_sz = W_telta.shape[0]
    vector = np.array([[0.0]]*node_sz)
    for entity in Ed:
        v = 0
        for mention in mentions:
            if entity in candidates[mention]:
                # we use uniformly weights
                v = tfidf[mention] * 1/len(candidates[mention])
        vector[entity[0]] = v
    vector = numpy_helper.normalize_vector(vector)
    r = random_walk.pre_compute_method(W_telta, vector, prob)
    r = numpy_helper.normalize_vector(r)
    return r


def compute_entity_signature(W_telta, entity, prob=PROB):
    # TODO
    l = W_telta.shape[0]
    ei = np.array([[0.0]]*l)
    ei[entity[0]] = 1
    r = random_walk.pre_compute_method(W_telta, ei, prob)
    r = numpy_helper.normalize_vector(r)
    return r


def semantic_similarity(sig_entity, sig_document):

    return 1.0/kl.kl(sig_entity, sig_document, 20)


def entity_link(mentions, graph, candidates, tfidf):
    """
    :param mentions: the set of mentions to disambiguation []
    :param graph: networkx
    :param candidates: the set of candidates {}
    :param tfidf: the importance score of mention in graph
    :return: a value to the mentions
    """
    Ed = []
    T = {}
    # corner case to check that there is no single node to assure
    for node in graph.nodes():
        if len(graph.neighbors(node)) == 0:
            # we add self link
            graph.add_edge(node, node, weight=1)
    W_telta = numpy_helper.normalize_matrix(graph)
    SIMLARITY_THREHOLD = 0

    for mention in mentions:
        if mention not in candidates.keys():
            candidates[mention] = []
            T[mention] = None
        elif len(candidates[mention]) == 0:
            T[mention] = None
        elif len(candidates[mention]) == 1:
            Ed.append(candidates[mention][0])
            T[mention] = candidates[mention][0]
    if len(Ed) == 0:
        # currently
        for mention in mentions:
            for entity in candidates[mention]:
                Ed.append(entity)
        if len(Ed) == 0:
            return T

    sig_document = compute_document_signature(W_telta, Ed, candidates, mentions, tfidf)

    mentions = sorted(mentions, key=lambda mention: len(candidates[mention]))
    local_sims = simrank.simrank(graph)
    # print local_sims
    for mention in mentions:
        if len(candidates[mention]) > 1:
            max_score = -999999999999
            max_score_entity = None
            for entity in candidates[mention]:
                sig_entity = compute_entity_signature(W_telta, entity)
                # use this cause too many noise
                # if one link has many sub node then it can be very high
                phy_1 = local_sims[mention[0]][entity[0]] / 10000
                phy_2 = semantic_similarity(sig_entity, sig_document)


                print entity[1],":",mention, phy_1 , phy_2
                if phy_1+phy_2 > max_score:
                    max_score = phy_1 + phy_2
                    max_score_entity = entity

            if max_score < SIMLARITY_THREHOLD:
                T[mention] = None
                #candidates[mention].remove(max_score_entity)
            else:
                Ed.append(max_score_entity)
                T[mention] = max_score_entity
                sig_document = compute_document_signature(W_telta, Ed, candidates, mentions, tfidf)
    return T


def wrap_link_document(links, doc):
    g, mp = graph_util.construct_from_dict(links)
    impscore = tfidf_util.construct_from_dict(links, doc)
    mentions = []
    candidates = {}
    entities = {}
    for name in mp.keys():
        entities[name] = (mp[name], name)
    for word in doc:
        mentions.append(entities[word])
    for word in doc:
        if word in links.keys():
            for candidate_name in links[word]:
                if entities[word] not in candidates.keys():
                    candidates[entities[word]] = []
                candidates[entities[word]].append(entities[candidate_name])
    tdi = {}
    for word in impscore:
        tdi[entities[word]] = impscore[word]
    print entities
    return mentions, candidates, g, tdi, entities

