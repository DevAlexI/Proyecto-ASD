# -*- coding: utf-8 -*-
"""

@author: Raduarez95
"""

import socket

PORT = 9999
DESCONECTAR = "-1"
SERV = "192.168.56.1"
DIR = (SERV, PORT)

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(DIR)

def presentarse(msg):
    mensaje = msg.encode()
    cliente.send(mensaje)
def mandarMsg(msg):
    mensaje = msg.encode()
    cliente.send(mensaje)

presentarse("servidor")    
input()
mandarMsg("Hola")
input()



mandarMsg(DESCONECTAR)