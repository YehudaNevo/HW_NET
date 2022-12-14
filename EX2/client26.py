
import socket
import protocol


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", 55554))

    while True:
        user_input = input("Enter command\n")



        my_socket.send(protocol.create_msg(user_input).encode())

        size = my_socket.recv(2).decode()
        data = my_socket.recv(int(size)).decode()

        if data == "EXIT":
            break
        print(data)


    print("Closing\n")
    # Close socket
    my_socket.close()


if __name__ == "__main__":
    main()
