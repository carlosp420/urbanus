# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.loader import ItemLoader

from urbanus.items import UrbanusItem


class UrbaniaSpider(scrapy.Spider):
    name = "urbania"
    allowed_domains = ["urbania.pe"]

    def start_requests(self):
        url = 'http://urbania.pe/alquiler-de-departamentos-en-peru'
        return [scrapy.Request(url, callback=self.extract_pagination)]

    def extract_pagination(self, response):
        pages = []
        for i in response.xpath("//div[contains(@class, 'paginator')]/ul//li"):
            page_url = i.xpath("./a/@href").extract_first()
            if page_url != "#":
                res = re.search("([0-9]+)$", page_url)
                if res:
                    pages.append(res.groups()[0])

        last_page = pages[-1]
        for i in range(1, int(last_page)):
            url = "http://urbania.pe/alquiler-de-departamentos-en-peru?pag={0}".format(i)
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        for i in response.xpath("//li[contains(@class, 'col_result tarjetas')]"):
            item_url = i.xpath("./a/@href").extract_first()
            url = "http://urbania.pe/{0}".format(item_url)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        l = ItemLoader(item=UrbanusItem(), response=response)
        l.add_xpath('title', "//section[1]/div/div[2]/div[1]/h1")
        l.add_xpath('address', "//section[2]/div/div/p")
        l.add_xpath('photos', "//div[contains(@class, 'slide_gale')]/span/img/@src")
        # properties "//div[3]/div[2]/div[1]/div[3]/div[2]/ul/li/
        return l.load_item()
