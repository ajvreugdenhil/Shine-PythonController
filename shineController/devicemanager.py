import queue
import threading
import time
from socket import *

import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class deviceManager:
    def __init__(self, broadcast_ip, port):
        self.broadcast_ip = broadcast_ip
        self.port = port
        self.queueLock = threading.Lock()
        self.deviceQueue = queue.Queue(0)
        self.thread = registrationReceiverThread(
            self.deviceQueue, port, self.queueLock)
        self.thread.start()
        self.devices = []
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    def exit(self):
        self.thread.exit()

    def refreshDeviceList(self):
        self.requestRegistration()
        self.updateDeviceList()

    def updateDeviceList(self):
        self.queueLock.acquire()
        while not self.deviceQueue.empty():
            self.devices.append(self.deviceQueue.get())
        self.queueLock.release()

    def getDevices(self):
        self.updateDeviceList()
        return self.devices

    def requestRegistration(self):
        commandByte = 0b01100000.to_bytes(1, "little")
        self.sock.sendto(commandByte, (self.broadcast_ip, self.port))

    def sendRawColorCommand(self, ip, color, brightness):
        commandByte = 0b00100000.to_bytes(1, "little")
        # r=1 g=2 b=3
        colorByte = color.to_bytes(1, "little")
        brightnessbyte = brightness.to_bytes(1, "little")
        message = commandByte + colorByte + brightnessbyte
        self.sock.sendto(message, (ip, self.port))

    def sendColorGlobal(self, colorObject):
        self.sendRawColorCommand(self.broadcast_ip, 1, colorObject["r"])
        self.sendRawColorCommand(self.broadcast_ip, 2, colorObject["g"])
        self.sendRawColorCommand(self.broadcast_ip, 3, colorObject["b"])

    def sendColorSpecific(self, colorObject, id):
        ip = None
        for device in self.devices:
            if device['id'].lower() == id.lower():
                ip = device['ip']
                break
        if ip == None:
            logger.error("ERROR: no such ID: " + id)
            return

        self.sendRawColorCommand(ip, 1, colorObject["r"])
        self.sendRawColorCommand(ip, 2, colorObject["g"])
        self.sendRawColorCommand(ip, 3, colorObject["b"])


class registrationReceiverThread (threading.Thread):
    def __init__(self, q, port, queueLock):
        threading.Thread.__init__(self)
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)
        self.serverSocket.bind(('', port))
        self.q = q
        self.queueLock = queueLock
        self.running = False

    def run(self):
        self.running = True
        while (self.running):
            message = None
            address = None
            try:
                message, address = self.serverSocket.recvfrom(1024)
            except:
                logger.error("An unexpected error occurred while receiving data")
                continue
            if (len(message) <= 0):
                continue
            if (message[0] != 0b01000000):
                continue
            device_ip = address[0]
            device_id = message[1:7].decode("utf-8")
            device = {"ip": device_ip, "id": device_id.lower()}
            self.queueLock.acquire()
            self.q.put(device)
            self.queueLock.release()

    def exit(self):
        self.running = False
        # TODO: fix this try except mess
        try:
            self.serverSocket.shutdown(SHUT_RDWR)
        except:
            pass
        self.serverSocket.close()
