# -*- coding: utf-8 -*-
import scrapy


class HappyescortsSpider(scrapy.Spider):
    name = 'happyescorts'
    allowed_domains = ['happyescorts.com']
    start_urls = ['http://happyescorts.com/']

    def parse(self, response):
        pass
