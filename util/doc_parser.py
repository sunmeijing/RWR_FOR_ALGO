import re


def parse(docfl,delimiter = "$"):
    fl = open(docfl, "r")
    content = ""
    for line in fl:
        content += line
        print line
    mentions = re.findall('\$([^$]*)\$', content)
    for i in range(0, len(mentions)):
        mentions[i] = delimiter+mentions[i]+delimiter
    return mentions
