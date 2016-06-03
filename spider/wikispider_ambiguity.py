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
    WORD = ""
    fn = os.path.realpath(__file__)+"temp_output.txt"

    def __init__(self, *args, **kwargs):
        super(WikiSpider_ambiguity, self).__init__(*args, **kwargs)
        self.word = WikiSpider_ambiguity.WORD
        self.start_urls = ('http://en.wikipedia.org/wiki/'+self.word+"_(disambiguation)",)
        self.fl = open(WikiSpider_ambiguity.fn, "wb")
        self.record = {}
        self.max_dis_link = 5
        self.max_link = 5
        self.round = 2
        self.first_title = "$"+self.word+"$"

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
        for l in range(0, min(self.max_link, len(links))):
            if "wiki" not in links[l] or "disambiguation" in links[l]:
                continue
            word = links[l][6:]
            if not self.record.has_key(word):
                self.record[title].append(word)
                nexts.append("http://en.wikipedia.org" + links[l])
        print "#####", rd, "#####", self.record
        # go to the next link
        for page in nexts:
            yield Request(page, self.parse_entity_page, meta={'round': rd - 1})


    def parse(self, response):

        # check whether this article is ambiguity
        self.record[self.first_title] = []
        page_title = response.xpath('//div[@id="content"]/h1[@id="firstHeading"]/text()').extract()[0]
        if "disambiguation" in page_title:
            print "@disambiguation page@"
            body = response.xpath("//body").extract()
            if "Wikipedia does not have an article with this exact name" in body:
                # no such word we try the search the word
                print "@not find@"
                yield Request('http://en.wikipedia.org/wiki/'+self.word, self.parse)

            else:
                print "@this is the exact disambiguation@"
                # so this is a truly ambiguity page
                # we need to copy all the links down as the candidates
                links = response.xpath\
                    ('//div[@id="content"]'
                     '/div[@id="bodyContent"]'
                     '/div[@id="mw-content-text"]'
                     '/descendant::ul/descendant::li/a/@href[not(contains(.,"#"))]').extract()
                print links
                nexts = []
                for l in range(0, min(self.max_dis_link, len(links))):
                    if "wiki" not in links[l] or "disambiguation" in links[l]:
                        print "illegal" ,links[l]
                        continue
                    word = links[l][6:]
                    if not self.record.has_key(word):

                        self.record[self.first_title].append(word)
                        nexts.append("http://en.wikipedia.org" + links[l])
                print "$$$$$", self.round, "$$$$$", nexts
                for page in nexts:
                    yield Request(page, self.parse_entity_page, meta={'round': self.round - 1})

        else:
            # we redirect here so the title is the only candidate
            # then we get the relative link
            print "@redirect to the page@"
            self.record[self.first_title] = [page_title]
            # then request
            yield Request(response.url, self.parse_entity_page, meta={"round": self.round-1})

    def close(self, reason):
        print "close..."
        json.dump(self.record, self.fl)
        self.fl.close()

    @staticmethod
    def crawl(word=""):
        process = CrawlerProcess()
        WikiSpider_ambiguity.WORD = word
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
