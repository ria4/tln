import scrapy

media = "albums"
last_page_index = 11

base_url = "https://www.senscritique.com/Max_L_Ipsum/collection/wish/%s/all/all/all/all/all/all/gallery/page-" % media
urls = []

for i in xrange(last_page_index + 1):
    urls.append(base_url + str(i))

class SummarySpider(scrapy.Spider):
    name = "summaries"
    start_urls = urls

    def parse(self, response):
        shelf = response.css('ul.elsh-list').css('li.elsh-item')
        for item in shelf:
            href = item.css('a::attr(href)').extract_first()
            next_page = response.urljoin(href)
            yield scrapy.Request(next_page, self.parse_summary)

    def parse_summary(self, response):
        big_title = response.css('div.d-rubric-inner')[0]
        title = big_title.css('h1.pvi-product-title::text').extract_first()[8:-7]
        try:
            year = big_title.css('small.pvi-product-year::text').extract_first()[1:-1]
        except:
            year = ''
        try:
            artist = response.css('li.pvi-productDetails-item span')[1].css('span::text').extract_first()
        except:
            artist = ''

        yield {
            'title': title,
            'year': year,
            'artist': artist
        }

