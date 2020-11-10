import cv2
import os 
import numpy
import subprocess
import shutil

# ! IMPORTANTE
# TODO: hace falta agregarle a algunas funciones operaciones para
# TODO: cuando ya exista algun archivo lo sobreescriba...
# ! DEBES ELIMINAR LA CARPETA CON EL NOMBRE DEL ARCHIVO ORIGEN PARA QUE FUNCIONE SIN INCONVENIENTES HASTA QUE RESUELVA ESO
# ! IMPORTANTE
# TODO: Hace falta agregarles Try/Except para si erras en el nombre del archivo o no existe.

# * Función para divir los cuadros y los guarda en la carpeta data
# * Al momento de dividir los cuadros invierte la matriz para hacer la imagen negativa
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
        frame = numpy.invert(frame)
        if ret == False:
            break
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
    except expression as identifier:
        print("falló")

# * Realiza toda las operaciones juntas ;9
def process_video(filename):
    # ! Descomentar la primer línea para su uso normal 
    # ! Comentarla para TESTEAR después de haberla corrido una vez para ahorrar tiempo
    split_frames(Filename)
    strip_audio(filename)
    make_video(filename)
    add_audio(filename)

# * Elimina la información para poder 
def destroy_data(filename):
    try:
        shutil.rmtree("data")
        print("Imágenes erradicados")
    except:
        print("No hay imágenes qué borrar")
    try:
        shutil.rmtree(os.path.splitext(filename)[0])
        print("Multimedia erradicada")
    except:
        print("No hay multimedia qué borrar")
    # ! Descomentar estas líneas después de haber probado esto de forma aislada
    """ 
    try:
        os.remove(filename)
    except:
    ("no hay archivo origen qué borrar")
    """

# ! Usar el video CORTO de tu preferencia, introducirlo en ésta carpeta. 
video = "Rivals0.mp4"

process_video(video)

# ! funcion importante para borrar la información después de  haberla utilizado
"""
destroy_data(video)
"""