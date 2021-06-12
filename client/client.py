import socket
import sys
import threading
import os
import pickle
from getpass import getpass

buff_size = 65535
HOST = '127.0.0.1'
PORT = 5000

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((HOST, PORT))
    
class Account:
    def __init__ (self, id, name, password):
        self.id = id
        self.name = name
        self.password = password
        self.friend = set()

def clear(args):
    if os.name == 'nt':
        _ = system('cls')
    else:
        _ = os.system('clear')

def header_page():
    clear('')
    print('Welcome to Esaiyy Chat')
    print('==============================')

def helper(args):
    print('''Manual for Esaiyy Chat\nCommand:
    help - show all command available
    add - add user to friend list
        add [user] - add user to your friend
    friend - show my friend list
    chat - chat to specific user or broadcast
        chat [user] - chat to account user
        chat [bcast] - broadcast chat
    send - send a file to friend
    ''')
    return

def friendlist(args):
    request = pickle.dumps(('friendlist',))
    socket_client.send(request)
    return

def chat(args):
    data = dict()
    data[0] = args[1] if args[1] else input('<Server>: Send to (use [user_id] or bcast) :\n')
    data[1] = input('<Server>: Type your message :\n')

    request = pickle.dumps(('chat', data))
    socket_client.send(request)    
    return

def addfriend(args):
    user_id = args[1] if args[1] else input('<Server>: Add Friend ID :\n')
    request = pickle.dumps(('addfriend', user_id))
    socket_client.send(request)
    return

def sendfile(args):

    return

def commandError():
    print('<Server>: Command Not Found')

def commandSwitch(args):
    commandAvailable = {
        'help' : helper,
        'friend' : friendlist,
        'add' : addfriend,
        'chat' : chat,
        'send' : sendfile,
        'clear' : clear
    }
    args = args.split(' ')
    commandAvailable.get(args[0], commandError)(args)

def read_message():
    while True:
        response = socket_client.recv(buff_size)
        response = pickle.loads(response)

        if response[0] == 'addfriend':
            if response[1] == 'success':
                print('<Server>: {} now added to your friend list'.format(response[2].id))
            else:
                print('<Server>: Cannot add user!')
            print()

        elif response[0] == 'friendlist':
            print('<Server>:\n== Your Friend ==')
            if response[1]:
                for idx, user in enumerate(response[1]):
                    print('  {}. {}'.format(idx + 1, user))
            else:
                print('No one in your friend list') 
            print()             
        
        elif response[0] == 'chat':
            if response[1] == 'failed':
                print("<Server>: {}".format(response[2]))
            else:
                senderid, sendername, message = response[2]
                print("<{}> {}: {}".format(senderid, sendername, message))
            print()

def dasboard(status, myAccount):
    header_page()
    print(status, end='')
    print('Hello, ' + myAccount.name + '\n')
    print('Type "help" to see all available command \n')
    
    thread = threading.Thread(target=read_message)
    thread.daemon = True
    thread.start()

    try:
        while True:
            command = input()
            commandSwitch(command)
    except KeyboardInterrupt:
        socket_client.close()
        sys.exit()

def register(status):
    try:
        header_page()
        print('Register an account\n')
        print(status, end='')

        id = input('Enter username: ')
        name = input('Enter your name: ')
        password = getpass('Enter password: ')
        newAccount = Account(id, name, password)

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
        return welcome_page()

def login(status):
    try:
        header_page()
        print('Login to chat\n')
        print(status, end='')

        id = input('Enter username: ')
        password = getpass('Enter password: ')
        
        loginRequest = pickle.dumps(('login', id, password))
        socket_client.send(loginRequest)
        response = socket_client.recv(buff_size)
        response = pickle.loads(response)

        if response[0] == 'failed':
            login('Login Failed, please check your credential\n')
        else:
            dasboard('Login success\n', response[1])
        return
    except KeyboardInterrupt:
        return welcome_page()
        
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