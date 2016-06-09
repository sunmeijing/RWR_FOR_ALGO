from app import entity_link
from util import doc_parser
from record_deco import *
from algo import random_walk, distance
from spider import wikispider_ambiguity


DATA_PATH = "./data/"
DATA_NAME = "doc0.txt"


def judge(T, ansfn):
    # read from the file
    ans_pair = doc_parser.read_ans_pair(ansfn)
    corrects = []
    if ans_pair == 0:
        return 1.0, corrects

    for ans in ans_pair:
        for run_ans_key in T.keys():
            if run_ans_key[1] == ans[0] and ans[1] == T[run_ans_key][1]:
                corrects.append(ans)

    return 1.0*len(corrects)/len(ans_pair), corrects


@record_results(DATA_PATH+DATA_NAME, DATA_NAME)
#@record_judge_result("./record.txt")
@record_time(DATA_PATH+DATA_NAME)
@record_use_parameter(DATA_PATH+DATA_NAME, depth=3, width=8, prob=0.85, kl_l=20)
@record_plug_algo(DATA_PATH+DATA_NAME, choice="normal")
def test_framework(docfn=None, ansfn=None, to_judge=False, links=None, doc=None,
                   delimeter="$", width=wikispider_ambiguity.ENTITY_WIDTH, depth=wikispider_ambiguity.DEPTH,
                   prob=random_walk.PROB, kl_l=distance.KL_L, choice="normal"):
    print ansfn
    if to_judge and not ansfn:
        raise Exception("please give ansfn")
    if docfn:
        doc = doc_parser.parse(docfn)
        links = wikispider_ambiguity.WikiSpider_ambiguity.crawl(words=doc, width=width, depth=depth)
        print links

    mentions, candidates, g, tdi, prior, entities \
        = entity_link.wrap_link_document(links, doc, delimeter=delimeter)
    T = None
    if choice == "normal":
        T = entity_link.entity_link(
            mentions, g, candidates, tdi, prior, prob=prob, kl_l=kl_l, isKL=True)
    elif choice == "only_simrank":
        T = entity_link.entity_link_only_with_simrank(
            mentions, g, candidates, tdi, prior, prob=prob, kl_l=kl_l, isKL=True)
    elif choice == "only_rwr":
        T = entity_link.entity_link_only_with_rwr(
            mentions, g, candidates, tdi, prior, prob=prob, kl_l=kl_l, isKL=True)
    elif choice == "with_dot":
        T = entity_link.entity_link(
            mentions, g, candidates, tdi, prior, prob=prob, kl_l=kl_l, isKL=False)
    elif choice == "prior":
        T = entity_link.entity_link_only_with_prior(
            mentions, g, candidates, tdi, prior, prob=prob, kl_l=kl_l, isKL=False)
        pass
    if to_judge:
        return judge(T, ansfn)
    else:
        return T, entities


def small_reason_test():
    # should return the ref with the only linking candidate
    links = {"zs": ["shzs", "bjzs", "njzs"], "shzs": ["maths"], "bjzs": ["english", "cpu"], "njzs": ["cpu"],
             "maths": ["science"],"cpu":["science"],"english":["literature"]}
    doc = ["zs", "english"]
    T, entities = test_framework(links=links, doc=doc)
    assert T[entities["zs"]] == entities["bjzs"]
    return T


def small_reason_test_2():
    # should return the ref with the linking candidate when linking is not the only one
    links = {"zs": ["shzs", "bjzs", "njzs"], "shzs": ["maths","english"], "bjzs": ["english", "cpu"], "njzs": ["maths","cpu"],
             "maths": ["science"], "cpu":["science"],"english":["literature"]}
    doc = ["zs", "cpu", "maths"]
    T, entities = test_framework(links=links, doc=doc)
    assert T[entities["zs"]] == entities["njzs"]
    return T


def small_reason_test_3():
    # TODO should catch the only candidate
    links = {"zs": ["shzs", "bjzs", "njzs"], "shzs": ["maths"], "bjzs": ["english", "cpu"], "njzs": ["cpu"],
             "maths": ["science"], "cpu": ["science"], "english": ["literature"]}
    doc = ["zs", "english"]
    return T


def small_reason_noise_test():
    links = {"stock":["market","finance","fish"],"market":["finance","price"],"price":["market","location"]}
    doc = ["stock","price"]
    T, entities = test_framework(links=links, doc=doc)
    assert T[entities["price"]] == entities["market"]
    return T


def small_doc_test(to_judge=False):
    T, entities = test_framework(docfn="../doc/doc0.txt", ansfn="../doc/ans/doc0.txt",to_judge=to_judge)
    return T


def market_doc_test(to_judge=False):
    T, entities = test_framework(docfn="../doc/doc1.txt", ansfn="../doc/ans/doc1.txt", to_judge=to_judge)
    return T


def first_article_test(to_judge=False):
    T, entities = test_framework(docfn="../doc/A Weekend in Chicago: Where Gunfire Is a Terrifying Norm",
                                 ansfn="../doc/A Weekend in Chicago: Where Gunfire Is a Terrifying Norm",
                                 to_judge=to_judge)
    return T


def try_doc_test():
    global DATA_PATH
    global DATA_NAME
    DATA_NAME = "doc0.txt"
    test_framework(docfn="../doc/"+DATA_NAME, ansfn="../doc/ans/"+DATA_NAME, to_judge=False)

    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"


if __name__ == "__main__":
    try_doc_test()
    #small_doc_test(to_judge=False)
    #small_reason_noise_test()
    #print doc_parser.parse("../doc/doc0.txt")

    #small_doc_test()
    #T = market_doc_test()
    #print T
    #kl_test()