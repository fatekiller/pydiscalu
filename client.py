import socket,threading

s = socket.socket()

s.connect(('127.0.0.1', 8080))

buffer_msg = []

msg = ''


def read_type():
    global msg
    while True:
        msg = raw_input()
        s.send(msg+':end')

threading.Thread(target=read_type, name="read").start()

while True:
    data = s.recv(512)
    if data:
        buffer_msg.append(data)
        if data.__contains__(':end'):
            print ''.join(buffer_msg)[0:-4]
            buffer_msg = []
        else:
            continue

