#!/usr/bin/env python
import os

import numpy as np
from currency_converter import CurrencyConverter
from pymongo import MongoClient
from pymongo.collection import Collection

c = CurrencyConverter()

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = int(os.getenv('MONGO_PORT'))
MONGO_NAME = os.getenv('MONGO_NAME')

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_NAME]

hookers_collection: Collection = db.hookers

median_rates_by_country_code = {}

for country_code in hookers_collection.distinct('country_code'):
    euro_rates = []
    for hooker in hookers_collection.find({'country_code': country_code}):
        try:
            euro_rates.append(c.convert(
                hooker['rate']['value'],
                hooker['rate']['currency'],
                'EUR',
            ))
        except ValueError as e:
            pass

    median_rates_by_country_code[country_code] = np.median(euro_rates)
