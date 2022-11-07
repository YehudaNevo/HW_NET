"""EX 2.6 client implementation
   Author:
   Date:
   Possible client commands defined in protocol.py
"""

import socket
import protocol


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    while True:
        user_input = input("Enter command\n")
        if user_input == "EXIT":
            my_socket.send(protocol.create_msg(user_input).encode())
            break
        else:
            my_socket.send(protocol.create_msg(user_input).encode())
            data = my_socket.recv(1024).decode()
            print(data)

        # 1. Add length field ("HELLO" -> "04HELLO")
        # 2. Send it to the server
        # 3. Get server's response
        # 4. If server's response is valid, print it
        # 5. If command is EXIT, break from while loop

    print("Closing\n")
    # Close socket
    my_socket.close()


if __name__ == "__main__":
    main()
