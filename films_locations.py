import folium
import requests
import json
import urllib.parse
import math


def calculate_distance(locations):
    lat1, lon1 = locations[0]
    lat2, lon2 = locations[1]
    # lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    radius = 6371  # km
 
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
 
    return d

def get_locations(file, start):
    with open(file, 'rb') as f:
        films_locations = {}
        for _ in range(14):
            f.readline()
        for line in f.readlines():
            try:
                info = line.decode('utf-8').split('\t')
                location = info[-1]
                if info[-1].startswith('('):
                    location = info[-2]
                if info[0] not in films_locations.keys():
                    films_locations[info[0]] = []
                films_locations[info[0]].append(location.strip())
            except UnicodeDecodeError:
                pass
    return films_locations


def get_coordinates(address):
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

    try:
        response = requests.get(url).json()[0]
        print([float(response['lat']), float(response['lon'])])
        return [float(response['lat']), float(response['lon'])]
    except (IndexError, json.decoder.JSONDecodeError):
        return [0, 0]


# def sort_by_distance(locations):
#     pass

def generate_map(start_location, file):
    locations = get_locations(file, start_location)
    # sorted_locations = sort_by_distance(locations)
    map = folium.Map(tiles="Stamen Terrain",
                location=start_location,
                zoom_control=3)
    fg = folium.FeatureGroup(name="Films map")
    number = 0
    for _, element in enumerate(locations.keys()):
        if number >= 20:
            break
        for location in locations[element]:
            coordinates = get_coordinates(location)
            if coordinates != [0, 0] and calculate_distance([start_location, coordinates]) <= 2000:
                fg.add_child(folium.Marker(location=[coordinates[0], coordinates[1]],
                                    popup=element,
                                    icon=folium.Icon()))
                number += 1
    map.add_child(fg)
    map.save("Map.html")


generate_map([34.0536909, -118.242766], 'locations.list')