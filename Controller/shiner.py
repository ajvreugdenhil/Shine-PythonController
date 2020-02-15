import controller
import time
import signal
import sys

UDP_IP = "192.168.4.255"
UDP_PORT = 5000

#print(controller.getStations(UDP_IP, UDP_PORT))

allStations = ["B745C3", "A588E8", "308176", "30847E"]

order = ["30847E", "308176", "B745C3", "A588E8", "B745C3", "308176"]

simpleColors = {"r": 0, "g": 0, "b": 255}
colors = [{"r": 0, "g": 0, "b": 0},{"r": 0, "g": 0, "b": 255}]
c = controller.controller(UDP_IP, UDP_PORT, allStations)

def signal_handler(sig, frame):
    global c
    del c
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


while True:
    for stationID in order:
        c.setLightStationColor(stationID, {"r": 0, "g": 0, "b": 0})
        time.sleep(0.1)
        c.setLightStationColor(stationID, {"r": 254, "g": 254, "b": 254})
        time.sleep(0.1)
        c.setLightStationColor(stationID, {"r": 0, "g": 0, "b": 0})

del c
