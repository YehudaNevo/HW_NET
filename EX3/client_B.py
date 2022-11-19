import socket
import protocol_A


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol_A.PORT))

    while True:
        user_input = input("Enter command\n")

        # sand the cmd
        my_socket.send( (protocol_A.create_msg(user_input)).encode() )
        if user_input =="EXIT":
            break
        #  accept the ans
        data = protocol_A.get_msg(my_socket)
        print(data)

    print("Closing\n")
    my_socket.close()


if __name__ == "__main__":
    main()
