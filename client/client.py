import socket
import sys
import threading
import os
import pickle
import time

buff_size = 65535
HOST = '127.0.0.1'
PORT = 5000

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((HOST, PORT))
    
class Account:
    def __init__ (self, id, name):
        self.id = id
        self.name = name
        self.friend = set()

    def get_friendlist(self):
        return self.friend

def clear():
    if os.name == 'nt':
        _ = system('cls')
    else:
        _ = os.system('clear')

def header_page():
    clear()
    print('Welcome to Esaiyy Chat')
    print('==============================')

def register(status):
    try:
        header_page()
        print('Register an account\n')
        print(status, end='')

        id = input('Enter username: ')
        name = input('Enter your name: ')
        newAccount = Account(id, name)

        registerRequest = pickle.dumps(('register', newAccount))
        socket_client.send(registerRequest)
        response = socket_client.recv(buff_size)
        response = pickle.loads(response)

        if response[0] == 'failed':
            register('Account is already Exist\n')
        else:
            dasboard('Account Created, you\'re login now\n', response[1])
        return
    except KeyboardInterrupt:
        welcome_page()

def helper():
    print('a')
    return

def friendlist():
    request = pickle.dumps(('friendlist',))
    socket_client.send(request)
    return

def chat():
    print('c')
    return

def addfriend():
    user_id = input('add user id : ')
    request = pickle.dumps(('addfriend', user_id))
    socket_client.send(request)
    return

def sendfile():
    print('e')
    return

def commandError():
    print('Command not found')

def commandSwitch(args):
    commandAvailable = {
        'help' : helper,
        'friendlist' : friendlist,
        'addfriend' : addfriend,
        'chat' : chat,
        'sendfile' : sendfile,
    }
    return commandAvailable.get(args, commandError)()

def read_message():
    while True:
        response = socket_client.recv(buff_size)
        response = pickle.loads(response)

        if response[0] == 'addfriend':
            if response[1] == 'success':
                print(response[2].id + ' now added to friendlist')
            else:
                print('Cannot add user!')
        
        elif response[0] == 'friendlist':
            print('Your friend : \n===========')
            for user in response[1]:
                print(user.id + ' | ' + user.name)

    return

def dasboard(status, myAccount):
    header_page()
    print(status, end='')
    print('Hello, ' + myAccount.name)

    thread = threading.Thread(target=read_message)
    thread.start()

    try:
        while True:
            command = input('>>> ')
            commandSwitch(command)
    except KeyboardInterrupt:
        socket_client.close()
        return

def login(status):
    try:
        header_page()
        print('Login\n')
        print(status, end='')

        id = input('Enter username: ')
        loginRequest = pickle.dumps(('login', id))
        socket_client.send(loginRequest)
        response = socket_client.recv(buff_size)
        response = pickle.loads(response)

        if response[0] == 'failed':
            login('Account is not Exist or Already login\n')
        else:
            dasboard('Login success\n', response[1])
        return
    except KeyboardInterrupt:
        welcome_page()

def welcome_page():
    try:
        header_page()
        status = ''
        islogin = input('Have an account? (y/n) : ')
        if islogin == 'n':
            register(status)
        elif islogin == 'y':
            login(status)
        else:
            print('Byee!!')
    except KeyboardInterrupt:
        sys.exit()

def main():  
    welcome_page()

if __name__ == '__main__':
    main()