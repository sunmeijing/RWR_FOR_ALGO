from scrapy import cmdline
from scrapy.spiders import Spider
from scrapy.http.request import Request
from scrapy.crawler import CrawlerProcess
import json
import os


class WikiSpider_ambiguity(Spider):

    name = 'wiki_am'
    allowed_domains = ["en.wikipedia.org"]
    start_urls = () # ("http://en.wikipedia.org/wiki/Apple_(disambiguation)",)
    WORDS = []
    handle_httpstatus_list = [404]
    fn = os.path.realpath(__file__)+"temp_output.txt"

    def __init__(self, *args, **kwargs):
        super(WikiSpider_ambiguity, self).__init__(*args, **kwargs)
        self.words = WikiSpider_ambiguity.WORDS
        self.start_urls = []
        for word in self.words:
            self.start_urls.append('http://en.wikipedia.org/wiki/'+word[1:-1]+"_(disambiguation)")
        self.fl = open(WikiSpider_ambiguity.fn, "wb")
        self.record = {}
        self.max_dis_link = 20
        self.max_link = 5
        self.round = 2
        for word in self.words:
            self.record[word.lower()] = []

    def parse_entity_page(self, response):
        rd = response.meta["round"]
        if rd <= 0:
            return
        titles = response.xpath('//div[@id="content"]/h1[@id="firstHeading"]/text()').extract()
        if len(titles) == 0:
            return
        title = titles[0]
        links = response.xpath(
            '//div[@id="content"]/div[@id="bodyContent"]/div[@id="mw-content-text"]/descendant::p/a/@href').extract()
        self.record[title.lower()] = []
        nexts = []
        for l in range(0, min(self.max_link, len(links))):
            if "wiki" not in links[l] or "disambiguation" in links[l]:
                continue
            word = links[l][6:]
            word = word.replace("_", " ")
            if not self.record.has_key(word):
                self.record[title.lower()].append(word.lower())
                nexts.append("http://en.wikipedia.org" + links[l])
        # print "#####", rd, "#####", self.record
        # go to the next link
        for page in nexts:
            yield Request(page, self.parse_entity_page, meta={'round': rd - 1})


    def parse(self, response):

        # check whether this article is ambiguity

        page_title = response.xpath('//div[@id="content"]/h1[@id="firstHeading"]/text()').extract()[0]
        first_title = "$"+page_title.replace(" (disambiguation)", "").lower()+"$"
        self.record[first_title] = []
        body_text = response.xpath("//body").extract()[0]
        if response.status == 404:
            #print "@not find 404@", page_title
            candidate_title = page_title

            if " (disambiguation)" in candidate_title:
                candidate_title = page_title.replace(" (disambiguation)", "")
            self.record[first_title.lower()].append(candidate_title.lower())
            yield Request("http://en.wikipedia.org/wiki/"+candidate_title, self.parse_entity_page, meta={"round": self.round - 1})

        elif "disambiguation" in page_title or "page lists articles associated with the title" in body_text:

            #print "@this is the exact disambiguation@"
            # so this is a truly ambiguity page
            # we need to copy all the links down as the candidates
            links = response.xpath\
                ('//div[@id="content"]'
                 '/div[@id="bodyContent"]'
                 '/div[@id="mw-content-text"]'
                 '/descendant::ul/descendant::li/a/@href[not(contains(.,"#"))]').extract()
            main_links = response.xpath(
            '//div[@id="content"]/div[@id="bodyContent"]/div[@id="mw-content-text"]/descendant::p/b/a/@href').extract()
            for l in links:
                main_links.append(l)
            links = main_links
            #print links
            nexts = []
            for l in range(0, min(self.max_dis_link, len(links))):
                if "wiki" not in links[l] or "disambiguation" in links[l]:
                    # print "illegal" ,links[l]
                    continue
                word = links[l][6:]
                word = word.replace("_", " ")
                if not self.record.has_key(word):

                    self.record[first_title.lower()].append(word.lower())
                    nexts.append("http://en.wikipedia.org" + links[l])
            # print "$$$$$", self.round, "$$$$$", nexts
            for page in nexts:
                yield Request(page, self.parse_entity_page, meta={'round': self.round - 1})

        else:
            # we redirect here so the title is the only candidate
            # then we get the relative link
            #print "@redirect to the page@"
            candidate_title = page_title
            if " (disambiguation)" in candidate_title:
                candidate_title = page_title.replace(" (disambiguation)", "")

            yield Request("http://en.wikipedia.org/wiki/" + candidate_title, self.parse_entity_page,
                          meta={"round": self.round - 1})

            # then request

    def close(self, reason):

        json.dump(self.record, self.fl)
        self.fl.close()

    @staticmethod
    def crawl(words=""):
        process = CrawlerProcess()
        WikiSpider_ambiguity.WORDS = words
        process.crawl(WikiSpider_ambiguity)
        process.start()
        f = open(WikiSpider_ambiguity.fn,"r")
        dic = json.load(f)
        f.close()
        return dic

if __name__=="__main__":
    process = CrawlerProcess()
    WikiSpider_ambiguity.WORD = "Apple"
    process.crawl(WikiSpider_ambiguity)
    process.start()
    #cmdline.execute("scrapy runspider wikispider_ambiguity.py".split())
