import time
import math

channels = ['r', 'g', 'b']


def main(dm, refreshrate=100):
    waitTime = 1 / refreshrate
    freq = 0.3
    while True:
        for i in range(31):
            for station in dm.getDevices():
                dm.sendColorSpecific(
                    {
                        'r': int(math.sin(freq*i + 0) * 127 + 128),
                        'g': int(math.sin(freq*i + math.tau/3) * 127 + 128),
                        'b': int(math.sin(freq*i + 2*math.tau/3) * 127 + 128),
                    },
                    station['id'])
                time.sleep(waitTime)
