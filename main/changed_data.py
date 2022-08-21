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
#     initial_data = process([
# { "type": "Feature", "properties": { "ADMIN": "Aruba", "ISO_A3": "ABW" }, "geometry": { "type": "Polygon", "coordinates": [ [ [ -69.996937628999916, 12.577582098000036 ], [ -69.936390753999945, 12.531724351000051 ], [ -69.924672003999945, 12.519232489000046 ], [ -69.915760870999918, 12.497015692000076 ], [ -69.880197719999842, 12.453558661000045 ], [ -69.876820441999939, 12.427394924000097 ], [ -69.888091600999928, 12.417669989000046 ], [ -69.908802863999938, 12.417792059000107 ], [ -69.930531378999888, 12.425970770000035 ], [ -69.945139126999919, 12.44037506700009 ], [ -69.924672003999945, 12.44037506700009 ], [ -69.924672003999945, 12.447211005000014 ], [ -69.958566860999923, 12.463202216000099 ], [ -70.027658657999922, 12.522935289000088 ], [ -70.048085089999887, 12.531154690000079 ], [ -70.058094855999883, 12.537176825000088 ], [ -70.062408006999874, 12.546820380000057 ], [ -70.060373501999948, 12.556952216000113 ], [ -70.051096157999893, 12.574042059000064 ], [ -70.048736131999931, 12.583726304000024 ], [ -70.052642381999931, 12.600002346000053 ], [ -70.059641079999921, 12.614243882000054 ], [ -70.061105923999975, 12.625392971000068 ], [ -70.048736131999931, 12.632147528000104 ], [ -70.00715084499987, 12.5855166690001 ], [ -69.996937628999916, 12.577582098000036 ] ] ] } }])
#     final_data = process([
# { "type": "Feature", "properties": { "ADMIN": "India", "ISO_A3": "IND" }, "geometry": { "type": "Polygon", "coordinates": [ [ [ -69.936390753999945, 12.531724351000051 ], [ -69.924672003999945, 12.519232489000046 ], [ -69.915760870999918, 12.497015692000076 ], [ -69.880197719999842, 12.453558661000045 ], [ -69.876820441999939, 12.427394924000097 ], [ -69.888091600999928, 12.417669989000046 ], [ -69.908802863999938, 12.417792059000107 ], [ -69.930531378999888, 12.425970770000035 ], [ -69.945139126999919, 12.44037506700009 ], [ -69.924672003999945, 12.44037506700009 ], [ -69.924672003999945, 12.447211005000014 ], [ -69.958566860999923, 12.463202216000099 ], [ -70.027658657999922, 12.522935289000088 ], [ -70.048085089999887, 12.531154690000079 ], [ -70.058094855999883, 12.537176825000088 ], [ -70.062408006999874, 12.546820380000057 ], [ -70.060373501999948, 12.556952216000113 ], [ -70.051096157999893, 12.574042059000064 ], [ -70.048736131999931, 12.583726304000024 ], [ -70.052642381999931, 12.600002346000053 ], [ -70.059641079999921, 12.614243882000054 ], [ -70.061105923999975, 12.625392971000068 ], [ -70.048736131999931, 12.632147528000104 ], [ -70.00715084499987, 12.5855166690001 ], [ -69.996937628999916, 12.577582098000036 ] ] ] } }])
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
