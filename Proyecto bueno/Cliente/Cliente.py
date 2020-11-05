import tkinter as tk
from tkinter import messagebox as mb
from tkinter.filedialog import askopenfilename
import pickle
import socket
import threading
import sys
import time
import os
import tqdm


class Cliente(tk.Frame):
    def __init__(self, ip, master = None):
        super().__init__(master)
        self.master = master
        #print("--Entrando a la Sala de Chat--")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.connect((ip, 10000))
        except:
            mb.showerror(title='Error de conexión', message='Hay un problema con la conexión')
        self.chat()
        #self.login(self.sock)
        #hilo0 = threading.Thread(target=self.chat)
        #hilo0.daemon = True
        #hilo0.start()
        #hilo1 = threading.Thread(target=self.mandarMsg, args=(self.sock,))
        #hilo1.daemon = True
        #hilo1.start()
        hilo2 = threading.Thread(target=self.listening, args=(self.sock,))
        hilo2.daemon = True
        hilo2.start()
    
    def chat(self):
    #chat = tk.Toplevel(self.master)
        self.master.title("Cha Cha Chat me - Chat")
        self.master.geometry("400x500")
        icon = tk.PhotoImage(master=self.master, file = 'images/chat.png')
        self.master.iconphoto(False, icon)

        self.ChatLog = tk.Text(self.master, bd=0, bg="white", height="8", width="50", font="Arial")
        self.ChatLog.insert(tk.END, "Connecting to your partner..\n ------------------------------\n")
        #self.ChatLog.configure(state= 'disabled')

        scrollbar = tk.Scrollbar(self.master, command=self.ChatLog.yview, cursor="heart")
        self.ChatLog['yscrollcommand'] = scrollbar.set

        self.SendButton = tk.Button(self.master, font=2, text="Enviar", width="11", height=5,
                    bd=0, bg="#FFBF00", activebackground="#FACC2E")
        
        #self.SendFilesButton = tk.Button(self.master, font=2, text="Enviar archivo", width="11", height=5,
        #            bd=0, bg="#00ffff", activebackground="#a4e1eb", justify = tk.LEFT, command = self.mandarArchivo)
    # SendFileButton = tk.Button()

        self.EntryBox = tk.Entry(self.master, bd=0, bg="white", font="Arial")
        scrollbar.place(x=376,y=6, height=386)
        self.ChatLog.place(x=6,y=6, height=386, width=370)
        self.EntryBox.place(x=128, y=401, height=90, width=265)
        self.SendButton.place(x=6, y=401, height=30)
        #self.SendFilesButton.place(x = 6, y = 450 , height = 30)

        self.SendButton.bind("<Button-1>", lambda e: self.mandarMsg(self.EntryBox.get()))
        #self.SendFilesButton.bind("<Button-1>", self.mandarArchivo())

    def listening(self, sock):
        while True:
            datos = self.sock.recv(1024)
            print(datos)
            if not datos:
                break
            if datos[0:1] == b'\x11':
                self.actPeers(datos[1:])
            else:
                print(str(datos, 'utf-8'))
                self.ChatLog.insert(tk.END, str(datos, 'utf-8'))
                #print(datos)
    
    def mandarArchivo(self):
        print('Entra a función')
        file = askopenfilename(title="Seleccionar archivo")     
        try:
            with open(file, "rb") as f:
                # send file
                data = f.read()
                self.sock.sendall(data)
                print("Archivo enviado")

        except:
            print("No seleccionaste nada o hay un error con el archivo")



    def mandarMsg(self, *args):
        if len(args) == 1:
            for msg in args:
                print(msg+'\n')
                self.sock.send(bytes(msg+'\n', 'utf-8'))
        else:
            pack_of_data = []
            for data in args:
                pack_of_data.append(data)
            pack_of_data = pickle.dumps(pack_of_data)
            print(pack_of_data)


    def actPeers(self, peerDatos):
        print("peer Datos: ", peerDatos)
        p2p.peers = str(peerDatos, 'utf-8').split(",")[:-1]
        print("p2p peers", p2p.peers)

class p2p:
    peers = ['127.0.0.1']

if __name__ == "__main__":
    root = tk.Tk()

    for peer in p2p.peers:
        try:
            cliente = Cliente(peer, master=root)
            cliente.mainloop()
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print('Error de código')
            sys.exit(0)
