# -*- coding: utf-8 -*-
import scrapy


class EurogirlsescortSpider(scrapy.Spider):
    name = 'eurogirlsescort'
    allowed_domains = ['eurogirlsescort.com']
    start_urls = ['http://eurogirlsescort.com/']

    def parse(self, response):
        pass
