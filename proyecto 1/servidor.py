import socket
import os 
import os.path
from os import listdir
from os.path import isfile, join
import time
import tqdm # Biblioteca para mostrar una barra de progreso
from encriptador import Encriptador

class SocketServidor:

    def __init__(self, host, puerto):
        self.host = host
        self.puerto = puerto

        # Empezar a busscar conexiones
        s = socket.socket()
        s.bind((self.host, self.puerto))
        print(f"[*] Escuchando como {self.host}:{self.puerto}")
        s.listen(5)
        
        # Una vez que se encuentra una conexion disponible
        socketCliente, direccion = s.accept() 
        print(f"[+] Conexion con {direccion}")

        # Recibir los archivos del lado cliente, usando el socket del cliente
        BUFFER = 5120 # Ir mandando 5120 kb's a la vez
        paquete = socketCliente.recv(BUFFER).decode('utf-8')
        # El archivo, el peso del archivo y la llave vienen separados por un '<>'
        archivo, peso, llave = paquete.split("<>")
        # Remover toda la direccion del archivo por cuestiones de compatibilidad
        archivo = os.path.basename(archivo)
        llave = os.path.basename(llave)
        # Convertir el peso a enteros
        peso = int(peso)

        # Empezar a recivir los archivos del lado cliente
        progreso = tqdm.tqdm(range(peso), f"[<-] Reciviendo {archivo}", unit="B", unit_scale=True, unit_divisor=1024)
        # Recibir primero la llave de encriptacion
        with open(llave, "wb") as f:
            leerBytes = socketCliente.recv(BUFFER)
            # Escribir al directorio los bytes recividos
            f.write(leerBytes)

        # Recibir el archivo
        with open(archivo, "wb") as f:
            for _ in progreso:
                leerBytes = socketCliente.recv(BUFFER)
                if not leerBytes:    
                    # Se acabo de transmitir datos
                    progreso.close()
                    break
                # Escribir al directorio los bytes recividos
                f.write(leerBytes)
                progreso.update(len(leerBytes))
            print(f"[+] {archivo} recibido con exito")

        # Mandar el archivo devuelta decifrado
        enc.decifrar_archivo(str(archivo))
        respuesta = archivo[:-4] # Quitarle la extension .enc
        socketCliente.send(respuesta.encode())
        progreso = tqdm.tqdm(range(peso), f"[->] Enviando {archivo} devuelta decifrado", unit="B", unit_scale=True, unit_divisor=1024)

        with open(respuesta, "rb") as f:
            for _ in progreso:
                leerBytes = f.read(BUFFER)
                if not leerBytes:
                # Se acabo de transmitir datos
                    progreso.close()
                    break
                socketCliente.sendall(leerBytes)
                progreso.refresh()
                progreso.update(len(leerBytes))
        print(f"[+] {archivo} decifrado enviado con exito")

        socketCliente.close()
        s.close()

if __name__ == "__main__":

    key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
    enc = Encriptador(key)
    s = SocketServidor('localhost', 5001)



