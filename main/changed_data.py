import re, os, json, requests
from deepdiff import DeepDiff


def process(data):
    processed_data = {}
    for d in data:
        key = d['properties']['ADMIN']
        processed_data[key] = d
    return processed_data


def get_data():
    initial_data = {}
    if os.path.exists('countries.geojson'):
        f = open('countries.geojson')
        if f:
            initial_data = process(json.load(f)['features'])
    url = 'https://datahub.io/core/geo-countries/r/countries.geojson'
    r = requests.get(url, allow_redirects=True)
    final_data = process(json.loads(r.content)['features'])
    open('countries.geojson', 'wb').write(r.content)
    return initial_data, final_data

def extract_name(key):
    return re.search("\'.+?\'", key).group(0)[1:-1]

def provide_changed_data():
    print('Started processing changed data')
    changed_data = {
        'added_or_updated': {},
        'deleted': []
    }
    initial_data, final_data = get_data()
    difference = DeepDiff(initial_data, final_data)
    dictionary_item_added = difference.get('dictionary_item_added')
    if dictionary_item_added:
        for item in dictionary_item_added:
            name = extract_name(item)
            changed_data['added_or_updated'][name] = final_data[name]

    values_changed = difference.get('values_changed')
    if values_changed:
        for item in values_changed:
            name = extract_name(item)
            changed_data['added_or_updated'][name] = final_data[name]
    dictionary_item_removed = difference.get('dictionary_item_removed')
    if dictionary_item_removed:
        for item in dictionary_item_removed:
            name = extract_name(item)
            changed_data['deleted'].append(name)

    return changed_data
