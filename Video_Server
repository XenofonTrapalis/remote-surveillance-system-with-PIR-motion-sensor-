import socket
import os
from subprocess import Popen, PIPE
#import struct
#from PIL import Image


server_address = ('0.0.0.0', 10000)


def my_server():
    #wait for client to connect
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM)as server_socket:
        print ('Server Started waiting for client to connect')
        server_socket.bind(server_address)
        server_socket.listen(5) #it can listen up to 5 devices
        connection = server_socket.accept()[0].makefile('rb') 
        
        
        try:
            #when a motion detected from the client the connection established and open run the vlc player for the
            #streaming
            cmdline = (os.path.join('C:/','Program Files (x86)','VideoLAN','VLC','vlc.exe'), '--demux', 'h264', '-')
            player = Popen(cmdline, stdin=PIPE)
            print('connection established')
    
            while True:

                data = connection.read(1024)
                #when the server doesn't receive any data it breaks the connection with the client
                if not data:
                    break
                player.stdin.write(data)


        finally:
            connection.close()
            server_socket.close()
            player.terminate()

if __name__ == '__main__':
    while 1:
        my_server()
