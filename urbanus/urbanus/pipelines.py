# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import re

import googlemaps

from urbanus.settings import GOOGLE_MAPS_KEY


class UrbanusPipeline(object):
    def process_item(self, item, spider):
        if spider.name == "urbania":
            gmaps = googlemaps.Client(key=GOOGLE_MAPS_KEY)

            if item['address']:
                updated_address = u'{0}, Lima, Peru'.format(item['address'])
            else:
                logging.log(logging.WARNING, "No address for url {0}".format(item['url']))

            geocoded_list = gmaps.geocode(updated_address)
            if geocoded_list:
                geocoded = geocoded_list[0]
                item['latitude'] = geocoded['geometry']['location']['lat']
                item['longitude'] = geocoded['geometry']['location']['lng']

            if item['description']:
                item['description'] = item['description'].strip()

            if item['price']:
                item['price'] = _convert_price_to_soles(item['price'])
            return item
        return item


def _convert_price_to_soles(price):
    price = price.replace(",", "")
    res = re.search("([0-9]+)", price)

    if res:
        if 'us$' in price.lower():
            price_soles = int(res.groups()[0]) * 3.2
        else:
            price_soles = int(res.groups()[0])
    else:
        price_soles = 0
    return price_soles
