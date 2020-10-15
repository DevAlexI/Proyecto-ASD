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

class SocketCliente:

    def __init__(self, host, puerto):
        self.host = host
        self.puerto = puerto

        # Iniciar el socket
        print("*///////////////////////////////////////////////////*")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print(f"[+] Conectandose a la sala de chat")
        s.connect((host, puerto))
        print("[+] Conexion establecida.")

        while True:
            lista_sockets = [s] 
            leer_sockets, _, _ = select.select(lista_sockets,[],[]) 

            for sockets in leer_sockets+[sys.stdin]: 
                if sockets == s: 
                    mensaje = sockets.recv(2048) 
                    print(mensaje.decode('utf-8'))
                else: 
                    mensaje = sys.stdin.readline() 
                    s.send(mensaje.encode('utf-8')) 
                    sys.stdout.write("<Tu>") 
                    sys.stdout.write(mensaje) 
                    sys.stdout.flush() 
        s.close() 

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
                    s = SocketCliente('localhost', 5001)

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

