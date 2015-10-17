# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
import re

import googlemaps
from scrapy.exceptions import DropItem

from urbanus.settings import GOOGLE_MAPS_KEY
from urbanus.settings import BASE_DIR
from urbanus.models import db_connect


class UrbanusPipeline(object):
    def __init__(self):
        self.gmaps = googlemaps.Client(key=GOOGLE_MAPS_KEY)
        with open(os.path.join(BASE_DIR, '..', '..', 'metro_stations.json'), "r") as handle:
            self.stations = json.loads(handle.read())

    def process_item(self, item, spider):
        if spider.name == "urbania":
            if 'address' in item:
                lat, long = self._do_geocoding(item)
                item['latitude'] = lat
                item['longitude'] = long

                # item['distance_to_metro'] = self._get_distance_to_metro(item)

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

    def _do_geocoding(self, item):
        updated_address = u'{0}, Lima, Peru'.format(item['address'])
        if _is_geocode_in_db(item['address']):
            return _get_geocoding(item['address'])
        else:
            geocoded_list = self.gmaps.geocode(updated_address)
            if geocoded_list:
                geocoded = geocoded_list[0]
                _save_geocoding(item['address'], item['latitude'], item['longitude'])
                lat = geocoded['geometry']['location']['lat']
                long = geocoded['geometry']['location']['lng']
                return lat, long

    def _get_distance_to_metro(self, item):
        distances = []
        for station in self.stations:
            orig = '{0},{1}'.format(item['latitude'], item['longitude'])
            dest = '{0},{1}'.format(station['lat'], station['long'])
            directions = self.gmaps.directions(orig, dest, mode='walking')

            if directions:
                for direction in directions:
                    legs = direction['legs']
                    for leg in legs:
                        distance = leg['distance']['value']
                        distances.append(distance)
        if distances:
            shortest_distance = sorted(distances)[0]
        else:
            shortest_distance = 99999999
        return shortest_distance



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