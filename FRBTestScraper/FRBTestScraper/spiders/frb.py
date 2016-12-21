"""
This is simple script for crawling data from 'www.federalreserve.gov'
and writing it into JSON format
"""
# -*- coding: utf-8 -*-

from time import gmtime, strftime
import scrapy

BASE_URL = 'https://www.federalreserve.gov/releases/h10/hist/'
TABLE_XPATH = './/table[@class="statistics"]/tr'
C_XPATH = './th/a[contains(@href, "dat")]/{}'
F_URI = '../results/scraped_result_{}.{}'
FEED_FORMAT = 'csv'


class FrbSpider(scrapy.Spider):

    name = 'frb'
    start_urls = (BASE_URL,)

    custom_settings = {
        'FEED_FORMAT': FEED_FORMAT,
        'FEED_URI': F_URI.format(
            strftime("%Y-%m-%d %H:%M:%S", gmtime()), FEED_FORMAT.lower()),
    }

    def parse(self, response):
        """
        Parsing table with countries
        @url https://www.federalreserve.gov/releases/h10/hist/
        """

        for country in response.xpath(TABLE_XPATH):
            country_name = country.xpath(C_XPATH.format('text()')).extract_first().strip()
            url = BASE_URL + country.xpath(C_XPATH.format('@href')).extract_first()
            request = scrapy.Request(url, callback=self._parse_rates)
            request.meta['country'] = country_name

            yield request

    @staticmethod
    def _parse_rates(response):
        """
        Parsing table with date and rate for a country
        @url https://www.federalreserve.gov/releases/h10/hist/
        @is_in_title 'Foreign Exchange Rates'
        """

        country = response.meta['country']
        for rate in response.xpath(TABLE_XPATH):
            rate_date = rate.xpath('.//th/text()').extract_first().strip()
            rate_value = rate.xpath('.//td/text()').extract_first().strip()
            yield {
                'Country': country,
                'Date': rate_date,
                'Rate': rate_value
            }
