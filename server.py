#!/bin/env python
from threading import Thread
from socket import * 

def accetta_richieste():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s si è collegato." % client_address)
        Thread(target=gestisce_client, args=(client,)).start()

def gestisce_client(client):
    message = client.recv(1024)
    try:
        print(message)
        filename = message.split()[1]
        # print('filename prima =', filename.decode())

        if "/" == filename.decode():
            filename = b'/index.html'
        print('filename dopo =', filename.decode())

        f = open(filename[1:],'rb') 
        outputdata = f.read()
        # print (outputdata) 
        print ("OK") 
        client.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        client.send(outputdata)
        client.send("\r\n".encode())
        client.close()

    except IOError:
        print("ERRORE")
        #Invia messaggio di risposta per file non trovato
        client.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n","UTF-8"))
        client.send(bytes("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n","UTF-8"))
        client.close()

HOST = 'localhost'
PORT = 8080
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = Thread(target=accetta_richieste)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()