import socket
import threading


class Server():
    def __init__(self, player,run=True):
        if run:
            self.player = player
            self.connected = True
            self.alive = True
            self.newPlayer = False
            self.newPowerup = False
            self.newMinion = False
            self.receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.receiver.bind((socket.gethostname(),65432))
            self.sender = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.serverThread = threading.Thread(target=self.readMsg)
            self.serverThread.start()
    
    def parse(self,msg):
        if msg == "init":
            self.sendMsg("confirm")
        if msg == "appClosed":
            self.connected = False
        if msg[0] == 'p':
            self.powerup = msg[2:]
            self.newPowerup = True
        if msg[0] == 'n':
            print("NFC: " + msg[2:])
            self.playerType = msg[2:]
            self.newPlayer = True
        if msg[0] == 'm':
            self.minionType = msg[2:]
            self.newMinion = True

    def readMsg(self):
        while(self.alive):
            try:
                bytesAddressPair = self.receiver.recvfrom(1024)
                self.msg = bytesAddressPair[0].decode('utf-8')
                self.sendTo = bytesAddressPair[1]
                self.parse(self.msg)
            except:
                pass

    def sendMsg(self,msg):
        try:
            self.sender.sendto(msg.encode(),(self.sendTo[0], 65433))
        except:
            pass

    def checkConnection(self):
        return self.connected
    
    def endServer(self):
        try:
            self.sendMsg("closedGame")
            self.alive = False
            self.sender.sendto("server killed".encode(),(socket.gethostname(), 65432))
        except:
            pass
