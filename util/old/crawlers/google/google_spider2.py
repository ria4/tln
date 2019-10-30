#!/usr/bin/python

import scrapy

class WikipediaSpider(scrapy.Spider):
    name = "wikipedia_id"
    custom_settings = {'DEFAULT_REQUEST_HEADERS': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en'}}

    def start_requests(self):
        url = 'https://google.com/'
        q = getattr(self, 'search', None)
        if q is not None:
            url += 'search?q=%s' % q
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        first_link = response.css('h3.r')[0].css('a::attr(href)').extract_first()
        q = getattr(self, 'search', None)
        if not 'en.wikipedia' in first_link or 'group' in first_link or 'musician' in first_link:
            wikipedia_id = None
        elif q[33].lower() != first_link[37].lower():
            wikipedia_id = None
        else:
            idx = first_link.find('&')
            wikipedia_id = first_link[37:idx]
        yield {'id': wikipedia_id}

