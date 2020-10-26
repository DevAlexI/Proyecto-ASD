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

                if len(data_decompressed) == 3:
                    self.save_user(data_decompressed, socketCliente)
                elif len(data_decompressed) == 2:
                    self.validate_user(data_decompressed, socketCliente)

        else:
            print("Error de conexión. Cerrando aplicación...")
        
        socketCliente.close()
        s.close()

    def save_user(self, data, cliente):
        print('Recibí 3 madriolas')
        with open(data[0], 'wb') as fp:
            pickle.dump(data, fp)
        cliente.send('registrado'.encode())
        #sys.exit(0)

    def validate_user(self, data, cliente):
        print('Recibí 2 madriolas')
        try: 
            with open(data[0], 'rb') as fp:
                data2 = pickle.load(fp)
                if(data[0] == data2[0] and data[1] == data2[2]):
                    cliente.send('concedido'.encode())
        except:
            cliente.send('denegado'.encode())
            print('No existe archivo')
        #sys.exit(0)

if __name__ == "__main__":
    s = Server('localhost', 5001)