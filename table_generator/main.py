#!/usr/bin/env python
import pycountry
from tabulate import tabulate

from income_collector import median_income_by_country_code
from rates_collector import median_rates_by_country_code

GROUP_SIZE = 8

list_of_countries_by_hooker_index = []

for country_code in median_income_by_country_code:
    if country_code in median_rates_by_country_code:
        median_rate = median_rates_by_country_code[country_code]
        median_income = median_income_by_country_code[country_code]
        hooker_index = median_income / median_rate

        country_name = pycountry.countries.get(alpha_2=country_code).name

        list_of_countries_by_hooker_index.append((
            country_name, median_income, median_rate, hooker_index
        ))

list_of_countries_by_hooker_index.sort(key=lambda a: a[3])

for i in range(0, len(list_of_countries_by_hooker_index), GROUP_SIZE):
    sublist = list_of_countries_by_hooker_index[i: i + GROUP_SIZE]
    min_index = sublist[0][-1]
    max_index = sublist[-1][-1]
    print(tabulate(sublist, headers=[
        'Country', 'Median income per year', 'Median hooker rate per hour', 'Hooker Index ({} - {})'.format(
            int(round(min_index)), int(round(max_index)),
        )
    ]))
    print('\n')
