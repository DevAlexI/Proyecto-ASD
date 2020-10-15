import socket
import os 
import os.path
from os import listdir
from os.path import isfile, join
from encriptador import Encriptador
import select 
import sys 
import _thread

class SocketServidor:

    def __init__(self, host, puerto):
        self.host = host
        self.puerto = puerto

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        s.bind((host,puerto))
        print(f"[*] Escuchando como {self.host}:{self.puerto}")
        s.listen(50) 
        self.lista_usuarios = []
        
        while True: 
            conn, ip = s.accept() 
            self.lista_usuarios.append(conn) 
            print(f"{ip[0]} se ha conectado")
            # Se crea un nuevo hilo por cada usuario que se conecta
            _thread.start_new_thread(self.usuarios,(conn,ip))     
        conn.close() 
        s.close() 

    def usuarios(self, conn, ip):
        conn.send("--Bienvenido a la sala de chat--".encode('utf-8')) 

        while True: 
                try: 
                    mensaje = conn.recv(2048) 
                    if mensaje: 
                        print(f"<{ip[0]}>  {mensaje}")
                        # Manda el mensaje a broadcast
                        mandar_mensaje = f"<{ip[0]}>  {mensaje}"
                        self.broadcast(mandar_mensaje, conn)  
                    else: 
                        self.remove(conn) 
                except: 
                    continue

    def broadcast(self, mensaje, conexion): 
        for usuarios in self.lista_usuarios: 
            if usuarios != conexion: 
                try: 
                    usuarios.send(mensaje) 
                except: 
                    usuarios.close() 
                    # Si se cierra la conexion, removemops al usuarios
                    self.remove(usuarios) 

    def remove(self, conexion): 
        if conexion in self.lista_usuarios: 
            self.lista_usuarios.remove(conexion) 


if __name__ == "__main__":

    key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
    enc = Encriptador(key)
    s = SocketServidor('localhost', 5001)




