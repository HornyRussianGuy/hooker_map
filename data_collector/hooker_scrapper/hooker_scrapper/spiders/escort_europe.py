# -*- coding: utf-8 -*-
import re
from typing import Generator, Union, Tuple

import pycountry
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule


def get_tables(response: HtmlResponse) -> dict:
    r = {}
    for tr in response.xpath('//table//tr'):  # type: Selector
        ths_tds_texts = tr.xpath('./*[self::th or self::td]//text()').extract()
        if len(ths_tds_texts) > 1:
            key: str = ths_tds_texts[0]
            key = key.lower()
            key = re.sub(r'\W+', '', key)
            r[key] = ths_tds_texts[1:]
    return r


def get_rate_and_currency(l: list) -> Union[Tuple[int, str], type(None)]:
    for s in l:  # type: str
        match_curr = re.search(r'[A-Z]{3}', s)
        match_rate = re.search(r'\d+', s)
        if match_curr and match_rate:
            return int(match_rate.group(0)), match_curr.group(0).upper()


class EscortEuropeSpider(CrawlSpider):
    name = 'escort-europe'
    allowed_domains = ['escort-europe.com']
    start_urls = ['https://escort-europe.com/SiteDirectory']

    rules = (
        Rule(LinkExtractor(allow=(
            r'escort-\w+/[^/]+/\w+',
        )), callback='parse_hooker_page'),
        Rule(LinkExtractor(allow=(
            r'escort-\w+',
        )))
    )

    @staticmethod
    def parse_country(response: HtmlResponse) -> Union[str, type(None)]:
        tables = get_tables(response)
        maybe_country_names = tables.get('country', None)
        if maybe_country_names:
            maybe_country_name = maybe_country_names[0]
            try:
                country = pycountry.countries.lookup(maybe_country_name)
                if country:
                    return country.alpha_2
            except LookupError:
                pass

    @staticmethod
    def parse_rate(response: HtmlResponse) -> Union[Tuple[int, str], type(None)]:
        maybe_rates = get_tables(response).get('1sthour', None)
        if maybe_rates is None:
            return None
        return get_rate_and_currency(maybe_rates)

    @staticmethod
    def parse_id(response: HtmlResponse) -> str:
        return response.url.rstrip('/').split('/')[-1]

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
