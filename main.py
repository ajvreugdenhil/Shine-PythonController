#!/usr/bin/env python3
from shineController import devicemanager
import time
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
    settings = {}
    try:
        programfile = open("./settings.json", "r")
        settings = json.load(programfile)
    except:
        print("Problem with reading the file")
        sys.exit(1)
    try:
        broadcastip = settings["broadcastip"]
        port = settings["port"]
        stationIDs = settings["stations"]
    except:
        print("Settings file invalid!")
        sys.exit(1)

    # Initial setup
    '''
    foundStationIds = []
    for station in controller.getStations(broadcastip, port):
        foundStationIds.append(station["id"])
        if station["id"] not in stationIDs:
            print("Rogue station will not be used: " + station["id"])
    '''
    global c
    #c = controller.controller(broadcastip, port, stationIDs)
    #c = controller.controller(broadcastip, port)
    #c.setColorGlobal({"r": 0, "g": 0, "b": 50})
    m = devicemanager.deviceManager("ESP_B745C3.wlan", port)

    pingpongval = 0
    cycletime = 150 #ms
    previoustime = time.time()*1000 #in ms
    while True:
        now = time.time()*1000
        if (now - cycletime > previoustime):
            previoustime = now

            pingpongval += 255
            if pingpongval > 255:
                pingpongval = 0
            
            #c.setColorGlobal({"r": 0, "g":0, "b":pingpongval})
            m.sendColorCommand("ESP_B745C3.wlan", 3, pingpongval)
            
            #print(pingpongval)

if __name__ == '__main__':
    main()
