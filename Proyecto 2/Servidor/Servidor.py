import socket
import os 
import os.path
from os import listdir
from os.path import isfile, join
import time

class Server:
    def __init__(self, host, port):
        while True:
            self.host = host
            self.port = port

            # Empezar a busscar conexiones
            s = socket.socket()
            s.bind((self.host, self.port))
            print(f"[*] Escuchando como {self.host}:{self.port}")
            s.listen(20)

            # Una vez que se encuentra una conexion disponible
            socketCliente, direccion = s.accept() 
            print(f"[+] Conexion con {direccion}")

    def validate_user(self):
        pass

if __name__ == "__main__":
    s = Server('localhost', 5001)