import socket
import os 
import os.path
from os import listdir
from os.path import isfile, join
from encriptador import Encriptador
import select 
import sys, traceback
import threading

LISTA_SOCKETS = []
POR_MANDAR = []
ENVIADO_POR = {}

class SocketServidor(threading.Thread):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.bind(('',5001))
        self.sock.listen(50)

        LISTA_SOCKETS.append(self.sock)
        print("--Escuchando en el puerto 5001--")

    def iniciar(self):
        while True:
            leer, escribir, err = select.select(LISTA_SOCKETS,[],[],0)     
            for sock in leer:
                if sock == self.sock:                    
                    sockfd , addr = self.sock.accept()
                    print(str(addr))
                    LISTA_SOCKETS.append(sockfd)
                    print(LISTA_SOCKETS[len(LISTA_SOCKETS)-1])
                else:
                    try:
                        s = sock.recv(1024)
                        if s == '':
                            print(str(sock.getpeername()))                            
                            continue
                        else:
                            POR_MANDAR.append(s)
                            ENVIADO_POR[s]=(str(sock.getpeername()))
                    except:
                        print(str(sock.getpeername()))

class Conexiones(threading.Thread):

    def correr(self):        
        while True:
            leer, escribir, err = select.select(LISTA_SOCKETS,[],[],0)  
            for i in POR_MANDAR:
                for s in escribir:
                    print("Enviando a %s"%(str(s.getpeername())))
                    s.send(i)                                                 
                POR_MANDAR.remove(i)   
                del(ENVIADO_POR[i])  


if __name__ == "__main__":

    key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
    enc = Encriptador(key)
    s = SocketServidor()
    s.iniciar()
    print(f"Sockets: {LISTA_SOCKETS}")
    h = Conexiones()
    h.correr()


