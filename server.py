from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import sys
import threading

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a server socket
host = "127.0.0.1"
port = 8080

serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

serverSocket.bind((host, port))
serverSocket.listen()
while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message: str = connectionSocket.recv(1024).decode()
        filename: str = message.split()[1]
        
        f = open(filename[1:])

        filedata = f.read()
        #Send one HTTP header line into socket
        responseCode = "HTTP/1.1 200 OK\r\n"
        contentType = "Content-Type: text/html\r\n\r\n"
        outputdata = responseCode + contentType + filedata
        
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        
        f.close()
        connectionSocket.close()
    except IOError:
        #Send response message for file not found        
        outputdata = "HTTP/1.1 404 Not Found\r\n"
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        
        connectionSocket.close()
serverSocket.close()
sys.exit()
