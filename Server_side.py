import socket

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Initalize server side to connect
ip = '192.168.0.62'
port = 9090
serverSocket.bind((ip,port))
serverSocket.listen()
print("Connect with server %s:%s",ip,port)

clientConnected = None
clientAddress = None

print("Initalize file")
from datetime import datetime
import time
time_run = datetime.today().strftime("%y-%m-%d_%H-%M-%S")
file_name = time_run + '.txt'


print("Waiting for client connect!!!")

while (True):
    (clientConnected, clientAddress) = serverSocket.accept()
    print("Wellcom form request %s:%s",clientAddress[0],clientAddress[1])

    if len(clientAddress) >= 2:
        break;

print("Start receive data from client")


while True:
    time.sleep(1)
    dataFromClient = clientConnected.recv(1024)
    value = dataFromClient.decode() 
    print(datetime.now(),value)