
LENGTH_FIELD_SIZE = 4
PORT = 8892

def check_cmd(data):
    return True
    #return data in ["TIME", "HELLO", "RAND", "EXIT"]


def create_msg(data):
    size = str(len(data)).zfill(4)
    return size + data


def get_msg(my_socket):
    size = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if size.isnumeric():
        data = my_socket.recv(int(size)).decode()
        if check_cmd(data):
            return  data
        return  "Please follow the protocol cmd "
    return  "ERR didnt get in the correct format"


