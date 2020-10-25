import socket
import os 
import sys
import os.path
from os import listdir
from os.path import isfile, join
import time
from encriptador import Encriptador
import getpass
import select
import threading
import _thread

class Servidor(threading.Thread):

    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host=''
        puerto = 5001
        self.s.bind((host, puerto))
        self.s.listen(5)
        print(f"--Escuchando en el puerto {puerto}--")         
        (cliente, addr) = self.s.accept()
        print(f"Conexion desde {str(addr)}") 

        while True:
            objeto = cliente.recv(4096)            
            print(f"{addr}:{objeto}")

class Cliente(threading.Thread): 

    def conectar(self, host, puerto):
        self.s.connect((host, puerto))

    def cliente(self, host, puerto, msg):               
        mandar = self.s.send(msg)           
        print("Mandar\n")

    def correr(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            host = input("Ingresa la direccion del host: \n>>")            
            puerto = int(input("Ingresa el puerto: \n>>"))
        except EOFError:
            print("Error")
            return True
        
        print("Conectando...\n")
        s = ''
        self.conectar(host, puerto)
        print("Conectado")

        while True:            
            print("Esperando mensajes...\n")
            msg = input(">>")
            if msg == 'salir':
                break
            if msg == '':
                continue
            print("Enviando\n")
            self.cliente(host, puerto, msg)
        return True

if __name__ == "__main__":
    
    key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
    enc = Encriptador(key)
    clear = lambda: os.system('cls')

    while True:
        if os.path.isfile('llave.txt.enc'):
            
            clave = str(getpass.getpass("Ingresa tu contraseña: "))
            enc.decifrar_archivo("llave.txt.enc")
            d = ''
            with open("llave.txt", "r") as f:
                d = f.readlines()
            if d[1] == clave:
                enc.encriptar_archivo("llave.txt")
                    
            while True:
                clear()
                opcion = int(input("1. Presiona '1' para entrar a la sala de chat.\n2. Presiona '2' para salir.\n"))
                clear()

                if opcion == 1:
                    print("--Iniciando Servidor--")
                    s = Servidor()
                    time.sleep(1)
                    c = Cliente()
                    c.correr()
                    print("--Sala de chat--")

                elif opcion == 2:
                    exit()
                    
                else:
                    print("Selecciona una opcion valida")
        else:
            while True:
                clear()
                nombre = str(input("Ingresa tu nombre de usuario: "))
                clave = str(getpass.getpass("Ingresa tu contraseña: "))
                reclave = str(getpass.getpass("Confirma la contraseña: "))
                if clave == reclave:
                    f = open("llave.txt", "w+")
                    f.write(f"{nombre}\n{clave}")
                    f.close()
                    enc.encriptar_archivo("llave.txt")
                    clear()
                    print("Espera unos segundos mientras se configura...")
                    time.sleep(3)
                    clear()
                    break
                else:
                    print("Las contraseñas no coinciden")

