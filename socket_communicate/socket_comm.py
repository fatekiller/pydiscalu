import socket, threading


def send_job(job, port, worker_address, on_reply, on_finish):
    s = socket.socket()
    s.connect((worker_address, port))


def __target__(job, port, worker_address, on_reply, on_finish):
    threading.Thread(target=send_job)
    s = socket.socket()
    s.connect((worker_address, port))
