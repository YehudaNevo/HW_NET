import re
import socket

IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 0.1
FIXED_RESPONSE = ""
dic_of_redirection_urls = {'/yehuda': '/index.html'}


#  return the content type to the http response header  , in case of error return empty str ""
def get_filetype(f):
    if f == 'txt' or f == 'html':
        return 'text/html; charset=utf-8'
    elif f in ['jpg', 'ico', 'gif']:
        return 'image/jpeg'
    elif f == 'js':
        return 'text/javascript; charset=UTF-8'
    elif f == 'css':
        return 'text/css'
    else:
        print("Debug: file type unrecognized " + f)
        return ""


def return_area(resource, client_socket):
    numbers = re.findall(r'\d+', resource)
    result = str(float(numbers[0]) * float(numbers[1]) / 2)
    response = 'HTTP/1.0 200 OK\r\n\n' + result
    client_socket.send(response.encode())
    return


#  send the content encoded  to client
def handle_client_request(resource, client_socket):
    code = "200"
    #  for redirection urls
    if resource in dic_of_redirection_urls.keys():
        resource = dic_of_redirection_urls[resource]
        code = "302"
    if resource == '/':
        resource = '/index.html'
    try:
        if re.match("\/calculate-area\?height=(\d+)&width=(\d+)", resource):
            return_area(resource, client_socket)
            return

        filetype = resource.split('.')[-1]
        if filetype not in ['jpg', 'ico', 'gif']:
            fin = open("webroot" + resource, encoding="utf8", errors='ignore')
            content = fin.read()
            fin.close()
        else:
            with open('webroot' + resource, 'rb') as file_handle:
                content = file_handle.read()
        size = len(content)
        response = 'HTTP/1.0 ' + code + ' OK\r\n'
        response += "Content-Type: " + get_filetype(filetype) + '\r\n'
        response += "Content-Length: " + str(size) + '\r\n\n'
        response = response.encode()
        if filetype not in ['jpg', 'ico', 'gif']:  # its not byte content yet ...
            content = content.encode()
        response += content
    except FileNotFoundError:
        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'.encode()
    client_socket.send(response)


#  return if valid or not, and the  resource asked
def validate_http_request(request):
    headers = request.split("\n")
    h0 = headers[0]
    idx_end_of_resource = h0.find("HTTP") - 1
    regular_exp_valid = "^GET.*HTTP\/1\.1\r$"
    valid = re.search(regular_exp_valid, h0)
    return valid is not None, h0[4:idx_end_of_resource]


def handle_client(client_socket):
    print('Client connected')
    client_socket.send(FIXED_RESPONSE.encode())
    while True:
        # Get the client request
        client_request = client_socket.recv(1024).decode()
        # print(request)
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            handle_client_request(resource, client_socket)
            break
        else:
            break
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
