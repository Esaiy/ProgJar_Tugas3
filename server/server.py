import socket
import pickle
import threading

class AccountManager():
    def __init__ (self):
        self.account = {}
        self.online = {}
    def add_account(self, account):
        check = self.account.get(account.id, None)
        if check == None:
            self.account[account.id] = account
            return self.account[account.id]
        else:
            return b'failed'
    def check_account(self, username):
        return self.account.get(username, 'failed')


class Account:
    def __init__ (self, id, name):
        self.id = id
        self.name = name

def read_message(socket_client, address_client):
    while True:
        request = socket_client.recv(buff_size)
        if request:
            print(request)
            data = pickle.loads(request)

            if data[0] == 'register' :
                response = accountManager.add_account(data[1])
                socket_client.send(pickle.dumps(response))

            elif data[0] == 'login' :
                response = accountManager.check_account(data[1])
                socket_client.send(pickle.dumps(response))
        else:
            break
    return

buff_size = 65535
HOST = '0.0.0.0'
PORT = 5000
clients = {}
accountManager = AccountManager()

def main():
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((HOST, PORT))
    socket_server.listen(5)
    
    while True:
        socket_client, address_client = socket_server.accept()

        thread_client = threading.Thread(target=read_message, args=(socket_client, address_client))
        thread_client.start()

if __name__ == '__main__':
    main()