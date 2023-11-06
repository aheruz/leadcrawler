from pathlib import Path
import re

from scrapy import Spider, Request
from scrapy_playwright.page import PageMethod


class LinkedinSalesSpider(Spider):
    """Scroll down on an infinite-scroll page."""

    name = "linkedinsales"

    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "DOWNLOAD_HANDLERS": {
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            # "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT": 25,
    }

    start_url = "https://www.linkedin.com/sales/search/people?lastViewedAt=1681218411357&savedSearchId=50524794"

    start_page = 13

    cookies = [
        {
            'name': 'li_at',
            'value': 'AQEDARqhW18BCzqPAAABiEfjGvkAAAGIa--e-U0Akp81h6y0wuhDux7drUHi00433s5nFwEgpGjNim482tC5J6GajJe4JrgOgdNDT7YkVudXJaFFXQQ3s7_I6qP-WyITFMhTzohkJ9zonzI4am3eZItk',
            'domain': '.www.linkedin.com',
            'path': '/',
        }
    ]


    def start_requests(self):
        yield self.request(self.start_page)

    async def parse(self, response):
        page = re.search(r'(?<=&page\=)(\d+)', response.url)
        page = page.group() if page else 1
        # check button dont have class disabled
        next_page = bool(response.xpath('.//*[@data-search-pagination-type="overflow"]/button[@aria-label="Next"][not(contains(@class, "artdeco-button--disabled"))]'))
        for li in response.xpath('//*[@id="search-results-container"]/div/ol/li'):
            lead = li.xpath('.//*[@data-x-search-result="LEAD"]/div')

            company = lead.xpath('.//*[@data-anonymize="company-name"]/text()').extract_first()
            company = company if company else lead.xpath('div[1]/div/div[2]/div[2]/text()[normalize-space() != ""]').extract_first()
            about = lead.xpath('div[2]/dl/div/dd/div/span[2]/text()[normalize-space() != ""]').extract_first()
            company_linkedin_url = li.xpath('.//*[@data-control-name="view_company_via_profile_lockup"][contains(@href,"sales/company")]/@href').get()
            company_linkedin_url = 'https://www.linkedin.com' + company_linkedin_url if company_linkedin_url else ''
            linkedin_url = 'https://www.linkedin.com' + li.xpath('.//*[@data-control-name="view_lead_panel_via_search_lead_name"][contains(@href,"sales/lead")]/@href').get()

            yield {
                'name' : lead.xpath('.//*[@data-anonymize="person-name"]/text()').extract_first(),
                'page' : page,
                'title' : lead.xpath('.//*[@data-anonymize="title"]/text()').extract_first(),
                'company_name' : str(company).strip(),
                'location' : lead.xpath('.//*[@data-anonymize="location"]/text()').extract_first(),
                'about' : str(about).strip(),
                'linkedin_url' : self.normalize_linkedin_url(linkedin_url),
                'company_linkedin_url' : self.normalize_linkedin_url(company_linkedin_url),
            }
        if next_page:
            yield self.request(int(page) + 1)

    def request(self, page):
        return Request(
            url=self.start_url + '&page=' + str(page),
            meta={
                "playwright": True,
                "playwright_include_page":True,
                'playwright_context': 'CTX_SNS_' + str(page),
                "playwright_context_kwargs": {
                    "storage_state": {
                        "cookies": self.cookies
                    }
                },
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "#search-results-container > div > ol"),
                    PageMethod("evaluate", "document.getElementById('search-results-container').scrollTop += document.getElementById('search-results-container').clientHeight"),
                    PageMethod("wait_for_load_state", "domcontentloaded"),

                    PageMethod("evaluate", "document.getElementById('search-results-container').scrollTop += document.getElementById('search-results-container').clientHeight"),
                    PageMethod("wait_for_load_state", "domcontentloaded"),
                
                    PageMethod("evaluate", "document.getElementById('search-results-container').scrollTop += document.getElementById('search-results-container').clientHeight"),
                    PageMethod("wait_for_load_state", "domcontentloaded"),

                    PageMethod("evaluate", "document.getElementById('search-results-container').scrollTop += document.getElementById('search-results-container').clientHeight"),
                    PageMethod("wait_for_load_state", "domcontentloaded"),

                    PageMethod("evaluate", "document.getElementById('search-results-container').scrollTop += document.getElementById('search-results-container').clientHeight"),
                    PageMethod("wait_for_load_state", "domcontentloaded"),

                    PageMethod("evaluate", "document.getElementById('search-results-container').scrollTop += document.getElementById('search-results-container').clientHeight"),
                    PageMethod("wait_for_load_state", "domcontentloaded"),

                    PageMethod("evaluate", "document.getElementById('search-results-container').scrollTop += document.getElementById('search-results-container').clientHeight"),
                    PageMethod("wait_for_load_state", "domcontentloaded"),
                    PageMethod("evaluate", "document.querySelectorAll('#search-results-container > div > ol > li > div > div > div.flex.justify-space-between.full-width > div.flex.flex-column > div.ml8.pl1 > dl > div > dd > div > span:nth-child(2) > button').forEach((button) => button.click())"),
                    PageMethod("wait_for_load_state", "domcontentloaded"),
                ],
            },
        )

    def normalize_linkedin_url(self, url):
        return url.split("?")[0]