import scrapy
import random
from scrapy.selector import Selector
from homework2.items import MovieItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        agent_list = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.%s (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.%s' % (v, v) for v in range(36)]
        cookie_str = 'uuid_n_v=v1; uuid=2CE50CA0B87E11EAAD7CEBC74F78E0F94ECA5236B6EC4B67973883C2E4F90193; _csrf=9ab4bc635c21bbaeb7a3b23fd286ba0a76137dd7f90bf8ecd84cce151a3de01e; mojo-uuid=5ff3b6503f3e0a9c032a1307389ee5c0; mojo-session-id={"id":"6878f48d7be9818cd10f401dbfa6ab6b","time":1593266266871}; _lxsdk_cuid=172f611e3f083-05918efc42347c-30760d58-12b178-172f611e3f1c8; _lxsdk=2CE50CA0B87E11EAAD7CEBC74F78E0F94ECA5236B6EC4B67973883C2E4F90193; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593266267; __mta=44356379.1593266267298.1593266267298.1593266267298.1; _lxsdk_s=172f611e3f2-c19-3cb-69a%7C%7C12; mojo-trace-id=9; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593268155'
        headers = {'user-agent': agent_list[random.randrange(36)], 'cookie': cookie_str}
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