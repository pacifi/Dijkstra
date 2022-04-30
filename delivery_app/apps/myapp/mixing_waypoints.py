from django.conf import settings
import requests
import json
import datetime
from humanfriendly import format_timespan

'''
Handles directions from Google
'''


def DirectionsWayPoint(*args, **kwargs):
    lat_a = kwargs.get("lat_a")
    long_a = kwargs.get("long_a")
    lat_b = kwargs.get("lat_b")
    long_b = kwargs.get("long_b")
    lat_c = kwargs.get("lat_c")
    long_c = kwargs.get("long_c")
    lat_d = kwargs.get("lat_d")
    long_d = kwargs.get("long_d")
    lat_e = kwargs.get("lat_e")
    long_e = kwargs.get("long_e")
    lat_f = kwargs.get("lat_f")
    long_f = kwargs.get("long_f")
    cantidad = kwargs.get("cantidad")

    origin = f'{lat_a},{long_a}'
    destination = f'{lat_b},{long_b}'

    if (cantidad == 3):
        waypoints = f'{lat_c},{long_c}'
    if (cantidad == 4):
        waypoints = f'{lat_c},{long_c}|{lat_d},{long_d}'
    if (cantidad == 5):
        waypoints = f'{lat_c},{long_c}|{lat_d},{long_d}|{lat_e},{long_e}'
    if (cantidad == 6):
        waypoints = f'{lat_c},{long_c}|{lat_d},{long_d}|{lat_e},{long_e}|{lat_f},{long_f}'
    result = requests.get(
        'https://maps.googleapis.com/maps/api/directions/json?',
        params={
            'origin': origin,
            'destination': destination,
            'waypoints': waypoints,
            "key": settings.GOOGLE_MAPS_API_KEY
        })

    directions = result.json()

    if directions["status"] == "OK":

        routes = directions["routes"][0]["legs"]

        distance = 0
        duration = 0
        route_list = []

        for route in range(len(routes)):
            distance += int(routes[route]["distance"]["value"])
            duration += int(routes[route]["duration"]["value"])

            route_step = {
                'origin': routes[route]["start_address"],
                'destination': routes[route]["end_address"],
                'distance': routes[route]["distance"]["text"],
                'duration': routes[route]["duration"]["text"],

                'steps': [
                    [
                        s["distance"]["text"],
                        s["duration"]["text"],
                        s["html_instructions"],

                    ]
                    for s in routes[route]["steps"]]
            }

            route_list.append(route_step)

    return {
        "origin": origin,
        "destination": destination,
        "distance": f"{round(distance / 1000, 2)} Km",
        "duration": format_timespan(duration),
        "route": route_list
    }
