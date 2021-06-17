import requests

URL="https://api.fda.gov/drug/label.json?search=drug_interactions:%s&limit=1"


cache = {}

_fetch_data = lambda drug: requests.get(URL.format(drug).lower()).json().get('results')[0]

def describe_drug(drug):
    if cache.get(drug): return cache.get(drug)
    cache[drug] = _fetch_data(drug)
    return cache.get(drug)

_get_field_for_drug = lambda drug: lambda field: describe_drug(drug).get(field)[0]

get_field_for_drug = lambda drug, field: _get_field_for_drug(drug)(field)



