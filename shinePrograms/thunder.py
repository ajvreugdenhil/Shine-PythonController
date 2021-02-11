import time
import random


def on(dm):
    for station in dm.getDevices():
        dm.sendColorSpecific(
            {"r": 100, "g": 255, "b": 200}, station['id'])


def off(dm):
    for station in dm.getDevices():
        dm.sendColorSpecific(
            {"r": 0, "g": 0, "b": 0}, station['id'])


def main(dm):
    while True:
        time.sleep(random.randint(20, 60))
        for i in range(random.randint(0, 4)):
            on(dm)
            time.sleep(random.randint(20, 100)/1000)
            off(dm)
            time.sleep(random.randint(20, 200)/1000)
