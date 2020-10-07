#!/usr/bin/env python

from math import sin, cos, atan2, radians
import asyncio
import websockets
import requests
import json


def distance_earth_coo(lat1, lon1, lat2, lon2) -> float:
    earthRadiusKm = 6371

    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)

    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(d_lat / 2) * sin(d_lat / 2) + sin(d_lon / 2) * sin(d_lon / 2) * cos(lat1) * cos(lat2)
    c = 2 * atan2(a ** 0.5, (1 - a) * 0.5)
    return earthRadiusKm * c


async def recv(websocket: websockets.WebSocketServerProtocol, path: str):
    async for message in websocket:
        print("recv", message)
        coo_data = json.loads(message)
        coo = {
            'lon1': coo_data['X'],
            'lat1': coo_data['Y'],
        }
        resp = json.loads(requests.get('http://127.0.0.1:8080/position').text)
        # resp = [{'latitude': 1.0, 'longitude': 1.0, 'id': 0}]

        data = [{
            'name': food['id'],
            'distance': distance_earth_coo(lon2=food['longitude'], lat2=food['latitude'], **coo),
            'coordinates': {
                'X': food['longitude'],
                'Y': food['latitude'],
            }
        } for food in resp]

        data.sort(key=lambda x: x['distance'])

        await websocket.send(json.dumps({
            'coo': coo_data,
            'data': data[:10]
        }))


asyncio.get_event_loop().run_until_complete(websockets.serve(recv, 'localhost', 5050))
print("Start on localhost:5050")
asyncio.get_event_loop().run_forever()
