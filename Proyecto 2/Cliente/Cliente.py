import tkinter as tk
from tkinter import messagebox as mb
import socket as s
import sys

class Login(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
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
        self.validating["command"] = self.validate
        self.validating.grid(columnspan=4)

        self.validating = tk.Button(self, text = "Crear una nueva cuenta", fg="green")
        self.validating["command"] = self.create_user
        self.validating.grid(columnspan=4)

        self.pack()
        
    def validate(self, event):
        print("Hi. The current entry content is:", self.user_name_entry.get())
    
    def create_user(self, event):
        #Crear usuario aquí 
        print("Creando usuario")
        pass

  #  mb.showinfo(title='Estado de conexión',
#        message='Conexión establecida al servidor')



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


    root = tk.Tk()
    # Gets both half the screen width/height and window width/height
    positionRight = int(root.winfo_screenwidth()/2 - root.winfo_reqwidth()/2)
    positionDown = int(root.winfo_screenheight()/2 - root.winfo_reqheight()/2)
 
    # Positions the window in the center of the page.
    root.geometry("+{}+{}".format(positionRight, positionDown))

    app = Login(master=root)
    app.mainloop()