import select
import socket

MAX_MSG_LENGTH = 1024
SERVER_PORT = 55554
SERVER_IP = "0.0.0.0"

server_socket = socket.socket()
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("server is running")

client_sockets = []
msg_to_send = []


def print_client_socket(cl_soc):
    for c in cl_soc:
        print("\t", c.getpeername())


while True:

    rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
    for s in rlist:
        if s is server_socket:
            connection, client_address = s.accept()
            print("new client", client_address)
            client_sockets.append(connection)
            print_client_socket(client_sockets)
        else:
            print("data from existing client ")
            data = s.recv(MAX_MSG_LENGTH).decode()
            if data == "":
                print("connection close ")
                client_sockets.remove(s)
                s.close()
                print_client_socket(client_sockets)
            else:
                # print(data)
                msg_to_send.append((s, data))
        for m in msg_to_send:
            soc, dat = m
            if soc in wlist:
                s.send(dat.encode())
                msg_to_send.remove(m)
