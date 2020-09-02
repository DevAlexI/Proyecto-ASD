import socket
import os
import sys
import struct

def sock_client_image():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((socket.gethostname(), 1234))

        except socket.error as msg:
            print(msg)
            print(sys.exit(1))
        filepath = input('input the file:')
        fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding ='utf-8'), os.stat(filepath).st_size) # packages xxx. JPG in 128sq format
        print(fhead)
        s.send(fhead)

        fp = open (filepath,'rb') # Open the picture to be transmitted
        while True:
            data = fp.read(1024) # Read in picture data
            if not data:
                print('{0} enviado...'.format(filepath))
                break
            s.send(data)  
        s.close()
        # Brea # Loop Sending
   
if __name__ == '__main__':
    sock_client_image()