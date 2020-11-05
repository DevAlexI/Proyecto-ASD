import socket
import threading
import sys
import time
import pickle

class Servidor:
    conexiones = []
    peers = []
    
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', 10000))
        sock.listen(1)
        print("---Iniciando Servidor---")

        while True:
            c, a = sock.accept()
            hilo = threading.Thread(target=self.handler, args=(c, a))
            hilo.daemon = True
            hilo.start()
            self.conexiones.append(c)
            self.peers.append(a[0])
            print(str(a[0]), ':', str(a[1]), 'Se ha conectado')
            self.mandarPeers()

    def handler(self, c, a):
        global conexiones

        while True:
            datos = c.recv(1024)
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

if __name__ == "__main__":
    try:
        servidor = Servidor()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        pass