# -*- coding: utf-8 -*-
import scrapy


class EscortEuropeSpider(scrapy.Spider):
    name = 'escort-europe'
    allowed_domains = ['escort-europe.com']
    start_urls = ['http://escort-europe.com/']

    def parse(self, response):
        pass
