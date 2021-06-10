import socket
import threading

buff_size = 65535
HOST = '0.0.0.0'
PORT = 5000

def read_message(client, socket_client, address_client, username_client):
    while True:
        data = socket_client.recv(buff_size)
        if len(data) == 0:
            break

        dest, message= data.decode('utf-8').split('|')
        message = "<{}>: {}".format(username_client, message)

        if dest == 'bcast':
            send_broadcast(client, message, address_client)
        else:
            dest_socket_client = client[dest][0]
            send_message(dest_socket_client, message)
        print(data)
    
    socket_client.close()
    print('Connection closed', address_client)

def send_broadcast(clients, message, sender_address_client):
    for socket_client, address_client, _ in clients.values():
        if not (sender_address_client[0] == address_client[0] and sender_address_client[1] == address_client[1]):
            send_message(socket_client, message)

def send_message(socket_client, message):
    socket_client.send(message.encode('utf-8'))

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind((HOST, PORT))
socket_server.listen(5)

clients = {}

try:
    while True:
        socket_client, address_client = socket_server.accept()

        username_client = socket_client.recv(buff_size).decode('utf-8')
        print(username_client, 'joined')

        thread_client = threading.Thread(target=read_message, args=(clients, socket_client, address_client, username_client))
        thread_client.start()

        clients[username_client] = (socket_client, address_client, thread_client)
except KeyboardInterrupt:
    socket_server.close()