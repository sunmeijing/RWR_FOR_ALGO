from scrapy import cmdline
from scrapy.spider import Spider
from scrapy.http.request import Request
from scrapy.xlib.pydispatch import dispatcher

class CollegesSpider(Spider):

    name = 'colleges'
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ('http://en.wikipedia.org/wiki/Apple',)

    def __init__(self):
        self.fl = open("output.txt", "wb")
        self.record = {}
        self.round = 2
        self.max_link = 2

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse_disambiguity(self, response):
        rd = response.meta["round"]
        if rd <= 0:
            return
        title = response.xpath('//div[@id="content"]/h1[@id="firstHeading"]/text()').extract()[0]
        links = response.xpath('//div[@id="content"]/div[@id="bodyContent"]/div[@id="mw-content-text"]/p/a/@href').extract()
        self.record[title] = []
        nexts = []
        for l in range(0, min(self.max_link, len(links))):
            word = links[l][5:]
            if not self.record.has_key(word):
                self.record[title].append(word)
                nexts.append("http://en.wikipedia.org"+links[l])
        print "#####", rd, "#####", self.record
        # go to the next link
        for page in nexts:
            yield Request(page, self.parse_disambiguity, meta={'round': rd-1})

    def parse(self, response):

        if self.round <= 0:
            return
        title = response.xpath('//div[@id="content"]/h1[@id="firstHeading"]/text()').extract()[0]
        links = response.xpath(
            '//div[@id="content"]/div[@id="bodyContent"]/div[@id="mw-content-text"]/p/a/@href').extract()
        self.record[title] = []
        nexts = []
        for l in range(0, min(self.max_link, len(links))):
            word = links[l][5:]
            if not self.record.has_key(word):
                self.record[title].append(word)
                nexts.append("http://en.wikipedia.org" + links[l])
        print "#####", self.round, "#####", self.record
        # go to the next link
        for page in nexts:
            yield Request(page, self.parse_disambiguity, meta={'round': self.round - 1}, )

    def close(self, reason):
        self.fl.close()
        pass

if __name__=="__main__":
    cmdline.execute("scrapy runspider wikispider.py".split())
