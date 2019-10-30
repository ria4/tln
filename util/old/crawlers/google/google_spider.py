#!/usr/bin/python

import scrapy

class IMDBIDSpider(scrapy.Spider):
    name = "imdb_id"

    def start_requests(self):
        url = 'https://google.com/'
        q = getattr(self, 'search', None)
        if q is not None:
            url += 'search?q=%s' % q
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        imbd_id = response.css('h3.r')[0].css('a::attr(href)').extract_first()[33:42]
        yield {'id': imbd_id}

