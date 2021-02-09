import time


def main(dm, station, refreshrate=100):
    waitTime = 1/refreshrate
    while True:
        for i in range(0, 3):
            for j in range(255):
                dm.sendColorSpecific(
                    {"r": (i == 0)*j, "g": (i == 1)*j, "b": (i == 2)*j}, station)
                time.sleep(waitTime)
            for j in range(255, 0, -1):
                dm.sendColorSpecific(
                    {"r": (i == 0)*j, "g": (i == 1)*j, "b": (i == 2)*j}, station)
                time.sleep(waitTime)
