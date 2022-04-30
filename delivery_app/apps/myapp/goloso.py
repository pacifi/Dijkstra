from django.conf import settings

from apps.myapp.punto import Punto


def goloso(data, lat_origen, long_origen):
    # Crenado array de coordenadas
    punto_list = []
    punto_goloso_list = []

    punto_inicial = Punto(lat=lat_origen, long=long_origen, distancia=0, referencia=0)
    # Data Oredenada a mi gusto
    punto_distancia_list = []
    punto_distancia_list_order = []
    punto_list.append(punto_inicial)
    # Seteado de das para trabajo inicial
    print("goloso")

    for pedido in data:
        punto = Punto(lat=pedido['fields']['geolocation'].split(',')[0],
                      long=pedido['fields']['geolocation'].split(',')[1],
                      distancia=pedido['fields']['distancia_numero'], referencia=pedido['pk'])
        punto_list.append(punto)

    print("list inicial")
    for p in punto_list:
        print("ref", p.referencia, ",", p.distancia)

    # Inicio Goloso

    while 0 < len(punto_list):
        punto_goloso_list.append(punto_list[0])
        punto_referencia = punto_list[0]

        del punto_list[0]
        cont = 0
        for punto in punto_list:
            distancia = calcular_distancia_map(punto_referencia.lat, punto_referencia.long, punto.lat, punto.long)
            punto_list[cont].distancia = distancia
            cont = cont + 1
        punto_list = burbuja(punto_list)
    distancia_oringen = calcular_distancia_map(
        lat_origin=punto_goloso_list[len(punto_goloso_list) - 1].lat,
        long_origen=punto_goloso_list[len(punto_goloso_list) - 1].long,
        lat_destino=punto_inicial.lat,
        long_destino=punto_inicial.long

    )
    punto_final = Punto(lat=punto_inicial.lat, long=punto_inicial.long,
                        distancia=distancia_oringen, referencia=0)
    punto_goloso_list.append(punto_final)
    return punto_goloso_list


import math


def calcular_distancia_coordenada(lat_origin, long_origen, lat_destino, long_destino):
    # print(lat_origin)
    # print(long_origen)
    # print(lat_destino)
    # print(long_destino)
    rad = math.pi / 180
    dlat = lat_destino - lat_origin
    dlon = long_destino - long_origen
    R = 6372.795477598
    a = (math.sin(rad * dlat / 2)) ** 2 + math.cos(rad * lat_origin) * math.cos(rad * lat_destino) * (
        math.sin(rad * dlon / 2)) ** 2
    distancia = 2 * R * math.asin(math.sqrt(a))
    return distancia
    # #


import requests


def calcular_distancia_map(lat_origin, long_origen, lat_destino, long_destino):
    origin = f'{lat_origin},{long_origen}'
    destination = f'{lat_destino},{long_destino}'

    result = requests.get(
        'https://maps.googleapis.com/maps/api/directions/json?',
        params={
            'origin': origin,
            'destination': destination,
            "key": settings.GOOGLE_MAPS_API_KEY
        })

    directions = result.json()
    distance = 0
    if directions["status"] == "OK":
        route = directions["routes"][0]["legs"][0]
        origin = route["start_address"]
        destination = route["end_address"]
        distance = route["distance"]["text"]
        duration = route["duration"]["text"]
    return float(distance.split()[0])


def burbuja(punto_list):
    intercambios = True
    numPasada = len(punto_list) - 1
    while numPasada > 0 and intercambios:
        intercambios = False
        for i in range(numPasada):
            if punto_list[i].distancia > punto_list[i + 1].distancia:
                intercambios = True
                temp = punto_list[i]
                punto_list[i] = punto_list[i + 1]
                punto_list[i + 1] = temp
        numPasada = numPasada - 1
    return punto_list
