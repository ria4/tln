import re
import scrapy

base_url = "https://www.senscritique.com/liste/Cine_2017_sur_un_coin_de_table/1562107"

class SC_Spider(scrapy.Spider):
    name = "liste"
    start_urls = [base_url]
    summary_done = False
    current_page = 1

    def parse(self, response):
        if not self.summary_done:
            list_title = re.sub('\s+', ' ', response.css('h1.d-heading1::text').extract_first())
            list_desc = str.join('\n', response.css('div.d-grid')[2].css('p::text').extract())
            yield {'list_title': list_title, 'list_desc': list_desc}
            self.summary_done = True

        list_fragment = response.css('div.elli-content')
        for item in list_fragment:
            title = item.css('a.elco-anchor::text').extract_first()
            try:
                comment = str.join('\n', item.css('div.elli-annotation-content::text').extract())
            except:
                comment = ''
            yield {'title': title, 'comment': comment}

        try:
            if self.current_page > 11:
                raise Exception
            self.current_page += 1
            next_page = response.css('div.eipa-interface')[0].css('li.eipa-page')[min(self.current_page, 7)].css('a.eipa-anchor::attr(href)').extract_first()
            idx = next_page.rfind('-')
            next_page = next_page[:idx+1] + str(self.current_page)
        except:
            next_page = None
        if next_page is not None:
            yield response.follow(next_page, self.parse)

