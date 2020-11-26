# -*- coding: utf-8 -*-
"""

@author: Raduarez95
"""
import os
import tqdm
import socket

#Uso de constantes
PORT = 9999
DESCONECTAR = "-1"
SERV = "169.254.92.49"
DIR = (SERV, PORT)
BUFFER = 4096
#Inicio de Socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(DIR)
#Método para mostrar quien es frente al servidor
def conectar(cliente):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(DIR)
def presentarse(msg):
    mensaje = msg.encode()
    cliente.send(mensaje)
#Método para mandar mensajes al servidor
def mandarMsg(msg):
    mensaje = msg.encode()
    cliente.send(mensaje)
    if(msg == DESCONECTAR): cliente.shutdown(socket.SHUT_WR)
#Método de envío de Video
def mandarVideo():
    mandarMsg("video")
    archivo = input("Ingresa nombre del archivo: ")
    peso = os.path.getsize(str(archivo))
    previo = f"{archivo}<>{peso}"
    input()
    mandarMsg(previo)
    barra = tqdm.tqdm(range(peso),f"[->] Enviado {archivo}", unit = "B", unit_scale=True, unit_divisor=1024)
    with open(archivo,"rb") as f:
        for _ in barra:
            lectura = f.read(BUFFER)
            if not lectura:
                barra.close()
                break
            cliente.sendall(lectura)
            barra.refresh()
            barra.update(len(lectura))
    print(f"{archivo} enviado con éxito!!")
    cliente.close()
    
    
######3Codigo ejecutable#########
presentarse("cliente")
input()
mandarMsg("Hola")
input()
mandarVideo()
input()
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(DIR)
presentarse("cliente")
input()
mandarMsg("cliente-final")
print("Recibiendo Video.")
contenido = cliente.recv(BUFFER).decode('utf-8')
archivo, peso = contenido.split("<>")
archivo = os.path.basename(archivo)
peso = int(peso)
barra = tqdm.tqdm(range(peso),f"[->] Recibiendo {archivo}", unit = "B", unit_scale=True, unit_divisor=1024)
with open(archivo, "wb") as f:
    for _ in barra:
        lectura = cliente.recv(BUFFER)
        if not lectura:
            print("ya no recibe datos")
            barra.close()
            break;
        f.write(lectura)
        barra.update(len(lectura))
cliente.close()
#Recibir el video final

