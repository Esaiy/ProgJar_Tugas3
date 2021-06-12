import socket
import sys
import threading

buff_size = 65535
HOST = '127.0.0.1'
PORT = 5000

CURSOR_UP_ONE = '\x1b[1A'

def read_message(socket_client):
    while True:
        data = socket_client.recv(buff_size)
        if len(data) == 0:
            break
        print(CURSOR_UP_ONE + '\n' + data.decode('utf-8'))

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((HOST, PORT))
print(sys.argv[1])
socket_client.send(sys.argv[1].encode('utf-8'))
    
thread_client = threading.Thread(target=read_message, args=(socket_client, ))
thread_client.start()

while True:
    dest = input("Username tujuan atau bcast untuk broadcast: ")
    message = input("Masukkan pesan: ")

    if message == 'exit':
        socket_client.close()
        break
    
    data = dest + '|' + message
    socket_client.send(data.encode('utf-8'))