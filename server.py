#!/bin/env python
from threading import Thread
from socket import * 
import sys, signal
def accetta_richieste():
    while True:
        client, client_address = server.accept()
        print("%s:%s si è collegato." % client_address)
        Thread(target=gestisce_client, args=(client,)).start()

def gestisce_client(client):
    message = client.recv(1024)
    try:
        filename = message.split()[1]

        if "/" == filename.decode():
            filename = b'/index.html'

        f = open(filename[1:],'rb') 
        outputdata = f.read()
        client.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        client.send(outputdata)
        client.send("\r\n".encode())
        client.close()

    except IOError:
        #Invia messaggio di risposta per file non trovato
        client.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n","UTF-8"))
        client.send(bytes("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n","UTF-8"))
        client.close()
        
def signal_handler(signal, frame):
    print( 'Sto uscendo dal server (Ctrl+C premuto)')
    try:
      if( server ):
        server.server_close()
    finally:
      sys.exit(0)

#interrompe l’esecuzione se da tastiera arriva la sequenza (CTRL + C) 
signal.signal(signal.SIGINT, signal_handler)
HOST = input("Inserire l'indirizzo dove hostare il server: ")
if HOST == "":
   HOST = 'localhost'

PORT = input("Inserire la porta: ")
if PORT == "":
   PORT = 8080

BUFSIZ = 1024
ADDR = (HOST, int(PORT))

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(ADDR)

if __name__ == "__main__":
    server.listen(5)
    print("Madagascar Web Server in esecuzione")
    print("In attesa di connessioni...")
    accept_thread = Thread(target=accetta_richieste)
    accept_thread.start()
    accept_thread.join()
    server.close()