from socket_communicate.socket_comm import send_msg


def on_reply(s, msg):
    print msg


send_msg("hello", "127.0.0.1", 9999, on_reply)