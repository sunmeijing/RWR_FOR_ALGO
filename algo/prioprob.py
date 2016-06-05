def construct_from_dict(dic, doc, delimeter="$", disambiguation=" (disambiguation)"):
    res = {}
    # construct tuple
    for mention in doc:
        # count all the mention appearance
        appearance = doc.count(mention) + dic.keys().count(mention[len(delimeter):len(mention)-len(delimeter)])
        for key in dic.keys():
            # ignore the $delimeter$
            for entity in dic[key]:
                if entity == mention[len(delimeter):len(mention)-len(delimeter)]:
                    appearance += 1

        for prop_entity in dic[mention]:
            compositions = 1
            # compute all the {b:a}
            if prop_entity in dic.keys() and mention[len(delimeter):len(mention)-len(delimeter)] in dic[prop_entity]:
                compositions += 1
            # compute all the $b$:a
            if (delimeter+prop_entity+delimeter) in dic.keys() and mention[len(delimeter):len(mention)-len(delimeter)] in dic[delimeter+prop_entity+delimeter]:
                compositions += 1
            for key in dic.keys():
                if key != mention:
                    if mention[1:-1] in dic[key] and prop_entity in dic[key]:
                        compositions += 1
            res[(prop_entity, mention)] = 1.0*compositions/appearance
        appearance = 0
    return res

if __name__ =="__main__":
    # unit tests
    T = construct_from_dict({"$a$":["b"],"$b$":["c"],"$c$":["a","b"]}, ["$a$","$b$","$c$"])
    assert (len(T) == 4 and T[('b','$a$')] == 1.0 and T[('c','$b$')] > 0.6 and T[('b','$c$')] == 1.0 and T[('a','$c$')] == 0.5)
    links = {"stock": ["market", "finance", "fish"], "market": ["finance", "price"], "price": ["market", "location"]}
    print construct_from_dict(links,["stock","price"], delimeter="")