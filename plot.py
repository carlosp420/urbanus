# -*- coding: utf-8 -*-
"""Parse scrapped data and plot results in a map"""

import sys

import pandas


__author__ = 'carlosp420'


def main():
    if len(sys.argv) < 2:
        print("Error, enter json data file as argument.")
        sys.exit(1)

    filename = sys.argv[1].strip()

    data = pandas.read_json(filename)

    apartments = data[data.price <= 1800].sort('price')
    print(apartments[['title', 'price', 'address', 'url']].head(10))


if __name__ == '__main__':
    main()
