# Ex 4.4 - HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants
import re
import sys

import socket

IP = '0.0.0.0'
PORT = 80
code = "200"
SOCKET_TIMEOUT = 0.1
FIXED_RESPONSE = ""
dic_of_redirection_urls = {'/yehuda': '/index.html'}


def handle_client_request(resource, client_socket):

    if resource in dic_of_redirection_urls.keys():
        resource = dic_of_redirection_urls[resource]
        # code = "302"
    if resource == '/':
        resource = '/index.html'
    try:
        fin = open("webroot" + resource, encoding="utf8", errors='ignore')
        content = fin.read()
        fin.close()
        size = len(content)
        filetype = resource.split('.')[-1]
        response = 'HTTP/1.0 200 OK\r\n'
        response += "Content-Type: " + filetype + '\r\n'
        response += "Content-Length: " + str(size) + '\r\n\n'
        response += content
    except FileNotFoundError:
        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
    print(response)
    client_socket.send(response.encode())


# ['GET /<PATH> HTTP/1.1\r',.....]
def validate_http_request(request):
    headers = request.split("\n")
    h0 = headers[0]
    idx_end_of_resource = h0.find("HTTP") - 1
    regular_exp_valid_get_h0 = "^GET.*HTTP\/1\.1\r$"
    valid = re.search(regular_exp_valid_get_h0, h0)
    return valid is not None, h0[4:idx_end_of_resource]


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP,
    calls function to handle the requests """
    print('Client connected')  # TODO  ?
    client_socket.send(FIXED_RESPONSE.encode())  # TODO ?
    while True:
        # Get the client request
        client_request = client_socket.recv(1024).decode()
        # print(request)
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            break

    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
