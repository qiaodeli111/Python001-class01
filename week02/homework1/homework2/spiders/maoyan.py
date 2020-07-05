import scrapy
import random
from scrapy.selector import Selector
from homework2.items import MovieItem
from fake_useragent import UserAgent


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        ua = UserAgent(verify_ssl=False)
        headers = {'user-agent': ua.random}
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse, headers=headers)

    def parse(self, response):
        movie_list_src = Selector(response=response).xpath('//div[@class="movie-hover-info"]')[:10]
        for m_src in movie_list_src:
            m = m_src.xpath('./div')
            item = MovieItem()
            item['title'] = m[0].xpath('./@title').extract_first().strip()
            item['movie_type'] = m[1].xpath('./text()').extract()[-1].strip()
            item['publish_date'] = m[3].xpath('./text()').extract()[-1].strip()
            print(item)
            yield item