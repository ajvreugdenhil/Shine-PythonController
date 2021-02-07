#!/usr/bin/env python3
from shineController import controller
import time
import datetime
import signal
import sys
import json
import time

import argparse
import math
import shutil
import numpy as np
import sounddevice as sd

c = None
colorChannels = ["r", "g", "b"]


device = 1

block_duration = 50
gain = 3200
low = 100
high = 2000
columns = 80
channel_amount = 1
test_freq = 4

device_dict = sd.query_devices()
samplerate = sd.query_devices(device, 'input')['default_samplerate']
print(device_dict)
print("#########")
print(sd.query_devices(device, 'input'))
print("#########")
delta_f = (high - low) / (columns - 1)
fftsize = math.ceil(samplerate / delta_f)
low_bin = math.floor(low / delta_f)


block_duration = 1
blocksize = samplerate * block_duration / 1000
blocksize = 1000


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
    foundStationIds = []
    for station in controller.getStations(broadcastip, port):
        foundStationIds.append(station["id"])
        if station["id"] not in stationIDs:
            print("Rogue station will not be used: " + station["id"])

    global c
    #c = controller.controller(broadcastip, port, stationIDs)
    c = controller.controller(broadcastip, port)
    c.setColorGlobal({"r": 0, "g": 0, "b": 50})

    pingpongval = 0
    cycletime = 500 #ms
    previoustime = time.time()*1000 #in ms
    while True:
        now = time.time()*1000
        if (now - cycletime > previoustime):
            previoustime = now

            pingpongval+= 1
            if pingpongval > 255:
                pingpongval = 0
            c.setColorGlobal({"r": 0, "g":0, "b":pingpongval})
            #print(pingpongval)
    
    #Debug stop

    with sd.InputStream(device=device, channels=1, callback=callback,
                        blocksize=int(blocksize),
                        samplerate=samplerate):
        while True:
            pass

def callback(indata, frames, time, status):
        magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
        magnitude *= gain / fftsize
        volume = int(magnitude[4])*10
        #print(volume)
        if volume > 255:
            volume = 255
        c.setColorGlobal({"r": volume, "g": 0, "b": volume})


if __name__ == '__main__':
    main()
