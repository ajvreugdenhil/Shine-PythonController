from shineController import controller
import time
import datetime
import signal
import sys
import json
#allStations = ["B745C3", "A588E8", "308176", "30847E"]

# User requested modes
if len(sys.argv) > 1:
    shineProgramFile = sys.argv[1]
else:
    print("No arguments. Using default values")
    shineProgramFile = "./program.json"

program = {}
try:
    programfile = open(shineProgramFile, "r")
    program = json.load(programfile)
except:
    print("Problem with reading the file")
    sys.exit(1)

# Todo: check program contents?

broacastip = program["broadcastip"]
port = program["port"]
timetable = program["timetable"]

stations = []
for event in timetable:
    if event["id"] not in stations:
        stations.append(event["id"])

# Initial setup
colorChannels = ["r", "g", "b"]
foundStationIds = []
for station in controller.getStations(broacastip, port):
    foundStationIds.append(station["id"])
    if station["id"] not in stations:
        print("Rogue station will not be used: " + station["id"])

c = controller.controller(broacastip, port, stations)
c.setColorGlobal({"r": 0, "g": 0, "b": 0})

# Set up sigint behavior
def signal_handler(sig, frame):
    global c
    c.setColorGlobal({"r": 0, "g": 0, "b": 0})
    del c
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Faster to make new color object
def color(i):
    return {"r": i, "g": i, "b": i}


def main():
    print("Starting!")
    colors = [{"r": 0, "g": 0, "b": 0}, {"r": 254, "g": 0, "b": 0}, {"r": 0, "g": 254, "b": 0}, {"r": 0, "g": 0, "b": 254}]
    currentcolor = color(0)
    steps = 16
    print(time.time())
    time.sleep(1)
    print(time.time())

    while True:
        for stationID in stations:
            for i in range(0, len(colors)):
                for step in range(0, steps + 1):
                    for channel in colorChannels:
                        currentcolor[channel] = (int)(colors[i][channel] + ((colors[((i + 1) % len(colors))][channel] - colors[i][channel]) / steps) * step)

                    c.setColor(stationID, currentcolor)
                    time.sleep(0.004)



if __name__ == '__main__':
    main()
    del c