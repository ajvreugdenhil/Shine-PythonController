#!/usr/bin/env python3
from shineController import devicemanager
from shinePrograms import thunder
from shinePrograms import shineambiance
from shinePrograms import shinelocation
import signal
import time
import datetime
import json

import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def init():
    settings = {}
    try:
        programfile = open("./settings.json", "r")
        settings = json.load(programfile)
    except:
        logger.error("Problem with reading the file")
        exit(1)
    try:
        broadcast_ip = settings["broadcastip"]
        port = settings["port"]
        stations = settings["stations"]
    except:
        logger.error("Settings file invalid!")
        exit(1)

    dm = devicemanager.deviceManager(broadcast_ip, port)
    dm.refreshDeviceList()
    time.sleep(3)
    logger.info(str(len(dm.getDevices())) + " Stations found")
    logger.debug(dm.getDevices())
    return (dm, stations)


def main(dm, stations):
    # directControl.main(dm)
    # thunder.main(dm)

    shineambiance.main(dm, 10)
    #shinelocation.main(dm, stations, 120)


if __name__ == '__main__':
    dm, stations = init()
    try:
        logger.info("Starting")
        main(dm, stations)
    except KeyboardInterrupt:
        logger.info("Stopping")
        time.sleep(1)
        dm.sendColorGlobal({'r': 0, 'g': 0, 'b': 0})
        time.sleep(0.1)
        dm.sendColorGlobal({'r': 0, 'g': 0, 'b': 0})
        time.sleep(0.1)
        dm.exit()
        logger.info("Stopped")
