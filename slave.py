from socket_communicate.socket_comm import worker_init
from socket_communicate.socket_comm import wrap_msg


def on_receive(s, msg):
    print msg
    s.send(wrap_msg("received"))


def on_conn(s, msg):
    print msg

worker_init(on_receive, "127.0.0.1", 9999, on_conn)
