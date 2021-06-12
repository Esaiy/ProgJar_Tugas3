import socket
import pickle
import threading

class AccountManager():
    def __init__ (self):
        self.account = {}
        self.online = {}
    def check_account(self, id):
        return self.account.get(id, None)

    def add_account(self, account):
        check = self.check_account(account.id)
        if check == None:
            self.account[account.id] = account
            return self.account[account.id]
        else:
            return None

    def check_online(self, account):
        return self.online.get(account.id, None)
        
    def add_online(self, account, socket_client, address_client):
        if not(self.check_online(account)):
            self.online[account.id] = (socket_client, address_client)
            return account
        return None
        
    def set_disconnected(self, account):
        print("Account " + account.id + " disconnected")
        del self.online[account.id]


class Account:
    def __init__ (self, id, name):
        self.id = id
        self.name = name
        self.friend = []

def commandHandler(socket_client, address_client):
    currentAccount = None
    while True:
        request = socket_client.recv(buff_size)
        if request:
            print(request)
            data = pickle.loads(request)

            if data[0] == 'register' :
                currentAccount = accountManager.add_account(data[1])
                response = dict()
                if currentAccount:
                    response[0] = 'success'
                    response[1] = currentAccount
                    accountManager.add_online(currentAccount, socket_client, address_client)
                else:
                    response[0] = 'failed'
                
                print(response)
                socket_client.send(pickle.dumps(response))
                
            elif data[0] == 'login' :
                currentAccount = accountManager.check_account(data[1])
                response = dict()
                if currentAccount and not(accountManager.check_online(currentAccount)):
                    response[0] = 'success'
                    response[1] = currentAccount
                    accountManager.add_online(currentAccount, socket_client, address_client)
                else:
                    response[0] = 'failed'
                    currentAccount = None
                
                print(response)
                socket_client.send(pickle.dumps(response))

            

        else:
            if currentAccount:
                accountManager.set_disconnected(currentAccount)
            break
    return

def new_func():
    return None

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

        thread_client = threading.Thread(target=commandHandler, args=(socket_client, address_client))
        thread_client.start()

if __name__ == '__main__':
    main()