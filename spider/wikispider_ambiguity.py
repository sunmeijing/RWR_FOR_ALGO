from scrapy.spiders import Spider
from scrapy.http.request import Request
from scrapy.crawler import CrawlerProcess
import json
import os

AMB_WIDTH = 20
ENTITY_WIDTH = 8
DEPTH = 3


class WikiSpider_ambiguity(Spider):

    name = 'wiki_am'
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ("http://en.wikipedia.org/",)
    WORDS = []
    handle_httpstatus_list = [404]
    fn = os.path.realpath(__file__)+".temp_output.txt"
    MAX_DIS_LINK = AMB_WIDTH
    MAX_LINK = ENTITY_WIDTH
    ROUND = DEPTH

    def __init__(self, *args, **kwargs):
        super(WikiSpider_ambiguity, self).__init__(*args, **kwargs)
        self.words = WikiSpider_ambiguity.WORDS
        self.record = {}
        for word in self.words:
            self.record[word] = []
        self.fl = open(WikiSpider_ambiguity.fn, "wb")

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
        self.record[title] = []
        nexts = []
        for l in range(0, min(WikiSpider_ambiguity.MAX_LINK, len(links))):
            if "wiki" not in links[l] or "disambiguation" in links[l]:
                continue
            word = links[l][6:]
            word = word.replace("_", " ")
            if not self.record.has_key(word):
                self.record[title].append(word)
                nexts.append("http://en.wikipedia.org" + links[l])
        # go to the next link
        for page in nexts:
            yield Request(page, self.parse_entity_page, meta={'round': rd - 1})

    def parse_disambiguation_page(self, response):
        # check whether this article is ambiguity

        page_title = response.xpath('//div[@id="content"]/h1[@id="firstHeading"]/text()').extract()[0]
        first_title = response.meta["name"]
        # first_title = "$" + page_title.replace(" (disambiguation)", "").lower() + "$"
        self.record[first_title] = []
        body_text = response.xpath("//body").extract()[0]
        if response.status == 404:
            print "@not find 404@", first_title
            # it might be directed to the only link try to link the first
            yield Request("http://en.wikipedia.org/wiki/" + first_title[1:-1], self.parse_disambiguation_page,
                          meta={"name": first_title})

        elif "disambiguation" in page_title or "page lists articles associated with the title" in body_text:

            print "@this is the exact disambiguation@", first_title
            # so this is a truly ambiguity page
            # we need to copy all the links down as the candidates
            links = response.xpath \
                ('//div[@id="content"]'
                 '/div[@id="bodyContent"]'
                 '/div[@id="mw-content-text"]'
                 '/descendant::ul/descendant::li/a/@href[not(contains(.,"#"))]').extract()
            main_links = response.xpath(
                '//div[@id="content"]/div[@id="bodyContent"]/div[@id="mw-content-text"]/descendant::p/b/a/@href').extract()
            for l in links:
                main_links.append(l)
            links = main_links
            # print links
            nexts = []
            for l in range(0, min(WikiSpider_ambiguity.MAX_DIS_LINK, len(links))):
                if "wiki" not in links[l] or "disambiguation" in links[l]:
                    # print "illegal" ,links[l]
                    continue
                word = links[l][6:]
                word = word.replace("_", " ")
                if not self.record.has_key(word):
                    self.record[first_title].append(word)
                    nexts.append("http://en.wikipedia.org" + links[l])
            # print "$$$$$", "$$$$$", nexts
            for page in nexts:
                yield Request(page, self.parse_entity_page, meta={'round': WikiSpider_ambiguity.ROUND - 1})
        elif "Wikipedia does not have an article with this exact name" in body_text:
            print "have no the correspondent article", first_title
            self.record[first_title] = []

        else:
            # we redirect here so the title is the only candidate
            # then we get the relative link
            print "@redirect to the page@", first_title
            self.record[first_title] = [page_title]
            yield Request(response.url+"?a=what", callback=self.parse_entity_page, meta={"round":WikiSpider_ambiguity.ROUND-1})

    def parse(self, response):
        # start search on the web

        self.start_urls = []
        for word in self.words:
            yield Request('http://en.wikipedia.org/wiki/' + word[1:-1] + "_(disambiguation)",
                          self.parse_disambiguation_page, meta={"name":word})

    def close(self, reason):

        json.dump(self.record, self.fl)
        self.fl.close()

    @staticmethod
    def crawl(words=[], width=ENTITY_WIDTH, depth=DEPTH):
        process = CrawlerProcess()
        WikiSpider_ambiguity.WORDS = words
        WikiSpider_ambiguity.ROUND = depth
        WikiSpider_ambiguity.MAX_LINK = width
        process.crawl(WikiSpider_ambiguity)
        process.start()
        f = open(WikiSpider_ambiguity.fn, "r")
        dic = json.load(f)
        f.close()
        return dic

if __name__=="__main__":
    # unit tests
    process = CrawlerProcess()
    print WikiSpider_ambiguity.crawl(words=["$NEW_YORK$","$Stock$","$price$","$share$","$market$"])

