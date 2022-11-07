"""EX 2.6 protocol implementation
   Author:
   Date:
   Possible client commands:
   NUMBER - server should reply with a random number, 0-99
   HELLO - server should reply with the server's name, anything you want
   TIME - server should reply with time and date
   EXIT - server should send acknowledge and quit
"""

LENGTH_FIELD_SIZE = 2
PORT = 8821
def check_cmd(data):
    return data in ["TIME", "WHORU", "RAND", "EXIT"]


def create_msg(data):
    size = str(len(data)).zfill(2)
    return size + data


def get_msg(my_socket):
    size = my_socket.recv(2).decode()
    if size.isnumeric():
        data = my_socket.recv(int(size)).decode()
        if check_cmd(data):
            return True, data
        return False, "Please follow the protocol cmd "
    return False, "ERR didnt get in the correct format"


