import datetime
import scrapy


def get_url(date):
    return 'http://english.entgroup.cn/boxoffice/cn/daily/?date=' + str(date.month) + '%20/' + str(date.day) + '%20/' + str(date.year)

def get_title(s):
    start = s.rfind('  ') + 2
    return s[start:]

def get_num(s):
    end = s.rfind('\r')
    start = s.rfind(' ', 0, end) + 1
    return s[start:end]

class ENT_Spider(scrapy.Spider):
    name = "box_office_ch"
    weekday = 0
    date = None

    def start_requests(self):
        q = getattr(self, 'date', None)
        if q is not None:
            self.date = datetime.datetime(int(q[:4]), int(q[4:6]), int(q[6:8]))
        yield scrapy.Request(get_url(self.date), self.parse)

    def parse(self, response):
        titles = response.xpath('//strong/text()')
        nums = response.css('td')
        for i, title in enumerate(titles[1:]):
            yield {'title': get_title(title.extract()), 'num': get_num(nums[22+10*i].extract())}

        self.weekday += 1
        if self.weekday < 7:
            self.date += datetime.timedelta(days=1)
            yield response.follow(get_url(self.date), self.parse)
