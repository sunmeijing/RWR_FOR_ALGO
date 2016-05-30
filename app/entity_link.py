import numpy as np

from algo import random_walk
from util import kl, simrank, numpy_helper, tfidf_util, graph_util


def compute_document_signature(W_telta, Ed, candidates, mentions, tfidf, prob=0.15):
    # TODO
    node_sz = W_telta.shape[0]
    vector = np.array([[0]]*node_sz)
    for entity in Ed:
        v = 0
        for mention in mentions:
            if entity in candidates[mention]:
                # we use uniformly weights
                v = tfidf[mention] * 1/len(candidates[mention])
        vector[entity.node] = v
    r = random_walk.pre_compute_method(W_telta, vector, prob)
    r = numpy_helper.normalize_vector(r)
    return r


def compute_entity_signature(W_telta, entity, prob=0.15):
    # TODO
    l = W_telta.shape[0]
    ei = np.array([[0]]*l)
    ei[entity.node] = 1
    r = random_walk.pre_compute_method(W_telta, ei, prob)
    r = numpy_helper.normalize_vector(r)
    return r


def semantic_similarity(sig_entity, sig_document):

    return kl.kl(sig_entity, sig_document, 20)


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
    W_telta = numpy_helper.normalize_matrix(graph)
    SIMLARITY_THREHOLD = 0.01

    for mention in mentions:
        if mention not in candidates.keys():
            candidates[mention] = []
            T[mention] = None
        elif len(candidates[mention]) == 0:
            T[mention] = None
        elif len(candidates[mention]) == 1:
            Ed = Ed.append(candidates[mention][0])

    if len(Ed) == 0:
        # currently we don't want to do this
        pass

    sig_document = compute_document_signature(W_telta, Ed, candidates, mentions, tfidf)

    mentions = sorted(mentions, key=lambda mention: len(candidates[mention]))
    local_sims = simrank.simrank(graph)
    for mention in mentions:
        if len(candidates[mention]) > 1:
            max_score = -999999999999
            max_score_entity = None
            for entity in candidates[mention]:
                sig_entity = compute_entity_signature(W_telta, entity)
                phy_2 = semantic_similarity(sig_entity, sig_document)
                phy_1 = local_sims[mention.node][entity.node]
                if phy_1+phy_2 > max_score:
                    max_score = phy_1 + phy_2
                    max_score_entity = entity

            if max_score < SIMLARITY_THREHOLD:
                T[mention] = None
                candidates[mention].remove(max_score_entity)
            else:
                Ed.append(max_score_entity)
                T[mention] = max_score_entity
                sig_document = compute_document_signature(W_telta, Ed, candidates, mentions, tfidf)
    return T

if __name__ == "__main__":
    links = {"zs":["shzs","bjzs","njzs"],"shzs":["maths"],"bjzs":["english","cpu"],"njzs":["cpu"]}
    doc = ["zs","cpu"]
    g, mp = graph_util.construct_from_dict(links)
    score = tfidf_util.construct_from_dict(links, doc)
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

    print candidates
    # entity_link(mentions, g, candidates, score)
