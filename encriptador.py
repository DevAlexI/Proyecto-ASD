from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time

class Encriptador:

    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encriptar(self, mensaje, key, key_size = 256):
        mensaje = self.pad(mensaje)
        iv = Random.new().read(AES.block_size) # Vector de inicializacion
        cifrado = AES.new(key, AES.MODE_CBC, iv) # Tipo de cifrado
        return iv + cifrado.encrypt(mensaje)
    
    def encriptar_archivo(self, nombreDeArchivo):
        with open(nombreDeArchivo, 'rb') as fo: # rb = leer en binario
            textoPlano = fo.read()
        enc = self.encriptar(textoPlano, self.key)
        with open(nombreDeArchivo + ".enc", 'wb') as fo: # wb = escrbir en binario
            fo.write(enc)
        os.remove(nombreDeArchivo)  

    def decifrar(self, textoCifrado, key):
        iv = textoCifrado[:AES.block_size]
        cifrado = AES.new(key, AES.MODE_CBC, iv)
        textoPlano = cifrado.decrypt(textoCifrado[AES.block_size:])
        return textoPlano.rstrip(b"\0")
    
    def decifrar_archivo(self, nombreDeArchivo):
        with open(nombreDeArchivo, 'rb') as fo:
            textoCifrado = fo.read()
        dec = self.decifrar(textoCifrado, self.key)
        with open(nombreDeArchivo[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(nombreDeArchivo)


