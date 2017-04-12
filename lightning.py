#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import requests
import json
import time
from datetime import datetime

latHome = xx.xxxx
lngHome = xx.xxxx
distanceRange = 15  # in km
jsonUrl = "http://www.onweerdetectie.com/domoticz_bo.json"

server = "http://localhost"
port = 8080
deviceIdx = "1"


def distance(lat1, lng1, lat2, lng2):
    radius = 6371

    dLat = (lat2 - lat1) * math.pi / 180
    dLng = (lng2 - lng1) * math.pi / 180

    lat1 = lat1 * math.pi / 180
    lat2 = lat2 * math.pi / 180

    val = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLng / 2) * \
        math.sin(dLng / 2) * math.cos(lat1) * math.cos(lat2)
    ang = 2 * math.atan2(math.sqrt(val), math.sqrt(1 - val))
    return radius * ang

last = 0
while True:
    z = requests.get(jsonUrl)
    data = json.loads(z.content)
    value = 0
    ignored = 0
    for pos in data:
        time_, lat, lng = pos
        distanceBetween = distance(latHome, lngHome, lat, lng)
        if (distanceBetween <= distanceRange):
            if (time_ > last):
                value += 1
            else:
                ignored += 1

    last = time_

    print ("%d strikes found -- %s" % (value, datetime.strftime(datetime.now(), "%c")))
    print ("%d old strikes ignored -- %s" % (ignored, datetime.strftime(datetime.now(), "%c")))
    requests.get(
        "%s:%d/json.htm?type=command&param=udevice&idx=%s&svalue=%d" %
        (server, port, deviceIdx, value))

    time.sleep(120)  # wacht 120 seconden
