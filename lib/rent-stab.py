#!/usr/bin/env python3
"""
Retrives information about tax bills for a given bbl
"""
import datetime
import json
import sys
from pathlib import Path

if len(sys.argv) == 1:
    raise Exception("Missing argument, BBL")

BBL = sys.argv[1]


def read_json(path):
    with open(path, 'r') as f:
        return json.loads(f.read())


def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d")


tax_bills = read_json(str(Path.home().joinpath('.nyc-data', 'dof', BBL, 'tax_bills.json')))

years = sorted(map(str, list(set([parse_date(x['date']).year for x in tax_bills]))))

is_rent_stabilized = len([ x for x in tax_bills if x['rentStabilized'] ]) > 0

unit_counts = {}

for year in years:
    unit_counts_for_year = [x['unitCount'] for x in tax_bills if x['rentStabilized'] and x['date'][0:4] == year]
    if len(unit_counts_for_year) > 0:
        unit_count = max(unit_counts_for_year)
    else:
        unit_count = 0
    unit_counts[year] = unit_count


rent_stab_info = {
    "bbl": BBL,
    "rentStabilized": is_rent_stabilized,
    "unitCounts": unit_counts,
    "taxBills": tax_bills
}

print(json.dumps(rent_stab_info))
