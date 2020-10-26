import socket
import os 
import os.path
from os import listdir
from os.path import isfile, join
import time
import pickle
import sys

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        # Empezar a busscar conexiones
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(20)
        print(f"[*] Escuchando como {self.host}:{self.port}")

        if True:
            # Una vez que se encuentra una conexion disponible
            socketCliente, direccion = s.accept() 
            print(f"[+] Conexion con {direccion}")

            while True:
                rcvData = socketCliente.recv(1024)
                data_decompressed = pickle.loads(rcvData)

                if data_decompressed.count() == 3:
                    self.save_user(data_decompressed)
                elif data_decompressed.count() == 2:
                    self.validate_user(data_decompressed)

                print("Servidor: ", rcvData)
                socketCliente.send('Mensaje enviado.'.encode())

        else:
            print("Error de conexión. Cerrando aplicación...")
        
        socketCliente.close()
        s.close()

    def save_user(self, data):
        pass

    def validate_user(self, data):
        pass

if __name__ == "__main__":
    s = Server('localhost', 5001)