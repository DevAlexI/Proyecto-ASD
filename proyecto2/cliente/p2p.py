import socket
import threading
import sys
import time

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

        for usuarios in self.conexiones:
            usuarios.send(b'\x11' + bytes(p, 'utf-8'))

class Cliente:
    def __init__(self, ip):
        print("--Entrando a la Sala de Chat--")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((ip, 10000))

        hilo = threading.Thread(target=self.mandarMsg, args=(sock,))
        hilo.daemon = True
        hilo.start()

        while True:
            datos = sock.recv(1024)
            if not datos:
                break
            if datos[0:1] == b'\x11':
                self.actPeers(datos[1:])
            else:
                print(str(datos, 'utf-8'))

    def mandarMsg(self, sock):
        while True:
            msg = input(">>")
            sock.send(bytes(msg, 'utf-8'))

    def actPeers(self, peerDatos):
        p2p.peers = str(peerDatos, 'utf-8').split(",")[:-1]

class p2p:
    peers = ['127.0.0.1']

if __name__ == "__main__":
    try:
        print("Tratando de conectar al servidor...")
        time.sleep(3)
        for peer in p2p.peers:
            try:
                cliente = Cliente(peer)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
            try:
                servidor = Servidor()
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print("Error al iniciar el servidor...")

    except KeyboardInterrupt:
        sys.exit(0)