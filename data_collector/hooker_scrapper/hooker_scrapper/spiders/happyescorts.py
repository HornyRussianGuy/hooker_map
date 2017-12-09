# -*- coding: utf-8 -*-
import re
from typing import Generator, Union, Tuple
from urllib.parse import ParseResult, urlparse

import pycountry
from scrapy import Selector
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class HappyescortsSpider(CrawlSpider):
    name = 'happyescorts'
    allowed_domains = ['happyescorts.com']
    start_urls = ['http://happyescorts.com/']

    rules = (
        Rule(LinkExtractor(allow=(
            r'escorts/',
        )), callback='parse_hooker_page'),
    )

    @staticmethod
    def parse_country(response: HtmlResponse) -> Union[str, type(None)]:
        url_parts: ParseResult = urlparse(response.url)
        path: str = url_parts.path
        path_parts = path.strip('/').split('/')
        if len(path_parts) >= 2:
            maybe_country_name = path.strip('/').split('/')[1]
            try:
                country = pycountry.countries.lookup(maybe_country_name)
                if country:
                    return country.alpha_2
            except LookupError:
                pass

    @staticmethod
    def parse_rate(response: HtmlResponse) -> Union[Tuple[int, str], type(None)]:
        for desc in response.css('div.details div.escortData div.description'):  # type: Selector
            for text in desc.xpath('.//text()').extract():
                text = text.replace('US$', 'USD')
                text = re.sub(r'\W', '', text)
                match_rate = re.search(r'(\d+)([A-Z]{3})perhour', text)
                if match_rate:
                    return int(match_rate.group(1)), match_rate.group(2)

    @staticmethod
    def parse_id(response: HtmlResponse) -> Union[str, type(None)]:
        return response.xpath('//@data-escort').extract_first(None)

    def parse_hooker_page(self, response: HtmlResponse) -> Generator[dict, None, None]:
        country_code = self.parse_country(response)
        rate_and_currency = self.parse_rate(response)
        hooker_id = self.parse_id(response)

        if hooker_id and country_code and rate_and_currency:
            yield {
                '_id': '__'.join([hooker_id, self.name]),
                'country_code': country_code,
                'rate': {
                    'value': rate_and_currency[0],
                    'currency': rate_and_currency[1],
                }
            }
