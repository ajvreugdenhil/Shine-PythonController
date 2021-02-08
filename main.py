#!/usr/bin/env python3
from shineController import devicemanager
import time
import datetime
import signal
import json
import time

import argparse
import math
import shutil
import numpy as np
import sounddevice as sd

dm = None
colorChannels = ["r", "g", "b"]

'''
device = 1

block_duration = 1
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
'''

def sigint_handler(sig, frame):
    global dm
    if dm is not None:
        dm.sendColorGlobal({"r": 0, "g": 0, "b": 0})
        dm.exit()
    exit(0)

signal.signal(signal.SIGINT, sigint_handler)


def main():
    settings = {}
    try:
        programfile = open("./settings.json", "r")
        settings = json.load(programfile)
    except:
        print("Problem with reading the file")
        exit(1)
    try:
        broadcastip = settings["broadcastip"]
        port = settings["port"]
        stationIDs = settings["stations"]
    except:
        print("Settings file invalid!")
        exit(1)


    global dm
    dm = devicemanager.deviceManager(broadcastip, port)
    dm.refreshDeviceList()
    time.sleep(1)
    print(dm.getDevices())

    while True:
        for i in range(0,3):
            dm.sendColorSpecific({"r": (i==0)*255, "g": (i==1)*255, "b": (i==2)*255}, '30847e')
            time.sleep(0.1)

    '''
    with sd.InputStream(device=device, channels=1, callback=audio_callback,
                        blocksize=int(blocksize),
                        samplerate=samplerate):
        while True:
            pass
    '''
def audio_callback(indata, frames, time, status):
        magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
        magnitude *= gain / fftsize
        volume = int(int(magnitude[16]) * int(magnitude[16]) / 2)
        #print(volume)
        if volume > 255:
            volume = 255
        c.setColorGlobal({"r": volume, "g": 0, "b": volume})


if __name__ == '__main__':
    main()
