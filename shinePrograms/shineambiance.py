import time
import math

channels = ['r', 'g', 'b']


def main(dm, refreshrate=100):
    waitTime = 1 / refreshrate
    r = 0
    g = 0
    b = 254
    state = 'r'
    while True:
        if state == 'r':
            r += 1
            b -= 1
            if r > 254:
                state = 'g'
        elif state == 'g':
            g += 1
            r -= 1
            if g > 254:
                state = 'b'
        elif state == 'b':
            b += 1
            g -= 1
            if b > 254:
                state = 'r'
        for station in dm.getDevices():
            dm.sendColorSpecific(
                {
                    'r': abs(r),
                    'g': abs(g),
                    'b': abs(b),
                },
                station['id'])
        time.sleep(waitTime)
