# -*- coding: utf-8 -*-
import re
from typing import Generator, Union, Tuple
from urllib.parse import urlparse, ParseResult

import pycountry
from scrapy import Selector
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


def get_details(response: HtmlResponse) -> dict:
    r = {}

    for detail in response.xpath('//*'):  # type: Selector
        name = detail.xpath('.//span[@class="name"]//text()').extract_first(None)
        value = detail.xpath('.//span[@class="text"]//text()').extract()
        if name is not None:
            name = name.lower()
            name = re.sub(r'\W', '', name)
            r[name] = value

    return r


def get_rate_and_currency(s: str) -> Union[Tuple[int, str], type(None)]:
    match_curr = re.search(r'[A-Z]{3}', s)
    match_rate = re.search(r'\d+', s)
    if match_curr and match_rate:
        return int(match_rate.group(0)), match_curr.group(0).upper()


class EurogirlsescortSpider(CrawlSpider):
    name = 'eurogirlsescort'
    allowed_domains = ['eurogirlsescort.com']
    start_urls = ['http://eurogirlsescort.com/']

    rules = (
        Rule(LinkExtractor(allow=(
            r'escort/[^/]+/\d+',
        )), callback='parse_hooker_page'),
        Rule(LinkExtractor(allow=(
            r'escorts/', r'escort/'
        )))
    )

    @staticmethod
    def parse_country(response: HtmlResponse) -> Union[str, type(None)]:
        details = get_details(response)
        maybe_country_names = details.get('country', None)
        if maybe_country_names:
            maybe_country_name = maybe_country_names[0]
            try:
                country = pycountry.countries.lookup(maybe_country_name)
                if country:
                    return country.alpha_2
            except LookupError:
                pass

    @staticmethod
    def parse_id(response: HtmlResponse) -> str:
        url_parts: ParseResult = urlparse(response.url)
        path: str = url_parts.path
        return path.rstrip('/').split('/')[-1]

    @staticmethod
    def parse_rate(response: HtmlResponse) -> Union[Tuple[int, str], type(None)]:
        incall_rate_text = response.xpath('//div[@class="incall third"]//text()').extract_first(None)
        outcall_rate_text = response.xpath('//div[@class="outcall third"]//text()').extract_first(None)

        for text_rate in [incall_rate_text, outcall_rate_text]:
            if text_rate is not None:
                rate_and_currency = get_rate_and_currency(text_rate)
                if rate_and_currency is not None:
                    return rate_and_currency

    def parse_hooker_page(self, response: HtmlResponse) -> Generator[dict, None, None]:
        country_code = self.parse_country(response)
        rate_and_currency = self.parse_rate(response)
        if country_code and rate_and_currency:
            yield {
                '_id': '__'.join([self.parse_id(response), self.name]),
                'country_code': country_code,
                'rate': {
                    'value': rate_and_currency[0],
                    'currency': rate_and_currency[1],
                }
            }
