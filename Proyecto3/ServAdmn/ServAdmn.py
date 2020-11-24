# -*- coding: utf-8 -*-
"""

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
#Conexion servidor
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(DIR)
#Método para atender clientes en multihilo
def atenderCliente(con, addr):
    conectado = True
    video = "prueba.mp4"
    print(f"<Nueva Conexion> direccion: {addr} conectada")
    while conectado:
        msg = str(con.recv(BUFFER).decode())
        print(f"<{addr}> {msg}")
        if(msg == "cliente"):
            clientes.append(addr[1])
        #Si es servidor, se agregara su objeto de conexion a un arreglo de conexiones servidores
        elif(msg == "servidor"):
            servidores.append(addr[1])
###########################Se Recibe video crudo del cliente####################
        elif(msg == "video"):
            print("Recibiendo Video.")
            contenido = con.recv(BUFFER).decode('utf-8')
            archivo, peso = contenido.split("<>")
            archivo = os.path.basename(archivo)
            peso = int(peso)
            barra = tqdm.tqdm(range(peso),f"[->] Recibiendo {archivo}", unit = "B", unit_scale=True, unit_divisor=1024)
            with open(archivo, "wb") as f:
                for _ in barra:
                    lectura = con.recv(BUFFER)
                    if not lectura:
                        print("ya no recibe datos")
                        barra.close()
                        break;
                    f.write(lectura)
                    barra.update(len(lectura))
                    
                print("recibido con éxito")
#############################Fin Recepción de video####################################################
#############################Se divide el video ####################################################
            print("Diviendo Archivo...")
            servs = 3
            video = archivo
            print("Dividiendo " + video + " con duración de " + str(get_video_length_s(video)) + "s en " + str(servs) + " servidores")
            chunk = get_video_length_s(video) / servs
            print("Dividiendo en segmentos de " + str(chunk) + "segundos")
            divide_video(video, chunk)
            print("listo")
            con.close()
            conectado = False
########################Fin de división y cierre de conexión con cliente##################################
########################Envio de fragmentos a servidores##########################################
        elif(msg == "recibir"):
            print("Enviando video fragmentado a servidor")
            identificador = servidores.index(addr[1])#Identificación para cada servidor
            archivo = "prueba/"+video[:-4]+str(identificador)+".mp4" 
            mandarVideo(archivo,con)
            conectado = False
########################Fin de envio fragmentos a servidores##########################################
        if(msg == "recibir-fragmentos"):
            print("hola")
        if(msg == "cliente-final"):
            print("hola")
                
                 
                
#            print("Enviando video fragmentado a servidor")
#            identificador = servidores.index(addr[1])#Identificación para cada servidor
#            archivo = "prueba/"+video[:-4]+str(identificador)+".mp4"
#            print(archivo);
        #conocerConexion(msg, con, addr)
        print(f"<Clientes> {clientes}")
        print(f"<Servidores> {servidores}")
        
        
        #enviar frames(servidores)
        #Pedir frames(servidores)
        #unirVideo
        #Regresar video a (clientes)
        if(msg == "-1"): 
            conectado = False
            break;
    print(f"<{addr}> Desconectado.")

#Método para comenzar a escuchar
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
#########Mandar Video###############################
def mandarVideo(archivo,cliente):
    peso = os.path.getsize(str(archivo))
    previo = f"{archivo}<>{peso}"
    input()
    mandarMsg(previo,cliente)
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

#Métodos de división de video.
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
def mandarMsg(msg,con):
    mensaje = msg.encode()
    con.send(mensaje)
############Código ejecutable###################################################################
print("<Iniciando> Servidor Esta Prendido...")
start()
