import socket

# client

# my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP IP SOCKET
# my_socket.connect(("127.0.0.1", 8820)) # ip port
#
# my_socket.send("hello".encode())
# data = my_socket.recv(1024).decode()
# print(data)
# my_socket.close()

# servers
server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 8820)) # listen over all interfaces 0000 nic or 127001 etc ...
server_socket.listen()
print("server is running")

(client_socket,server_socket) = server_socket.accept()
print("connect")

data = client_socket.recv(1024).decode()
print("client sand " , data)

reply = "hello" + data
client_socket.send(reply.encode())
client_socket.close()
server_socket.close()




