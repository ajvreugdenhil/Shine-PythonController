from shineController import controller
import time
import datetime
import signal
import sys
import json

c = None

colorChannels = ["r", "g", "b"]

def sigint_handler(sig, frame):
    global c
    if c is not None:
        c.setColorGlobal({"r": 0, "g": 0, "b": 0})
        del c
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

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
