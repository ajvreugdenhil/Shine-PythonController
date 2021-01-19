from shineController import controller
import time
import datetime
import signal
import sys
import json

c = None

def sigint_handler(sig, frame):
    global c
    if c is not None:
        c.setColorGlobal({"r": 0, "g": 0, "b": 0})
        del c
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

colorChannels = ["r", "g", "b"]

'''
class Station:
    def __init__(self, id, colorstates, repeat):
        self.repeat = repeat
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
            next = self.colorstates[0]

        return [previous, next]

    def getState(self, steps):
        if self.repeat:
            steps = steps % self.colorstates[-1]["step"]
        result = color(0)
        for channel in colorChannels:
            previous, next = self.getRelevantStates(steps)
            if next is None:
                result[channel] = previous[channel]
                continue
            stepDifference = next["step"] - previous["step"]
            stepsBetweenPreviousAndNext = steps - previous["step"]
            if stepsBetweenPreviousAndNext < 0:
                stepsBetweenPreviousAndNext = -2 * stepsBetweenPreviousAndNext
            result[channel] = (int)((previous[channel] + ((next[channel] - previous[channel]) / stepDifference) * (stepsBetweenPreviousAndNext)) % 255)
        return result

    def __repr__(self):
        return "ID: " + self.id + " number of states: " + str(len(self.colorstates))
'''


def getTime(object):
    return object["event"]["time"]

def main():
    if len(sys.argv) > 1:
        settings_file = sys.argv[1]
    else:
        print("No arguments. Using default settings file")
        settings_file = "./settings.json"
    settings = {}
    try:
        programfile = open(settings_file, "r")
        settings = json.load(programfile)
    except:
        print("Problem with reading the file")
        sys.exit(1)
    try:
        broacastip = settings["broadcastip"]
        port = settings["port"]
        stationIDs = settings["stations"]
    except:
        print("Settings file invalid!")
        sys.exit(1)

    # Initial setup
    foundStationIds = []
    for station in controller.getStations(broacastip, port):
        foundStationIds.append(station["id"])
        if station["id"] not in stationIDs:
            print("Rogue station will not be used: " + station["id"])

    global c
    #c = controller.controller(broacastip, port, stationIDs)
    c = controller.controller(broacastip, port)
    c.setColorGlobal({"r": 0, "g": 0, "b": 0})

    while True:
        c.setColorGlobal({"r": 10, "g": 99, "b": 50})
        time.sleep(2)

if __name__ == '__main__':
    main()
