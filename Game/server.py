import socket
import threading

class Server():
    def __init__(self):
        self.host = socket.gethostname()
        self.listenPort = 65432
        self.sendPort = 65433
        self.currData = ""
        x = threading.Thread(target=self.connect)
        x.start()

    def connect(self):
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver.bind((self.host, self.listenPort))
        self.receiver.listen()
        self.recvConn, self.addr = self.receiver.accept()
        self.recvConn.recv(1024)
        print("Connection from: " + self.addr[0])

        self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sender.connect((self.addr[0], self.sendPort))



    def getMsg(self):
        try:
            data = self.recvConn.recv(1024)
            data = data[3:].decode('utf-8')
            self.currData = data
        except:
           return

    def checkIn(self):
        x = threading.Thread(target=self.getMsg)
        x.start()

    def getCurrData(self):
        return self.currData

    def writeMsg(self,msg):
        try:
            self.sender.send(len(msg).to_bytes(2, 'big') + msg.encode('utf-8'))
        except:
            return
