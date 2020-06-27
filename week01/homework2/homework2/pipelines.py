# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Homework2Pipeline:
    def process_item(self, item, spider):
        with open('movies.csv', 'a', encoding='utf-8') as m:
            m.writelines('%s,%s,%s\n' % (item['title'], item['movie_type'], item['publish_date']))
        return item
