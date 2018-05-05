"""
Base class for Scrapy spiders
See documentation in docs/topics/spiders.rst
"""
import logging
import warnings

import scrapy
from scrapy import signals
from scrapy.http import Request
from scrapy.utils.trackref import object_ref
from scrapy.utils.url import url_is_from_spider
from scrapy.utils.deprecate import create_deprecated_class
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy.utils.deprecate import method_is_overridden


class ReviewspiderSpider(scrapy.Spider):
    name = 'reviewspider'
    allowed_domains = ['amazon.co.uk']

    def __init__(self, *args,  **kwargs):
        super(ReviewspiderSpider, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.get('start_url')]



    def parse(self, response):
        #raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))
        print(self.start_urls)
        review_body = response.xpath('//span[contains(@data-hook, "review-body")]/text()').extract()
        desc = response.xpath('//div[contains(@id, "feature-bullets-btf")]//li').extract()
        print("xxxxxxxxxxxxxxx")
        yield {
            # 'title'  :title,
            # 'rating' :rating,
            # 'helpful':helpful,
            'review_body':review_body,
            'desc': desc
        }
