import socket
import os 
import os.path
from os import listdir
from os.path import isfile, join
import time
import tqdm # Biblioteca ara mostrar una barra de progreso
from encriptador import Encriptador

BUFFER = 5120 # Ir mandando 5 kb's a la vez
host = "localhost"
puerto = 5001

# Ni idea por que la llave tiene que ser asi, trate de cambiarlo a una generada aleatoriamente pero el programa truena
key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = Encriptador(key)
clear = lambda: os.system('cls')

# 'datos.txt.enc' es un archivo de texto encriptado donde estan todos los datos relevantes
# para la encriptacion, como la llave, la primera vez que se corra el programa buscara este archivo
# en la raiz, si no esta, se creara uno y le pedira al usuario una nueva contraseña
if os.path.isfile('datos.txt.enc'):

    while True:
        clave = str(input("Ingresa la contraseña: "))
        enc.decifrar_archivo("datos.txt.enc")
        p = ''
        with open("datos.txt", "r") as f:
            p = f.readlines()
        if p[0] == clave:
            enc.encriptar_archivo("datos.txt")
            break

    while True:
        clear()
        opcion = int(input("1. Presiona '1' para encriptar un archivo.\n2. Presiona '2' para decifrar un archivo.\n3. Presiona '3' para salir.\n"))
        clear()
        if opcion == 1:
            archivo = (input("Ingresa el nombre del archivo: "))
            enc.encriptar_archivo(str(archivo))
            archivo += ".enc"
            peso = os.path.getsize(archivo)
            llave = "datos.txt.enc"

            # Iniciar el socket
            print("*///////////////////////////////////////////////////*")
            s = socket.socket()
            print(f"[+] Conectandose a {host}:{puerto}")
            s.connect((host, puerto))
            print("[+] Conexion establecida.")

            # Empezar a mandar los archivos
            s.send(f"{archivo}<>{peso}<>{llave}".encode())
            progreso = tqdm.tqdm(range(peso), f"[->] Enviando {archivo}", unit="B", unit_scale=True, unit_divisor=1024)

            # Mandar la llave para la encriptacion y decifrado
            with open(llave, "rb") as f:
                leerBytes = f.read(BUFFER)
                s.sendall(leerBytes)
            
            # Mandar el archivo
            with open(archivo, "rb") as f:
                for _ in progreso:
                    leerBytes = f.read(BUFFER)
                    if not leerBytes:
                        # Se acabo de transmitir datos
                        progreso.close()
                        break
                    s.sendall(leerBytes)
                    progreso.refresh()
                    progreso.update(len(leerBytes))
            print(f"[+] {archivo} enviado con exito")
            s.shutdown(socket.SHUT_WR)

            # Recibir de vuelta la imagen decifrada desde el servidor
            respuesta = s.recv(BUFFER).decode('utf-8')
            respuesta = os.path.basename(respuesta)
            progreso = tqdm.tqdm(range(peso), f"[+] Reciviendo {respuesta}", unit="B", unit_scale=True, unit_divisor=1024)

            with open(respuesta, "wb") as f:
                for _ in progreso:
                    leerBytes = s.recv(BUFFER)
                    if not leerBytes:    
                        # Se acabo de transmitir datos
                        progreso.close()
                        break
                    # Escribir al directorio los bytes recividos
                    f.write(leerBytes)
                    progreso.update(len(leerBytes))
            print(f"[+] {respuesta} decifrado recibido con exito")
            
            nombre, extension = respuesta.split('.')
            os.rename(respuesta, f"copiaDecifrada.{extension}")
            
            s.close()
            input("Presiona cualquier tecla para continuar...")

        elif opcion == 2:
            archivo = (input("Ingresa el nombre del archivo: "))
            enc.decifrar_archivo(str(archivo))
            print("Archivo decifrado")
            input("Presiona cualquier tecla para continuar...")

        elif opcion == 3:
            exit()
        else:
            print("Selecciona una opcion valida")

else:
    while True:
        clear()
        clave = str(input("Ingresa la contraseña que se usara para el cifrado: "))
        reclave = str(input("Confirma la contraseña: "))
        if clave == reclave:
            break
        else:
            print("Las contraseñas no coinciden")
    f = open("datos.txt", "w+")
    f.write(clave)
    f.close()
    enc.encriptar_archivo("datos.txt")
    print("Reinicia el programa")
    time.sleep(5)