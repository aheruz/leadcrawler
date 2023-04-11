import json

from pathlib import Path
import re

from scrapy import Spider, Request
from scrapy_playwright.page import PageMethod

from playwright.async_api import Response as PlaywrightResponse, BrowserContext, Request as PlaywrightRequest

class LinkedinXhrSpider(Spider):
    """Scroll down on an infinite-scroll page."""

    name = "linkedinxhr"

    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "DOWNLOAD_HANDLERS": {
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            # "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
    }

    def start_requests(self):
        yield Request(
            url="https://www.linkedin.com/sales/search/people?_ntb=AuB8SON5Q3ulLQka2WArew%3D%3D&savedSearchId=50520427&sessionId=OY%2FmOIrJQXKLnjJ418sTjA%3D%3D",
            meta={
                "playwright": True,
                "playwright_include_page":True,
                'playwright_context': 'new',
                "playwright_context_kwargs": {
                    "storage_state": {
                        "cookies": [
                            {
                                'name': 'li_at',
                                'value': 'AQEDARqhW18D9KYaAAABhufTJrcAAAGHeMgM104AGegezxPpAvP--59isAnuODzdJcsRQ8BtwZMqSHTxiUtTrcGbvgMCs0matY0csw7aRcP9GbTO4RnLp5K0B3d3i1iSd2Zm7SWJB3udBmeBHwt83Pgx',
                                'domain': '.www.linkedin.com',
                                'path': '/',
                            }
                        ]
                    }
                },
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "#search-results-container > div > ol")
                ],
                "playwright_page_event_handlers": {
                    "response": self.handle_response,
                },
                "playwright_page": self.init_page,
                'errback': self.errback,
            },
        )

    async def init_page(self, page, request):
        jl_file = "init_page.json"
        data = {"world":"hello"}
        with open(jl_file, mode='a') as writer:
            json.dump(data, writer)
        await page.route("*", lambda route: route.abort())
    
    async def handle_route(self, route):
        jl_file = "handle_route.json"
        data = {route}
        with open(jl_file, mode='a') as writer:
            json.dump(data, writer)
        route.abort()

    async def handle_response(self, response: PlaywrightResponse) -> None:
        jl_file = "handle_response.json"
        data = {response.request.resource_type:[response.request.url]}
        with open(jl_file, mode='a') as writer:
            json.dump(data, writer)

    def parse(self, response):
        return {"url": response.url}

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()