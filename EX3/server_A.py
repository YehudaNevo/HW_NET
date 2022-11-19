import select
import socket
import protocol_A

SERVER_IP = "0.0.0.0"

server_socket = socket.socket()
server_socket.bind((SERVER_IP, protocol_A.PORT))
server_socket.listen()
print("server is running")

client_sockets = []
msg_to_send = []
client_dict = {}


def set_name(dict, port, name, insert=True):
    if insert:
        if name in dict.values():
            return False
        dict[port] = name
        return True
    else:  # delete name from dict
        if port in dict.keys():
            del dict[port]
            return True
        return False


def print_dic_for_DEBUG(dic):
    for key, value in dic.items():
        print(key, ': ', value)


def print_client_socket(cl_soc):
    print("clients:")
    for c in cl_soc:
        print("\t", c.getpeername(), ",")


def insert_name(soc, data):
    name = data[5:]
    ans = set_name(client_dict, soc.getsockname()[1], name)
    if ans:
        msg_to_send.append((soc, protocol_A.create_msg("Set your name to " + name)))
    else:
        msg_to_send.append((soc, protocol_A.create_msg("please choose diff name")))


def print_dict_exp_me(soc):
    pass


def send_data(soc, data):
    pass


while True:

    read_list, write_list, x_list = select.select([server_socket] + client_sockets, client_sockets, [])

    for soc in read_list:
        # new client
        if soc is server_socket:
            connection, client_address = soc.accept()
            print("new client", client_address)
            client_sockets.append(connection)
            client_dict[client_address[1]] = 0
            print_dic_for_DEBUG(client_dict)
        #  existing client
        else:
            data = protocol_A.get_msg(soc)

            if data == "":
                print("connection close ")
                set_name(client_dict, soc.getsockname()[1], False)
                client_sockets.remove(soc)
                soc.close()
                print_client_socket(client_sockets)
            # option = NAME , GET_NAMES , MSG DEST HELLO , EXIT
            elif data[0:4] == "NAME":
                res = insert_name(soc, data)
                print(res)
            elif data == "GET_NAMES":
                print_dict_exp_me(soc)
            elif data[0] == "MSG":
                res = send_data(soc, data)
            elif data == "EXIT":
                pass
            elif data != "":
                print("Please enter valid command")
            #  client leave

            if data != "":
                # print(data)
                msg_to_send.append((soc, protocol_A.create_msg(data)))

        # if there is msgs to sand
        for m in msg_to_send:
            sock, dat = m
            if soc in write_list:
                soc.send(dat.encode())
                msg_to_send.remove(m)
