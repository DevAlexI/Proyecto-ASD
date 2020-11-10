import subprocess
import os

# TODO: Hace falta agregarles Try/Except para si erras en el nombre del archivo o no existe.
# TODO: Hace falta hacer una función para juntar todos los archivos de los servidores de procesamiento.

# * Calcula la duración del video en segundos
def get_video_length_s(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

# * divide el video en la duración ingresada
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


servidores = 8
video = input("Elige el video a subir> ")
print("Dividiendo" + video + "con duración de " + str(get_video_length_s(video)) + "s en" + str(servidores) + " servidores")

# ! esta línea de abajo no sólo es prueba de código, hay que guiarse en ella para que a cada servidor se le asignen la misma cantidad de cuadros.
chunk = get_video_length_s(video) / servidores
print("Dividiendo en segmentos de " + str(chunk) + "segundos")
divide_video(video, chunk)
print("listo")

# * Función para eliminar el video una vez que se envió el archivo, probablemente haya que agrandarla
def destroy_data(filename):
    try:
        os.remove(filename)
    except:
    ("no hay archivo origen qué borrar")