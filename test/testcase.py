from app import entity_link
from util import doc_parser

def small_reason_test():
    links = {"zs": ["shzs", "bjzs", "njzs"], "shzs": ["maths"], "bjzs": ["english", "cpu"], "njzs": ["cpu"],
             "maths": ["science"],"cpu":["science"],"english":["literature"]}
    doc = ["zs", "english"]
    mentions, candidates, g, tdi, entities = entity_link.wrap_link_document(links, doc)

    T = entity_link.entity_link(mentions, g, candidates, tdi)
    print T
    assert T[entities["zs"]] == entities["bjzs"]


def small_reason_test_2():
    links = {"zs": ["shzs", "bjzs", "njzs"], "shzs": ["maths","english"], "bjzs": ["english", "cpu"], "njzs": ["maths","cpu"],
             "maths": ["science"],"cpu":["science"],"english":["literature"]}
    doc = ["zs", "cpu", "maths"]
    mentions, candidates, g, tdi, entities = entity_link.wrap_link_document(links, doc)

    T = entity_link.entity_link(mentions, g, candidates, tdi)
    print T
    #assert T[entities["zs"]] == entities["bjzs"]


if __name__ == "__main__":
    # small_reason_test_2()
    print doc_parser.parse("../doc/doc0.txt")