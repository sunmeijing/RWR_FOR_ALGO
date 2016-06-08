import re
import os


def parse(docfl, delimiter = "$"):
    fl = open(docfl, "r")
    content = ""
    for line in fl:
        content += line

    mentions = re.findall('\$([^$]*)\$', content)
    for i in range(0, len(mentions)):
        mentions[i] = (delimiter+mentions[i]+delimiter)
    fl.close()
    return mentions


def copy_mentions_into_answers(docfn, ansfn, delimiter="$"):
    fl = open(docfn, "r")
    ansfl = open(ansfn, "w")
    content = ""
    for line in fl:
        content += line

    mentions = re.findall('\$([^$]*)\$', content)
    for i in range(0, len(mentions)):
        mentions[i] = (delimiter + mentions[i] + delimiter)
    fl.close()
    for mention in mentions:
        ansfl.write(mention+":\n\r")
    ansfl.close()


def read_ans_pair(ansfn):
    ansfl = open(ansfn, "r")
    ans_pair = []
    for line in ansfl:
        line = line.rstrip()
        if line != "":
            rec = line.split(":")
            mention, ans = rec[0], rec[1]
            ans_pair.append((mention, ans))
    return ans_pair

if __name__ == "__main__":
    # unit tests
    # filenames = next(os.walk("../doc"))[2]
    # print filenames
    # for fn in filenames:
    #    copy_mentions_into_answers("../doc/"+fn, "../doc/ans/"+fn)
    print judge({(0,"$Jiaotong University$"): (1, "a")}, "../doc/ans/doc0.txt")
