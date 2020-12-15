import threading
import requests
import json
from queue import Queue
import logging
logging.basicConfig(level=logging.DEBUG)

class CrawlThread(threading.Thread):
    def __init__(self, name, city_queue:Queue):
        self.name = name
        self.city_queue = city_queue
    
    def run(self):
        while True:
            if self.city_queue.empty():
                break

def gen_url_queue(cities:list, pages):
    url_queue = Queue(100)
    for city in cities:
        for page in pages:
            url_queue.put(f'https://www.lagou.com/{city}-zhaopin/Python/{page}/')
    return url_queue


if __name__ == '__main__':
    cities = ['beijing', 'shanghai', 'guangzhou', 'shenzhen']
    url_queue = gen_url_queue(cities, range(1, 15))

    