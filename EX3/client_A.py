import socket
import os
import select
import msvcrt
import protocol_A


clear = lambda: os.system('cls')


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol_A.PORT))
    user_cmd = ""
    want_to_sand = False
    clear()
    print("please enter cmd:")

    while True:
        read_list, write_list, x_list = select.select([my_socket, ], [my_socket, ], [], 1)

        # read input , unblocking
        if msvcrt.kbhit():
            try:
                c = msvcrt.getch().decode("ASCII")
                print(c, end="", flush=True)
                if c == '\r':
                    want_to_sand = True
                else:
                    user_cmd += c
            except UnicodeDecodeError:
                clear()
                user_cmd = ''
                print("please enter command")

        if user_cmd == "EXIT" and want_to_sand:
            break

        if want_to_sand:
            my_socket.send((protocol_A.create_msg(user_cmd)).encode())
            user_cmd = ""
            print()
            want_to_sand = False

        for soc in read_list:
            ans, data = protocol_A.get_msg(soc)
            if ans:
                print(data)

    print("Closing\n")
    my_socket.close()


if __name__ == "__main__":
    main()
