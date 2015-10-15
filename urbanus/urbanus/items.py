# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from w3lib.html import remove_tags
from scrapy.loader.processors import Join, MapCompose, TakeFirst


class UrbanusItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    address = scrapy.Field()
    photos = scrapy.Field()
    bedrooms = scrapy.Field()
    area = scrapy.Field()
    bathrooms = scrapy.Field()
    garage = scrapy.Field()
    description = scrapy.Field()
    price_soles = scrapy.Field()
    price_dollars = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    url = scrapy.Field()
