from shineController import controller
import time
import signal
import sys

UDP_IP = "192.168.4.255"
UDP_PORT = 5000
colorChannels = ["r", "g", "b"]

allStations = ["B745C3", "A588E8", "308176", "30847E"]
someStations = ["A588E8", "30847E"]


foundStationIds = []

for station in controller.getStations(UDP_IP, UDP_PORT):
    foundStationIds.append(station["id"])
    print(station["id"])

c = controller.controller(UDP_IP, UDP_PORT, foundStationIds)
c.setColorGlobal({"r": 0, "g": 0, "b": 0})

def signal_handler(sig, frame):
    global c
    c.setColorGlobal({"r": 0, "g": 0, "b": 0})
    del c
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def color(i):
    return {"r": i, "g": i, "b": i}



colors = [{"r": 0, "g": 0, "b": 0}, {"r": 254, "g": 0, "b": 0}, {"r": 0, "g": 254, "b": 0}, {"r": 0, "g": 0, "b": 254}]
currentcolor = color(0)
steps = 16

while True:
    for stationID in foundStationIds:
        for i in range(0, len(colors)):
            for step in range(0, steps + 1):
                for channel in colorChannels:
                    currentcolor[channel] = (int)(colors[i][channel] + ((colors[((i + 1) % len(colors))][channel] - colors[i][channel]) / steps) * step)

                c.setColor(stationID, currentcolor)
                time.sleep(0.04)

del c
