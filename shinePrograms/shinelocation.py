import time
import math

import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

occlusionFactor = 0.12


def sendLocation(dm, devices, x, y, basecolor={'r': 255, 'g': 200, 'b': 200}):
    for device in devices:
        distance = abs(math.hypot(
            abs(y-device["y"]), abs(x-device["x"])))
        brightnessfactor = 1 - (distance * occlusionFactor)
        if brightnessfactor < 0:
            brightnessfactor = 0
        dm.sendColorSpecific(
            {
                'r': int(basecolor["r"]*brightnessfactor),
                'g': int(basecolor["g"]*brightnessfactor),
                'b': int(basecolor["b"]*brightnessfactor),
            },
            device['id'])


def main(dm, devices, refreshrate=100):
    waitTime = 1 / refreshrate
    color = {
        'r': 255,
        'g': 200,
        'b': 0
    }

    '''
    # Line
    resolution = 600
    while True:
        for y in range(0, resolution):
            y = y/(resolution/10)
            x = 0
            sendLocation(dm, devices, x, y, color)
            time.sleep(waitTime)

        for y in range(resolution, 0, -1):
            y = y/(resolution/10)
            x = 0
            sendLocation(dm, devices, x, y, color)
            time.sleep(waitTime)
    '''

    # Square
    squareSize = 10
    while True:
        x = 0
        y = 0
        for side in range(4):
            for i in range(squareSize):
                if side == 0:
                    x = 0
                    y = i
                if side == 1:
                    x = i
                    y = squareSize
                if side == 2:
                    x = squareSize
                    y = squareSize - i
                if side == 3:
                    x = squareSize - i
                    y = 0
                sendLocation(dm, devices, x, y, color)
                time.sleep(waitTime*10)
