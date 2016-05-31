import re


def parse(docfl):
    fl = open(docfl, "r")
    content = ""
    for line in fl:
        content += line
        print line
    mentions = re.findall('\$([^$]*)\$', content)
    return mentions
