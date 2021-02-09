#!/usr/bin/env python3
from shineController import devicemanager
import signal

import time
import datetime
import json
import time

from shinePrograms import shineambiance


def init():
    settings = {}
    try:
        programfile = open("./settings.json", "r")
        settings = json.load(programfile)
    except:
        print("Problem with reading the file")
        exit(1)
    try:
        broadcast_ip = settings["broadcastip"]
        port = settings["port"]
        stationIDs = settings["stations"]
    except:
        print("Settings file invalid!")
        exit(1)

    dm = devicemanager.deviceManager(broadcast_ip, port)
    dm.refreshDeviceList()
    time.sleep(1)
    print(dm.getDevices())
    return dm


def main(dm):
    shineambiance.main(dm, dm.getDevices()[0]['id'], 600)


if __name__ == '__main__':
    dm = init()
    try:
        print("starting")
        main(dm)
    except KeyboardInterrupt:
        print("doei")
        time.sleep(0.01)
        dm.sendColorGlobal({'r': 0, 'g': 0, 'b': 0})
        dm.exit()
