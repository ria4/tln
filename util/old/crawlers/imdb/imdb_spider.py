#!/usr/bin/python
# coding: utf-8

import scrapy


class IMDBInfoSpider(scrapy.Spider):
    name = "imdb_info"

    custom_settings = {'DEFAULT_REQUEST_HEADERS': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'fr'}}

    #def make_requests_from_url(self, url):
    #    return Request(url, method='HEAD', dont_filter=True)
    
    def start_requests(self):
        url = 'http://www.imdb.com/title/'
        q = getattr(self, 'search', None)
        if q is not None:
            url += q + '/'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        vf_title = response.xpath("//h1[@itemprop='name']//text()")[0].extract()[:-1]

        original_title_res = response.xpath("//div[@class='originalTitle']//text()")
        if len(original_title_res) > 0:
            original_title = original_title_res[0].extract()
        else:
            original_title = ''

        directors_raw = response.xpath("//meta[@name='description']/@content")[0].extract()
        start = directors_raw.find('by') + 3
        end = directors_raw.find('.')
        directors = directors_raw[start:end].split(', ')

        date_raw = response.xpath("//meta[@property='og:title']/@content")[0].extract()
        start = date_raw.rfind('(') + 1
        end = -1
        date = date_raw[start:end]

        image_raw = response.xpath("//link[@rel='image_src']/@href")[0].extract()
        start = 0
        end = image_raw.rfind('.') - 1
        end = image_raw.rfind('.', 0, end)
        image_src = image_raw[start:end]

        yield {'artists': directors, 'year': date, 'image_src': image_src, 'title_vo': original_title, 'title_vf': vf_title}

