import queue
import threading
import time
from socket import *

#self.sock = socket(AF_INET, SOCK_DGRAM)
#self.othersock = socket(AF_INET, SOCK_DGRAM)
#self.sock.settimeout(0.0000005)
##self.sock.bind(('192.168.137.1', 5000))
#self.sock.setsockopt(SOL_SOCKET, SO_SNDBUF, 0)
#self.sock.connect((ip, port))

class sender(threading.Thread):
    def __init__(self, brightness):
        threading.Thread.__init__(self)
        self.brightness = brightness

    def run(self):
        color = 2
        commandByte = 0b00100000.to_bytes(1, "little")
        colorByte = color.to_bytes(1, "little")
        brightnessbyte = self.brightness.to_bytes(1, "little")
        message = commandByte + colorByte + brightnessbyte
        socket(AF_INET, SOCK_DGRAM).sendto(message, MSG_DONTWAIT, ("192.168.4.255", 5000))


def main():
    for i in range(200):
        b = ((i%2)*255)
        s = sender(b)
        s.start()
        time.sleep(0.1)

if __name__ == "__main__":
    main()


'''
for i in range(100):
    color = 2
    brightness = (i%2) * 255
    
    start = time.time()
    #self.othersock.sendto(message, ("192.168.137.104", self.port))
    #self.sock.sendall(message)
    socket(AF_INET, SOCK_DGRAM).sendto(message, MSG_DONTWAIT, ("192.168.137.104", 5000))
    print((time.time()-start)*1000)
    time.sleep(0.01)
'''