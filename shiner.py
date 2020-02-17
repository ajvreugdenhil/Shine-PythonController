from shineController import controller
import time
import datetime
import signal
import sys
import json
#allStations = ["B745C3", "A588E8", "308176", "30847E"]


colorChannels = ["r", "g", "b"]
def color(i):
    return {"r": i, "g": i, "b": i}

class Station:
    def __init__(self, id, colorstates):
        self.id = id
        self.colorstates = colorstates # has "step"; "r" "g" and "b"

    def getRelevantStates(self, steps):
        i = 0
        # FIXME
        try:
            while ((self.colorstates[i]["step"] < steps)):
                i += 1
        except:
            pass

        previous = {}
        next = {}
        # FIXME
        try:
            previous = self.colorstates[i - 1]
            next = self.colorstates[i]
        except:
            previous = self.colorstates[-1]
            next = None

        return [previous, next]

    def getState(self, steps):
        result = color(0)
        for channel in colorChannels:
            previous, next = self.getRelevantStates(steps)
            if next is None:
                result[channel] = previous[channel]
                continue
            stepDifference = next["step"] - previous["step"]
            stepsBetweenPreviousAndNext = steps - previous["step"]
            if stepsBetweenPreviousAndNext < 0:
                stepsBetweenPreviousAndNext = 0
            result[channel] = (int)((previous[channel] + ((next[channel] - previous[channel]) / stepDifference) * (stepsBetweenPreviousAndNext)) % 255)
        return result

    def __repr__(self):
        return "ID: " + self.id + " number of states: " + str(len(self.colorstates))



# Set up sigint behavior
def signal_handler(sig, frame):
    global c
    c.setColorGlobal({"r": 0, "g": 0, "b": 0})
    del c
    sys.exit(0)


def getTime(object):
    return object["event"]["time"]


signal.signal(signal.SIGINT, signal_handler)

# Get the program
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

# TODO: check program contents?
broacastip = program["broadcastip"]
port = program["port"]
programStations = program["stations"]

# Get all the station ids in the program
stationIDs = []
for station in programStations:
    if station["id"] not in stationIDs:
        stationIDs.append(station["id"])
print(stationIDs)

# Initial setup
foundStationIds = []
for station in controller.getStations(broacastip, port):
    foundStationIds.append(station["id"])
    if station["id"] not in stationIDs:
        print("Rogue station will not be used: " + station["id"])

c = controller.controller(broacastip, port, stationIDs)
c.setColorGlobal({"r": 0, "g": 0, "b": 0})

stations = []

def Tick(currentStep):
    global c
    for station in stations:
        c.setColor(station.id, station.getState(currentStep))
        #print(station.getState(currentStep))

def main():
    for station in programStations:
        id = station["id"]
        colorstates = []
        for event in station["timetable"]:
            # One step every millisecond in this case:
            step = event["time"] * 1000 
            r = event["r"]
            g = event["g"]
            b = event["b"]
            colorstates.append({"step": step, "r":r, "g":g, "b":b})
        stations.append(Station(id, colorstates))

    print(stations)

    currentStep = 0

    while True:
        # Measure time
        Tick(currentStep)
        currentStep += 10
        time.sleep(0.01)
        # Measure time
        # if the time is too long, error out

if __name__ == '__main__':
    main()
    del c



'''
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
'''