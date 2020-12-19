import socket
import threading

#Creating an INET , STREAMing socket
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
IP=socket.gethostbyname(socket.gethostname())
PORT=1234
ADDR=(IP,PORT)

MSG_SIZE=32
FORMAT='utf-8'
sending=False
printing=False
MsgList=[]
def send(username):
    global sending,printing
    while True:
        if printing:
            continue
        sending=True
        msg=input(f"{username}:=>")
        sending=False
        msg=(f"{len(msg):<{MSG_SIZE}}"+msg).encode(FORMAT)
        client.send(msg)
def recv():
    while True:
        msglen=int(client.recv(MSG_SIZE).decode(FORMAT))
        if msglen:
            message=client.recv(msglen).decode(FORMAT)
            MsgList.append(message)
def printMsg():
    global MsgList,sending,printing
    while True:
        if sending:
            continue
        if len(MsgList):
            printing=True
            print(MsgList[0])
            MsgList.pop(0)
            printing=False
def start_client():
    username=input("Enter Your Username:=>")
    uname=username.encode(FORMAT)
    client.connect(ADDR)
    client.send(uname)
    threading.Thread(target=printMsg).start()
    sendThread=threading.Thread(target=send,args=(username))
    sendThread.start()
    recvThread=threading.Thread(target=recv)
    recvThread.start()

if __name__ == "__main__":
    start_client()
