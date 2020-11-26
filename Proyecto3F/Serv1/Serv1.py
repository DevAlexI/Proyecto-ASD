# -*- coding: utf-8 -*-
"""

@author: Raduarez95
"""
import os
import cv2
import numpy
import socket
import subprocess
import glob
import tqdm

#Constantes
PORT = 9999
DESCONECTAR = "-1"
SERV = "169.254.92.49"
DIR = (SERV, PORT)
BUFFER = 4096
SERVIDOR = 0 ################Cambiar para cada servidor
#Inicio de Socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(DIR)
#Método conexión
def conectar(cliente):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(DIR)
#Método para mostrar quien es frente al servidor
def presentarse(msg):
    mensaje = msg.encode()
    cliente.send(mensaje)
#Método para mandar mensajes al servidor
def mandarMsg(msg):
    mensaje = msg.encode()
    cliente.send(mensaje)
###################Modificar videos
def split_frames(filename):
    cap= cv2.VideoCapture(filename) 
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print ('Error: Creating directory of data')
    i=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False or None:
            break
        frame = numpy.invert(frame)
        if(i<10):
            cv2.imwrite('./data/f0'+str(i)+'.png', frame)
        else:
            cv2.imwrite('./data/f'+str(i)+'.png', frame)
        i+=1
    
    cap.release()
    cv2.destroyAllWindows()

# * extrae el audio del video
def strip_audio(filename):
    print("Extrayendo audio...")
    if not os.path.exists(os.path.splitext(filename)[0]):
            os.makedirs(os.path.splitext(filename)[0])
    result = subprocess.run(["ffmpeg", "-i", filename, 
                            os.path.splitext(filename)[0]+"/"+os.path.os.path.splitext(filename)[0]+".mp3"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    print("Audio extraído.")

# * Junta las imagenes de data en un video mp4 sin audio.
def make_video(filename):
    if not os.path.exists(os.path.splitext(filename)[0]):
            os.makedirs(os.path.splitext(filename)[0])
    print("Realizando video...")
    result = subprocess.run(["ffmpeg", "-f", "image2", 
                        "-pattern_type", "glob", "-framerate", "60", 
                        "-i", "data/f*.png", os.path.splitext(filename)[0]+"/"+os.path.splitext(filename)[0]+"Inv.mp4"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    print("Video completado.")

# * Junta el audio con el video ya extraidos
def add_audio(filename):
    print("Agregando audio...")
    try:
        result = subprocess.run(["ffmpeg", "-i", os.path.splitext(filename)[0]+"/"+os.path.splitext(filename)[0]+"Inv.mp4", 
                            "-i", os.path.splitext(filename)[0]+"/"+os.path.splitext(filename)[0]+".mp3",
                            "-map", "0:v", "-map", "1:a", "-c:v", 
                            "copy", "-shortest", os.path.splitext(filename)[0]+"/output.mp4"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
        print("Video listo")
    except:
        print("falló")

# * Realiza toda las operaciones juntas ;9
def process_video(filename):
    # ! Descomentar la primer línea para su uso normal 
    # ! Comentarla para TESTEAR después de haberla corrido una vez para ahorrar tiempo
    split_frames(filename)
    strip_audio(filename)
    make_video(filename)
    add_audio(filename)
#Método Mandar video
def mandarVideo(archivo):
    mandarMsg("fragmentos")
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


#######################################################Codigo ejecutable##################################################3
presentarse("servidor")
input()
mandarMsg("recibir")

##############################Inicio Recepción video####################################
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
            barra.close()
            break;
        f.write(lectura)
        barra.update(len(lectura))
    print(f"{archivo} recibido con éxito")
cliente.close()
##############################Fin Recepción video#######################################
############################Invertir imágenes###########################################
process_video(archivo)
############################Fin Invertir imágenes#######################################
############################Rearmar Video###############################################
print("Rearmando video...")
img_array = []
for filename in glob.glob(r'data\f*.png'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)

videoF = 'parte'+str(SERVIDOR)+'.mp4'
out = cv2.VideoWriter(videoF,cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()    
print("Video rearmado!!!")
############################Fin Rearmar Video###########################################
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(DIR)
presentarse("servidor")
input()
mandarVideo(videoF)
#Enviar el video
input()