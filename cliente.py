import socket
import json
import pickle

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9998

class Client:
    def __init__(self):
        self.sock = None
        self.ip = "127.0.0.1"
        self.port = 9992

        print("CLIENTE CRIADO")

    def closeSocket(self):
        try:
            self.sock.close()
        except:
            pass

    def createSocketTCP(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_STREAM)  # TCP

    def run(self):
        op = 1

        self.createSocketTCP()
        self.connect()
        '''
        while op != 0:
            op = self.getService()

            print("Menu")

            for i in range(len(self.serviceList)):
                print(i+1, "- ", self.serviceList[i])

            print("0 - Sair")

            op = int(input("Selecione o serviço: "))

            while op < 0 or op > len(self.serviceList):
                op = int(input("Serviço invalido, digite novamente: "))

            self.selectService(op)
        '''

    def connect(self):
        self.sock.connect((SERVER_IP, SERVER_PORT))

        #print("\nConectado\n")

        msg = "getServices"

        while msg != "exit":
            # Request
            self.sendTCP(self.prepareMsg(msg))

            # Reply
            msg = self.loadMessage(self.sock.recv(1024))
            if msg != "exit":
                msg = input(msg)
            else:
                print("SAIU")

        print("\n")

    def convertJson(self, message):
        try:
            msg = json.dumps(message)
            return msg
        except:
            return message

    def loadJson(self, message):
        try:
            msg = json.loads(message)
            return msg
        except:
            return message

    def loadMessage(self, message):
        return self.loadJson(pickle.loads(message))

    def prepareMsg(self, msg):
        jsonMsg = self.convertJson(msg)

        serializedMsg = pickle.dumps(jsonMsg)

        return serializedMsg

    def sendTCP(self, serializedMsg):
        self.sock.send(serializedMsg)

cliente = Client()
cliente.run()