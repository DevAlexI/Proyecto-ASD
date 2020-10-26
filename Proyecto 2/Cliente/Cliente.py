import tkinter as tk
from tkinter import messagebox as mb
import socket as s
import sys
import pickle

class Cliente(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets_login()

        #self.chat()
    
    def chat(self):
        chat = tk.Toplevel(self.master)
        chat.title("Cha Cha Chat me - Chat")
        chat.geometry("400x500")
        icon = tk.PhotoImage(master=chat, file = 'images/chat.png')
        chat.iconphoto(False, icon)

        ChatLog = tk.Text(chat, bd=0, bg="white", height="8", width="50", font="Arial")
        ChatLog.insert(tk.END, "Connecting to your partner..\n")
        ChatLog.config(state=tk.DISABLED)

        scrollbar = tk.Scrollbar(chat, command=ChatLog.yview, cursor="heart")
        ChatLog['yscrollcommand'] = scrollbar.set

        SendButton = tk.Button(chat, font=30, text="Send", width="12", height=5,
                    bd=0, bg="#FFBF00", activebackground="#FACC2E")
       # SendFileButton = tk.Button()

        EntryBox = tk.Text(chat, bd=0, bg="white",width="29", height="5", font="Arial")
        scrollbar.place(x=376,y=6, height=386)
        ChatLog.place(x=6,y=6, height=386, width=370)
        EntryBox.place(x=128, y=401, height=90, width=265)
        SendButton.place(x=6, y=401, height=90)
        #chat.mainloop()

    def analyze_response(self, response):
        if(response == 'concedido'):
            self.chat()
        elif(response == 'denegado'):
            print('No hay acceso')
    
    def send_data(self, *args):
        pack_of_data = []
        for data in args:
            pack_of_data.append(data)
        pack_of_data = pickle.dumps(pack_of_data)
        print(pack_of_data)
        client.send(pack_of_data)
        res = client.recv(1024).decode()
        self.analyze_response(res)

    def send_file(self):
        pass
    
    def create_user(self):
        register = tk.Toplevel(self.master)
        register.title("Cha Cha Chat me - Registro de usuario") 
        icon = tk.PhotoImage(master=register, file = 'images/chat.png')
        register.iconphoto(False, icon)

    
        tk.Label(register, text ="Registro de usuario :)").grid(row = 0, column = 0, sticky = "W", pady = 2)
        tk.Label(register, text = 'Nombre: ', font=("Verdana", 13)).grid(row = 1, column = 0, sticky = "W", pady = 2)
        tk.Label(register, text = 'Nickname: ', font=("Verdana", 13)).grid(row = 2, column = 0, sticky = "W", pady = 2)
        tk.Label(register, text = 'Contraseña: ', font=("Verdana", 13)).grid(row = 3, column = 0, sticky = "W", pady = 2)

        name = tk.Entry(register)
        user = tk.Entry(register)
        password = tk.Entry(register, show="*")

        name.grid(row = 1, column = 1, pady = 2) 
        user.grid(row = 2, column = 1, pady = 2) 
        password.grid(row = 3, column = 1, pady = 2) 

        regis = tk.Button(register, text='Registrarme')
        regis.bind("<Button-1>", lambda e: [self.send_data(name.get(), user.get(), password.get()), register.destroy()])
        regis.grid(row = 4, column = 1, pady = 3)

    def create_widgets_login(self):
        self.master.title("Cha Cha Chat me - Inicio de sesión")
        icon = tk.PhotoImage(file = 'images/chat.png')
        self.master.iconphoto(False, icon)

        self.label_user_name = tk.Label(self, text = 'Nombre de usuario: ', font=("Verdana", 13))
        self.label_password = tk.Label(self, text = 'Contraseña: ', font=("Verdana", 13))

        self.user_name_entry = tk.Entry(self)
        self.password_entry = tk.Entry(self, show="*")

        self.label_user_name.grid(row=0 , sticky="E")
        self.label_password.grid(row=1, sticky="E")
        self.user_name_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        self.validating = tk.Button(self, text = "Ingresar", fg="red")
        self.validating.bind("<Button-1>", lambda e: self.send_data(self.user_name_entry.get(), self.password_entry.get())) 
        self.validating.grid(columnspan=4)

        self.validating = tk.Button(self, text = "Crear una nueva cuenta", fg="green", command = self.create_user)
        self.validating.grid(columnspan=4)

        self.pack()

if __name__ == "__main__":
    host = "localhost"
    port = 5001
    client = s.socket(s.AF_INET, s.SOCK_STREAM)
    try:
        client.connect((host, port)) 
    except:
        mb.showerror(title='Error de conexión', message='Hay un problema con la conexión')

    print("[+] Conexion establecida.")
    print(f"[+] Conectandose a {host}:{port}")

    if True:
        root = tk.Tk()
        # Gets both half the screen width/height and window width/height
        positionRight = int(root.winfo_screenwidth()/2 - root.winfo_reqwidth()/2)
        positionDown = int(root.winfo_screenheight()/2 - root.winfo_reqheight()/2)
    
        # Positions the window in the center of the page.
        root.geometry("+{}+{}".format(positionRight, positionDown))

        app = Cliente(master=root)
        app.mainloop()
    else:
        print('Adios')

    client.close()