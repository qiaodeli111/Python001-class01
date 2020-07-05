# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class Homework2Pipeline:
    conn = None
    cur = None

    def open_spider(self, spider):
        print('Open spider......')
        
        self.conn = pymysql.connect(host = 'localhost',
            port = 3306,
            user = 'root',
            password = 'xxxxxxxxxx',
            db = 'geektime_python_train')
        
        self.cur = self.conn.cursor()
        self.cur.execute('select VERSION()')
        print(self.cur.fetchone())

    def process_item(self, item, spider):
        values = [(id,'testuser'+str(id)) for id in range(4, 21) ]
        sql_str = "INSERT INTO `week02_maoyan_movie` (`movie_name`, `movie_type`, `movie_showtime`) values(%s, %s, %s)"
        self.cur.execute(sql_str, (item['title'], item['movie_type'], item['publish_date']))


    def close_spider(self, spider):
        print('Closing spider......')
        self.conn.commit()
        self.cur.close()
        self.conn.close()