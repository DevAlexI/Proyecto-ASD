# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 15:14:52 2020

@author: Raduarez95
"""

import os
import socket 
import threading
import tqdm
import subprocess

#Constantes usadas durante el código
PORT = 9999
SERV = socket.gethostbyname(socket.gethostname())
DIR = (SERV,PORT)
BUFFER = 4096
DESCONECTAR = "-1"
#Definir clientes y servidores
clientes = []
servidores = []
video = "prueba.mp4"
#Conexion servidor
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(DIR)
def atenderCliente(con, addr):
    conectado = True
    print(f"<Nueva Conexion> direccion: {addr} conectada")
    while conectado:
        msg = str(con.recv(BUFFER).decode())
        print(f"<{addr}> {msg}")
        if(msg == "cliente"):
            clientes.append(addr[1])
        #Si es servidor, se agregara su objeto de conexion a un arreglo de conexiones servidores
        elif(msg == "servidor"):
            servidores.append(addr[1])
            print("Dividiendo Video.")
            servs = 3
            print("Dividiendo" + video + "con duración de " + str(get_video_length_s(video)) + "s en " + str(servs) + " servidores")
            chunk = get_video_length_s(video) / servs
            print("Dividiendo en segmentos de " + str(chunk) + "segundos")
            divide_video(video, chunk)
            print("listo")
            print("Enviando video fragmentado a servidor")
            identificador = servidores.index(addr[1])#Identificación para cada servidor
            archivo = "prueba/"+video[:-4]+str(identificador)+".mp4"
            print(archivo);
            
            
##############################3
def get_video_length_s(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def divide_video(filename, duration):
    try:
        if not os.path.exists(os.path.splitext(filename)[0]):
            os.makedirs(os.path.splitext(filename)[0])
    except OSError:
        print ('Error: Creating directory of data')
    result = subprocess.run(["ffmpeg", "-i", filename, "-acodec", "copy", 
                            "-f", "segment", "-segment_time", str(duration), 
                            "-vcodec", "copy", "-reset_timestamps", str(1), 
                            os.path.splitext(filename)[0]+"/"+ os.path.splitext(filename)[0]+"%d"+os.path.splitext(filename)[1]],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
def mandarVideo(con):
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
            con.sendall(lectura)
            barra.refresh()
            barra.update(len(lectura))
    print(f"{archivo} enviado con éxito!!")
    
def mandarMsg(msg,con):
    mensaje = msg.encode()
    con.send(mensaje)
def start():
    serv.listen()
    print(f"<Escuchando> Servidor escuchando desde {SERV}")
    while True:
        con, addr = serv.accept()
        #Uso de hilos para antender peticiones de clientes (y servidores)
        thread = threading.Thread(target=atenderCliente, args=(con,addr))
        thread.start()
        #Mostrar conexion activas, por alguna razón a mi me marca 4 iniciales
        #Nota, cambiar la resta si se muestra diferente a las conexiones reales.
        print(f"<Conexiones Activas> {threading.activeCount()-5}")
#####################
print("<Iniciando> Servidor Esta Prendido...")
start()