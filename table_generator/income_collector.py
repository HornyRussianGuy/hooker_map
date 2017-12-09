#!/usr/bin/env python
# !/usr/bin/env python
import csv

median_income_by_country_code = {}

with open('ilc_di03.tsv') as tsv_file:
    tsv_reader = csv.reader(tsv_file, delimiter='\t')
    for row in tsv_reader:
        keys = row[0].split(',')
        if len(keys) >= 5:
            if keys[0] == 'TOTAL' and keys[1] == 'T' and keys[2] == 'MED_E' and keys[3] == 'EUR':
                country_code = keys[4]
                country_median_income = None
                for col in row[1:]:
                    try:
                        country_median_income = int(col)
                        break
                    except ValueError:
                        pass
                if country_median_income is not None:
                    median_income_by_country_code[country_code] = country_median_income
