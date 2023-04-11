# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser

class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    allowed_domains = ['www.linkedin.com']
    start_urls = [
        'https://www.linkedin.com/sales/search/people?_ntb=AuB8SON5Q3ulLQka2WArew%3D%3D&savedSearchId=50520427&sessionId=OY%2FmOIrJQXKLnjJ418sTjA%3D%3D',
    ]

    # set cookies for linkedin
    # set headers required for linkedin
    # hide robot detection
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                cookies=[
                    {
                        'name': 'li_at',
                        'value': 'AQEDARqhW18D9KYaAAABhufTJrcAAAGHeMgM104AGegezxPpAvP--59isAnuODzdJcsRQ8BtwZMqSHTxiUtTrcGbvgMCs0matY0csw7aRcP9GbTO4RnLp5K0B3d3i1iSd2Zm7SWJB3udBmeBHwt83Pgx',
                        'domain': '.www.linkedin.com',
                        'path': '/',
                    }
                ],
                headers= 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15'
            )

    def parse(self, response):
        # yield text from css class eah-product-lockup__text
        yield {'text' : response.xpath('//*[@id="ember7"]/div/div/span/text()').extract_first()}