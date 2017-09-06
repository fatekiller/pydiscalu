# -*- coding:utf-8 -*-
import socket
import threading as tr
from util.utils import json2obj, obj2json

sockets = dict()


def __receive_msg__(s, call):
    buffer_msg = []
    while True:
        data = s.recv(512)
        if data:
            buffer_msg.append(data)
            if data.__contains__(':end'):
                call(s, ''.join(buffer_msg))
                return
            else:
                continue


'''
一次通信结束不注销监听器
'''


def _receive_msg_no_exit_(s, call, is_alive=None):
    buffer_msg = []
    condition = True
    if is_alive:
        condition = is_alive()
    while condition:
        data = s.recv(512)
        if data:
            buffer_msg.append(data)
            if data.__contains__(':end'):
                call(s, ''.join(buffer_msg))
                buffer_msg = []
            else:
                continue


'''
msg:要发送的消息
port:端口号
address:接收方ip
on_reply:接收回调
'''


def init_s_conn(msg, worker, on_reply=None):
    if worker.address+str(worker.port) in sockets:
        s = sockets[worker.address+str(worker.port)]
    else:
        s = socket.socket()
        s.connect((worker.address, int(worker.port)))
    send_http_msg(Conn(on_reply, s), msg)


def send_http_msg(conn, msg):
    conn.conn_socket.send(msg)

    def server_receive():
        __receive_msg__(conn.conn_socket, conn.on_reply)
    # 开始一个本次会话的消息监听线程
    msg_listener = tr.Thread(target=server_receive)
    msg_listener.start()


def send_msg(conn, msg):
    conn.conn_socket.send(msg)

    def server_receive():
        _receive_msg_no_exit_(conn.conn_socket, conn.on_reply)
    # 开始一个本次会话的消息监听线程
    msg_listener = tr.Thread(target=server_receive)
    msg_listener.start()

'''
为worker初始化一个socket并监听上面的消息
on_receive 接收消息的回调函数
ip 地址
port 端口
on_conn 连接回调
'''


def worker_init(on_receive, ip, port, on_conn, is_alive=None):
    worker_socket = socket.socket()
    worker_socket.bind((ip, port))
    worker_socket.listen(10)

    def worker_receive():
        server, address = worker_socket.accept()
        on_conn(server, address)
        _receive_msg_no_exit_(server, on_receive, is_alive=is_alive)
    tr.Thread(target=worker_receive).start()


'''
msg_type 0:master连接worker发送hello校验连接状态
msg_type 1:worker确认连接成功建立，发送connected
msg_type 2:master发送job给worker
msg_type 3:worker发送job结果给master
msg_type 4:worker接收完任务的反馈

status 0:成功消息 默认值
status 1:错误报告消息

'''


class Msg(object):
    MSG_HELLO = 0
    MSG_CONNECTED = 1
    MSG_JOB = 2
    MSG_RESULT = 3
    MSG_JOB_REPLY = 4

    STATUS_SUCCESS = 0
    STATUS_ERROR = 1

    def __init__(self, msg_type=None, content=None, status=STATUS_SUCCESS):
        self.msg_type = msg_type
        self.content = content
        self.status = status

    @staticmethod
    def get_msg(json_str):
        return json2obj(json_str[0:-4])

    def get_json_msg(self):
        return obj2json(self)+':end'


class Conn(object):
    def __init__(self, on_reply=None, conn_socket=None):
        self.conn_socket = conn_socket
        self.on_reply = on_reply
