# -*- coding: utf-8 -*-
from collections import namedtuple
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
        l.add_value('url', response.url)

        properties = extract_properties(response)
        l.add_value('bedrooms', properties.bedrooms)
        l.add_value('bathrooms', properties.bathrooms)
        l.add_value('area_total', properties.area_total)
        l.add_value('area_constructed', properties.area_constructed)
        l.add_value('garage', properties.garage)

        l.add_css('price', "span.inmueble_price")
        l.add_css('description', "div.show_detail")

        return l.load_item()


def extract_properties(response):
    Properties = namedtuple('Properties', ['bedrooms', 'area_total', 'area_constructed',
                            'bathrooms', 'garage'])
    bedrooms = ""
    area_total = ""
    area_constructed = ""
    bathrooms = ""
    garage = ""

    for sel in response.xpath("//div[3]/div[2]/div[1]/div[3]/div[2]/ul/li"):
        if sel.xpath("./span/text()").extract_first().lower() == 'dormitorios':
            bedrooms = sel.xpath("./p/text()").extract_first()
        elif sel.xpath("./span/text()").extract_first().lower() == u'baños':
            bathrooms = sel.xpath("./p/text()").extract_first()
        elif sel.xpath("./span/text()").extract_first().lower() == u'área total':
            area_total = sel.xpath("./p/text()").extract_first()
        elif sel.xpath("./span/text()").extract_first().lower() == u'área construida':
            area_constructed = sel.xpath("./p/text()").extract_first()
        elif sel.xpath("./span/text()").extract_first().lower() == 'cochera':
            garage = sel.xpath("./p/text()").extract_first()
    return Properties(bedrooms, area_total, area_constructed, bathrooms, garage)
