import socket
import threading


class Server():
    def __init__(self):
        self.host = socket.gethostname()
        self.listenPort = 65432
        self.sendPort = 65433
        self.read = True
        self.currData = ""
        self.listenerThread = threading.Thread(target=self.connect)
        self.listenerThread.start()

    def connect(self):
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver.bind((self.host, self.listenPort))
        self.receiver.listen()
        self.recvConn, self.addr = self.receiver.accept()
        self.recvConn.recv(1024)

        if self.recvConn.getpeername()[0] != self.recvConn.getsockname()[0]:
            print("Connected to: " + self.addr[0])
            self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sender.connect((self.addr[0], self.sendPort))
            self.recvConn.setblocking(False)
            self.readThread = threading.Thread(target=self.getMsg)
            self.readThread.start()

    def getMsg(self):
        while (self.read):
            try:
                data = self.recvConn.recv(1024)
                data = data[3:].decode('utf-8')
                self.currData = data
            except:
                pass

    def getCurrData(self):
        return self.currData

    def writeMsg(self, msg):
        try:
            self.sender.send(len(msg).to_bytes(2, 'big') + msg.encode('utf-8'))
        except:
            return

    def endServer(self):
        self.read = False
        if self.listenerThread.is_alive():
            socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM).connect((self.host, self.listenPort))
            self.receiver.close()
