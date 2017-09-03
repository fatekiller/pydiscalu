# -*- coding:utf-8 -*-
import socket
import threading as tr

sockets = dict()


def __receive_msg__(s, call):
    buffer_msg = []
    while True:
        data = s.recv(512)
        if data:
            buffer_msg.append(data)
            if data.__contains__(':end'):
                call(s, ''.join(buffer_msg)[0:-4])
                buffer_msg = []
            else:
                continue


def wrap_msg(msg):
    return msg+":end"


'''
msg:要发送的消息
port:端口号
address:接收方ip
on_reply:接收回调
'''


def send_msg(msg, address, port, on_reply=None):
    s = None

    def server_receive():
        __receive_msg__(s, on_reply)

    if address in sockets:
        s = sockets.get(address)
    else:
        s = socket.socket()
        s.connect((address, port))
        tr.Thread(target=server_receive, name=address).start()
    s.send(wrap_msg(msg))

'''
为worker初始化一个socket并监听上面的消息
on_receive 接收消息的回调函数
ip 地址
port 端口
on_conn 连接回调
'''


def worker_init(on_receive, ip, port, on_conn):
    worker_socket = socket.socket()
    worker_socket.bind((ip, port))
    worker_socket.listen(10)

    def worker_receive():
        while True:
            server, address = worker_socket.accept()
            on_conn(server, address)
            __receive_msg__(server, on_receive)
    tr.Thread(target=worker_receive()).start()
