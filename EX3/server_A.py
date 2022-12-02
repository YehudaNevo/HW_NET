import select
import socket
import protocol_A

# INIT
SERVER_IP = "0.0.0.0"
server_socket = socket.socket()
server_socket.bind((SERVER_IP, protocol_A.PORT))
server_socket.listen()
print("server is running")

client_sockets = []
msg_to_send = []
client_dict = {}
count_no_name_client = 0


def debug(str):
    print("Debug: " + str)


# set name , insert or delete . insert false if fail
def set_name(dict, port, name, insert=True):
    if insert:
        if name in dict.values():
            return False
        dict[port] = name
        return True
    else:  # delete name from dict
        print(port)
        if port in dict.keys():
            del dict[port]
            return True
        return False


# send the clients names
def send_names(soc):
    msg = "Names : "
    for key, value in client_dict.items():
        msg += ', ' + value

    msg_to_send.append((soc, protocol_A.create_msg(msg)))


def print_client_socket(cl_soc):  # for debugging
    print("clients:")
    for c in cl_soc:
        print("\t", c.getpeername(), ",")


# insert new name , if fail return false and please choose diff name
def insert_name(soc, data):
    name = data[5:]
    valid = set_name(client_dict, soc.getpeername()[1], name)
    if valid:
        msg_to_send.append((soc, protocol_A.create_msg("Set your name to " + name)))
        return True
    else:
        msg_to_send.append((soc, protocol_A.create_msg("please choose diff name")))
        return False


def get_key(val):
    for key, value in client_dict.items():
        if val == value:
            return key

    return "key doesn't exist"


def find_sock_by_port(port):
    for s in client_sockets:
        if s.getpeername()[1] == port:
            return s
    return "NOT FOUND"


# sand msgs between clients , can sand to your self , if client not exist  - do nothing
def send_data(soc, data):
    port_from = soc.getpeername()[1]
    name_from = client_dict[port_from]

    lst = data.split(" ")
    to = lst[1]
    msg = str(name_from) + " sent: "
    for item in lst[2:]:
        msg += " " + item

    port_to = get_key(to)
    if port_to == "key doesn't exist":
        return

    soc_to = find_sock_by_port(port_to)

    msg_to_send.append((soc_to, protocol_A.create_msg(msg)))


while True:

    read_list, write_list, x_list = select.select([server_socket] + client_sockets, client_sockets, [], 1)

    for soc in read_list:
        # new client
        if soc is server_socket:
            connection, client_address = soc.accept()
            client_sockets.append(connection)
            client_dict[client_address[1]] = 'No name yet #' + str(count_no_name_client)
            count_no_name_client += 1

        #  existing client
        else:
            ans, data = protocol_A.get_msg(soc)
            if data != "":
                if data[0:4] == "NAME":
                    insert_name(soc, data)
                elif data[0:9] == "GET NAMES":
                    send_names(soc)
                elif data[0:3] == "MSG":
                    send_data(soc, data)
                elif data == "EXIT":
                    pass

            else:  # client leave...
                print("connection close ")
                set_name(client_dict, soc.getpeername()[1], "", False)
                client_sockets.remove(soc)
                soc.close()

    # loop to sand msgs
    for m in msg_to_send:
        soc, dat = m
        if soc in write_list:
            soc.send(dat.encode())
            msg_to_send.remove(m)
