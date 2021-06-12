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
        if type(account) == Account:
            return self.online.get(account.id, None)
        elif type(account) == str:
            return self.online.get(account, None)
        
    def add_online(self, account, socket_client, address_client):
        if not(self.check_online(account)):
            self.online[account.id] = (socket_client, address_client)
            return account
        return None
        
    def set_disconnected(self, account):
        print("Account " + account.id + " disconnected")
        del self.online[account.id]

class Account:
    def __init__ (self, id, name, password):
        self.id = id
        self.name = name
        self.password = password
        self.friend = set()
    def get_friendlist(self):
        return self.friend
    def check_friend(self, account):
        return account in self.friend

def commandHandler(socket_client, address_client):
    currentAccount = None
    while True:
        request = socket_client.recv(buff_size)
        if request:
            data = pickle.loads(request)

            if data[0] == 'register' :
                currentAccount = accountManager.add_account(data[1])
                response = dict()
                if currentAccount:
                    response[0] = 'success'
                    response[1] = currentAccount
                    print("user {} has been created".format(currentAccount.id))
                    accountManager.add_online(currentAccount, socket_client, address_client)
                else:
                    response[0] = 'failed'
                socket_client.send(pickle.dumps(response))
                
            elif data[0] == 'login' :
                currentAccount = accountManager.check_account(data[1])
                response = dict()
                if currentAccount and not(accountManager.check_online(currentAccount)) and data[2] == currentAccount.password:
                    response[0] = 'success'
                    response[1] = currentAccount
                    print("{} is online".format(currentAccount.id))
                    accountManager.add_online(currentAccount, socket_client, address_client)
                else:
                    response[0] = 'failed'
                    print("Failed login for user {}".format(data[1]))
                    currentAccount = None    
                socket_client.send(pickle.dumps(response))

            elif data[0] == 'friendlist':
                response = dict()
                response[0] = data[0]
                response[1] = currentAccount.get_friendlist()
                print('Request friend list for user {}'.format(currentAccount.id))
                socket_client.send(pickle.dumps(response))

            elif data[0] == 'addfriend':
                userTarget = accountManager.check_account(data[1])
                response = dict()
                response[0] = data[0]            
                if userTarget and not(userTarget == currentAccount):
                    currentAccount.friend.add(userTarget.id)
                    response[1] = 'success'
                    response[2] = userTarget
                else:
                    response[1] = 'failed'
                socket_client.send(pickle.dumps(response))

            elif data[0] == 'chat' :
                requestData = data[1]
                destination = requestData[0]
                message = requestData[1]
                
                response = dict()
                response[0] = data[0]
                if destination == 'bcast' : 
                    send_broadcast(currentAccount, message, socket_client)
                else:
                    send_message(currentAccount, destination, message, socket_client) 
            
        else:
            if currentAccount:
                accountManager.set_disconnected(currentAccount)
            break
    return

def send_broadcast(currentAccount, message, socket_client):
    for destination in currentAccount.friend:
        send_message(currentAccount, destination, message, socket_client)
    return

def send_message(currentAccount, destination, message, socket_client):
    response = dict()
    response[0] = 'chat'
    if not(destination == currentAccount.id):
        if(currentAccount.check_friend(destination)):
            checkDestination = accountManager.check_online(destination)
            if checkDestination:
                dest_socket, _ = checkDestination
                response[1] = 'success'
                response[2] = (currentAccount.id, currentAccount.name, message)
                dest_socket.send(pickle.dumps(response))
                return
            else:
                response[2] = destination + ' is not online'
        else:
            response[2] = destination + ' is not your friend'
    else:
        response[2] = 'Cannot sent message to yourself'
    
    response[1] = 'failed'
    socket_client.send(pickle.dumps(response))
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

        thread_client = threading.Thread(target=commandHandler, args=(socket_client, address_client))
        thread_client.start()

if __name__ == '__main__':
    main()