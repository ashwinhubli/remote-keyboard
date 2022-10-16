from email import message
from http import client, server
from ipaddress import ip_address
import socket
from  threading import Thread
from pynput.mouse import Button, Controller
from remote_keyboard import IP_ADDRESS
from screeninfo import get_monitors
from pynput.keyboard import Key, Controller

SERVER = None
PORT = 8000

IP_ADDRESS= "192.168.29.214"

screen_width = None
screen_height = None

keyboard = Controller()

def acceptConnections():
    global SERVER
    while True:
        client_socket,addr = SERVER.accept()
        print(f"Connection Established With {client_socket}:{addr}")
        thread = Thread(target=receiveMsg,args=client_socket)
        thread.start()

def getDeviceSize():
    global screen_width
    global screen_height
    for m in get_monitors():
        screen_width = int(str(m).split(",")[2].strip().split('width=')[1])
        screen_height = int(str(m).split(",")[3].strip().split('height=')[1])

def receiveMsg(client_socket):
    global keyboard
    while True:
        try:
            msg = client_socket.recv(2048).decode()
            if(msg):
                keyboard.press(msg)
                keyboard.release(msg)
                print(msg)

        except Exception as error:
            pass
        
def setup():
    print("\n\t\t\t\t\t*** Welcome To Remote Keyboard ***\n")
    global SERVER
    global PORT
    global ip_address
    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS,PORT))
    SERVER.listen(10)
    print("\t\t\t\tSERVER IS WAITING FOR INCOMING CONNECTIONS...\n")
    getDeviceSize()
    acceptConnections()

setup()