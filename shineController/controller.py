import time
from shineController import devicemanager

class controller:
    def __init__(self, ip, port, stations):
        self.ip = ip
        self.port = port
        self.manager = devicemanager.deviceManager(ip, port)
        if (stations == None):
            self.stationAware = False
        else:
            self.stationAware = True
            self.stations = []
            self.validateStations(stations)

    def __del__(self):
        del self.manager
    
    def validateStations(self, orderedStationIds):
        self.manager.refreshDeviceList()
        devices = self.manager.getDevices()
        while len(devices) < len(orderedStationIds):
            devices = self.manager.getDevices()

        for stationId in orderedStationIds:
            if not any(device["id"] == stationId for device in devices):
                print("device not found: " + stationId)
                time.sleep(1)
                self.validateStations(orderedStationIds)
            else:
                for device in devices:
                    if device["id"] == stationId:
                        self.stations.append(device)

    def setColor(self, id, colorData):
        if not self.stationAware:
            print("This instance is not station aware.")
            return False
        ip = None
        for station in self.stations:
            if station["id"] == id:
                ip = station["ip"]
        if ip == None:
            print("Error! this station does not have an IP associated to it")
            return
        self.manager.sendColorCommand(ip, 1, colorData["r"])
        self.manager.sendColorCommand(ip, 2, colorData["g"])
        self.manager.sendColorCommand(ip, 3, colorData["b"])

    def setColorGlobal(self, colorData):
        self.manager.sendColorCommand(self.ip, 1, colorData["r"])
        self.manager.sendColorCommand(self.ip, 2, colorData["g"])
        self.manager.sendColorCommand(self.ip, 3, colorData["b"])


def getStations(ip, port):
    manager = devicemanager.deviceManager(ip, port)
    manager.refreshDeviceList()
    time.sleep(2)
    return manager.getDevices()