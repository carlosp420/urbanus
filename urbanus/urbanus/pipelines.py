# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

import googlemaps
from scrapy.exceptions import DropItem

from urbanus.settings import GOOGLE_MAPS_KEY
from urbanus.models import db_connect


class UrbanusPipeline(object):
    def process_item(self, item, spider):
        if spider.name == "urbania":
            gmaps = googlemaps.Client(key=GOOGLE_MAPS_KEY)

            if 'address' in item:
                updated_address = u'{0}, Lima, Peru'.format(item['address'])

                if _is_geocode_in_db(item['address']):
                    item['latitude'], item['longitude'] = _get_geocoding(item['address'])
                else:
                    geocoded_list = gmaps.geocode(updated_address)
                    if geocoded_list:
                        geocoded = geocoded_list[0]
                        item['latitude'] = geocoded['geometry']['location']['lat']
                        item['longitude'] = geocoded['geometry']['location']['lng']
                        _save_geocoding(item['address'], item['latitude'], item['longitude'])

                if item['description']:
                    item['description'] = item['description'].strip()

                if item['price']:
                    item['price'] = _convert_price_to_soles(item['price'])

                if 'area_constructed' in item:
                    item['area_constructed'] = _remove_meters(item['area_constructed'])
                return item
            else:
                raise DropItem("Not address given")

        return item


def _is_geocode_in_db(address):
    db = db_connect()
    table = db['geocoding']
    row = table.find_one(address=address)
    if row:
        return True
    else:
        return False


def _get_geocoding(address):
    db = db_connect()
    table = db['geocoding']
    row = table.find_one(address=address)
    if row:
        return row['lat'], row['long']


def _save_geocoding(address, lat, long):
    db = db_connect()
    table = db['geocoding']
    row = table.find_one(address=address)
    if not row:
        table.insert({'address': address, 'lat': lat, 'long': long})


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


def _remove_meters(area):
    if 'm' in area.lower():
        res = re.search('([0-9]+)', area)
        if res:
            return res.groups()[0]
    return None