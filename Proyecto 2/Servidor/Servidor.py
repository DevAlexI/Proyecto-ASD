import socket
import os 
import os.path
from os import listdir
from os.path import isfile, join
import time
import pickle
import sys
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conexiones = []
        self.peers = []

        # Empezar a busscar conexiones
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(20)
        print(f"[*] Escuchando como {self.host}:{self.port}")

        while True:
            self.socketCliente, self.direccion = s.accept() 
            hilo = threading.Thread(target=self.handler, args=(self.socketCliente, self.direccion))
            hilo.daemon = True
            hilo.start()
            self.conexiones.append(self.socketCliente)
            self.peers.append(self.direccion[0])
            self.mandarPeers()

        self.socketCliente.close()
        s.close()
    
    def handler(self, c, a):
        global conexiones

        while True:
            datos = c.recv(1024)
            data_decompressed = pickle.loads(datos)

            if len(data_decompressed) == 3:
                self.save_user(data_decompressed, self.socketCliente)
            elif len(data_decompressed) == 2:
                self.validate_user(data_decompressed, self.socketCliente)


            for usuarios in self.conexiones:
                usuarios.send(bytes(datos))

            if not datos:
                print(str(a[0]), ':', str(a[1]), 'se ha desconectado')
                self.conexiones.remove(c)
                self.peers.remove(a[0])
                c.close()
                self.mandarPeers()
                break

    def mandarPeers(self):
        p = ""
        for peer in self.peers:
            p = p + peer + ","
            print("p: ", p)

        for usuarios in self.conexiones:
            print(usuarios)
            usuarios.send(b'\x11' + bytes(p, 'utf-8'))

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
    s = Server('0.0.0.0', 10000)