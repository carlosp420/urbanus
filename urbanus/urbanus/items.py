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
    address = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    photos = scrapy.Field()
    bedrooms = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    area_total = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    area_constructed = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    bathrooms = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    garage = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    url = scrapy.Field(
        output_processor=TakeFirst(),
    )
