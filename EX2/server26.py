"""EX 2.6 server implementation
   Author: Yehuda Nevo
   Date: 05/11/22
   Possible client commands defined in protocol.py
"""

from datetime import datetime
from datetime import date

from random import randrange


import socket
import protocol


def create_server_rsp(cmd):
    if cmd == "TIME":
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        return current_time +"  "+  d1
    elif cmd == "HELLO":
        return "Yehuda"
    elif cmd == "RAND":
        A = randrange(100)
        return str(A)
    elif cmd == "EXIT":
        return "EXIT"
    else:
        return "ERROR"


def main():
    server_socket = socket.socket()
    server_socket.bind(("0.0.0.0", protocol.PORT))  # listen over all interfaces 0000 nic or 127001 etc ...
    server_socket.listen()
    print("server is running")
    # Create client socket for incoming connection
    (client_socket, client_address) = server_socket.accept()
    print("connect")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)

        if valid_msg:
            response = create_server_rsp(cmd)
        else:
            response = cmd
        # client_socket.recv(1024)  # Attempt to empty the socket from possible garbage

        # Send response to the client
        client_socket.send(protocol.create_msg(response).encode())

        # If EXIT command, break from loop
        if cmd == "EXIT":
            break

    print("Closing\n")
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
