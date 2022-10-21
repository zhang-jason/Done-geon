import socket
import threading


class Server():
    def __init__(self):
        self.alive = True
        self.receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.receiver.bind((socket.gethostname(),65432))
        self.sender = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.serverThread = threading.Thread(target=self.readMsg)
        self.serverThread.start()

    def readMsg(self):
        while(self.alive):
            try:
                bytesAddressPair = self.receiver.recvfrom(1024)
                self.msg = bytesAddressPair[0].decode('utf-8')
                self.sendTo = bytesAddressPair[1]
                print(self.msg)
                if self.msg == "init":
                    self.sendMsg("confirm")
            except:
                pass

    def sendMsg(self,msg):
        try:
            self.sender.sendto(msg.encode(),(self.sendTo[0], 65433))
        except Exception as e:
            print(e)
    
    def endServer(self):
        self.sendMsg("closedGame")
        self.alive = False
        self.sender.sendto("server killed".encode(),(socket.gethostname(), 65432))
