import socket
import os
import sys
import struct

def socket_service_image():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.bind(('127.0.0.1', 6666))
        s.bind((socket.gethostname(), 1234))
        s.listen(10)
    except socket.error as msg:
        print("Error de conexión:")
        print(msg)
        sys.exit(1)

    print("Esperando por cliente.....................")

    while True:
        sock, addr = s.accept()
        deal_image(sock, addr)

def deal_image(sock, addr):
    print("Aceptando conexión desde: {0}".format(addr)) 

    while True:
        fileinfo_size = struct.calcsize('128sq')
        buf = sock.recv(fileinfo_size) # receive picture name
        if buf:
            filename, filesize = struct.unpack('128sq', buf)
            fn = filename.decode().strip('\x00')
            new_filename = (os.path.join(os.getcwd(),fn))
            #sys.exit(1)
            recvd_size = 0
            fp = open(new_filename, 'wb')

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = sock.recv(1024)
                    recvd_size += len(data)
                else:
                    data = sock.recv(1024)
                    recvd_size = filesize
                fp.write(data) 
            fp.close()
        sock.close()
        break
        
if __name__ == '__main__':
    socket_service_image()