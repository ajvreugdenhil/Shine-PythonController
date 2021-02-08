import queue
import threading
import time
from socket import *

import os

class deviceManager:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.queueLock = threading.Lock()
        self.deviceQueue = queue.Queue(0)
        #self.thread = registrationReceiverThread(self.deviceQueue, port, self.queueLock)
        #self.thread.start()
        self.devices = []
        self.sock = socket(AF_INET, SOCK_DGRAM)
        #self.othersock = socket(AF_INET, SOCK_DGRAM)
        #self.sock.settimeout(0.0000005)
        ##self.sock.bind(('192.168.137.1', 5000))
        #self.sock.setsockopt(SOL_SOCKET, SO_SNDBUF, 0)
        self.sock.connect((ip, port))
        

    def __del__(self):
        pass
        #self.thread.exit()

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
        self.sock.sendto(commandByte, (self.ip, self.port))
        
    def sendColorCommand(self, ip, color, brightness):
        commandByte = 0b00100000.to_bytes(1, "little")
        colorByte = color.to_bytes(1, "little")
        brightnessbyte = brightness.to_bytes(1, "little")
        message = commandByte + colorByte + brightnessbyte
        start = time.time()
        #self.othersock.sendto(message, ("192.168.137.104", self.port))
        self.sock.sendall(message)
        #socket(AF_INET, SOCK_DGRAM).sendto(message, MSG_DONTWAIT, (ip, self.port))
        print((time.time()-start)*1000)


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
            receiveData(self.serverSocket, self.q, self.queueLock)

    def exit(self):
        self.running = False
        # TODO: fix this try except mess
        try:
            self.serverSocket.shutdown(SHUT_RDWR)
        except:
            pass
        self.serverSocket.close()


def receiveData(socket, q, queueLock):
    message = None
    address = None
    try:
        message, address = socket.recvfrom(1024)
    except:
        print("An error occurred while receiving data")
        return
    if (len(message) <= 0):
        return
    if (message[0] != 0b01000000):
        return
    device_ip = address[0]
    device_id = message[1:7].decode("utf-8") 
    device = {"ip": device_ip, "id": device_id}
    queueLock.acquire()
    q.put(device)
    queueLock.release()
    