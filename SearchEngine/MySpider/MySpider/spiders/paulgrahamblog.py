# -*- coding: utf-8 -*-
import scrapy
import tldextract
#from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider
import json


class paulgrahamblogSpider(scrapy.Spider):
    name = 'paulgrahamblog'
    allowed_domains = ['paulgraham.com']

    maximumPagesPerSite = 10
    crawledPagesPerSite = {}
    file_link_map = {}
    count = 0

    def __init__(self):
        self.maximumPagesPerSite = 10

    def start_requests(self):
        urls = [
            'http://paulgraham.com/articles.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # limit running times
        domain_name = tldextract.extract(response.url).domain
        #print("The domain name is", domain_name)
        if domain_name != 'paulgraham':
            return
        if domain_name in self.crawledPagesPerSite:
            if self.crawledPagesPerSite['paulgraham'] >= self.maximumPagesPerSite:
                with open("file_link_map.json", 'w') as f:
                    f.write(json.dumps(self.file_link_map))
                    f.close()
                raise CloseSpider('spider closed!')
                # return
            self.crawledPagesPerSite[domain_name] += 1
        else:
            self.crawledPagesPerSite[domain_name] = 1

        # page = response.url.split("/")[-2]
        # filename = './input/%s.html' % page
        print
        response.url
        self.count = self.count + 1
        filename = './input/%s.html' % self.count
        self.file_link_map[filename] = response.url
        with open(filename, 'wb') as f:
            f.write(response.body)
        # self.log('Saved file %s' % filename)

        # get next url
        sel = Selector(response)
        urls = sel.xpath('//a/@href').extract()
        for url in urls:
            # print url
            if url.find("http") == -1:
                url = "http://paulgraham.com/" + url
                # print url

            yield Request(url, callback=self.parse)