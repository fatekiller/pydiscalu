import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('127.0.0.1', 8080))

buffer_msg = []

s.listen(50)

while True:
    client, address = s.accept()
    print address
    client.send("welcome connect:end")
    while True:
        data = client.recv(512)
        if data:
            buffer_msg.append(data)
            if data.__contains__(':end'):
                client.send(''.join(buffer_msg)[0:-4]+' from server :end')
                buffer_msg = []
            else:
                continue
