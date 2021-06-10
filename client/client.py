import socket
import sys
import threading
import os
import pickle

buff_size = 65535
HOST = '127.0.0.1'
PORT = 5000

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((HOST, PORT))

class Account:
    def __init__ (self, id, name):
        self.id = id
        self.name = name

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
    header_page()
    print(status, end='')

    id = input('Enter username: ')
    name = input('Enter your name: ')
    newAccount = Account(id, name)

    registerRequest = pickle.dumps(('register', newAccount))
    socket_client.send(registerRequest)
    status = socket_client.recv(buff_size)
    status = pickle.loads(status)

    print(status)
    if status == 'failed':
        register('Account is already Exist\n')
    else:
        dasboard('Account Created, you\'re login now\n', status)
    return
    
def dasboard(status, myAccount):
    header_page()
    print(status, end='')
    print('Hello, ' + myAccount.name)

    socket_client.close()
    return

def login(status):
    header_page()
    print(status, end='')

    id = input('Enter username: ')
    loginRequest = pickle.dumps(('login', id))
    socket_client.send(loginRequest)
    status = socket_client.recv(buff_size)
    status = pickle.loads(status)

    print(status)
    if status == 'failed':
        login('Account is not Exist\n')
    else:
        dasboard('Login success\n', status)
    return

def welcome_page():
    header_page()
    status = ''
    islogin = input('Have an account? (y/n) : ')
    if islogin == 'n':
        register(status)
    elif islogin == 'y':
        login(status)
    else:
        print('Byee!!')

def main():  
    welcome_page()

if __name__ == '__main__':
    main()