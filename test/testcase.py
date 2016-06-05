from app import entity_link
from util import doc_parser
from spider import wikispider_ambiguity


def small_reason_test():
    links = {"zs": ["shzs", "bjzs", "njzs"], "shzs": ["maths"], "bjzs": ["english", "cpu"], "njzs": ["cpu"],
             "maths": ["science"],"cpu":["science"],"english":["literature"]}
    doc = ["zs", "english"]
    mentions, candidates, g, tdi, entities = entity_link.wrap_link_document(links, doc)

    T = entity_link.entity_link(mentions, g, candidates, tdi)
    assert T[entities["zs"]] == entities["bjzs"]


def small_reason_test_2():
    links = {"zs": ["shzs", "bjzs", "njzs"], "shzs": ["maths","english"], "bjzs": ["english", "cpu"], "njzs": ["maths","cpu"],
             "maths": ["science"], "cpu":["science"],"english":["literature"]}
    doc = ["zs", "cpu", "maths"]
    mentions, candidates, g, tdi, entities = entity_link.wrap_link_document(links, doc)

    T = entity_link.entity_link(mentions, g, candidates, tdi)
    assert T[entities["zs"]] == entities["njzs"]


def small_reason_noise_test():
    links = {"stock":["market","finance","fish"],"market":["finance","price"],"price":["market","location"]}
    mentions = ["stock","price"]
    mentions, candidates, g, tdi, prior, entities = entity_link.wrap_link_document(links, mentions)
    T = entity_link.entity_link(mentions, g, candidates, tdi, prior)
    assert T[entities["price"]] == entities["market"]


def small_doc_test():
    mentions = doc_parser.parse("../doc/doc0.txt")
    links = wikispider_ambiguity.WikiSpider_ambiguity.crawl(words=mentions)
    print links
    mentions, candidates, g, tdi, prior, entities = entity_link.wrap_link_document(links, mentions)
    T = entity_link.entity_link(mentions, g, candidates, tdi, prior)
    print T


def market_doc_test():
    mentions = doc_parser.parse("../doc/doc1.txt")
    links = wikispider_ambiguity.WikiSpider_ambiguity.crawl(words=mentions)
    print links
    mentions, candidates, g, tdi, prior, entities = entity_link.wrap_link_document(links, mentions)
    T = entity_link.entity_link(mentions, g, candidates, tdi, prior)
    print T

def first_article_test():
    mentions = doc_parser.parse("../doc/A Weekend in Chicago: Where Gunfire Is a Terrifying Norm")
    links = wikispider_ambiguity.WikiSpider_ambiguity.crawl(words=mentions)
    print links
    mentions, candidates, g, tdi, prior, entities = entity_link.wrap_link_document(links, mentions)
    T = entity_link.entity_link(mentions, g, candidates, tdi, prior)
    print T


if __name__ == "__main__":

    #small_reason_test()
    #small_reason_test_2()
    #print doc_parser.parse("../doc/doc0.txt")

    #small_doc_test()
    first_article_test()
    #kl_test()