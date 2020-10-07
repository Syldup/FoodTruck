#!/usr/bin/env python

from math import sin, cos, atan2, radians
import asyncio
import websockets
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


async def echo(websocket: websockets.WebSocketServerProtocol, path: str):
    async for message in websocket:
        dist = distance_earth_coo(**json.loads(message))
        await websocket.send(dist)


asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8765))
asyncio.get_event_loop().run_forever()
