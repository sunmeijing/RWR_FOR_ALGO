#!/usr/bin/env python

"""
The simplest TF-IDF library imaginable.
Add your documents as two-element lists `[docname, [list_of_words_in_the_document]]` with `addDocument(docname, list_of_words)`. Get a list of all the `[docname, similarity_score]` pairs relative to a document by calling `similarities([list_of_words])`.
See the README for a usage example.
"""

import math


class tfidf:
    def __init__(self):
        self.weighted = False
        self.documents = []
        self.corpus_dict = {}


    def addDocument(self, doc_name, list_of_words):
        # building a dictionary
        doc_dict = {}
        for w in list_of_words:
          doc_dict[w] = doc_dict.get(w, 0.) + 1.0
          self.corpus_dict[w] = self.corpus_dict.get(w, 0.0) + 1.0

        # normalizing the dictionary
        length = float(len(list_of_words))
        for k in doc_dict:
          doc_dict[k] = doc_dict[k] / length

        # add the normalized document to the corpus
        self.documents.append([doc_name, doc_dict])


    def similarities(self, list_of_words):
        """Returns a list of all the [docname, similarity_score] pairs relative to a list of words."""

        # building the query dictionary
        query_dict = {}
        for w in list_of_words:
          query_dict[w] = query_dict.get(w, 0.0) + 1.0

        # normalizing the query
        length = float(len(list_of_words))
        for k in query_dict:
          query_dict[k] = query_dict[k] / length

        # computing the list of similarities
        sims = []
        for doc in self.documents:
          score = 0.0
          doc_dict = doc[1]
          for k in query_dict:
            if k in doc_dict:
              score += (query_dict[k] / self.corpus_dict[k]) + (doc_dict[k] / self.corpus_dict[k])
          sims.append([doc[0], score])

        return sims


def construct_from_dict(dic, doc, delimeter="$", disambiguation=" (disambiguation)"):
    in_counts_mp = {}
    out_counts_mp = {}
    for word in doc:

        in_counts_mp[word] = doc.count(word)
        if word not in out_counts_mp.keys():
            out_counts_mp[word] = 0
            for key in dic:
                if key == word:
                    out_counts_mp[word] += 1
                elif delimeter+key+delimeter == word:
                    out_counts_mp[word] += 1

                elif word[len(delimeter):len(word)-len(delimeter)] in dic[key]:
                    out_counts_mp[word] += 1

    tdf = {}
    for word in doc:
        if out_counts_mp[word] == 0:
            out_counts_mp[word] = 1
        else:
            tdf[word] = 1.0*in_counts_mp[word]/len(doc) * math.log(1.0*len(dic.keys())/out_counts_mp[word])
    return tdf

if __name__ == "__main__":
    # unit tests
    links = {"stock": ["market", "finance", "fish"], "market": ["finance", "price"], "price": ["market", "location"]}
    ans = construct_from_dict(links,["stock","price"], delimeter="")
    assert ans["stock"] < ans["price"]